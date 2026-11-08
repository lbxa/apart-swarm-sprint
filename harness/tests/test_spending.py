from concurrent.futures import ThreadPoolExecutor
from decimal import Decimal

import pytest

from veracity_harness.spending import (
    CampaignSpending,
    ModelPrice,
    SpendingLimitReached,
    cloudflare_charge,
    cloudflare_price,
)


def price():
    return ModelPrice(
        id="fixture/model", context_length=1000, pricing={"prompt": "0.001", "completion": "0.01"}
    )


def test_shared_cap_is_durable_and_unknown_charge_keeps_hold(tmp_path):
    path = tmp_path / "spending.sqlite"
    first = CampaignSpending(path, Decimal(3))
    first.reserve("first", price(), 100)
    first.reconcile("first", None)
    other = CampaignSpending(path, Decimal(3))
    with pytest.raises(SpendingLimitReached):
        other.reserve("second", price(), 100)
    first.reconcile("first", Decimal("0.25"))
    other.reserve("second", price(), 100)
    assert Decimal(other.snapshot()["accounted_usd"]) == Decimal("2.25")
    assert other.snapshot()["unresolved_requests"] == 1
    with pytest.raises(ValueError, match="original campaign cap"):
        CampaignSpending(path, Decimal(100))


def test_concurrent_requests_cannot_oversubscribe_the_cap(tmp_path):
    spending = CampaignSpending(tmp_path / "spending.sqlite", Decimal(3))

    def reserve(index):
        try:
            spending.reserve(str(index), price(), 100)
            return True
        except SpendingLimitReached:
            return False

    with ThreadPoolExecutor(max_workers=8) as pool:
        assert sum(pool.map(reserve, range(8))) == 1
    assert spending.snapshot()["requests"] == 1


def test_ceiling_covers_price_tiers_cache_write_and_reasoning():
    model = ModelPrice(
        id="fixture/tiered",
        context_length=1000,
        pricing={
            "prompt": "0.001",
            "completion": "0.01",
            "internal_reasoning": "0.02",
            "overrides": [{"input_cache_write_1h": "0.004", "completion": "0.03"}],
        },
    )
    assert model.request_ceiling(100) == Decimal(9)


def test_catalog_drift_stops_further_spending(tmp_path):
    spending = CampaignSpending(tmp_path / "spending.sqlite", Decimal(100))
    spending.reserve("first", price(), 100)
    with pytest.raises(SpendingLimitReached, match="exceeded"):
        spending.reconcile("first", Decimal("3.1"))
    with pytest.raises(SpendingLimitReached):
        spending.reserve("next", price(), 100)


def test_cloudflare_catalog_entry_becomes_per_token_ceiling_rates():
    entry = {
        "name": "@cf/deepseek-ai/deepseek-v4.1-flash-1017",
        "properties": [
            {"property_id": "context_window", "value": "1048576"},
            {
                "property_id": "price",
                "value": [
                    {"unit": "per M input tokens", "price": 0.3, "currency": "USD"},
                    {"unit": "per M output tokens", "price": 1.2, "currency": "USD"},
                    {"unit": "per M cached input tokens", "price": 0.006, "currency": "USD"},
                ],
            },
        ],
    }
    price = cloudflare_price(entry)
    assert price.id == "@cf/deepseek-ai/deepseek-v4.1-flash-1017"
    assert price.context_length == 1048576
    assert price.maximum_rates["prompt"] == Decimal("0.0000003")
    assert price.maximum_rates["completion"] == Decimal("0.0000012")


def test_cloudflare_entry_without_token_prices_is_rejected():
    entry = {"name": "@cf/fixture", "properties": [{"property_id": "context_window", "value": 8}]}
    with pytest.raises(ValueError, match="price"):
        cloudflare_price(entry)


def deepseek_price():
    return ModelPrice(
        id="@cf/fixture",
        context_length=1048576,
        pricing={"prompt": "0.0000003", "completion": "0.0000012"},
    )


def test_cloudflare_neurons_are_charged_when_consistent_with_catalog_token_prices():
    # Live 2026-10-28 observations: uncached and mostly cached requests.
    usage = {"input_tokens": 298, "output_tokens": 63, "input_token_details": {"cache_read": 0}}
    charge = cloudflare_charge(15.000000953674316, usage, deepseek_price())
    assert round(charge, 9) == Decimal("0.000165000")
    cached = {
        "input_tokens": 6304,
        "output_tokens": 97,
        "input_token_details": {"cache_read": 6080},
    }
    assert round(cloudflare_charge(20.007246, cached, deepseek_price()), 6) == Decimal("0.000220")
    # Nemotron billed 0.99x its catalog token price in a live smoke.
    nemotron = ModelPrice(
        id="@cf/nemotron",
        context_length=256000,
        pricing={"prompt": "0.0000005", "completion": "0.0000015"},
    )
    observed = {"input_tokens": 4720, "output_tokens": 79, "input_token_details": {"cache_read": 0}}
    assert cloudflare_charge(223.14, observed, nemotron) is not None


def test_missing_neurons_keep_the_conservative_hold():
    usage = {"input_tokens": 298, "output_tokens": 63}
    assert cloudflare_charge(None, usage, deepseek_price()) is None
    assert cloudflare_charge(15, None, deepseek_price()) is None


@pytest.mark.parametrize("neurons", [0, 1, 40])
def test_neurons_contradicting_catalog_token_prices_stop_spending(neurons):
    usage = {"input_tokens": 298, "output_tokens": 63, "input_token_details": {"cache_read": 0}}
    with pytest.raises(SpendingLimitReached, match="contradict"):
        cloudflare_charge(neurons, usage, deepseek_price())
