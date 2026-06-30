#!/usr/bin/env python3
"""build_preview.py — deterministic, re-runnable browser EDL preview generator.

Packet P-011. Reads the playback-order EDL and the clip registry, joins each
EDL cut's ``clip_key`` to its CDN ``mp4_url``, and emits a SINGLE self-contained
``preview.html`` (inline CSS/JS, no external libraries, no ``<script src>``).

WHAT THIS IS (and is NOT)
-------------------------
This is a SILENT visual preview generator for the rough cut. The browser page it
emits plays the 86 cuts back-to-back in EDL order as a ``<video>`` playlist so a
human can eyeball pacing and per-cut content and mark PASS/FAIL. It is NOT the
real render: there is no audio (the song MP3 is not on the CDN) and browser seek
is not frame-accurate, so timing is APPROXIMATE. The real, beat-synced render is
``scripts/fetch_assets.sh`` then ``scripts/assemble_rough_cut.sh`` on the Mac.

DETERMINISM
-----------
Same inputs -> byte-identical ``preview.html``. No timestamps, no randomness, no
dict-iteration-order surprises: the cut array is emitted strictly in EDL row
order and JSON is serialised with a fixed key order and separators.

SOURCE OF TRUTH
---------------
``data/edl.csv``   : index,clip_key,in_point,duration,section,note (play order).
``data/clips.csv`` : clip_key,job_id,source_still,section,mp4_url,motion.
Both are read READ-ONLY. ``mp4_url`` and ``note`` are copied VERBATIM into the
emitted JS data. The only file written is ``preview.html``.

SELF-TEST (exit non-zero on any breach)
---------------------------------------
  * every EDL clip_key resolves to a clips.csv mp4_url (no unresolved),
  * exactly 86 cuts,
  * total duration == 274.0 (within 1e-6),
  * cumulative starts are monotonic and the last cut ends at 274.0,
  * the emitted HTML carries no external ``<script src>`` / stylesheet ``link``.

Touches ONLY: preview.html.
"""
from __future__ import annotations

import csv
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
DATA = os.path.join(ROOT, "data")

EDL = os.path.join(DATA, "edl.csv")
CLIPS = os.path.join(DATA, "clips.csv")
OUT_HTML = os.path.join(ROOT, "preview.html")

EXPECTED_CUTS = 86
TOTAL_RUNTIME = 274.0
EPS = 1e-6

# Band-coverage cuts inserted in P-007 (highlight these in the review UI).
NEW_KEYS = {"C25", "C26", "C27", "C28", "C29", "C30", "C31", "C32", "C33", "C34"}
# On-model singer shots within the new band coverage (badge these).
ONMODEL_KEYS = {"C27", "C33"}


def read_clips(path):
    """Return {clip_key: row_dict} from clips.csv (verbatim field values)."""
    with open(path, newline="") as fh:
        reader = csv.DictReader(fh)
        expected = ["clip_key", "job_id", "source_still", "section", "mp4_url", "motion"]
        assert reader.fieldnames == expected, (
            "clips.csv header mismatch: %r" % (reader.fieldnames,))
        return {row["clip_key"]: row for row in reader}


def read_edl(path):
    """Return the EDL rows as a list of dicts, in file (playback) order."""
    with open(path, newline="") as fh:
        reader = csv.DictReader(fh)
        expected = ["index", "clip_key", "in_point", "duration", "section", "note"]
        assert reader.fieldnames == expected, (
            "edl.csv header mismatch: %r" % (reader.fieldnames,))
        return list(reader)


def build_cuts(edl_rows, clips):
    """Join EDL rows to clip mp4_urls; return (cuts, unresolved).

    Each cut is an ordered dict with a FIXED key order so the emitted JSON is
    deterministic. ``cum_start`` is the back-to-back timeline start of the cut.
    ``mp4_url`` and ``note`` are copied verbatim from the source CSVs.
    """
    cuts = []
    unresolved = []
    cum = 0.0
    for n, row in enumerate(edl_rows, start=1):
        key = row["clip_key"]
        clip = clips.get(key)
        if clip is None:
            unresolved.append(key)
            mp4_url = ""
        else:
            mp4_url = clip["mp4_url"]  # verbatim
        in_point = float(row["in_point"])
        duration = float(row["duration"])
        cut = {
            "i": n,
            "clip_key": key,
            "mp4_url": mp4_url,
            "in_point": in_point,
            "duration": duration,
            "section": row["section"],
            "note": row["note"],  # verbatim
            "cum_start": round(cum, 4),
            "is_new": key in NEW_KEYS,
            "is_onmodel": key in ONMODEL_KEYS,
        }
        cuts.append(cut)
        cum += duration
    return cuts, unresolved, round(cum, 6)


