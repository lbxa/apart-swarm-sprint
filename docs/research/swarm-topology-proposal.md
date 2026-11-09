# Proposed controlled topology experiment

Status: **proposed, unrun**. This document does not change or relaunch the
active campaign, its plan, configurations, budget or data-admission rules.

## Question and identified gap

Does the deliberation graph change the reach and speed of bad-vote adoption
from one adversarial juror, after holding incentives, population and seed dose
fixed? The current shared-forum study cannot identify that effect: all targets
receive the seeded attempt directly, `m=(n-1)/2` grows with jury size, and one
more false vote always captures the colluding bloc.

## Fixed environment and factors

- Seven jurors, one scripted bad juror, six evaluated jurors. Majority is four;
  capture requires three evaluated false reveals. Use the same model, charter,
  stakes, opportunity budget and case across graph conditions.
- For a clean single-source version, disable publisher recruiting messages.
  The claim, evidence and a fixed payment rule are common environment inputs;
  only the seeded juror supplies adversarial deliberation. This changes the
  present non-escrowed publisher-offer mechanism and needs a calibrated positive
  control before a topology contrast. Define the measured network as the jury.
- Use vertices `0..6`, undirected permitted juror-message edges, and synchronous
  delivery so a message crosses at most one edge per logical round.
- Ring, seven edges: `01, 12, 23, 34, 45, 56, 60`.
- Hub graph, seven edges: `01, 02, 03, 04, 05, 06, 12`.
- A complete graph is an optional dense reference, not an equal-density shape
  control. Ring versus hub holds edge count fixed but changes the degree
  distribution; this is the intended graph treatment.
- Randomize seed location with a declared schedule. Hub versus peripheral
  placement is a separate factor; keep the matched starting vertex schedule
  in the ring. Do not interpret placement and graph effects interchangeably.
- Include no-bad-peer controls with the same fixed payment rule. This measures
  false decisions induced by incentives without a supplied bad peer.

## Communication enforcement and lineage

Disable unrestricted public deliberation and all alternate forwarding paths.
Enforce graph membership at the communication gateway, including private chat
creation, existing histories and shared stores. Keep factual case access equal.
Record the first actual exposure, sender, recipient, round, content hash and
whether a message is original or relayed. Do not inject the bad seed again
each round or case. Verify that denied non-edge messages never reach targets.

## Endpoints and sampling

Record first false commitment and first confirmed false reveal by logical
round, newly adopting jurors per round, maximum reached graph distance,
persistence and capture. Report all assigned seats, abstentions, unrevealed
commitments and execution failures separately. A message proves exposure;
adoption requires the subsequent action. Forwarding without a false action
and false action without a retained forwarding path are distinct observations.

Use independently initialized runs as sampling units, and block or randomize
order across graph and seed-location conditions. Determine the number of runs
from a stated precision or power target before execution. Do not pool votes
within a run into independent trials. Keep all failures after play begins.
Use only Cloudflare Workers AI if this proposal is later authorized to run.

## Acceptance criteria before a topology claim

1. The initial bad juror and matched no-seed control differ only in the intended
   intervention, and a positive control demonstrates a feasible adoption path.
2. Non-edge delivery and public-forum bypass tests pass.
3. Seed message is supplied once, exposures precede attributed actions, and
   recorded timestamps are logical rounds rather than provider latency.
4. Graphs have the declared node/edge counts and seed-placement assignments.
5. Analysis retains unsuccessful runs and identifies the independent unit.
6. The graph comparison estimates a declared reach/speed contrast. A null is
   reported with its uncertainty; it is not treated as proof that shape never
   matters.
