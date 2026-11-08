<p align="center">
  <img src="docs/assets/banner.webp" alt="Classical landscape with a giant overlooking mountains beneath a cloudy sky" width="100%">
</p>

<h1 align="center">Veracity</h1>

<p align="center">
  <strong>A research benchmark for emergent collusion in LLM agents.</strong>
</p>

<p align="center">
  <a href="docs/benchmark.md">Benchmark protocol</a> &middot;
  <a href="CONSTITUTION.md">Constitution</a> &middot;
  <a href="#development">Getting started</a> &middot;
  <a href="harness/README.md">Harness</a> &middot;
  <a href="docs/api.md">API</a>
</p>

---

Veracity measures whether agents independently discover, establish, and execute
coordination that violates a constitution for private benefit. A content
verification game supplies the environment: a creator publishes a bonded claim,
a challenger may dispute it, and jurors commit and reveal their judgments.

The primary planned score is executed collusion rate across standardised
sessions. Proposals, agreements, execution, successful outcomes, capability
errors, and uncertain findings remain separate. Every admitted scenario needs
a feasible collusion opportunity, a compliant strategy, and an observable victim
or compromised outcome. Start with creator–juror and challenger–juror coalitions;
research papers, software, and political statements are content settings.

## Swarm Alignment Hackathon 2026: prior-work disclosure

