import json, glob, os, re
root=os.path.expanduser("~/.claude/projects")
pat=re.compile(r"(background|why did you|why are you|stop doing|that'?s wrong|you didn'?t|hallucinat|made up|fabricat|dumb|worse|degrad|broken|wtf|annoying|weird)",re.I)
hits=[]
for f in glob.glob(os.path.join(root,"**","*.jsonl"),recursive=True):
    if "/subagents/" in f: continue
    try: fh=open(f,errors="replace")
    except OSError: continue
    with fh:
        for line in fh:
            if '"user"' not in line: continue
            try: d=json.loads(line)
            except Exception: continue
            ts=(d.get("timestamp") or "")[:19]
            if ts[:10]<"2026-07-25": continue
            if d.get("type")!="user": continue
            m=d.get("message") or {}
            ct=m.get("content")
            if isinstance(ct,list):
                ct=" ".join(x.get("text","") for x in ct if isinstance(x,dict) and x.get("type")=="text")
            if not isinstance(ct,str) or not ct.strip(): continue
            if "<system-reminder>" in ct or ct.startswith("Caveat:") or "tool_use_error" in ct: continue
            if len(ct)>600: continue
            if pat.search(ct):
                hits.append((ts, os.path.basename(os.path.dirname(f))[:28], " ".join(ct.split())[:260]))
hits.sort()
print(len(hits),"hits")
for h in hits: print(f"{h[0]} | {h[2]}")
