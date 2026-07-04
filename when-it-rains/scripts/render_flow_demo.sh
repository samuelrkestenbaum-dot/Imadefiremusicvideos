#!/usr/bin/env bash
# render_flow_demo.sh — show the TURN -> CHORUS hand-off in context.
# turn shot (82.0-89.8, "like you never left") + locked chorus_v16
# (89.8-101.8, "when it rains you're in the water...") under one continuous
# song bed, so the transition can be judged as it actually plays.
set -euo pipefail
cd "$(dirname "$0")/.."
command -v ffmpeg >/dev/null 2>&1 || { echo "ERROR: install ffmpeg"; exit 1; }
[ -s audio_relay/flow_demo_bed.mp3 ] || { echo "ERROR: flow_demo_bed.mp3 missing"; exit 1; }
[ -s chorus_v16.mp4 ] || { echo "ERROR: chorus_v16.mp4 missing"; exit 1; }
B="https://d8j0ntlcm91z4.cloudfront.net/user_3FjIki1qP1YKJkNjWdqvy8pFZnR"
mkdir -p flowdemo; : > flowdemo/concat.txt
VFG="scale=1280:720:force_original_aspect_ratio=decrease,pad=1280:720:(ow-iw)/2:(oh-ih)/2,setsar=1,noise=alls=5:allf=t+u,eq=saturation=0.93:contrast=1.03"
VFP="scale=1280:720:force_original_aspect_ratio=decrease,pad=1280:720:(ow-iw)/2:(oh-ih)/2,setsar=1"
get() { [ -s "flowdemo/$2" ] || { echo "  get $2"; curl -fSL --retry 4 --retry-delay 2 -o "flowdemo/$2" "$1"; }; }
get "$B/hf_20260704_130632_fc47fa23-c0b0-4439-b446-5a368ce954c7.mp4" turn.mp4
# turn seg 82.0-89.8 (in 0.10, 7.80s) — grain to match the film
ffmpeg -nostdin -y -loglevel error -ss 0.10 -t 7.80 -i flowdemo/turn.mp4 -vf "$VFG,fps=24,format=yuv420p" -r 24 -an \
  -c:v libx264 -preset medium -crf 20 -video_track_timescale 12800 flowdemo/seg_00.mp4
echo "file 'seg_00.mp4'" >> flowdemo/concat.txt
# locked chorus (already graded/grained) — plain scale, video only
ffmpeg -nostdin -y -loglevel error -i chorus_v16.mp4 -vf "$VFP,fps=24,format=yuv420p" -r 24 -an \
  -c:v libx264 -preset medium -crf 20 -video_track_timescale 12800 flowdemo/seg_01.mp4
echo "file 'seg_01.mp4'" >> flowdemo/concat.txt
( cd flowdemo && ffmpeg -nostdin -y -loglevel error -f concat -safe 0 -i concat.txt -c copy silent.mp4 )
ffmpeg -nostdin -y -loglevel error -i flowdemo/silent.mp4 -i audio_relay/flow_demo_bed.mp3 \
  -map 0:v:0 -map 1:a:0 -c:v libx264 -profile:v main -level 3.1 -preset medium -crf 24 -pix_fmt yuv420p \
  -c:a aac -b:a 160k -ac 2 -ar 44100 -movflags +faststart -shortest flow_demo.mp4
dur=$(ffprobe -v error -show_entries format=duration -of default=nk=1:nw=1 flow_demo.mp4 2>/dev/null || echo "?")
echo "wrote flow_demo.mp4 (${dur}s)"
