import json, re, subprocess, sys, urllib.parse, time

UA = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0 Safari/537.36"

def fetch(url):
    r = subprocess.run(["curl","-s","-H","User-Agent: "+UA,"-H","Accept-Language: en-US,en;q=0.9",url],
                       capture_output=True, text=True, timeout=90)
    return r.stdout

def search(q, limit=25):
    url = "https://www.youtube.com/results?search_query=" + urllib.parse.quote(q) + "&sp=EgIQAQ%253D%253D"
    html = fetch(url)
    m = re.search(r"var ytInitialData = (\{.*?\});</script>", html)
    if not m:
        m = re.search(r'ytInitialData"\]\s*=\s*(\{.*?\});</script>', html)
    if not m:
        return []
    data = json.loads(m.group(1))
    out = []
    def walk(o):
        if isinstance(o, dict):
            if "videoRenderer" in o:
                v = o["videoRenderer"]
                vid = v.get("videoId")
                title = ""
                try:
                    title = "".join(r["text"] for r in v["title"]["runs"])
                except Exception:
                    title = v.get("title",{}).get("simpleText","")
                ch = ""
                try:
                    ch = v["ownerText"]["runs"][0]["text"]
                except Exception:
                    try: ch = v["longBylineText"]["runs"][0]["text"]
                    except Exception: pass
                dur = ""
                try: dur = v["lengthText"]["simpleText"]
                except Exception: pass
                if vid: out.append({"id":vid,"title":title,"channel":ch,"dur":dur})
            for val in o.values(): walk(val)
        elif isinstance(o, list):
            for val in o: walk(val)
    walk(data)
    seen=set(); res=[]
    for r in out:
        if r["id"] in seen: continue
        seen.add(r["id"]); res.append(r)
    return res[:limit]

if __name__ == "__main__":
    for q in sys.argv[1:]:
        print("="*10, q)
        for r in search(q):
            print(f"{r['id']} | {r['channel']} | {r['dur']} | {r['title']}")
        time.sleep(1)
