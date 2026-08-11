#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""The status board, generated like every other page rather than hand-written.

WHY IT IS A BUILDER AND NOT AN ARTIFACT

A status board that somebody has to remember to update is a status board that
is wrong. This one is built by the pipeline: page counts and page titles come
out of the live registry, so they cannot drift, and the judgement - what is
blocked, on whom, what is next - lives in `_dev/ops_state.py` where it is
short enough to read in one screen.

Run the pipeline and the board is current. That is the whole design.

WHERE IT LIVES, AND WHY IT IS NOT INDEXED

`/_ops/`. Every content pass on this site scopes itself to the site root plus
the five topic directories, so nothing here is rewritten, restyled, counted as
a page, or put in the sitemap - the same way `concepts.html` and `tycoon.html`
are kept out of search. robots.txt disallows the directory. It is reachable by
anyone with the URL, which is the point: a board you can open on a phone
without a login beats one locked inside a desktop app.

Nothing private goes here. It is a work log, not a document store.
"""
import json, os, sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import ops_state as S

SITE = os.path.dirname(HERE)
OUT_DIR = os.path.join(SITE, "_ops")
OUT = os.path.join(OUT_DIR, "index.html")
REGISTRY = os.path.join(SITE, "mock", "library", "registry.json")
BASE = "https://therapistsupport.org"


def registry():
    with open(REGISTRY, encoding="utf-8") as f:
        d = json.load(f)
    return {p["file"]: p for p in d["pages"]}


CSS = """
:root{--paper:#F4F0E6;--cream:#FBF9F3;--ink:#16211B;--pine:#2C6350;--gold:#F6C560;
 --gp:#FFD37A;--muted:#635E53;--red:#B5483F;--line:#E2DACA;--deep:#15342B;--green:#3F9577;
 --sans:'Bricolage Grotesque',system-ui,sans-serif;--body:Inter,system-ui,sans-serif;
 --fig:'Fraunces',Georgia,serif;--mono:'IBM Plex Mono',ui-monospace,monospace}
*{box-sizing:border-box}html{scroll-behavior:smooth}
body{margin:0;background:var(--paper);color:var(--ink);font-family:var(--body);
 font-size:15.5px;line-height:1.6;-webkit-font-smoothing:antialiased}
.wrap{max-width:1120px;margin:0 auto;padding:0 20px}
h1,h2,h3{font-family:var(--sans);font-weight:800;line-height:1.08;letter-spacing:-.022em;margin:0}
h1{font-size:clamp(30px,4.8vw,52px)}h2{font-size:clamp(23px,3vw,33px);margin:0 0 4px}
h3{font-size:18px;margin:0 0 4px}
p{margin:0 0 12px;max-width:76ch}a{color:var(--pine);text-underline-offset:3px}
code{font-family:var(--mono);font-size:12.5px;background:rgba(22,33,27,.07);padding:1px 5px;
 border-radius:2px;overflow-wrap:anywhere;word-break:break-word}
.lab{font-family:var(--mono);font-size:10.5px;font-weight:600;letter-spacing:.15em;
 text-transform:uppercase;color:var(--muted)}
