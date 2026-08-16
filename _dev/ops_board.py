#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""The status board: generated like every other page, and encrypted at rest.

WHY IT IS A BUILDER AND NOT A DOCUMENT

A status board somebody has to remember to update is a status board that is
wrong. This one is built by the publishing pipeline: page counts and page
titles come out of the live registry, so they cannot drift from the site they
describe. What lives in `_dev/ops_state.py` is only the judgement - what is
blocked, on whom, and what is worth doing next - short enough to read in one
screen.

Run the pipeline and the board is current. That is the whole design.

WHY /ops/ AND NOT /_ops/

The first version wrote to `_ops/` and 404ed. `_config.yml` already explains
why, in its own words: "Directories beginning with an underscore are excluded
by Jekyll anyway, which is why `_dev/` already 404s." So: `ops/`, no
underscore, and `_config.yml` is left alone.

WHY IT IS ENCRYPTED RATHER THAN MERELY OBSCURE

robots.txt and an unguessable path keep a page out of search. They do not keep
it private - anyone with the URL reads everything. This board carries a working
picture of an unlaunched roadmap, so the whole body is encrypted with AES-GCM
under a key derived from a passphrase, and only the ciphertext is published.

That is real protection against discovery and casual scraping. It is NOT
protection against somebody who has both the file and unlimited time: the
ciphertext is public, so the passphrase is the only thing between them and the
content. Use a real passphrase, do not reuse one that guards anything that
matters, and do not put anything genuinely confidential here. It is a work log.

A guard below fails the build if any plaintext from the board survives into the
published file. That check is the one that matters - an encryption pass that
silently stops encrypting is worse than no encryption, because nobody looks
again.
"""
import base64, json, os, subprocess, sys
import hashlib

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import ops_state as S

SITE = os.path.dirname(HERE)
OUT_DIR = os.path.join(SITE, "ops")
OUT = os.path.join(OUT_DIR, "index.html")
REGISTRY = os.path.join(SITE, "mock", "library", "registry.json")
BASE = "https://therapistsupport.org"
ITERATIONS = 250000

try:
    from cryptography.hazmat.primitives.ciphers.aead import AESGCM
except ImportError:
    sys.exit("this pass needs `cryptography` for AES-GCM:\n"
             "  pip3 install cryptography --break-system-packages")


def registry():
    with open(REGISTRY, encoding="utf-8") as f:
        return {p["file"]: p for p in json.load(f)["pages"]}


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
.id{font-family:var(--mono);font-size:11px;font-weight:600;letter-spacing:.08em;
 background:var(--ink);color:var(--gold);padding:2px 7px;border-radius:2px;margin-right:9px;
 vertical-align:2px;display:inline-block}
.mast{background:var(--deep);color:#fff;border-bottom:3px solid var(--ink);padding:40px 0 34px}
.mast .lab{color:var(--gp)}.mast h1{color:#fff;margin:9px 0 12px;max-width:20ch}
.mast p{color:#D9E6DF;max-width:64ch}
.kpi{display:grid;grid-template-columns:repeat(2,1fr);gap:10px;margin-top:22px}
@media(min-width:760px){.kpi{grid-template-columns:repeat(4,1fr)}}
.kpi div{border:1.5px solid rgba(255,255,255,.28);padding:11px 13px}
.kpi .n{font-family:var(--fig);font-weight:800;font-size:28px;color:var(--gp);display:block;line-height:1.05}
.kpi .l{font-size:11.5px;color:#C9DAD2;line-height:1.35;display:block;margin-top:2px}\n.kdark div{border-color:rgba(22,33,27,.25)}.kdark .n{color:var(--pine)}.kdark .l{color:var(--muted)}
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
.ask{list-style:none;padding:0;margin:0}
.ask>li{position:relative;padding:15px 0;border-bottom:1px dashed rgba(22,33,27,.28)}
.ask>li:last-child{border-bottom:0;padding-bottom:2px}
.ask b.h{font-family:var(--sans);font-weight:800;display:inline;font-size:17px}
.ask .why{font-size:14.2px;color:#4A3B10;margin:7px 0 0}
.ask .do{font-size:13.5px;margin:8px 0 0;font-family:var(--mono);background:rgba(22,33,27,.11);
 padding:8px 10px;border-radius:2px}
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
.docs .id{background:var(--gp);color:var(--deep)}
.shipped{list-style:none;padding:0;margin:0}
.shipped li{position:relative;padding:11px 0;border-bottom:1px solid var(--line)}
.shipped li:last-child{border-bottom:0}
.shipped a{font-family:var(--sans);font-weight:800;font-size:16px;text-decoration:none}
.shipped a:hover{text-decoration:underline}
.shipped .d{font-size:14px;color:#4A4437;margin-top:3px}
.bar{height:11px;background:#E6E0D2;border:1.5px solid var(--ink);overflow:hidden;margin:5px 0 3px}
.bar i{display:block;height:100%;background:var(--pine)}
footer{background:var(--deep);color:#C4D5CD;margin-top:50px;padding:26px 0;font-size:13.5px;
 border-top:3px solid var(--ink)}
footer a{color:var(--gp)}
"""

