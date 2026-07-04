#!/usr/bin/env bash
# render_turn_compare.sh — A/B the turn lip-sync: wan2_7 vs seedance_2_0, each
# muxed with the actual vocal slice so the user can hear+see the sync. Outputs
# two short clips for a side-by-side judgement. No grade/zoom — raw sync only.
set -euo pipefail
cd "$(dirname "$0")/.."
command -v ffmpeg >/dev/null 2>&1 || { echo "ERROR: install ffmpeg"; exit 1; }
[ -s audio_relay/pre1_line12.mp3 ] || { echo "ERROR: pre1_line12.mp3 missing"; exit 1; }
B="https://d8j0ntlcm91z4.cloudfront.net/user_3FjIki1qP1YKJkNjWdqvy8pFZnR"
mkdir -p turncmp
get() { [ -s "turncmp/$2" ] || { echo "  get $2"; curl -fSL --retry 4 --retry-delay 2 -o "turncmp/$2" "$1"; }; }
get "$B/hf_20260704_124957_62f4313d-efcf-431e-a071-5bab3f99fbec.mp4" wan.mp4
get "$B/hf_20260704_125453_38054380-ad4f-4a34-afe8-c4d58935abb3.mp4" seedance.mp4

mux() { # $1 src  $2 out-label
  ffmpeg -nostdin -y -loglevel error -i "turncmp/$1" -i audio_relay/pre1_line12.mp3 \
    -map 0:v:0 -map 1:a:0 -vf "scale=1280:720:force_original_aspect_ratio=decrease,pad=1280:720:(ow-iw)/2:(oh-ih)/2,setsar=1,fps=24,format=yuv420p" \
    -r 24 -c:v libx264 -profile:v main -level 3.1 -preset medium -crf 24 -pix_fmt yuv420p \
    -c:a aac -b:a 160k -ac 2 -ar 44100 -movflags +faststart -shortest "turn_$2.mp4"
  echo "wrote turn_$2.mp4"; }

mux wan.mp4 wan
mux seedance.mp4 seedance
