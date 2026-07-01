#!/usr/bin/env bash
# render_chorus_v15.sh — v14 with a COMPOSITED reflection insert:
#   her insert clip is blended at 55% opacity over an identical "empty case" plate,
#   so the pastries genuinely show through her at a controlled, guaranteed level.
#   Real VFX translucency (math), not a prompt suggestion.
#
# Usage:  cd when-it-rains && bash scripts/render_chorus_v15.sh && open chorus_v15.mp4
set -euo pipefail
cd "$(dirname "$0")/.."
command -v ffmpeg >/dev/null 2>&1 || { echo "ERROR: install ffmpeg (brew install ffmpeg)"; exit 1; }
[ -s audio_relay/chorus_couplet.mp3 ] || { echo "ERROR: audio_relay/chorus_couplet.mp3 missing (git pull)"; exit 1; }
B="https://d8j0ntlcm91z4.cloudfront.net/user_3FjIki1qP1YKJkNjWdqvy8pFZnR"
GHOST_OPACITY=0.55   # her layer's opacity over the empty plate (lower = more ghostly)
mkdir -p chorus15; : > chorus15/concat.txt
VF="scale=1280:720:force_original_aspect_ratio=decrease,pad=1280:720:(ow-iw)/2:(oh-ih)/2,setsar=1"

get() { [ -s "chorus15/$2" ] || { echo "  get $2"; curl -fSL --retry 4 --retry-delay 2 -o "chorus15/$2" "$1"; }; }
get "$B/hf_20260701_165718_491e39d1-548b-49ea-9f40-aa70ecef1d12.mp4" hero.mp4    # ORIGINAL hero (kept)
get "$B/hf_20260701_201522_b22edfc6-01f3-4d78-8f75-2e611da0eb8a.mp4" puddle.mp4  # her in the puddle (v5)
get "$B/hf_20260701_211804_c1ffc156-7682-4fb5-8ba3-29e4a554df6a.mp4" take.mp4    # THE one-take
get "$B/hf_20260701_222907_6b3be8f1-7d15-401f-b44a-2fbe1fd92289.mp4" insert.mp4  # her reflection clip (fg layer)
get "$B/hf_20260701_224652_ec557078-0f7e-40ff-a950-3ad3736ba374.png" empty.png   # empty-case plate (bg layer)

seg() { # file in dur idx  — normal trimmed segment
  ffmpeg -nostdin -y -loglevel error -ss "$2" -t "$3" -i "chorus15/$1" -vf "$VF,fps=24,format=yuv420p" -r 24 -an \
    -c:v libx264 -preset medium -crf 18 -video_track_timescale 12800 "$(printf "chorus15/seg_%02d.mp4" "$4")"
  echo "file '$(printf "seg_%02d.mp4" "$4")'" >> chorus15/concat.txt
}

seg hero.mp4   0.00 2.95 0    # HERO held — "when it rains you're in the water"
seg puddle.mp4 1.00 1.95 1    # her, only in the puddle's reflection
seg hero.mp4   4.90 0.97 2    # quick hero return
seg take.mp4   1.00 1.95 3    # beat 1: in line, gaze drifts down to the case

# seg 4 — the COMPOSITED reveal: her clip at ${GHOST_OPACITY} over the empty plate
ffmpeg -nostdin -y -loglevel error \
  -loop 1 -t 1.95 -i chorus15/empty.png \
  -ss 0.80 -t 1.95 -i chorus15/insert.mp4 \
  -filter_complex "[0:v]${VF}[bg];[1:v]${VF},format=yuva420p,colorchannelmixer=aa=${GHOST_OPACITY}[fg];[bg][fg]overlay=shortest=1,fps=24,format=yuv420p" \
  -an -c:v libx264 -preset medium -crf 18 -video_track_timescale 12800 chorus15/seg_04.mp4
echo "file 'seg_04.mp4'" >> chorus15/concat.txt

seg take.mp4   6.90 2.23 5    # beat 2: same take — he turns; no one

( cd chorus15 && ffmpeg -nostdin -y -loglevel error -f concat -safe 0 -i concat.txt -c copy silent.mp4 )
ffmpeg -nostdin -y -loglevel error -i chorus15/silent.mp4 -i audio_relay/chorus_couplet.mp3 \
  -map 0:v:0 -map 1:a:0 -c:v copy -c:a aac -b:a 256k -shortest chorus_v15.mp4
dur=$(ffprobe -v error -show_entries format=duration -of default=nk=1:nw=1 chorus_v15.mp4 2>/dev/null || echo "?")
echo "Wrote chorus_v15.mp4  (${dur}s — composited ghost reflection @ ${GHOST_OPACITY})"
