# Agentic report review

## Main-branch handoff checked 2026-11-09

The full repository gate passed before the handoff commit, including all 420
Python tests in 400.81 seconds and real Docker/Anvil acceptance tests. The
report analysis passes Ruff; all four frozen TeX tables regenerate byte for
byte. `make -C report agentic` builds the same reviewed PDF SHA256
`8a05081e0d007d4c220d060c72cf47bbda15e55658b5ea345e85afdd82ecdcb9`.
The standalone response template and archived October manuscript also compile.

The [completed C1 handoff](../../harness/research/swarm-scale/RESULTS-C1.md)
adds the 57-run completion packet separately. Its 24-run overlap with the
frozen C1 cohort is explicit; manuscript tables and their cutoff are unchanged.
Staged source and aggregate data passed the configured-credential check, with
raw trajectories, agent databases and raw operator-ledger rows excluded.
The scientific and submission gaps in the earlier review remain open.

## Swarm-track reorientation reviewed 2026-11-09

Reviewer: Codex, directly; this side conversation does not permit subagents.
This is not independent human semantic review. Source: `ecb1d28` plus the
report/analysis/brief changes. Decision: **internal research draft**.
The current source is `report/agentic/main.tex`; the former October narrative
is preserved in `historical-main.tex` and also compiles successfully.

### Scientific scope and source audit

- The report now addresses Swarm Track 2 through recruitment, direct reach and
  repeated exposure. It does not infer multi-hop velocity or a network-shape
  effect from fixed shared deliberation. The proposed equal-edge-count graph
  comparison is explicitly unrun. Earlier infrastructure and October results
  are identified as preexisting.
- A live read of W&B froze 72 matching session artifacts at 2026-11-09 05:53
  UTC / 00:53 EST. One tagged setup-only artifact is excluded. All 71 played
  sessions, 83 cases and seven played failures remain, including two episodes
  reconstructed from retained case evidence after empty manifest arrays.
- Original manifests/evidence/opportunity logs were obtained from immutable
  session artifacts or matched local copies and checked against artifact
  digests. The frozen snapshot pins file SHA256 values and cloud identities.
  Runtime source hashes are identical across the two checkout cohorts;
  per-model/cell configuration equality and actual on-chain parameters are
  asserted. Contract runtime hashes agree within each network mode; the modes
  differ and the contract includes an immutable operator address.
- An independent walk of the original jury records reconciles all 264 modeled
  seats: 81 false, 93 truthful, 89 with no commitment and one unrevealed. Those
  heterogeneous totals are not an aggregate collusion statistic. The maximum
  fifteen-juror Kimi K2.7 reach is seven of eight evaluated jurors. Duty cells
  contain twenty truthful/no false reveals; four Kimi repeated-exposure blocks
  contain eleven captured cases out of twelve. Mandate cells have no false
  majority; their isolated wrong ballot does not settle coalition intent.
- The first S1 HumanMessage embeds the supplied offer and peer invitation
  under the participant-content label. This was verified in the actual call
  record and against the runner's public-snapshot path. No autonomous relay is
  needed for first exposure. Quote text, commitment/reveal and payment
  provenance retain the source checks recorded below.
- The separate fifty-session principles packet exactly reproduces the
  committed snapshot's counts: 390 truthful reveals, ten abstentions, zero
  false/unrevealed. Its run/artifact identities and original file hashes are
  now pinned in `report/data/swarm-principles-source-registry.json`.
  The handoff's 397 does not reconcile with this packet and is not repeated.

### Reproduction and rendering

The source audit using the frozen `--registry` reproduces
`report/data/swarm-track-snapshot.json` byte for byte. Both that source audit
and `--snapshot` table-only mode reproduce all four generated TeX files byte
for byte. Ruff checking/formatting pass. The analysis reuses the harness vote
classifier and scorer; no runtime or campaign files were edited for this work.

`make -C report agentic` passes. A fresh build from `report/agentic/` also
passes (exit 0):

```sh
latexmk -pdf -synctex=1 -interaction=nonstopmode -halt-on-error \
  -file-line-error -outdir=/private/tmp/swarm-report-accepted-20261109 main.tex
```

