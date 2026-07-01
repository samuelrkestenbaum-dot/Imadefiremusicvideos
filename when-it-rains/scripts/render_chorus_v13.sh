#!/usr/bin/env bash
# render_chorus_v13.sh — v12 with the GLASSIFIED reflection insert (true glass read):
#   ONE take carries his body (no posture mismatches possible); the insert is his
#   POV of the case glass with HER single translucent reflection (physically
#   correct for an angled viewer); measured beats from video-analysis.
#   look down (take 1.0-2.95s) -> her reflection (insert) -> turn (same take @6.9s)
#   Original hero on the hooks, v5 puddle of her.
#
# Usage:  cd when-it-rains && bash scripts/render_chorus_v13.sh && open chorus_v13.mp4
set -euo pipefail
cd "$(dirname "$0")/.."
command -v ffmpeg >/dev/null 2>&1 || { echo "ERROR: install ffmpeg (brew install ffmpeg)"; exit 1; }
[ -s audio_relay/chorus_couplet.mp3 ] || { echo "ERROR: audio_relay/chorus_couplet.mp3 missing (git pull)"; exit 1; }
B="https://d8j0ntlcm91z4.cloudfront.net/user_3FjIki1qP1YKJkNjWdqvy8pFZnR"
mkdir -p chorus13; : > chorus13/concat.txt
VF="scale=1280:720:force_original_aspect_ratio=decrease,pad=1280:720:(ow-iw)/2:(oh-ih)/2,setsar=1,fps=24,format=yuv420p"

get() { [ -s "chorus13/$2" ] || { echo "  get $2"; curl -fSL --retry 4 --retry-delay 2 -o "chorus13/$2" "$1"; }; }
get "$B/hf_20260701_165718_491e39d1-548b-49ea-9f40-aa70ecef1d12.mp4" hero.mp4    # ORIGINAL hero (kept)
get "$B/hf_20260701_201522_b22edfc6-01f3-4d78-8f75-2e611da0eb8a.mp4" puddle.mp4  # her in the puddle (v5)
get "$B/hf_20260701_211804_c1ffc156-7682-4fb5-8ba3-29e4a554df6a.mp4" take.mp4    # THE one-take (his only body source)
get "$B/hf_20260701_221229_9bf9d028-352b-40fb-887e-85b897dc09f2.mp4" insert.mp4  # POV: her single reflection in the case glass

# hero in_points == output start so its lip-sync stays locked to the couplet audio.
CUTS=(
  "hero.mp4 0.00 2.95"     # HERO held — "when it rains you're in the water"
  "puddle.mp4 1.00 1.95"   # her, only in the puddle's reflection
  "hero.mp4 4.90 0.97"     # quick hero return
  "take.mp4 1.00 1.95"     # beat 1 (measured): in line, gaze drifts down to the case
  "insert.mp4 0.80 1.95"   # what he sees: HER reflection alone in the angled glass
  "take.mp4 6.90 2.23"     # beat 2 (measured 0:07): same take — he turns; no one
)
i=0
for c in "${CUTS[@]}"; do
  set -- $c; f=$1; ip=$2; du=$3
  seg=$(printf "chorus13/seg_%02d.mp4" "$i")
  ffmpeg -nostdin -y -loglevel error -ss "$ip" -t "$du" -i "chorus13/$f" -vf "$VF" -r 24 -an \
    -c:v libx264 -preset medium -crf 18 -video_track_timescale 12800 "$seg"
  echo "file '$(basename "$seg")'" >> chorus13/concat.txt
  i=$((i+1))
done
( cd chorus13 && ffmpeg -nostdin -y -loglevel error -f concat -safe 0 -i concat.txt -c copy silent.mp4 )
ffmpeg -nostdin -y -loglevel error -i chorus13/silent.mp4 -i audio_relay/chorus_couplet.mp3 \
  -map 0:v:0 -map 1:a:0 -c:v copy -c:a aac -b:a 256k -shortest chorus_v13.mp4
dur=$(ffprobe -v error -show_entries format=duration -of default=nk=1:nw=1 chorus_v13.mp4 2>/dev/null || echo "?")
echo "Wrote chorus_v13.mp4  (${dur}s — spec-staged cafe: one take, POV reflection, measured beats)"
