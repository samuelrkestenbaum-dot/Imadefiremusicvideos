#!/usr/bin/env bash
# render_v2_v2.sh — V2 street, likeness-era recut: door + curb takes re-shot
# from anchor-picked masters (fuller face); one continuous door take carries
# out -> walk -> SHOULDER LOOK (measured 4.0-6.5) -> walk on; the section
# button is the LADDER INSERT: her reflection in the puddle, rippled apart by
# a raindrop the moment after we see it.
set -euo pipefail
cd "$(dirname "$0")/.."
command -v ffmpeg >/dev/null 2>&1 || { echo "ERROR: install ffmpeg"; exit 1; }
[ -s audio_relay/v2_bed.mp3 ] || { echo "ERROR: audio_relay/v2_bed.mp3 missing"; exit 1; }
B="https://d8j0ntlcm91z4.cloudfront.net/user_3FjIki1qP1YKJkNjWdqvy8pFZnR"
mkdir -p v2sec2; : > v2sec2/concat.txt
VF="scale=1280:720:force_original_aspect_ratio=decrease,pad=1280:720:(ow-iw)/2:(oh-ih)/2,setsar=1"
get() { [ -s "v2sec2/$2" ] || { echo "  get $2"; curl -fSL --retry 4 --retry-delay 2 -o "v2sec2/$2" "$1"; }; }
get "$B/hf_20260703_010041_c742b889-9c29-4f0d-b214-3b70ea5b794f.mp4" door.mp4       # repaired door take
get "$B/hf_20260702_203815_d818ba44-2b4c-4c27-8b89-8ef52dfcff5d.mp4" sync.mp4       # awning sync (unchanged)
get "$B/hf_20260703_010044_896f8dfb-c3d5-4b06-9fb4-9b904540721d.mp4" curb.mp4       # repaired curb hold
get "$B/hf_20260702_202914_7923e3e5-8b1f-4f8c-9d2e-fdba618f8e52.mp4" puddle.mp4     # plain rings
get "$B/hf_20260703_010458_31ccf929-5637-4a0d-a75c-ebfbaba8ca51.mp4" ghostpud.mp4   # her reflection, rippled apart

seg() { ffmpeg -nostdin -y -loglevel error -ss "$2" -t "$3" -i "v2sec2/$1" -vf "$VF,fps=24,format=yuv420p" -r 24 -an \
  -c:v libx264 -preset medium -crf 18 -video_track_timescale 12800 "$(printf "v2sec2/seg_%02d.mp4" "$4")"
  echo "file '$(printf "seg_%02d.mp4" "$4")'" >> v2sec2/concat.txt; }

seg door.mp4     1.20 7.80 0   # 43.0-50.8 one take: out -> walk -> LOOK (4.0-6.5 -> song 45.8-48.3) -> walk on
seg puddle.mp4   0.60 3.90 1   # 50.8-54.7 "between the drops"
seg sync.mp4     0.50 3.90 2   # 54.7-58.6 SYNC "the sky still holds your whisper"
seg curb.mp4     0.30 9.70 3   # 58.6-68.3 THE HOLD: still while the world moves
seg ghostpud.mp4 2.20 2.00 4   # 68.3-70.3 LADDER: her reflection - a drop hits - gone

( cd v2sec2 && ffmpeg -nostdin -y -loglevel error -f concat -safe 0 -i concat.txt -c copy silent.mp4 )
ffmpeg -nostdin -y -loglevel error -i v2sec2/silent.mp4 -i audio_relay/v2_bed.mp3 \
  -map 0:v:0 -map 1:a:0 -c:v copy -c:a aac -b:a 256k -shortest v2_v2.mp4
echo "Wrote v2_v2.mp4"
