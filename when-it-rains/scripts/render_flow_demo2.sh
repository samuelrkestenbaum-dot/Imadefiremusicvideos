#!/usr/bin/env bash
# render_flow_demo2.sh — EXTENDED street lead-in -> chorus hook hand-off.
# The street take now sings BOTH "like you never left" (82.02) AND rolls
# straight into "when it rains you're in the water" (89.82-93.72) to camera,
# no turn/exit; then a short DISSOLVE hands to the cafe chorus, which lands
# fully-visible exactly on "like the thunder" (93.72). One continuous song bed
# (lead_bed.mp3 = song 82.02 +18.4s) keeps street AND cafe perfectly in sync
# straight through the dissolve.
set -euo pipefail
cd "$(dirname "$0")/.."
command -v ffmpeg >/dev/null 2>&1 || { echo "ERROR: install ffmpeg"; exit 1; }
[ -s audio_relay/lead_bed.mp3 ] || { echo "ERROR: lead_bed.mp3 missing"; exit 1; }
[ -s chorus_v16.mp4 ] || { echo "ERROR: chorus_v16.mp4 missing"; exit 1; }
B="https://d8j0ntlcm91z4.cloudfront.net/user_3FjIki1qP1YKJkNjWdqvy8pFZnR"
mkdir -p flowdemo2
VFG="scale=1280:720:force_original_aspect_ratio=decrease,pad=1280:720:(ow-iw)/2:(oh-ih)/2,setsar=1,noise=alls=5:allf=t+u,eq=saturation=0.93:contrast=1.03"
VFP="scale=1280:720:force_original_aspect_ratio=decrease,pad=1280:720:(ow-iw)/2:(oh-ih)/2,setsar=1"
get() { [ -s "flowdemo2/$2" ] || { echo "  get $2"; curl -fSL --retry 4 --retry-delay 2 -o "flowdemo2/$2" "$1"; }; }

# --- the extended street take (wan 1cfafdb2, 1080p, 12s: 81.92-93.92) ---
get "$B/__TAKE__" take.mp4

# street video: in 0.10 (=82.02) for 11.75s -> to 93.77 (past the 93.72 cut)
ffmpeg -nostdin -y -loglevel error -ss 0.10 -t 11.75 -i flowdemo2/take.mp4 \
  -vf "$VFG,fps=24,format=yuv420p" -an -r 24 \
  -c:v libx264 -preset medium -crf 20 -video_track_timescale 12800 flowdemo2/street.mp4

# cafe video: in 3.50 (=93.32, 0.4s before "like the thunder") for 7.00s, silent
ffmpeg -nostdin -y -loglevel error -ss 3.50 -t 7.00 -i chorus_v16.mp4 \
  -vf "$VFP,fps=24,format=yuv420p" -an -r 24 \
  -c:v libx264 -preset medium -crf 20 -video_track_timescale 12800 flowdemo2/cafe.mp4

# xfade street->cafe: dissolve completes at 11.30+0.40 = 11.70 = song 93.72
# ("like the thunder"), so the cafe is fully in on the beat. Then mux the one
# continuous song bed over the whole thing (perfectly synced to both clips).
ffmpeg -nostdin -y -loglevel error \
  -i flowdemo2/street.mp4 -i flowdemo2/cafe.mp4 -i audio_relay/lead_bed.mp3 \
  -filter_complex "[0:v][1:v]xfade=transition=fade:duration=0.40:offset=11.30,format=yuv420p[v]" \
  -map "[v]" -map 2:a:0 -t 18.30 -r 24 \
  -c:v libx264 -preset medium -crf 24 -pix_fmt yuv420p -profile:v main -level 3.1 \
  -c:a aac -b:a 160k -ac 2 -ar 44100 -movflags +faststart flow_demo2.mp4
dur=$(ffprobe -v error -show_entries format=duration -of default=nk=1:nw=1 flow_demo2.mp4 2>/dev/null || echo "?")
echo "wrote flow_demo2.mp4 (${dur}s)"
