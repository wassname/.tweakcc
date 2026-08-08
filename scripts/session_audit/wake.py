import json,glob,os,collections,re
root=os.path.expanduser("~/.claude/projects")
wake=[]; tmo=collections.Counter(); tmo_set=collections.Counter(); ids={}
for f in glob.glob(os.path.join(root,"**","*.jsonl"),recursive=True):
    try: fh=open(f,errors="replace")
    except OSError: continue
    with fh:
        for line in fh:
            if 'ScheduleWakeup' not in line and 'timed out' not in line and '"Bash"' not in line: continue
            try: d=json.loads(line)
            except Exception: continue
            ts=(d.get("timestamp") or "")[:16]
            m=d.get("message") or {}; ct=m.get("content")
            if not isinstance(ct,list): continue
            for x in ct:
                if not isinstance(x,dict): continue
                if x.get("type")=="tool_use":
                    ids[x.get("id")]=(x.get("name"), x.get("input") or {})
                    if x.get("name")=="ScheduleWakeup":
                        wake.append((ts,(x.get("input") or {})))
                    if x.get("name")=="Bash":
                        t=(x.get("input") or {}).get("timeout")
                        tmo_set["explicit "+str(t)] += 1 if t else 0
                        if not t: tmo_set["absent (120s default)"]+=1
                elif x.get("type")=="tool_result" and x.get("is_error"):
                    b=x.get("content")
                    if isinstance(b,list): b=" ".join(y.get("text","") for y in b if isinstance(y,dict))
                    b=str(b)
                    mm=re.search(r"Command timed out after ([^\n]+)", b)
                    if mm:
                        n,inp=ids.get(x.get("tool_use_id"),("?",{}))
                        tmo[(mm.group(1).strip(), str(inp.get("timeout")))]+=1
print("=== ScheduleWakeup calls (all time) ===")
for ts,inp in wake:
    print(f"  {ts} delaySeconds={inp.get('delaySeconds')} stop={inp.get('stop')} reason={str(inp.get('reason'))[:70]}")
print("\n=== Bash 'Command timed out after X' (grouped: message, requested timeout ms) ===")
for (msg,req),v in tmo.most_common(12): print(f"  {v:4d}  after {msg:14} | requested timeout={req}")
print("\n=== Bash timeout param usage ===")
for k,v in tmo_set.most_common(10):
    if v: print(f"  {v:6d}  {k}")
