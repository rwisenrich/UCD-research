#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")"
mkdir -p results/hot_runs
python code/electroweak_chiral.py > results/electroweak-run.log
python code/gravity_spin2_bounce.py > results/gravity-run.log
python code/q72_group_css.py > results/native-dic6-run.log
python code/q72_search_distance.py > results/native-dic6-optimized-run.log
python code/qec_distance12_concat.py > results/qec-concatenation-run.log
python code/h504_character_spectrum.py > results/h504-spectrum-run.log
python code/glueball_nt8.py --beta 16 --L 3 --nt 8 --warm 300 --measure 80 --stride 3 --angle 0.18 --hot --seed 1016001 --out results/hot_runs > results/MC-hot-16.log
python code/glueball_nt8.py --beta 19 --L 3 --nt 8 --warm 300 --measure 80 --stride 3 --angle 0.18 --hot --seed 1019001 --out results/hot_runs > results/MC-hot-19.log
python code/glueball_multichannel.py --beta 16 --warm 300 --measure 80 --stride 3 --seed 2016010 --out results > results/MC-multi-16.log
python code/glueball_multichannel.py --beta 19 --warm 300 --measure 80 --stride 3 --seed 2019010 --out results > results/MC-multi-19.log
python code/verify_frontiers.py | tee results/verification-latest.log
python - <<'PY'
import json
from pathlib import Path
p=Path("results/frontier_verification_summary.json")
d=json.loads(p.read_text())
assert d["passed"]==32, d
print("ALL FOUR UCD FRONTIERS: 32/32 checks; fresh Nt=8 SU3 raw trajectories saved")
PY