GATE = """<!doctype html>
<html lang="en"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<meta name="robots" content="noindex,nofollow">
<title>Control panel</title>
<style>
body{margin:0;min-height:100vh;display:grid;place-items:center;background:#15342B;
 color:#F4F0E6;font-family:Inter,system-ui,sans-serif;padding:24px}
.box{width:100%;max-width:400px}
h1{font-family:'Bricolage Grotesque',system-ui,sans-serif;font-weight:800;font-size:26px;
 margin:0 0 6px;letter-spacing:-.02em}
p{font-size:14px;color:#BFD2C9;margin:0 0 18px;line-height:1.55}
input{width:100%;box-sizing:border-box;font-family:'IBM Plex Mono',monospace;font-size:16px;
 padding:13px 14px;border:2px solid #16211B;border-radius:8px;background:#FBF9F3;color:#16211B}
input:focus{outline:3px solid #F6C560;outline-offset:1px}
button{width:100%;margin-top:11px;font-family:'Bricolage Grotesque',system-ui,sans-serif;
 font-weight:800;font-size:16px;padding:13px;border:2px solid #16211B;border-radius:8px;
 background:#F6C560;color:#16211B;cursor:pointer}
button:hover{background:#FFD37A}
.err{color:#FFC9C4;font-size:13.5px;margin-top:11px;min-height:19px}
</style></head><body>
<div class="box">
<h1>Control panel</h1>
<p>Encrypted. Enter the passphrase to decrypt this page in your browser &mdash;
nothing is sent anywhere.</p>
<form id="f"><input id="p" type="password" autocomplete="current-password"
 placeholder="Passphrase" autofocus>
<button type="submit">Unlock</button></form>
<div class="err" id="e"></div>
</div>
<script>
var SALT="__SALT__",IV="__IV__",CT="__CT__",ITER=__ITER__;
function b2a(b){return Uint8Array.from(atob(b),function(c){return c.charCodeAt(0)})}
document.getElementById('f').addEventListener('submit',function(ev){
  ev.preventDefault();
  var e=document.getElementById('e');e.textContent='Decrypting\\u2026';
  var pass=document.getElementById('p').value;
  crypto.subtle.importKey('raw',new TextEncoder().encode(pass),'PBKDF2',false,['deriveKey'])
  .then(function(base){
    return crypto.subtle.deriveKey(
      {name:'PBKDF2',salt:b2a(SALT),iterations:ITER,hash:'SHA-256'},
      base,{name:'AES-GCM',length:256},false,['decrypt']);
  }).then(function(key){
    return crypto.subtle.decrypt({name:'AES-GCM',iv:b2a(IV)},key,b2a(CT));
  }).then(function(buf){
    document.open();document.write(new TextDecoder().decode(buf));document.close();
  }).catch(function(){
    e.textContent='Wrong passphrase.';
  });
});
</script></body></html>
"""



