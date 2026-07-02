#!/usr/bin/env bash
# render_v1_v1.sh — VERSE 1, the kitchen (song 23.5–43.0s, 19.5s):
#   THE TWO MUGS (one take: touch -> pickup -> carry, measured) ->
#   SYNC LINE "my heart had crossed the ocean" at the window (real vocal) ->
#   RAIN-RIVERS insert ("where the rivers bend", punched-in center pane) ->
#   back into the take: the mug goes back, the door closes on it ->
#   rain again as the verse rides out.
# All him/room assets derive from the LOCKED kitchen master 4709db96.
set -euo pipefail
cd "$(dirname "$0")/.."
command -v ffmpeg >/dev/null 2>&1 || { echo "ERROR: install ffmpeg"; exit 1; }
[ -s audio_relay/v1_bed.mp3 ] || { echo "ERROR: audio_relay/v1_bed.mp3 missing (git pull)"; exit 1; }
B="https://d8j0ntlcm91z4.cloudfront.net/user_3FjIki1qP1YKJkNjWdqvy8pFZnR"
mkdir -p v1sec; : > v1sec/concat.txt
VF="scale=1280:720:force_original_aspect_ratio=decrease,pad=1280:720:(ow-iw)/2:(oh-ih)/2,setsar=1"
PUNCH="crop=768:432:256:144,scale=1280:720,setsar=1"   # center-pane punch-in for the rain take
get() { [ -s "v1sec/$2" ] || { echo "  get $2"; curl -fSL --retry 4 --retry-delay 2 -o "v1sec/$2" "$1"; }; }
get "$B/hf_20260702_171154_a61bf1b4-092f-457f-84fa-0e54db106137.mp4" mugs.mp4   # THE take (from locked master)
get "$B/SYNC_URL_TBD.mp4" sync.mp4                                              # window sync line (wan2_7 + 2K)
get "$B/hf_20260702_172036_aaea0be1-b6db-4797-919d-4235466bdf03.mp4" rain.mp4   # rain-rivers on the kitchen pane

seg() { # file in dur idx [vf]
  local vf="${5:-$VF}"
  ffmpeg -nostdin -y -loglevel error -ss "$2" -t "$3" -i "v1sec/$1" -vf "$vf,fps=24,format=yuv420p" -r 24 -an \
    -c:v libx264 -preset medium -crf 18 -video_track_timescale 12800 "$(printf "v1sec/seg_%02d.mp4" "$4")"
  echo "file '$(printf "seg_%02d.mp4" "$4")'" >> v1sec/concat.txt; }

seg mugs.mp4 0.70 7.80 0            # 0-7.8    "soft touch": thumb on the rim -> pickup -> carry (measured 0-3/3-5.5/5.5-8.3)
seg sync.mp4 0.80 3.90 1            # 7.8-11.7 SYNC: "my heart had crossed the ocean" (clip0=song30.5 -> in 0.8)
seg rain.mp4 0.60 3.00 2 "$PUNCH"   # 11.7-14.7 "where the rivers bend" drawn on the glass
seg mugs.mp4 8.40 1.60 3            # 14.7-16.3 back into the take: the mug goes back, the door closes on it
seg rain.mp4 1.20 3.20 4 "$PUNCH"   # 16.3-19.5 rain rides the verse out

( cd v1sec && ffmpeg -nostdin -y -loglevel error -f concat -safe 0 -i concat.txt -c copy silent.mp4 )
ffmpeg -nostdin -y -loglevel error -i v1sec/silent.mp4 -i audio_relay/v1_bed.mp3 \
  -map 0:v:0 -map 1:a:0 -c:v copy -c:a aac -b:a 256k -shortest v1_v1.mp4
dur=$(ffprobe -v error -show_entries format=duration -of default=nk=1:nw=1 v1_v1.mp4 2>/dev/null || echo "?")
echo "Wrote v1_v1.mp4  (${dur}s — Verse 1: the two mugs, the sung line, the rivers on the glass)"
