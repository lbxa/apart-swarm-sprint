import importlib.util
import json
from pathlib import Path

REPO = Path(__file__).resolve().parents[3]
spec = importlib.util.spec_from_file_location(
    "swarm_track_snapshot", REPO / "report/analysis/swarm_track_snapshot.py"
)
snapshot = importlib.util.module_from_spec(spec)
spec.loader.exec_module(snapshot)


def test_completed_c1_table_preserves_the_completed_cohort_counts(tmp_path):
    data = json.loads((REPO / "report/data/swarm-track-snapshot.json").read_text())
    data["cohorts"]["C1"] = json.loads(
        (REPO / "harness/research/swarm-scale/summary-c1.json").read_text()
    )

    snapshot.tables(data, tmp_path)

    table = (tmp_path / "swarm-c1-completion.tex").read_text()
    rows = [line for line in table.splitlines() if " & " in line][1:]
    assert rows == [
        r"Kimi K2.6 & 21 & 23 & 29 & 20 & 0 & 11 & 0 \\",
        r"Kimi K2.7 Code & 21 & 22 & 20 & 30 & 0 & 9 & 2 \\",
        r"DeepSeek V4 Pro & 21 & 0 & 28 & 44 & 0 & 0 & 0 \\",
    ]
    numbers = (tmp_path / "swarm-snapshot-numbers.tex").read_text()
    assert r"\newcommand{\SnapshotCOneSessions}{57}" in numbers
    assert r"\newcommand{\SnapshotCOneCases}{63}" in numbers
    assert r"\newcommand{\SnapshotCOneFalse}{45}" in numbers
    assert r"\newcommand{\SnapshotCOneTruthful}{77}" in numbers
    size_table = (tmp_path / "swarm-c1-scale-counts.tex").read_text()
    assert r"Kimi K2.6 & 3 / colluding & 3 & 4 & 0 & 2 & 0 & 2 & 0 \\" in size_table
    assert r" & 7 / colluding & 3 & 1 & 0 & 11 & 0 & 1 & 0 \\" in size_table


def test_registry_extends_c1_once_and_preserves_the_c2_cohort():
    data = json.loads((REPO / "report/data/swarm-track-snapshot.json").read_text())
    completed = json.loads(
        (REPO / "harness/research/swarm-scale/cloud-sessions-c1.json").read_text()
    )

    sources = data["sources"]
    assert len(sources) == len({s["run_id"] for s in sources}) == 104
    assert (
        len(data["cases"])
        == len({(case["run_id"], case["episode_id"]) for case in data["cases"]})
        == 116
    )
    assert sum(s["status"] == "failed" for s in sources) == 8
    assert {s["run_id"] for s in sources if s["cohort"] == "C1"} == {
        s["run_id"] for s in completed["sessions"]
    }
    assert data["cohorts"]["C1"] == json.loads(
        (REPO / "harness/research/swarm-scale/summary-c1.json").read_text()
    )
    c2_cases = [case for case in data["cases"] if case["cohort"] == "C2"]
    assert sum(s["cohort"] == "C2" for s in sources) == 47
    assert len(c2_cases) == 53
    assert [
        sum(case[key] for case in c2_cases)
        for key in ("false", "truthful", "abstained", "unrevealed")
    ] == [52, 65, 55, 1]
