# Recover transient failures within scheduled opportunities

- **Date:** 2026-11-03
- **Status:** Accepted
- **Deciders:** Benchmark owner, through the debugging and research-design authority delegated in this session
- **Area:** harness, benchmark

## Context

The five-model campaign retained three 600-second turn cancellations and one
HTTP 502 opportunity failure. The scheduler disabled the affected participant
for the remaining case, including reveal opportunities after a commitment.
The turn timer also cancelled an in-flight request that had started near the
end of the turn. A commitment is an external effect that survives either error;
the harness must not choose a replacement vote or repeat an uncertain action.
The shared USD 500 cap includes unresolved request holds.

## Decision

Classify timeouts, connection failures, HTTP 408/429 and server errors as
recoverable at remaining scheduled opportunities. Keep every error, the failed
case label, existing deadlines, call limits and monetary holds. Every subsequent
model invocation receives its own ledger reservation; SDK and adapter retries
remain disabled for participants.

Stop starting model invocations when the turn time budget expires, then allow
bounded completion. The hard watchdog is twice the configured turn interval
plus one 60-second rate window and 30 seconds of tool grace. Its expiry still
cancels and records the request. Before a fresh turn, insert explicit error
messages for missing tool results, describing external effects as unknown;
never automatically replay those tools. Preserve prior checkpoints and raw
call evidence. Record this policy as scheduler v2 for future runs.

## Consequences

Recovery consumes existing opportunities and episode call budgets. A provider
outage can still prevent participation, and a participant that misses every
remaining opportunity still cannot reveal. A turn may drain beyond its soft
time budget; continuous scheduling still skips phase reminders after native
deadlines. Historical v1 runs and published results are unchanged.

Cloudflare rate storage is validated before live setup or money reservation.
Honor an explicit shared path strictly; otherwise try the XDG cache, home cache,
then a stable per-user temporary directory. An invalid explicit path, lock
contention or corrupt database fails without creating an independent counter.
Use an explicit shared path for every campaign worker on the host.

See [the error review](../execution-error-review.md),
[agent execution](../../harness/src/veracity_harness/agents.py),
[scheduling](../../harness/src/veracity_harness/runner.py), and
[benchmark authority](../benchmark.md).

## Alternatives considered

Hidden immediate retries obscure paid attempts and uncertain charges. Unlimited
extra opportunities change exposure and case deadlines. Automatically revealing
or replaying a tool substitutes harness choices for participant actions. Clearing
failed labels after recovery hides operational contamination. None is admitted.
