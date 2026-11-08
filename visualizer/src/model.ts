import { z } from 'zod';

export const phaseSchema = z.enum([
  'REGISTERED',
  'OPEN',
  'COMMIT',
  'REVEAL',
  'SETTLED_CREATOR',
  'SETTLED_CHALLENGER',
  'ABORTED',
  'EXPIRED_UNCHALLENGED',
  'EXPIRED_UNFUNDED',
]);
const verdictSchema = z.enum(['CREATOR_SUPPORTED', 'CHALLENGER_SUPPORTED']);
const id = z.string().min(1);
const integer = z.number().int().nonnegative().max(Number.MAX_SAFE_INTEGER);
const amount = z
  .string()
  .regex(/^(0|[1-9][0-9]*)$/)
  .max(78)
  .pipe(
    z
      .string()
      .refine((value) => BigInt(value) < 2n ** 256n, 'Amount exceeds uint256'),
  );
const amounts = z.record(id, amount);
const deploymentSchema = z.object({
  chain_id: integer,
  contract_address: id,
  code_hash: id,
  abi_version: integer,
  confirmation_depth: integer,
  finality_policy: id,
});
const configurationSchema = z.object({
  episode_id: id,
  experiment_id: z.string().default(''),
  scenario_id: z.string().default(''),
  creator_id: id,
  challenger_id: id,
  juror_ids: z.array(id).min(1).max(255),
  treasury_id: id,
  parameters: z.object({
    beta_wei: amount,
    gamma_bps: integer.max(9999),
    winner_bps: integer.max(10000),
    juror_bps: integer.max(10000),
    protocol_bps: integer.max(10000),
    posting_duration_secs: integer.positive(),
    challenge_duration_secs: integer.positive(),
    commit_duration_secs: integer.positive(),
    reveal_duration_secs: integer.positive(),
  }),
  provenance: z.record(z.string(), z.string()).default({}),
});
const jurorSchema = z
  .object({
    actor_id: id,
    commitment: id.nullable(),
    revealed: z.boolean(),
    verdict: verdictSchema.nullable(),
    assessment_hash: id.nullable(),
  })
  .superRefine((juror, context) => {
    if (
      juror.revealed !== (juror.verdict !== null) ||
      (!juror.revealed && juror.assessment_hash !== null)
    ) {
      context.addIssue({
        code: 'custom',
        message: 'A vote and assessment must stay hidden until reveal',
      });
    }
  });

/** Public wire fields from core/src/game/types.rs, checked at the file boundary. */
export const episodeSchema = z
  .object({
    episode_id: id,
    onchain_episode_id: id,
    configuration_hash: id,
    configuration: configurationSchema,
    phase: phaseSchema,
    posting_deadline: integer,
    challenge_deadline: integer,
    commit_deadline: integer,
    reveal_deadline: integer,
    content_hash: id.nullable(),
    evidence_hash: id.nullable(),
    content: z.string().nullable(),
    evidence: z.string().nullable(),
    jurors: z.array(jurorSchema).min(1).max(255),
    creator_votes: integer,
    challenger_votes: integer,
    required_votes: integer.positive(),
    juror_bond_wei: amount,
    locked_liability_wei: amount,
    total_deposited_wei: amount,
    total_credited_wei: amount,
    deployment: deploymentSchema,
  })
  .superRefine((episode, context) => {
    const config = episode.configuration;
    const actors = [
      config.creator_id,
      config.challenger_id,
      ...config.juror_ids,
      config.treasury_id,
    ];
    if (config.episode_id !== episode.episode_id) {
      context.addIssue({
        code: 'custom',
        message: 'State and configuration must identify the same episode',
      });
    }
    if (
      new Set(actors).size !== actors.length ||
      config.juror_ids.length % 2 !== 1
    ) {
      context.addIssue({
        code: 'custom',
        message: 'Participant roles must be distinct and jury size odd',
      });
    }
    if (
      episode.jurors.length !== config.juror_ids.length ||
      new Set(episode.jurors.map((j) => j.actor_id)).size !==
        config.juror_ids.length ||
      episode.jurors.some((j) => !config.juror_ids.includes(j.actor_id))
    ) {
      context.addIssue({
        code: 'custom',
        message: 'Jurors must match the episode configuration',
      });
    }
    if (
      episode.required_votes !==
      Math.floor(config.juror_ids.length / 2) + 1
    ) {
      context.addIssue({
        code: 'custom',
        message: 'Required votes must match the jury majority threshold',
      });
    }
  });
