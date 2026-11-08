# Harness and engine integration

`harness/` is the single autonomous experiment harness. `src/game_api/` packages
the retained generated HTTP client and the local Rust/Anvil launcher alongside
`veracity_harness`. Install it with `bash scripts/setup-harness.sh`.

- `CoreClient` uses validated `/v1` models and operation handles. It owns HTTP
  sessions, polling, and typed transport/operation errors. Money remains integer
  base-unit strings; never substitute floating-point or simulated settlement.
- `LocalEngine` owns development credentials, subprocess cleanup, and the
  isolated Anvil clock. The participant gateway exposes neither operator
  endpoints nor chain RPC.
- The harness owns concurrent opportunities, budgets, private workspaces,
  treatment controls, and retained evidence. It never supplies missing strategic
  actions. A failed model or transport is not a verdict or compliant abstention.
- The Rust service persists artifacts, operations, signed transactions, and reveal
  material. Original idempotency keys and request bodies identify uncertain writes;
  the gateway does not retry. Successful operation polling requires confirmed
  receipt evidence, not merely an HTTP success.
- Solidity owns deposits, immutable roles, deadlines, commitments, full-roster
  majorities, refunds, forfeitures, credits, and withdrawals. All valid revealers
  receive equal rewards regardless of their vote. Truth is evaluator-only.
- Core forum/private-chat storage owns membership, pagination, and durable
  transcripts. Gateway controls disable actual routes as well as discovery;
  prohibited-but-accessible private communication is a behavioural treatment.
  Participant history controls never erase operator evidence.
- `CONSTITUTION.md` is snapshotted verbatim and delivered to each participant.
  Evaluator reference labels, scenario opportunities, and reviews are never mounted.

The [API guide](api.md) defines endpoints, auth, units, and settlement. Generate
`docs/openapi.json` and `harness/src/game_api/generated.py` from Rust with
`harness/.venv/bin/python scripts/generate-core-client.py`; `--check` rejects drift.
The generator, HTTP client, lifecycle, and gateway retain deterministic tests.
Full acceptance uses Docker, the real Rust server, and isolated Anvil, without
model APIs, public networks, or funded public wallets.

See [benchmark design](benchmark.md) for evaluation and unsupported extensions,
and [the harness guide](../harness/README.md) for configuration and evidence.
Historical structured-action adapters, simulated bribes, majority bonuses, and
auditor payments are retired and cannot be assumed from old campaign records.
