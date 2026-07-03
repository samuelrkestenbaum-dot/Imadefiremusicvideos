#!/usr/bin/env bash
# render_p022.sh — P-022 wrapper: recut both repaired sections, then stitch
# the continuous first 70.3 seconds (intro_v6 + v1_v2 + v2_v2, one audio).
set -euo pipefail
HERE="$(dirname "$0")"
bash "$HERE/render_v1_v2.sh"
bash "$HERE/render_v2_v2.sh"
cd "$HERE/.."
[ -s audio_relay/first70.mp3 ] || { echo "ERROR: audio_relay/first70.mp3 missing"; exit 1; }
[ -s intro_v6.mp4 ] || { echo "ERROR: intro_v6.mp4 missing"; exit 1; }
mkdir -p first70; : > first70/concat.txt
VF="scale=1280:720:force_original_aspect_ratio=decrease,pad=1280:720:(ow-iw)/2:(oh-ih)/2,setsar=1"
VFG="$VF,noise=alls=5:allf=t+u,eq=saturation=0.93:contrast=1.03"
ffmpeg -nostdin -y -loglevel error -t 24.0 -i intro_v6.mp4 -vf "$VFG,fps=24,format=yuv420p" -r 24 -an \
  -c:v libx264 -preset medium -crf 18 -video_track_timescale 12800 first70/seg_00.mp4
echo "file 'seg_00.mp4'" >> first70/concat.txt
ffmpeg -nostdin -y -loglevel error -ss 0.5 -i v1_v2.mp4 -vf "$VF,fps=24,format=yuv420p" -r 24 -an \
  -c:v libx264 -preset medium -crf 18 -video_track_timescale 12800 first70/seg_01.mp4
echo "file 'seg_01.mp4'" >> first70/concat.txt
ffmpeg -nostdin -y -loglevel error -i v2_v2.mp4 -vf "$VF,fps=24,format=yuv420p" -r 24 -an \
  -c:v libx264 -preset medium -crf 18 -video_track_timescale 12800 first70/seg_02.mp4
echo "file 'seg_02.mp4'" >> first70/concat.txt
( cd first70 && ffmpeg -nostdin -y -loglevel error -f concat -safe 0 -i concat.txt -c copy silent.mp4 )
ffmpeg -nostdin -y -loglevel error -i first70/silent.mp4 -i audio_relay/first70.mp3 \
  -map 0:v:0 -map 1:a:0 -c:v copy -c:a aac -b:a 256k -shortest first70.mp4
dur=$(ffprobe -v error -show_entries format=duration -of default=nk=1:nw=1 first70.mp4 2>/dev/null || echo "?")
echo "Wrote first70.mp4 (${dur}s) + v1_v2.mp4 + v2_v2.mp4"
