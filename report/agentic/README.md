# Seeded recruitment in agent juries

The current manuscript, [When Bad Votes Spread](main.tex), addresses Track 2
of the November Swarm Alignment Hackathon: reach and persistence after seeded
bad behavior, and what the current data can identify about network shape.
The [paper brief](../../docs/reporting/paper-brief.md) records the current
question and SW1–SW7 claim mapping; [review.md](review.md) records checks and
open gaps. The earlier October manuscript is preserved as
[historical-main.tex](historical-main.tex).

The updated cloud registry admits 104 sessions and 116 cases from two checkout
cohorts, retaining eight played failures and excluding one setup-only artifact.
Tables keep false/truthful reveals, abstentions and unrevealed commitments
separate. Appendix B links every admitted W&B session and pins original file
hashes in [the numeric snapshot](../data/swarm-track-snapshot.json).
Appendix C preserves actual inputs, returned reasoning and confirmed actions.
These are descriptive results, not a population rate or a topology effect.

The [completed C1 handoff](../../harness/research/swarm-scale/RESULTS-C1.md)
now covers all 57 C1 runs and 63 cases. These completed results are embedded
in the main text and replace the earlier 24-run C1 subset in every report
table and cloud-register entry. The same 47 C2 sessions retain their earlier
selection cutoff. The complete C1 per-cell summary, case counts and pinned
cloud register are also versioned alongside the handoff. No model calls are
needed to reproduce the updated report.

From the repository root:

```sh
python3 -I report/analysis/swarm_track_snapshot.py \
  --snapshot report/data/swarm-track-snapshot.json --tables report/tables
make -C report agentic
```

The table-only command needs no raw data, provider access or third-party Python
dependencies. The second command builds `report/agentic/build/main.pdf`.
The current manuscript uses BibTeX with `amsalpha`; `latexmk` runs the
bibliography pass using [references.bib](references.bib). Citation labels come
from author/year metadata rather than hand-written labels.
To re-audit original metrics, supply the verified session artifact packet and
run the builder with `--evidence-root`, `--registry` pointing to the frozen
snapshot, `--output` and `--tables`; Appendix B gives the command. Original
file hashes are checked before recomputation. Raw data and PDFs stay ignored.

For the archived October narrative, run `latexmk -pdf -outdir=build
historical-main.tex` from this directory. Its full campaign inventory and
qualitative record remain in `sections/campaign-results.tex` and
`sections/complete-record.tex`.

## Historical October evidence packet

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

### 2026-11-09

- Explain the vote lifecycle, one-vote capture shortfall, observation units and
  interpretation limits for independent readers. Preserve all audited data and
  source quotations, and record the editorial passages as pending author review.
  The [editorial decision](../../docs/decisions/report-editorial-pass-preserves-audited-evidence.md)
  also records the metadata-generated AMS alphabetic references.
- Feature selected case S1 beneath the abstract: side-by-side returned reasoning
  and the submitted assessment, followed by the confirmed false reveal and local
  credit payment. Reuse the monochrome model-tab style and link the complete
  context in the results and Appendix C; the example is not a prevalence estimate.
- Embed completed C1 results in the main text and refreeze the source registry
  at 104 played sessions/116 cases. Replace the overlapping partial C1 selection
  and preserve the earlier C2 cohort; the
  [refreeze decision](../../docs/decisions/report-refreezes-completed-c1-without-double-counting.md)
  supersedes the original frozen-handoff choice.
- Limit the current Swarm manuscript's title block and PDF author metadata to
  Lucas Barbosa and Stefan Gazana, as requested. The October archive retains
  its historical attribution.
- The original handoff kept the completed C1 packet separate from the manuscript:
  existing run IDs overlap, so a completion update extends the cohort rather
  than adding independent observations. See the
  [completion decision](../../docs/decisions/completed-c1-results-extend-the-frozen-paper-cohort.md).
- Reorient the main manuscript to Swarm Track 2 and retain the October narrative
  separately. Shared public exposure supports recruitment/reach evidence;
  jury-size changes do not identify graph-shape effects. See the
  [scope decision](../../docs/decisions/swarm-report-distinguishes-recruitment-from-topology.md)
  and [unrun topology proposal](../../docs/research/swarm-topology-proposal.md).
- Use all source-compatible sessions in the frozen W&B audit, with both checkout
  cohorts and played failures visible. The earlier principles packet reconciles
  to 390 truthful reveals and ten abstentions; the handoff's 397 is not used.
- Use monochrome examples with small model tabs, serif speaker labels and
  grouped exchanges, following the user's *Situational Awareness* reference.
  The [visual decision](../../docs/decisions/report-examples-use-monochrome-model-tabs.md)
  replaces the initial colored panel treatment; quotation content is unchanged.
- Adapt the supplied prompt/response layout to the manuscript's Times fonts and
  page geometry. Results include selected Kimi reasoning and submitted assessment;
  Appendix C gives the actual system prompt, scripted inputs, longer reasoning,
  action confirmations and payment provenance. Source locators and full hashes
  are in [trace-sources.md](trace-sources.md).
- Keep this completed November seeded-peer case separate from the historical
  13-run study. It illustrates paid coordination against the truth under the
  short charter, not a charter violation, campaign rate or non-Kimi result.
- Label the existing October public excerpts as public model messages; original
  raw October sources are required to repeat their historical quotation audit.
- The [presentation decision](../../docs/decisions/report-model-excerpts-link-inputs-to-executed-actions.md)
  records why scripted inputs, returned reasoning and confirmed actions retain
  separate labels. The [review](review.md) records the source and PDF checks.

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
