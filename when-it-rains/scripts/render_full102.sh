#!/usr/bin/env bash
# render_full102.sh — the full first ~102s: intro_v6 + v1_v2 + v2_v2 (4K curb-zoom
# fix) + pre1_v1 (no-turn street) + storm insert + chorus_v16 from FRAME 7.
# Continuous song bed (first102.mp3 = song 0-102). Extends render_p024's proven
# frame-exact grid (576/456/655/468) with two appended segs (storm 37f, chorus 252f).
set -euo pipefail
HERE="$(dirname "$0")"
bash "$HERE/render_intro_v6.sh"      # rebuilds intro_v6.mp4 (push-in reverted -> known-good intro)
# v2_v2.mp4 (curb cutaway) + pre1_v1.mp4 (no-turn street) + chorus_v17.mp4 are already
# committed and correct — reuse them (avoids the slow double-4K curb re-render).
cd "$HERE/.."
command -v ffmpeg >/dev/null 2>&1 || { echo "ERROR: install ffmpeg"; exit 1; }
[ -s audio_relay/first102.mp3 ] || { echo "ERROR: audio_relay/first102.mp3 missing"; exit 1; }
for f in intro_v6.mp4 v1_v2.mp4 v2_v2.mp4 pre1_v1.mp4 chorus_v17.mp4; do
  [ -s "$f" ] || { echo "ERROR: $f missing"; exit 1; }
done
B="https://d8j0ntlcm91z4.cloudfront.net/user_3FjIki1qP1YKJkNjWdqvy8pFZnR"
mkdir -p full102; : > full102/concat.txt
VF="scale=1920:1080:force_original_aspect_ratio=decrease,pad=1920:1080:(ow-iw)/2:(oh-ih)/2,setsar=1"
VFG="$VF,noise=alls=5:allf=t+u,eq=saturation=0.93:contrast=1.03"
get() { [ -s "full102/$2" ] || { echo "  get $2"; curl -fSL --retry 4 --retry-delay 2 -o "full102/$2" "$1"; }; }
get "$B/hf_20260703_145658_3d0619c6-3b9c-4f10-b7f9-1f3f309c2605.mp4" trees.mp4   # storm/gust insert

emit() { echo "file '$1'" >> full102/concat.txt; }
# --- first 90 (proven grid) ---
ffmpeg -nostdin -y -loglevel error -t 25.0 -i intro_v6.mp4 -vf "$VFG,fps=24,tpad=stop_mode=clone:stop_duration=1.0,trim=end_frame=576,format=yuv420p" -r 24 -an \
  -c:v libx264 -preset medium -crf 18 -video_track_timescale 12800 full102/seg_00.mp4; emit seg_00.mp4
ffmpeg -nostdin -y -loglevel error -ss 0.5 -i v1_v2.mp4 -vf "$VF,fps=24,tpad=stop_mode=clone:stop_duration=1.0,trim=end_frame=456,format=yuv420p" -r 24 -an \
  -c:v libx264 -preset medium -crf 18 -video_track_timescale 12800 full102/seg_01.mp4; emit seg_01.mp4
ffmpeg -nostdin -y -loglevel error -i v2_v2.mp4 -vf "$VF,fps=24,tpad=stop_mode=clone:stop_duration=1.0,trim=end_frame=655,format=yuv420p" -r 24 -an \
  -c:v libx264 -preset medium -crf 18 -video_track_timescale 12800 full102/seg_02.mp4; emit seg_02.mp4
ffmpeg -nostdin -y -loglevel error -i pre1_v1.mp4 -vf "$VF,fps=24,tpad=stop_mode=clone:stop_duration=1.0,trim=end_frame=468,format=yuv420p" -r 24 -an \
  -c:v libx264 -preset medium -crf 18 -video_track_timescale 12800 full102/seg_03.mp4; emit seg_03.mp4
# --- storm insert (89.79-91.33, 37 frames) covering "when it rains you're in the wa-" ---
ffmpeg -nostdin -y -loglevel error -ss 2.80 -i full102/trees.mp4 -vf "$VFG,fps=24,trim=end_frame=37,format=yuv420p" -r 24 -an \
  -c:v libx264 -preset medium -crf 18 -video_track_timescale 12800 full102/seg_04.mp4; emit seg_04.mp4
# --- chorus_v16 from FRAME 7 (in 1.50 = native song 91.32), mic->puddle->mic->cafe, 252 frames ---
ffmpeg -nostdin -y -loglevel error -ss 1.50 -i chorus_v17.mp4 -vf "$VF,fps=24,trim=end_frame=252,format=yuv420p" -r 24 -an \
  -c:v libx264 -preset medium -crf 18 -video_track_timescale 12800 full102/seg_05.mp4; emit seg_05.mp4

( cd full102 && ffmpeg -nostdin -y -loglevel error -f concat -safe 0 -i concat.txt -c copy silent.mp4 )
ffmpeg -nostdin -y -loglevel error -i full102/silent.mp4 -i audio_relay/first102.mp3 \
  -map 0:v:0 -map 1:a:0 -c:v copy -c:a aac -b:a 256k -shortest full102_master.mp4
# small phone-safe delivery encode
ffmpeg -nostdin -y -loglevel error -i full102_master.mp4 \
  -vf "scale=1280:720:force_original_aspect_ratio=decrease,pad=1280:720:(ow-iw)/2:(oh-ih)/2,setsar=1" \
  -c:v libx264 -preset medium -crf 26 -pix_fmt yuv420p -profile:v main -level 3.1 \
  -c:a aac -b:a 160k -ac 2 -ar 44100 -movflags +faststart full102.mp4
mdur=$(ffprobe -v error -show_entries format=duration -of default=nk=1:nw=1 full102_master.mp4 2>/dev/null || echo "?")
echo "wrote full102_master.mp4 (${mdur}s) + full102.mp4 (720 delivery)"
# QC frames of the whole cut
mkdir -p review/full102_frames
ffmpeg -nostdin -y -loglevel error -i full102_master.mp4 -vf "fps=1,scale=480:-2" -q:v 4 review/full102_frames/f_%03d.jpg
echo "wrote QC frames"
