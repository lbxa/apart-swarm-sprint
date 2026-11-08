# Agentic dispute-game case studies

This manuscript describes the 2026-10-26 neutral-prompt Deep Agents campaign.
Its evidence is separate from the older structured-action harness reports.
The [paper brief](../../docs/reporting/paper-brief.md) records A0–A3 and the
claim-to-evidence mapping; [review.md](review.md) records acceptance checks and
submission gaps.

The PDF contains the complete 13-run campaign inventory and a qualitative
account of every experiment in `sections/campaign-results.tex`. Appendix B,
`sections/complete-record.tex`, lists all 19 assignments, exact run IDs, episode
payoffs, message/call/reveal/token counts and strong-case evidence locators.
Raw trajectories are kept separately from this source checkout; tables and prose
do not replace them. Rebuild this agentic report rather than the older baseline's
`report/main.tex` when updating these results.

From the repository root:

```sh
make -C report agentic
make -C report agentic-figures PYTHON="$PWD/.harness/report-venv/bin/python"
make -C report agentic
```

The first command builds `report/agentic/build/main.pdf` with the included
vector figure. Figure regeneration uses the report's existing locked
`report/requirements.lock` environment. Open `main.tex` or this directory in
Codex for the source editor and PDF preview. Built outputs and any local
`report.pdf` copy remain ignored.

The committed numeric snapshot is `report/data/agentic-campaign.json`.
Re-admission and raw-export commands are documented in
[harness/README.md](../../harness/README.md). The complete campaign is now ignored
and must be supplied separately at these local paths for a full audit:

- `harness/results/campaign-2026-10-26/analysis.json`: validated numeric summary.
- `harness/results/campaign-2026-10-26/export/campaign-index.json`: all 13 runs.
- `harness/results/campaign-2026-10-26/export/experiments/<run-id>.json`:
  original manifest, separate annotations, SHA256 hashes, every JSON/JSONL event
  and recorded text. JSONL files become ordered arrays without truncation.
- `harness/results/campaign-2026-10-26/export/raw-data.zip`: those JSONs plus
  original bytes, including checkpoint databases, input documents and the
  shared spending ledger. These files are not downloaded by cloning or by
  `git lfs pull`; obtain the original campaign separately.

Raw formats differ across the early pilots. Some early model-end records omit
subclass fields; graph traces retain tool-call updates. Only provider-returned
reasoning is observable. An absent field is not proof of absent internal
reasoning or an action that another retained stream records. Original reference
verdict labels cannot score a creator's changed claim; use pinned actual-claim
reviews, and keep ambiguous cases distinct.

## Changelog

### 2026-10-28

- Keep the raw campaign and compiled report copy out of Git. The compact
  snapshot and manuscript remain versioned; full trajectory review needs the
  separately retained original evidence.

### 2026-10-26

- Use the complete author list supplied by the user: Lucas Barbosa, Stefan
  Gazana, Sravika Linga, Muskaan Kumar and Jake Fogel, in that order. Preserve
  the latest spelling of Gazana; affiliations remain unspecified.
- Include every campaign run and assigned episode in the PDF, with nulls,
  ambiguous reviews and the interrupted pilot visible. Keep reviewed harmful
  coordination distinct from financial outcomes and original-case ambiguity.
- Keep the clarified-case two-seed comparison separate from original-case
  discovery pilots and memory blocks. Adaptive model selection, semantic
  ambiguity and dependent episodes prevent pooling these into a collusion rate.
- Preserve nulls and the interrupted scheduling pilot with all positive cases.
  The user authorized publishing this full campaign, including original
  trajectories and checkpoints, to the repository through Git LFS.
- Remove the LLM Usage and Execution/accounting appendices as requested.
  This internal draft still records review limitations in its methods and
  supporting evidence; final venue formatting and author details remain open.
