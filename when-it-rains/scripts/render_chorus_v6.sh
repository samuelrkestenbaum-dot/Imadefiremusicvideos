#!/usr/bin/env bash
# render_chorus_v6.sh — chorus with the ORIGINAL hero + the COHESIVE cafe scene.
# All normal-life cutaways now come from ONE cafe (master-derived coverage: same
# jacket, same counter, same light — continuity verified). Her only in reflections.
#   hero -> her in the puddle outside the cafe -> hero -> your CU in the cafe
#   -> her ghosted in the pastry-case glass -> you turn, no one there.
#
# Usage:  cd when-it-rains && bash scripts/render_chorus_v6.sh && open chorus_v6.mp4
set -euo pipefail
cd "$(dirname "$0")/.."
command -v ffmpeg >/dev/null 2>&1 || { echo "ERROR: install ffmpeg (brew install ffmpeg)"; exit 1; }
[ -s audio_relay/chorus_couplet.mp3 ] || { echo "ERROR: audio_relay/chorus_couplet.mp3 missing (git pull)"; exit 1; }
B="https://d8j0ntlcm91z4.cloudfront.net/user_3FjIki1qP1YKJkNjWdqvy8pFZnR"
mkdir -p chorus6; : > chorus6/concat.txt
VF="scale=1280:720:force_original_aspect_ratio=decrease,pad=1280:720:(ow-iw)/2:(oh-ih)/2,setsar=1,fps=24,format=yuv420p"

get() { [ -s "chorus6/$2" ] || { echo "  get $2"; curl -fSL --retry 4 --retry-delay 2 -o "chorus6/$2" "$1"; }; }
get "$B/hf_20260701_165718_491e39d1-548b-49ea-9f40-aa70ecef1d12.mp4" hero.mp4    # ORIGINAL hero (kept)
get "$B/hf_20260701_203136_1bc82dc2-d9df-414c-99aa-4a92dc8a8aa5.mp4" puddle.mp4  # her reflection, puddle outside the cafe
get "$B/hf_20260701_202834_adfcbf3a-8ad1-4050-8c5a-62d8ffdb492a.mp4" cafe.mp4    # YOUR CU in the cafe (continuity PASS)
get "$B/hf_20260701_202837_6dc58028-109e-4227-9655-1bdc76748bf9.mp4" glass.mp4   # her ghosted in the pastry-case glass
get "$B/hf_20260701_203103_7a35eaff-5d2d-4043-8fb1-eb70431ba52d.mp4" turn.mp4    # you turn on the stool (continuity PASS)

# hero in_points == output start so its lip-sync stays locked to the couplet audio.
CUTS=(
  "hero.mp4 0.00 2.95"    # HERO held — "when it rains you're in the water"
  "puddle.mp4 1.00 1.95"  # her, only in the puddle outside the cafe window
  "hero.mp4 4.90 0.97"    # quick hero return
  "cafe.mp4 0.80 1.95"    # you at the window counter, glancing up
  "glass.mp4 1.00 1.95"   # her, ghosted in the glass of the case
  "turn.mp4 0.80 2.23"    # you turn — no one there; hold on the loss
)
i=0
for c in "${CUTS[@]}"; do
  set -- $c; f=$1; ip=$2; du=$3
  seg=$(printf "chorus6/seg_%02d.mp4" "$i")
  ffmpeg -nostdin -y -loglevel error -ss "$ip" -t "$du" -i "chorus6/$f" -vf "$VF" -r 24 -an \
    -c:v libx264 -preset medium -crf 18 -video_track_timescale 12800 "$seg"
  echo "file '$(basename "$seg")'" >> chorus6/concat.txt
  i=$((i+1))
done
( cd chorus6 && ffmpeg -nostdin -y -loglevel error -f concat -safe 0 -i concat.txt -c copy silent.mp4 )
ffmpeg -nostdin -y -loglevel error -i chorus6/silent.mp4 -i audio_relay/chorus_couplet.mp3 \
  -map 0:v:0 -map 1:a:0 -c:v copy -c:a aac -b:a 256k -shortest chorus_v6.mp4
dur=$(ffprobe -v error -show_entries format=duration -of default=nk=1:nw=1 chorus_v6.mp4 2>/dev/null || echo "?")
echo "Wrote chorus_v6.mp4  (${dur}s — hero + ONE cohesive cafe scene, her in reflections)"