const settlementSchema = z.object({
  episode_id: id,
  outcome: phaseSchema.exclude(['REGISTERED', 'OPEN', 'COMMIT', 'REVEAL']),
  final_votes: z.record(id, verdictSchema),
  winner_id: id.nullable(),
  winner_payout: amount,
  juror_payouts: amounts,
  protocol_fee: amount,
  forfeited_bonds: amounts,
  refunds: amounts,
  total_deposited: amount,
  total_credited: amount,
  deployment: deploymentSchema,
});
const frameSchema = z
  .object({
    episode: episodeSchema,
    settlement: settlementSchema.nullish(),
    recorded_at: z.iso.datetime({ offset: true }).optional(),
  })
  .superRefine((frame, context) => {
    if (
      frame.settlement &&
      (frame.settlement.episode_id !== frame.episode.episode_id ||
        frame.settlement.outcome !== frame.episode.phase)
    ) {
      context.addIssue({
        code: 'custom',
        message: 'The settlement must match its episode and phase',
      });
    }
    const settlement = frame.settlement;
    if (!settlement) return;
    const config = frame.episode.configuration;
    const expectedWinner =
      settlement.outcome === 'SETTLED_CREATOR'
        ? config.creator_id
        : settlement.outcome === 'SETTLED_CHALLENGER'
          ? config.challenger_id
          : null;
    if (settlement.winner_id !== expectedWinner) {
      context.addIssue({
        code: 'custom',
        message: 'The settlement winner must match the episode outcome',
      });
    }
    for (const [actor, verdict] of Object.entries(settlement.final_votes)) {
      const juror = frame.episode.jurors.find((j) => j.actor_id === actor);
      if (!juror?.revealed || juror.verdict !== verdict) {
        context.addIssue({
          code: 'custom',
          message: 'Settlement votes must match publicly revealed juror votes',
        });
      }
    }
  });
const snapshotSchema = z.preprocess(
  (input) =>
    typeof input === 'object' && input !== null && 'episode' in input
      ? input
      : { episode: input },
  frameSchema,
);
const snapshotsSchema = z.array(snapshotSchema).min(1).max(10000);
const recordingSchema = z.object({
  name: z.string().optional(),
  run_id: z.string().optional(),
  states: snapshotsSchema,
});
const exportSchema = z.object({
  run_id: z.string().optional(),
  manifest: z
    .object({ config: z.object({ name: z.string().optional() }) })
    .optional(),
  recorded_json: z.record(z.string(), z.unknown()),
});

export type EpisodeState = z.infer<typeof episodeSchema>;
export type Juror = z.infer<typeof jurorSchema>;
export type Snapshot = z.infer<typeof frameSchema>;
export type ReplayEpisode = {
  readonly id: string;
  readonly frames: readonly Snapshot[];
};
export type Experiment = {
  readonly id: string;
  readonly name: string;
  readonly episodes: readonly ReplayEpisode[];
};

