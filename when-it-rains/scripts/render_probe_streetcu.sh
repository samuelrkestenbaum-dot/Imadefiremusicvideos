#!/usr/bin/env bash
# render_probe_streetcu.sh — PROBE: pull clean frontal frames of the "like you
# never left" street close-up (d07ecfa1, the fuller-beard shot) so we can refit
# its face to the awning/walk bald look. Commits stills for media_import.
set -euo pipefail
cd "$(dirname "$0")/.."
command -v ffmpeg >/dev/null 2>&1 || { echo "ERROR: install ffmpeg"; exit 1; }
B="https://d8j0ntlcm91z4.cloudfront.net/user_3FjIki1qP1YKJkNjWdqvy8pFZnR"
mkdir -p probe review/streetcu_stills
get() { [ -s "probe/$2" ] || { echo "  get $2"; curl -fSL --retry 4 --retry-delay 2 -o "probe/$2" "$1"; }; }
get "$B/hf_20260704_150931_d07ecfa1-f03e-4f13-8be2-c9c49b9a52aa.mp4" streetcu.mp4
i=0; for t in 0.5 1.5 2.5 3.5 4.5 5.5; do
  ffmpeg -nostdin -y -loglevel error -ss "$t" -i probe/streetcu.mp4 -frames:v 1 -q:v 2 "$(printf 'review/streetcu_stills/scu_%02d.jpg' "$i")"
  i=$((i+1)); done
echo "wrote streetcu stills"; ls -la review/streetcu_stills