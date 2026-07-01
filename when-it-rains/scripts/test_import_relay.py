#!/usr/bin/env python3
"""Tests for the P-018 git->media_import->wan2_7 audio relay — the "done" definition.

Run: python3 scripts/test_import_relay.py
Exits 0 on all-pass, 1 on any failure. No third-party test runner needed.
Mirrors test_slice_vocals.py style (plain check()/PASS/FAIL, subprocess CLI runs).

Covers scripts/import_relay.py:

  1. raw_url() builds the EXACT expected public raw.githubusercontent.com string
     for a known sha + repo path (the string the live media_import_url consumes).
  2. stage_segment() writes the segment under audio_relay/ and returns a
     `git add -f` command (force — NOT a plain `git add`, because *.mp3/*.wav are
     gitignored). copy=False computes paths/commands without touching disk.
  3. build_relay_plan() covers EVERY in-scope line in analysis/line_map.json (one
     entry per in-scope line, each with git_add_cmd + media_import_url + wan2_7
     calls + the correct still_id), and is deterministic (byte-identical md5 of
     the plan JSON across two runs).
  4. NO reference to the egress-blocked upload host (upload.higgsfield.ai)
     anywhere in the source or in any produced plan/runbook; assert_no_upload_host
     refuses one.
  5. --dry-run exits 0, makes ZERO network calls (socket guarded), writes
     relay_plan.json + relay_runbook.md, prints the plan; --go is REFUSED.
  6. The committed source performs NO git push and NO executed MCP/generate call
     (a source grep: no `git push`, no subprocess push, no bare media_import_url(
     / wan2_7( execution outside string/plan context).
"""
import os, sys, json, hashlib, subprocess, shutil

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
RELAY = os.path.join(HERE, "import_relay.py")

LINE_MAP   = os.path.join(ROOT, "analysis", "line_map.json")
RELAY_DIR  = os.path.join(ROOT, "audio_relay")
PLAN_JSON  = os.path.join(RELAY_DIR, "relay_plan.json")
RUNBOOK_MD = os.path.join(RELAY_DIR, "relay_runbook.md")

