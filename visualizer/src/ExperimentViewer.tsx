import { useEffect, useId, useMemo, useState, type CSSProperties } from 'react';
import {
  formatWei,
  phaseLabels,
  playerStatus,
  type Experiment,
  type Snapshot,
} from './model';
import { describeSnapshot } from './replay';
import './style.css';

export type ExperimentViewerProps = {
  readonly experiment: Experiment;
  readonly illustrative?: boolean;
  readonly initialFrame?: number;
};

export function ExperimentViewer({
  experiment,
  illustrative = false,
  initialFrame = 0,
}: ExperimentViewerProps) {
  const [episodeId, setEpisodeId] = useState(experiment.episodes[0]?.id ?? '');
  const episode =
    experiment.episodes.find((item) => item.id === episodeId) ??
    experiment.episodes[0];
  if (!episode || episode.frames.length === 0)
    return <div className="vv-empty">No recorded episodes to display.</div>;
  return (
    <div className="vv-viewer">
      <aside className="vv-sidebar" aria-label="Episodes">
        <div className="vv-eyebrow vv-sidebar-label">
          EXPERIMENT / {illustrative ? 'EXAMPLE' : 'RECORDED'}
        </div>
        <h2>{experiment.name}</h2>
        <p className="vv-muted vv-sidebar-note">
          {experiment.episodes.length} episode
          {experiment.episodes.length === 1 ? '' : 's'} to explore
        </p>
        <nav className="vv-episode-list" aria-label="Select episode">
          {experiment.episodes.map((item, index) => (
            <button
              className={`vv-episode ${item.id === episode.id ? 'is-selected' : ''}`}
              key={item.id}
              aria-current={item.id === episode.id ? 'true' : undefined}
              onClick={() => setEpisodeId(item.id)}
            >
              <span className="vv-episode-number">
                {String(index + 1).padStart(2, '0')}
              </span>
              <span>
                <strong>{item.id}</strong>
                <small>
                  {item.frames.length} snapshot
                  {item.frames.length === 1 ? '' : 's'}
                </small>
              </span>
              <span className="vv-episode-arrow" aria-hidden="true">
                ↗
              </span>
            </button>
          ))}
        </nav>
        <div className="vv-sidebar-foot">
          <span className="vv-mini-orbit" aria-hidden="true">
            ◌
          </span>
          <p>
            Follow the incentives.
            <br />
            Observe the decisions.
          </p>
          <span className="vv-eyebrow">A CONTENT TRUST EXPERIMENT</span>
        </div>
      </aside>
      <Replay
        key={`${experiment.id}/${episode.id}`}
        frames={episode.frames}
        illustrative={illustrative}
        initialFrame={initialFrame}
      />
    </div>
  );
}

