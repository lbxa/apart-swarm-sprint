# Repository Guidelines

## Project Structure & Module Organization

This repository implements the `SPEC.md` game engine and `/v1` API plus the Python experiment harness in `harness/`. `core/src/` contains `api`, `game`, `chain`, `chat`, `forum`, `store`, and configuration modules. `contracts/` owns Solidity rules, Foundry tests, and the deployment artifact. The harness owns agents, treatments, observations, and metrics; it calls HTTP. Keep financial authority in the contract.

`docs/api.md` is the harness integration guide; `docs/architecture.md` records boundaries. `configs/` and `examples/` contain deployment and request templates. Shared skills live in `.agents/skills/`; `.claude/skills` points there. Agent definitions and hooks live in `.codex/` and `.claude/`.

`docs/private-chat.md` defines the experimental chat API. Prohibited chat is delivered and flagged; membership is enforced. Participant history settings never remove the operator's retained audit transcript. Keep chat bodies out of public game state and logs.

`docs/public-forum.md` defines the core-owned public forum. Assigned episode participants share history; operator transcript/audit access is distinct. The harness publishes and reads public deliberation through HTTP. Keep message bodies out of ordinary logs and metadata audits.

## Build, Test, and Development Commands

- `bash scripts/setup.sh`: install pinned local Foundry, build contracts, and fetch locked dependencies.
- `cargo run -p veracity-game-service -- --local`: start the API with isolated Anvil.
- `bash scripts/verify.sh`: run hooks, Solidity/Rust tests, artifact checks, formatting, Clippy, and builds.
- `cargo build --workspace --locked`: build workspace packages.
- `cargo test --workspace --locked`: run unit, integration, and documentation tests.
- `cargo test -p veracity-game-service`: test the service during iteration.
- `bash scripts/verify-harness.sh`: run Python client/agent regressions and Docker-isolated engine acceptance tests after building Rust.
- `cargo fmt --all`: format Rust sources.
- `cargo clippy --workspace --all-targets --all-features --locked -- -D warnings`: reject lint warnings.

Rust tooling is pinned in `rust-toolchain.toml`; Foundry in `.foundry-version`. Commit `Cargo.lock`, `harness/uv.lock`, and intentional artifact updates. Setup requires uv and creates `harness/.venv`.

## Coding Style & Naming Conventions

Use Rust 2024 and rustfmt's default four-space indentation. Use `snake_case` for modules, functions, and variables; `PascalCase` for types and traits; and `SCREAMING_SNAKE_CASE` for constants. Prefer explicit ownership, typed errors, and narrow module boundaries. Share dependency versions through `[workspace.dependencies]` when needed. Workspace members inherit the unsafe-code prohibition.

## Testing Guidelines

Follow the shared `tdd` skill: witness the intended failure, implement, and expand outward. Rust integration tests live in `core/tests/`, contract tests in `contracts/test/`, and Python pytest regressions in `harness/tests/`. Prove deadlines, conservation, commitments, role boundaries, and recovery with actual Anvil. Default tests require no public networks, funded public wallets, or model APIs. Never skip chain tests silently. No coverage percentage is configured.

## Benchmark authority

`CONSTITUTION.md` is the short canonical participant constitution and game-rule summary.
`docs/benchmark.md` defines scenarios, experimental axes, evidence thresholds, and
session scoring. Measure executed coordination separately from proposals,
agreements, success, and capability errors. Every admitted scenario needs a
feasible collusion opportunity, compliant strategy, and observable victim or
compromised outcome. Keep evaluator labels and coalition plans out of agent inputs.
The sole harness is `harness/`; its `src/game_api/` owns the retained HTTP client.
Historical payoff-only campaigns are not constitution-conditioned benchmark evidence.

## Decision Records

Writing a decision record is part of "done", for every agent and without being
asked. When a change encodes a choice with real trade-offs — a constraint the
code does not show, a rejected alternative, behavior that looks like a bug but
is intended, a parked experiment — add `docs/decisions/<short-statement>.md`
from `docs/decisions/_template.md` in the same change. Use today's date, no
number in the filename, and people (not agents) as deciders. Never invent the
rationale: mark unverified parts `> ⚠️ NEEDS CONFIRMATION (who)`. Records are
append-only; supersede rather than rewrite. Do not edit `docs/decisions/INDEX.md`;
the Stop hook regenerates it and `scripts/verify.sh` rejects a stale one. Small
package facts stay in the package README changelog; see `docs/decisions/README.md`.

## Commit & Pull Request Guidelines

Use focused, imperative subjects such as `Add Cargo verification hooks`. Pull requests should describe behavior, link spec sections or issues, and report verification results and blockers.

## Agent-Specific Instructions

Use Context7 for current dependency and tool documentation: resolve the library ID, then query the full question. Author source and documentation directly with editing tools. Never commit wallet keys, credentials, or private observations. Both Stop hooks share `scripts/agent-hooks/stop-checks.sh`; disclose failures even when a repeated failure permits handoff.

## Research Reports

A LaTeX research report is a main project deliverable. Before planning, drafting,
or reviewing a report, use the [reporting guide and table of contents](docs/reporting/README.md).
Read in this order:

1. [Paper brief](docs/reporting/paper-brief.md): reader, research question, actual evidence, and unresolved claims.
2. [Venue](docs/reporting/venue.md): selected official template and submission rules. Venue requirements take precedence over house formatting.
3. [Writing](docs/reporting/writing.md): argument, mathematical exposition, and reader comprehension.
4. [Visuals](docs/reporting/visuals.md) and [LaTeX](docs/reporting/latex.md): figures, tables, diagrams, notation, and build conventions.
5. [Review](docs/reporting/review.md): evidence, compilation, and rendered-page acceptance checks.

Update the brief as evidence changes. Do not turn historical, mock, scripted, or
heuristic outputs into claims about model behavior on the integrated protocol.
Report completion requires the brief's claim-to-evidence mapping, a reproducible
PDF build, final-size visual inspection, and a recorded review with open gaps.
Source notes and reusable examples are indexed in the reporting guide; consult
them for technical lookup rather than expanding this entry point.
The current sample lives in `report/main.tex`, with prose in `report/sections/`
and shared formatting in `report/preamble.tex`. Build it with `make -C report`.
Its teaching counts remain fictional until replaced with admitted evidence.
