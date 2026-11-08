# Execution error review, 2026-11-03

The retained five-model campaign contains 18 failed or timed-out opportunities:
12 host filesystem errors, three turn cancellations, two invalid-request errors,
and one provider gateway error. Two additional runs failed during Docker startup.
This review fixes future execution; historical results and unresolved spending
holds remain evidence of the original scheduler.

The raw evidence is in `harness/results/frontier-2026-10-31` and the
[published W&B audit](https://forge.coreweave.com/wandb/lbxa-corp/collusion-benchmark/runs/2lkzpteb).
Use `run-*/run.json`, each case's `opportunities.jsonl` and
`<actor>.trace.calls.jsonl`, `failure-review-*.json`, and `operator-logs/*.stderr`.
The call traces contain private participant inputs and provider-returned
reasoning; inspect them in the retained artifact rather than copying them to Git.

| Evidence | Diagnosis | Prevention and recovery |
| --- | --- | --- |
| `run-024a0333cfda`, `run-7d656add1dcc`: 12 `OSError` opportunities | The default rate-limit database used an unwritable home cache. The campaign driver later supplied a writable path, but direct execution retained the faulty default. | Validate the shared SQLite store before catalog access or a paid reservation. Honor `VERACITY_RATE_DB`; default to writable XDG/home/per-user temporary storage. Never silently replace an explicitly configured counter. |
| `run-db9e0164208b/VR-585965`, `run-143b532370d0/VR-526410`, `run-0d97358dc7da/VR-582919`: exactly 600-second cancellations | Total-turn timeout cancelled a later request with only about 43, 129 and 18 seconds left, respectively. The scheduler then disabled the actor for the entire case. | Stop new requests at the soft deadline; allow bounded completion of in-flight work. Record hard cancellations explicitly and retain monetary holds. Recover at remaining scheduled opportunities. |
| `run-557a30e653e6/VR-577434`: HTTP 502 in REVEAL | Upstream gateway failure; later requests succeeded. The same permanent actor-disable rule suppressed later participation. | Classify transient errors separately from invalid/authentication requests. Allow a fresh, budgeted request at the next scheduled opportunity without hidden transport retries. |
| `run-8a3f2a012430`: two failed opportunities and one failed probe, HTTP 400 | Malformed JSON from an earlier generated tool call was sent again as structured history, poisoning subsequent requests. | Existing fix `8e317de` preserves the unexecuted call/error as text in Cloudflare payloads. Its regressions remain. New interrupted-tool recovery marks missing results as unknown and never replays uncertain actions. |
| `run-da060f2973e7`, `run-baee2f2ea5c6`: top-level Docker `APIError` | Original logs retained the exception class only. Exact Docker status and cause are unavailable; no specific cause is established. | Future failure records include stage, exception class, safe numeric HTTP status and errno, without private exception bodies. Catalog rejection now also leaves a run manifest. |

The scheduler recovery policy is versioned as
`concurrent-opportunity-rounds-v2`; see the
[decision record](decisions/recover-transient-failures-within-scheduled-opportunities.md).
Recovered cases still have `agent_execution_failed = true`. Normal deadline
yields are counted separately from errors and call-budget exhaustion. No
additional rounds, default ballots or native financial actions are supplied.
Provider outages and invalid model-generated actions can still occur.
The 95 recorded `budget_exhausted` opportunities are the configured request
limits taking effect. They remain resource-limited outcomes; this repair does
not increase those limits or rewrite invalid participant commands.

## Reproduce the checks

With the pinned environment, Docker, Rust binary and Anvil available:

```sh
uv run --project harness --locked pytest -q \
  harness/tests/test_execution_recovery.py harness/tests/test_ratelimit.py \
  harness/tests/test_scheduling.py harness/tests/test_malformed_history.py
uv run --project harness --locked pytest -q -m '' \
  harness/tests/test_integration.py -k transient_failure_keeps
bash scripts/verify.sh
```

The new tests cover transient HTTP failures, permanent request/authentication
errors, reservations and unresolved holds, request-boundary deadlines, a hung
request's hard cancellation, interrupted tool history, rate-store fallback,
preflight failure, safe startup diagnostics, and local native reveal recovery.
The two Anvil fixtures inject failures after a confirmed commitment or during
REVEAL. They require three native revealed ballots and challenger settlement,
while preserving the failed execution label. They make zero model API calls
and provide no new evidence about model collusion.

Debugging creates no paid requests. The campaign remains at 6,232 requests,
USD 42.561955184278488157441 confirmed charges and
USD 65.957651824278488157441 including 40 unresolved holds, under its USD 500 cap.
