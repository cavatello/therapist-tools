import json,re,subprocess,sys
UA="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0 Safari/537.36"
def desc(vid):
    h=subprocess.run(["curl","-s","-H","User-Agent: "+UA,f"https://www.youtube.com/watch?v={vid}"],capture_output=True,text=True,timeout=90).stdout
    m=re.search(r'"shortDescription":"(.*?)","isCrawlable"',h,re.S)
    d=json.loads('"'+m.group(1)+'"') if m else "(none)"
    t=re.search(r'"title":"(.*?)","lengthSeconds"',h)
    return (json.loads('"'+t.group(1)+'"') if t else "?"), d[:600]
for v in sys.argv[1:]:
    t,d=desc(v)
    print("="*8,v,"|",t); print(d); print()