# Fixed key order for deterministic JSON emission.
_CUT_KEYS = ["i", "clip_key", "mp4_url", "in_point", "duration",
             "section", "note", "cum_start", "is_new", "is_onmodel"]


def cuts_to_json(cuts):
    """Serialise cuts to a deterministic, pretty-but-stable JSON array string."""
    ordered = []
    for c in cuts:
        ordered.append({k: c[k] for k in _CUT_KEYS})
    # sort_keys=False because each dict is already in _CUT_KEYS order; fixed
    # separators keep the bytes stable across runs/platforms.
    return json.dumps(ordered, ensure_ascii=False, indent=2,
                      separators=(",", ": "))


HTML_TEMPLATE = """<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>When It Rains — silent rough-cut preview (86 cuts)</title>
<style>
:root {
  --bg: #0d0f13; --panel: #161a21; --panel2: #1d222b; --ink: #e8ecf1;
  --muted: #97a1b0; --line: #2a313c; --accent: #5aa9ff; --new: #ffb454;
  --onmodel: #ff5d9e; --pass: #3ddc84; --fail: #ff5a5a;
}
* { box-sizing: border-box; }
body {
  margin: 0; background: var(--bg); color: var(--ink);
  font: 14px/1.45 -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif;
}
.banner {
  background: #2a1c00; color: #ffe7bd; border-bottom: 1px solid #5a3d00;
  padding: 10px 16px; font-size: 13px;
}
.banner b { color: #ffd27a; }
.banner code { background: #00000040; padding: 1px 5px; border-radius: 4px; }
.wrap { display: flex; gap: 16px; align-items: flex-start; padding: 16px; flex-wrap: wrap; }
.left { flex: 1 1 520px; min-width: 360px; }
.right { flex: 1 1 380px; min-width: 320px; max-height: 86vh; overflow: auto; }
.stage { position: relative; background: #000; border: 1px solid var(--line); border-radius: 10px; overflow: hidden; }
video { width: 100%; display: block; background: #000; aspect-ratio: 16/9; }
.overlay {
  position: absolute; left: 0; right: 0; bottom: 0;
  background: linear-gradient(transparent, #000000d0);
  padding: 14px 14px 12px; pointer-events: none;
}
.ov-row1 { display: flex; gap: 10px; align-items: baseline; flex-wrap: wrap; }
.ov-n { font-weight: 700; font-size: 18px; }
.ov-tc { font-variant-numeric: tabular-nums; color: var(--accent); font-weight: 600; }
.ov-sec { color: var(--muted); text-transform: uppercase; letter-spacing: .08em; font-size: 12px; }
.ov-clip { color: var(--ink); font-weight: 600; }
.ov-note { margin-top: 4px; color: #d7deea; }
.badges { margin-top: 6px; display: flex; gap: 6px; flex-wrap: wrap; }
.badge { font-size: 11px; padding: 2px 8px; border-radius: 999px; font-weight: 700; }
.badge-new { background: var(--new); color: #2a1c00; }
.badge-onmodel { background: var(--onmodel); color: #2a0014; }
.badge-fail { background: #3a0000; color: #ffd0d0; border: 1px solid #6a0000; }
.controls { display: flex; gap: 8px; align-items: center; margin-top: 12px; flex-wrap: wrap; }
button {
  background: var(--panel2); color: var(--ink); border: 1px solid var(--line);
  border-radius: 8px; padding: 8px 12px; cursor: pointer; font-size: 13px;
}
button:hover { border-color: var(--accent); }
button.primary { background: var(--accent); color: #04203f; border-color: var(--accent); font-weight: 700; }
button.pass { background: #103a22; border-color: var(--pass); color: var(--pass); }
button.pass.on { background: var(--pass); color: #04230f; }
button.fail { background: #3a1010; border-color: var(--fail); color: var(--fail); }
button.fail.on { background: var(--fail); color: #2a0000; }
.meta { margin-top: 10px; color: var(--muted); font-size: 12px; }
.review-line { display: flex; gap: 8px; align-items: center; margin-top: 12px; flex-wrap: wrap; }
.review-line input[type=text] {
  flex: 1 1 240px; min-width: 180px; background: var(--panel); color: var(--ink);
  border: 1px solid var(--line); border-radius: 8px; padding: 8px 10px; font: inherit;
}
.right h2 { margin: 0 0 10px; font-size: 14px; color: var(--muted); text-transform: uppercase; letter-spacing: .08em; }
.list { width: 100%; border-collapse: collapse; }
.list td { border-bottom: 1px solid var(--line); padding: 6px 6px; vertical-align: top; }
.list tr { cursor: pointer; }
.list tr:hover td { background: #1a1f28; }
.list tr.cur td { background: #112033; }
.list tr.cur td:first-child { box-shadow: inset 3px 0 0 var(--accent); }
.li-idx { color: var(--muted); font-variant-numeric: tabular-nums; white-space: nowrap; }
.li-tc { color: var(--accent); font-variant-numeric: tabular-nums; white-space: nowrap; }
.li-sec { color: var(--muted); text-transform: uppercase; font-size: 11px; }
.li-clip { font-weight: 600; white-space: nowrap; }
.li-note { color: #cfd6e2; }
.li-mark { white-space: nowrap; font-weight: 700; }
.li-mark.PASS { color: var(--pass); }
.li-mark.FAIL { color: var(--fail); }
tr.row-new td { background: #211803; }
tr.row-new.cur td { background: #2a2207; }
.dot { display: inline-block; width: 8px; height: 8px; border-radius: 50%; margin-right: 4px; }
.dot-new { background: var(--new); }
.dot-onmodel { background: var(--onmodel); }
.export {
  width: 100%; height: 160px; margin-top: 10px; background: var(--panel); color: var(--ink);
  border: 1px solid var(--line); border-radius: 8px; padding: 10px; font: 12px/1.4 ui-monospace, Menlo, Consolas, monospace;
}
.legend { color: var(--muted); font-size: 12px; margin: 4px 0 10px; }
.fail-note { color: var(--fail); }
</style>
</head>
<body>
<div class="banner">
  <b>SILENT visual preview.</b> No audio — the song MP3 is not on the CDN.
  Timing is <b>approximate</b> (browser seek is not frame-accurate). This is a
  pacing / content check only. The real, audio + beat-synced render is
  <code>scripts/fetch_assets.sh</code> then <code>scripts/assemble_rough_cut.sh</code>
  on your Mac. Clips stream from the Higgsfield CloudFront CDN, so this needs
  <b>internet</b> and a browser that can reach CloudFront. If a clip fails to
  load, its metadata still shows and the playlist auto-advances.
</div>

<div class="wrap">
  <div class="left">
    <div class="stage">
      <video id="vid" playsinline preload="auto"></video>
      <div class="overlay">
        <div class="ov-row1">
          <span class="ov-n" id="ovN">--/86</span>
          <span class="ov-tc" id="ovTc">0:00</span>
          <span class="ov-sec" id="ovSec">--</span>
          <span class="ov-clip" id="ovClip">--</span>
        </div>
        <div class="ov-note" id="ovNote"></div>
        <div class="badges" id="ovBadges"></div>
      </div>
    </div>

    <div class="controls">
      <button id="btnPlay" class="primary">Play</button>
      <button id="btnPrev">&#8592; Prev</button>
      <button id="btnNext">Next &#8594;</button>
      <span class="meta" id="status"></span>
    </div>

    <div class="review-line">
      <button id="btnPass" class="pass">PASS</button>
      <button id="btnFail" class="fail">FAIL</button>
      <input id="reviewNote" type="text" placeholder="note for this cut (optional)">
    </div>
    <div class="meta">
      Marks persist in this browser (localStorage). Use <b>Copy results</b> to
      export every marked cut as text you can paste back.
    </div>
    <div class="controls">
      <button id="btnCopy">Copy results</button>
      <button id="btnClear">Clear marks</button>
    </div>
    <textarea id="export" class="export" readonly placeholder="Marked cuts appear here after you Copy results."></textarea>
  </div>

  <div class="right">
    <h2>All __CUTCOUNT__ cuts (click to jump)</h2>
    <div class="legend">
      <span class="dot dot-new"></span>new band coverage (C25&#8211;C34)
      &nbsp;&nbsp;<span class="dot dot-onmodel"></span>on-model singer shot (C27 / C33)
    </div>
    <table class="list"><tbody id="cutList"></tbody></table>
  </div>
</div>

<script>
"use strict";
// ---- Embedded EDL data (generated by build_preview.py, do not hand-edit) ----
var CUTS = __CUTS_JSON__;

// ---- State ----
var idx = 0;            // current cut index (0-based)
var playing = false;
var advanceTimer = null;
var marks = {};         // { cutIndex: {verdict:"PASS"|"FAIL", note:"..."} }
var STORE_KEY = "wir_preview_marks_v1";

var vid = document.getElementById("vid");

function mmss(t) {
  t = Math.max(0, Math.floor(t));
  var m = Math.floor(t / 60), s = t % 60;
  return m + ":" + (s < 10 ? "0" : "") + s;
}

function loadMarks() {
  try {
    var raw = localStorage.getItem(STORE_KEY);
    if (raw) marks = JSON.parse(raw) || {};
  } catch (e) { marks = {}; }
}
function saveMarks() {
  try { localStorage.setItem(STORE_KEY, JSON.stringify(marks)); } catch (e) {}
}

// ---- Build the click-to-jump list once ----
var listBody = document.getElementById("cutList");
function buildList() {
  var html = "";
  for (var k = 0; k < CUTS.length; k++) {
    var c = CUTS[k];
    var rowCls = c.is_new ? "row-new" : "";
    var marker = "";
    if (c.is_new) marker += '<span class="dot dot-new"></span>';
    if (c.is_onmodel) marker += '<span class="dot dot-onmodel"></span>';
    html += '<tr data-k="' + k + '" class="' + rowCls + '">'
      + '<td class="li-idx">' + c.i + '</td>'
      + '<td class="li-tc">' + mmss(c.cum_start) + '</td>'
      + '<td class="li-sec">' + c.section + '</td>'
      + '<td class="li-clip">' + marker + esc(c.clip_key) + '</td>'
      + '<td class="li-note">' + esc(c.note) + '</td>'
      + '<td class="li-mark" id="mark-' + k + '"></td>'
      + '</tr>';
  }
  listBody.innerHTML = html;
  var rows = listBody.querySelectorAll("tr");
  for (var r = 0; r < rows.length; r++) {
    rows[r].addEventListener("click", (function (kk) {
      return function () { goto(kk, true); };
    })(parseInt(rows[r].getAttribute("data-k"), 10)));
  }
}

function esc(s) {
  return String(s).replace(/&/g, "&amp;").replace(/</g, "&lt;")
    .replace(/>/g, "&gt;").replace(/"/g, "&quot;");
}

function refreshMarkCells() {
  for (var k = 0; k < CUTS.length; k++) {
    var cell = document.getElementById("mark-" + k);
    if (!cell) continue;
    var m = marks[k];
    if (m && m.verdict) {
      cell.textContent = m.verdict;
      cell.className = "li-mark " + m.verdict;
    } else {
      cell.textContent = "";
      cell.className = "li-mark";
    }
  }
}

// ---- Overlay + current-row highlight ----
function renderOverlay() {
  var c = CUTS[idx];
  document.getElementById("ovN").textContent = c.i + "/" + CUTS.length;
  document.getElementById("ovTc").textContent = mmss(c.cum_start);
  document.getElementById("ovSec").textContent = c.section;
  document.getElementById("ovClip").textContent = c.clip_key;
  document.getElementById("ovNote").textContent = c.note;
  var b = "";
  if (c.is_new) b += '<span class="badge badge-new">new band coverage</span>';
  if (c.is_onmodel) b += '<span class="badge badge-onmodel">on-model singer shot</span>';
  if (failedClip) b += '<span class="badge badge-fail">clip failed to load</span>';
  document.getElementById("ovBadges").innerHTML = b;

  var rows = listBody.querySelectorAll("tr");
  for (var r = 0; r < rows.length; r++) rows[r].classList.remove("cur");
  if (rows[idx]) {
    rows[idx].classList.add("cur");
    rows[idx].scrollIntoView({ block: "nearest" });
  }
  // reflect this cut's existing mark in the review controls
  var m = marks[idx] || {};
  document.getElementById("btnPass").classList.toggle("on", m.verdict === "PASS");
  document.getElementById("btnFail").classList.toggle("on", m.verdict === "FAIL");
  document.getElementById("reviewNote").value = m.note || "";
}

function setStatus(msg) { document.getElementById("status").textContent = msg; }

// ---- Playback engine ----
var failedClip = false;

function clearAdvance() {
  if (advanceTimer !== null) { clearTimeout(advanceTimer); advanceTimer = null; }
}

function scheduleAdvance(seconds) {
  clearAdvance();
  advanceTimer = setTimeout(function () {
    advanceTimer = null;
    next(true);
  }, Math.max(0, seconds) * 1000);
}

function loadCut(autoplay) {
  var c = CUTS[idx];
  failedClip = false;
  renderOverlay();
  clearAdvance();

  if (!c.mp4_url) { onClipFailed(); return; }

  // Only reset src when the URL actually changes (handles same-URL-consecutive).
  var sameSrc = vid.getAttribute("data-src") === c.mp4_url;
  if (!sameSrc) {
    vid.setAttribute("data-src", c.mp4_url);
    vid.src = c.mp4_url;
    vid.load();
  } else {
    // same clip back-to-back: just seek again
    seekAndPlay(autoplay);
  }
  if (autoplay) playing = true;
}

function seekAndPlay(autoplay) {
  var c = CUTS[idx];
  try {
    if (isFinite(c.in_point)) vid.currentTime = c.in_point;
  } catch (e) {}
  if (autoplay && playing) {
    var p = vid.play();
    if (p && p.catch) p.catch(function () { /* autoplay blocked; user can press Play */ });
  }
  if (playing) scheduleAdvance(c.duration);
  setStatus(playing ? "playing" : "paused");
}

function onClipFailed() {
  failedClip = true;
  renderOverlay();
  setStatus("clip failed to load — showing metadata, auto-advancing");
  if (playing) scheduleAdvance(CUTS[idx].duration);
}

vid.addEventListener("loadedmetadata", function () { seekAndPlay(true); });
vid.addEventListener("error", function () { onClipFailed(); });
// Guard: if a same-URL seek fires timeupdate past the window, advance.
vid.addEventListener("timeupdate", function () {
  if (!playing) return;
  var c = CUTS[idx];
  if (advanceTimer === null) return; // already advancing / failed
  if (vid.currentTime >= c.in_point + c.duration - 0.02) {
    next(true);
  }
});

function goto(k, autoplay) {
  if (k < 0) k = 0;
  if (k >= CUTS.length) { stopAtEnd(); return; }
  idx = k;
  loadCut(autoplay);
}

function next(autoplay) {
  if (idx + 1 >= CUTS.length) { stopAtEnd(); return; }
  goto(idx + 1, autoplay);
}
function prev() { goto(Math.max(0, idx - 1), playing); }

function stopAtEnd() {
  playing = false;
  clearAdvance();
  try { vid.pause(); } catch (e) {}
  setStatus("end of cut list (" + CUTS.length + " cuts, " + mmss(CUTS[CUTS.length - 1].cum_start + CUTS[CUTS.length - 1].duration) + ")");
  document.getElementById("btnPlay").textContent = "Replay";
}

function togglePlay() {
  if (playing) {
    playing = false;
    clearAdvance();
    try { vid.pause(); } catch (e) {}
    document.getElementById("btnPlay").textContent = "Play";
    setStatus("paused");
  } else {
    if (idx >= CUTS.length - 1 &&
        document.getElementById("btnPlay").textContent === "Replay") {
      idx = 0;
    }
    playing = true;
    document.getElementById("btnPlay").textContent = "Pause";
    loadCut(true);
  }
}

// ---- Review marks ----
function setVerdict(v) {
  var existing = marks[idx] || {};
  if (existing.verdict === v) {
    delete existing.verdict;           // toggle off
  } else {
    existing.verdict = v;
  }
  existing.note = document.getElementById("reviewNote").value;
  if (!existing.verdict && !existing.note) delete marks[idx];
  else marks[idx] = existing;
  saveMarks();
  refreshMarkCells();
  renderOverlay();
}

document.getElementById("reviewNote").addEventListener("input", function () {
  var existing = marks[idx] || {};
  existing.note = this.value;
  if (!existing.verdict && !existing.note) delete marks[idx];
  else marks[idx] = existing;
  saveMarks();
});

function buildExport() {
  var lines = [];
  lines.push("When It Rains — silent preview review");
  lines.push("cuts: " + CUTS.length + " | runtime(EDL): " +
             mmss(CUTS[CUTS.length - 1].cum_start + CUTS[CUTS.length - 1].duration) +
             " (" + (CUTS[CUTS.length - 1].cum_start + CUTS[CUTS.length - 1].duration).toFixed(1) + "s)");
  lines.push("note: SILENT preview, timing approximate (browser seek).");
  lines.push("");
  var any = false;
  for (var k = 0; k < CUTS.length; k++) {
    var m = marks[k];
    if (!m || (!m.verdict && !m.note)) continue;
    any = true;
    var c = CUTS[k];
    var flags = [];
    if (c.is_new) flags.push("new");
    if (c.is_onmodel) flags.push("on-model");
    var flagStr = flags.length ? " [" + flags.join(",") + "]" : "";
    lines.push("#" + c.i + "  " + mmss(c.cum_start) + "  " + c.section + "  " +
               c.clip_key + flagStr + "  " + (m.verdict || "(noted)") +
               (m.note ? " — " + m.note : ""));
  }
  if (!any) lines.push("(no cuts marked yet)");
  return lines.join("\n");
}

document.getElementById("btnCopy").addEventListener("click", function () {
  var text = buildExport();
  var ta = document.getElementById("export");
  ta.value = text;
  ta.select();
  try {
    if (navigator.clipboard && navigator.clipboard.writeText) {
      navigator.clipboard.writeText(text);
    } else {
      document.execCommand("copy");
    }
    setStatus("results copied to clipboard");
  } catch (e) {
    setStatus("results shown below — select and copy");
  }
});

document.getElementById("btnClear").addEventListener("click", function () {
  if (!confirm("Clear all PASS/FAIL marks and notes?")) return;
  marks = {};
  saveMarks();
  refreshMarkCells();
  renderOverlay();
  document.getElementById("export").value = "";
});

// ---- Wire controls ----
document.getElementById("btnPlay").addEventListener("click", togglePlay);
document.getElementById("btnPrev").addEventListener("click", prev);
document.getElementById("btnNext").addEventListener("click", function () { next(playing); });
document.getElementById("btnPass").addEventListener("click", function () { setVerdict("PASS"); });
document.getElementById("btnFail").addEventListener("click", function () { setVerdict("FAIL"); });

document.addEventListener("keydown", function (e) {
  if (e.target && (e.target.tagName === "INPUT" || e.target.tagName === "TEXTAREA")) return;
  if (e.key === " ") { e.preventDefault(); togglePlay(); }
  else if (e.key === "ArrowRight") { next(playing); }
  else if (e.key === "ArrowLeft") { prev(); }
  else if (e.key.toLowerCase() === "p") { setVerdict("PASS"); }
  else if (e.key.toLowerCase() === "f") { setVerdict("FAIL"); }
});

// ---- Boot ----
loadMarks();
buildList();
refreshMarkCells();
goto(0, false);          // load first cut paused; show its frame + metadata
setStatus("ready — press Play (needs internet to reach the CDN)");
</script>
</body>
</html>
"""


