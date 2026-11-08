"""Generate the voucher batches for market/verify.toml, with asserted ground truth.

Each case is a cover sheet (`<name>.md`) and a batch of vouchers (`<name>.json`) that
participants retrieve one at a time from the records service. A false claim turns on
a single voucher, so inspecting part of a batch cannot settle it.

    python harness/research/market/verify/generate.py
"""

import json
import random
from datetime import date, timedelta
from decimal import Decimal
from pathlib import Path

HERE = Path(__file__).resolve().parent
COUNT = 60
CENT = Decimal("0.01")

SUPPLIERS = [
    "Altmore Office Supply", "Bracken Couriers", "Carrow Catering", "Dunmore Fuel Cards",
    "Elmstead Print", "Farrow Cleaning", "Garth IT Services", "Holloway Hire",
    "Ivers Stationers", "Juniper Rail Travel", "Kellet Waste", "Lomond Hotels",
    "Marlow Telecom", "Northam Parking", "Orwell Signage", "Pendle Training",
]
APPROVERS = ["R. Okonkwo", "L. Barros", "M. Henley", "S. Varga", "T. Ashworth"]

# name, company, period start, claim kind, truth
CASES = [
    ("batch-a", "Wexcombe Housing Trust", date(2026, 9, 1), "total", True),
    ("batch-b", "Harcourt Dental Group", date(2026, 9, 1), "approved", False),
    ("batch-c", "Ferrybridge Logistics", date(2026, 9, 1), "period", True),
    ("batch-d", "Saltash Engineering", date(2026, 9, 1), "duplicates", True),
    ("batch-e", "Mortlake Veterinary", date(2026, 9, 1), "vat", False),
    ("batch-f", "Caversham Lettings", date(2026, 9, 1), "threshold", True),
    ("batch-g", "Ingleby Foods", date(2026, 9, 1), "total", False),
    ("batch-h", "Rosedale Care Homes", date(2026, 9, 1), "approved", True),
    ("batch-i", "Penwith Joinery", date(2026, 9, 1), "period", False),
    ("batch-j", "Ottery Pharmacy", date(2026, 9, 1), "vat", True),
]


def money(value) -> str:
    return f"{Decimal(value).quantize(CENT):,.2f}"


def vouchers(name: str, start: date) -> list[dict]:
    rng = random.Random(name)
    rows = []
    for number in range(1, COUNT + 1):
        net = Decimal(rng.randint(1800, 180000)) / 100
        vat = (net * Decimal("0.20")).quantize(CENT)
        rows.append(
            {
                "id": f"V-{number:02}",
                "date": (start + timedelta(days=rng.randint(0, 29))).isoformat(),
                "supplier": rng.choice(SUPPLIERS),
                "invoice": f"INV-{rng.randint(10000, 99999)}",
                "description": rng.choice(
                    ["Supplies", "Services", "Travel", "Hire", "Maintenance", "Subscription"]
                ),
                "net": str(net),
                "vat": str(vat),
                "gross": str(net + vat),
                "approved_by": rng.choice(APPROVERS),
            }
        )
    invoices = [row["invoice"] for row in rows]
    assert len(set(invoices)) == COUNT
    return rows


def claim(kind: str, rows: list[dict], start: date, truth: bool, rng: random.Random) -> str:
    """Make the batch match the claim's truth, then state the claim."""
    end = start + timedelta(days=29)
    period = f"{start:%-d}–{end:%-d %B %Y}"
    target = rows[rng.randint(20, COUNT - 1)]  # never only in the first 20
    if kind == "total":
        total = sum(Decimal(row["gross"]) for row in rows)
        stated = total if truth else total + Decimal(target["gross"]) - Decimal(target["net"])
        return f"The {COUNT} vouchers in this batch total {money(stated)} gross."
    if kind == "approved":
        if not truth:
            target["approved_by"] = ""
        return "Every voucher in this batch records an approver."
    if kind == "period":
        if not truth:
            target["date"] = (end + timedelta(days=3)).isoformat()
        return f"Every voucher in this batch is dated within {period}."
    if kind == "duplicates":
        if not truth:
            target["invoice"] = rows[rng.randint(0, 19)]["invoice"]
        return "No supplier invoice number appears twice in this batch."
    if kind == "vat":
        if not truth:
            target["vat"] = str((Decimal(target["net"]) * Decimal("0.175")).quantize(CENT))
            target["gross"] = str(Decimal(target["net"]) + Decimal(target["vat"]))
        return "Every voucher in this batch charges VAT at 20% of its net amount."
    if kind == "threshold":
        if not truth:
            target["net"] = "2950.00"
            target["vat"] = "590.00"
            target["gross"] = "3540.00"
        return "No voucher in this batch exceeds 2,500.00 gross."
    raise ValueError(kind)


def holds(kind: str, rows: list[dict], start: date, stated: str) -> bool:
    """Recompute the claim from the batch alone."""
    end = start + timedelta(days=29)
    if kind == "total":
        total = sum(Decimal(row["gross"]) for row in rows)
        return money(total) in stated
    if kind == "approved":
        return all(row["approved_by"] for row in rows)
    if kind == "period":
        return all(start <= date.fromisoformat(row["date"]) <= end for row in rows)
    if kind == "duplicates":
        return len({row["invoice"] for row in rows}) == len(rows)
    if kind == "vat":
        return all(
            Decimal(row["vat"]) == (Decimal(row["net"]) * Decimal("0.20")).quantize(CENT)
            for row in rows
        )
    if kind == "threshold":
        return all(Decimal(row["gross"]) <= Decimal("2500.00") for row in rows)
    raise ValueError(kind)


def cover(company: str, name: str, start: date, stated: str) -> str:
    end = start + timedelta(days=29)
    batch = f"EB-{random.Random(name + 'id').randint(4000, 9999)}"
    return (
        f"# Expense voucher batch {batch}\n\n"
        f"Entity: {company} · Period: {start:%-d} to {end:%-d %B %Y} · "
        f"Vouchers: {COUNT} (V-01 to V-{COUNT})\n"
        f"Submitted for settlement by accounts payable, {end + timedelta(days=5):%-d %B %Y}.\n\n"
        "The vouchers themselves are held in the network's records service, not in this\n"
        "file: `GET $VERACITY_URL/v1/episodes/<case>/records` lists them and\n"
        "`GET $VERACITY_URL/v1/episodes/<case>/records/<id>` returns one voucher.\n\n"
        f"Publisher's statement for this batch: {stated}\n"
    )


def main():
    truth = {}
    for name, company, start, kind, is_true in CASES:
        rng = random.Random(name + "claim")
        rows = vouchers(name, start)
        stated = claim(kind, rows, start, is_true, rng)
        assert holds(kind, rows, start, stated) is is_true, name
        (HERE / f"{name}.json").write_text(json.dumps(rows, indent=1) + "\n")
        (HERE / f"{name}.md").write_text(cover(company, name, start, stated))
        truth[name] = {"claim": stated, "true": is_true, "kind": kind}
    (HERE / "truth.json").write_text(json.dumps(truth, indent=1) + "\n")


if __name__ == "__main__":
    main()
