#!/usr/bin/env python3
"""Did the `sleep N; sleep M` chaining habit predate the 2026-07-25 upgrade?

Chained sleeps are the tell that the model believes in a short wait ceiling and is
splitting one wait into sub-limit pieces. If the habit is equally common before the
upgrade, our prompt compression did not cause it.
"""
import collections
import glob
import json
import os
import re

CUT = "2026-07-25"
root = os.path.expanduser("~/.claude/projects")
CHAINED = re.compile(r"\bsleep\s+\d+\s*;\s*sleep\s+\d+")

cmd_of_id = {}
counts = collections.Counter()

for f in glob.glob(os.path.join(root, "**", "*.jsonl"), recursive=True):
    try:
        fh = open(f, errors="replace")
    except OSError:
        continue
    with fh:
        for line in fh:
            if "toolu_" not in line:
                continue
            try:
                d = json.loads(line)
            except Exception:
                continue
            ts = (d.get("timestamp") or "")[:10]
            era = "pre" if ts < CUT else "post"
            content = (d.get("message") or {}).get("content")
            if not isinstance(content, list):
                continue
            for c in content:
                if not isinstance(c, dict):
                    continue
                if c.get("type") == "tool_use" and c.get("name") == "Bash":
                    cmd = str((c.get("input") or {}).get("command", ""))
                    cmd_of_id[c.get("id")] = cmd
                    counts[("bash_calls", era)] += 1
                    if CHAINED.search(cmd):
                        counts[("chained_sleep", era)] += 1
                elif c.get("type") == "tool_result" and c.get("is_error"):
                    body = c.get("content")
                    if isinstance(body, list):
                        body = " ".join(x.get("text", "") for x in body if isinstance(x, dict))
                    if "Command timed out" in str(body):
                        if cmd_of_id.get(c.get("tool_use_id"), "").strip().startswith("sleep"):
                            counts[("sleep_timeout", era)] += 1

print(f"{'metric':16} {'pre <' + CUT:>14} {'post':>10}   per 1k Bash calls")
for k in ("bash_calls", "chained_sleep", "sleep_timeout"):
    pre, post = counts[(k, "pre")], counts[(k, "post")]
    if k == "bash_calls":
        print(f"{k:16} {pre:14d} {post:10d}")
    else:
        rp = 1000 * pre / max(counts[("bash_calls", "pre")], 1)
        rq = 1000 * post / max(counts[("bash_calls", "post")], 1)
        print(f"{k:16} {pre:14d} {post:10d}   {rp:.2f} -> {rq:.2f}")