function Replay({
  frames,
  illustrative,
  initialFrame,
}: {
  readonly frames: readonly Snapshot[];
  readonly illustrative: boolean;
  readonly initialFrame: number;
}) {
  const [cursor, setCursor] = useState(
    Math.max(0, Math.min(initialFrame, frames.length - 1)),
  );
  const [playing, setPlaying] = useState(false);
  const [speed, setSpeed] = useState(1);
  const [selectedActor, setSelectedActor] = useState<string | null>(null);
  const [tab, setTab] = useState<'activity' | 'evidence' | 'state'>('activity');
  const [sourceFrames, setSourceFrames] = useState(frames);
  // Reset component-owned playback when an embedding app supplies another recording.
  if (sourceFrames !== frames) {
    setSourceFrames(frames);
    setCursor(Math.max(0, Math.min(initialFrame, frames.length - 1)));
    setPlaying(false);
    setSelectedActor(null);
  }
  const rangeId = useId();
  const tabId = useId();
  const frame = frames[Math.min(cursor, frames.length - 1)]!;
  const state = frame.episode;
  const config = state.configuration;
  const change = describeSnapshot(frame, frames[cursor - 1]);
  const changes = useMemo(
    () =>
      frames.map((item, index) => describeSnapshot(item, frames[index - 1])),
    [frames],
  );
  const events = useMemo(
    () =>
      changes
        .map((event, index) => ({ ...event, index }))
        .filter(
          (event) => !selectedActor || event.actors.includes(selectedActor),
        ),
    [changes, selectedActor],
  );
  const currentEventIndex = events.findLastIndex(
    (event) => event.index <= cursor,
  );
  const visibleEvents = events.slice(
    Math.max(0, currentEventIndex - 3),
    Math.max(4, currentEventIndex + 2),
  );

  useEffect(() => {
    if (!playing || cursor >= frames.length - 1) return;
    const timer = window.setTimeout(
      () => setCursor((position) => position + 1),
      1800 / speed,
    );
    return () => window.clearTimeout(timer);
  }, [playing, cursor, frames.length, speed]);

  const isPlaying = playing && cursor < frames.length - 1;
  const seek = (position: number) => {
    setPlaying(false);
    setCursor(position);
  };
  const togglePlayback = () => {
    if (isPlaying) setPlaying(false);
    else {
      if (cursor === frames.length - 1) setCursor(0);
      setPlaying(true);
    }
  };
  const selectActor = (actor: string) =>
    setSelectedActor((current) => (current === actor ? null : actor));
  const selectedJuror = state.jurors.find((j) => j.actor_id === selectedActor);
  const selectedRole =
    selectedActor === config.creator_id
      ? 'Creator'
      : selectedActor === config.challenger_id
        ? 'Challenger'
        : selectedActor === config.treasury_id
          ? 'Protocol treasury'
          : 'Juror';
  const terminal = !['REGISTERED', 'OPEN', 'COMMIT', 'REVEAL'].includes(
    state.phase,
  );
  const revealedCount = state.jurors.filter((j) => j.revealed).length;

  return (
    <main className="vv-replay">
      <div className="vv-replay-header">
        <div>
          <div className="vv-eyebrow">EPISODE / {state.episode_id}</div>
          <h2>{state.configuration.scenario_id || 'Content verification'}</h2>
        </div>
        <span className={`vv-source ${illustrative ? '' : 'is-recorded'}`}>
          <i />
          {illustrative ? 'Illustrative replay' : 'Recorded states'}
        </span>
      </div>
      <div className="vv-arena-panel">
        <div className="vv-arena-toolbar">
          <span className="vv-eyebrow">01 — THE ARENA</span>
          <span className="vv-snapshot-counter">
            SNAPSHOT {String(cursor + 1).padStart(2, '0')} /{' '}
            {String(frames.length).padStart(2, '0')}
          </span>
        </div>
        <div className={`vv-arena ${isPlaying ? 'is-playing' : ''}`}>
          <div className="vv-arena-grid" aria-hidden="true" />
          <div className="vv-arena-lines" aria-hidden="true">
            <svg viewBox="0 0 800 440" preserveAspectRatio="none">
              <path
                className={`vv-flow vv-flow-creator ${state.content_hash ? 'is-active' : ''}`}
                d="M160 140 Q280 140 340 180"
              />
              <path
                className={`vv-flow vv-flow-challenger ${state.evidence_hash ? 'is-active' : ''}`}
                d="M640 140 Q520 140 460 180"
              />
              <path
                className={`vv-flow ${state.phase === 'COMMIT' || state.phase === 'REVEAL' || terminal ? 'is-active' : ''}`}
                d="M400 208 L400 310 M400 270 Q250 270 235 340 M400 270 Q550 270 565 340"
              />
            </svg>
          </div>
          <div className="vv-party vv-creator">
            <Player
              actor={config.creator_id}
              role="Creator"
              monogram="C"
              tone="creator"
              status={state.content_hash ? 'Claim published' : 'Awaiting claim'}
              active={change.actors.includes(config.creator_id)}
              selected={selectedActor === config.creator_id}
              onSelect={selectActor}
            />
            <span className="vv-stake">
              β = {formatWei(config.parameters.beta_wei)} <small>native</small>
            </span>
          </div>
          <div className="vv-party vv-challenger">
            <Player
              actor={config.challenger_id}
              role="Challenger"
              monogram="X"
              tone="challenger"
              status={
                state.evidence_hash
                  ? 'Challenge submitted'
                  : 'Awaiting challenge'
              }
              active={change.actors.includes(config.challenger_id)}
              selected={selectedActor === config.challenger_id}
              onSelect={selectActor}
            />
            <span className="vv-stake">
              β = {formatWei(config.parameters.beta_wei)} <small>native</small>
            </span>
          </div>
          <div className={`vv-contest ${terminal ? 'is-terminal' : ''}`}>
            <div className="vv-contest-symbol" aria-hidden="true">
              <span />
              <span />
            </div>
            <span className="vv-eyebrow">
              {terminal ? 'OUTCOME' : 'CONTENT TRUST'}
            </span>
            <strong key={state.phase} className="vv-phase-name">
              {phaseLabels[state.phase]}
            </strong>
            <span className="vv-contest-votes">
              {revealedCount
                ? `${state.creator_votes} : ${state.challenger_votes} votes`
                : 'Independent judgments. Shared stakes.'}
            </span>
          </div>
          <div className="vv-jury">
            {state.jurors.map((juror, index) => (
              <Player
                key={juror.actor_id}
                actor={juror.actor_id}
                role={`Juror ${String(index + 1).padStart(2, '0')}`}
                monogram={String(index + 1).padStart(2, '0')}
                tone={
                  juror.revealed
                    ? juror.verdict === 'CREATOR_SUPPORTED'
                      ? 'creator'
                      : 'challenger'
                    : 'juror'
                }
                status={playerStatus(juror)}
                sealed={!!juror.commitment && !juror.revealed}
                active={change.actors.includes(juror.actor_id)}
                selected={selectedActor === juror.actor_id}
                onSelect={selectActor}
              />
            ))}
          </div>
          <span className="vv-arena-caption">
            Select a player to inspect their state
          </span>
        </div>
        <div className="vv-arena-legend">
          <span>
            <i className="vv-legend-dot vv-tone-creator" />
            Creator
          </span>
          <span>
            <i className="vv-legend-dot vv-tone-challenger" />
            Challenger
          </span>
          <span>
            <i className="vv-legend-dot vv-tone-juror" />
            Jury
          </span>
          <span className="vv-legend-note">
            {state.required_votes} votes required for a majority
          </span>
        </div>
        <div className="vv-transport">
          <div className="vv-transport-top">
            <div className="vv-playback-buttons">
              <button
                className="vv-icon-button"
                aria-label="First snapshot"
                disabled={cursor === 0}
                onClick={() => seek(0)}
              >
                ↤
              </button>
              <button
                className="vv-icon-button"
                aria-label="Previous snapshot"
                disabled={cursor === 0}
                onClick={() => seek(cursor - 1)}
              >
                ‹
              </button>
              <button
                className="vv-play"
                aria-label={
                  isPlaying
                    ? 'Pause replay'
                    : cursor === frames.length - 1
                      ? 'Replay from beginning'
                      : 'Play replay'
                }
                disabled={frames.length < 2}
                onClick={togglePlayback}
              >
                <span aria-hidden="true">{isPlaying ? 'Ⅱ' : '▶'}</span>
                {isPlaying ? 'Pause' : 'Play'}
              </button>
              <button
                className="vv-icon-button"
                aria-label="Next snapshot"
                disabled={cursor === frames.length - 1}
                onClick={() => seek(cursor + 1)}
              >
                ›
              </button>
              <button
                className="vv-icon-button"
                aria-label="Last snapshot"
                disabled={cursor === frames.length - 1}
                onClick={() => seek(frames.length - 1)}
              >
                ↦
              </button>
            </div>
            <div className="vv-transport-status">
              <span className={isPlaying ? 'vv-live-dot' : 'vv-paused-dot'} />
              {isPlaying ? 'Playing' : 'Paused'}
              <span className="vv-transport-divider" />
              <label>
                Speed{' '}
                <select
                  aria-label="Playback speed"
                  value={speed}
                  onChange={(event) => setSpeed(Number(event.target.value))}
                >
                  <option value={0.5}>0.5×</option>
                  <option value={1}>1×</option>
                  <option value={2}>2×</option>
                  <option value={4}>4×</option>
                </select>
              </label>
            </div>
          </div>
          <label className="vv-sr-only" htmlFor={rangeId}>
            Replay position
          </label>
          <input
            id={rangeId}
            className="vv-scrubber"
            type="range"
            min={0}
            max={Math.max(0, frames.length - 1)}
            value={cursor}
            disabled={frames.length < 2}
            onChange={(event) => seek(Number(event.target.value))}
            aria-valuetext={`Snapshot ${cursor + 1} of ${frames.length}: ${phaseLabels[state.phase]}`}
            style={
              {
                '--vv-progress': `${frames.length > 1 ? (cursor / (frames.length - 1)) * 100 : 0}%`,
              } as CSSProperties
            }
          />
          <div className="vv-scrubber-labels">
            <span>FIRST RECORDED STATE</span>
            <span>
              {frames.length === 1
                ? 'Single snapshot · no playback history'
                : 'LAST RECORDED STATE'}
            </span>
          </div>
        </div>
      </div>
      <div className="vv-metrics" aria-label="Current snapshot metrics">
        <Metric
          label="LOCKED IN ESCROW"
          value={formatWei(state.locked_liability_wei)}
          unit="native"
        />
        <Metric
          label="VOTES REVEALED"
          value={`${revealedCount}`}
          unit={`/ ${state.jurors.length}`}
        />
        <Metric
          label="TOTAL DEPOSITED"
          value={formatWei(state.total_deposited_wei)}
          unit="native"
        />
        <Metric
          label="TOTAL CREDITED"
          value={formatWei(state.total_credited_wei)}
          unit="native"
        />
      </div>
      {selectedActor && (
        <section className="vv-player-inspector" aria-label="Selected player">
          <div>
            <span className="vv-eyebrow">{selectedRole}</span>
            <h3>{selectedActor}</h3>
          </div>
          <p>
            {selectedJuror
              ? playerStatus(selectedJuror)
              : selectedActor === config.creator_id
                ? state.content_hash
                  ? 'Public claim recorded'
                  : 'No public claim recorded'
                : selectedActor === config.challenger_id
                  ? state.evidence_hash
                    ? 'Public challenge recorded'
                    : 'No public challenge recorded'
                  : 'Protocol treasury'}
          </p>
          <button
            className="vv-text-button"
            onClick={() => setSelectedActor(null)}
          >
            Clear selection ×
          </button>
          {selectedJuror?.commitment && (
            <code title={selectedJuror.commitment}>
              Commitment: {selectedJuror.commitment}
            </code>
          )}
        </section>
      )}
      <section className="vv-details">
        <div
          className="vv-detail-tabs"
          role="tablist"
          aria-label="Episode details"
        >
          {(['activity', 'evidence', 'state'] as const).map((item, index) => (
            <button
              key={item}
              role="tab"
              id={`${tabId}-${item}`}
              aria-controls={`${tabId}-panel`}
              aria-selected={tab === item}
              tabIndex={tab === item ? 0 : -1}
              onKeyDown={(event) => {
                const items = ['activity', 'evidence', 'state'] as const;
                const next =
                  event.key === 'ArrowRight'
                    ? (index + 1) % 3
                    : event.key === 'ArrowLeft'
                      ? (index + 2) % 3
                      : event.key === 'Home'
                        ? 0
                        : event.key === 'End'
                          ? 2
                          : null;
                if (next === null) return;
                event.preventDefault();
                setTab(items[next]!);
                document.getElementById(`${tabId}-${items[next]}`)?.focus();
              }}
              onClick={() => setTab(item)}
            >
              {item === 'activity'
                ? '02 — Activity'
                : item === 'evidence'
                  ? 'Public evidence'
                  : 'State data'}
            </button>
          ))}
          <span>
            {selectedActor
              ? `Filtered: ${selectedActor}`
              : 'RECORDED OBSERVATIONS'}
          </span>
        </div>
        <div
          role="tabpanel"
          id={`${tabId}-panel`}
          aria-labelledby={`${tabId}-${tab}`}
          tabIndex={0}
        >
          {tab === 'activity' ? (
            <ol className="vv-activity">
              {events.length === 0 ? (
                <li className="vv-empty">
                  No observed changes for this player in the recorded snapshots.
                </li>
              ) : (
                visibleEvents.map((event) => (
                  <li
                    key={event.index}
                    className={`${event.index === cursor ? 'is-current' : ''} ${event.index > cursor ? 'is-future' : ''}`}
                  >
                    <button
                      className="vv-event"
                      onClick={() => seek(event.index)}
                      aria-label={`Go to snapshot ${event.index + 1}: ${event.title}`}
                    >
                      <span className="vv-event-number">
                        {String(event.index + 1).padStart(2, '0')}
                      </span>
                      <span>
                        <strong>{event.title}</strong>
                        <small>{event.detail}</small>
                      </span>
                      <span className="vv-event-marker">
                        {event.index === cursor
                          ? 'NOW'
                          : event.index > cursor
                            ? 'LATER'
                            : '↗'}
                      </span>
                    </button>
                  </li>
                ))
              )}
            </ol>
          ) : tab === 'evidence' ? (
            <div className="vv-evidence">
              <article>
                <span className="vv-eyebrow">CREATOR’S CLAIM</span>
                <p>{state.content ?? 'No claim text in this snapshot.'}</p>
              </article>
              <article>
                <span className="vv-eyebrow">CHALLENGER’S EVIDENCE</span>
                <p>{state.evidence ?? 'No challenge text in this snapshot.'}</p>
              </article>
            </div>
          ) : (
            <pre className="vv-state-data">
              {JSON.stringify(frame, null, 2)}
            </pre>
          )}
        </div>
      </section>
      {frame.settlement && (
        <section className="vv-settlement">
          <div className="vv-section-heading">
            <div>
              <span className="vv-eyebrow">03 — SETTLEMENT</span>
              <h3>{phaseLabels[frame.settlement.outcome]}</h3>
            </div>
            <span className="vv-muted">
              Recorded entitlements · native units
            </span>
          </div>
          <table>
            <thead>
              <tr>
                <th scope="col">Recipient</th>
                <th scope="col">Type</th>
                <th scope="col">Amount</th>
              </tr>
            </thead>
            <tbody>
              {frame.settlement.winner_id && (
                <tr>
                  <th scope="row">{frame.settlement.winner_id}</th>
                  <td>Winner payout</td>
                  <td>{formatWei(frame.settlement.winner_payout)}</td>
                </tr>
              )}
              {Object.entries(frame.settlement.juror_payouts).map(
                ([actor, payout]) => (
                  <tr key={`juror-${actor}`}>
                    <th scope="row">{actor}</th>
                    <td>Juror entitlement</td>
                    <td>{formatWei(payout)}</td>
                  </tr>
                ),
              )}
              {Object.entries(frame.settlement.refunds).map(
                ([actor, payout]) => (
                  <tr key={`refund-${actor}`}>
                    <th scope="row">{actor}</th>
                    <td>Refund</td>
                    <td>{formatWei(payout)}</td>
                  </tr>
                ),
              )}
              <tr>
                <th scope="row">{config.treasury_id}</th>
                <td>Protocol fee</td>
                <td>{formatWei(frame.settlement.protocol_fee)}</td>
              </tr>
              {Object.entries(frame.settlement.forfeited_bonds).map(
                ([actor, payout]) => (
                  <tr key={`forfeit-${actor}`}>
                    <th scope="row">{actor}</th>
                    <td>Forfeited bond</td>
                    <td>{formatWei(payout)}</td>
                  </tr>
                ),
              )}
            </tbody>
          </table>
        </section>
      )}
      <div className="vv-replay-foot">
        <span>
          {illustrative
            ? 'Teaching example. Not benchmark evidence.'
            : 'Local file · public state only · no uploads'}
        </span>
        <span>
          {frame.recorded_at
            ? new Date(frame.recorded_at).toLocaleString()
            : 'Snapshot order preserved'}
        </span>
      </div>
    </main>
  );
}

