# Mandated accounts act only after the client filing

- **Date:** 2026-10-31
- **Status:** Accepted
- **Deciders:** Benchmark owner, through delegated error-fixing authority
- **Area:** harness, scheduling

## Context

The full gate caught a challenger filing inside its initial REGISTERED-phase
turn after a concurrent publisher opened the claim, before the required client
filing. The account could therefore replace the client's evidence and bypass
the intended prefiled mandate. A deterministic scheduler regression reproduces
the race, and a real-engine regression checks the actual retained filing.

## Decision

Withhold a mandated account's turns until its client's claim or challenge has
been filed through that account's own sandbox and gateway. Other participants
retain their normal opportunities. This enforces the existing mandate rather
than introducing another participant action or changing financial rules.

## Consequences

The controlled five-model suite uses `mandate = "none"`, so this repair changes
no selected behaviour or participant material in its v3 cells. The baseline wave
finished before applying the repair; later waves use the updated source revision.
All revisions and raw inputs remain recorded for audit.
