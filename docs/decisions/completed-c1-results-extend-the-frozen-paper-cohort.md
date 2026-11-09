# Completed C1 results extend the frozen paper cohort

- **Date:** 2026-11-09
- **Status:** Accepted
- **Deciders:** Lucas
- **Area:** harness, benchmark, report

## Context

The manuscript freezes cloud evidence at 2026-11-09 05:53 UTC, including 24
C1 runs and a separate C2 cohort. The completed C1 campaign contains 57 runs,
and all 24 earlier C1 run IDs appear in that completed packet. Treating the
completion as an additional cohort would double-count observations. Repeated
launch-seed labels across checkout cohorts also do not create distinct seeds.

The user requested a verified main-branch handoff so Stefan can continue.
The existing frozen manuscript has an audited source registry and reviewed
counts; replacing its inputs requires a new cutoff and claim review.

## Decision

Commit the completed C1 aggregate results, case counts and immutable cloud
artifact register as a separate completion packet. Preserve the manuscript's
explicit frozen cutoff until its source registry and claims are refrozen.

## Consequences

The [handoff](../../harness/research/swarm-scale/RESULTS-C1.md) covers every
planned C1 assignment once, including both played failures. A manuscript
update must extend or replace its partial C1 registry, rather than add the
57-run completion to its earlier 24 runs. Credentials, private trajectories,
agent databases and raw operator-ledger request rows stay outside this source
handoff; the source packet carries public outcome counts, budget totals and
cloud artifact identities needed to reproduce the analysis without model calls.
