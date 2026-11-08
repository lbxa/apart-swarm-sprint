import { phaseLabels, type Snapshot } from './model';

export type RecordedChange = {
  readonly title: string;
  readonly detail: string;
  readonly actors: readonly string[];
};

/** Describes differences between actual snapshots, never inferred transactions. */
export function describeSnapshot(
  frame: Snapshot,
  previous?: Snapshot,
): RecordedChange {
  const current = frame.episode;
  const before = previous?.episode;
  if (!before)
    return {
      title: 'First recorded state',
      detail: `${phaseLabels[current.phase]} · earlier history is not included.`,
      actors: [],
    };
  const revealed = current.jurors.filter(
    (j) =>
      j.revealed &&
      !before.jurors.find((p) => p.actor_id === j.actor_id)?.revealed,
  );
  if (revealed.length)
    return {
      title: `${revealed.length === 1 ? revealed[0]!.actor_id : `${revealed.length} jurors`} revealed`,
      detail: 'Previously sealed judgments are now public.',
      actors: revealed.map((j) => j.actor_id),
    };
  const committed = current.jurors.filter(
    (j) =>
      j.commitment &&
      !before.jurors.find((p) => p.actor_id === j.actor_id)?.commitment,
  );
  if (committed.length)
    return {
      title: `${committed.length === 1 ? committed[0]!.actor_id : `${committed.length} jurors`} committed`,
      detail: 'Votes are sealed. Their contents are not yet observable.',
      actors: committed.map((j) => j.actor_id),
    };
  if (!before.content_hash && current.content_hash)
    return {
      title: 'Claim published',
      detail: 'The creator’s public claim is now recorded.',
      actors: [current.configuration.creator_id],
    };
  if (!before.evidence_hash && current.evidence_hash)
    return {
      title: 'Challenge recorded',
      detail: 'Counter-evidence is now available for the jury.',
      actors: [current.configuration.challenger_id],
    };
  if (current.phase !== before.phase)
    return {
      title: phaseLabels[current.phase],
      detail: frame.settlement
        ? 'Recorded settlement is available below.'
        : 'The public game phase changed.',
      actors: frame.settlement?.winner_id ? [frame.settlement.winner_id] : [],
    };
  return {
    title: 'State recorded',
    detail: 'Another public snapshot of this episode.',
    actors: [],
  };
}
