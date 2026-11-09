# Report examples use monochrome model tabs

- **Date:** 2026-11-09
- **Status:** Accepted
- **Deciders:** Lucas Barbosa
- **Area:** report presentation

## Context

Lucas found the initial colored prompt/response panels visually tacky and
supplied an image of examples from *Situational Awareness* as the desired
reference: white interiors, thin black rounded borders, small black model
tabs and bold serif labels inside a shared frame.

## Decision

Use that visual treatment for the report's model examples. Related passages
share a frame with restrained dashed separators; source details appear as
small serif captions below. This supersedes the blue panel treatment in
[the earlier excerpt decision](report-model-excerpts-link-inputs-to-executed-actions.md),
while preserving its evidence and interpretation requirements.

## Consequences

The report keeps its existing fonts and page geometry. Scripted inputs,
returned reasoning and submitted assessments retain explicit labels, and no
quoted source text or scientific result changes. Short paired inputs stay on
one page; the shared environment still supports longer breakable examples.
The supplied screenshot is a layout reference, not research evidence or an
instruction to reproduce its examples.

See [panel definitions](../../report/agentic/trace-panels.tex) and
[rendered review](../../report/agentic/review.md).