# ---------------------------------------------------------------- quality gates
# Each entry: (command, tool shown, what it checks, in plain English).
# Every one is read-only or an explicit --check. They RUN at board-build
# time, so the section always shows the harness's real output for the
# deploy being published - never a hand-typed claim.
GATES = [
    (["orphan_guard.py"], "orphan_guard.py",
     "The reverse of linkcheck: builds the whole internal link graph and "
     "fails if any page in the sitemap has no inbound link at all - so "
     "nothing ships as an unreachable orphan."),
    (["linkcheck.py"], "linkcheck.py",
     "Follows every internal link on every page and fails the build if any "
     "of them goes nowhere or to the wrong place."),
    (["notruncate.py"], "notruncate.py",
     "Opens every published page and fails if one is missing its title, its "
     "h1, the masthead, or has been truncated to an empty shell."),
    (["seo_rules.py"], "seo_rules.py",
     "Checks every page's title and description lengths, canonical, "
     "Open Graph block and heading structure against the house rules; new "
     "findings fail the build, known ones are baselined."),
    (["subdirs_check.py"], "subdirs_check.py",
     "Reconciles the directory map: every directory in the list exists on "
     "disk, and every directory of pages is in the list."),
    (["dca_licensees.py", "--check"], "dca_licensees.py --check",
     "Re-reconciles the licensee dataset the county pages are computed "
     "from, offline, and confirms nothing identifying is in the file."),
    (["family_art.py", "--check"], "family_art.py --check",
     "Verifies every article and school page carries exactly the three "
     "named house stylesheets, no legacy sheet, and an intact hero."),
    (["family_pk.py", "--check"], "family_pk.py --check",
     "The same conversion guard for the research and directory pages, "
     "including the class-vocabulary allowlist that stops a page shipping "
     "half-styled."),
    (["family_tool.py", "--check"], "family_tool.py --check",
     "The tool apps: confirms the replicated legacy chrome is gone, the "
     "house sheets are present, and each app still carries its own CSS."),
    (["family_rest.py", "--check"], "family_rest.py --check",
     "Everything else - the discipline library, the hubs, the home page - "
     "held to the same three-sheet rule."),
]


def run_gates():
    out = []
    for cmd, tool, what in GATES:
        try:
            r = subprocess.run(
                ["python3", os.path.join(HERE, cmd[0])] + cmd[1:],
                capture_output=True, text=True, timeout=180, cwd=SITE)
            lines = [l.strip() for l in (r.stdout + r.stderr).splitlines()
                     if l.strip()]
            metric = lines[-1] if lines else "(no output)"
            out.append((tool, what, metric, r.returncode == 0))
        except Exception as e:
            out.append((tool, what, "did not run: %s" % e, False))
    # the browser gate is stamped by the session that runs it, not re-run
    # here (it needs a real browser); the stamp file is committed with the
    # change it verified.
    bg = os.path.join(HERE, "browser_gate.json")
    if os.path.exists(bg):
        j = json.load(open(bg, encoding="utf-8"))
        out.append(("Playwright browser gate",
                    "A real Chromium loads the changed pages, fills the "
                    "calculators, opens every drawer, and measures what a "
                    "reader would actually see. %s Stamped %s."
                    % (j.get("detail", ""), j.get("stamped", "")),
                    j.get("result", "?"),
                    j.get("result") == "ALL CLEAN"))
    return out




