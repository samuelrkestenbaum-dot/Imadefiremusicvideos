#!/usr/bin/env bash
# render_probe_scurefit.sh — compare street-CU refit candidates vs awning ref + original.
set -euo pipefail
cd "$(dirname "$0")/.."
command -v ffmpeg >/dev/null 2>&1 || { echo "ERROR: install ffmpeg"; exit 1; }
B="https://d8j0ntlcm91z4.cloudfront.net/user_3FjIki1qP1YKJkNjWdqvy8pFZnR"
mkdir -p probe review
get() { [ -s "probe/$2" ] || { echo "  get $2"; curl -fSL --retry 4 --retry-delay 2 -o "probe/$2" "$1"; }; }
get "$B/hf_20260705_235349_2a3e04f2-8017-4bdc-a20c-2077860b2b62.png" scuA.png
get "$B/hf_20260705_235349_167d21fe-b0ea-4476-b760-c3aedfc5bc5d.png" scuB.png
cp review/awn_stills/awn_02.jpg        probe/awnref.jpg
cp review/streetcu_stills/scu_03.jpg   probe/scuorig.jpg
for f in awnref scuorig scuA scuB; do
  src="probe/$f.png"; [ -s "$src" ] || src="probe/$f.jpg"
  ffmpeg -nostdin -y -loglevel error -i "$src" -vf "scale=-2:540" "probe/n_$f.png"
done
ffmpeg -nostdin -y -loglevel error -i probe/n_awnref.png -i probe/n_scuorig.png -i probe/n_scuA.png -i probe/n_scuB.png \
  -filter_complex "[0:v][1:v][2:v][3:v]hstack=inputs=4" -frames:v 1 review/scurefit_compare.png
echo "wrote review/scurefit_compare.png (awning-ref | original-scu | refitA | refitB)"