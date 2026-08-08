import json, glob, os, collections
root=os.path.expanduser("~/.claude/projects")
c=collections.Counter()
for f in glob.glob(os.path.join(root,"**","*.jsonl"),recursive=True):
    try: fh=open(f,errors="replace")
    except OSError: continue
    with fh:
        for line in fh:
            if '"tool_use"' not in line: continue
            try: d=json.loads(line)
            except Exception: continue
            ts=(d.get("timestamp") or "")[:10]
            if ts<"2026-06-25": continue
            m=d.get("message") or {}
            ct=m.get("content")
            if not isinstance(ct,list): continue
            for x in ct:
                if isinstance(x,dict) and x.get("type")=="tool_use" and x.get("name") in ("Agent","Bash"):
                    inp=x.get("input") or {}
                    v=inp.get("run_in_background")
                    c[(ts,x["name"],"bg=True" if v is True else ("bg=False" if v is False else "absent"))]+=1
days=sorted({k[0] for k in c})
print(f"{'day':11} {'Agent bg':>8} {'Ag fg':>6} {'Ag abs':>6} | {'Bash bg':>7} {'Bash abs':>8}")
for d in days:
    print(f"{d:11} {c[(d,'Agent','bg=True')]:8d} {c[(d,'Agent','bg=False')]:6d} {c[(d,'Agent','absent')]:6d} | {c[(d,'Bash','bg=True')]:7d} {c[(d,'Bash','absent')]:8d}")
