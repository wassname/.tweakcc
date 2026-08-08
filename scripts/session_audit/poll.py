import json, glob, os, collections, re
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
            if ts<"2026-07-01": continue
            m=d.get("message") or {}
            ct=m.get("content")
            if not isinstance(ct,list): continue
            for x in ct:
                if not (isinstance(x,dict) and x.get("type")=="tool_use"): continue
                n=x.get("name"); inp=x.get("input") or {}
                c[(ts,"ALL")]+=1
                if n=="Bash":
                    cmd=inp.get("command","")
                    if re.search(r'\bsleep\s+\d', cmd): c[(ts,"bash_sleep")]+=1
                if n in ("TaskOutput","BashOutput","TaskGet","TaskList"): c[(ts,"poll_"+n)]+=1
                if n=="ScheduleWakeup": c[(ts,"wakeup")]+=1
days=sorted({k[0] for k in c})
cols=["bash_sleep","poll_TaskOutput","poll_BashOutput","poll_TaskGet","poll_TaskList","wakeup"]
print(f"{'day':11}{'total':>7}"+"".join(f"{x.replace('poll_',''):>12}" for x in cols))
for d in days:
    print(f"{d:11}{c[(d,'ALL')]:7d}"+"".join(f"{c[(d,x)]:12d}" for x in cols))
