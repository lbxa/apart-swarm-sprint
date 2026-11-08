# Render malformed tool history without executing it

- **Date:** 2026-11-01
- **Status:** Accepted
- **Deciders:** Benchmark owner, through research-design authority delegated in this session
- **Area:** harness, benchmark, research

## Context

A model generated malformed JSON tool arguments during the supplemental quota
condition. The tool runtime correctly rejected the action, but the provider
adapter forwarded the malformed arguments as a structured historical call on
later requests. Those requests received HTTP 400, including in the next case
and awareness probe. The server error body was not retained; offline payload
reconstruction establishes the invalid history, not an independent server
diagnostic. The original session and unknown cost reservations remain evidence.

## Decision

Render malformed historical calls and their tool errors as explicit unexecuted
historical text in the Cloudflare request payload. Keep valid calls and results
unchanged, preserve original recorded messages, and never repair or execute the
malformed arguments. Apply the fix only after the active wave has completed and
uploaded; pass the full gate before dispatching the final planned condition.

## Consequences

The model can observe the prior formatting error and produce a fresh action.
That action is a separate, budgeted model call. There is no automatic paid retry
or replacement session, and earlier failures remain in their assigned cohort.
The adapter changes how invalid history is represented, so the final short-charter
calibration has a conditional recovery difference from the quota condition.
Do not attribute their contrast solely to the charter. Clean histories retain
their previous payloads.

See [the adapter](../../harness/src/veracity_harness/agents.py),
[regressions](../../harness/tests/test_malformed_history.py), and
[campaign protocol](../../harness/research/frontier-2026-10-31/PROTOCOL.md).

## Alternatives considered

Forwarding the malformed structured call can poison later requests. Inventing
valid arguments could misrepresent what the model attempted. Deleting the call
and error would lose context needed to diagnose and correct the failure.
