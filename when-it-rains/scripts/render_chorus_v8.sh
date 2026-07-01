#!/usr/bin/env bash
# render_chorus_v8.sh — the connected cut:
#   - ORIGINAL hero on the hooks (untouched)
#   - v5 puddle of her (the one you liked)
#   - cafe glance + turn now FROM THE SAME FRAME (same table/cup/jacket by construction)
#   - her ghosted in the glass between them
#
# Usage:  cd when-it-rains && bash scripts/render_chorus_v8.sh && open chorus_v8.mp4
set -euo pipefail
cd "$(dirname "$0")/.."
command -v ffmpeg >/dev/null 2>&1 || { echo "ERROR: install ffmpeg (brew install ffmpeg)"; exit 1; }
[ -s audio_relay/chorus_couplet.mp3 ] || { echo "ERROR: audio_relay/chorus_couplet.mp3 missing (git pull)"; exit 1; }
B="https://d8j0ntlcm91z4.cloudfront.net/user_3FjIki1qP1YKJkNjWdqvy8pFZnR"
mkdir -p chorus8; : > chorus8/concat.txt
VF="scale=1280:720:force_original_aspect_ratio=decrease,pad=1280:720:(ow-iw)/2:(oh-ih)/2,setsar=1,fps=24,format=yuv420p"

get() { [ -s "chorus8/$2" ] || { echo "  get $2"; curl -fSL --retry 4 --retry-delay 2 -o "chorus8/$2" "$1"; }; }
get "$B/hf_20260701_165718_491e39d1-548b-49ea-9f40-aa70ecef1d12.mp4" hero.mp4    # ORIGINAL hero (kept)
get "$B/hf_20260701_201522_b22edfc6-01f3-4d78-8f75-2e611da0eb8a.mp4" puddle.mp4  # her in the puddle — the v5 one you liked
get "$B/hf_20260701_201452_0c6c7fbf-926e-4eaa-bcab-8dad905cbb4a.mp4" cafe.mp4    # you (Soul) at the table, glancing up
get "$B/hf_20260701_201618_fca42cda-6104-4a27-9342-c33b71b492f2.mp4" glass.mp4   # her ghosted in the glass case
get "$B/hf_20260701_204152_33e7cf65-7c92-46d6-b61d-e18de09dfbf3.mp4" turn.mp4    # you turn — SAME frame as the glance (same table)

# hero in_points == output start so its lip-sync stays locked to the couplet audio.
CUTS=(
  "hero.mp4 0.00 2.95"    # HERO held — "when it rains you're in the water"
  "puddle.mp4 1.00 1.95"  # her, only in the puddle's reflection (v5)
  "hero.mp4 4.90 0.97"    # quick hero return
  "cafe.mp4 0.80 1.95"    # you at the table, glancing up
  "glass.mp4 1.00 1.95"   # her, ghosted in the glass of the case
  "turn.mp4 0.80 2.23"    # SAME table: you set the cup down, turn — no one
)
i=0
for c in "${CUTS[@]}"; do
  set -- $c; f=$1; ip=$2; du=$3
  seg=$(printf "chorus8/seg_%02d.mp4" "$i")
  ffmpeg -nostdin -y -loglevel error -ss "$ip" -t "$du" -i "chorus8/$f" -vf "$VF" -r 24 -an \
    -c:v libx264 -preset medium -crf 18 -video_track_timescale 12800 "$seg"
  echo "file '$(basename "$seg")'" >> chorus8/concat.txt
  i=$((i+1))
done
( cd chorus8 && ffmpeg -nostdin -y -loglevel error -f concat -safe 0 -i concat.txt -c copy silent.mp4 )
ffmpeg -nostdin -y -loglevel error -i chorus8/silent.mp4 -i audio_relay/chorus_couplet.mp3 \
  -map 0:v:0 -map 1:a:0 -c:v copy -c:a aac -b:a 256k -shortest chorus_v8.mp4
dur=$(ffprobe -v error -show_entries format=duration -of default=nk=1:nw=1 chorus_v8.mp4 2>/dev/null || echo "?")
echo "Wrote chorus_v8.mp4  (${dur}s — connected story: one table, one moment)"
