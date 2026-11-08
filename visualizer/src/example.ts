import { parseExperiment, type EpisodeState, type Snapshot } from './model';

const deployment = {
  chain_id: 31337,
  contract_address: '0x0000000000000000000000000000000000000001',
  code_hash: '0xillustrative',
  abi_version: 1,
  confirmation_depth: 1,
  finality_policy: 'confirmation_depth',
};

/** Authored teaching data, deliberately separate from admitted experiment evidence. */
function createIllustrativeEpisode(
  episodeId: string,
  outcome: 'creator' | 'challenger' | 'unchallenged',
): Snapshot[] {
  const configuration = {
    episode_id: episodeId,
    experiment_id: 'illustrative',
    scenario_id: 'invoice-reconciliation',
    creator_id: 'creator',
    challenger_id: 'challenger',
    juror_ids: ['juror-1', 'juror-2', 'juror-3'],
    treasury_id: 'treasury',
    provenance: {},
    parameters: {
      beta_wei: '1000000000000000000',
      gamma_bps: 1000,
      winner_bps: 6000,
      juror_bps: 3000,
      protocol_bps: 1000,
      posting_duration_secs: 60,
      challenge_duration_secs: 120,
      commit_duration_secs: 120,
      reveal_duration_secs: 120,
    },
  };
  const initial: EpisodeState = {
    episode_id: episodeId,
    onchain_episode_id: `0x${episodeId}`,
    configuration_hash: '0xconfiguration',
    configuration,
    phase: 'REGISTERED',
    posting_deadline: 1793422860,
    challenge_deadline: 0,
    commit_deadline: 0,
    reveal_deadline: 0,
    content: null,
    evidence: null,
    content_hash: null,
    evidence_hash: null,
    jurors: configuration.juror_ids.map((actor_id) => ({
      actor_id,
      commitment: null,
      revealed: false,
      verdict: null,
      assessment_hash: null,
    })),
    creator_votes: 0,
    challenger_votes: 0,
    required_votes: 2,
    juror_bond_wei: '100000000000000000',
    locked_liability_wei: '0',
    total_deposited_wei: '0',
    total_credited_wei: '0',
    deployment,
  };
  const frames: Snapshot[] = [{ episode: initial }];
  const record = (changes: Partial<EpisodeState>) => {
    const previous = frames.at(-1)!.episode;
    frames.push({ episode: { ...previous, ...changes } });
  };
  record({
    phase: 'OPEN',
    content:
      'The October invoice total reconciles with the recorded line items.',
    content_hash: '0xclaim',
    challenge_deadline: 1793422980,
    total_deposited_wei: '1000000000000000000',
    locked_liability_wei: '1000000000000000000',
  });
  if (outcome === 'unchallenged') {
    record({
      phase: 'EXPIRED_UNCHALLENGED',
      total_credited_wei: '1000000000000000000',
      locked_liability_wei: '0',
    });
    frames.at(-1)!.settlement = {
      episode_id: episodeId,
      outcome: 'EXPIRED_UNCHALLENGED',
      final_votes: {},
      winner_id: null,
      winner_payout: '0',
      juror_payouts: {},
      protocol_fee: '0',
      forfeited_bonds: {},
      refunds: { creator: '1000000000000000000' },
      total_deposited: '1000000000000000000',
      total_credited: '1000000000000000000',
      deployment,
    };
    return frames;
  }
  record({
    phase: 'COMMIT',
    evidence:
      'The supporting ledger lists an adjustment absent from the invoice. Review the reconciliation before voting.',
    evidence_hash: '0xevidence',
    commit_deadline: 1793423100,
    total_deposited_wei: '2000000000000000000',
    locked_liability_wei: '2000000000000000000',
  });
  for (let index = 0; index < 3; index++) {
    record({
      jurors: frames
        .at(-1)!
        .episode.jurors.map((juror, j) =>
          j === index ? { ...juror, commitment: `0xcommit${index}` } : juror,
        ),
      total_deposited_wei: (
        2000000000000000000n +
        BigInt(index + 1) * 100000000000000000n
      ).toString(),
      locked_liability_wei: (
        2000000000000000000n +
        BigInt(index + 1) * 100000000000000000n
      ).toString(),
    });
  }
  record({ phase: 'REVEAL', reveal_deadline: 1793423220 });
  let creatorVotes = 0;
  for (let index = 0; index < 3; index++) {
    const supportsCreator = outcome === 'creator' ? index !== 2 : index === 2;
    if (supportsCreator) creatorVotes++;
    record({
      jurors: frames.at(-1)!.episode.jurors.map((juror, j) =>
        j === index
          ? {
              ...juror,
              revealed: true,
              verdict: supportsCreator
                ? 'CREATOR_SUPPORTED'
                : 'CHALLENGER_SUPPORTED',
              assessment_hash: `0xassessment${index}`,
            }
          : juror,
      ),
      creator_votes: creatorVotes,
      challenger_votes: index + 1 - creatorVotes,
    });
  }
  record({
    phase: outcome === 'creator' ? 'SETTLED_CREATOR' : 'SETTLED_CHALLENGER',
    locked_liability_wei: '0',
    total_credited_wei: '2300000000000000000',
  });
  const terminalPhase =
    outcome === 'creator' ? 'SETTLED_CREATOR' : 'SETTLED_CHALLENGER';
  frames.at(-1)!.settlement = {
    episode_id: episodeId,
    outcome: terminalPhase,
    final_votes: Object.fromEntries(
      frames.at(-1)!.episode.jurors.map((j) => [j.actor_id, j.verdict!]),
    ),
    winner_id: outcome,
    winner_payout: '1600000000000000000',
    juror_payouts: {
      'juror-1': '200000000000000000',
      'juror-2': '200000000000000000',
      'juror-3': '200000000000000000',
    },
    protocol_fee: '100000000000000000',
    forfeited_bonds: {},
    refunds: {},
    total_deposited: '2300000000000000000',
    total_credited: '2300000000000000000',
    deployment,
  };
  return frames;
}

export const exampleExperiment = parseExperiment({
  name: 'The content trust game',
  run_id: 'illustrative-replay',
  states: [
    ...createIllustrativeEpisode('case-01', 'creator'),
    ...createIllustrativeEpisode('case-02', 'challenger'),
    ...createIllustrativeEpisode('case-03', 'unchallenged'),
  ],
});
