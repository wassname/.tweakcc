import json,glob,os,collections,re
root=os.path.expanduser("~/.claude/projects")
ids={}; hits=collections.Counter()
for f in glob.glob(os.path.join(root,"**","*.jsonl"),recursive=True):
    try: fh=open(f,errors="replace")
    except OSError: continue
    with fh:
        for line in fh:
            if 'toolu_' not in line: continue
            try: d=json.loads(line)
            except Exception: continue
            ct=(d.get("message") or {}).get("content")
            if not isinstance(ct,list): continue
            for x in ct:
                if not isinstance(x,dict): continue
                if x.get("type")=="tool_use" and x.get("name")=="Bash":
                    ids[x.get("id")]=(x.get("input") or {})
                elif x.get("type")=="tool_result" and x.get("is_error"):
                    b=x.get("content")
                    if isinstance(b,list): b=" ".join(y.get("text","") for y in b if isinstance(y,dict))
                    if "Command timed out after" in str(b):
                        inp=ids.get(x.get("tool_use_id"),{})
                        cmd=" ".join(str(inp.get("command","?")).split())[:70]
                        hits[(cmd.split()[0] if cmd.split() else "?", cmd)]+=1
print("top timed-out commands:")
for (head,cmd),v in hits.most_common(15): print(f"  {v:4d}  {cmd}")
print("\nby leading binary:")
agg=collections.Counter()
for (head,cmd),v in hits.items(): agg[head]+=v
for k,v in agg.most_common(12): print(f"  {v:4d}  {k}")
