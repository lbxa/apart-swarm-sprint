#!/usr/bin/env bash
set -euo pipefail
repo_root="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"
fixture="$(mktemp -d "${TMPDIR:-/tmp}/veracity-decision-index-test.XXXXXX")"
trap 'rm -rf "$fixture"' EXIT
mkdir -p "$fixture/scripts" "$fixture/docs/decisions"
cp "$repo_root/scripts/decision-index.py" "$fixture/scripts/"
cp "$repo_root/docs/decisions/_template.md" "$repo_root/docs/decisions/README.md" "$fixture/docs/decisions/"
generator="$fixture/scripts/decision-index.py"
decisions="$fixture/docs/decisions"

write_record() {
  printf '# %s\n\n- **Date:** %s\n- **Status:** Accepted\n' "$2" "$3" >"$decisions/$1.md"
}

write_record older 'Older choice' 2026-01-02
write_record newer 'Newer choice' 2026-03-04

if python3 "$generator" --check >"$fixture/output" 2>&1; then
  printf 'Decision index check accepted a missing index\n' >&2
  exit 1
fi

python3 "$generator"
python3 "$generator" --check
grep -q '^- \[Newer choice\](./newer.md) — 2026-03-04$' "$decisions/INDEX.md"
[ "$(grep -n 'Newer choice' "$decisions/INDEX.md" | cut -d: -f1)" -lt "$(grep -n 'Older choice' "$decisions/INDEX.md" | cut -d: -f1)" ]
[ "$(grep -c '^- \[' "$decisions/INDEX.md")" = 2 ]

write_record latest 'Latest choice' 2026-05-06
if python3 "$generator" --check >"$fixture/output" 2>&1; then
  printf 'Decision index check accepted a stale index\n' >&2
  exit 1
fi

printf '# Undated choice\n' >"$decisions/undated.md"
if python3 "$generator" >"$fixture/output" 2>&1; then
  printf 'Decision index accepted a record without a date\n' >&2
  exit 1
fi
grep -q 'undated.md' "$fixture/output"
printf 'Decision index: ordering, staleness, and malformed-record checks passed.\n'
