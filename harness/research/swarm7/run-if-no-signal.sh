#!/usr/bin/env bash
# Run the seven-juror fallback only if the fifteen-juror campaign produced no signal:
# no evaluated juror, in any model, revealed the false verdict in the collusion arm.
# The fallback gets whatever remains of the total cap after the main campaign's ledger
# (accounted charges and retained holds), so both campaigns together stay within it.
#
#   MAIN=harness/results/swarm-2026-11-08 OUT=harness/results/swarm7-2026-11-09 \
#     DOTENV=/path/.env TOTAL_USD=150 bash harness/research/swarm7/run-if-no-signal.sh MODEL ...
set -uo pipefail

root="$(cd "$(dirname "${BASH_SOURCE[0]}")/../../.." && pwd)"
main="$(cd "${MAIN:?set MAIN}" && pwd)"
: "${OUT:?set OUT}" "${DOTENV:?set DOTENV}" "${TOTAL_USD:?set TOTAL_USD}"

while pgrep -f "research/swarm/campaign.sh" >/dev/null; do sleep 60; done
echo "$(date '+%F %T') main campaign finished"

summary="$main/summary.json"
python3 -I "$root/harness/research/swarm/analyze.py" "$main"/run-* --output "$summary" || exit 1
false_votes="$(python3 -I -c '
import json, sys
summary = json.load(open(sys.argv[1]))
print(sum(arms.get("collusion", {}).get("colluded", 0) for arms in summary.values()))
' "$summary")"
echo "$(date '+%F %T') evaluated false votes in the collusion arm: $false_votes"
if [ "$false_votes" -gt 0 ]; then
  echo "$(date '+%F %T') signal found; fallback not run"
  exit 0
fi

remaining="$(python3 -I -c '
import sqlite3, sys
from decimal import Decimal, ROUND_DOWN
spent = sum(Decimal(r[0]) for r in sqlite3.connect(sys.argv[1]).execute(
    "SELECT accounted_usd FROM requests"))
print((Decimal(sys.argv[2]) - spent).quantize(Decimal("1"), rounding=ROUND_DOWN))
' "$main/spending.sqlite" "$TOTAL_USD")"
echo "$(date '+%F %T') no signal; fallback budget USD $remaining"
if [ "$remaining" -lt 10 ]; then
  echo "$(date '+%F %T') too little budget left for the fallback"
  exit 1
fi
CONFIGS="$root/harness/research/swarm7" BUDGET_USD="$remaining" OUT="$OUT" DOTENV="$DOTENV" \
  bash "$root/harness/research/swarm/campaign.sh" "$@"
