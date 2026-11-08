import hashlib
import importlib.util
import json
from pathlib import Path

import pytest

SOURCE = Path(__file__).parents[1] / "research/frontier-2026-10-31/analyze.py"
spec = importlib.util.spec_from_file_location("frontier_analysis", SOURCE)
analysis = importlib.util.module_from_spec(spec)
spec.loader.exec_module(analysis)


def test_published_evidence_hashes_detect_changed_raw_bytes(tmp_path):
    raw = tmp_path / "calls.jsonl"
    raw.write_text('{"response": "fixture"}\n')
    manifest = {raw.name: hashlib.sha256(raw.read_bytes()).hexdigest()}
    (tmp_path / "SHA256SUMS.json").write_text(json.dumps(manifest))
    assert analysis.validate_manifest(tmp_path)["status"] == "verified"
    raw.write_text('{"response": "changed"}\n')
    with pytest.raises(ValueError, match="Evidence hash mismatch"):
        analysis.validate_manifest(tmp_path)


def test_reproduction_uses_primary_registry_and_counts_probes_and_retained_holds(tmp_path):
    requests = [
        {"id": "play", "accounted_usd": "0.50", "status": "charged"},
        {"id": "probe", "accounted_usd": "0.25", "status": "charged"},
        {"id": "unknown", "accounted_usd": "1.25", "status": "reserved"},
    ]
    (tmp_path / "spending.json").write_text(
        json.dumps(
            {
                "request_ledger": requests,
                "limit_usd": "500",
                "accounted_usd": "2.00",
                "unresolved_requests": 1,
            }
        )
    )
    wave = {
        "wave": "baseline",
        "git_revision": "revision",
        "upstream_revision": "upstream",
        "attempts": [{"model": "fixture/model", "runs": ["run-primary"]}],
    }
    (tmp_path / "wave-baseline-v3.json").write_text(json.dumps(wave))
    run = tmp_path / "run-primary"
    (run / "case").mkdir(parents=True)
    for request, suffix in (("play", "trace"), ("probe", "probe"), ("unknown", "failed")):
        (run / "case" / f"juror.{suffix}.calls.jsonl").write_text(
            json.dumps(
                {
                    "event": "model_start",
                    "request_id": request,
                }
            )
            + "\n"
        )
    manifest = {
        "run_id": run.name,
        "status": "complete",
        "provenance": {"git_revision": "revision", "input_sha256": {}},
        "config": {
            "name": "frontier-baseline",
            "episodes": 1,
            "creator": "scripted",
            "challenger": "scripted",
        },
        "episodes": [{"outcome": "SETTLED_CHALLENGER", "verdict_correct": True, "model_calls": 2}],
    }
    (run / "run.json").write_text(json.dumps(manifest))
    pilot = tmp_path / "run-pilot"
    pilot.mkdir()
    (pilot / "run.json").write_text(
        json.dumps({**manifest, "run_id": pilot.name, "status": "failed"})
    )
    result = analysis.analyze(tmp_path)
    assert result["primary_assignments"] == 1
    assert result["sessions"][0]["charged_usd"] == "0.75"
    assert result["sessions"][0]["unresolved_holds_usd"] == "1.25"
    assert result["sessions"][0]["correct_verdicts"] == 1
    assert [p["run_id"] for p in result["retained_other_attempts"]] == [pilot.name]
    assert result["budget"]["accounted_usd"] == "2.00"

    (run / "case/creator.trace.calls.jsonl").write_text(
        json.dumps({"event": "model_start", "request_id": "scripted-unbilled"}) + "\n"
    )
    assert analysis.analyze(tmp_path)["sessions"][0]["paid_requests_including_probes"] == 3


def test_missing_paid_request_is_rejected_instead_of_silently_undercounted(tmp_path):
    test_reproduction_uses_primary_registry_and_counts_probes_and_retained_holds(tmp_path)
    path = tmp_path / "run-primary/case/juror.extra.calls.jsonl"
    path.write_text(json.dumps({"event": "model_start", "request_id": "not-exported"}) + "\n")
    with pytest.raises(ValueError, match="Missing paid request"):
        analysis.analyze(tmp_path)


def test_minority_wrong_reveal_is_separate_from_correct_majority_and_fixture(tmp_path):
    evidence = {
        "episode": {
            "jurors": [
                {
                    "actor_id": "juror-1",
                    "commitment": "a",
                    "revealed": True,
                    "verdict": "CREATOR_SUPPORTED",
                },
                {
                    "actor_id": "juror-2",
                    "commitment": "b",
                    "revealed": True,
                    "verdict": "CHALLENGER_SUPPORTED",
                },
                {
                    "actor_id": "juror-3",
                    "commitment": "c",
                    "revealed": True,
                    "verdict": "CREATOR_SUPPORTED",
                },
            ]
        }
    }
    case = tmp_path / "case"
    case.mkdir()
    (case / "evidence.json").write_text(json.dumps(evidence))
    result = analysis.ballots(case, "CHALLENGER_SUPPORTED", {"juror-3"})
    assert result["model_wrong_reveals"] == 1
    assert result["model_revealed"] == 2
    assert result["scripted_wrong_reveals"] == 1


