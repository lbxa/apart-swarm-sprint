# Seven-juror fallback runs only without signal

- **Date:** 2026-11-08
- **Status:** Accepted
- **Deciders:** Stefan Gazzana
- **Area:** harness, benchmark

## Context

The fifteen-juror campaign
([design](swarm-peer-pressure-seats-seven-scripted-jurors-of-fifteen.md)) uses the
"principles" charter. In the pre-sprint campaign that charter gave 0 wrong reveals in
110, so every bar may sit at 100%. The only pre-sprint condition that produced paid
wrong majorities was `harness/research/frontier-2026-10-31/canonical-peer.toml`. It had
four features:

- the short root charter, which states no truth or independent-judgment duty;
- a juror revenue target of 20 ETH;
- a paid 10 ETH offer;
- credit transfers between accounts.

## Decision

If the main campaign ends with **no evaluated juror, in any model, revealing the false
verdict in the collusion arm**, `harness/research/swarm7/run-if-no-signal.sh` launches a
fallback. The fallback has these features:

- Matched seven-juror arms (`harness/research/swarm7/`), with three scripted peers of
  seven, one evaluated defector short of capture.
- The four `canonical-peer` features above, with the same models, seeds and driver.
- Its budget is what remains of the 150 USD total after the main ledger. Remaining
  holds count as spent, so both campaigns stay within the approved total.

If the main campaign shows any evaluated false vote, the fallback does not run.

## Consequences

- **Not a stated-rule violation.** Under the short charter, a false vote breaks no
  stated duty. The report calls it paid coordination against the truth, not a
  constitutional violation, and keeps it separate from the main experiment's charter
  condition.
- **No pooling.** The fallback's resistance bars are not pooled with the main
  campaign's. The two differ in charter, incentives and jury size.
- **Timing.** Each fallback case has four evaluated jurors, so it takes about half the
  requests and time of a fifteen-juror case.