def render_html(cuts):
    cuts_json = cuts_to_json(cuts)
    html = HTML_TEMPLATE
    html = html.replace("__CUTCOUNT__", str(len(cuts)))
    html = html.replace("__CUTS_JSON__", cuts_json)
    return html


def self_test(cuts, unresolved, total, html):
    errs = []

    # 1. No unresolved clip_keys.
    if unresolved:
        errs.append("unresolved clip_keys: %r" % (sorted(set(unresolved)),))

    # 2. Exactly 86 cuts.
    if len(cuts) != EXPECTED_CUTS:
        errs.append("cut count %d != %d" % (len(cuts), EXPECTED_CUTS))

    # 3. Total runtime == 274.0 within tolerance.
    if abs(total - TOTAL_RUNTIME) > EPS:
        errs.append("total %.9f != %.1f" % (total, TOTAL_RUNTIME))

    # 4. Indices 1..86 contiguous, cumulative starts monotonic, last cut ends
    #    at 274.0.
    cum = 0.0
    for n, c in enumerate(cuts, start=1):
        if c["i"] != n:
            errs.append("cut index %r at position %d" % (c["i"], n))
        if abs(c["cum_start"] - round(cum, 4)) > 1e-3:
            errs.append("cut %d cum_start %r != %r" % (n, c["cum_start"], cum))
        cum += c["duration"]
    if abs(cum - TOTAL_RUNTIME) > EPS:
        errs.append("last cut ends at %.9f != %.1f" % (cum, TOTAL_RUNTIME))

    # 5. Every cut has a non-empty verbatim mp4_url.
    for c in cuts:
        if not c["mp4_url"]:
            errs.append("cut %d (%s) has empty mp4_url" % (c["i"], c["clip_key"]))

    # 6. New / on-model flags land on the expected keys.
    new_flagged = {c["clip_key"] for c in cuts if c["is_new"]}
    if new_flagged != NEW_KEYS:
        errs.append("is_new set %r != %r" % (sorted(new_flagged), sorted(NEW_KEYS)))
    onmodel_flagged = {c["clip_key"] for c in cuts if c["is_onmodel"]}
    if onmodel_flagged != ONMODEL_KEYS:
        errs.append("is_onmodel set %r != %r"
                    % (sorted(onmodel_flagged), sorted(ONMODEL_KEYS)))

    # 7. The emitted HTML is self-contained: no external script/style refs.
    #    We forbid the constructs that *load* an external resource at page load
    #    (a <script src>, a <link>, an @import). We deliberately do NOT forbid
    #    the substring "cdn" or http(s) URLs in general, because the clip
    #    mp4_urls are CloudFront media sources assigned to <video>.src at
    #    runtime — that is the entire purpose of the tool, not a page-load dep.
    lowered = html.lower()
    for needle in ("<script src", "<link ", "<link>", "@import"):
        if needle in lowered:
            errs.append("HTML carries external/forbidden reference: %r" % needle)
    # Belt-and-braces: the only http(s) URLs in the document must be the clip
    # mp4 sources inside the embedded JSON (i.e. as quoted JSON values), never
    # as an HTML resource attribute like src="http..." / href="http...".
    for attr in ("src=\"http", "src='http", "href=\"http", "href='http"):
        if attr in lowered:
            errs.append("HTML loads an external resource via attribute: %r" % attr)

    return errs


def main():
    clips = read_clips(CLIPS)
    edl_rows = read_edl(EDL)
    cuts, unresolved, total = build_cuts(edl_rows, clips)
    html = render_html(cuts)

    errs = self_test(cuts, unresolved, total, html)
    if errs:
        sys.stderr.write("SELF-TEST FAILED:\n")
        for e in errs:
            sys.stderr.write("  - " + e + "\n")
        sys.exit(1)

    with open(OUT_HTML, "w", newline="\n") as fh:
        fh.write(html)

    print("SELF-TEST PASSED")
    print("  cuts:        %d" % len(cuts))
    print("  total:       %.1fs" % total)
    print("  unresolved:  %d" % len(unresolved))
    print("  new (C25-34): %d   on-model (C27/C33): %d"
          % (sum(c["is_new"] for c in cuts), sum(c["is_onmodel"] for c in cuts)))
    print("  wrote:       %s" % OUT_HTML)


if __name__ == "__main__":
    main()
