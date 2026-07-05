#!/usr/bin/env bash
# render_probe_faces.sh — PROBE: pull clean face frames of the AWNING (the look the
# user validated as "looks like me") and the CURB (base to refit), so we can element-
# refit the curb face to the awning likeness. Commits stills for media_import.
set -euo pipefail
cd "$(dirname "$0")/.."
command -v ffmpeg >/dev/null 2>&1 || { echo "ERROR: install ffmpeg"; exit 1; }
B="https://d8j0ntlcm91z4.cloudfront.net/user_3FjIki1qP1YKJkNjWdqvy8pFZnR"
mkdir -p probe review/awn_stills review/curb_stills
get() { [ -s "probe/$2" ] || { echo "  get $2"; curl -fSL --retry 4 --retry-delay 2 -o "probe/$2" "$1"; }; }
get "$B/hf_20260703_043914_ab86a6c8-ba25-48b5-9be4-b81f5ae0e58d.mp4" awn.mp4    # AWNING sync (validated likeness)
get "$B/hf_20260704_124310_17d2a03f-1498-4117-bebc-4cb4d3400ffa.mp4" curb.mp4   # CURB sync (base to refit)
i=0; for t in 0.6 1.2 1.8 2.4 3.0; do
  ffmpeg -nostdin -y -loglevel error -ss "$t" -i probe/awn.mp4  -frames:v 1 -q:v 2 "$(printf 'review/awn_stills/awn_%02d.jpg' "$i")"
  i=$((i+1)); done
i=0; for t in 0.5 1.5 2.5 3.5 4.5; do
  ffmpeg -nostdin -y -loglevel error -ss "$t" -i probe/curb.mp4 -frames:v 1 -q:v 2 "$(printf 'review/curb_stills/curb_%02d.jpg' "$i")"
  i=$((i+1)); done
echo "wrote awn + curb stills"; ls -la review/awn_stills review/curb_stills