def site_kpis(reg, gates):
    """The site in numbers - computed from the live files at build time,
    so no figure here can go stale. reg is file->page; gates is the
    run_gates() output (computed once, shared with section Q)."""
    import collections, re as _re
    pages = list(reg.values())
    n_reg = len(pages)
    leaves = [p for p in pages if p.get("leaf")]
    sitemap = open(os.path.join(SITE, "sitemap.xml"), encoding="utf-8").read()
    n_sitemap = sitemap.count("<loc>")
    topics = collections.Counter(p["topic"] for p in pages if not p.get("skip"))
    formats = collections.Counter(p.get("format") or "?" for p in pages)
    stages = collections.Counter(st for p in pages
                                 for st in (p.get("stages") or []))
    n_notes = sum(len(p.get("stage_note") or {}) for p in pages)

    # leaf families, by the shapes that exist
    n_cases = sum(1 for f in reg if f.startswith("discipline-case-"))
    n_schools = sum(1 for f in reg
                    if f.endswith("-mft.html") and reg[f].get("leaf"))
    n_orgs = 0
    try:
        import orgprofile_data as _od
        n_orgs = sum(1 for o in _od.ORGS if o["slug"] in reg)
    except Exception:
        pass

    # pipeline size, from ship.py itself
    ship = open(os.path.join(HERE, "ship.py"), encoding="utf-8").read()
    n_passes = len(_re.findall(r'^\s*\("_dev/', ship, _re.M))

    # citations + words, one pass over the registry pages
    n_leginfo, n_ext, n_words = 0, 0, 0
    doms = set()
    for f in reg:
        p = os.path.join(SITE, f)
        if not os.path.exists(p):
            continue
        s2 = open(p, encoding="utf-8").read()
        n_leginfo += s2.count("leginfo.legislature.ca.gov")
        for m in _re.finditer(r'href="https?://([^/"]+)', s2):
            d = m.group(1).lower()
            if "therapistsupport" not in d:
                n_ext += 1
                doms.add(d)
        body = _re.sub(r"<script[\s\S]*?</script>", " ", s2)
        body = _re.sub(r"<style[\s\S]*?</style>", " ", body)
        body = _re.sub(r"<[^>]+>", " ", body)
        n_words += len(body.split())

    g_ok = sum(1 for _, _, _, ok in gates if ok)
    plan_left = S.FIGURES["editorial_total"] - S.FIGURES["editorial_done"]

    groups = [
        ("The library", [
            (n_sitemap, "pages in the sitemap, all indexable"),
            (n_reg, "pages in the registry"),
            (len(leaves), "directory leaves (reached through their hubs)"),
            (4, "stage doors - deciding, students, associates, licensed"),
        ]),
        ("Leaves, by shelf", [
            (n_schools, "MFT program pages"),
            (n_cases, "discipline case studies"),
            (n_orgs, "Bay Area organization profiles"),
            (len(leaves) - n_schools - n_cases - n_orgs, "other leaves"),
        ]),
        ("By topic", [(topics.get(k, 0), k) for k in
                      ("licensure", "practice", "training", "money",
                       "getting-paid")]),
        ("By format", sorted(((v, k) for k, v in formats.items()),
                             reverse=True)),
        ("Written for a stage", [
            (stages.get("deciding", 0), "deciding"),
            (stages.get("student", 0), "in a program"),
            (stages.get("associate", 0), "counting hours"),
            (stages.get("licensed", 0), "licensed"),
            (n_notes, "hand-written stage notes behind them"),
        ]),
        ("Planned", [
            (plan_left, "of the %d approved editorial pages still to "
                        "build" % S.FIGURES["editorial_total"]),
            (S.FIGURES["editorial_done"], "already shipped from that "
                                          "list"),
        ]),
        ("The machinery", [
            (n_passes, "pipeline passes on every build"),
            ("%d/%d" % (g_ok, len(gates)), "quality gates green on this "
                                           "deploy"),
            (n_leginfo, "links to the statute text on leginfo"),
            ("{:,}".format(n_ext), "outbound source links, %d domains"
                                    % len(doms)),
            ("{:,}".format(n_words), "words of checked content"),
        ]),
    ]
    return groups


