#!/usr/bin/env bash
# render_flow_demo3.sh — the CORRECT street->chorus rework.
#   * ORIGINAL street take (84b73e44, no regen -> hair matches) "like you never left"
#   * 1.5s STORM insert (trees/gust) = the connective a director drops in, covering
#     "when it rains you're in the wa-" (89.82-91.32)
#   * chorus_v16 started on FRAME 7 (in-point 1.50s) -> the mic clip's dead front
#     is trimmed; frame 7 == native song 91.32, so the mic lip-sync stays perfect.
#   * puddle -> mic -> cafe montage kept in the ORIGINAL order (chorus_v16 intact
#     from 1.50s on).
#   One continuous song bed (flow_demo_bed.mp3 = song 82.02 +20s) keeps street,
#   insert and chorus all perfectly aligned (song-time is continuous across cuts).
set -euo pipefail
cd "$(dirname "$0")/.."
command -v ffmpeg >/dev/null 2>&1 || { echo "ERROR: install ffmpeg"; exit 1; }
[ -s audio_relay/flow_demo_bed.mp3 ] || { echo "ERROR: flow_demo_bed.mp3 missing"; exit 1; }
[ -s chorus_v16.mp4 ] || { echo "ERROR: chorus_v16.mp4 missing"; exit 1; }
B="https://d8j0ntlcm91z4.cloudfront.net/user_3FjIki1qP1YKJkNjWdqvy8pFZnR"
mkdir -p flowdemo3; : > flowdemo3/concat.txt
VFG="scale=1280:720:force_original_aspect_ratio=decrease,pad=1280:720:(ow-iw)/2:(oh-ih)/2,setsar=1,noise=alls=5:allf=t+u,eq=saturation=0.93:contrast=1.03"
VFP="scale=1280:720:force_original_aspect_ratio=decrease,pad=1280:720:(ow-iw)/2:(oh-ih)/2,setsar=1"
get() { [ -s "flowdemo3/$2" ] || { echo "  get $2"; curl -fSL --retry 4 --retry-delay 2 -o "flowdemo3/$2" "$1"; }; }
get "$B/hf_20260704_133740_84b73e44-5859-4ff0-9278-6440159aed27.mp4" street.mp4
get "$B/hf_20260703_145658_3d0619c6-3b9c-4f10-b7f9-1f3f309c2605.mp4" trees.mp4

emit() { echo "file '$1'" >> flowdemo3/concat.txt; }
# seg 0 — street "like you never left" (82.02-89.82), in 0.10 for 7.80
ffmpeg -nostdin -y -loglevel error -ss 0.10 -t 7.80 -i flowdemo3/street.mp4 \
  -vf "$VFG,fps=24,format=yuv420p" -an -r 24 \
  -c:v libx264 -preset medium -crf 20 -video_track_timescale 12800 flowdemo3/seg_00.mp4; emit seg_00.mp4
# seg 1 — 1.5s storm insert (peak gust), covering 89.82-91.32
ffmpeg -nostdin -y -loglevel error -ss 2.80 -t 1.50 -i flowdemo3/trees.mp4 \
  -vf "$VFG,fps=24,format=yuv420p" -an -r 24 \
  -c:v libx264 -preset medium -crf 20 -video_track_timescale 12800 flowdemo3/seg_01.mp4; emit seg_01.mp4
# seg 2 — chorus_v16 from FRAME 7 (in 1.50 = song 91.32) to end, ORIGINAL montage order
ffmpeg -nostdin -y -loglevel error -ss 1.50 -i chorus_v16.mp4 \
  -vf "$VFP,fps=24,format=yuv420p" -an -r 24 \
  -c:v libx264 -preset medium -crf 20 -video_track_timescale 12800 flowdemo3/seg_02.mp4; emit seg_02.mp4

( cd flowdemo3 && ffmpeg -nostdin -y -loglevel error -f concat -safe 0 -i concat.txt -c copy silent.mp4 )
# one continuous song bed over the whole thing (perfect sync for street + mic)
ffmpeg -nostdin -y -loglevel error -i flowdemo3/silent.mp4 -i audio_relay/flow_demo_bed.mp3 \
  -map 0:v:0 -map 1:a:0 -c:v libx264 -preset medium -crf 24 -pix_fmt yuv420p -profile:v main -level 3.1 \
  -c:a aac -b:a 160k -ac 2 -ar 44100 -movflags +faststart -shortest flow_demo3.mp4
dur=$(ffprobe -v error -show_entries format=duration -of default=nk=1:nw=1 flow_demo3.mp4 2>/dev/null || echo "?")
echo "wrote flow_demo3.mp4 (${dur}s)"

# QC frames for the sandbox
mkdir -p review/flowdemo3_frames
ffmpeg -nostdin -y -loglevel error -i flow_demo3.mp4 -vf "fps=3,scale=560:-2" -q:v 4 review/flowdemo3_frames/f_%03d.jpg
echo "wrote QC frames"
