#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Build mft-programs-california.html — the directory.

Sixty-five institutions whose graduate degrees are listed by the Board of
Behavioral Sciences as qualifying towards California LMFT licensure, with what
could be verified about each: the exact degree name, COAMFTE accreditation,
units, length, format, whether it also opens the LPCC route, and published
tuition with the year the figure is from.

THREE THINGS THIS PAGE REFUSES TO DO.

It will not estimate tuition. Twenty-one institutions publish a per-unit or
total figure; forty-four do not. The forty-four say "not published" rather than
carrying a plausible number, because a prospective student comparing a
$42,000 programme against a $152,000 one deserves to know which of those two
figures came from the institution and which came from me. None came from me.

It will not rank. There is no scoring, no stars and no "best of". The one
comparative fact that is objective - COAMFTE accreditation, which decides
whether the degree travels out of California - is shown as a filter rather than
as a verdict.

It will not hide the forum threads that are unflattering. Each institution
links to real discussion where it exists, tagged by sentiment, opening in a new
window. Where nothing credible was found the page says so by name, because a
missing link is otherwise indistinguishable from an endorsement.

Chrome and the nav script are lifted from the published hub, so the header
works. That last clause is not decoration: every page previously built this way
shipped with a dead header because the script was not lifted.
"""
import os, re, sys, json, html

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import forums as F
import charts

SRC = os.path.join(HERE, "_chrome.html")
DATA = os.path.join(HERE, "programs.json")
OUT = os.path.join(HERE, "mft-programs-california.html")
UPDATED = "6 August 2026"

PROGRAMS = json.load(open(DATA, encoding="utf-8"))

# Slugs for the thirty-seven institutions that earned a page of their own.
# Written by build_schools.py, read here, so the two can never disagree about
# which schools have pages - a card linking to a page that was not built is a
# 404 the directory would happily ship.
SLUGS = {}
_sf = os.path.join(HERE, "school_slugs.json")
if os.path.exists(_sf):
    SLUGS = json.load(open(_sf, encoding="utf-8"))


def balanced(s, tag):
    i = s.find("<" + tag)
    if i < 0:
        return None
    d = 0
    for m in re.finditer(r"<%s\b|</%s>" % (tag, tag), s[i:]):
        d += 1 if m.group(0).startswith("<" + tag) else -1
        if d == 0:
            return (i, i + m.end())
    return None


src = open(SRC, encoding="utf-8").read()
head_end = src.find("</head>")
links = [m.group(0) for m in re.finditer(r"<link\b[^>]*>", src[:head_end])
         if 'rel="stylesheet"' in m.group(0) or "fonts." in m.group(0)
         or 'rel="preconnect"' in m.group(0)]
styles = re.findall(r"<style>.*?</style>", src, re.S)
assert styles, "no stylesheet lifted"
hs = balanced(src, "header")
header = re.sub(r'(<a href="[^"]*") class="on"', r"\1", src[hs[0]:hs[1]])
fs = balanced(src, "footer")
footer = re.sub(r'(<a href="[^"]*") class="on"', r"\1", src[fs[0]:fs[1]])
navscript = ""
for m in re.finditer(r"<script>([\s\S]*?)</script>", src):
    if "navpanel" in m.group(1):
        navscript = m.group(0)
assert navscript, "no nav script in the chrome - the header would be dead"

NP = '<span class="np">not published</span>'


def esc(x):
    return html.escape(x) if x else None


def region(city):
    c = (city or "").lower()
    south = ("los angeles", "san diego", "irvine", "orange", "alhambra", "azusa",
             "fullerton", "anaheim", "northridge", "long beach", "carson", "pasadena",
             "malibu", "santa barbara", "san bernardino", "redlands", "riverside",
             "loma linda", "culver city", "bakersfield", "la verne", "westwood",
             "los alamitos", "san marcos", "point loma", "calabasas", "claremont",
             "thousand oaks", "costa mesa")
    north = ("san francisco", "berkeley", "oakland", "san jose", "palo alto",
             "santa clara", "hayward", "sacramento", "rohnert park", "arcata",
             "stockton", "turlock", "chico", "belmont", "moraga", "san rafael",
             "fresno", "petaluma", "menlo park", "sunnyvale", "campbell")
    for s in south:
        if s in c:
            return "Southern California"
    for n in north:
        if n in c:
            return "Northern California"
    return "California"


SENT = {"positive": ("pos", "positive"), "negative": ("neg", "critical"),
        "mixed": ("mix", "mixed"), "info": ("inf", "informational")}


def threads_for(name):
    t = F.THREADS.get(name)
    if not t:
        return ""
    rows = "".join(
        '<a class="th %s" href="%s" target="_blank" rel="noopener noreferrer">'
        '<span class="tm">%s &middot; %s</span><b>%s</b><i>%s</i>'
        '<span class="sn">%s</span></a>'
        % (SENT[s][0], u, f, y, esc(title), esc(note), SENT[s][1])
        for u, f, title, y, s, note in t)
    return ('<details class="fx"><summary>What people say about it '
            '<span class="ct">%d</span></summary><div class="thl">%s</div></details>'
            % (len(t), rows))


def card(p):
    name = p["institution"]
    coam = ('<span class="badge acc">COAMFTE accredited</span>'
            if p.get("coamfte") else "")
    lpcc = p.get("lpcc")
    lp = ""
    if lpcc is True:
        lp = '<span class="badge lp">LPCC route too</span>'
    elif isinstance(lpcc, str):
        lp = '<span class="badge lpc">LPCC: conditional</span>'
    tu = NP
    if p.get("total"):
        tu = "$%s total" % "{:,}".format(int(p["total"]))
    elif p.get("per_unit"):
        tu = "$%s a unit" % "{:,}".format(int(p["per_unit"]))
    tyear = (' <span class="yr">%s</span>' % esc(str(p["tyear"]))) if p.get("tyear") else ""
    turl = p.get("turl") or p.get("url")
    rows = [("Degree", esc(p.get("degree")) or NP),
            ("Units", esc(p.get("units")) or NP),
            ("Length", esc(p.get("length")) or NP),
            ("Format", esc(p.get("format")) or NP),
            ("Published tuition",
             ('<a href="%s" target="_blank" rel="noopener noreferrer">%s</a>%s'
              % (turl, tu, tyear)) if tu != NP else NP)]
    body = "".join('<div class="r"><span>%s</span><b>%s</b></div>' % (k, v)
                   for k, v in rows)
    note = ""
    if p.get("notable"):
        note = '<p class="nt">%s</p>' % esc(p["notable"])
    elif p.get("note"):
        note = '<p class="nt">%s</p>' % esc(p["note"])
    return ('<article class="pg" data-name="%s" data-coamfte="%s" data-region="%s" '
            'data-tuition="%s">'
            '<div class="ph"><h3>%s</h3><span class="city">%s</span></div>'
            "%s%s"
            '<div class="bd">%s</div>%s%s'
            "%s"
            "%s</article>"
            % (esc(name).lower(), "yes" if p.get("coamfte") else "no",
               region(p.get("city")), "yes" if tu != NP else "no",
               esc(name), esc(p.get("city")) or "California",
               coam, lp, body, note, threads_for(name),
               "", cta(p)))


def cta(p):
    """Where a card sends the reader.

    A card used to carry two links: ours and the school's own. That was the
    wrong default. This directory exists because a programme's own page is
    marketing - it will not tell you that the placement is yours to find, that
    the degree does not travel out of state, or that the extension version costs
    twice the state-side one. Sending a reader straight back out to the thing
    the page exists to contextualise wasted the work.

    So where we have researched a school, the card links to our page and only to
    our page; the school's own site is linked from there, once, in context. For
    the twenty-eight where we have nothing beyond a directory row, the external
    link stays - it is the only place left to send someone, and pretending
    otherwise would be worse than an outbound link.
    """
    name = p["institution"]
    if name in SLUGS:
        return ('<a class="go mine" href="%s">Courses, curriculum, practicum '
                "and cost &rarr;</a>" % SLUGS[name])
    return ('<a class="go ext" href="%s" target="_blank" rel="noopener '
            'noreferrer">Programme page &rarr;<span class="noown">no page '
            "here yet</span></a>" % p["url"])


CSS = """<style>/* programmes */
.pd{--pine:#2C6350;--amber:#F6C560;--ink:#17271F;--line:#E2DACA;--mut:#7C8878;
  --green:#3F9577;--red:#B5483F}
.pdband{background:linear-gradient(135deg,#14261E 0%,#1B4536 48%,#2C6350 100%);
  color:#EFF5F2;padding:30px 0 36px}
.pdband .in{max-width:1180px;margin:0 auto;padding:0 26px;display:grid;
  grid-template-columns:minmax(0,1.3fr) minmax(250px,.7fr);gap:34px;align-items:center}
.pdband .bcr{display:flex;flex-wrap:wrap;align-items:center;gap:4px 8px;margin:0 0 14px;
  padding:0;list-style:none;font-family:'IBM Plex Mono',ui-monospace,monospace;
  font-size:10.4px;letter-spacing:.1em;text-transform:uppercase}
.pdband .bcr li{display:flex;align-items:center;gap:8px}
.pdband .bcr a{color:#EFF5F2;opacity:.66;text-decoration:none;padding:5px 0;min-height:26px;
  display:inline-flex;align-items:center;border-bottom:1px solid transparent}
.pdband .bcr a:hover{opacity:1;border-bottom-color:currentColor}
.pdband .bcr .sep{opacity:.36}
.pdband .bcr [aria-current]{opacity:.95;font-weight:600;color:var(--amber)}
.pdband h1{font-family:Fraunces,Georgia,serif;font-size:clamp(27px,3.7vw,43px);
  line-height:1.06;font-weight:600;letter-spacing:-.022em;color:#fff;margin:0 0 14px;max-width:18ch}
.pdband h1 em{font-style:normal;color:var(--amber)}
.pdband .dek{font-size:15.4px;line-height:1.72;color:rgba(255,255,255,.87);margin:0;max-width:57ch}
.pdmeta{display:flex;gap:14px;flex-wrap:wrap;margin-top:17px;
  font-family:'IBM Plex Mono',monospace;font-size:10.4px;letter-spacing:.06em;
  text-transform:uppercase;color:rgba(255,255,255,.62)}
.pdfig{background:rgba(0,0,0,.26);border:1px solid rgba(255,255,255,.18);border-radius:16px;
  padding:20px 22px;min-width:0}
.pdfig b{display:block;font-family:Fraunces,Georgia,serif;font-size:clamp(30px,4vw,44px);
  line-height:1;color:var(--amber)}
.pdfig span{display:block;font-size:12.5px;line-height:1.55;color:rgba(255,255,255,.74);margin-top:9px}
.pdfig .row{display:flex;justify-content:space-between;gap:10px;padding:8px 0;
  border-top:1px solid rgba(255,255,255,.14);font-size:12.2px;color:rgba(255,255,255,.8)}
.pdfig .row:first-of-type{margin-top:16px}
.pdfig .row b{display:inline;font-size:12.4px;font-family:inherit;color:#fff}

.pdwrap{max-width:1180px;margin:0 auto;padding:30px 26px 40px}
.pdlede{font-size:15.4px;line-height:1.78;color:#3B4A38;margin:0 0 18px;max-width:70ch}
.pdlede b{color:var(--ink)}
.pdlede a{color:var(--pine)}

/* filters */
.flt{position:sticky;top:0;z-index:20;background:#FBF7EE;padding:14px 0 13px;
  border-bottom:1px solid var(--line);margin-bottom:20px}
.fbar{display:flex;flex-wrap:wrap;gap:9px;align-items:center}
.fbar input[type=search]{flex:1;min-width:210px;font:inherit;font-size:14.4px;
  padding:9px 13px;border:1px solid var(--line);border-radius:9px;background:#fff;color:var(--ink)}
.fb{font-family:'IBM Plex Mono',monospace;font-size:11px;letter-spacing:.05em;
  text-transform:uppercase;background:#fff;border:1px solid var(--line);border-radius:20px;
  padding:7px 13px;cursor:pointer;color:#4A5A46}
.fb[aria-pressed=true]{background:var(--pine);border-color:var(--pine);color:#fff}
.cnt{font-family:'IBM Plex Mono',monospace;font-size:11.5px;color:var(--mut);margin-left:auto}

/* cards */
.grid{display:grid;grid-template-columns:repeat(auto-fill,minmax(330px,1fr));gap:13px}
.pg{background:#fff;border:1px solid var(--line);border-radius:12px;padding:17px 18px;min-width:0}
.pg.hide{display:none}
.ph{display:flex;justify-content:space-between;align-items:baseline;gap:10px;flex-wrap:wrap}
.pg h3{font-family:Fraunces,Georgia,serif;font-size:17px;line-height:1.22;margin:0;color:var(--ink)}
/* nowrap was right for "Northridge" and wrong for Alliant, whose city field is
   "San Diego, Irvine, Los Angeles/Alhambra, Sacramento, Online" - 400px of
   unbreakable text that pushed the page to 445px wide on a 390px phone. It is
   the only overflow on the page and it came from assuming one campus. */
.city{font-family:'IBM Plex Mono',monospace;font-size:10.4px;letter-spacing:.05em;
  text-transform:uppercase;color:var(--mut);min-width:0;overflow-wrap:anywhere;
  text-align:right}
.badge{display:inline-block;font-family:'IBM Plex Mono',monospace;font-size:9.4px;
  letter-spacing:.08em;text-transform:uppercase;border-radius:20px;padding:3px 9px;
  margin:9px 6px 0 0}
.badge.acc{background:#E0F0EA;color:#20614B;border:1px solid #BFE0D3}
.badge.lp{background:#EAF3DE;color:#27500A;border:1px solid #CFE2B8}
.badge.lpc{background:#FBF0E2;color:#8A5B22;border:1px solid #EBD9BC}
.bd{margin-top:12px;border-top:1px solid #F0EBDE;padding-top:10px}
.bd .r{display:grid;grid-template-columns:104px minmax(0,1fr);gap:10px;padding:5px 0;font-size:13px}
.bd .r span{color:var(--mut);font-family:'IBM Plex Mono',monospace;font-size:10.2px;
  letter-spacing:.06em;text-transform:uppercase;padding-top:2px}
.bd .r b{font-weight:500;color:#3B4A38;min-width:0;overflow-wrap:anywhere}
.bd .r b a{color:var(--pine)}
.np{color:#B0A896;font-style:italic}
.yr{font-family:'IBM Plex Mono',monospace;font-size:10px;color:var(--mut)}
.nt{font-size:12.6px;line-height:1.58;color:#4A5A46;margin:11px 0 0;
  border-left:2px solid #EDE7D8;padding-left:11px}
.go{display:inline-block;margin-top:13px;margin-right:16px;font-size:13px;color:var(--pine);
  text-decoration:none;border-bottom:1px solid rgba(44,99,80,.3)}
.go.mine{font-weight:600}
.go.ext{color:var(--mut);border-bottom-color:rgba(124,136,120,.3)}

/* forum threads */
.fx{margin-top:12px;border-top:1px dashed #E7E0D0;padding-top:10px}
.fx summary{cursor:pointer;font-size:12.8px;color:var(--pine);list-style:none;
  display:flex;align-items:center;gap:8px}
.fx summary::-webkit-details-marker{display:none}
.fx summary::before{content:"+";font-family:'IBM Plex Mono',monospace;color:var(--mut)}
.fx[open] summary::before{content:"\\2212"}
.fx .ct{font-family:'IBM Plex Mono',monospace;font-size:10px;background:#EFEDE4;
  color:var(--mut);border-radius:9px;padding:1px 7px}
.thl{display:grid;gap:8px;margin-top:11px}
.th{display:block;background:#FBFAF6;border:1px solid #EDE7D8;border-radius:9px;
  padding:10px 12px;text-decoration:none;min-width:0;border-left:3px solid #CFC7B4}
.th:hover{background:#fff}
.th.pos{border-left-color:var(--green)}
.th.neg{border-left-color:var(--red)}
.th.mix{border-left-color:#C98B4B}
.th.inf{border-left-color:#8FA3C4}
.tm{display:block;font-family:'IBM Plex Mono',monospace;font-size:9.8px;letter-spacing:.06em;
  text-transform:uppercase;color:var(--mut);margin-bottom:4px}
.th b{display:block;font-size:13.4px;line-height:1.35;color:var(--ink);font-weight:600;margin-bottom:4px}
.th i{display:block;font-style:normal;font-size:12.3px;line-height:1.5;color:#4A5A46}
.sn{display:inline-block;margin-top:7px;font-family:'IBM Plex Mono',monospace;font-size:9.2px;
  letter-spacing:.08em;text-transform:uppercase;color:var(--mut)}

/* general + none-found */
h2.sec{font-family:Fraunces,Georgia,serif;font-size:clamp(21px,2.5vw,27px);color:var(--ink);
  margin:46px 0 12px;padding-top:22px;border-top:1px solid var(--line)}
.gen{display:grid;grid-template-columns:repeat(auto-fill,minmax(300px,1fr));gap:10px}
.none{background:#fff;border:1px dashed #CFC7B4;border-radius:11px;padding:17px 19px;margin:14px 0}
.none b{display:block;font-family:'IBM Plex Mono',monospace;font-size:10px;letter-spacing:.11em;
  text-transform:uppercase;color:var(--mut);margin-bottom:10px}
.none p{font-size:13.4px;line-height:1.62;color:#4A5A46;margin:0 0 10px;max-width:none}
.none span{display:inline-block;font-size:12.4px;background:#F4F1E8;border-radius:20px;
  padding:3px 10px;margin:0 5px 5px 0;color:#4A5A46}
.meth{font-size:13.4px;line-height:1.7;color:#4A5A46;max-width:70ch}
.meth a{color:var(--pine)}
.empty{display:none;padding:30px;text-align:center;color:var(--mut);font-size:14.5px}

@media (max-width:820px){
  .pdband .in{grid-template-columns:minmax(0,1fr);gap:22px}
  .grid{grid-template-columns:minmax(0,1fr)}
  .cnt{margin-left:0;width:100%}
}
</style>"""

JS = """<script>
(function(){
  var q=document.getElementById('q'), cards=[].slice.call(document.querySelectorAll('.pg')),
      cnt=document.getElementById('cnt'), empty=document.getElementById('empty'),
      btns=[].slice.call(document.querySelectorAll('.fb'));
  function apply(){
    var term=(q.value||'').trim().toLowerCase();
    var on={};
    btns.forEach(function(b){ if(b.getAttribute('aria-pressed')==='true') on[b.dataset.k]=b.dataset.v; });
    var n=0;
    cards.forEach(function(c){
      var ok=true;
      for(var k in on){ if(c.dataset[k]!==on[k]) ok=false; }
      if(ok && term && c.textContent.toLowerCase().indexOf(term)<0) ok=false;
      c.classList.toggle('hide', !ok);
      if(ok) n++;
    });
    cnt.textContent = n + ' of ' + cards.length + ' programmes';
    empty.style.display = n ? 'none' : 'block';
  }
  btns.forEach(function(b){
    b.addEventListener('click', function(){
      var was=b.getAttribute('aria-pressed')==='true';
      btns.forEach(function(o){ if(o.dataset.k===b.dataset.k) o.setAttribute('aria-pressed','false'); });
      b.setAttribute('aria-pressed', was?'false':'true');
      apply();
    });
  });
  q.addEventListener('input', apply);
  apply();
})();
</script>"""


def build():
    progs = sorted(PROGRAMS, key=lambda p: p["institution"])
    n_coam = sum(1 for p in progs if p.get("coamfte"))
    n_tui = sum(1 for p in progs if p.get("per_unit") or p.get("total"))
    n_forum = len(F.THREADS)

    cards = "".join(card(p) for p in progs)

    # Threads keyed to an institution that is not in the BBS list - Saybrook is
    # one - would otherwise be silently dropped, taking verified research with
    # them. They join the general section rather than disappearing, and the
    # guard below still insists every gathered URL appears somewhere.
    known = {x["institution"] for x in PROGRAMS}
    orphan = [t for k, v in F.THREADS.items() if k not in known for t in v]

    gen = "".join(
        '<a class="th %s" href="%s" target="_blank" rel="noopener noreferrer">'
        '<span class="tm">%s &middot; %s</span><b>%s</b><i>%s</i>'
        '<span class="sn">%s</span></a>'
        % (SENT[s][0], u, f, y, esc(t), esc(note), SENT[s][1])
        for u, f, t, y, s, note in F.GENERAL + orphan)

    none_found = "".join("<span>%s</span>" % esc(x) for x in F.NONE_FOUND)

    fig = ('<div class="pdfig"><b>%d</b><span>institutions whose degrees the Board '
           "lists as qualifying towards California LMFT licensure</span>"
           '<div class="row"><span>COAMFTE accredited</span><b>%d</b></div>'
           '<div class="row"><span>Publish their tuition</span><b>%d</b></div>'
           '<div class="row"><span>With real forum discussion</span><b>%d</b></div>'
           "</div>" % (len(progs), n_coam, n_tui, n_forum))

    return """<!doctype html>
<html lang="en"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>California MFT graduate programmes: %d schools, what each publishes, and what people say</title>
<meta name="description" content="Every California graduate programme leading to LMFT licensure — degree, units, length, format, COAMFTE accreditation, LPCC eligibility and published tuition, with links to real forum discussion for each. No rankings, and no estimated tuition.">
<link rel="canonical" href="https://cavatello.github.io/therapist-tools/mft-programs-california.html">
%s
%s
%s
</head><body class="pd">
%s
<main>
<section class="pdband"><div class="in"><div>
<ol class="bcr" aria-label="Breadcrumb">
<li><a href="index.html">Therapist Support</a><span class="sep">&rsaquo;</span></li>
<li><a href="resources.html">Resources</a><span class="sep">&rsaquo;</span></li>
<li><span aria-current="page">MFT programmes</span></li></ol>
<h1>Every California programme that leads to <em>an MFT licence</em>.</h1>
<p class="dek">What each one publishes about itself &mdash; degree, units, length, format,
accreditation and cost &mdash; next to what students and graduates actually say about it
in public. No rankings. No estimated tuition.</p>
<div class="pdmeta"><span>California</span><span>Updated %s</span><span>%d institutions</span></div>
</div>%s</div></section>

<div class="pdwrap">
<p class="pdlede">The Board keeps a list of institutions whose degrees <b>may</b> qualify
&mdash; its own word &mdash; and the statute reserves the Board the final say regardless
of any accreditation. So treat this as a starting point for your own checking, not as an
approval. <a href="become-an-mft-california.html">What the degree has to contain is on the
licensure page &rarr;</a></p>
<p class="pdlede"><b>One filter matters more than the rest.</b> COAMFTE accreditation is
what decides whether your degree travels: inside California a BBS-approved,
regionally-accredited programme is fine, and outside it a non-COAMFTE degree can mean
remedial coursework or no licence at all. <b>%d of the %d</b> hold it.</p>

%s

<div class="flt"><div class="fbar">
<input type="search" id="q" placeholder="Search school, city, degree or format&hellip;"
       aria-label="Search programmes">
<button class="fb" data-k="coamfte" data-v="yes" aria-pressed="false">COAMFTE only</button>
<button class="fb" data-k="region" data-v="Southern California" aria-pressed="false">Southern CA</button>
<button class="fb" data-k="region" data-v="Northern California" aria-pressed="false">Northern CA</button>
<button class="fb" data-k="tuition" data-v="yes" aria-pressed="false">Publishes tuition</button>
<span class="cnt" id="cnt"></span>
</div></div>

<div class="grid">%s</div>
<div class="empty" id="empty">Nothing matches that. Clear a filter or try a shorter search.</div>

<h2 class="sec">Threads about the decision itself</h2>
<p class="pdlede">Not about one school &mdash; about accreditation, debt, practicum risk
and whether the route is worth walking at all.</p>
<div class="gen thl">%s</div>

<h2 class="sec">What is not here</h2>
<div class="none"><b>Institutions with no credible discussion found</b>
<p>Searched by every name variant across Reddit, Student Doctor Network and The GradCafe.
Silence is not a verdict &mdash; several of these are small, and two have closed &mdash;
but a missing link should not read as an endorsement, so they are named.</p>
%s
<p style="margin-top:12px">%s</p></div>

<h2 class="sec">How this was built</h2>
<p class="meth"><b>Tuition is never estimated.</b> Twenty-one institutions publish a
per-unit or total figure and it is shown with the year and a link to the page it came
from. The other forty-four say <i>not published</i>. A prospective student comparing a
$42,000 programme against a $152,000 one deserves to know which figure came from the
institution and which came from me. None came from me.</p>
<p class="meth"><b>Nothing is ranked.</b> There is no score, no stars and no best-of. The
one comparative fact that is objective is COAMFTE accreditation, and it is a filter
rather than a verdict.</p>
<p class="meth"><b>Every forum link was verified to resolve</b> on %s, against the host's
own endpoint rather than constructed from a thread ID. Descriptions are mine; nothing is
quoted beyond a phrase. Sentiment tags are my reading of the thread, not a measurement.</p>
<p class="meth">Accreditation status is from the
<a href="https://coamfte.org/COAMFTE/Directory_of_Accredited_Programs/MFT_Training_Programs.aspx"
   target="_blank" rel="noopener noreferrer">COAMFTE directory</a>; the institution list is
from the
<a href="https://www.bbs.ca.gov/applicants/education_resources.html"
   target="_blank" rel="noopener noreferrer">BBS education resources page</a>. Everything
else is from each institution's own site. If something here is wrong,
<a href="contact.html">tell me</a> &mdash; that is what the page is for.</p>
</div>
</main>
%s
%s
%s
</body></html>""" % (len(progs), "\n".join(links), "\n".join(styles), CSS + charts.CSS, header,
                     UPDATED, len(progs), fig, n_coam, len(progs), charts.render(progs),
                     cards, gen,
                     none_found, F.DEAD_SUBS, UPDATED, footer, navscript, JS)


def main():
    doc = build()
    open(OUT, "w", encoding="utf-8").write(doc)

    bad = []
    if doc.count("<h1") != 1:
        bad.append("%d h1" % doc.count("<h1"))
    n = doc.count('<article class="pg"')
    if n != len(PROGRAMS):
        bad.append("%d cards for %d programmes" % (n, len(PROGRAMS)))
    # Every card must lead somewhere. Which somewhere depends on whether we
    # researched the school: ours if we did, the institution's own page if we
    # did not. A card with neither is a dead end and the reader has no next
    # move at all.
    for p in PROGRAMS:
        nm = p["institution"]
        if nm in SLUGS:
            if ('href="%s"' % SLUGS[nm]) not in doc:
                bad.append("no internal link for %s" % nm[:30])
        elif p["url"] not in doc:
            bad.append("no link at all for %s" % nm[:30])
    # A researched school must not still be pushed straight back out to its own
    # marketing from the directory - that is the behaviour this change removed,
    # and it would come back silently if cta() were ever edited carelessly.
    for nm, sl in SLUGS.items():
        pr = next((x for x in PROGRAMS if x["institution"] == nm), None)
        if pr and ('class="go ext" href="%s"' % pr["url"]) in doc:
            bad.append("%s has a page but the card still links out" % nm[:30])
    # every forum thread must be present and open in a new window
    allt = [t for v in F.THREADS.values() for t in v] + F.GENERAL
    for u, *_ in allt:
        if u not in doc:
            bad.append("missing thread %s" % u[:52])
    for m in re.finditer(r'<a class="th [^"]*" href="[^"]+"([^>]*)>', doc):
        if 'target="_blank"' not in m.group(1) or "noopener" not in m.group(1):
            bad.append("a forum link does not open safely in a new window")
            break
    # tuition honesty: the count of "not published" must equal the count of
    # programmes with no published figure, times the fields that can carry it
    have = sum(1 for p in PROGRAMS if p.get("per_unit") or p.get("total"))
    if doc.count("not published") < (len(PROGRAMS) - have):
        bad.append("fewer 'not published' cells than programmes without tuition")
    if "navpanel" in doc and not re.search(r"<script>[\s\S]*?navpanel[\s\S]*?</script>", doc):
        bad.append("header would be dead - nav script missing")
    # Look for ranking MARKUP, not for the word. The first version matched
    # "no best-of" in the page's own methodology note and refused to ship a
    # page for saying it does not rank.
    # The accreditation count appears in prose AND in the hero figure. A
    # hardcoded "eleven" in the copy went stale the moment a twelfth accredited
    # institution entered the data, which is exactly how a page that insists on
    # cited figures ends up carrying an uncited one.
    n_acc = sum(1 for p in PROGRAMS if p.get("coamfte"))
    if ("<b>%d of the %d</b>" % (n_acc, len(PROGRAMS))) not in doc:
        bad.append("the accreditation count in the copy does not match the data")
    if re.search(r'class="[^"]*\b(rank|score|stars?)\b', doc) \
       or re.search(r"\branked\s+#?\d", doc, re.I) \
       or re.search(r"\btop\s+\d+\s+(programmes?|programs?|schools?)", doc, re.I):
        bad.append("the page appears to rank something")
    for name, sl in SLUGS.items():
        if ('href="%s"' % sl) not in doc:
            bad.append("school page built but not linked: %s" % sl)
    if bad:
        sys.exit("build_programs: " + "; ".join(bad))

    print("%-40s %d bytes  %d programmes  %d COAMFTE  %d with tuition  %d threads"
          % (os.path.basename(OUT), len(doc), len(PROGRAMS),
             sum(1 for p in PROGRAMS if p.get("coamfte")), have, len(allt)))


if __name__ == "__main__":
    main()