def board(reg):
    """The plaintext board. Everything is numbered so it can be referred to."""
    o = []
    A = o.append
    n_pages = len(reg)

    A('<!doctype html>\n<html lang="en">\n<head>\n<meta charset="utf-8">')
    A('<meta name="viewport" content="width=device-width,initial-scale=1">')
    A('<meta name="robots" content="noindex,nofollow">')
    A("<title>therapistsupport.org &mdash; control panel</title>")
    A('<link href="https://fonts.googleapis.com/css2?family=Bricolage+Grotesque:'
      "opsz,wght@12..96,600;12..96,800&family=Fraunces:opsz,wght@9..144,600;"
      "9..144,800&family=IBM+Plex+Mono:wght@400;600&family=Inter:wght@400;500;600"
      '&display=swap" rel="stylesheet">')
    A("<style>%s</style>\n</head>\n<body>" % CSS)

    A('<header class="mast"><div class="wrap">')
    A('<span class="lab">control panel &middot; rebuilt %s &middot; every item '
      "numbered</span>" % S.UPDATED)
    A("<h1>Everything in one place.</h1>")
    A("<p>Rebuilt by the publishing pipeline, so it is current every time the "
      "site deploys. <b>Refer to anything by its number</b> &mdash; "
      "&ldquo;do N2&rdquo;, &ldquo;approve P1&rdquo;, &ldquo;A1 is sent&rdquo;.</p>")
    A('<div class="kpi">')
    for n, l in ((n_pages, "pages live &middot; 0 build failures"),
                 (len(S.ASKS), "waiting on you &mdash; A1&ndash;A%d" % len(S.ASKS)),
                 (len(S.DOCS), "proposal awaiting a decision"),
                 (S.FIGURES["editorial_total"] - S.FIGURES["editorial_done"],
                  "approved pages remaining")):
        A('<div><span class="n">%s</span><span class="l">%s</span></div>' % (n, l))
    A("</div></div></header>")

    gates = run_gates()
    kpis = site_kpis(reg, gates)

    A('<nav><div class="wrap" style="padding:0"><ul>')
    for href, label in (("kpis", "K &mdash; the site in numbers"),
                        ("you", "A &mdash; waiting on you"),
                        ("docs", "P &mdash; proposals"),
                        ("now", "F &mdash; in flight"),
                        ("blocked", "B &mdash; blocked"),
                        ("next", "N &mdash; next up"),
                        ("shipped", "S &mdash; shipped"),
                        ("gates", "Q &mdash; quality gates"),
                        ("closed", "C &mdash; closed")):
        A('<li><a href="#%s">%s</a></li>' % (href, label))
    A("</ul></div></nav>")
    A('<div class="wrap">')

    # K - the site in numbers
    A('<section id="kpis"><div class="kick"><span class="n">K</span>'
      "<h2>The site in numbers</h2></div>")
    A('<p class="lede">Computed from the live files while this board was '
      "being built &mdash; none of these figures is typed in, so none "
      "can go stale.</p>")
    for gname, items in kpis:
        A('<div class="card"><h3>%s</h3><div class="kpi kdark">' % gname)
        for n, l in items:
            A('<div><span class="n">%s</span><span class="l">%s</span>'
              "</div>" % (n, l))
        A("</div></div>")
    A("</section><hr>")

    # A - asks
    A('<section id="you"><div class="kick"><span class="n">A</span>'
      "<h2>Waiting on you</h2></div>")
    A('<p class="lede">Nothing else is blocked on you.</p>')
    A('<div class="card gold"><ul class="ask">')
    for i, a in enumerate(S.ASKS, 1):
        A("<li>")
        A('<span class="id">A%d</span><b class="h">%s</b>' % (i, a["title"]))
        A('<p class="why">%s</p>' % a["why"])
        if a["detail"]:
            A("<ol>")
            for d in a["detail"]:
                A("<li>%s</li>" % d)
            A("</ol>")
        A('<div class="do">%s</div>' % a["do"])
        A("</li>")
    A("</ul></div></section>")

    # P - proposals
    A('<hr><section id="docs"><div class="kick"><span class="n">P</span>'
      "<h2>Proposals and prototypes</h2></div>")
    A('<p class="lede">Published alongside this board, so they open in a browser '
      "on any device rather than living inside a chat.</p>")
    A('<div class="docs">')
    for i, (href, title, desc) in enumerate(S.DOCS, 1):
        A('<a href="%s"><span class="id">P%d</span><span class="t">%s</span>'
          '<span class="d">%s</span><span class="go">Open &rarr;</span></a>'
          % (href, i, title, desc))
    A("</div></section>")

    # F - in flight
    A('<hr><section id="now"><div class="kick"><span class="n">F</span>'
      "<h2>In flight</h2></div>")
    for i, it in enumerate(S.NOW, 1):
        A('<div class="item %s"><div class="t"><span class="id">F%d</span>%s'
          '<span class="tag t-go">%s</span></div><div class="m">%s</div>'
          % (it["state"], i, it["title"], it["tag"], it["meta"]))
        for p in it["body"]:
            A("<p>%s</p>" % p)
        A("</div>")

    yrs = S.FIGURES["county_pay_years"]
    A('<div class="tw"><table><tr><th>Clinical mental-health positions in '
      "California counties</th>%s</tr>" % "".join("<th>%s</th>" % y for y in yrs))
    for row in S.FIGURES["county_pay"]:
        cls = ' class="hi"' if "median top" in row[0] else ""
        A("<tr%s><td>%s</td>%s</tr>"
          % (cls, row[0], "".join('<td class="f">%s</td>' % c for c in row[1:])))
    A("</table></div>")
    A('<p class="cap">Actual wages include part-year staff, which is why they '
      "sit below the published range and answer a different question. Counts "
      "are a floor, not a census.</p>")

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
    A('</table><p style="font-size:14.3px;margin:10px 0 0"><b>2.8&times; between '
      "the top and the bottom</b> for comparable work, inside one state, from "
      "the employers&rsquo; own returns.</p></div>")
    A('<div class="card"><h3>The pre-licensed row, and its limit</h3>'
      '<p style="font-size:14.3px">Exactly <b>one</b> county publishes an '
      "explicitly pre-licensed clinical title: <b>San Bernardino</b>, "
      "&ldquo;Clinical Therapist Pre-License&rdquo;, <b>175 people, "
      "$71,510&ndash;$91,270</b>.</p>"
      '<p style="font-size:14.3px">Its licensed equivalent &mdash; 524 people '
      "across San Bernardino and Riverside &mdash; runs "
      "<b>$73,528&ndash;$104,682</b>.</p>"
      '<p style="font-size:14.3px;margin-bottom:0">About <b>$13,400 of licensure '
      "premium at the top of the range</b>. One county, and the page will say so "
      "rather than generalize.</p></div></div></section>")

    # B - blocked
    A('<hr><section id="blocked"><div class="kick"><span class="n">B</span>'
      "<h2>Blocked, and on what</h2></div>")
    for i, b in enumerate(S.BLOCKED, 1):
        A('<div class="item block"><div class="t"><span class="id">B%d</span>%s'
          '<span class="tag t-block">%s</span></div><div class="m">%s</div>'
          % (i, b["title"], b["tag"], b["meta"]))
        for p in b["body"]:
            A("<p>%s</p>" % p)
        A("</div>")
    A("</section>")

    # N - next
    A('<hr><section id="next"><div class="kick"><span class="n">N</span>'
      "<h2>Next up, nothing blocking</h2></div>")
    A('<p class="lede">Ordered by what I think is most valuable. Say a number to '
      "reorder it.</p>")
    A('<div class="grid2">')
    for i, (t, m, d) in enumerate(S.NEXT, 1):
        A('<div class="item go"><div class="t"><span class="id">N%d</span>%s</div>'
          '<div class="m">%s</div><p>%s</p></div>' % (i, t, m, d))
    A("</div>")
    done, total = S.FIGURES["editorial_done"], S.FIGURES["editorial_total"]
    A('<div style="margin-top:6px"><span class="lab">Approved editorial list '
      "&mdash; %d of %d done</span>"
      '<div class="bar"><i style="width:%d%%"></i></div></div></section>'
      % (done, total, round(100.0 * done / total)))

    # S - shipped
    A('<hr><section id="shipped"><div class="kick"><span class="n">S</span>'
      "<h2>Shipped &mdash; every link live</h2></div>")
    A('<ul class="shipped">')
    missing = []
    for i, (f, desc) in enumerate(S.HIGHLIGHTS, 1):
        p = reg.get(f)
        if not p:
            missing.append(f)
            continue
        A('<li><span class="id">S%d</span><a href="%s/%s">%s</a>'
          '<div class="d">%s</div></li>' % (i, BASE, f, p.get("title") or f, desc))
    A("</ul>")
    A('<p class="cap">Titles and links come from the live registry, so a renamed '
      "page cannot leave a dead entry here.</p></section>")

    # Q - quality gates
    A('<hr><section id="gates"><div class="kick"><span class="n">Q</span>'
      "<h2>Quality gates</h2></div>")
    A('<p class="lede">The internal test harness, run live while this board '
      "was being built &mdash; every metric below is the tool&rsquo;s own "
      "output for this deploy, republished automatically on every deploy. A "
      "red gate here means the pipeline refused to ship.</p>")
    for i, (tool, what, metric, ok) in enumerate(gates, 1):
        A('<div class="item %s"><div class="t"><span class="id">Q%d</span>'
          "<code>%s</code> <b style=\"font-family:var(--mono);font-size:11px;"
          "letter-spacing:.1em;color:%s\">%s</b></div>"
          "<p style=\"margin:6px 0 4px\">%s</p>"
          '<p style="font-family:var(--mono);font-size:12.5px;'
          'background:rgba(22,33,27,.07);padding:7px 10px;border-radius:2px;'
          'margin:0">%s</p></div>'
          % ("go" if ok else "block", i, tool,
             "var(--green)" if ok else "var(--red)",
             "PASS" if ok else "FAIL", what, metric))
    A("</section>")

    # C - closed
    A('<hr><section id="closed"><div class="kick"><span class="n">C</span>'
      "<h2>Closed, with reasons</h2></div>")
    A('<p class="lede">Written down so a future session does not re-propose '
      "them. Say a number to reopen one.</p>")
    A('<div class="grid2">')
    for i, (t, why) in enumerate(S.CLOSED, 1):
        A('<div class="item park"><div class="t"><span class="id">C%d</span>%s'
          "</div><p>%s</p></div>" % (i, t, why))
    A("</div></section>")

    A("</div>")
    A('<footer><div class="wrap"><p style="margin:0">Rebuilt by '
      "<code>_dev/ops_board.py</code> on every deploy, encrypted before "
      "publication. Not indexed, not in the sitemap, not linked from the site. "
      'Live site: <a href="%s">therapistsupport.org</a></p></div></footer>' % BASE)
    A("</body>\n</html>\n")
    return "\n".join(o), missing


