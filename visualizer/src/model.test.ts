import assert from 'node:assert/strict';
import { readFileSync } from 'node:fs';
import { test } from 'node:test';
import {
  parseExperiment,
  parseExperimentText,
  formatWei,
  playerStatus,
} from './model';
import { exampleExperiment } from './example';

const state = () =>
  structuredClone(exampleExperiment.episodes[0]!.frames[0]!.episode);

test('reads the exact public API EpisodeView and evidence wrapper', () => {
  const episode = state();
  assert.equal(parseExperiment(episode).episodes[0]!.id, episode.episode_id);
  const replay = parseExperiment({
    episode,
    private_transcripts: { secret: 'do not retain' },
  });
  assert.equal(replay.episodes[0]!.frames.length, 1);
  assert.ok(!JSON.stringify(replay).includes('do not retain'));
});

test('groups interleaved episode snapshots without inventing history', () => {
  const first = state();
  const second = structuredClone(first);
  second.episode_id = 'other';
  second.configuration.episode_id = 'other';
  const next = structuredClone(first);
  next.phase = 'OPEN';
  const replay = parseExperiment([first, second, next]);
  assert.equal(replay.episodes.length, 2);
  assert.deepEqual(
    replay.episodes[0]!.frames.map((f) => f.episode.phase),
    ['REGISTERED', 'OPEN'],
  );
  assert.equal(replay.episodes[1]!.frames.length, 1);
});

test('supports retained raw export with multiple episode evidence files', () => {
  const replay = parseExperiment({
    run_id: 'run-1',
    manifest: { config: { name: 'Recorded experiment' } },
    recorded_json: {
      'a/evidence.json': { episode: state() },
      'a/summary.json': { unrelated: true },
    },
  });
  assert.equal(replay.name, 'Recorded experiment');
  assert.equal(replay.episodes[0]!.frames.length, 1);
});

test('rejects malformed exports instead of silently dropping an episode', () => {
  assert.throws(
    () =>
      parseExperiment({
        recorded_json: {
          'a/evidence.json': { episode: state() },
          'b/evidence.json': { episode: {} },
        },
      }),
    /Invalid/,
  );
});

test('rejects unsafe amounts, unknown phases, role drift and wrong episode identities', () => {
  const episode = state();
  assert.throws(
    () => parseExperiment({ ...episode, phase: 'VOTING' }),
    /Invalid/,
  );
  assert.throws(
    () => parseExperiment({ ...episode, total_deposited_wei: 1e20 }),
    /Invalid/,
  );
  const changed = structuredClone(episode);
  changed.configuration.creator_id = 'replacement';
  assert.throws(() => parseExperiment([episode, changed]), /configuration/);
  assert.throws(
    () => parseExperiment({ ...episode, episode_id: 'mismatch' }),
    /episode/,
  );
});

test('rejects inconsistent votes and settlement metadata', () => {
  const episode = state();
  episode.jurors[0]!.verdict = 'CREATOR_SUPPORTED';
  assert.throws(() => parseExperiment(episode), /reveal/);
  assert.throws(
    () =>
      parseExperiment({
        episode: state(),
        settlement: {
          ...exampleExperiment.episodes[0]!.frames.at(-1)!.settlement,
          episode_id: 'wrong',
        },
      }),
    /settlement/,
  );
});

test('settlements cannot expose votes before reveal or name an unrelated winner', () => {
  const finalFrame = structuredClone(
    exampleExperiment.episodes[0]!.frames.at(-1)!,
  );
  assert.throws(
    () =>
      parseExperiment({
        episode: exampleExperiment.episodes[0]!.frames[5]!.episode,
        settlement: { ...finalFrame.settlement, outcome: 'COMMIT' },
      }),
    /Invalid/,
  );
  finalFrame.settlement!.winner_id = 'unrelated-actor';
  assert.throws(() => parseExperiment(finalFrame), /winner/);
});

test('preserves chronology from JSONL and rejects empty input', () => {
  const replay = parseExperimentText(
    `${JSON.stringify(state())}\n\n${JSON.stringify(state())}\n`,
    'states.jsonl',
  );
  assert.equal(replay.episodes[0]!.frames.length, 2);
  assert.throws(() => parseExperimentText('', 'empty.jsonl'), /empty/i);
  assert.throws(() => parseExperiment([]), /Invalid/);
});

test('keeps committed votes secret and uses exact integer formatting', () => {
  const juror = {
    actor_id: 'j',
    commitment: '0xabc',
    revealed: false,
    verdict: null,
    assessment_hash: null,
  };
  assert.equal(playerStatus(juror), 'Vote sealed');
  assert.equal(formatWei('1000000000000000001'), '1.000000000000000001');
  assert.equal(formatWei('1'), '0.000000000000000001');
  assert.equal(formatWei('0'), '0');
  assert.equal(formatWei('1200000000000000000'), '1.2');
});

test('invalid decimal strings produce safe validation errors without echoing input', () => {
  assert.throws(
    () =>
      parseExperiment({ ...state(), total_deposited_wei: 'private material' }),
    (error: unknown) =>
      error instanceof Error &&
      error.message.startsWith('Invalid experiment') &&
      !error.message.includes('private material'),
  );
});

test('parsing owns its data and does not mutate or alias the caller’s snapshots', () => {
  const original = state();
  const before = structuredClone(original);
  const parsed = parseExperiment(original);
  parsed.episodes[0]!.frames[0]!.episode.configuration.juror_ids[0] = 'changed';
  assert.deepEqual(original, before);
});

test('examples conform to the retained core OpenAPI required public fields', () => {
  const api = JSON.parse(
    readFileSync(new URL('../../docs/openapi.json', import.meta.url), 'utf8'),
  );
  for (const episode of exampleExperiment.episodes) {
    for (const frame of episode.frames) {
      for (const field of api.components.schemas.EpisodeView.required) {
        assert.ok(field in frame.episode, `EpisodeView missing ${field}`);
      }
      for (const field of api.components.schemas.RegisterEpisode.required) {
        assert.ok(
          field in frame.episode.configuration,
          `RegisterEpisode missing ${field}`,
        );
      }
    }
  }
});
