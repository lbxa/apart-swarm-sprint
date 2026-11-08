#!/usr/bin/env bash
# Run the swarm peer-pressure arms: one case per run, seeds 811-815, honest and collusion
# alternating per seed, two models at a time (each model has its own Workers AI rate).
#
#   OUT=harness/results/swarm-2026-11-08 DOTENV=/path/.env BUDGET_USD=150 \
#     bash harness/research/swarm/campaign.sh MODEL [MODEL ...]
#
# CONFIGS selects the experiment directory (default harness/research/swarm; the seven-
# juror fallback is harness/research/swarm7).
#
# A run that fails before any model call (sandbox, network, engine setup) is moved to
# $OUT/excluded/failed/ and retried, at most three attempts. A run that fails after play
# began is kept as an unresolved case and never re-run: substituting only the cases that
# went wrong would bias the measured rates. Every attempt keeps its own log.
set -uo pipefail

root="$(cd "$(dirname "${BASH_SOURCE[0]}")/../../.." && pwd)"
out="$(mkdir -p "${OUT:?set OUT}" && cd "$OUT" && pwd)"
dotenv="${DOTENV:?set DOTENV}"
budget="${BUDGET_USD:?set BUDGET_USD}"
seeds=(${SEEDS:-811 812 813 814 815})
configs="$(cd "${CONFIGS:-$root/harness/research/swarm}" && pwd)"
export VERACITY_RATE_DB="$out/request-rate.sqlite"
mkdir -p "$out/logs" "$out/excluded/failed"

played() {  # Did the run reach any model call?
  find "$out/$1" -name '*.calls.jsonl' -size +0 2>/dev/null | grep -q .
}

run_case() {
  local model="$1" arm="$2" seed="$3" attempt log run
  for attempt in 1 2 3; do
    log="$out/logs/${model##*/}-$arm-$seed-$attempt.log"
    if env -u VIRTUAL_ENV uv run --project "$root/harness" --locked veracity-harness run \
      --config "$configs/$arm-peers.toml" --model "$model" \
      --seed "$seed" --output "$out" --dotenv "$dotenv" \
      --budget-ledger "$out/spending.sqlite" --budget-usd "$budget" >"$log" 2>&1; then
      echo "$(date '+%F %T') ok ${model##*/} $arm $seed attempt=$attempt"
      return 0
    fi
    run="$(grep -o 'run=run-[0-9a-f]*' "$log" | head -1 | cut -d= -f2)"
    if grep -q 'SpendingLimitReached' "$log"; then
      echo "$(date '+%F %T') STOP budget ${model##*/} $arm $seed"
      return 2
    fi
    if [ -n "$run" ] && played "$run"; then
      echo "$(date '+%F %T') kept-failed ${model##*/} $arm $seed $run (play had begun)"
      return 1
    fi
    [ -n "$run" ] && mv "$out/$run" "$out/excluded/failed/"
    echo "$(date '+%F %T') retry ${model##*/} $arm $seed after setup failure (attempt $attempt)"
    sleep 20
  done
  echo "$(date '+%F %T') GAVE-UP ${model##*/} $arm $seed"
  return 1
}

run_model() {
  local model="$1" seed i=0 arms
  for seed in "${seeds[@]}"; do
    # Alternate which arm runs first so time of day does not track the arm.
    if (( i++ % 2 )); then arms=(collusion honest); else arms=(honest collusion); fi
    for arm in "${arms[@]}"; do
      run_case "$model" "$arm" "$seed"
      [ $? -eq 2 ] && return 2
    done
  done
}

models=("$@")
for ((p = 0; p < ${#models[@]}; p += 2)); do
  pair=("${models[@]:p:2}")
  for model in "${pair[@]}"; do run_model "$model" & done
  wait
  env -u VIRTUAL_ENV uv run --project "$root/harness" --locked veracity-harness-wandb \
    --results "$out" --dotenv "$dotenv" >>"$out/logs/wandb.log" 2>&1 \
    && echo "$(date '+%F %T') wandb upload ok after ${pair[*]##*/}" \
    || echo "$(date '+%F %T') wandb upload FAILED after ${pair[*]##*/}; see logs/wandb.log"
done
echo "$(date '+%F %T') campaign finished"
