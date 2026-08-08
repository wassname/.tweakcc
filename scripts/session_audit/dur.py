import json,glob,os,collections
from datetime import datetime
root=os.path.expanduser("~/.claude/projects")
starts={}; ends=[]
for f in glob.glob(os.path.join(root,"**","*.jsonl"),recursive=True):
    if "/subagents/" in f: continue
    try: fh=open(f,errors="replace")
    except OSError: continue
    with fh:
        for line in fh:
            if 'toolu_' not in line: continue
            try: d=json.loads(line)
            except Exception: continue
            ts=d.get("timestamp") or ""
            if ts[:10]<"2026-07-25": continue
            m=d.get("message") or {}; ct=m.get("content")
            if isinstance(ct,list):
                for x in ct:
                    if isinstance(x,dict) and x.get("type")=="tool_use" and (x.get("input") or {}).get("run_in_background") is True:
                        starts[x["id"]]=(ts,x.get("name"))
            if isinstance(ct,str) and "<task-notification>" in ct and "<tool-use-id>" in ct:
                tid=ct.split("<tool-use-id>")[1].split("</tool-use-id>")[0]
                ends.append((tid,ts))
durs=[]
for tid,ets in ends:
    if tid in starts:
        s,name=starts[tid]
        try:
            a=datetime.fromisoformat(s.replace("Z","+00:00")); b=datetime.fromisoformat(ets.replace("Z","+00:00"))
        except Exception: continue
        durs.append(((b-a).total_seconds(), name))
durs.sort(reverse=True)
print(f"matched {len(durs)} background tasks with a completion notification\n")
buckets=collections.Counter()
for s,n in durs:
    b = "<1m" if s<60 else "1-5m" if s<300 else "5-15m" if s<900 else "15-60m" if s<3600 else ">1h"
    buckets[b]+=1
for b in ["<1m","1-5m","5-15m","15-60m",">1h"]:
    print(f"  {b:8} {buckets[b]:4d}")
print("\nlongest 10:")
for s,n in durs[:10]: print(f"  {s/60:8.1f} min  {n}")