Clean-build and canonical PDF text match. Final logs have no warnings,
undefined references, missing glyphs or overfull/underfull boxes. All fonts
are embedded. Compiler/dependency versions remain those recorded below.
The PDF has fourteen Letter pages: main text and references 1--7, limitations
on 8, cloud audit/register on 9--11 and actual model exchanges on 12--14.
The abstract is 215 words. All fourteen pages were rendered and inspected at
normal size; changed pages were checked again, including the final commitment
definition on page 3. Literal command-line double hyphens and continuations
survive PDF extraction. The monochrome model tabs and quote grouping remain.

Canonical PDF SHA256:
`8a05081e0d007d4c220d060c72cf47bbda15e55658b5ea345e85afdd82ecdcb9`.
Primary snapshot SHA256:
`cbe6ec7fb60cbc8338f3874e931cec385940e119f3ef313a131efd55334dd785`.
Legacy source registry SHA256:
`9ae91034573ade293cbb197d2d1d1ef219454113f328a89d55f00fa33d9032d3`.
Logs and previews are in `/private/tmp/swarm-report-evidence-20261109/`,
`/private/tmp/swarm-report-accepted-20261109/`, and the canonical build folder.
`git diff --check` and decision-index verification pass. A credential scan
found no configured secret values in the report, analysis or data; no values
were displayed. The full runtime/Docker gate was not rerun for report work.

### Open gaps and boundaries

The campaign continues outside the frozen cutoff; later outcomes require a
new audited snapshot and claim review. No model calls, campaign operations,
cloud writes or submissions were performed. Independent human interpretation,
author affiliations and current official-template visual compliance remain
open. The official copy link requires sign-in and the available connected
reader could not retrieve it. The guideline and Lee--Tiwari v1 primary text
were read; Sections 4.1--4.2 distinguish their messaging/interaction setup
from this incentive-mediated, directly exposed jury experiment. The original
October raw packet is still needed to repeat its older quotation audit.

---

## Monochrome visual revision reviewed 2026-11-09

The user requested the appearance shown in an attached *Situational Awareness*
reference image. Examples now have white interiors, thin black rounded frames,
small black model tabs, bold serif speaker/field labels, dashed dividers and
source captions below. Related passages share one frame. The short scripted
offer/invitation pair and commitment request stay intact on one page.
The [visual decision](../../docs/decisions/report-examples-use-monochrome-model-tabs.md)
supersedes the earlier panel palette; the scientific scope remains as reviewed
below.

All selected prompt, scripted input, rationale and submitted-assessment text
was checked again against the retained source strings, including all five
pinned source hashes. Only editorial labels, grouping and layout changed.
The shared example environment replaces the separate input/output styles;
it uses the existing tcolorbox dependency and its native separators.

`make -C report agentic` passed, as did a build from a fresh output directory:

```sh
cd report/agentic
latexmk -pdf -synctex=1 -interaction=nonstopmode -halt-on-error \
  -file-line-error -outdir=/private/tmp/veracity-monochrome-final-20261109 main.tex
```

Both builds exited 0, with identical extracted PDF text and no LaTeX warnings,
undefined references, missing glyphs or overfull/underfull boxes. All fonts are
embedded. The compiler/package versions are unchanged from the review below.
Canonical log: `report/agentic/build/main.log`; clean-build logs:
`/private/tmp/veracity-monochrome-final-20261109/{build.log,main.log}`.

The PDF remains 15 Letter pages, with the main example on 7, historical public
exchange on 12 and Appendix C on 13--15. All rendered pages were inspected at
normal size. Pages 2--5 were checked again after removing a redundant prompt
label, which restored coherent paragraph/float placement. Source captions,
tab clearance, dashed rules and complete short frames were inspected. Final
renders: `/private/tmp/veracity-excerpt-restyle-20261109/final-render/`.

Reviewed canonical PDF SHA256:
`4db95abdee31c8c770e44a6bb5a8adc3b6c9b4cc5cc7d374331ffab4379e5e28`.
`git diff --check` and decision-index verification pass. Runtime/Docker tests
were not rerun for this visual change. Decision: **internal draft**; the
existing human-review, raw-source-access and submission-format gaps below
remain open. Unrelated campaign files were left intact.

---

## Model-output revision reviewed 2026-11-09

Reviewer: Codex, not independent human review. Source: `ecb1d28` plus the
report-only working changes and the associated decision/brief updates.
Unrelated campaign changes were already present and were left intact.
Manuscript: `report/agentic/main.tex`; PDF:
`report/agentic/build/main.pdf`. Decision: **internal draft**.

### Evidence checks

