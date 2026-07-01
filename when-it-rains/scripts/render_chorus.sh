#!/usr/bin/env bash
# render_chorus.sh — stitch the 6 lip-synced chorus angles into one preview.
# Each clip is wan2_7 lip-sync (your face + your real vocal phrase), internally
# in sync. This concatenates them in phrase order into the full chorus.
#
# Usage:  cd when-it-rains && bash scripts/render_chorus.sh && open chorus_preview.mp4
set -euo pipefail
cd "$(dirname "$0")/.."
command -v ffmpeg >/dev/null 2>&1 || { echo "ERROR: install ffmpeg (brew install ffmpeg)"; exit 1; }
command -v curl   >/dev/null 2>&1 || { echo "ERROR: curl not found"; exit 1; }

mkdir -p chorus_clips
BASE="https://d8j0ntlcm91z4.cloudfront.net/user_3FjIki1qP1YKJkNjWdqvy8pFZnR"

# phrase-ordered: front CU -> face-up -> window -> low angle -> extreme CU -> wide
URLS=(
  "$BASE/hf_20260701_170538_f6d62af7-6e13-4d5e-ac44-66743fb1b81d.mp4"   # 1 front close-up
  "$BASE/hf_20260701_170539_d8505bab-eaec-4492-893b-a5a4309a8fb3.mp4"   # 2 face-up in rain
  "$BASE/hf_20260701_170541_ebc5e48c-31db-4a0c-a0f4-e7a27667218e.mp4"   # 3 at the window
  "$BASE/hf_20260701_170543_4ad3efca-bda8-47fb-97ed-6aed0c42e171.mp4"   # 4 low angle
  "$BASE/hf_20260701_170546_11231440-3ab2-46c7-8519-27eb66b573c5.mp4"   # 5 extreme close-up
  "$BASE/hf_20260701_170547_057d5ab8-fd04-440b-975f-5f32130752a3.mp4"   # 6 wide, full body
)

VF="scale=1280:720:force_original_aspect_ratio=decrease,pad=1280:720:(ow-iw)/2:(oh-ih)/2,setsar=1,fps=24,format=yuv420p"
: > chorus_clips/concat.txt
i=1
for u in "${URLS[@]}"; do
  raw=$(printf "chorus_clips/raw_%02d.mp4" "$i")
  seg=$(printf "chorus_clips/seg_%02d.mp4" "$i")
  [ -s "$raw" ] || { echo "  get angle $i"; curl -fSL --retry 4 --retry-delay 2 -o "$raw" "$u"; }
  # normalize each to a uniform format, KEEP the clip's own synced vocal audio
  ffmpeg -nostdin -y -loglevel error -i "$raw" -vf "$VF" -r 24 \
    -c:v libx264 -preset medium -crf 18 -video_track_timescale 12800 \
    -c:a aac -b:a 256k -ar 48000 "$seg"
  echo "file '$(basename "$seg")'" >> chorus_clips/concat.txt
  i=$((i+1))
done

( cd chorus_clips && ffmpeg -nostdin -y -loglevel error -f concat -safe 0 -i concat.txt -c copy ../chorus_preview.mp4 )
dur=$(ffprobe -v error -show_entries format=duration -of default=nk=1:nw=1 chorus_preview.mp4 2>/dev/null || echo "?")
echo "Wrote chorus_preview.mp4  (${dur}s, 6 angles, your voice + lip-sync)"
