#!/usr/bin/env bash
# render_probe_refit.sh — PROBE: assemble a comparison of the MIC face refit
# candidates against the canonical reference and the original off-model mic, so
# we can pick the best refit before re-animating.
set -euo pipefail
cd "$(dirname "$0")/.."
command -v ffmpeg >/dev/null 2>&1 || { echo "ERROR: install ffmpeg"; exit 1; }
B="https://d8j0ntlcm91z4.cloudfront.net/user_3FjIki1qP1YKJkNjWdqvy8pFZnR"
mkdir -p probe review
get() { [ -s "probe/$2" ] || { echo "  get $2"; curl -fSL --retry 4 --retry-delay 2 -o "probe/$2" "$1"; }; }
get "$B/hf_20260701_210019_32058bcb-bb09-40cc-851d-598975012aeb.png" canon.png      # wir-him canonical reference
get "$B/hf_20260705_042836_02659799-e266-44de-bbd3-2a23508e8f7e.png" refit1.png     # candidate 1
get "$B/hf_20260705_042836_9b115df7-ec29-4473-ad16-3547c99f6a17.png" refit2.png     # candidate 2
cp review/hero_stills/hero_02.jpg probe/orig.jpg
# normalize heights and lay out: canon | orig(off-model) | refit1 | refit2
for f in canon orig refit1 refit2; do
  src="probe/$f.png"; [ -s "$src" ] || src="probe/$f.jpg"
  ffmpeg -nostdin -y -loglevel error -i "$src" -vf "scale=-2:520" "probe/n_$f.png"
done
ffmpeg -nostdin -y -loglevel error -i probe/n_canon.png -i probe/n_orig.png -i probe/n_refit1.png -i probe/n_refit2.png \
  -filter_complex "[0:v][1:v][2:v][3:v]hstack=inputs=4" -frames:v 1 review/refit_compare.png
echo "wrote review/refit_compare.png (canon | original | refit1 | refit2)"