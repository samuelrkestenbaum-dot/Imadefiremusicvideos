#!/usr/bin/env bash
# render_probe_curbrefit.sh — compare the two curb-face refit candidates against
# the awning reference (validated likeness) and the original curb.
set -euo pipefail
cd "$(dirname "$0")/.."
command -v ffmpeg >/dev/null 2>&1 || { echo "ERROR: install ffmpeg"; exit 1; }
B="https://d8j0ntlcm91z4.cloudfront.net/user_3FjIki1qP1YKJkNjWdqvy8pFZnR"
mkdir -p probe review
get() { [ -s "probe/$2" ] || { echo "  get $2"; curl -fSL --retry 4 --retry-delay 2 -o "probe/$2" "$1"; }; }
get "$B/hf_20260705_232522_2a836342-3019-4dd1-aafc-ee3891c652b3.png" refitA.png
get "$B/hf_20260705_232522_66f00084-4f14-4b02-951a-12ce6005a815.png" refitB.png
cp review/awn_stills/awn_02.jpg   probe/awnref.jpg
cp review/curb_stills/curb_00.jpg probe/curborig.jpg
for f in awnref curborig refitA refitB; do
  src="probe/$f.png"; [ -s "$src" ] || src="probe/$f.jpg"
  ffmpeg -nostdin -y -loglevel error -i "$src" -vf "scale=-2:540" "probe/n_$f.png"
done
ffmpeg -nostdin -y -loglevel error -i probe/n_awnref.png -i probe/n_curborig.png -i probe/n_refitA.png -i probe/n_refitB.png \
  -filter_complex "[0:v][1:v][2:v][3:v]hstack=inputs=4" -frames:v 1 review/curbrefit_compare.png
echo "wrote review/curbrefit_compare.png (awning-ref | original-curb | refitA | refitB)"