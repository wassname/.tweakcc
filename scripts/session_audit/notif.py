import json, glob, os, collections
root=os.path.expanduser("~/.claude/projects")
c=collections.Counter(); sess=collections.Counter()
for f in glob.glob(os.path.join(root,"**","*.jsonl"),recursive=True):
    if "/subagents/" in f: continue
    try: fh=open(f,errors="replace")
    except OSError: continue
    with fh:
        for line in fh:
            if 'task-notification' not in line: continue
            try: d=json.loads(line)
            except Exception: continue
            ts=(d.get("timestamp") or "")[:10]
            m=d.get("message") or {}
            ct=m.get("content")
            if isinstance(ct,list):
                ct=" ".join(x.get("text","") for x in ct if isinstance(x,dict))
            if not isinstance(ct,str) or "<task-notification>" not in ct: continue
            c[ts]+=1; sess[(ts,os.path.basename(f)[:8])]+=1
print("day        task-notifications")
for d in sorted(c):
    if d>="2026-07-01": print(f"{d}  {c[d]:4d}")
print("\ntop sessions by notifications:")
for k,v in sess.most_common(8): print(f"  {k[0]} {k[1]} {v}")