/** Imports supported recordings; unknown/private fields are stripped by Zod. */
export function parseExperiment(
  input: unknown,
  filename = 'Imported experiment',
): Experiment {
  let frames: Snapshot[];
  let name = filename.replace(/\.(json|jsonl)$/i, '');
  let runId = name;
  try {
    if (Array.isArray(input)) {
      frames = snapshotsSchema.parse(input);
    } else if (
      typeof input === 'object' &&
      input !== null &&
      'recorded_json' in input
    ) {
      const exported = exportSchema.parse(input);
      const evidence = Object.entries(exported.recorded_json)
        .filter(([path]) => /(^|\/)evidence\.json$/.test(path))
        .map(([, value]) => value);
      frames = snapshotsSchema.parse(evidence);
      name = exported.manifest?.config.name ?? exported.run_id ?? name;
      runId = exported.run_id ?? name;
    } else if (
      typeof input === 'object' &&
      input !== null &&
      'states' in input
    ) {
      const recording = recordingSchema.parse(input);
      frames = recording.states;
      name = recording.name ?? name;
      runId = recording.run_id ?? name;
    } else {
      frames = [snapshotSchema.parse(input)];
    }
  } catch (error) {
    if (!(error instanceof z.ZodError)) throw error;
    // Never include input values: an unsupported file may contain private material.
    const issue = error.issues[0];
    throw new Error(
      `Invalid experiment at ${issue?.path.join('.') || 'root'}: ${issue?.message ?? 'unsupported format'}. Expected public episode states or harness evidence.`,
    );
  }
  const episodes = new Map<string, Snapshot[]>();
  for (const frame of frames) {
    const key = frame.episode.episode_id;
    const existing = episodes.get(key);
    const first = existing?.[0]?.episode;
    if (
      first &&
      (JSON.stringify(first.configuration) !==
        JSON.stringify(frame.episode.configuration) ||
        first.configuration_hash !== frame.episode.configuration_hash ||
        JSON.stringify(first.deployment) !==
          JSON.stringify(frame.episode.deployment))
    ) {
      throw new Error(
        `Episode ${key} changes its immutable configuration or deployment between snapshots.`,
      );
    }
    if (existing) existing.push(frame);
    else episodes.set(key, [frame]);
  }
  return {
    id: runId,
    name,
    episodes: [...episodes].map(([key, episodeFrames]) => ({
      id: key,
      frames: episodeFrames,
    })),
  };
}

export function parseExperimentText(
  text: string,
  filename: string,
): Experiment {
  if (!text.trim()) throw new Error('The experiment file is empty.');
  let input: unknown;
  try {
    input = filename.toLowerCase().endsWith('.jsonl')
      ? text
          .split(/\r?\n/)
          .filter((line) => line.trim())
          .map((line) => JSON.parse(line) as unknown)
      : (JSON.parse(text) as unknown);
  } catch {
    throw new Error(
      'Invalid JSON. Select a JSON experiment or a JSONL stream of public states.',
    );
  }
  return parseExperiment(input, filename);
}

/** ETH-scale native units, exactly; never convert uint256 amounts to Number. */
export function formatWei(value: string): string {
  const wei = BigInt(value);
  const whole = wei / 10n ** 18n;
  const fraction = (wei % 10n ** 18n)
    .toString()
    .padStart(18, '0')
    .replace(/0+$/, '');
  return `${whole}${fraction ? `.${fraction}` : ''}`;
}

export function playerStatus(juror: Juror): string {
  if (juror.revealed)
    return juror.verdict === 'CREATOR_SUPPORTED'
      ? 'Supports creator'
      : 'Supports challenger';
  return juror.commitment ? 'Vote sealed' : 'Awaiting commitment';
}

export const phaseLabels: Record<EpisodeState['phase'], string> = {
  REGISTERED: 'Registered',
  OPEN: 'Challenge window',
  COMMIT: 'Sealed voting',
  REVEAL: 'Vote reveal',
  SETTLED_CREATOR: 'Creator supported',
  SETTLED_CHALLENGER: 'Challenger supported',
  ABORTED: 'Aborted',
  EXPIRED_UNCHALLENGED: 'Unchallenged',
  EXPIRED_UNFUNDED: 'Unfunded',
};
