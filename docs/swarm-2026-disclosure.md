# Swarm Alignment Hackathon 2026: provenance and research-report disclosure

## Cutoff and sources

Sprint window: November 6–8, 2026. The cutoff is the start of November 6 in the applicable sprint timezone; verify timestamps against the organizer's rules before classifying any borderline commits. The identified benchmark baseline is `c81c03a6d7cd` (2026-11-03 20:54:14 UTC), and the earlier implementation baseline is `f3826f16c97c` (2026-10-28 04:05:02 UTC). Both are pre-sprint.

- https://github.com/lbxa/collusion-benchmark/commit/c81c03a6d7cd
- https://github.com/lbxa/apart-collusion-sprint/commit/f3826f16c97c

## Prior work: paste into the research report

**Prior work and attribution.** This project builds on Veracity, a creator–challenger–juror game and agent-collusion research environment developed before the November 6–8, 2026 Swarm Alignment Hackathon. Preexisting software includes a Rust HTTP game engine, Solidity contracts for escrow and voting, a Python agent harness, API integration, experiment controls, evaluation/reporting infrastructure, and visualization. The benchmark repository had reached commit `c81c03a6d7cd` on November 3, 2026; the earlier `apart-collusion-sprint` repository had reached commit `f3826f16c97c` on October 28, 2026. We reuse these components as prior infrastructure and do not count their original development as hackathon contributions. The standardized scenario suite, human annotation workflow, and benchmark session scorer were incomplete at the start of the sprint. Earlier campaigns, exploratory probes, and fictional reporting examples are not presented as new sprint results. [Insert only verified November 6–8 changes, commit hashes, methods, and results here.]

## Sprint contribution register

| Item | Before November 6 | New during November 6–8 | Evidence |
| --- | --- | --- | --- |
| Rust/Solidity game, settlement, HTTP API | Yes | No claim | Pre-sprint baselines above |
| Python harness, agent orchestration, evaluation scaffolding | Yes | No claim | Pre-sprint baselines above |
| Viewer and report infrastructure | Yes | No claim | Pre-sprint baseline |
| Standardized scenario suite | Incomplete | Not yet established | Require code diff and validation |
| Human annotation workflow | Incomplete | Not yet established | Require code diff and validation |
| Benchmark session scorer | Incomplete | Not yet established | Require code diff and validation |
| New sprint experiments | Earlier campaigns remain preexisting evidence | November principles campaign and source-compatible swarm-scale sessions verified at the report cutoff | `report/data/swarm-summary.json`; `report/data/swarm-track-snapshot.json`; current report's source audit and frozen cloud registry |
| Disclosure documentation | No | Documentation only | This file and README |
| Multi-juror scripted peers (`peer_offers`) and swarm peer-pressure arms | No | Yes: config, runner scheduling, observers, tests | `harness/research/swarm/`, decision record of 2026-11-08 |
| Juries of up to 15 (contract, engine, harness, charter text) | No (3–7 only) | Yes | `contracts/src/Veracity.sol`, `core/src/game/validation.rs`, decision record of 2026-11-08 |
| Swarm scorer and figure | No | Yes: case-clustered resistance, capture rate, chart | `harness/research/swarm/analyze.py`, `report/analysis/swarm_figure.py` |
| Swarm-scale replication of canonical-peer across jury sizes | No | Yes: configs, run plan, campaign options, payment-funding and mandate tests | `harness/research/swarm-scale/`, decision record of 2026-11-09 |

## Results classification

- **Pre-sprint:** pilot data, historical reports, earlier model campaigns, and imported snapshots. Attribute to their original dates and protocols.
- **Illustrative:** fictional examples and synthetic teaching tables. Never report as observations.
- **Proposed:** new scenarios, hypotheses, planned metrics, or incomplete scoring. Never describe as executed or validated.
- **Sprint results:** only completed November 6–8 experiments with recorded code revision, configuration, sample counts, reproducible artifacts, and explicit failure/uncertainty handling.

## Limitations and Dual-Use / Ethical Considerations (mandatory appendix draft)

The current benchmark does not yet implement its complete standardized scenario suite, human annotation workflow, or session-level scorer. Results from earlier campaigns may use different constitutions, incentive rules, model configurations, or measurement definitions and are not directly comparable without revalidation. Small or exploratory samples cannot establish general collusion prevalence. Model outputs and automatic judgments can misclassify intent, coordination, or rule violations. Reproducibility depends on access to run configurations, traces, model versions, and the underlying game state.

The environment models private coordination, inducements, and manipulation of collective judgments. Such mechanisms can be misused to study how to compromise real-world review or governance systems. Experiments should use sandboxed fictional claims, simulated stakes, test wallets, limited tool permissions, and controlled access to sensitive traces. Report detection failures and uncertainty without providing operational instructions for exploiting real systems. Review any additional sprint-specific risks before submission.

## Submission checks

The main report must be 4–8 pages, with eight pages a hard cap excluding references and appendices. Include the mandatory Limitations and Dual-Use / Ethical Considerations appendix. Deadline: November 8, 2026, 11:59 PM Anywhere on Earth (November 9, 6:59 AM EST). Verify final artifacts and provenance before submission.
