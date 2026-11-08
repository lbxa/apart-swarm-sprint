# Scripted offers and seeded votes precede evaluated juror notifications

- **Date:** 2026-10-31
- **Status:** Accepted
- **Deciders:** Benchmark owner, through delegated methodology and error-fixing authority
- **Area:** harness, benchmark, scheduling

## Context

Live audits showed jurors committing inside an OPEN-phase opportunity after the
scripted challenger opened voting, before the offering party received its next
notification and posted the offer. Such votes cannot measure susceptibility to
the offer. The same race can place a model's vote before a scripted first mover.

## Decision

The capped exploratory suite enables `scripted_setup_first`. Both parties must
be scripted. They act before evaluated jurors, and the harness waits for their
asynchronous claim/challenge operations. In COMMIT it verifies the exact party
offer is present, then runs the seeded peer and waits for its binding commitment.
Only then are evaluated jurors notified. Each fixture acts once per phase;
evaluated jurors retain the configured concurrent opportunities and free choices.
The initial public discussion is included as participant-message data in the
first evaluated voting notification, without operator role identifiers. An empty
list is supplied in the baseline. This is a controlled exposure test, not an
autonomous discovery test.

## Consequences

The operator submits no participant actions. All fixture actions still use the
assigned participant's sandbox and gateway. A missing offer or seeded action
fails before model notification instead of silently becoming a negative result.
An operator metadata record and retained API/model traces establish the order.
This mode is opt-in; the general autonomous scheduler keeps its current default.

The earlier v2 offer attempts are retained as exposure-invalid pilots. The v3
suite reruns its matched baseline under the same scheduling rule, so setup timing
is not confounded with the offer condition. A real-engine fast-voter regression
witnessed the original race and now requires offer, seeded commitment, then every
evaluated juror commitment, with exactly one party offer per case.
