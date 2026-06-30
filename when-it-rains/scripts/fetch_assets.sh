#!/usr/bin/env bash
# Download every generated "When It Rains" asset from Higgsfield's CDN.
# RUN THIS ON YOUR OWN MACHINE — this repo's cloud session blocks the CDN hosts.
#
# Usage:  bash scripts/fetch_assets.sh
# Result: clips/<KEY>.mp4   (36 animated clips)
#         stills/<ID>.png   (52 source stills)
#
# Re-running skips files already downloaded.
set -euo pipefail
cd "$(dirname "$0")/.."

mkdir -p clips stills
need() { command -v "$1" >/dev/null 2>&1 || { echo "ERROR: '$1' not found"; exit 1; }; }
need curl

dl() { # url dest
  if [ -s "$2" ]; then echo "  skip $(basename "$2")"; return; fi
  echo "  get  $(basename "$2")"
  curl -fSL --retry 4 --retry-delay 2 -o "$2" "$1"
}

echo "== Clips =="
tail -n +2 data/clips.csv | while IFS=, read -r key job src section url motion; do
  [ -z "$key" ] && continue
  dl "$url" "clips/${key}.mp4"
done

echo "== Stills =="
tail -n +2 data/stills.csv | while IFS=, read -r id url rest; do
  [ -z "$id" ] && continue
  dl "$url" "stills/${id}.png"
done

echo "Done. $(ls clips/*.mp4 2>/dev/null | wc -l) clips, $(ls stills/*.png 2>/dev/null | wc -l) stills."
