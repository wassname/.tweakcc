#!/usr/bin/env python3
"""Scan Claude Code session JSONL for tool-call error rates, grouped by day and tool."""
import json, sys, os, glob, collections, re

root = os.path.expanduser("~/.claude/projects")
files = glob.glob(os.path.join(root, "**", "*.jsonl"), recursive=True)

use_by_day = collections.Counter()      # (day, tool) -> count
err_by_day = collections.Counter()      # (day, tool) -> count
err_msgs = collections.Counter()        # normalized message -> count
err_msgs_recent = collections.Counter()
tool_of_id = {}

CUT = "2026-07-25"

def norm(s):
    s = re.sub(r"\d+", "N", s[:200])
    s = re.sub(r"/[^\s]+", "PATH", s)
    return s.strip()

for f in files:
    try:
        fh = open(f, errors="replace")
    except OSError:
        continue
    with fh:
        for line in fh:
            if '"tool_use"' not in line and '"tool_result"' not in line:
                continue
            try:
                d = json.loads(line)
            except Exception:
                continue
            ts = (d.get("timestamp") or "")[:10]
            msg = d.get("message") or {}
            content = msg.get("content")
            if not isinstance(content, list):
                continue
            for c in content:
                if not isinstance(c, dict):
                    continue
                if c.get("type") == "tool_use":
                    tool_of_id[c.get("id")] = c.get("name")
                    use_by_day[(ts, c.get("name"))] += 1
                elif c.get("type") == "tool_result":
                    name = tool_of_id.get(c.get("tool_use_id"), "?")
                    if c.get("is_error"):
                        err_by_day[(ts, name)] += 1
                        body = c.get("content")
                        if isinstance(body, list):
                            body = " ".join(x.get("text", "") for x in body if isinstance(x, dict))
                        body = str(body)
                        err_msgs[(name, norm(body))] += 1
                        if ts >= CUT:
                            err_msgs_recent[(name, norm(body))] += 1

days = sorted({d for d, _ in use_by_day} | {d for d, _ in err_by_day})
days = [d for d in days if d >= "2026-06-20"]
print("day        uses   errs   err%")
for d in days:
    u = sum(v for (dd, _), v in use_by_day.items() if dd == d)
    e = sum(v for (dd, _), v in err_by_day.items() if dd == d)
    if u:
        print(f"{d} {u:6d} {e:6d} {100*e/u:6.1f}")

print("\n--- per-tool error rate, since", CUT)
tot_u = collections.Counter(); tot_e = collections.Counter()
for (d, t), v in use_by_day.items():
    if d >= CUT: tot_u[t] += v
for (d, t), v in err_by_day.items():
    if d >= CUT: tot_e[t] += v
print(f"{'tool':28} {'uses':>6} {'errs':>6} {'err%':>6}")
for t, u in tot_u.most_common(25):
    e = tot_e[t]
    print(f"{str(t):28} {u:6d} {e:6d} {100*e/u:6.1f}")

print("\n--- top error messages since", CUT)
for (t, m), v in err_msgs_recent.most_common(25):
    print(f"{v:5d}  [{t}] {m[:150]}")
