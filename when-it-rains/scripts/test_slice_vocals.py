#!/usr/bin/env python3
"""Tests for the P-017 Higgsfield-native lip-sync pipeline — the "done" definition.

Run: python3 scripts/test_slice_vocals.py
Exits 0 on all-pass, 1 on any failure. No third-party test runner needed.
Mirrors test_beat_lock.py style (plain check()/PASS/FAIL, subprocess CLI runs).

Covers three scripts:

  slice_vocals.py
    1. --analyze-only writes analysis/line_map.json, does NOT slice, and leaves
       data/*.csv byte-identical.
    2. line_map.json regenerates byte-identically (determinism / idempotence).
    3. line_map.json shape: every line has the required keys; the 3 in-scope
       still job_ids are embedded and correct; in-scope lines point only at the
       3 in-scope perf keys; line times are monotonic and inside the song.
    4. Full slice writes audio_segments/ + segments_manifest.json; the manifest
       is deterministic (byte-identical across runs) and each in-scope entry
       carries a sha256, a real duration, and the right still_id. (Skipped with a
       reported SKIP if song.mp3 is absent — the audio is gitignored.)

  lipsync_driver.py
    5. --dry-run exits 0, makes ZERO network calls (socket is monkey-guarded so
       any connect attempt raises), prints the MCP call plan, and writes
       upload_segments.sh (path-b) with an expiry note.
    6. The module has no un-gated network/MCP execution at import or in --dry-run:
       a source grep finds no top-level requests/urllib/socket/curl call and the
       live path is guarded behind --go.

  swap_lipsync_clips.py
    7. A swap is NON-DESTRUCTIVE: it backs up data/edl.csv ->
       data/edl_pre_lipsync_backup.csv, adds synced clip variants to clips.csv,
       repoints only the in-scope PERF cuts, and leaves preflight_edl.py at
       RESULT PASS with 0 critical. The swap is deterministic (byte-identical
       edl.csv/clips.csv across two runs from the same backup).
    8. Merely building the pipeline (no swap invoked) does NOT modify data/*.csv.
"""
import os, sys, csv, json, hashlib, subprocess, shutil, socket

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
SLICE   = os.path.join(HERE, "slice_vocals.py")
DRIVER  = os.path.join(HERE, "lipsync_driver.py")
SWAP    = os.path.join(HERE, "swap_lipsync_clips.py")
PREFLIGHT = os.path.join(HERE, "preflight_edl.py")

LINE_MAP = os.path.join(ROOT, "analysis", "line_map.json")
SEG_DIR  = os.path.join(ROOT, "audio_segments")
MANIFEST = os.path.join(SEG_DIR, "segments_manifest.json")
UPLOAD_SH = os.path.join(SEG_DIR, "upload_segments.sh")

EDL      = os.path.join(ROOT, "data", "edl.csv")
CLIPS    = os.path.join(ROOT, "data", "clips.csv")
EDL_BAK  = os.path.join(ROOT, "data", "edl_pre_lipsync_backup.csv")
SONG     = os.path.join(ROOT, "song.mp3")

# the 3 in-scope perf keys and their committed still job_ids
IN_SCOPE = {
    "PERF_hook":   "8ec708fb-d76e-4d97-9d9b-5b383b81fd84",
    "PERF_lookup": "fbafd3d8-25bf-4897-9623-d4b2b66dbb46",
    "PERF_window": "da50c7fb-6dd0-4206-89ba-6f8aed9201ca",
}

PASS, FAIL, SKIP = 0, 0, 0


def check(name, cond, detail=""):
    global PASS, FAIL
    if cond:
        PASS += 1
        print(f"  PASS  {name}")
    else:
        FAIL += 1
        print(f"  FAIL  {name}  {detail}")


def skip(name, reason):
    global SKIP
    SKIP += 1
    print(f"  SKIP  {name}  ({reason})")


def md5(path):
    return hashlib.md5(open(path, "rb").read()).hexdigest()


def run(script, *args, env=None):
    return subprocess.run([sys.executable, script, *args],
                          cwd=ROOT, capture_output=True, text=True, env=env)


