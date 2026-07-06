#!/usr/bin/env bash
# render_probe_matchscu.sh — compare awning + curb refits (to the STREET-CU likeness)
# against the street-CU target and the originals.
set -euo pipefail
cd "$(dirname "$0")/.."
command -v ffmpeg >/dev/null 2>&1 || { echo "ERROR: install ffmpeg"; exit 1; }
B="https://d8j0ntlcm91z4.cloudfront.net/user_3FjIki1qP1YKJkNjWdqvy8pFZnR"
mkdir -p probe review
get() { [ -s "probe/$2" ] || { echo "  get $2"; curl -fSL --retry 4 --retry-delay 2 -o "probe/$2" "$1"; }; }
get "$B/hf_20260706_002428_bc3bb964-0977-4b02-b73d-a1cf1edde1b5.png" awnrefit.png
get "$B/hf_20260706_002450_ffcd446e-a833-441b-942c-356b4bfa3644.png" curbrefit.png
cp review/streetcu_stills/scu_03.jpg   probe/target.jpg
cp review/awn_stills/awn_02.jpg        probe/awnorig.jpg
cp review/curb_stills/curb_00.jpg      probe/curborig.jpg
for f in target awnorig awnrefit curborig curbrefit; do
  src="probe/$f.png"; [ -s "$src" ] || src="probe/$f.jpg"
  ffmpeg -nostdin -y -loglevel error -i "$src" -vf "scale=-2:520" "probe/n_$f.png"
done
ffmpeg -nostdin -y -loglevel error -i probe/n_target.png -i probe/n_awnorig.png -i probe/n_awnrefit.png -i probe/n_curborig.png -i probe/n_curbrefit.png \
  -filter_complex "[0:v][1:v][2:v][3:v][4:v]hstack=inputs=5" -frames:v 1 review/matchscu_compare.png
echo "wrote review/matchscu_compare.png (TARGET streetCU | awn-orig | awn-REFIT | curb-orig | curb-REFIT)"