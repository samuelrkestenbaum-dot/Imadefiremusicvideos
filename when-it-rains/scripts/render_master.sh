#!/usr/bin/env bash
# render_master.sh — ONE command to produce the real "When It Rains" master video.
#
#   fetch the assets  ->  assemble per data/edl.csv + song  ->  verify the result.
#
# Wraps scripts/fetch_assets.sh + scripts/assemble_rough_cut.sh and adds a network
# preflight, an ffmpeg fallback, and an output check so you get a clear PASS/FAIL.
#
# Usage:
#   bash scripts/render_master.sh
#
# Requirements:
#   - Outbound HTTPS to the Higgsfield CDN (the clip/still URLs in data/*.csv).
#       NOTE: a managed/sandboxed Claude session BLOCKS that CDN by org egress
#       policy (you'll see "CDN unreachable" below). Run this on a normal
#       machine, OR have the CDN host allowlisted for the session.
#   - ffmpeg (system install preferred). If ffmpeg isn't on PATH, this script
#       falls back to Python's imageio-ffmpeg bundled binary when available.
#   - The song present as song.wav|mp3|m4a|flac in the project root (song.mp3 ok).
#
# Output: when_it_rains_roughcut.mp4  (1280x720, 24fps, song on top, ~274s / 4:34)
set -euo pipefail
cd "$(dirname "$0")/.."                       # -> when-it-rains/ project root

TOTAL=274                                     # target master length (4:34), matches assemble_rough_cut.sh
OUT="when_it_rains_roughcut.mp4"
say() { printf '%s\n' "$*"; }
rule() { printf '%s\n' "------------------------------------------------------------"; }

# --- ffmpeg / ffprobe resolution -------------------------------------------------
# Prefer a real system ffmpeg. If missing, shim in imageio-ffmpeg's bundled binary
# so this can also run inside a Claude session (which ships that static build).
if ! command -v ffmpeg >/dev/null 2>&1; then
  BUNDLED="$(python3 - <<'PY' 2>/dev/null || true
import imageio_ffmpeg
print(imageio_ffmpeg.get_ffmpeg_exe())
PY
)"
  if [ -n "${BUNDLED:-}" ] && [ -x "$BUNDLED" ]; then
    SHIM="$(mktemp -d)"; ln -sf "$BUNDLED" "$SHIM/ffmpeg"
    export PATH="$SHIM:$PATH"
    say "note: no system ffmpeg; using bundled imageio-ffmpeg at $BUNDLED"
  else
    say "ERROR: ffmpeg not found and no bundled fallback. Install ffmpeg."; exit 1
  fi
fi
# ffprobe is optional — the bundled static build ships ffmpeg only. get_dur() copes.
HAVE_FFPROBE=0; command -v ffprobe >/dev/null 2>&1 && HAVE_FFPROBE=1

get_dur() { # echo duration in seconds of $1, or "?" if undeterminable
  if [ "$HAVE_FFPROBE" = 1 ]; then
    ffprobe -v error -show_entries format=duration -of default=nk=1:nw=1 "$1" 2>/dev/null || echo "?"
  else
    # parse "Duration: HH:MM:SS.ss" out of ffmpeg -i stderr
    ffmpeg -hide_banner -i "$1" 2>&1 | awk -F'[:,]' '/Duration:/{printf "%.2f\n",($2*3600)+($3*60)+$4; exit}'
  fi
}
has_stream() { # $1=file  $2=Video|Audio  -> return 0 if that stream type is present
  # NB: `ffmpeg -i` always exits non-zero (no output file), which under
  # `set -o pipefail` would poison a piped grep — so capture first, then match.
  local t info
  if [ "$HAVE_FFPROBE" = 1 ]; then
    t=$(printf '%s' "$2" | tr '[:upper:]' '[:lower:]')   # Video->video / Audio->audio
    info=$(ffprobe -v error -show_entries stream=codec_type -of csv=p=0 "$1" 2>/dev/null || true)
    printf '%s\n' "$info" | grep -qi "^${t}\$"
  else
    info=$(ffmpeg -hide_banner -i "$1" 2>&1 || true)
    printf '%s\n' "$info" | grep -q "Stream.*$2"
  fi
}

