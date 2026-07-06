#!/usr/bin/env bash
# render_probe_wide.sh — fetch the two WIDE establishing-shot candidates (0:55 replacement)
# and tile them side by side for a pick. Commits review/wide_compare.png.
set -euo pipefail
cd "$(dirname "$0")/.."
command -v ffmpeg >/dev/null 2>&1 || { echo "ERROR: install ffmpeg"; exit 1; }
B="https://d8j0ntlcm91z4.cloudfront.net/user_3FjIki1qP1YKJkNjWdqvy8pFZnR"
mkdir -p probe review
get() { [ -s "probe/$2" ] || { echo "  get $2"; curl -fSL --retry 4 --retry-delay 2 -o "probe/$2" "$1"; }; }
get "$B/hf_20260706_125758_0de129ed-c9e7-4360-8cda-e7c1f20e7420.png" wideA.png
get "$B/hf_20260706_125758_7219b256-6413-4b98-9aba-71d183e27173.png" wideB.png
for f in wideA wideB; do
  ffmpeg -nostdin -y -loglevel error -i "probe/$f.png" -vf "scale=-2:540" "probe/n_$f.png"
done
ffmpeg -nostdin -y -loglevel error -i probe/n_wideA.png -i probe/n_wideB.png \
  -filter_complex "[0:v][1:v]hstack=inputs=2" -frames:v 1 review/wide_compare.png
echo "wrote review/wide_compare.png (A 0de129ed | B 7219b256)"
