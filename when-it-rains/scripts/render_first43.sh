#!/usr/bin/env bash
# render_first43.sh — the film so far, continuous: intro_v6 (song 0-24) +
# v1_v1 from its 0.5s mark (song 24-43), muxed over ONE unbroken audio slice
# (audio_relay/first43.mp3, song 0-43). Both sources are LOCKED cuts already
# committed to the repo — no CDN fetches needed.
set -euo pipefail
cd "$(dirname "$0")/.."
command -v ffmpeg >/dev/null 2>&1 || { echo "ERROR: install ffmpeg"; exit 1; }
[ -s audio_relay/first43.mp3 ] || { echo "ERROR: audio_relay/first43.mp3 missing (git pull)"; exit 1; }
[ -s intro_v6.mp4 ] || { echo "ERROR: intro_v6.mp4 missing"; exit 1; }
[ -s v1_v1.mp4 ] || { echo "ERROR: v1_v1.mp4 missing"; exit 1; }
mkdir -p first43; : > first43/concat.txt
VF="scale=1280:720:force_original_aspect_ratio=decrease,pad=1280:720:(ow-iw)/2:(oh-ih)/2,setsar=1"

ffmpeg -nostdin -y -loglevel error -t 24.0 -i intro_v6.mp4 -vf "$VF,fps=24,format=yuv420p" -r 24 -an \
  -c:v libx264 -preset medium -crf 18 -video_track_timescale 12800 first43/seg_00.mp4
echo "file 'seg_00.mp4'" >> first43/concat.txt
ffmpeg -nostdin -y -loglevel error -ss 0.5 -i v1_v1.mp4 -vf "$VF,fps=24,format=yuv420p" -r 24 -an \
  -c:v libx264 -preset medium -crf 18 -video_track_timescale 12800 first43/seg_01.mp4
echo "file 'seg_01.mp4'" >> first43/concat.txt

( cd first43 && ffmpeg -nostdin -y -loglevel error -f concat -safe 0 -i concat.txt -c copy silent.mp4 )
ffmpeg -nostdin -y -loglevel error -i first43/silent.mp4 -i audio_relay/first43.mp3 \
  -map 0:v:0 -map 1:a:0 -c:v copy -c:a aac -b:a 256k -shortest first43.mp4
dur=$(ffprobe -v error -show_entries format=duration -of default=nk=1:nw=1 first43.mp4 2>/dev/null || echo "?")
echo "Wrote first43.mp4  (${dur}s — the film so far: bedroom morning through the kitchen verse)"
