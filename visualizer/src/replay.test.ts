import assert from 'node:assert/strict';
import { test } from 'node:test';
import { exampleExperiment } from './example';
import { describeSnapshot } from './replay';

test('describes observed commitments and reveals without exposing a sealed verdict', () => {
  const frames = exampleExperiment.episodes[0]!.frames;
  assert.match(describeSnapshot(frames[3]!, frames[2]).title, /committed/);
  assert.ok(
    !JSON.stringify(describeSnapshot(frames[3]!, frames[2])).includes(
      'CREATOR_SUPPORTED',
    ),
  );
  assert.match(describeSnapshot(frames[7]!, frames[6]).title, /revealed/);
  assert.equal(
    describeSnapshot(frames[10]!, frames[9]).title,
    'Creator supported',
  );
});

test('terminal evidence starts at its first recorded state without fabricated steps', () => {
  const last = exampleExperiment.episodes[0]!.frames.at(-1)!;
  assert.equal(describeSnapshot(last).title, 'First recorded state');
  assert.match(
    describeSnapshot(last).detail,
    /earlier history is not included/,
  );
});
