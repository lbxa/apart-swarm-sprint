# Veracity experiment viewer

A local, embeddable replay viewer for the game service's recorded public states.
The interface follows [Veracity](https://veracity.lbxa.net): warm white, quiet
typography, black rules, and restrained accents for participant roles.

## Run locally

Requires Node 22.12+ and npm. From the repository root:

```sh
npm --prefix visualizer ci
npm --prefix visualizer run dev
```

Open the localhost URL printed by Vite, then choose **Open experiment**. Files
are parsed in your browser, with no API keys, uploads, or external requests.
Fonts are bundled locally (DM Sans and IBM Plex Mono, distributed under the SIL
Open Font License by Fontsource). Playback supports pause, step, first/last,
speed selection, and keyboard-accessible scrubbing. Player selection filters the
observed activity. Reduced-motion preferences disable decorative animations.

## Input formats

- A public `EpisodeView` returned by `GET /v1/episodes/{episode_id}`.
- An ordered JSON array or JSONL stream of those states.
- A harness episode's `evidence.json` (`episode` plus optional `settlement`).
- A full per-run JSON file from `veracity_harness.export`: every
  `recorded_json["<episode>/evidence.json"]` becomes an episode.
- A named recording containing `name`, optional `run_id`, and `states`. Each
  state can be a public episode or an object with `episode`, optional
  `settlement`, and optional ISO 8601 `recorded_at`.

For example, gather consecutive public responses into this structure:

```ts
const recording = {
  name: 'Invoice reconciliation',
  run_id: 'run-01',
  states: [
    { episode: firstPublicState, recorded_at: '2026-10-31T14:00:00Z' },
    { episode: secondPublicState, recorded_at: '2026-10-31T14:00:05Z' },
  ],
};
```

Snapshots retain input order and are grouped by `episode_id`; no timestamps or
intermediate phases are inferred. The current harness retains terminal evidence,
so its exports usually provide **one snapshot per episode**, not a full replay.
For animations through an entire game, supply snapshots collected during play.
Playback time is a presentation interval, not elapsed experiment time.

The browser limits files to 25 MiB; the adapter accepts at most 10,000 snapshots.
It validates the public projection against the fields in
`core/src/game/types.rs`, with fixtures checked against `docs/openapi.json`.
It ignores unrelated input fields, including private transcripts, traces, and
evaluator annotations. Malformed episodes reject the entire import. Recorded
payouts are displayed verbatim; no outcome is interpreted as evidence of
collusion. Amounts use 18-decimal native units, with exact wei values in
**State data**. A beta label describes the configured bond, not a wallet balance
or proof that a participant has deposited it.

## Embed the package

```sh
npm --prefix visualizer run build
```

The standalone app builds to `visualizer/site/`; the ESM library, CSS, and type
declarations build to `visualizer/dist/`. To use from another local React app,
add `"@veracity/experiment-viewer": "file:../visualizer"` to its dependencies
(adjust the path to your checkout), then install dependencies:

```tsx
import { ExperimentViewer, parseExperiment } from '@veracity/experiment-viewer';
import '@veracity/experiment-viewer/style.css';

const experiment = parseExperiment(recordedJson);
// Pass a new immutable experiment value when loading another recording.
<ExperimentViewer experiment={experiment} />;
```

The library has no demo data or file picker. Only the standalone app starts with
three explicitly illustrative teaching episodes. All CSS uses the `vv-` prefix;
the embedding page's body is only styled when it contains the standalone app.

## Verify

```sh
npm --prefix visualizer test
npm --prefix visualizer run build
```

`build` includes strict TypeScript and formatting checks, the standalone build,
the library build, and declaration emission. `npm run format` formats authored
source. The root Rust/Python verification gate remains separate.

## Architecture contract

- **Boundary and ownership:** this package owns import validation, replay position,
  and presentation. The contract and core retain all rule and financial authority;
  the viewer never sends game actions or computes settlement entitlements.
- **Capability and use cases:** open public episode states or retained harness
  evidence, choose an episode, play or scrub recorded snapshots, inspect players,
  and inspect public evidence and recorded payouts.
- **Change axes and domain:** file adapters may evolve independently of the React
  view. An experiment contains episodes, an episode contains ordered snapshots,
  and each snapshot contains a public `EpisodeView` and optional settlement.
- **Invariants:** imported fields are validated at the adapter boundary; actor and
  configuration identities stay fixed within an episode; committed votes stay
  hidden until revealed; amounts remain decimal strings and use integer
  formatting; missing history stays missing. Tests cover these boundaries.
- **Ports and adapters:** `parseExperiment` accepts untrusted data and returns a
  typed replay. Browser file APIs provide local input; `ExperimentViewer` is the
  embeddable React presentation. There is no service or database adapter.
- **State and orchestration:** playback owns only paused/playing position; recorded
  phases come from core and are never simulated or advanced by the viewer.
- **Failure model:** invalid JSON, unsupported shapes, inconsistent episodes, and
  invalid amounts produce actionable import errors without replacing the current
  experiment. Private transcripts and unrelated fields are excluded at import.
- **Consistency and retries:** imports replace the current experiment atomically.
  There are no external writes, transactions, persistence, or retry workflows.
  Repositories, idempotency machinery, and process managers are unnecessary.
- **Tests:** deterministic adapter and replay tests, TypeScript checks, production
  app/library builds, and desktop/mobile browser verification of the real UI.

## Changelog

### 2026-10-31

- Keep replay separate from protocol execution: recorded snapshots are the only
  source of history, and terminal harness evidence is shown as one snapshot.
- Import public state and settlement only. Operator private transcripts never
  enter the view model or exported snapshots.
