#!/usr/bin/env bash
# render_intro_v1.sh — the film's opening 22s per INTRO_SCENE_SPEC.md:
#   rain on glass (long hold) -> him in bed, still -> the untouched half (insert)
#   -> he wakes and rises (same take, measured @7.6s) -> V1 opens at the window
#   -> THE BUTTON on "I think I feel you": ambiguous shape composited into the
#   glass at 0.30 for 1.5s -> gone.
#
# Usage:  cd when-it-rains && bash scripts/render_intro_v1.sh && open intro_v1.mp4
set -euo pipefail
cd "$(dirname "$0")/.."
command -v ffmpeg >/dev/null 2>&1 || { echo "ERROR: install ffmpeg (brew install ffmpeg)"; exit 1; }
[ -s audio_relay/intro_open.mp3 ] || { echo "ERROR: audio_relay/intro_open.mp3 missing (git pull)"; exit 1; }
B="https://d8j0ntlcm91z4.cloudfront.net/user_3FjIki1qP1YKJkNjWdqvy8pFZnR"
GHOST_OPACITY=0.30   # the ambiguous shape — barely there
mkdir -p intro1; : > intro1/concat.txt
VF="scale=1280:720:force_original_aspect_ratio=decrease,pad=1280:720:(ow-iw)/2:(oh-ih)/2,setsar=1"

get() { [ -s "intro1/$2" ] || { echo "  get $2"; curl -fSL --retry 4 --retry-delay 2 -o "intro1/$2" "$1"; }; }
get "$B/hf_20260701_234433_086b45d2-f014-403a-881c-c782e19f8edf.mp4" rain.mp4    # rain on the pane
get "$B/hf_20260701_234436_0f7abae9-8ad2-44cd-b83c-5760e054bca3.mp4" bed.mp4     # THE bed take (his only body source here)
get "$B/hf_20260701_234940_31dad2a4-b739-440a-ae5b-b533c59c5965.mp4" bedside.mp4 # the untouched half (no him)
get "$B/hf_20260701_234439_2280a662-c5e2-4bf2-aa65-4d5535bd6783.mp4" window.mp4  # V1 window take
get "$B/hf_20260701_234443_f4405992-922d-448f-af9b-4806393a556e.png" shape.png   # ambiguous shape (with-shape still)

seg() { # file in dur idx
  ffmpeg -nostdin -y -loglevel error -ss "$2" -t "$3" -i "intro1/$1" -vf "$VF,fps=24,format=yuv420p" -r 24 -an \
    -c:v libx264 -preset medium -crf 18 -video_track_timescale 12800 "$(printf "intro1/seg_%02d.mp4" "$4")"
  echo "file '$(printf "seg_%02d.mp4" "$4")'" >> intro1/concat.txt
}

seg rain.mp4    0.50 6.00 0   # 0:00-0:06  the first breath
seg bed.mp4     1.50 5.80 1   # 0:06-0:11.8  lying still (measured: stillness 0-7.3s)
seg bedside.mp4 0.60 3.90 2   # 0:11.8-0:15.7  the made, untouched half
seg bed.mp4     7.60 2.30 3   # 0:15.7-0:18  he wakes, rises (measured @~8s)
seg window.mp4  0.80 1.60 4   # 0:18-0:19.6  V1 opens: at the window

# seg 5 — THE BUTTON (19.6-21.1): shape still composited over the take @ GHOST_OPACITY
ffmpeg -nostdin -y -loglevel error \
  -ss 2.40 -t 1.50 -i intro1/window.mp4 \
  -loop 1 -t 1.50 -i intro1/shape.png \
  -filter_complex "[0:v]${VF},setpts=PTS-STARTPTS[bg];[1:v]${VF},setpts=PTS-STARTPTS,format=yuva420p,colorchannelmixer=aa=${GHOST_OPACITY}[fg];[bg][fg]overlay=shortest=1,fps=24,format=yuv420p" \
  -an -c:v libx264 -preset medium -crf 18 -video_track_timescale 12800 intro1/seg_05.mp4
echo "file 'seg_05.mp4'" >> intro1/concat.txt

seg window.mp4  3.90 0.90 6   # 0:21.1-0:22  he refocuses — the glass is just glass

( cd intro1 && ffmpeg -nostdin -y -loglevel error -f concat -safe 0 -i concat.txt -c copy silent.mp4 )
ffmpeg -nostdin -y -loglevel error -i intro1/silent.mp4 -i audio_relay/intro_open.mp3 \
  -map 0:v:0 -map 1:a:0 -c:v copy -c:a aac -b:a 256k -shortest intro_v1.mp4
dur=$(ffprobe -v error -show_entries format=duration -of default=nk=1:nw=1 intro_v1.mp4 2>/dev/null || echo "?")
echo "Wrote intro_v1.mp4  (${dur}s — the film's opening: rain, the bed, the untouched half, the rise, the maybe-her)"
