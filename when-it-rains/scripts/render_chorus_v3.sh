#!/usr/bin/env bash
# render_chorus_v3.sh — the DIRECTOR'S chorus: atmosphere-led, your hero shot held on
# the hooks, the storm + her carrying the releases ("in the water" / "like the thunder").
# Uses only footage that already works + the committed couplet vocal. Needs only ffmpeg.
#
# Usage:  cd when-it-rains && bash scripts/render_chorus_v3.sh && open chorus_v3.mp4
set -euo pipefail
cd "$(dirname "$0")/.."
command -v ffmpeg >/dev/null 2>&1 || { echo "ERROR: install ffmpeg (brew install ffmpeg)"; exit 1; }
[ -s audio_relay/chorus_couplet.mp3 ] || { echo "ERROR: audio_relay/chorus_couplet.mp3 missing (git pull)"; exit 1; }
B="https://d8j0ntlcm91z4.cloudfront.net/user_3FjIki1qP1YKJkNjWdqvy8pFZnR"
mkdir -p chorus3; : > chorus3/concat.txt
VF="scale=1280:720:force_original_aspect_ratio=decrease,pad=1280:720:(ow-iw)/2:(oh-ih)/2,setsar=1,fps=24,format=yuv420p"

get() { [ -s "chorus3/$2" ] || { echo "  get $2"; curl -fSL --retry 4 --retry-delay 2 -o "chorus3/$2" "$1"; }; }
get "$B/hf_20260701_165718_491e39d1-548b-49ea-9f40-aa70ecef1d12.mp4" hero.mp4       # you, hero (real vocal, looks like you)
get "$B/hf_20260701_151102_ba6f80d3-bf4e-4dad-8ad0-bc9191d231e7.mp4" her.mp4        # her in the rain
get "$B/hf_20260701_151505_19aef6dc-3648-4166-8477-f5e1a7337298.mp4" lightning.mp4  # lightning ("thunder")
get "$B/hf_20260701_151534_8151b0b4-e370-4ce7-9bd1-36bdc796c11e.mp4" clouds.mp4     # her figure in the storm sky
get "$B/hf_20260701_151123_90bc84b2-e7ec-4801-acbc-0df77e6efcae.mp4" rain.mp4       # silver rain plate

# cut list (file  in_point  duration). Hero in_points == output start so they stay lip-synced.
CUTS=(
  "hero.mp4 0.00 2.95"       # HERO held — "when it rains you're in the water"
  "her.mp4 1.00 1.95"        # her, in the rain  ("...in the water")
  "hero.mp4 4.90 0.97"       # quick hero return
  "lightning.mp4 0.40 1.95"  # lightning         ("...like the thunder")
  "clouds.mp4 1.00 1.95"     # her in the storm sky
  "rain.mp4 0.50 2.23"       # rain, storm close
)
i=0
for c in "${CUTS[@]}"; do
  set -- $c; f=$1; ip=$2; du=$3
  seg=$(printf "chorus3/seg_%02d.mp4" "$i")
  ffmpeg -nostdin -y -loglevel error -ss "$ip" -t "$du" -i "chorus3/$f" -vf "$VF" -r 24 -an \
    -c:v libx264 -preset medium -crf 18 -video_track_timescale 12800 "$seg"
  echo "file '$(basename "$seg")'" >> chorus3/concat.txt
  i=$((i+1))
done

( cd chorus3 && ffmpeg -nostdin -y -loglevel error -f concat -safe 0 -i concat.txt -c copy silent.mp4 )
ffmpeg -nostdin -y -loglevel error -i chorus3/silent.mp4 -i audio_relay/chorus_couplet.mp3 \
  -map 0:v:0 -map 1:a:0 -c:v copy -c:a aac -b:a 256k -shortest chorus_v3.mp4
dur=$(ffprobe -v error -show_entries format=duration -of default=nk=1:nw=1 chorus_v3.mp4 2>/dev/null || echo "?")
echo "Wrote chorus_v3.mp4  (${dur}s — atmosphere-led: hero on the hooks, storm + her on the releases)"
