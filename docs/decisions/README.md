# Decision records

Short, dated write-ups of choices with real trade-offs: the ones someone will
later look at and ask "why is it like this?". They hold the *why* that is not in
the code, the spec, or the commit message.

Records are **append-only**. Do not rewrite an old record to match a new
reality. Write a new one, set the old one's status to `Superseded by
new-slug.md`, and link the two, so the history of our reasoning stays intact.

## When to write one

Write a record when a choice:

- has trade-offs a reasonable person would question later,
- is driven by a constraint the code does not show (a spec or constitution
  rule, an evidence threshold, a chain or provider limitation, a budget), or
- keeps coming up because nobody wrote it down.

Skip it for routine implementation choices with an obvious answer. A small
package-level fact belongs in that package's README `## Changelog`; a rule of the
game belongs in `SPEC.md`, `CONSTITUTION.md`, or `docs/benchmark.md`.

## How to add one

Agents (Claude Code and Codex) write these as part of the change, following
`AGENTS.md`. By hand it is the same:

1. Copy [`_template.md`](./_template.md) to `short-statement-of-the-decision.md`.
   **No number**: records are identified by slug and ordered by `Date`, so two
   branches adding records never collide on a number.
2. Fill it in. Keep it short: context, decision, consequences.
3. Ship it in the same commit or PR as the change it explains.

**Don't invent the why.** If part of the rationale cannot be verified from the
conversation, the code, or the docs, mark it with
`> ⚠️ NEEDS CONFIRMATION (who should confirm)` instead of guessing.

## Index

**[INDEX.md](./INDEX.md)** lists every record, newest first. It is generated:
never edit it by hand. The agent Stop hook rebuilds it before verification,
`bash scripts/verify.sh` fails on a stale one, and
`python3 scripts/decision-index.py` rebuilds it manually. It is marked
`merge=union` in `.gitattributes`, so two branches adding records merge cleanly
and the next rebuild restores the order.