function Player({
  actor,
  role,
  monogram,
  tone,
  status,
  selected,
  active,
  sealed,
  onSelect,
}: {
  readonly actor: string;
  readonly role: string;
  readonly monogram: string;
  readonly tone: 'creator' | 'challenger' | 'juror';
  readonly status: string;
  readonly selected: boolean;
  readonly active: boolean;
  readonly sealed?: boolean;
  readonly onSelect: (actor: string) => void;
}) {
  return (
    <button
      className={`vv-player vv-tone-${tone} ${selected ? 'is-selected' : ''} ${active ? 'is-active' : ''}`}
      onClick={() => onSelect(actor)}
      aria-label={`${role}: ${actor}, ${status}`}
      aria-pressed={selected}
    >
      <span className="vv-avatar">
        <span>{monogram}</span>
        {sealed && (
          <span className="vv-seal" aria-hidden="true">
            •
          </span>
        )}
      </span>
      <strong>{role}</strong>
      <span className="vv-player-id" title={actor}>
        {actor}
      </span>
      <span
        className={`vv-player-status ${sealed ? 'is-sealed' : ''}`}
        key={status}
      >
        {status}
      </span>
    </button>
  );
}

function Metric({
  label,
  value,
  unit,
}: {
  readonly label: string;
  readonly value: string;
  readonly unit: string;
}) {
  return (
    <div className="vv-metric">
      <span className="vv-eyebrow">{label}</span>
      <div title={`${value} ${unit}`}>
        <strong key={value}>{value}</strong>
        <span>{unit}</span>
      </div>
    </div>
  );
}
