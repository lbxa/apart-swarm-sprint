# Swarm-scale summaries preserve every treatment cell

- **Date:** 2026-11-08
- **Status:** Accepted
- **Deciders:** Lucas
- **Area:** harness, benchmark

## Context

The campaign requires results per model and arm. The existing swarm analyzer
reduced experiment names to their last word, pooling jury sizes 3, 7 and 15 and
the principles and contagion contrasts into one collusion cell. That pooling
would hide the comparisons defined in the
[campaign design](swarm-scale-replicates-canonical-peer-across-jury-sizes.md),
including the distinction between paid coordination against the truth and a
violation of an explicit truth duty.

## Decision

Keep the complete size and contrast label after `swarm-scale-` when grouping
retained evidence. Strip only the final `-peers` suffix. Preserve the existing
labels for the earlier `swarm` and `swarm7` campaigns.

## Consequences

The [analyzer](../../harness/research/swarm/analyze.py) reports nine distinct
swarm-scale cells, such as `n3-collusion`, `n15-honest`, and
`n3-principles-collusion`. Its vote, non-vote, execution-failure, and interval
calculations remain unchanged. The historical pooled `peer_effect` field is
not emitted for swarm-scale cells; a cross-size or cross-charter pooled effect
would not answer the campaign's question. Consumers must select the full cell
label when reading these summaries.