# --- 1. preflight ---------------------------------------------------------------
rule; say "render_master: preflight"; rule
[ -s data/edl.csv ]    || { say "ERROR: data/edl.csv missing."; exit 1; }
[ -s data/clips.csv ]  || { say "ERROR: data/clips.csv missing."; exit 1; }

# Offline data check: proves every cut resolves to a real clip URL and the edit is
# on-target BEFORE we download anything. Critical failures abort here.
if [ -f scripts/preflight_edl.py ] && command -v python3 >/dev/null 2>&1; then
  python3 scripts/preflight_edl.py || { say "ERROR: preflight_edl found critical issues; fix data/*.csv first."; exit 1; }
fi

SONG=""; for c in song.wav song.mp3 song.m4a song.flac; do [ -s "$c" ] && { SONG="$c"; break; }; done
if [ -z "$SONG" ]; then
  say "WARN: no song.(wav|mp3|m4a|flac) in project root — master will be SILENT."
else
  say "song: $SONG"
fi

# CDN reachability check against the first real clip URL (column 5 of clips.csv).
CDN_URL="$(awk -F, 'NR==2{print $5}' data/clips.csv)"
if [ -n "${CDN_URL:-}" ] && command -v curl >/dev/null 2>&1; then
  say "checking CDN reachability: ${CDN_URL%%\?*}"
  code="$(curl -sS -o /dev/null -m 25 -w '%{http_code}' --range 0-0 "$CDN_URL" 2>/dev/null || true)"
  [ -z "$code" ] && code=000
  if [ "$code" = "200" ] || [ "$code" = "206" ]; then
    say "CDN reachable (HTTP $code). Proceeding."
  else
    rule
    say "CDN UNREACHABLE (HTTP $code) — cannot download the source clips here."
    say "This is expected inside a managed Claude session: the Higgsfield CDN is"
    say "blocked by org egress policy. Two fixes:"
    say "  1) run this script on a normal machine with internet, or"
    say "  2) have the CDN host allowlisted for the session, then re-run."
    say "Nothing was written. Aborting before partial work."
    rule
    exit 2
  fi
fi

# --- 2. fetch -------------------------------------------------------------------
rule; say "render_master: fetch assets"; rule
bash scripts/fetch_assets.sh

# --- 3. assemble ----------------------------------------------------------------
rule; say "render_master: assemble"; rule
bash scripts/assemble_rough_cut.sh

# --- 4. verify ------------------------------------------------------------------
rule; say "render_master: verify"; rule
[ -s "$OUT" ] || { say "FAIL: $OUT was not produced."; exit 1; }
dur="$(get_dur "$OUT")"
vid=FAIL; aud=FAIL
has_stream "$OUT" "Video" && vid=ok
has_stream "$OUT" "Audio" && aud=ok
size=$(wc -c < "$OUT")

say "output : $OUT"
say "size   : $size bytes"
say "video  : $vid"
say "audio  : $aud  (expected ok when a song is present)"
say "length : ${dur}s  (target ~${TOTAL}s = 4:34)"

ok=1
[ "$vid" = ok ] || ok=0
if [ -n "$SONG" ] && [ "$aud" != ok ]; then ok=0; fi
# duration within +/-3s of target (when ffprobe/parse succeeded)
if [ "$dur" != "?" ]; then
  awk -v d="$dur" -v t="$TOTAL" 'BEGIN{exit !(d>=t-3 && d<=t+3)}' || ok=0
fi

rule
if [ "$ok" = 1 ]; then
  say "PASS — master rendered: $OUT"
else
  say "CHECK — master written but a check did not pass (see above)."
  exit 1
fi
rule
