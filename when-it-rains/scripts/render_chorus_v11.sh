#!/usr/bin/env bash
# render_chorus_v11.sh — the RESTAGED cafe (director's blocking):
#   he stands IN LINE at the counter, pastry case beside him -> his idle gaze drops
#   to the case glass and catches something -> HER reflection in the glass -> he
#   turns AROUND to look behind him -> strangers, no one. Both his moments animate
#   from ONE master still (same line, same jacket, bare hands, no text).
#   Original hero on the hooks, v5 puddle of her.
#
# Usage:  cd when-it-rains && bash scripts/render_chorus_v11.sh && open chorus_v11.mp4
set -euo pipefail
cd "$(dirname "$0")/.."
command -v ffmpeg >/dev/null 2>&1 || { echo "ERROR: install ffmpeg (brew install ffmpeg)"; exit 1; }
[ -s audio_relay/chorus_couplet.mp3 ] || { echo "ERROR: audio_relay/chorus_couplet.mp3 missing (git pull)"; exit 1; }
B="https://d8j0ntlcm91z4.cloudfront.net/user_3FjIki1qP1YKJkNjWdqvy8pFZnR"
mkdir -p chorus11; : > chorus11/concat.txt
VF="scale=1280:720:force_original_aspect_ratio=decrease,pad=1280:720:(ow-iw)/2:(oh-ih)/2,setsar=1,fps=24,format=yuv420p"

get() { [ -s "chorus11/$2" ] || { echo "  get $2"; curl -fSL --retry 4 --retry-delay 2 -o "chorus11/$2" "$1"; }; }
get "$B/hf_20260701_165718_491e39d1-548b-49ea-9f40-aa70ecef1d12.mp4" hero.mp4    # ORIGINAL hero (kept)
get "$B/hf_20260701_201522_b22edfc6-01f3-4d78-8f75-2e611da0eb8a.mp4" puddle.mp4  # her in the puddle (v5)
get "$B/hf_20260701_211031_e0693743-bb60-47e2-ba79-f57de5890092.mp4" notice.mp4  # IN LINE: gaze drops to the case, he stills
get "$B/hf_20260701_201618_fca42cda-6104-4a27-9342-c33b71b492f2.mp4" glass.mp4   # REVEAL: her reflection in the case glass
get "$B/hf_20260701_211033_6a0f494e-ff64-4ccc-8787-9ef025054628.mp4" turn.mp4    # REACTION: he turns around — strangers, no one

# hero in_points == output start so its lip-sync stays locked to the couplet audio.
CUTS=(
  "hero.mp4 0.00 2.95"     # HERO held — "when it rains you're in the water"
  "puddle.mp4 1.00 1.95"   # her, only in the puddle's reflection
  "hero.mp4 4.90 0.97"     # quick hero return
  "notice.mp4 1.20 1.95"   # in line: his gaze catches the case glass
  "glass.mp4 1.00 1.95"    # what he sees: her, ghosted in the glass
  "turn.mp4 0.60 2.23"     # he turns around — no one; hold on the loss
)
i=0
for c in "${CUTS[@]}"; do
  set -- $c; f=$1; ip=$2; du=$3
  seg=$(printf "chorus11/seg_%02d.mp4" "$i")
  ffmpeg -nostdin -y -loglevel error -ss "$ip" -t "$du" -i "chorus11/$f" -vf "$VF" -r 24 -an \
    -c:v libx264 -preset medium -crf 18 -video_track_timescale 12800 "$seg"
  echo "file '$(basename "$seg")'" >> chorus11/concat.txt
  i=$((i+1))
done
( cd chorus11 && ffmpeg -nostdin -y -loglevel error -f concat -safe 0 -i concat.txt -c copy silent.mp4 )
ffmpeg -nostdin -y -loglevel error -i chorus11/silent.mp4 -i audio_relay/chorus_couplet.mp3 \
  -map 0:v:0 -map 1:a:0 -c:v copy -c:a aac -b:a 256k -shortest chorus_v11.mp4
dur=$(ffprobe -v error -show_entries format=duration -of default=nk=1:nw=1 chorus_v11.mp4 2>/dev/null || echo "?")
echo "Wrote chorus_v11.mp4  (${dur}s — restaged: in line at the counter; notice -> reveal -> turn around)"
