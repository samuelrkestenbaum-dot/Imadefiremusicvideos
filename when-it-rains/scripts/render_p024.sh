#!/usr/bin/env bash
# render_p024.sh — P-024 wrapper: cut PRE1, then stitch the continuous first
# 89.8 seconds (intro_v6 + v1_v2 + v2_v2 + pre1_v1, one audio bed from the
# July Reverb mix).
set -euo pipefail
HERE="$(dirname "$0")"
bash "$HERE/render_pre1.sh"
cd "$HERE/.."
[ -s audio_relay/first90.mp3 ] || { echo "ERROR: audio_relay/first90.mp3 missing"; exit 1; }
[ -s intro_v6.mp4 ] || { echo "ERROR: intro_v6.mp4 missing"; exit 1; }
[ -s v1_v2.mp4 ] || { echo "ERROR: v1_v2.mp4 missing (checkout includes it)"; exit 1; }
[ -s v2_v2.mp4 ] || { echo "ERROR: v2_v2.mp4 missing"; exit 1; }
mkdir -p first90; : > first90/concat.txt
VF="scale=1280:720:force_original_aspect_ratio=decrease,pad=1280:720:(ow-iw)/2:(oh-ih)/2,setsar=1"
VFG="$VF,noise=alls=5:allf=t+u,eq=saturation=0.93:contrast=1.03"
ffmpeg -nostdin -y -loglevel error -t 24.0 -i intro_v6.mp4 -vf "$VFG,fps=24,format=yuv420p" -r 24 -an \
  -c:v libx264 -preset medium -crf 18 -video_track_timescale 12800 first90/seg_00.mp4
echo "file 'seg_00.mp4'" >> first90/concat.txt
ffmpeg -nostdin -y -loglevel error -ss 0.5 -i v1_v2.mp4 -vf "$VF,fps=24,format=yuv420p" -r 24 -an \
  -c:v libx264 -preset medium -crf 18 -video_track_timescale 12800 first90/seg_01.mp4
echo "file 'seg_01.mp4'" >> first90/concat.txt
ffmpeg -nostdin -y -loglevel error -i v2_v2.mp4 -vf "$VF,fps=24,format=yuv420p" -r 24 -an \
  -c:v libx264 -preset medium -crf 18 -video_track_timescale 12800 first90/seg_02.mp4
echo "file 'seg_02.mp4'" >> first90/concat.txt
ffmpeg -nostdin -y -loglevel error -i pre1_v1.mp4 -vf "$VF,fps=24,format=yuv420p" -r 24 -an \
  -c:v libx264 -preset medium -crf 18 -video_track_timescale 12800 first90/seg_03.mp4
echo "file 'seg_03.mp4'" >> first90/concat.txt
( cd first90 && ffmpeg -nostdin -y -loglevel error -f concat -safe 0 -i concat.txt -c copy silent.mp4 )
ffmpeg -nostdin -y -loglevel error -i first90/silent.mp4 -i audio_relay/first90.mp3 \
  -map 0:v:0 -map 1:a:0 -c:v copy -c:a aac -b:a 256k -shortest first90.mp4
dur=$(ffprobe -v error -show_entries format=duration -of default=nk=1:nw=1 first90.mp4 2>/dev/null || echo "?")
echo "Wrote first90.mp4 (${dur}s) + pre1_v1.mp4"
