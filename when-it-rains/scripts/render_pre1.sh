#!/usr/bin/env bash
# render_pre1.sh — PRE1 "the darkening walk" (70.3-89.8, 19.5s), P-024.
# walk (tracking cam settles as he stops) -> stop+breath fog -> trees gust
# insert -> THE TURN: lip-sync "like you never left" to the empty street,
# exits with purpose toward the cafe (CH1 cause).
set -euo pipefail
cd "$(dirname "$0")/.."
command -v ffmpeg >/dev/null 2>&1 || { echo "ERROR: install ffmpeg"; exit 1; }
[ -s audio_relay/pre1_bed.mp3 ] || { echo "ERROR: audio_relay/pre1_bed.mp3 missing (needs song.mp3 slice 70.3-89.8)"; exit 1; }
B="https://d8j0ntlcm91z4.cloudfront.net/user_3FjIki1qP1YKJkNjWdqvy8pFZnR"
mkdir -p pre1sec; : > pre1sec/concat.txt
VF="scale=1280:720:force_original_aspect_ratio=decrease,pad=1280:720:(ow-iw)/2:(oh-ih)/2,setsar=1,noise=alls=5:allf=t+u,eq=saturation=0.93:contrast=1.03"
get() { [ -s "pre1sec/$2" ] || { echo "  get $2"; curl -fSL --retry 4 --retry-delay 2 -o "pre1sec/$2" "$1"; }; }
get "$B/hf_20260703_135740_d035bb3b-e0ce-47e4-af97-06355884ca30.mp4" walk.mp4      # walk-stop-breath take (P-025 realism refit)
get "$B/hf_20260703_114838_8543a623-7cc9-4ef5-be1a-68008df05334.mp4" trees.mp4     # gust insert
get "$B/hf_20260703_130622_c6888a50-e111-4f3a-84f6-9261a45a4965.mp4" turnsync.mp4   # wan "like you never left" 2K

seg() { ffmpeg -nostdin -y -loglevel error -ss "$2" -t "$3" -i "pre1sec/$1" -vf "$VF,fps=24,format=yuv420p" -r 24 -an \
  -c:v libx264 -preset medium -crf 18 -video_track_timescale 12800 "$(printf "pre1sec/seg_%02d.mp4" "$4")"
  echo "file '$(printf "seg_%02d.mp4" "$4")'" >> pre1sec/concat.txt; }

seg walk.mp4  0.00 3.90 0   # 70.3-74.2 "don't know if you still feel it" — the fast walk (cam tracks, then settles)
seg walk.mp4  5.50 3.90 1   # 74.2-78.1 "I lose my breath" — settle, STOP at 7.0, breath fog 7.0-8.5
seg trees.mp4 0.80 3.90 2   # 78.1-82.0 "the trees are moving" — gust builds 2.0, peaks 2.5-3.0
# 82.0-89.8 "like you never left" — TURN SYNC (in-point = slot_start - slice_start; set when slice exists)
seg turnsync.mp4 0.10 7.80 3

( cd pre1sec && ffmpeg -nostdin -y -loglevel error -f concat -safe 0 -i concat.txt -c copy silent.mp4 )
ffmpeg -nostdin -y -loglevel error -i pre1sec/silent.mp4 -i audio_relay/pre1_bed.mp3 \
  -map 0:v:0 -map 1:a:0 -c:v copy -c:a aac -b:a 256k -shortest pre1_v1.mp4
echo "Wrote pre1_v1.mp4"
