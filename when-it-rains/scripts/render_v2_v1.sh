#!/usr/bin/env bash
# render_v2_v1.sh — VERSE 2, the street (song 43.0–70.3s, 27.3s), first exterior:
#   out the door (one take) -> walk + SHOULDER LOOK ("I look for you beyond my
#   shoulder", look measured at take 6.0-7.5) -> puddle rings ("somewhere
#   between the drops") -> SYNC "the sky still holds your whisper" under the
#   awning (real vocal, 2K) -> THE HOLD: him dead still at the curb while the
#   world keeps moving ("and I need my world to stop") -> puddle button.
# All him/street assets derive from the gated street master 4b892de9.
set -euo pipefail
cd "$(dirname "$0")/.."
command -v ffmpeg >/dev/null 2>&1 || { echo "ERROR: install ffmpeg"; exit 1; }
[ -s audio_relay/v2_bed.mp3 ] || { echo "ERROR: audio_relay/v2_bed.mp3 missing (git pull)"; exit 1; }
B="https://d8j0ntlcm91z4.cloudfront.net/user_3FjIki1qP1YKJkNjWdqvy8pFZnR"
mkdir -p v2sec; : > v2sec/concat.txt
VF="scale=1280:720:force_original_aspect_ratio=decrease,pad=1280:720:(ow-iw)/2:(oh-ih)/2,setsar=1"
get() { [ -s "v2sec/$2" ] || { echo "  get $2"; curl -fSL --retry 4 --retry-delay 2 -o "v2sec/$2" "$1"; }; }
get "$B/hf_20260702_201225_fccf32d3-f0ad-45b4-ad3b-dbc8e7d8dcc8.mp4" door.mp4    # door take (out + look + walk)
get "$B/SYNC_URL_TBD.mp4" sync.mp4                                               # awning sync (wan2_7 + 2K)
get "$B/hf_20260702_202835_0328c8be-1e00-4a8f-b146-aef3a5e4a029.mp4" curb.mp4      # the world-keeps-moving hold
get "$B/hf_20260702_202914_7923e3e5-8b1f-4f8c-9d2e-fdba618f8e52.mp4" puddle.mp4    # rings between the drops

seg() { ffmpeg -nostdin -y -loglevel error -ss "$2" -t "$3" -i "v2sec/$1" -vf "$VF,fps=24,format=yuv420p" -r 24 -an \
  -c:v libx264 -preset medium -crf 18 -video_track_timescale 12800 "$(printf "v2sec/seg_%02d.mp4" "$4")"
  echo "file '$(printf "seg_%02d.mp4" "$4")'" >> v2sec/concat.txt; }

seg door.mp4   0.40 3.90 0   # 43.0-46.9 out the door, the door closes, he turns
seg door.mp4   5.90 3.90 1   # 46.9-50.8 walking away + the SHOULDER LOOK (measured 6.0-7.5)
seg puddle.mp4 0.60 3.90 2   # 50.8-54.7 "between the drops": rings in the water
seg sync.mp4   0.50 3.90 3   # 54.7-58.6 SYNC: "the sky still holds your whisper" (slice0=song54.2 -> in 0.5)
seg curb.mp4   0.30 9.70 4   # 58.6-68.3 THE HOLD: still at the curb, world moves
seg puddle.mp4 1.20 2.00 5   # 68.3-70.3 button: the rings again, into PRE1

( cd v2sec && ffmpeg -nostdin -y -loglevel error -f concat -safe 0 -i concat.txt -c copy silent.mp4 )
ffmpeg -nostdin -y -loglevel error -i v2sec/silent.mp4 -i audio_relay/v2_bed.mp3 \
  -map 0:v:0 -map 1:a:0 -c:v copy -c:a aac -b:a 256k -shortest v2_v1.mp4
dur=$(ffprobe -v error -show_entries format=duration -of default=nk=1:nw=1 v2_v1.mp4 2>/dev/null || echo "?")
echo "Wrote v2_v1.mp4  (${dur}s — Verse 2: the street, the look back, the world that will not stop)"