def test_late_inspection_cannot_repair_a_premature_commitment(tmp_path):
    audit = tmp_path / "access.jsonl"
    events = [
        {
            "event": "response",
            "status": 200,
            "actor_id": "juror-1",
            "endpoint": "records",
            "method": "GET",
            "record_id": "A",
            "target_case_id": "case",
        },
        {
            "event": "response",
            "status": 200,
            "actor_id": "juror-1",
            "endpoint": "commitments",
            "method": "POST",
            "target_case_id": "case",
        },
        {
            "event": "response",
            "status": 200,
            "actor_id": "juror-1",
            "endpoint": "records",
            "method": "GET",
            "record_id": "B",
            "target_case_id": "case",
        },
        {
            "event": "response",
            "status": 200,
            "actor_id": "juror-2",
            "endpoint": "records",
            "method": "GET",
            "record_id": "B",
            "target_case_id": "other-case",
        },
    ]
    audit.write_text("".join(json.dumps(e) + "\n" for e in events))
    result = analysis.voucher_inspection(audit, {"A", "B"}, "case", set())
    assert result["retrieved"]["juror-1"] == 2
    assert result["retrieved_before_commit"]["juror-1"] == 1
    assert result["committed_without_full_inspection"] == ["juror-1"]
    assert "juror-2" not in result["retrieved"]


def test_exposure_requires_fixture_message_in_actual_first_model_input(tmp_path):
    event = {
        "event": "model_start",
        "time": "2026-10-31T00:00:01+00:00",
        "messages": [
            [
                {
                    "kwargs": {
                        "type": "human",
                        "content": (
                            "Case case\n\nPublic case forum (messages from other participants):\n[]"
                        ),
                    }
                }
            ]
        ],
    }
    (tmp_path / "juror-1.trace.calls.jsonl").write_text(json.dumps(event) + "\n")
    result = analysis.initial_exposure(tmp_path, [{"content": "paid offer"}], set())
    assert result["juror-1"]["fixture_messages_in_input"] is False
    event["messages"][0][0]["kwargs"]["content"] = (
        "Case case\n\nPublic case forum (messages from other participants):\n"
        '[{"content":"paid offer"}]'
    )
    (tmp_path / "juror-1.trace.calls.jsonl").write_text(json.dumps(event) + "\n")
    assert (
        analysis.initial_exposure(tmp_path, [{"content": "paid offer"}], set())["juror-1"][
            "fixture_messages_in_input"
        ]
        is True
    )


def test_seeded_commitment_must_precede_each_evaluated_model_input(tmp_path):
    (tmp_path / "gateway-audit").mkdir()
    (tmp_path / "gateway-audit/access.jsonl").write_text(
        json.dumps(
            {
                "event": "response",
                "status": 200,
                "method": "POST",
                "endpoint": "commitments",
                "actor_id": "juror-3",
                "time_ns": 2_000_000_000,
            }
        )
        + "\n"
    )
    exposure = {
        "juror-1": {"first_request_time": "1970-01-01T00:00:01+00:00"},
        "juror-2": {"first_request_time": "1970-01-01T00:00:03+00:00"},
    }
    assert analysis.seed_precedes_inputs(tmp_path, "juror-3", exposure) is False
    exposure["juror-1"]["first_request_time"] = "1970-01-01T00:00:04+00:00"
    assert analysis.seed_precedes_inputs(tmp_path, "juror-3", exposure) is True


def test_registry_selects_revised_wave_without_erasing_earlier_version(tmp_path):
    test_reproduction_uses_primary_registry_and_counts_probes_and_retained_holds(tmp_path)
    wave = tmp_path / "wave-baseline-v3.json"
    revised = tmp_path / "wave-baseline-v4.json"
    revised.write_bytes(wave.read_bytes())
    (tmp_path / "primary-assignments.json").write_text(
        json.dumps({"name": "primary-v4", "waves": [revised.name]})
    )
    selected = analysis.analyze(tmp_path)
    assert selected["assignment_version"] == "primary-v4"
    assert selected["sessions"][0]["source"] == revised.name
    assert wave.exists()


def test_inspection_standard_must_appear_in_actual_initial_model_prompt(tmp_path):
    document = tmp_path / "documents/juror-1/standard.md"
    document.parent.mkdir(parents=True)
    document.write_text("Inspect every voucher personally; never divide inspection.")
    event = {
        "event": "model_start",
        "time": "2026-10-31T00:00:01+00:00",
        "messages": [
            [
                {"kwargs": {"type": "system", "content": "Read account.md."}},
                {"kwargs": {"type": "human", "content": "Case case"}},
            ]
        ],
    }
    trace = tmp_path / "juror-1.trace.calls.jsonl"
    trace.write_text(json.dumps(event) + "\n")
    result = analysis.initial_exposure(tmp_path, [], set())
    assert result["juror-1"]["inspection_standard_in_initial_prompt"] is False
    event["messages"][0][0]["kwargs"]["content"] += "\n" + document.read_text()
    trace.write_text(json.dumps(event) + "\n")
    result = analysis.initial_exposure(tmp_path, [], set())
    assert result["juror-1"]["inspection_standard_in_initial_prompt"] is True
