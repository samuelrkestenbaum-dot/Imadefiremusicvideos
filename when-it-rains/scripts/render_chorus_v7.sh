#!/usr/bin/env bash
# render_chorus_v7.sh — likeness first: the SOUL-generated cafe shots restored
# (v5's, which held his face), v6's cohesive puddle kept (no face in it).
#   hero -> her in the puddle outside a cafe -> hero -> your Soul CU in the cafe
#   -> her ghosted in the glass case -> you turn, no one there.
#
# Usage:  cd when-it-rains && bash scripts/render_chorus_v7.sh && open chorus_v7.mp4
set -euo pipefail
cd "$(dirname "$0")/.."
command -v ffmpeg >/dev/null 2>&1 || { echo "ERROR: install ffmpeg (brew install ffmpeg)"; exit 1; }
[ -s audio_relay/chorus_couplet.mp3 ] || { echo "ERROR: audio_relay/chorus_couplet.mp3 missing (git pull)"; exit 1; }
B="https://d8j0ntlcm91z4.cloudfront.net/user_3FjIki1qP1YKJkNjWdqvy8pFZnR"
mkdir -p chorus7; : > chorus7/concat.txt
VF="scale=1280:720:force_original_aspect_ratio=decrease,pad=1280:720:(ow-iw)/2:(oh-ih)/2,setsar=1,fps=24,format=yuv420p"

get() { [ -s "chorus7/$2" ] || { echo "  get $2"; curl -fSL --retry 4 --retry-delay 2 -o "chorus7/$2" "$1"; }; }
get "$B/hf_20260701_165718_491e39d1-548b-49ea-9f40-aa70ecef1d12.mp4" hero.mp4    # ORIGINAL hero (kept)
get "$B/hf_20260701_203136_1bc82dc2-d9df-414c-99aa-4a92dc8a8aa5.mp4" puddle.mp4  # her reflection, puddle by the cafe (v6, no face)
get "$B/hf_20260701_201452_0c6c7fbf-926e-4eaa-bcab-8dad905cbb4a.mp4" cafe.mp4    # YOUR Soul CU in the cafe (v5 — the good one)
get "$B/hf_20260701_201618_fca42cda-6104-4a27-9342-c33b71b492f2.mp4" glass.mp4   # her ghosted in the glass (v5, matches cafe warmth)
get "$B/hf_20260701_201733_d7e0b6d1-7834-4da7-884f-689e36bb8106.mp4" turn.mp4    # YOUR Soul turn (v5 — the good one)

# hero in_points == output start so its lip-sync stays locked to the couplet audio.
CUTS=(
  "hero.mp4 0.00 2.95"    # HERO held — "when it rains you're in the water"
  "puddle.mp4 1.00 1.95"  # her, only in the puddle's reflection
  "hero.mp4 4.90 0.97"    # quick hero return
  "cafe.mp4 0.80 1.95"    # you (Soul) in the cafe, glancing up
  "glass.mp4 1.00 1.95"   # her, ghosted in the glass of the case
  "turn.mp4 0.80 2.23"    # you (Soul) turn — no one there; hold
)
i=0
for c in "${CUTS[@]}"; do
  set -- $c; f=$1; ip=$2; du=$3
  seg=$(printf "chorus7/seg_%02d.mp4" "$i")
  ffmpeg -nostdin -y -loglevel error -ss "$ip" -t "$du" -i "chorus7/$f" -vf "$VF" -r 24 -an \
    -c:v libx264 -preset medium -crf 18 -video_track_timescale 12800 "$seg"
  echo "file '$(basename "$seg")'" >> chorus7/concat.txt
  i=$((i+1))
done
( cd chorus7 && ffmpeg -nostdin -y -loglevel error -f concat -safe 0 -i concat.txt -c copy silent.mp4 )
ffmpeg -nostdin -y -loglevel error -i chorus7/silent.mp4 -i audio_relay/chorus_couplet.mp3 \
  -map 0:v:0 -map 1:a:0 -c:v copy -c:a aac -b:a 256k -shortest chorus_v7.mp4
dur=$(ffprobe -v error -show_entries format=duration -of default=nk=1:nw=1 chorus_v7.mp4 2>/dev/null || echo "?")
echo "Wrote chorus_v7.mp4  (${dur}s — Soul cafe shots restored, likeness first)"