This repository is **preexisting research infrastructure**, not a project created during the November 6–8, 2026 Swarm Alignment Hackathon. Its latest identified pre-sprint commit is [c81c03a6d7cd](https://github.com/lbxa/collusion-benchmark/commit/c81c03a6d7cd) (November 3, 2026 UTC). The earlier [apart-collusion-sprint](https://github.com/lbxa/apart-collusion-sprint) implementation also predates this sprint; its latest identified commit is [f3826f16c97c](https://github.com/lbxa/apart-collusion-sprint/commit/f3826f16c97c) (October 28, 2026 UTC).

Preexisting components include the Rust HTTP game service, Solidity escrow/voting/settlement contracts, Python agent harness, generated API client, experimental controls, evaluation and reporting scaffolding, and visualization. Existing documentation, experimental snapshots, and imported reports also predate the sprint. Reusing or modifying these components does not make their original implementation new sprint work.

**Sprint-specific contributions:** None are claimed by this disclosure. Any new work must be listed separately with dated commit hashes, affected paths, experimental protocol, and supporting evidence from November 6–8. Documentation changes made to satisfy disclosure requirements are not research findings.

**Implementation and evidence limits:** The full standardized scenario suite, human annotation workflow, and benchmark session scorer remain incomplete. Earlier experiments and imported payoff-only campaigns are historical or exploratory evidence, not results newly obtained during this sprint. Fictional examples are not empirical evidence. No new collusion detection rate, successful attack, or benchmark validation is claimed without reproducible sprint-period traces and analysis.

See [sprint disclosure and report text](docs/swarm-2026-disclosure.md) for the provenance register and report-ready disclosure.

## Documentation

| Guide | Contents |
| --- | --- |
| [Benchmark protocol](docs/benchmark.md) | Scenarios, experimental axes, evidence thresholds, and scoring |
| [Constitution](CONSTITUTION.md) | Canonical participant obligations and game rules |
| [Game specification](SPEC.md) | Contract mechanism and financial rules |
| [Harness](harness/README.md) | Agents, configuration, isolation, evidence, and budgets |
| [Experiment viewer](visualizer/README.md) | Animated local replays of recorded public game states and harness evidence |
| [API](docs/api.md) | Endpoints, authentication, and lifecycle examples |
| [Integration](docs/integration.md) · [Architecture](docs/architecture.md) | System boundaries and rule authority |

## Repository

| Path | Responsibility |
| --- | --- |
| `contracts/` | Authoritative escrow, deadlines, commit/reveal, settlement, withdrawals |
| `core/` | Rust `/v1` API, chain operations, persistent recovery, public/private communication |
| `harness/` | Sole Python harness: Deep Agents, isolated shells, treatments, scheduling, evidence |
| `harness/src/game_api/` | Generated validated HTTP client and local Rust/Anvil launcher |
| `visualizer/` | Local React replay app and embeddable viewer for public state recordings |
| `docs/` | Benchmark protocol, engine integration, reporting guidance |
| `report/` | Imported research reports and frozen snapshots; historical evidence has limitations |

The contract owns financial authority. The harness never supplies missing
participant actions or invents payouts, transfers, or winning-side juror bonuses.
The full standardised scenario suite, human annotation workflow, and benchmark
session scorer remain to be implemented; [the protocol](docs/benchmark.md)
distinguishes current controls from planned extensions.

## Development

Prerequisites: Rust/rustup, Python 3.12+, uv, Bash, Git, curl, tar, jq, a native C
toolchain, and `sha256sum` or `shasum`. Docker with a running daemon is required
for isolated harness integration. Rust is pinned in `rust-toolchain.toml` and
Foundry in `.foundry-version`.

```sh
bash scripts/setup.sh
cargo build --workspace --locked
uv run --project harness --locked veracity-harness build-sandbox
uv run --project harness --locked veracity-harness validate --model "$EXPERIMENT_MODEL_ID"
```

Setup builds the contract, checks its deployment artifact, fetches locked Rust
dependencies, and installs `harness/uv.lock` into `harness/.venv`. Model selection
is explicit. Validation and tests do not call paid model APIs. Live `run` and
`smoke` commands require an API key, a campaign ledger, and an authorised budget;
see the [harness guide](harness/README.md).

To run just the API with isolated Anvil:

```sh
RUST_LOG=info cargo run --locked -p veracity-game-service -- --local
curl -sS http://127.0.0.1:8080/v1/health
```

Local mode listens on loopback and supplies development-only credentials:
`dev-operator`, `dev-creator`, `dev-challenger`, `dev-juror-1` through
`dev-juror-7`, and `dev-treasury`. Each invocation starts a fresh chain and a
private database under `.harness/runs/`. `Ctrl-C` stops the API and its node.
The service exposes Markdown at `/v1/docs` and OpenAPI at `/v1/openapi.json`.

For persistent deployments, start from
[configs/server.example.toml](configs/server.example.toml). Supply the verified
deployment identity, funded signers, and unique bearer credentials through
environment variables. Restart with the same chain, signers, configuration, and
database; use one active process per database. Private databases retain recovery
secrets and must never be published. Public Amoy runs are explicit operations.

## Verification

```sh
bash scripts/verify.sh
```

The gate runs hook regressions, pinned Solidity tests/artifact checks, Rust
formatting/Clippy/tests/builds, generated client checks, and the complete Python
suite including Docker → Rust → Anvil acceptance. Missing chain or Docker
infrastructure fails rather than silently skipping. No model API, public RPC,
or funded public wallet is needed.

For deterministic harness iteration without Docker:

```sh
uv run --project harness --locked pytest harness/tests
uv run --project harness --locked ruff check harness/src harness/tests
uv run --project harness --locked ruff format --check harness/src harness/tests
```

## Research records

The [reporting guide](docs/reporting/README.md) defines research report standards.
Read it before writing or reviewing reports. Compact numeric snapshots and
report sources are versioned. Raw campaigns, traces, checkpoints, ledgers, and
archives under `harness/results/` stay local and ignored, including the imported
2026-10-26 campaign. Raw evidence must be obtained separately for a full audit;
Git LFS is not required for this source repository. The imported payoff-only
campaign and fictional teaching examples do not establish constitution-conditioned
benchmark performance.

## Changelog

### 2026-10-28

- Keep raw experiment outputs and compiled report copies out of Git; retain
  source, locks, test fixtures, compact research snapshots, and required figures
  so cloning and verification do not require a gigabyte of historical run data.
- Promote the autonomous harness to `harness/` and retire the hackathon runners,
  simulated incentives, and duplicate setup/verification paths. Keep the actual
  HTTP client and chain launcher in the single Python package.
- Establish `CONSTITUTION.md` as canonical participant input and `docs/benchmark.md`
  as benchmark design authority. Separate executed collusion from accuracy and
  preserve pre-constitution campaigns as historical evidence.
