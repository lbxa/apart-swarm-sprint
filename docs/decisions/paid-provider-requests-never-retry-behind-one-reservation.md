# Paid provider requests never retry behind one reservation

- **Date:** 2026-10-31
- **Status:** Accepted
- **Deciders:** Benchmark owner, through the explicit USD 500 cap and delegated fixes
- **Area:** harness, spending, benchmark evidence

## Context

A model-call reservation covers one provider request. The Cloudflare adapter
could retry timeouts and gateway errors internally, although their billing may
be unknown. Replacing the hold with the final successful charge would not bound
an earlier failed attempt. The campaign must remain under its immutable cap.

Inspection also found two observer errors: per-session W&B costs omitted
post-session probe calls, and pooled coverage excluded the scripted peer's
records even though that peer participates in the coalition.

## Decision

Disable SDK and adapter retries in participant execution. An unsuccessful
attempt retains its full hold; an explicitly recorded rerun gets new request
identities under the same ledger. Direct adapter tests retain an opt-in retry
setting, while `ParticipantAgent` always selects zero retries.

Include probe requests in charged and hold-inclusive session cost totals, and
keep probe raw calls under the same export opt-in as play calls. Measure
collective coverage across all jurors, while counting model inspection and
commitment outcomes only for evaluated jurors. Coverage alone is not a
coordination label.

## Consequences

Transient failures can end a model turn instead of silently restarting a paid
request. This favours auditable spending over automatic recovery. Existing
completed baseline responses reported no capacity retries; retain their source
revision and account for every probe when updating derived W&B summaries.
The canonical participant materials are unchanged by these observer fixes.

See `harness/src/veracity_harness/agents.py`, `tracking.py`, the observer
regressions, and the real-engine pooling feasibility calibration.

## Alternatives considered

Reserving and reconciling each HTTP retry separately would also work, but needs
attempt-level identities and explicit unknown-charge holds. Disabling retries
is the smaller change for this capped exploratory campaign.
