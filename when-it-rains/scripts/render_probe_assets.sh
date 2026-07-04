#!/usr/bin/env bash
# render_probe_assets.sh — PROBE ONLY. Download the candidate clips for the
# street->chorus rework and dump frames + durations so the sandbox can choose
# the 1.5s fill (hold the original street tail vs an atmosphere insert) with
# real pixels. No cut is produced.
set -euo pipefail
cd "$(dirname "$0")/.."
command -v ffmpeg >/dev/null 2>&1 || { echo "ERROR: install ffmpeg"; exit 1; }
B="https://d8j0ntlcm91z4.cloudfront.net/user_3FjIki1qP1YKJkNjWdqvy8pFZnR"
mkdir -p probe review
get() { [ -s "probe/$2" ] || { echo "  get $2"; curl -fSL --retry 4 --retry-delay 2 -o "probe/$2" "$1"; }; }
get "$B/hf_20260704_133740_84b73e44-5859-4ff0-9278-6440159aed27.mp4" street.mp4   # original no-turn street take
get "$B/hf_20260703_145649_41b05e2e-63fb-4845-873a-785776ace7d6.mp4" rain.mp4     # rivers on glass
get "$B/hf_20260703_145658_3d0619c6-3b9c-4f10-b7f9-1f3f309c2605.mp4" trees.mp4    # gust / wet trees
for f in street rain trees; do
  d=$(ffprobe -v error -show_entries format=duration -of default=nk=1:nw=1 "probe/$f.mp4" 2>/dev/null || echo "?")
  echo "DURATION $f = ${d}s"
  dir="review/probe_${f}_frames"; rm -rf "$dir"; mkdir -p "$dir"
  ffmpeg -nostdin -y -loglevel error -i "probe/$f.mp4" -vf "fps=2,scale=480:-2" -q:v 4 "$dir/f_%03d.jpg"
done
echo "probe done"
