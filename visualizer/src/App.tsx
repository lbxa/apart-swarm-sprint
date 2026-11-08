import { useRef, useState, type ChangeEvent } from 'react';
import { ExperimentViewer } from './ExperimentViewer';
import { exampleExperiment } from './example';
import { parseExperimentText, type Experiment } from './model';

export default function App() {
  const [experiment, setExperiment] = useState<Experiment>(exampleExperiment);
  const [illustrative, setIllustrative] = useState(true);
  const [error, setError] = useState('');
  const [loading, setLoading] = useState(false);
  const [revision, setRevision] = useState(0);
  const fileInput = useRef<HTMLInputElement>(null);

  async function importFile(event: ChangeEvent<HTMLInputElement>) {
    const file = event.target.files?.[0];
    if (!file) return;
    setError('');
    setLoading(true);
    try {
      if (file.size > 25 * 1024 * 1024)
        throw new Error(
          'This file exceeds 25 MiB. Open per-episode evidence or a smaller recording.',
        );
      const imported = parseExperimentText(await file.text(), file.name);
      setExperiment(imported);
      setIllustrative(false);
      setRevision((current) => current + 1);
    } catch (failure) {
      setError(
        failure instanceof Error
          ? failure.message
          : 'Unable to read this experiment.',
      );
    } finally {
      setLoading(false);
      event.target.value = '';
    }
  }

  return (
    <div className="vv-app">
      <header className="vv-masthead">
        <a
          className="vv-wordmark"
          href="https://veracity.lbxa.net"
          target="_blank"
          rel="noreferrer"
        >
          <span className="vv-logo" aria-hidden="true">
            <i />
            <i />
          </span>
          VERACITY
          <span className="vv-wordmark-divider" />
          <span className="vv-wordmark-sub">EXPERIMENT OBSERVATORY</span>
        </a>
        <a
          className="vv-paper-link"
          href="https://veracity.lbxa.net"
          target="_blank"
          rel="noreferrer"
        >
          Read the paper <span aria-hidden="true">↗</span>
        </a>
      </header>
      <section className="vv-intro">
        <div>
          <div className="vv-eyebrow">INCENTIVES. DECISIONS. OUTCOMES.</div>
          <h1>
            Observe the game<span>.</span>
          </h1>
          <p>
            A closer look at how content trust unfolds, one state at a time.
          </p>
        </div>
        <div className="vv-import-area">
          <input
            ref={fileInput}
            type="file"
            accept=".json,.jsonl,application/json"
            onChange={importFile}
            aria-label="Experiment JSON file"
            className="vv-sr-only"
            tabIndex={-1}
          />
          <button
            className="vv-import-button"
            disabled={loading}
            onClick={() => fileInput.current?.click()}
          >
            <span aria-hidden="true">↑</span>
            {loading ? 'Opening…' : 'Open experiment'}
          </button>
          <span>JSON / JSONL · stays on your device</span>
        </div>
      </section>
      {error && (
        <div className="vv-import-error" role="alert">
          <strong>Couldn’t open this experiment.</strong> {error}
          <button className="vv-text-button" onClick={() => setError('')}>
            Dismiss ×
          </button>
        </div>
      )}
      <div className="vv-context-bar">
        <span>
          <i className="vv-context-dot" />
          {illustrative ? 'EXAMPLE COLLECTION' : 'YOUR EXPERIMENT'}
          <span className="vv-context-separator">/</span>
          {illustrative
            ? 'Explore the mechanism with illustrative states'
            : experiment.name}
        </span>
        {!illustrative && (
          <button
            className="vv-text-button"
            onClick={() => {
              setExperiment(exampleExperiment);
              setIllustrative(true);
              setRevision((current) => current + 1);
            }}
          >
            View examples ↗
          </button>
        )}
        {illustrative && (
          <span className="vv-context-note">No model behavior is claimed</span>
        )}
      </div>
      <ExperimentViewer
        key={revision}
        experiment={experiment}
        illustrative={illustrative}
        initialFrame={illustrative ? 5 : 0}
      />
      <footer className="vv-footer">
        <span>
          VERACITY{' '}
          <span className="vv-muted">
            / A research benchmark for emergent collusion
          </span>
        </span>
        <span>Designed for observation.</span>
      </footer>
    </div>
  );
}