.mast{background:var(--deep);color:#fff;border-bottom:3px solid var(--ink);padding:40px 0 34px}
.mast .lab{color:var(--gp)}.mast h1{color:#fff;margin:9px 0 12px;max-width:20ch}
.mast p{color:#D9E6DF;max-width:64ch}
.kpi{display:grid;grid-template-columns:repeat(2,1fr);gap:10px;margin-top:22px}
@media(min-width:760px){.kpi{grid-template-columns:repeat(4,1fr)}}
.kpi div{border:1.5px solid rgba(255,255,255,.28);padding:11px 13px}
.kpi .n{font-family:var(--fig);font-weight:800;font-size:28px;color:var(--gp);display:block;line-height:1.05}
.kpi .l{font-size:11.5px;color:#C9DAD2;line-height:1.35;display:block;margin-top:2px}
nav{position:sticky;top:0;z-index:40;background:var(--cream);border-bottom:2px solid var(--ink)}
nav ul{display:flex;list-style:none;margin:0;padding:0;overflow-x:auto;scrollbar-width:none}
nav ul::-webkit-scrollbar{display:none}
nav a{display:block;white-space:nowrap;padding:11px 15px;font-family:var(--mono);font-size:11px;
 letter-spacing:.11em;text-transform:uppercase;text-decoration:none;color:var(--muted);
 border-right:1px solid var(--line)}
nav a:hover{background:var(--gold);color:var(--ink)}
section{padding:40px 0 6px}hr{border:0;border-top:2px solid var(--ink);opacity:.14;margin:36px 0 0}
.kick{display:flex;align-items:baseline;gap:12px;margin-bottom:16px}
.kick .n{font-family:var(--fig);font-weight:800;font-size:32px;color:var(--pine);line-height:1}
.lede{font-size:17px;max-width:66ch;color:#2C3A33}
.card{background:var(--cream);border:2px solid var(--ink);box-shadow:5px 5px 0 var(--ink);
 padding:17px 19px;margin:0 0 17px}
.card.gold{background:var(--gold)}
.grid2{display:grid;gap:16px}@media(min-width:780px){.grid2{grid-template-columns:1fr 1fr}}
.grid2>*{min-width:0}
.ask{counter-reset:a;list-style:none;padding:0;margin:0}
.ask>li{counter-increment:a;position:relative;padding:15px 0 15px 56px;
 border-bottom:1px dashed rgba(22,33,27,.28)}
.ask>li:last-child{border-bottom:0;padding-bottom:2px}
.ask>li::before{content:counter(a);position:absolute;left:0;top:15px;width:34px;height:34px;
 background:var(--ink);color:var(--gold);font-family:var(--mono);font-size:15px;font-weight:600;
 display:grid;place-items:center;border-radius:2px}
.ask b.h{font-family:var(--sans);font-weight:800;display:block;font-size:17px;margin-bottom:3px}
.ask .why{font-size:14.2px;color:#4A3B10;margin:5px 0 0}
.ask .do{font-size:13.5px;margin:8px 0 0;font-family:var(--mono);background:rgba(22,33,27,.09);
 padding:7px 10px;border-radius:2px}
.ask ol{font-size:14px;margin:9px 0 0;padding-left:20px}.ask ol li{margin-bottom:5px}
.item{border-left:4px solid var(--line);padding:0 0 0 15px;margin:0 0 16px}
.item.go{border-color:var(--green)}.item.block{border-color:var(--red)}
.item.park{border-color:var(--muted)}
.item .t{font-family:var(--sans);font-weight:800;font-size:17px;line-height:1.22}
.item .m{font-size:13.2px;color:var(--muted);margin:3px 0 6px}
.item p{font-size:14.3px;margin:0 0 8px}.item p:last-child{margin-bottom:0}
.tag{display:inline-block;font-family:var(--mono);font-size:9.5px;font-weight:600;
 letter-spacing:.11em;text-transform:uppercase;padding:2px 7px;border:1.5px solid;border-radius:2px;
 vertical-align:2px;margin-left:6px;white-space:nowrap}
.t-go{color:#1E5C46;border-color:#1E5C46;background:#E4F0EA}
.t-block{color:var(--red);border-color:var(--red);background:#F7E7E5}
.t-park{color:var(--muted);border-color:var(--muted);background:#EFEBE0}
.tw{overflow-x:auto;border:2px solid var(--ink);box-shadow:5px 5px 0 var(--ink);
 background:var(--cream);margin:0 0 9px}
table{border-collapse:collapse;width:100%;min-width:540px;font-size:14px}
th{background:var(--deep);color:#fff;font-family:var(--mono);font-size:10px;letter-spacing:.12em;
 text-transform:uppercase;text-align:left;padding:9px 12px;font-weight:600}
td{padding:9px 12px;border-top:1px solid var(--line);vertical-align:top}
tbody tr:nth-child(even){background:rgba(226,218,202,.3)}
td.f{font-family:var(--fig);font-weight:600;font-size:16px;text-align:right;white-space:nowrap}
tr.hi{background:var(--gold)!important}
.cap{font-size:13px;color:var(--muted);margin:7px 0 0}
.docs a{display:block;background:var(--pine);color:#fff;border:2px solid var(--ink);
 box-shadow:5px 5px 0 var(--ink);padding:16px 18px;text-decoration:none;margin:0 0 14px}
.docs a:hover{background:var(--deep)}
.docs .t{font-family:var(--sans);font-weight:800;font-size:19px;line-height:1.2}
.docs .d{font-size:14px;color:#DCEAE3;margin-top:5px}
.docs .go{font-family:var(--mono);font-size:10.5px;letter-spacing:.13em;text-transform:uppercase;
 color:var(--gp);margin-top:9px;display:block}
.shipped{list-style:none;padding:0;margin:0}
.shipped li{position:relative;padding:11px 0 11px 28px;border-bottom:1px solid var(--line)}
.shipped li:last-child{border-bottom:0}
.shipped li::before{content:"";position:absolute;left:0;top:17px;width:11px;height:11px;
 background:var(--pine);border:2px solid var(--pine)}
.shipped a{font-family:var(--sans);font-weight:800;font-size:16px;text-decoration:none}
.shipped a:hover{text-decoration:underline}
.shipped .d{font-size:14px;color:#4A4437;margin-top:2px}
.bar{height:11px;background:#E6E0D2;border:1.5px solid var(--ink);overflow:hidden;margin:5px 0 3px}
.bar i{display:block;height:100%;background:var(--pine)}
footer{background:var(--deep);color:#C4D5CD;margin-top:50px;padding:26px 0;font-size:13.5px;
 border-top:3px solid var(--ink)}
footer a{color:var(--gp)}
"""


def build():
    reg = registry()
    n_pages = len(reg)
    o = []
    A = o.append

    A('<!doctype html>\n<html lang="en">\n<head>\n<meta charset="utf-8">')
    A('<meta name="viewport" content="width=device-width,initial-scale=1">')
    A('<meta name="robots" content="noindex,nofollow">')
    A('<title>therapistsupport.org &mdash; control panel</title>')
    A('<link rel="preconnect" href="https://fonts.googleapis.com">')
    A('<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>')
    A('<link href="https://fonts.googleapis.com/css2?family=Bricolage+Grotesque:'
      'opsz,wght@12..96,600;12..96,800&family=Fraunces:opsz,wght@9..144,600;'
      '9..144,800&family=IBM+Plex+Mono:wght@400;600&family=Inter:wght@400;500;600'
      '&display=swap" rel="stylesheet">')
    A("<style>%s</style>\n</head>\n<body>" % CSS)

    # masthead
    A('<header class="mast"><div class="wrap">')
    A('<span class="lab">therapistsupport.org &middot; control panel &middot; '
      'rebuilt %s</span>' % S.UPDATED)
    A("<h1>Everything in one place.</h1>")
    A("<p>What&rsquo;s live, what&rsquo;s moving, what&rsquo;s waiting on you, "
      "and what&rsquo;s parked pending a decision. This page is rebuilt by the "
      "publishing pipeline, so it is current every time the site deploys.</p>")
    A('<div class="kpi">')
    for n, l in ((n_pages, "pages live &middot; 0 build failures"),
                 (len(S.ASKS), "things waiting on you"),
                 (len(S.DOCS), "proposal awaiting a decision"),
                 (S.FIGURES["editorial_total"] - S.FIGURES["editorial_done"],
                  "approved pages remaining")):
        A('<div><span class="n">%s</span><span class="l">%s</span></div>' % (n, l))
    A("</div></div></header>")

    # jump nav
    A('<nav><div class="wrap" style="padding:0"><ul>')
    for href, label in (("you", "Waiting on you"), ("docs", "Proposals"),
                        ("now", "In flight"), ("blocked", "Blocked"),
                        ("next", "Next up"), ("shipped", "Shipped"),
                        ("closed", "Closed")):
        A('<li><a href="#%s">%s</a></li>' % (href, label))
    A("</ul></div></nav>")
    A('<div class="wrap">')

    # 01 asks
    A('<section id="you"><div class="kick"><span class="n">01</span>'
      "<h2>Waiting on you</h2></div>")
    A('<p class="lede">Nothing else is blocked on you.</p>')
    A('<div class="card gold"><ol class="ask">')
    for a in S.ASKS:
        A("<li>")
        A('<b class="h">%s</b>' % a["title"])
        A('<p class="why">%s</p>' % a["why"])
        if a["detail"]:
            A("<ol>")
            for d in a["detail"]:
                A("<li>%s</li>" % d)
            A("</ol>")
        A('<div class="do">%s</div>' % a["do"])
        A("</li>")
    A("</ol></div></section>")

    # 02 docs
    A('<hr><section id="docs"><div class="kick"><span class="n">02</span>'
      "<h2>Proposals and prototypes</h2></div>")
    A('<p class="lede">Published alongside this board, so they open in a browser '
      "on any device rather than living inside a chat.</p>")
    A('<div class="docs">')
    for href, title, desc in S.DOCS:
        A('<a href="%s"><span class="t">%s</span>'
          '<span class="d">%s</span>'
          '<span class="go">Open &rarr;</span></a>' % (href, title, desc))
    A("</div></section>")

    # 03 in flight
    A('<hr><section id="now"><div class="kick"><span class="n">03</span>'
      "<h2>In flight</h2></div>")
    for it in S.NOW:
        A('<div class="item %s"><div class="t">%s<span class="tag t-go">%s</span></div>'
          '<div class="m">%s</div>' % (it["state"], it["title"], it["tag"], it["meta"]))
        for p in it["body"]:
            A("<p>%s</p>" % p)
        A("</div>")

    yrs = S.FIGURES["county_pay_years"]
    A('<div class="tw"><table><tr><th>Clinical mental-health positions in '
      "California counties</th>%s</tr>"
      % "".join("<th>%s</th>" % y for y in yrs))
    for row in S.FIGURES["county_pay"]:
        cls = ' class="hi"' if "median top" in row[0] else ""
        A("<tr%s><td>%s</td>%s</tr>"
          % (cls, row[0], "".join('<td class="f">%s</td>' % c for c in row[1:])))
    A("</table></div>")
    A('<p class="cap">Actual wages include part-year staff, which is why they sit '
      "below the published range and answer a different question. Counts are a "
      "floor, not a census &mdash; county title conventions vary and anything "
      "named unusually is missed.</p>")

    A('<div class="grid2" style="margin-top:16px"><div class="card">'
      "<h3>The spread is the story</h3>"
      '<p style="font-size:14.3px">Median top of the published range, %s:</p>'
      '<table style="min-width:0;font-size:13.5px">' % yrs[-1])
    for c, v in S.FIGURES["spread_high"]:
        A('<tr><td>%s</td><td class="f">%s</td></tr>' % (c, v))
    A('<tr><td colspan="2" style="color:var(--muted)">&hellip; 42 counties '
      "between &hellip;</td></tr>")
    for c, v in S.FIGURES["spread_low"]:
        A('<tr><td>%s</td><td class="f">%s</td></tr>' % (c, v))
    A("</table>"
      '<p style="font-size:14.3px;margin:10px 0 0"><b>2.8&times; between the top '
      "and the bottom</b> for comparable work, inside one state, from the "
      "employers&rsquo; own returns.</p></div>")
    A('<div class="card"><h3>The pre-licensed row, and its limit</h3>'
      '<p style="font-size:14.3px">Exactly <b>one</b> county publishes an '
      "explicitly pre-licensed clinical title: <b>San Bernardino</b>, "
      "&ldquo;Clinical Therapist Pre-License&rdquo;, <b>175 people, "
      "$71,510&ndash;$91,270</b>.</p>"
      '<p style="font-size:14.3px">Its licensed equivalent &mdash; 524 people '
      "across San Bernardino and Riverside &mdash; runs "
      "<b>$73,528&ndash;$104,682</b>.</p>"
      '<p style="font-size:14.3px;margin-bottom:0">About <b>$13,400 of licensure '
      "premium at the top of the range</b>. One county, and the page will say "
      "so rather than generalize.</p></div></div></section>")

    # 04 blocked
    A('<hr><section id="blocked"><div class="kick"><span class="n">04</span>'
      "<h2>Blocked, and on what</h2></div>")
    for b in S.BLOCKED:
        A('<div class="item block"><div class="t">%s<span class="tag t-block">%s'
          '</span></div><div class="m">%s</div>' % (b["title"], b["tag"], b["meta"]))
        for p in b["body"]:
            A("<p>%s</p>" % p)
        A("</div>")
    A("</section>")

    # 05 next
    A('<hr><section id="next"><div class="kick"><span class="n">05</span>'
      "<h2>Next up, nothing blocking</h2></div>")
    A('<div class="grid2">')
    for t, m, d in S.NEXT:
        A('<div class="item go"><div class="t">%s</div><div class="m">%s</div>'
          "<p>%s</p></div>" % (t, m, d))
    A("</div>")
    done, total = S.FIGURES["editorial_done"], S.FIGURES["editorial_total"]
    A('<div style="margin-top:6px"><span class="lab">Approved editorial list '
      "&mdash; %d of %d done</span>"
      '<div class="bar"><i style="width:%d%%"></i></div></div></section>'
      % (done, total, round(100.0 * done / total)))

    # 06 shipped
    A('<hr><section id="shipped"><div class="kick"><span class="n">06</span>'
      "<h2>Shipped &mdash; every link live</h2></div>")
    A('<ul class="shipped">')
    missing = []
    for f, desc in S.HIGHLIGHTS:
        p = reg.get(f)
        if not p:
            missing.append(f)
            continue
        A('<li><a href="%s/%s">%s</a><div class="d">%s</div></li>'
          % (BASE, f, p.get("title") or f, desc))
    A("</ul>")
    A('<p class="cap">Titles and links come from the live registry, so a renamed '
      "page cannot leave a dead entry here.</p></section>")

    # 07 closed
    A('<hr><section id="closed"><div class="kick"><span class="n">07</span>'
      "<h2>Closed, with reasons</h2></div>")
    A('<p class="lede">Written down so a future session does not re-propose '
      "them.</p>")
    A('<div class="grid2">')
    for t, why in S.CLOSED:
        A('<div class="item park"><div class="t">%s</div><p>%s</p></div>' % (t, why))
    A("</div></section>")

    A("</div>")
    A('<footer><div class="wrap"><p style="margin:0">Rebuilt by '
      "<code>_dev/ops_board.py</code> on every deploy. Not indexed, not in the "
      "sitemap, and not linked from the site &mdash; but reachable by anyone "
      'with the URL. Live site: <a href="%s">therapistsupport.org</a></p>'
      "</div></footer>" % BASE)
    A("</body>\n</html>\n")
    return "\n".join(o), missing


def main():
    print("the control panel")
    if not os.path.isdir(OUT_DIR):
        os.makedirs(OUT_DIR)
    html, missing = build()

    if missing:
        sys.exit("these pages are listed in ops_state.HIGHLIGHTS and are not in "
                 "the registry, so the board would print a dead link:\n  %s"
                 % "\n  ".join(missing))

    open(OUT, "w", encoding="utf-8").write(html)
    print("  wrote _ops/index.html, %s bytes" % format(len(html), ",d"))

    # The board must stay out of search and out of the sitemap. Both are true
    # by construction - every content pass scopes itself to the site root plus
    # the five topic directories - but robots.txt is a separate file that a
    # person edits, so it is checked rather than assumed.
    robots = os.path.join(SITE, "robots.txt")
    txt = open(robots, encoding="utf-8").read() if os.path.exists(robots) else ""
    if "Disallow: /_ops/" not in txt:
        print("GUARD: robots.txt does not disallow /_ops/")
        sys.exit(1)
    sm = os.path.join(SITE, "sitemap.xml")
    if os.path.exists(sm) and "/_ops/" in open(sm, encoding="utf-8").read():
        print("GUARD: /_ops/ has got into sitemap.xml")
        sys.exit(1)
    if 'name="robots" content="noindex' not in html:
        print("GUARD: the board is missing its noindex")
        sys.exit(1)

    for href, _, _ in S.DOCS:
        if not os.path.exists(os.path.join(OUT_DIR, href)):
            print("GUARD: the board links to _ops/%s and it is not there" % href)
            sys.exit(1)
    print("  guards ok - noindex, robots, no sitemap entry, every doc present")


if __name__ == "__main__":
    main()