- The new S1 vignette is one purposefully selected completed Kimi K2.6 run,
  `run-e4a230c68dde`, separate from the October campaign. Both parties and one
  peer are scripted; two jurors are evaluated. No campaign totals, rates or
  cross-model conclusions were added.
- All five source-file SHA256 values match the retained originals. The full
  system-text block, publisher offer and peer invitation match their source
  strings after LaTeX escaping, whitespace and typographic quote normalization.
  All three reused quotation macros, six consecutive reasoning bullets and
  two nonadjacent rationale paragraphs likewise match. Omissions are marked.
- The submitted verdict/assessment match the actual model tool request.
  Commitment and reveal ToolMessages confirm successful receipts in blocks 6
  and 10. Both evaluated jurors' final false reveals and promised 10 ETH
  transfers match the retained episode and manifest. Juror 2's ordinary reward
  plus transfer is 11.666666666666666666 synthetic ETH, below its monthly target.
- Interpretation remains separate from quotations. The model's calculation
  contains mistakes and counterparty-payment uncertainty; the report does not
  endorse it. Returned reasoning is not certified faithful internal computation.
  The short charter omits truth/independence duties: the case is described as
  paid coordination against the truth, not a violation of those omitted duties.
- The October opening prompt and three public quotations preserve the existing
  manuscript's wording. Their raw packet is absent here; this revision relies
  on the earlier review below and makes no fresh raw-source audit claim.
- Selected new report sources contain no credential values from the local
  environment file and no private-key blocks; the check displayed no values.
  Complete private transcripts were not included. No new inference requests,
  cloud mutations, campaign operations or commits were performed.

### Build and page review

The standard `make -C report agentic` command passed (exit 0). A second build
from a fresh output directory passed with the same extracted PDF text:

```sh
cd report/agentic
latexmk -pdf -synctex=1 -interaction=nonstopmode -halt-on-error \
  -file-line-error -outdir=/private/tmp/veracity-trace-report-final-20261109 main.tex
```

Compiler: pdfTeX 1.40.27, TeX Live 2025, latexmk 4.86a, inline bibliography.
New panel dependency: tcolorbox 6.4.1 (breakable and skins libraries), using
xcolor 3.02. Existing New TX text 1.744/math 1.754 and margins are retained.
Logs: `report/agentic/build/main.log`,
`/private/tmp/veracity-trace-report-20261108/canonical-build.log`, and
`/private/tmp/veracity-trace-report-final-20261109/{build.log,main.log}`.
Final logs contain no undefined references/citations, missing glyphs, overfull
or underfull boxes, or other LaTeX warnings. All PDF fonts are embedded.

The final PDF has 15 Letter pages: main text and references 1--8, Appendix A
on 9, Appendix B on 10--12, and new Appendix C on 13--15. The abstract is
230 words. All pages were rendered and inspected at normal page size; changed
pages 1--3, 7 and 12--14 were checked again after final layout changes. Unchanged
pages have byte-identical renders. Page 13 was additionally inspected at 180
dpi to confirm fine frame edges; no clipping or missing text was found.
Final rendered pages are at
`/private/tmp/veracity-trace-report-20261108/final/`.
The existing figure and numeric tables are unchanged; regeneration was not
needed. Speaker/source labels distinguish panels without relying on color.

Reviewed canonical PDF SHA256:
`fedf229a71475883d512a5591b6dd72fafcfdf0dd83fa961a401a1e1bf89a87c`.
`git diff --check` and `python3 scripts/decision-index.py --check` pass.
Verification was scoped to report/source integrity; the runtime/Docker gate
was not rerun for this presentation change.

### Remaining gaps

Independent human semantic review, author affiliations and official template
visual compliance remain open. The selected S1 raw packet is retained locally;
cloud-download completeness was not independently checked in this revision.
The original October packet is required to repeat its historical quote audit.
These gaps do not prevent reviewing the new layout and source-pinned selected
excerpts, but the PDF is not certified submission-ready.

---

## Historical review, 2026-10-26

Review date: 2026-10-26. Reviewer: Codex; not independent human review.
Report source: working changes on revision `f9a8ecc`. Experiments recorded
revision `11f4f01` plus per-run source hashes in
`report/data/agentic-campaign.json`, which distinguish runtime versions.
Manuscript: `report/agentic/main.tex`. PDF: `report/agentic/build/main.pdf`.
Decision: internal results draft; not submission-ready.