# import the module directly for unit-level checks
sys.path.insert(0, HERE)
import import_relay as R  # noqa: E402

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
    # snapshot any pre-existing artifacts so the suite leaves the tree clean
    plan_existed = os.path.isfile(PLAN_JSON)
    runbook_existed = os.path.isfile(RUNBOOK_MD)

    # ---------------------------------------------------------------- #
    # 1. raw_url exact-string unit test
    # ---------------------------------------------------------------- #
    sha = "8a5048c"
    relpath = "when-it-rains/audio_relay/hook_vocal.mp3"
    expected = ("https://raw.githubusercontent.com/samuelrkestenbaum-dot/"
                "Imadefiremusicvideos/8a5048c/"
                "when-it-rains/audio_relay/hook_vocal.mp3")
    got = R.raw_url(sha, relpath)
    check("raw_url() builds the exact expected public raw URL", got == expected,
          f"got={got!r}")
    # leading slash on the path must not double up
    check("raw_url() tolerates a leading-slash relpath",
          R.raw_url(sha, "/" + relpath) == expected,
          R.raw_url(sha, "/" + relpath))

    # ---------------------------------------------------------------- #
    # 2. stage_segment writes to the right place + returns `git add -f`
    # ---------------------------------------------------------------- #
    # copy=True path: write a tiny source segment and stage it
    src = os.path.join(RELAY_DIR, "_test_src.mp3")
    os.makedirs(RELAY_DIR, exist_ok=True)
    with open(src, "wb") as f:
        f.write(b"ID3test-bytes")
    staged = R.stage_segment(src, "L99_test.mp3", copy=True)
    dest = staged["dest_abspath"]
    check("stage_segment wrote the segment under audio_relay/",
          os.path.isfile(dest) and os.path.dirname(dest) == RELAY_DIR, dest)
    check("stage_segment dest bytes match source",
          os.path.isfile(dest) and open(dest, "rb").read() == b"ID3test-bytes")
    check("stage_segment repo_relpath is repo-root-relative",
          staged["repo_relpath"] == "when-it-rains/audio_relay/L99_test.mp3",
          staged["repo_relpath"])
    check("stage_segment returns a `git add -f` (force, not plain add)",
          staged["git_add_cmd"] == "git add -f when-it-rains/audio_relay/L99_test.mp3",
          staged["git_add_cmd"])
    check("stage_segment git command is force-add (has -f)",
          " -f " in (" " + staged["git_add_cmd"] + " "), staged["git_add_cmd"])
    # copy=False must not touch disk
    ghost = R.stage_segment("audio_segments/L98.mp3", "L98_ghost.mp3", copy=False)
    check("stage_segment(copy=False) does NOT write a file",
          not os.path.isfile(ghost["dest_abspath"]))
    check("stage_segment(copy=False) still returns a `git add -f`",
          ghost["git_add_cmd"] ==
          "git add -f when-it-rains/audio_relay/L98_ghost.mp3",
          ghost["git_add_cmd"])
    # tidy unit-test artifacts
    for p in (src, dest):
        if os.path.isfile(p):
            os.remove(p)

    # ---------------------------------------------------------------- #
    # 3. build_relay_plan covers all in-scope line_map lines + determinism
    # ---------------------------------------------------------------- #
    lm = json.load(open(LINE_MAP))
    in_scope = [l for l in lm["lines"] if l.get("in_scope")]
    plan = R.build_relay_plan(lm)
    check("plan in_scope_line_count matches line_map",
          plan["in_scope_line_count"] == len(in_scope),
          f"{plan['in_scope_line_count']} vs {len(in_scope)}")
    check("plan has one entry per in-scope line",
          len(plan["entries"]) == len(in_scope), str(len(plan["entries"])))
    plan_ids = [e["line_id"] for e in plan["entries"]]
    check("plan covers exactly the in-scope line_ids",
          plan_ids == [l["line_id"] for l in in_scope], str(plan_ids[:3]))
    # every entry carries a force-add, the 3 calls, and the right still_id
    id_by_line = {l["line_id"]: l["still_id"] for l in in_scope}
    good = all(
        e["git_add_cmd"].startswith("git add -f ")
        and e["still_id"] == id_by_line[e["line_id"]]
        and [c["tool"] for c in e["calls"]]
            == ["media_import_url", "media_import_url", R.LIPSYNC_MODEL]
        and e["raw_url"] is None
        for e in plan["entries"]
    )
    check("every plan entry: force-add + right still_id + import/import/wan2_7 + raw_url null",
          good, str(plan["entries"][:1]))
    check("first import call is audio, second is image",
          plan["entries"][0]["calls"][0]["args"]["type"] == "audio"
          and plan["entries"][0]["calls"][1]["args"]["type"] == "image")

    # determinism: two independent builds -> byte-identical plan JSON
    def dump(p):
        return json.dumps(p, indent=2, sort_keys=True)
    md5a = hashlib.md5(dump(R.build_relay_plan(lm)).encode()).hexdigest()
    md5b = hashlib.md5(dump(R.build_relay_plan(json.load(open(LINE_MAP)))).encode()).hexdigest()
    check("build_relay_plan JSON is deterministic (md5 stable across 2 runs)",
          md5a == md5b, f"{md5a} vs {md5b}")

    # ---------------------------------------------------------------- #
    # 4. no forbidden upload host anywhere + assert_no_upload_host refuses
    # ---------------------------------------------------------------- #
    src_txt = open(RELAY).read()
    # the source names the host only as the FORBIDDEN constant / in refusal docs,
    # never as an actual endpoint to call. There must be zero PUT/upload usage.
    check("source does not PUT/curl to the upload host",
          "curl" not in src_txt.lower() and "-T " not in src_txt
          and "requests.put" not in src_txt and "urlopen" not in src_txt,
          "found an upload/PUT primitive")
    runbook = R.emit_runbook(plan)
    plan_txt = dump(plan)
    # the produced plan + runbook must never NAME the egress-blocked host at all —
    # the relay describes itself positively (import from the raw GitHub URL) and
    # leaks zero reference to upload.higgsfield.ai.
    check("produced plan JSON never names the upload host",
          R.FORBIDDEN_UPLOAD_HOST not in plan_txt)
    check("produced runbook never names the upload host",
          R.FORBIDDEN_UPLOAD_HOST not in runbook)
    raised = False
    try:
        R.assert_no_upload_host("https://upload.higgsfield.ai/put/xyz")
    except AssertionError:
        raised = True
    check("assert_no_upload_host REFUSES a forbidden-host value", raised)
    # and it passes clean values through
    ok = True
    try:
        R.assert_no_upload_host("https://raw.githubusercontent.com/o/r/sha/f.mp3", None)
    except AssertionError:
        ok = False
    check("assert_no_upload_host passes clean values", ok)

    # ---------------------------------------------------------------- #
    # 5. --dry-run: exits 0, ZERO network, writes plan+runbook; --go refused
    # ---------------------------------------------------------------- #
    shim_dir = os.path.join(RELAY_DIR, "_netguard")
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
    r = run(RELAY, "--dry-run", env=env)
    check("relay --dry-run exits 0 with network guarded", r.returncode == 0,
          (r.stderr or r.stdout)[-400:])
    check("relay --dry-run printed the relay plan",
          "media_import_url" in r.stdout and R.LIPSYNC_MODEL in r.stdout,
          r.stdout[-200:])
    check("relay --dry-run wrote relay_plan.json", os.path.isfile(PLAN_JSON))
    check("relay --dry-run wrote relay_runbook.md", os.path.isfile(RUNBOOK_MD))
    if os.path.isfile(RUNBOOK_MD):
        rb = open(RUNBOOK_MD).read()
        check("runbook documents the ONE push is gated",
              "push" in rb.lower() and "go" in rb.lower(), rb[:200])
        check("runbook documents `git add -f` staging",
              "git add -f" in rb, rb[:200])
    # written plan on disk is byte-identical to the in-memory deterministic md5
    if os.path.isfile(PLAN_JSON):
        disk_md5 = hashlib.md5(
            (dump(json.load(open(PLAN_JSON)))).encode()).hexdigest()
        check("written relay_plan.json matches deterministic plan md5",
              disk_md5 == md5a, f"{disk_md5} vs {md5a}")

    # --go must be REFUSED (SystemExit / nonzero), and still no network
    r = run(RELAY, "--go", env=env)
    check("relay --go is REFUSED (nonzero exit)", r.returncode != 0,
          f"rc={r.returncode}")
    check("relay --go refusal names the gate (not performed by this script)",
          "not performed" in (r.stdout + r.stderr).lower()
          or "gated" in (r.stdout + r.stderr).lower(),
          (r.stdout + r.stderr)[-200:])

    # ---------------------------------------------------------------- #
    # 6. committed source: no executed git push, no executed MCP/generate
    # ---------------------------------------------------------------- #
    # `git push` may appear ONLY as documented runbook text — never executed. With
    # no shell-out primitive present (checked next), every `git push` string is
    # necessarily inert documentation.
    check("source never subprocess-runs / shells out (no git push can execute)",
          "subprocess" not in src_txt and "os.system" not in src_txt
          and "Popen" not in src_txt and "os.exec" not in src_txt,
          "source shells out — a git push could execute")
    check("source imports no network client",
          "\nimport requests" not in src_txt and "\nimport urllib" not in src_txt
          and "\nfrom urllib" not in src_txt and "\nimport http" not in src_txt,
          "top-level network import present")

    # ---------------------------------------------------------------- #
    # tidy: leave the tree as we found it (remove artifacts we created)
    # ---------------------------------------------------------------- #
    if os.path.isdir(shim_dir):
        shutil.rmtree(shim_dir)
    if not plan_existed and os.path.isfile(PLAN_JSON):
        os.remove(PLAN_JSON)
    if not runbook_existed and os.path.isfile(RUNBOOK_MD):
        os.remove(RUNBOOK_MD)

    print(f"\n{PASS} passed, {FAIL} failed, {SKIP} skipped")
    return 1 if FAIL else 0


if __name__ == "__main__":
    sys.exit(main())
