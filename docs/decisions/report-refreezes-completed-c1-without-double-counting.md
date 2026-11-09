# Report refreezes completed C1 without double-counting

- **Date:** 2026-11-09
- **Status:** Accepted
- **Deciders:** Lucas
- **Area:** report, harness, benchmark

## Context

The previous manuscript admitted 24 C1 sessions and a separate 47-session C2
cohort. The completed C1 campaign has 57 sessions, including all 24 already
admitted C1 run IDs. Its final 33 sessions were available as a completion
handoff, but the paper retained its earlier cutoff. Lucas now requests that
the completed results be embedded in the project report.

## Decision

Supersede the frozen-manuscript choice in
[the completion handoff](completed-c1-results-extend-the-frozen-paper-cohort.md).
Replace the partial C1 selection with all 57 completed C1 sessions, retain the
same 47 C2 sessions and one setup-only exclusion, and regenerate the report
from the resulting immutable artifact registry. Show completed C1 counts in
the main text as well as the combined per-cell results and cloud appendix.

## Consequences

The report admits 104 unique played sessions and 116 unique run/case pairs,
including eight played failures. The 24 overlapping C1 sessions are not added
again. All completed C1 counts must reproduce the committed completion packet;
the C2 counts and earlier source hashes must remain unchanged. The two
checkout cohorts remain provenance strata rather than randomized treatments,
and repeated seed labels do not create additional distinct seeds.

The current manuscript keeps Lucas Barbosa and Stefan Gazana as its authors.
This update changes the evidence registry, tables, claims and PDF; it performs
no new model calls. Earlier snapshot bytes remain available in Git history.