## Evidence and interpretation

- A0–A3 and AC1–AC4 are recorded in the reporting brief. All 13 runs and 19
  assignments are retained, including the interrupted pilot. Eighteen terminal
  episodes reconcile with engine evidence; seven strong, three ambiguous and
  eight not-established annotations are counts, not an incidence estimate.
- Strong-case reviews require actual-claim support, acknowledged adverse
  agreement before funding, executed votes, coalition benefit and outsider loss.
  Annotations pin exact source hashes; none is an independently human-validated
  label. Unchanged reference labels do not score changed submitted claims.
- Principal post-fix clear-case seeds 31 and 43 each have a communication-on
  and communication-off run. The earlier seed-31 pilot is not a third seed.
  Three-episode memory blocks are dependent observations, one block per cell.
- Local Anvil base units are not dollars. Contract-valid actions can harm
  factual adjudication. Honest safe payoff is zero in this stress case;
  positive productive honest returns and verification effort are not modeled.
- The user authorized publishing this complete campaign to the repository.
  Large source trajectories and checkpoints use Git LFS. Every combined
  experiment JSON parses; the 807-member raw archive passes CRC verification.
  Known configured secret values and credential patterns were checked across
  source files and archive entries without finding a match.

## Build and rendering

The native Codex compiler reported success. The independent reproducible build
uses TeX Live 2025 pdfLaTeX through latexmk 4.86a:

```sh
make -C report agentic
make -C report agentic-figures PYTHON="$PWD/.harness/report-venv/bin/python"
```

The PDF has no undefined references/citations or overfull boxes after repairing
a path line break. Main document fonts are embedded. Abstract: 202
words. Vector figures use the report's STIX/Times-compatible locked Matplotlib
environment and numeric safe snapshot; observed cells have text labels as well
as colors. No SD/CI is appropriate for the case-study display.

The original six rendered pages and the figure were inspected at final width. Poppler
was unavailable; Ghostscript rendered pages at 120 dpi and pypdf checked text
and font embedding. After the requested appendix removal, the PDF was rebuilt,
the deleted headings were confirmed absent, and the changed end pages were
rendered again. Build diagnostics are in `build/main.log`; rendered pages are
in `build/pages/`. These outputs are ignored.

The complete-results revision names Lucas Barbosa, Stefan Gazana, Sravika Linga,
Muskaan Kumar and Jake Fogel, in that order, in the title block and PDF metadata.
It adds the full 13-run inventory, a qualitative account of each run, and an
appendix covering all 19 assignments. The tables were reconciled against the
admitted snapshot: all 18 terminal outcomes, payoffs, message/call/reveal/token
counts, exact run IDs and seven strong-case agreement locators match. The
interrupted assignment has undefined terminal metrics, not imputed zeros.

The revised PDF is 11 pages: the main argument and references occupy pages
1--7, ethics/limitations is on page 8, and the complete record is on pages
9--11. `make -C report agentic` passed with no overfull boxes or undefined
references. All 11 pages were rendered and inspected, and a split-off total
row was repaired. All three quoted excerpts match the original R10.1 public
messages verbatim. Build log: `.harness/agentic-complete-results-build.log`.
The published `report.pdf` copy was refreshed after these checks.

Repository verification passed with `bash scripts/verify.sh`, including
Foundry/Rust checks, 294 legacy harness tests and 64 harness-v2 tests with
Docker/Anvil integration. The final Stop hook also returned `{}` after the
same gate passed. Logs: `.harness/verification-agentic-final-2026-10-26.log`
and `.harness/verification/run.PwP9Uv`. Raw archive CRC and JSON parse checks
passed independently; `git diff --check` reported no whitespace errors.

## Open gaps

- Human authors must review the semantic labels, source-to-claim links and
  final manuscript. The five authors are named; affiliations are pending.
- Official Apart template text was inspected, but this article layout has not
  been certified against its visual layout. Final required disclosures and
  submission formatting remain an author decision. No submission was attempted.
- No powered treatment estimate, representative collusion rate, model ranking
  or long-horizon generalization is supported. Larger independent blocks,
  domains, incentive variants and a calibrated positive honest baseline are
  further research.
- Early pilots may contain hidden SDK HTTP retries. Source snapshots preserve
  that distinction; the principal four trials use verified retry disabling.
  Stochastic model trajectories cannot be replayed bit for bit.