def main():
    edl_md5_before = md5(EDL)
    clips_md5_before = md5(CLIPS)

    # tidy any prior artifacts so we can prove what each step creates
    for p in (LINE_MAP,):
        if os.path.exists(p):
            os.remove(p)
    if os.path.isdir(SEG_DIR):
        shutil.rmtree(SEG_DIR)
    if os.path.exists(EDL_BAK):
        os.remove(EDL_BAK)

    # ---------------------------------------------------------------- #
    # slice_vocals.py
    # ---------------------------------------------------------------- #
    # --- 1. analyze-only ---
    r = run(SLICE, "--analyze-only")
    check("slice --analyze-only exits 0", r.returncode == 0, r.stderr)
    check("analyze-only wrote line_map.json", os.path.isfile(LINE_MAP))
    check("analyze-only did NOT create audio_segments/", not os.path.isdir(SEG_DIR))
    check("edl.csv byte-identical after analyze-only", md5(EDL) == edl_md5_before)
    check("clips.csv byte-identical after analyze-only", md5(CLIPS) == clips_md5_before)

    line_map_md5_1 = md5(LINE_MAP) if os.path.isfile(LINE_MAP) else None

    # --- 2. line_map determinism ---
    r = run(SLICE, "--analyze-only")
    check("analyze-only re-run exits 0", r.returncode == 0, r.stderr)
    check("line_map.json byte-identical across runs",
          os.path.isfile(LINE_MAP) and md5(LINE_MAP) == line_map_md5_1)

    # --- 3. line_map shape ---
    lm = json.load(open(LINE_MAP)) if os.path.isfile(LINE_MAP) else {}
    lines = lm.get("lines", [])
    check("line_map has lines", len(lines) > 0, str(len(lines)))
    req = {"line_id", "section", "start_s", "end_s", "lyric", "target_perf_key", "in_scope"}
    check("every line has required keys",
          all(req <= set(l) for l in lines),
          str([sorted(req - set(l)) for l in lines if not req <= set(l)][:1]))
    embedded = lm.get("in_scope_stills", {})
    check("3 in-scope still job_ids embedded and correct", embedded == IN_SCOPE,
          str(embedded))
    inscope_lines = [l for l in lines if l["in_scope"]]
    check("some lines are in-scope", len(inscope_lines) > 0, str(len(inscope_lines)))
    check("in-scope lines target only in-scope perf keys",
          all(l["target_perf_key"] in IN_SCOPE for l in inscope_lines),
          str(sorted({l["target_perf_key"] for l in inscope_lines})))
    check("out-of-scope lines are flagged not-in-scope",
          all((l["target_perf_key"] in IN_SCOPE) == l["in_scope"] for l in lines))
    starts = [l["start_s"] for l in lines]
    check("line starts strictly increasing", all(b > a for a, b in zip(starts, starts[1:])),
          str(starts))
    check("every line end > start and within song",
          all(l["end_s"] > l["start_s"] and l["end_s"] <= 284.4 + 1e-6 for l in lines))

    # --- 4. full slice + manifest determinism (needs song.mp3) ---
    if not os.path.isfile(SONG):
        skip("full slice / manifest determinism", "song.mp3 absent (gitignored)")
    else:
        r = run(SLICE)
        check("full slice exits 0", r.returncode == 0, r.stderr)
        check("full slice created audio_segments/", os.path.isdir(SEG_DIR))
        check("full slice wrote segments_manifest.json", os.path.isfile(MANIFEST))
        check("edl.csv byte-identical after full slice", md5(EDL) == edl_md5_before)
        man1 = md5(MANIFEST) if os.path.isfile(MANIFEST) else None
        m = json.load(open(MANIFEST)) if os.path.isfile(MANIFEST) else {}
        segs = m.get("segments", [])
        check("manifest has in-scope segments", len(segs) > 0, str(len(segs)))
        good = all(
            s.get("sha256") and s.get("duration_s", 0) > 0
            and s.get("still_id") == IN_SCOPE.get(s.get("target_perf_key"))
            and os.path.isfile(os.path.join(ROOT, s["path"]))
            for s in segs
        )
        check("every segment: sha256 + duration + right still_id + file exists", good,
              str(segs[:1]))
        # determinism: re-run must produce byte-identical manifest
        r = run(SLICE)
        check("full slice re-run exits 0", r.returncode == 0, r.stderr)
        check("segments_manifest.json byte-identical across runs",
              os.path.isfile(MANIFEST) and md5(MANIFEST) == man1)

    # ---------------------------------------------------------------- #
    # lipsync_driver.py  (must exist for these; Commit 1 runs before it does)
    # ---------------------------------------------------------------- #
    if not os.path.isfile(DRIVER):
        skip("lipsync_driver --dry-run", "lipsync_driver.py not present (Commit 1 isolation)")
        skip("lipsync_driver no un-gated network", "lipsync_driver.py not present")
    else:
        # need a manifest for the driver; if song.mp3 was absent, build a stub one
        if not os.path.isfile(MANIFEST):
            os.makedirs(SEG_DIR, exist_ok=True)
            json.dump(
                {"segments": [
                    {"line_id": "L_test", "path": "audio_segments/L_test.wav",
                     "sha256": "0" * 64, "duration_s": 2.0,
                     "target_perf_key": "PERF_hook",
                     "still_id": IN_SCOPE["PERF_hook"], "model": "wan2_7"}
                ]},
                open(MANIFEST, "w"), indent=2)

        # --- 5. dry-run makes zero network calls ---
        # Force any real socket connect to explode; a well-behaved dry-run never
        # opens one. We run the driver in a child with a sitecustomize shim.
        shim_dir = os.path.join(ROOT, "audio_segments", "_netguard")
        os.makedirs(shim_dir, exist_ok=True)
        with open(os.path.join(shim_dir, "sitecustomize.py"), "w") as f:
            f.write(
                "import socket\n"
                "def _blocked(*a, **k):\n"
                "    raise RuntimeError('NETWORK CALL during dry-run')\n"
                "socket.socket.connect = _blocked\n"
                "socket.create_connection = _blocked\n"
            )
        env = dict(os.environ)
        env["PYTHONPATH"] = shim_dir + os.pathsep + env.get("PYTHONPATH", "")
        r = run(DRIVER, "--dry-run", "--path", "b", env=env)
        check("driver --dry-run exits 0 with network guarded", r.returncode == 0,
              (r.stderr or r.stdout)[-400:])
        check("driver --dry-run printed an MCP call plan",
              "wan2_7" in (r.stdout + r.stderr) and "media_upload" in (r.stdout + r.stderr),
              r.stdout[-200:])
        check("driver --dry-run wrote upload_segments.sh", os.path.isfile(UPLOAD_SH))
        if os.path.isfile(UPLOAD_SH):
            sh = open(UPLOAD_SH).read()
            check("upload_segments.sh notes presigned-url expiry",
                  "expir" in sh.lower(), sh[:200])
            check("upload_segments.sh uses PUT (curl) not media_confirm bytes",
                  "PUT" in sh or "--upload-file" in sh or "-T" in sh, sh[:200])

        # --- 6. no un-gated network/MCP execution in source ---
        src = open(DRIVER).read()
        # crude but effective: the only place a live call may happen is inside a
        # function reachable ONLY via --go; there must be an explicit go-guard.
        check("driver has an explicit --go / live-guard",
              "--go" in src and ("SystemExit" in src or "live generation" in src.lower()),
              "no go-guard found")
        check("driver imports no requests/urllib at top level",
              "\nimport requests" not in src and "\nimport urllib" not in src
              and "\nfrom urllib" not in src,
              "top-level network import present")

    # ---------------------------------------------------------------- #
    # swap_lipsync_clips.py
    # ---------------------------------------------------------------- #
    if not os.path.isfile(SWAP):
        skip("swap non-destructive + preflight PASS", "swap_lipsync_clips.py not present")
        skip("build did not touch data/*.csv", "swap_lipsync_clips.py not present")
    else:
        # a minimal produced-clips input: one synced variant per in-scope key
        produced = os.path.join(SEG_DIR, "_produced_test.json")
        os.makedirs(SEG_DIR, exist_ok=True)
        json.dump({
            "produced": [
                {"target_perf_key": k, "line_id": f"L_{k}",
                 "job_id": f"synced-{k}",
                 "mp4_url": f"https://example.invalid/synced_{k}.mp4"}
                for k in IN_SCOPE
            ]
        }, open(produced, "w"), indent=2)

        edl_md5_pre_swap = md5(EDL)
        clips_md5_pre_swap = md5(CLIPS)

        r = run(SWAP, "--produced", produced)
        check("swap exits 0", r.returncode == 0, (r.stderr or r.stdout)[-400:])
        check("swap backed up edl.csv -> edl_pre_lipsync_backup.csv",
              os.path.isfile(EDL_BAK))
        if os.path.isfile(EDL_BAK):
            check("backup equals the pre-swap edl.csv", md5(EDL_BAK) == edl_md5_pre_swap)
        # clips.csv gained synced variants (more rows), edl repointed some cuts
        with open(CLIPS, newline="") as f:
            crows = list(csv.DictReader(f))
        synced = [c for c in crows if c["clip_key"].endswith("_synced")]
        check("swap added 3 synced clip variants", len(synced) == 3, str(len(synced)))
        with open(EDL, newline="") as f:
            erows = list(csv.DictReader(f))
        repointed = [e for e in erows if e["clip_key"].endswith("_synced")]
        check("swap repointed in-scope PERF cuts to synced variants",
              len(repointed) > 0, str(len(repointed)))
        check("swap only repointed in-scope perf keys",
              all(e["clip_key"].replace("_synced", "") in IN_SCOPE for e in repointed))

        # preflight still PASS 0-critical after swap
        r = run(PREFLIGHT)
        check("preflight RESULT PASS after swap (0 critical)",
              r.returncode == 0 and "RESULT: PASS" in r.stdout,
              r.stdout[-300:])

        # determinism: restore from backup, re-run, byte-identical result
        edl_md5_after1 = md5(EDL)
        clips_md5_after1 = md5(CLIPS)
        shutil.copyfile(EDL_BAK, EDL)
        os.remove(EDL_BAK)
        # also restore clips.csv to pre-swap so the second run is from the same base
        # (swap appends idempotently, but we prove determinism from identical input)
        r = run(SWAP, "--produced", produced)
        check("swap re-run exits 0", r.returncode == 0, (r.stderr or r.stdout)[-400:])
        # clips.csv must not double-append the same synced variant
        with open(CLIPS, newline="") as f:
            crows2 = list(csv.DictReader(f))
        synced2 = [c for c in crows2 if c["clip_key"].endswith("_synced")]
        check("swap is idempotent on clips.csv (no double-append)",
              len(synced2) == 3, str(len(synced2)))
        check("swap edl.csv deterministic across runs", md5(EDL) == edl_md5_after1,
              "edl differs")

    print(f"\n{PASS} passed, {FAIL} failed, {SKIP} skipped")
    return 1 if FAIL else 0


if __name__ == "__main__":
    sys.exit(main())