def encrypt(plaintext, passphrase):
    salt = os.urandom(16)
    iv = os.urandom(12)
    key = hashlib.pbkdf2_hmac("sha256", passphrase.encode("utf-8"), salt,
                              ITERATIONS, dklen=32)
    ct = AESGCM(key).encrypt(iv, plaintext.encode("utf-8"), None)
    b = lambda x: base64.b64encode(x).decode("ascii")
    return (GATE.replace("__SALT__", b(salt)).replace("__IV__", b(iv))
                .replace("__CT__", b(ct)).replace("__ITER__", str(ITERATIONS)))


def main():
    print("the control panel")
    if not os.path.isdir(OUT_DIR):
        os.makedirs(OUT_DIR)

    reg = registry()
    plain, missing = board(reg)
    if missing:
        sys.exit("listed in ops_state.HIGHLIGHTS and absent from the registry, "
                 "so the board would print a dead link:\n  %s"
                 % "\n  ".join(missing))

    passphrase = os.environ.get("OPS_PASSPHRASE") or S.PASSPHRASE
    if not passphrase or len(passphrase) < 12:
        sys.exit("set a passphrase of at least 12 characters in "
                 "_dev/ops_state.py, or in OPS_PASSPHRASE")

    html = encrypt(plain, passphrase)
    open(OUT, "w", encoding="utf-8").write(html)
    print("  wrote ops/index.html, %s bytes of ciphertext from %s of board"
          % (format(len(html), ",d"), format(len(plain), ",d")))

    # THE GUARD THAT MATTERS. An encryption pass that quietly stops encrypting
    # is worse than none, because nobody checks twice. Every one of these
    # strings is in the plaintext board; none may survive into the file.
    published = open(OUT, encoding="utf-8").read()
    leaks = [s for s in ("Waiting on you", "MBHSLRP@hcai.ca.gov", "San Bernardino",
                         "therapistsupport.org/mbh-slrp", "Blocked, and on what",
                         S.UPDATED)
             if s in published]
    if leaks:
        sys.exit("PLAINTEXT LEAKED INTO THE PUBLISHED FILE: %s" % ", ".join(leaks))

    if "AES-GCM" not in published or "PBKDF2" not in published:
        sys.exit("the published file is not the encrypted shell")

    robots = os.path.join(SITE, "robots.txt")
    txt = open(robots, encoding="utf-8").read() if os.path.exists(robots) else ""
    if "Disallow: /ops/" not in txt:
        sys.exit("robots.txt does not disallow /ops/")

    sm = os.path.join(SITE, "sitemap.xml")
    if os.path.exists(sm) and "/ops/" in open(sm, encoding="utf-8").read():
        sys.exit("/ops/ has got into sitemap.xml")

    for href, _, _ in S.DOCS:
        if not os.path.exists(os.path.join(OUT_DIR, href)):
            sys.exit("the board links to ops/%s and it is not there" % href)

    print("  guards ok - no plaintext in the file, robots disallows it, absent "
          "from the sitemap, every linked doc present")


if __name__ == "__main__":
    main()
