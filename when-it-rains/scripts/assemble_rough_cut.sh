#!/usr/bin/env bash
# Assemble the 4:36 rough cut of "When It Rains" from the clip library + the song.
# RUN THIS ON YOUR OWN MACHINE. Needs ffmpeg + the clips downloaded (fetch_assets.sh).
#
# Usage:
#   bash scripts/fetch_assets.sh            # 1) get the clips
#   cp /path/to/your_song.wav song.wav      # 2) drop the song in (rename to song.wav)
#   bash scripts/assemble_rough_cut.sh      # 3) build it
#
# Output: when_it_rains_roughcut.mp4  (1280x720, 24fps, song on top, capped at 4:36)
#
# Re-time the edit by editing data/edl.csv (durations / clip keys / in-points)
# and re-running this script. Nothing is baked in.
set -euo pipefail
cd "$(dirname "$0")/.."

command -v ffmpeg >/dev/null 2>&1 || { echo "ERROR: ffmpeg not found. Install it first."; exit 1; }
[ -d clips ] || { echo "ERROR: clips/ missing. Run scripts/fetch_assets.sh first."; exit 1; }

W=1280; H=720; FPS=24; TOTAL=276   # 4:36
BUILD=build
rm -rf "$BUILD"; mkdir -p "$BUILD"
: > "$BUILD/concat.txt"

VF="scale=${W}:${H}:force_original_aspect_ratio=decrease,pad=${W}:${H}:(ow-iw)/2:(oh-ih)/2,setsar=1,fps=${FPS},format=yuv420p"

echo "== Building segments from data/edl.csv =="
n=0
while IFS=, read -r index clip_key in_point duration rest; do
  [ "$index" = "index" ] && continue          # header
  [ -z "${index// }" ] && continue            # blank line
  src="clips/${clip_key}.mp4"
  if [ ! -s "$src" ]; then
    echo "  !! missing $src — skipping cut $index ($clip_key)"; continue
  fi
  out=$(printf "%s/seg_%03d.mp4" "$BUILD" "$n")
  # -ss before -i = fast seek to the in-point; -t = how long to take from there.
  ffmpeg -nostdin -y -loglevel error -ss "$in_point" -i "$src" -t "$duration" \
    -vf "$VF" -an -c:v libx264 -preset medium -crf 18 -video_track_timescale 12800 "$out"
  echo "file '$(basename "$out")'" >> "$BUILD/concat.txt"
  printf "  cut %02d  %-4s  in=%s  dur=%s\n" "$index" "$clip_key" "$in_point" "$duration"
  n=$((n+1))
done < data/edl.csv

[ "$n" -gt 0 ] || { echo "No segments built — is data/edl.csv populated?"; exit 1; }

echo "== Concatenating $n segments =="
( cd "$BUILD" && ffmpeg -nostdin -y -loglevel error -f concat -safe 0 -i concat.txt -c copy video_silent.mp4 )

if [ -s song.wav ]; then
  echo "== Muxing song.wav (cap ${TOTAL}s) =="
  ffmpeg -nostdin -y -loglevel error -i "$BUILD/video_silent.mp4" -i song.wav \
    -map 0:v:0 -map 1:a:0 -c:v copy -c:a aac -b:a 320k -t "$TOTAL" \
    when_it_rains_roughcut.mp4
  echo "Wrote when_it_rains_roughcut.mp4 (with song)."
else
  echo "== No song.wav found — writing silent cut =="
  cp "$BUILD/video_silent.mp4" when_it_rains_roughcut.mp4
  echo "Wrote when_it_rains_roughcut.mp4 (SILENT). Add song.wav and re-run to lay the track."
fi

dur=$(ffprobe -v error -show_entries format=duration -of default=nk=1:nw=1 when_it_rains_roughcut.mp4 2>/dev/null || echo "?")
echo "Final duration: ${dur}s (target ${TOTAL}s = 4:36)"
