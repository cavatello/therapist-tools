import sys, time, json
sys.path.insert(0,'/home/claude/work/mftguide')
from ytsearch import search

queries = json.load(open(sys.argv[1]))
out = {}
for school, qs in queries.items():
    print("="*20, school, flush=True)
    seen=set()
    for q in qs:
        try:
            rs = search(q, 14)
        except Exception as e:
            print("  ERR", q, e); continue
        for r in rs:
            if r["id"] in seen: continue
            seen.add(r["id"])
            print(f"  {r['id']} | {r['channel']} | {r['dur']} | {r['title']}", flush=True)
        time.sleep(0.6)
