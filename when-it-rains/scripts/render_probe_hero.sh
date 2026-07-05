#!/usr/bin/env bash
# render_probe_hero.sh — PROBE: pull the chorus MIC hero (491e39d1) and dump a
# few clean full-face frames so we can element-refit the off-model (bald/dark-beard)
# face to canonical. Commits stills to review/hero_stills/ for media_import.
set -euo pipefail
cd "$(dirname "$0")/.."
command -v ffmpeg >/dev/null 2>&1 || { echo "ERROR: install ffmpeg"; exit 1; }
B="https://d8j0ntlcm91z4.cloudfront.net/user_3FjIki1qP1YKJkNjWdqvy8pFZnR"
mkdir -p probe review/hero_stills
get() { [ -s "probe/$2" ] || { echo "  get $2"; curl -fSL --retry 4 --retry-delay 2 -o "probe/$2" "$1"; }; }
get "$B/hf_20260701_165718_491e39d1-548b-49ea-9f40-aa70ecef1d12.mp4" hero.mp4
d=$(ffprobe -v error -show_entries format=duration -of default=nk=1:nw=1 probe/hero.mp4 2>/dev/null || echo "?")
echo "hero duration = ${d}s"
# full-res stills at a few timestamps where he's mid-phrase, face open to camera
i=0
for t in 0.6 1.2 1.8 2.4 3.0; do
  ffmpeg -nostdin -y -loglevel error -ss "$t" -i probe/hero.mp4 -frames:v 1 -q:v 2 "$(printf "review/hero_stills/hero_%02d.jpg" "$i")"
  i=$((i+1))
done
# a 2fps contact sheet too
mkdir -p review/hero_frames
ffmpeg -nostdin -y -loglevel error -i probe/hero.mp4 -vf "fps=2,scale=480:-2" -q:v 3 review/hero_frames/f_%03d.jpg
echo "wrote hero stills + frames"; ls -la review/hero_stills