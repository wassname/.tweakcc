import json, glob, os, collections
root=os.path.expanduser("~/.claude/projects")
c=collections.Counter()
for f in glob.glob(os.path.join(root,"**","*.jsonl"),recursive=True):
    if "/subagents/" in f: continue
    try: fh=open(f,errors="replace")
    except OSError: continue
    with fh:
        for line in fh:
            if '"model"' not in line: continue
            try: d=json.loads(line)
            except Exception: continue
            ts=(d.get("timestamp") or "")[:10]
            if ts<"2026-07-10": continue
            m=d.get("message") or {}
            mod=m.get("model")
            v=d.get("version")
            if mod: c[(ts,mod,v)]+=1
days=sorted({k[0] for k in c})
for d in days:
    parts=[f"{k[1].replace('claude-','')}/{k[2]}:{v}" for k,v in sorted(c.items(),key=lambda x:-x[1]) if k[0]==d]
    print(d, "  ".join(parts[:5]))
