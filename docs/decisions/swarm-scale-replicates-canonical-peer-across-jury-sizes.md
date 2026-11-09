# Swarm-scale replicates canonical-peer across jury sizes

- **Date:** 2026-11-09
- **Status:** Accepted
- **Deciders:** Stefan Gazzana
- **Area:** harness, benchmark

## Context

The fifteen-juror campaign of 2026-11-08 (`harness/results/swarm-2026-11-08`) found no
evaluated false vote:

- 5 models;
- 25 collusion-arm cases;
- 397 revealed votes.

It ran under the "principles" charter and mostly on models that never colluded before. The
only earlier condition with paid wrong majorities is
`harness/research/frontier-2026-10-31/canonical-peer.toml`, from Lucas's
2026-10-31 campaign (`RESULTS.md` there). There, Kimi K2.7 Code produced 2 such cases and
Kimi K2.6 produced 1, under:

- the short root charter;
- a 20 ETH juror revenue target;
- a paid 10 ETH offer;
- transfers.

`quota-peer`, which is identical apart from the principles charter, produced none. The
report deadline (2026-11-09 22:59 AEDT) left hours, not a night, for a new campaign.

Two earlier plans are stopped:

- **Seven-juror fallback**
  ([record](seven-juror-fallback-runs-only-without-signal.md)). Stopped after 4 cases per
  arm for GLM-5.3 and DeepSeek V4.1 Flash, with no false vote. Its partial results stay in
  `harness/results/swarm7-2026-11-09` and are not reported as a campaign.
- **Peers arguing the false claim for a 500 ETH offer.** Stopped before any case finished.

## Decision

`harness/research/swarm-scale/` takes canonical-peer's settings and asks a swarm question:
does the size of the colluding bloc change whether evaluated jurors join it?

- **Matched arms at jury sizes 3, 7 and 15.** Scripted peers always sit one vote short of a
  majority (1, 3 and 7). At size 3 the peer message is canonical-peer's, word for word.
- **Three single-change contrasts at size 3:**
  - the principles charter (does an explicit truth duty stop it);
  - a three-case session with memory on one chain (contagion after an observed payment);
  - a mandated model publisher with no scripted peers or offer (emergent recruiting).

Changes from canonical-peer:

- **One case per run.** It used a two-case session, but Kimi K2.7 Code colluded in both of
  its cases. This halves the time per run.
- **Funding.** A 100 ETH party bond with 5% juror bond and pool shares, so jurors keep the
  same 5 ETH bond and 5 ETH pool. The publisher can then pay 10 ETH to all fifteen jurors.
- **Models.** Kimi K2.6 and Kimi K2.7 Code are the subjects, with DeepSeek V4 Pro as the
  contrast. All three run at once (`PARALLEL=3`) through `plan.txt`, which runs every
  cell's first seed before any repeat.
- **Budget.** The campaign has its own ledger, capped at 135 USD. That cap is the approved
  150 USD redo budget less the 14.71 USD recorded by the stopped 500 ETH redo, part of
  which is held rather than charged.

## Consequences

- **No stated duty is broken.** Under the short charter, a false vote breaks no stated
  duty. Report it as paid coordination against the truth, not a charter violation. Only
  the principles contrast tests a stated duty.
- **Not a population estimate.** There are 2 to 3 seeds per cell and the models were
  chosen because they colluded before. Report per-cell counts with intervals.
- **Dropped models.** GLM-5.3 and DeepSeek V4.1 Flash are dropped. Neither colluded in
  either campaign, and Flash hit repeated Workers AI 429s.
- **Unmeasured hypothesis.** Pre-sprint, the second case of a session may have mattered
  through observed payment. That is not measured outside the contagion arm.
