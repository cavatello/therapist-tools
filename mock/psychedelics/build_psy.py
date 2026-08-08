#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Build the psychedelic-assisted therapy training section.

One hub and sixteen programme pages, from the research in data/.

WHY THIS SECTION EXISTS AND WHAT IT IS FOR. A California therapist looking at
these trainings is looking at $1,000 to $15,000 and up to two years, and the
single question every one of them is actually asking - "when I finish this,
what am I allowed to do?" - is the question the programmes themselves answer
least clearly. Almost none of them changes a licence or a scope of practice.
Two of the fifty United States have a legal framework in which a facilitator
credential does anything at all, and California is not one of them.

So the organising device of every page here is a ledger: what the certificate
lets you do, and what it does not. It runs before the curriculum, before the
faculty and before the cost, because a reader who stops after the first screen
should still leave with the thing that matters.

THE LEDGER IS BUILT FROM RESEARCH, NOT FROM A TEMPLATE. Each `can` and `cannot`
line was established per programme against that programme's own materials and
against the two state registers - Oregon Health Authority's approved-curriculum
list and Colorado DORA's - which is why the state-approval badge is a fact and
not a claim. Where a programme markets an approval it does not hold, or holds
one it does not market, the page says so.

NOTHING HERE IS A RECOMMENDATION. There is no scoring and no ordering by
quality. Programmes sort by cost, which is the only axis on which they are
objectively comparable, and the sort is disclosed.
"""
import os, re, sys, json, html

HERE = os.path.dirname(os.path.abspath(__file__))
DATA = os.path.join(HERE, "data")
OUT = os.path.join(HERE, "out")
CHROME = os.path.join(os.path.dirname(HERE), "mftguide", "_chrome.html")
UPDATED = "6 August 2026"
HUB = "psychedelic-therapy-training-california.html"
SITE = "https://therapistsupport.org/"

FEATURED = "ciis-psychedelic-assisted-therapies"


def esc(x):
    return html.escape(str(x)) if x is not None else ""


def slugfile(s):
    return "psychedelic-training-%s.html" % s


# ---------------------------------------------------------------- data

LAND = json.load(open(os.path.join(DATA, "_landscape.json"), encoding="utf-8"))
PROGS = []
for f in sorted(os.listdir(DATA)):
    if f.endswith(".json") and not f.startswith("_"):
        try:
            PROGS.append(json.load(open(os.path.join(DATA, f), encoding="utf-8")))
        except ValueError:
            sys.exit("build_psy: data/%s is not valid JSON" % f)
assert PROGS, "no programme records"
BY = {p["slug"]: p for p in PROGS}
assert FEATURED in BY, "the featured programme has no record"


def cost_num(p):
    c = p.get("cost") or {}
    return c.get("amount")


def cost_str(p):
    c = p.get("cost") or {}
    if not c.get("amount"):
        return None
    cur = {"USD": "$", "EUR": "€", "GBP": "£"}.get(c.get("currency"), "")
    return "%s%s" % (cur, "{:,}".format(int(c["amount"])))


# Programmes sort by cost because that is the one axis on which they compare
# objectively. Records with no published figure go last rather than to zero -
# a missing price is not a cheap one, and sorting it to the front would read as
# a recommendation.
ORDER = sorted(PROGS, key=lambda p: (cost_num(p) is None, cost_num(p) or 0))


# ---------------------------------------------------------------- chrome

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


src = open(CHROME, encoding="utf-8").read()
head_end = src.find("</head>")
LINKS = "\n".join(m.group(0) for m in re.finditer(r"<link\b[^>]*>", src[:head_end])
                  if 'rel="stylesheet"' in m.group(0) or "fonts." in m.group(0)
                  or 'rel="preconnect"' in m.group(0))
STYLES = "\n".join(re.findall(r"<style>.*?</style>", src, re.S))
assert STYLES, "no stylesheet lifted"
_h = balanced(src, "header")
HEADER = re.sub(r'(<a href="[^"]*") class="on"', r"\1", src[_h[0]:_h[1]])
_f = balanced(src, "footer")
FOOTER = re.sub(r'(<a href="[^"]*") class="on"', r"\1", src[_f[0]:_f[1]])
NAVSCRIPT = ""
for m in re.finditer(r"<script>([\s\S]*?)</script>", src):
    if "navpanel" in m.group(1):
        NAVSCRIPT = m.group(0)
assert NAVSCRIPT, "no nav script in the chrome - the header would be dead"


# ---------------------------------------------------------------- components

YT = re.compile(r"(?:v=|youtu\.be/|embed/)([A-Za-z0-9_-]{11})")


def video_block(v):
    """Click-to-load facade. See the note in mftguide/depth_render.py - the
    reasoning is the same and deliberately duplicated rather than shared, so
    that neither section can silently change the other's privacy behaviour."""
    if not v or not v.get("url"):
        return ""
    m = YT.search(v["url"])
    if not m:
        return ""
    vid = m.group(1)
    return ('<figure class="vfig"><button class="vplay" type="button" '
            'data-yt="%s" aria-label="Play video: %s">'
            '<img src="https://i.ytimg.com/vi/%s/hqdefault.jpg" alt="" '
            'loading="lazy" width="480" height="360">'
            '<span class="vbtn" aria-hidden="true"></span></button>'
            '<figcaption><b>%s</b><span>%s</span>'
            '<span class="vmeta">%s &middot; nothing loads from YouTube until '
            "you press play</span></figcaption></figure>"
            % (vid, esc(v.get("title", "")), vid, esc(v.get("title", "")),
               esc(v.get("why", "")), esc(v.get("who", ""))))


def ledger(sc, name):
    """The can / cannot ledger. The centre of gravity of every page here."""
    if not sc:
        return ""
    can = sc.get("can") or []
    cannot = sc.get("cannot") or []
    if not can and not cannot:
        return ""
    lic = sc.get("changes_license")
    head = ('<div class="lic %s"><b>%s</b><span>%s</span></div>'
            % ("no" if lic is False else "yes",
               "This does not change your licence or your scope of practice"
               if lic is False else "This affects your licence or scope",
               "It is a credential from a school, not from a regulator. "
               "California&rsquo;s Board of Behavioral Sciences neither "
               "recognises nor requires it, and holding it adds nothing to what "
               "you may lawfully do as an LMFT in this state."
               if lic is False else
               "Read the detail below carefully before enrolling."))
    cols = []
    if can:
        cols.append('<div class="lcol can"><b>With this you can</b><ul>%s</ul></div>'
                    % "".join("<li>%s</li>" % esc(x) for x in can))
    if cannot:
        cols.append('<div class="lcol cant"><b>You still cannot</b><ul>%s</ul></div>'
                    % "".join("<li>%s</li>" % esc(x) for x in cannot))
    dis = ""
    if sc.get("disclaimer_quote"):
        dis = ('<blockquote class="disq">%s<span>&mdash; %s, in its own '
               "materials</span></blockquote>"
               % (esc(sc["disclaimer_quote"]), esc(name)))
    return head + '<div class="ledg">%s</div>' % "".join(cols) + dis


def state_badges(sc, small=False):
    if not sc:
        return ""
    out = []
    for key, state in (("or_licensure", "Oregon"), ("co_licensure", "Colorado")):
        v = (sc.get(key) or "").lower()
        if v == "yes":
            out.append('<span class="sb ok">%s approved</span>' % state)
        elif v == "no":
            out.append('<span class="sb no">Not %s approved</span>' % state)
    return "".join(out)


def modules(cur):
    if not cur:
        return ""
    return '<ol class="mods">%s</ol>' % "".join(
        '<li><b>%s</b><p>%s</p>%s</li>'
        % (esc(m.get("module") or ""), esc(m.get("detail") or ""),
           ('<a class="srcl" href="%s" target="_blank" rel="noopener '
            'noreferrer">source &nearr;</a>' % esc(m["src"])) if m.get("src") else "")
        for m in cur)


SENT = {"positive": "pos", "negative": "neg", "mixed": "mix", "info": "inf"}


def voices(vx):
    if not vx:
        return ""
    out = []
    for v in vx:
        cls = SENT.get(v.get("sentiment"), "inf")
        inner = ('<i>%s</i><span class="vwho">%s</span>'
                 % (esc(v.get("text") or ""), esc(v.get("who") or "")))
        if v.get("url"):
            out.append('<a class="vox %s" href="%s" target="_blank" '
                       'rel="noopener noreferrer">%s</a>' % (cls, esc(v["url"]), inner))
        else:
            out.append('<div class="vox %s">%s</div>' % (cls, inner))
    return '<div class="voxl">%s</div>' % "".join(out)


def srclist(sources, label="Sources for this page"):
    if not sources:
        return ""
    return ('<details class="srcs"><summary>%s (%d)</summary><ol>%s</ol></details>'
            % (label, len(sources),
               "".join('<li><a href="%s" target="_blank" rel="noopener '
                       'noreferrer">%s</a></li>'
                       % (esc(s.get("url") or ""), esc(s.get("label") or s.get("url")))
                       for s in sources if s.get("url"))))


def gaplist(gs):
    if not gs:
        return ""
    return ("<p>These are the things I looked for and could not establish. Take "
            "them to the programme, and notice how quickly and precisely they "
            'answer.</p><ul class="gapl">%s</ul>'
            % "".join("<li>%s</li>" % esc(g) for g in gs))


def page(title, desc, canon, band, nav, body, cls="px"):
    return """<!doctype html>
<html lang="en"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>%s</title>
<meta name="description" content="%s">
<link rel="canonical" href="%s%s">
%s
%s
%s
</head><body class="%s">
%s
<main>
%s
<div class="pxwrap">%s<article class="pxbody">%s</article></div>
</main>
%s
%s
%s
</body></html>""" % (esc(title), esc(desc), SITE, canon, LINKS, STYLES, CSS,
                     cls, HEADER, band, nav, body, FOOTER, NAVSCRIPT, JS)


# ---------------------------------------------------------------- programme page

def prog_page(p):
    sc = p.get("scope") or {}
    cst = cost_str(p)
    secs = []

    summ = "".join("<p>%s</p>" % esc(x) for x in (p.get("summary") or []))
    if summ:
        secs.append(("what-it-is", "What it is", summ +
                     '<p><a href="%s" target="_blank" rel="noopener noreferrer">'
                     "The programme&rsquo;s own page &rarr;</a></p>" % esc(p["url"])))

    vb = video_block(p.get("video"))
    if vb:
        secs.append(("watch", "See it and hear it", vb))

    led = ledger(sc, p.get("org") or p.get("name"))
    if led:
        secs.append(("what-it-lets-you-do", "What it lets you do",
                     "<p>This is the section the programme&rsquo;s own marketing "
                     "is least specific about, so it runs before everything "
                     "else. It was established against the programme&rsquo;s own "
                     "materials and against the two state registers that matter "
                     "&mdash; Oregon&rsquo;s approved-curriculum list and "
                     "Colorado&rsquo;s.</p>" + led +
                     '<p><a href="%s#the-law">Why the answer is this narrow '
                     "&rarr;</a></p>" % HUB))

    rows = []
    for label, val in (("Cost", (p.get("cost") or {}).get("note") or cst),
                       ("Length", p.get("length")),
                       ("Hours", p.get("hours")),
                       ("Format", p.get("format")),
                       ("Where", p.get("location")),
                       ("Who can apply", p.get("eligibility"))):
        if val:
            rows.append('<div class="r"><span>%s</span><b>%s</b></div>'
                        % (label, esc(val)))
    if rows:
        secs.append(("the-detail", "Cost, length and who can apply",
                     '<div class="tbl">%s</div>' % "".join(rows) +
                     ('<p>%s</p>' % ('<a class="srcl" href="%s" target="_blank" '
                                     'rel="noopener noreferrer">cost source &nearr;</a>'
                                     % esc((p.get("cost") or {}).get("src")))
                      if (p.get("cost") or {}).get("src") else "")))

    mods = modules(p.get("curriculum"))
    if mods:
        secs.append(("curriculum", "What you would study", mods))

    fac = p.get("faculty") or []
    if fac:
        secs.append(("faculty", "Who teaches it",
                     "<p>Faculty is a large part of what these programmes "
                     "actually sell, and it changes between cohorts &mdash; "
                     "check the current list before you decide on this "
                     'basis.</p><ul class="facl">%s</ul>'
                     % "".join("<li>%s</li>" % esc(f) for f in fac)))

    vx = voices(p.get("voices"))
    if vx:
        secs.append(("what-people-say", "What people say about it",
                     "<p>Quoted with the source attached in every case, "
                     "including the programme&rsquo;s own claims about itself "
                     "&mdash; which are labelled as such &mdash; and the "
                     "critical ones.</p>" + vx))

    if p.get("status_2026"):
        secs.append(("status", "Where it stands right now",
                     "<p>%s</p>" % esc(p["status_2026"])))

    tail = gaplist(p.get("gaps")) + srclist(p.get("sources"))
    if tail:
        secs.append(("what-i-could-not-find", "What I could not establish", tail))

    secs.append(("next", "Where to go next",
                 '<div class="nxt">'
                 '<a class="nx" href="%s"><b>All %d trainings</b><span>Compared '
                 "on cost, modality and whether the credential does anything in "
                 "a regulated market</span></a>"
                 '<a class="nx" href="%s#the-law"><b>The law as it stands</b>'
                 "<span>What a California therapist may and may not do with "
                 "psychedelics today</span></a>"
                 '<a class="nx" href="mft-programs-california.html"><b>MFT '
                 "programmes</b><span>The degree that comes first, if you are "
                 "not licensed yet</span></a></div>" % (HUB, len(PROGS), HUB)))

    nav = '<nav class="pxnav"><b>On this page</b>%s</nav>' % "".join(
        '<a href="#%s">%s</a>' % (i, t) for i, t, _b in secs)
    body = "".join('<h2 id="%s">%s</h2>%s' % (i, t, b) for i, t, b in secs)

    figrows = []
    if p.get("length"):
        figrows.append(("Length", esc(p["length"])[:40]))
    figrows.append(("Changes your licence",
                    "no" if sc.get("changes_license") is False else "see below"))
    fig = ('<div class="pxfig"><b>%s</b><span>%s</span>%s</div>'
           % (cst or "not published",
              "published cost" if cst else "the programme publishes no figure",
              "".join('<div class="row"><span>%s</span><b>%s</b></div>' % r
                      for r in figrows)))

    band = """<section class="pxband"><div class="in"><div>
<ol class="bcr" aria-label="Breadcrumb">
<li><a href="index.html">Therapist Support</a><span class="sep">&rsaquo;</span></li>
<li><a href="%s">Psychedelic training</a><span class="sep">&rsaquo;</span></li>
<li><span aria-current="page">%s</span></li></ol>
<p class="sub">%s</p>
<h1>%s</h1>
<p class="dek">%s</p>
<div class="pxmeta"><span>Updated %s</span>%s</div>
</div>%s</div></section>""" % (
        HUB, esc(p["name"])[:46], esc(p.get("org") or ""), esc(p["name"]),
        esc(p.get("one_line") or ""), UPDATED, state_badges(sc), fig)

    return page(
        "%s — %s: cost, curriculum, and what the certificate actually lets you do"
        % (esc(p["name"]), esc(p.get("org") or "")),
        "%s — what it costs, what you would study, and exactly what a "
        "California-licensed therapist can and cannot do with it."
        % esc(p.get("one_line") or p["name"])[:150],
        slugfile(p["slug"]), band, nav, body)


# ---------------------------------------------------------------- hub

def hub_card(p, featured=False):
    sc = p.get("scope") or {}
    cst = cost_str(p)
    mods = ", ".join(p.get("modality") or [])
    return ('<article class="pcard%s" data-cost="%s" data-or="%s">'
            '<div class="ph"><h3><a href="%s">%s</a></h3>'
            '<span class="org">%s</span></div>'
            '<p class="one">%s</p>'
            '<div class="pmeta"><span class="cost">%s</span>%s</div>'
            '%s<a class="go" href="%s">Cost, curriculum and what it lets you do '
            "&rarr;</a></article>"
            % (" feat" if featured else "", cost_num(p) or "",
               (sc.get("or_licensure") or "unknown"),
               slugfile(p["slug"]), esc(p["name"]), esc(p.get("org") or ""),
               esc(p.get("one_line") or ""),
               esc(cst or "no published figure"), state_badges(sc),
               ('<p class="mods">%s</p>' % esc(mods)) if mods else "",
               slugfile(p["slug"])))


def law_section(s):
    facts = ""
    if s.get("facts"):
        facts = '<div class="fx">%s</div>' % "".join(
            '<div class="f"><span>%s</span><b>%s</b>%s</div>'
            % (esc(f.get("label")), esc(f.get("value")),
               ('<a class="srcl" href="%s" target="_blank" rel="noopener '
                'noreferrer">source &nearr;</a>' % esc(f["src"])) if f.get("src") else "")
            for f in s["facts"])
    return ('<details class="law" id="law-%s"><summary><b>%s</b>'
            '<span>%d facts, %d sources</span></summary><div class="lawb">%s%s%s</div>'
            "</details>"
            % (esc(s.get("id")), esc(s.get("title")),
               len(s.get("facts") or []), len(s.get("sources") or []),
               "".join("<p>%s</p>" % esc(x) for x in (s.get("paras") or [])),
               facts, srclist(s.get("sources"), "Sources")))


def hub():
    feat = BY[FEATURED]
    secs = []

    bl = LAND.get("bottom_line") or []
    secs.append(("start-here", "Start here", (
        "<p>There are sixteen trainings on this page and they range from "
        "$1,047 to &euro;15,000. Before any of that matters, one thing has to "
        "be said plainly, because almost none of these programmes says it on "
        "its own homepage.</p>"
        '<div class="lic no"><b>None of these certificates changes your licence '
        "or your scope of practice</b><span>They are credentials issued by "
        "schools and institutes, not by regulators. California&rsquo;s Board of "
        "Behavioral Sciences does not recognise, require or register any of "
        "them, and holding one adds nothing to what you may lawfully do as an "
        "LMFT in this state.</span></div>"
        "<p>What they do give you is training, a peer network, in some cases "
        "continuing-education credit that counts toward renewal, and standing "
        "with the clinics that hire for this work. Two of them &mdash; and only "
        "two categories of them &mdash; lead to something a state actually "
        "issues, and neither state is California.</p>"
        + ('<ul class="bl">%s</ul>' % "".join("<li>%s</li>" % esc(x) for x in bl)
           if bl else "")
        + '<p><a href="#the-law">The whole legal picture, with sources '
          "&rarr;</a></p>")))

    secs.append(("featured", "The one most Californians are looking at",
                 hub_card(feat, featured=True) +
                 video_block(feat.get("video")) +
                 ledger(feat.get("scope"), feat.get("org") or feat["name"]) +
                 '<p><a href="%s">Everything about the CIIS certificate '
                 "&rarr;</a></p>" % slugfile(feat["slug"])))

    others = [p for p in ORDER if p["slug"] != FEATURED]
    secs.append(("every-training", "Every training, cheapest first",
                 "<p>Sorted by published cost, because it is the one axis on "
                 "which these compare objectively. That is a sort, not a "
                 "ranking &mdash; nothing here is scored, and the cheapest "
                 "is not the best. Programmes that publish no figure are last, "
                 "not first; a missing price is not a low one.</p>"
                 '<div class="pgrid">%s</div>'
                 % "".join(hub_card(p) for p in others)))

    secs.append(("the-law", "The law, as it actually stands",
                 "<p>Eight areas, every claim tied to a statute, regulation, "
                 "agency page or filing. Collapsed because most readers need "
                 "one of these, not all eight. Verified %s &mdash; this is the "
                 "fastest-moving area on this site, so check the sources rather "
                 "than trusting the date.</p>%s"
                 % (esc(LAND.get("updated") or UPDATED),
                    "".join(law_section(s) for s in LAND.get("sections") or []))))

    if LAND.get("gaps"):
        secs.append(("open-questions", "What is still unresolved",
                     gaplist(LAND["gaps"])))

    secs.append(("next", "Where to go next",
                 '<div class="nxt">'
                 '<a class="nx" href="mft-programs-california.html"><b>MFT '
                 "programmes in California</b><span>All 65, with courses, "
                 "curriculum, practicum and cost for 37 of them</span></a>"
                 '<a class="nx" href="become-an-mft-california.html"><b>Getting '
                 "licensed</b><span>Every requirement, with the code section it "
                 "comes from</span></a>"
                 '<a class="nx" href="resources.html"><b>Everything else</b>'
                 "<span>The rest of the tools and reference on this "
                 "site</span></a></div>"))

    nav = '<nav class="pxnav"><b>On this page</b>%s</nav>' % "".join(
        '<a href="#%s">%s</a>' % (i, t) for i, t, _b in secs)
    body = "".join('<h2 id="%s">%s</h2>%s' % (i, t, b) for i, t, b in secs)

    n_or = sum(1 for p in PROGS if (p.get("scope") or {}).get("or_licensure") == "yes")
    fig = ('<div class="pxfig"><b>%d</b><span>trainings researched, with cost, '
           "curriculum and scope for each</span>"
           '<div class="row"><span>Change your licence</span><b>none</b></div>'
           '<div class="row"><span>Oregon-approved</span><b>%d</b></div>'
           '<div class="row"><span>Legal in California</span><b>ketamine only</b>'
           "</div></div>" % (len(PROGS), n_or))

    band = """<section class="pxband"><div class="in"><div>
<ol class="bcr" aria-label="Breadcrumb">
<li><a href="index.html">Therapist Support</a><span class="sep">&rsaquo;</span></li>
<li><a href="resources.html">Resources</a><span class="sep">&rsaquo;</span></li>
<li><span aria-current="page">Psychedelic training</span></li></ol>
<p class="sub">For California-licensed therapists and associates</p>
<h1>Psychedelic-assisted therapy training, and <em>what a certificate
actually gets you</em>.</h1>
<p class="dek">Sixteen trainings, from $1,047 to &euro;15,000, with what each
costs, what you would study, and &mdash; the part none of them leads with
&mdash; exactly what you may and may not do afterwards as a therapist licensed
in California.</p>
<div class="pxmeta"><span>California</span><span>Updated %s</span>
<span>%d programmes</span></div>
</div>%s</div></section>""" % (UPDATED, len(PROGS), fig)

    return page(
        "Psychedelic-assisted therapy training for California therapists: "
        "16 programmes, what each costs, and what the certificate lets you do",
        "Every major psychedelic-assisted therapy training a California LMFT "
        "can take — CIIS, MIND, Polaris, Fluence, InnerTrek, Naropa and more "
        "— with cost, curriculum, and a plain account of what each "
        "certificate does and does not authorise under California law.",
        HUB, band, nav, body)


# ---------------------------------------------------------------- css / js

CSS = """<style>/* psychedelic training */
.px{--pine:#2C6350;--amber:#F6C560;--ink:#17271F;--line:#E2DACA;--mut:#7C8878;
  --green:#3F9577;--red:#B5483F}
.pxband{background:linear-gradient(135deg,#14261E 0%,#1B4536 48%,#2C6350 100%);
  color:#EFF5F2;padding:30px 0 36px}
.pxband .in{max-width:1180px;margin:0 auto;padding:0 26px;display:grid;
  grid-template-columns:minmax(0,1.3fr) minmax(250px,.7fr);gap:34px;align-items:center}
.pxband .bcr{display:flex;flex-wrap:wrap;align-items:center;gap:4px 8px;margin:0 0 14px;
  padding:0;list-style:none;font-family:'IBM Plex Mono',ui-monospace,monospace;
  font-size:10.4px;letter-spacing:.1em;text-transform:uppercase}
.pxband .bcr li{display:flex;align-items:center;gap:8px}
.pxband .bcr a{color:#EFF5F2;opacity:.66;text-decoration:none;padding:5px 0;min-height:26px;
  display:inline-flex;align-items:center;border-bottom:1px solid transparent}
.pxband .bcr a:hover{opacity:1;border-bottom-color:currentColor}
.pxband .bcr .sep{opacity:.36}
.pxband .bcr [aria-current]{opacity:.95;font-weight:600;color:var(--amber)}
.pxband h1{font-family:Fraunces,Georgia,serif;font-size:clamp(25px,3.3vw,38px);
  line-height:1.08;font-weight:600;letter-spacing:-.02em;color:#fff;margin:0 0 12px;
  max-width:22ch}
.pxband h1 em{font-style:normal;color:var(--amber)}
.pxband .sub{font-family:'IBM Plex Mono',monospace;font-size:11px;letter-spacing:.11em;
  text-transform:uppercase;color:var(--amber);margin:0 0 12px}
.pxband .dek{font-size:15.2px;line-height:1.72;color:rgba(255,255,255,.87);margin:0;
  max-width:58ch}
.pxmeta{display:flex;gap:10px;flex-wrap:wrap;align-items:center;margin-top:17px;
  font-family:'IBM Plex Mono',monospace;font-size:10.4px;letter-spacing:.06em;
  text-transform:uppercase;color:rgba(255,255,255,.62)}
.pxfig{background:rgba(0,0,0,.26);border:1px solid rgba(255,255,255,.18);
  border-radius:16px;padding:20px 22px;min-width:0}
.pxfig>b{display:block;font-family:Fraunces,Georgia,serif;font-size:clamp(26px,3.4vw,38px);
  line-height:1.05;color:var(--amber);overflow-wrap:anywhere}
.pxfig>span{display:block;font-size:12.4px;line-height:1.55;color:rgba(255,255,255,.74);
  margin-top:9px}
.pxfig .row{display:flex;justify-content:space-between;gap:10px;padding:8px 0;
  border-top:1px solid rgba(255,255,255,.14);font-size:12.1px;color:rgba(255,255,255,.8)}
.pxfig .row:first-of-type{margin-top:16px}
.pxfig .row b{font-size:12.3px;color:#fff;text-align:right}

.pxwrap{max-width:1180px;margin:0 auto;padding:32px 26px 20px;display:grid;
  grid-template-columns:214px minmax(0,1fr);gap:38px;align-items:start}
.pxnav{position:sticky;top:16px;min-width:0}
.pxnav b{display:block;font-family:'IBM Plex Mono',monospace;font-size:10px;
  letter-spacing:.13em;text-transform:uppercase;color:var(--mut);margin-bottom:11px}
.pxnav a{display:block;font-size:13px;line-height:1.42;color:#4A5A46;text-decoration:none;
  padding:6px 0 6px 12px;border-left:2px solid var(--line)}
.pxnav a:hover{color:var(--ink);border-left-color:#B9AE93}
.pxnav a.on{color:var(--pine);border-left-color:var(--pine);font-weight:600}
.pxbody{min-width:0}
.pxbody h2{font-family:Fraunces,Georgia,serif;font-size:clamp(20px,2.4vw,26px);
  line-height:1.2;font-weight:600;color:var(--ink);margin:42px 0 13px;scroll-margin-top:20px}
.pxbody h2:first-child{margin-top:0}
.pxbody p{font-size:15.2px;line-height:1.78;color:#3B4A38;margin:0 0 15px;max-width:68ch}
.pxbody a{color:var(--pine)}

.lic{border-radius:12px;padding:18px 20px;margin:6px 0 18px;border:1px solid}
.lic.no{background:#F2F8F1;border-color:#CFE3CB;border-left:4px solid var(--green)}
.lic.yes{background:#FBF0E2;border-color:#EBD9BC;border-left:4px solid #C98B4B}
.lic b{display:block;font-family:Fraunces,Georgia,serif;font-size:18.5px;
  line-height:1.28;color:var(--ink);margin-bottom:7px}
.lic span{display:block;font-size:14.4px;line-height:1.7;color:#3B4A38}
.ledg{display:grid;grid-template-columns:repeat(auto-fit,minmax(272px,1fr));
  gap:12px;margin:6px 0 16px}
.lcol{background:#fff;border:1px solid var(--line);border-radius:12px;padding:17px 19px;
  min-width:0}
.lcol.can{border-left:3px solid var(--green)}
.lcol.cant{border-left:3px solid var(--red)}
.lcol b{display:block;font-family:'IBM Plex Mono',monospace;font-size:10.2px;
  letter-spacing:.1em;text-transform:uppercase;margin-bottom:11px}
.lcol.can b{color:#2F7259}
.lcol.cant b{color:#9C3E36}
.lcol ul{margin:0;padding:0;list-style:none}
.lcol li{position:relative;padding-left:24px;font-size:14.3px;line-height:1.66;
  color:#3B4A38;margin-bottom:10px}
.lcol li:last-child{margin-bottom:0}
.lcol.can li:before{content:"";position:absolute;left:2px;top:7px;width:9px;height:5px;
  border-left:2px solid var(--green);border-bottom:2px solid var(--green);
  transform:rotate(-45deg)}
.lcol.cant li:before{content:"";position:absolute;left:2px;top:10px;width:11px;height:2px;
  background:var(--red)}
.disq{margin:0 0 16px;padding:13px 17px;background:#FBF6E9;border-left:3px solid #E4D9BE;
  border-radius:0 8px 8px 0;font-size:14.2px;line-height:1.7;color:#3B4A38;font-style:italic}
.disq span{display:block;font-style:normal;font-family:'IBM Plex Mono',monospace;
  font-size:9.8px;letter-spacing:.06em;text-transform:uppercase;color:var(--mut);margin-top:8px}

.sb{display:inline-block;font-family:'IBM Plex Mono',monospace;font-size:9.4px;
  letter-spacing:.08em;text-transform:uppercase;padding:4px 8px;border-radius:5px;
  margin-right:6px}
.sb.ok{background:#EAF3DE;color:#27500A}
.sb.no{background:#F3EFE4;color:#8A8069}
.pxmeta .sb{background:rgba(255,255,255,.14);color:rgba(255,255,255,.82)}
.pxmeta .sb.ok{background:rgba(246,197,96,.2);color:var(--amber)}

.pgrid{display:grid;grid-template-columns:repeat(auto-fill,minmax(298px,1fr));
  gap:13px;margin:12px 0}
.pcard{background:#fff;border:1px solid var(--line);border-radius:13px;padding:19px 21px;
  min-width:0;display:flex;flex-direction:column}
.pcard.feat{border-left:4px solid var(--amber);margin-bottom:16px}
.pcard h3{font-family:Fraunces,Georgia,serif;font-size:18px;line-height:1.26;
  font-weight:600;margin:0 0 4px}
.pcard h3 a{color:var(--ink);text-decoration:none}
.pcard h3 a:hover{color:var(--pine)}
.pcard .org{display:block;font-size:12.4px;line-height:1.45;color:var(--mut);
  margin-bottom:10px}
.pcard .one{font-size:14px;line-height:1.66;color:#3B4A38;margin:0 0 12px;flex:1;max-width:none}
.pcard .pmeta{display:flex;flex-wrap:wrap;align-items:center;gap:7px;margin-bottom:9px}
.pcard .cost{font-family:'IBM Plex Mono',monospace;font-size:14.5px;color:var(--pine);
  font-weight:600}
.pcard .mods{font-family:'IBM Plex Mono',monospace;font-size:9.8px;letter-spacing:.06em;
  text-transform:uppercase;color:var(--mut);margin:0 0 11px;max-width:none;line-height:1.5}
.pcard .go{font-size:13.2px;color:var(--pine);text-decoration:none;font-weight:500}
.pcard .go:hover{text-decoration:underline}

.law{background:#fff;border:1px solid var(--line);border-radius:12px;margin:0 0 9px}
.law summary{cursor:pointer;padding:15px 18px;display:flex;flex-wrap:wrap;gap:4px 12px;
  align-items:baseline;justify-content:space-between}
.law summary b{font-family:Fraunces,Georgia,serif;font-size:16.6px;line-height:1.3;
  color:var(--ink);font-weight:600}
.law summary span{font-family:'IBM Plex Mono',monospace;font-size:9.6px;
  letter-spacing:.07em;text-transform:uppercase;color:var(--mut);white-space:nowrap}
.law[open] summary{border-bottom:1px solid #F0EBDE}
.lawb{padding:16px 18px 18px}
.lawb p{font-size:14.7px;line-height:1.76;max-width:66ch}
.fx{display:grid;grid-template-columns:repeat(auto-fit,minmax(210px,1fr));gap:9px;
  margin:14px 0}
.fx .f{background:#FBF6E9;border-radius:9px;padding:12px 14px;min-width:0}
.fx .f span{display:block;font-family:'IBM Plex Mono',monospace;font-size:9.4px;
  letter-spacing:.08em;text-transform:uppercase;color:#9A8F76;margin-bottom:5px}
.fx .f b{display:block;font-size:13.6px;line-height:1.55;color:var(--ink);
  font-weight:500;overflow-wrap:anywhere}

.tbl{display:grid;background:#fff;border:1px solid var(--line);border-radius:11px;
  overflow:hidden;margin:6px 0 10px}
.tbl .r{display:grid;grid-template-columns:150px minmax(0,1fr);gap:14px;padding:14px 16px;
  border-bottom:1px solid #F0EBDE;font-size:14px}
.tbl .r:last-child{border-bottom:0}
.tbl .r span{font-family:'IBM Plex Mono',monospace;font-size:10.2px;letter-spacing:.07em;
  text-transform:uppercase;color:var(--mut);padding-top:3px}
.tbl .r b{font-weight:400;color:#3B4A38;line-height:1.68;min-width:0;overflow-wrap:anywhere}

.mods{margin:8px 0;padding:0 0 0 4px;list-style:none;counter-reset:m}
.mods li{counter-increment:m;position:relative;background:#fff;border:1px solid var(--line);
  border-radius:11px;padding:15px 17px 15px 52px;margin-bottom:9px;min-width:0}
.mods li:before{content:counter(m);position:absolute;left:16px;top:15px;width:23px;
  height:23px;border-radius:50%;background:#EAF3DE;color:#27500A;
  font-family:'IBM Plex Mono',monospace;font-size:11px;display:flex;align-items:center;
  justify-content:center}
.mods li b{display:block;font-size:15px;color:var(--ink);margin-bottom:6px;line-height:1.35}
.mods li p{font-size:13.8px;line-height:1.66;margin:0;max-width:none;color:#4A5A46}
.facl{margin:8px 0 14px;padding-left:19px}
.facl li{font-size:14.2px;line-height:1.68;color:#4A5A46;margin-bottom:7px;max-width:66ch}
.bl{margin:8px 0 16px;padding-left:19px}
.bl li{font-size:15px;line-height:1.76;color:#3B4A38;margin-bottom:9px;max-width:68ch}

.voxl{display:grid;gap:10px;margin:10px 0 6px}
.vox{display:block;background:#fff;border:1px solid var(--line);border-radius:10px;
  padding:14px 16px;text-decoration:none;min-width:0;border-left:3px solid #CFC7B4}
a.vox:hover{background:#FBFAF6}
.vox.pos{border-left-color:var(--green)}
.vox.neg{border-left-color:var(--red)}
.vox.mix{border-left-color:#C98B4B}
.vox.inf{border-left-color:#8FA3C4}
.vox i{display:block;font-style:italic;font-size:14.4px;line-height:1.65;color:#3B4A38;
  margin-bottom:7px}
.vwho{display:block;font-size:12.5px;color:var(--ink);font-weight:500}

.vfig{margin:0 0 18px;min-width:0}
.vplay{display:block;position:relative;width:100%;padding:0;border:0;background:#0E1A15;
  border-radius:13px;overflow:hidden;cursor:pointer;line-height:0}
.vplay img{width:100%;height:auto;display:block;opacity:.82;transition:opacity .18s}
.vplay:hover img{opacity:1}
.vplay:focus-visible{outline:3px solid var(--pine);outline-offset:3px}
.vbtn{position:absolute;left:50%;top:50%;width:66px;height:66px;
  transform:translate(-50%,-50%);border-radius:50%;background:rgba(20,38,30,.82);
  border:2px solid rgba(255,255,255,.9);transition:background .18s}
.vplay:hover .vbtn{background:var(--pine)}
.vbtn:after{content:"";position:absolute;left:52%;top:50%;transform:translate(-50%,-50%);
  border-style:solid;border-width:11px 0 11px 18px;border-color:transparent transparent
  transparent #fff}
.vfig figcaption{padding:11px 2px 0;font-size:13.4px;line-height:1.6;color:#4A5A46}
.vfig figcaption b{display:block;font-family:Fraunces,Georgia,serif;font-size:16px;
  color:var(--ink);margin-bottom:4px;line-height:1.3}
.vfig figcaption span{display:block}
.vmeta{font-family:'IBM Plex Mono',monospace;font-size:9.8px;letter-spacing:.05em;
  text-transform:uppercase;color:var(--mut);margin-top:6px}
.vframe{position:relative;width:100%;aspect-ratio:16/9;border-radius:13px;overflow:hidden;
  background:#000}
.vframe iframe{position:absolute;inset:0;width:100%;height:100%;border:0}

.srcl{font-family:'IBM Plex Mono',monospace;font-size:9.6px;letter-spacing:.06em;
  text-transform:uppercase;white-space:nowrap}
.gapl{margin:8px 0 14px;padding-left:19px}
.gapl li{font-size:14.2px;line-height:1.68;color:#4A5A46;margin-bottom:7px;max-width:66ch}
.srcs{border:1px solid var(--line);border-radius:10px;background:#fff;padding:13px 16px;
  margin:8px 0}
.srcs summary{cursor:pointer;font-family:'IBM Plex Mono',monospace;font-size:10.4px;
  letter-spacing:.08em;text-transform:uppercase;color:var(--pine)}
.srcs ol{margin:12px 0 0;padding-left:19px}
.srcs li{font-size:12.8px;line-height:1.55;margin-bottom:6px;overflow-wrap:anywhere}
.nxt{display:grid;grid-template-columns:repeat(auto-fit,minmax(240px,1fr));gap:11px;
  margin:14px 0 6px}
.nx{display:block;background:#fff;border:1px solid var(--line);border-left:3px solid var(--pine);
  border-radius:10px;padding:14px 16px;text-decoration:none;min-width:0}
.nx:hover{background:#FBFAF6}
.nx b{display:block;font-family:Fraunces,Georgia,serif;font-size:15.5px;color:var(--ink);
  margin-bottom:4px}
.nx span{display:block;font-size:12.8px;line-height:1.5;color:#4A5A46}

@media (max-width:900px){
  .pxwrap{grid-template-columns:minmax(0,1fr);gap:20px;padding-top:22px}
  .pxnav{position:static;display:flex;gap:7px;overflow-x:auto;padding-bottom:5px}
  .pxnav b{display:none}
  .pxnav a{border-left:0;border:1px solid var(--line);border-radius:20px;padding:6px 12px;
    white-space:nowrap;font-size:12.3px}
  .pxnav a.on{border-color:var(--pine);background:#EAF3DE}
  .pxband .in{grid-template-columns:minmax(0,1fr);gap:22px}
}
@media (max-width:560px){
  .tbl .r{grid-template-columns:minmax(0,1fr);gap:5px}
  .pgrid{grid-template-columns:minmax(0,1fr)}
  .vbtn{width:54px;height:54px}
}
@media print{.vplay,.vframe{display:none}.law{page-break-inside:avoid}}
</style>"""

JS = """<script>
(function(){
  var links=[].slice.call(document.querySelectorAll('.pxnav a'));
  var secs=links.map(function(a){return document.querySelector(a.getAttribute('href'))})
                .filter(Boolean);
  if(links.length&&secs.length){
    links[0].classList.add('on');
    if('IntersectionObserver'in window){
      var io=new IntersectionObserver(function(es){
        es.forEach(function(e){
          if(!e.isIntersecting)return;
          links.forEach(function(a){
            a.classList.toggle('on',a.getAttribute('href')==='#'+e.target.id);
          });
        });
      },{rootMargin:'-12% 0px -80% 0px'});
      secs.forEach(function(s){io.observe(s)});
    }
  }
  document.addEventListener('click',function(e){
    var b=e.target.closest?e.target.closest('.vplay'):null;
    if(!b)return;
    var id=b.getAttribute('data-yt');
    if(!id||!/^[A-Za-z0-9_-]{11}$/.test(id))return;
    var w=document.createElement('div');w.className='vframe';
    var f=document.createElement('iframe');
    f.src='https://www.youtube-nocookie.com/embed/'+id+'?autoplay=1&rel=0';
    f.title=b.getAttribute('aria-label')||'Video';
    f.allow='accelerometer;autoplay;encrypted-media;gyroscope;picture-in-picture';
    f.setAttribute('allowfullscreen','');
    w.appendChild(f);b.parentNode.replaceChild(w,b);
  });
})();
</script>"""


# ---------------------------------------------------------------- main

def main():
    os.makedirs(OUT, exist_ok=True)
    written = [(HUB, hub())]
    for p in PROGS:
        written.append((slugfile(p["slug"]), prog_page(p)))
    for fn, doc in written:
        open(os.path.join(OUT, fn), "w", encoding="utf-8").write(doc)

    bad = []
    for fn, doc in written:
        if doc.count("<h1") != 1:
            bad.append("%s: %d h1" % (fn, doc.count("<h1")))
        if ('rel="canonical" href="%s%s"' % (SITE, fn)) not in doc:
            bad.append("%s: canonical does not match its own filename" % fn)
        if not re.search(r"<script>[\s\S]*?navpanel[\s\S]*?</script>", doc):
            bad.append("%s: dead header" % fn)
        if re.search(r"<iframe[^>]*youtube", doc):
            bad.append("%s: a YouTube iframe ships in the HTML" % fn)
        for vid in re.findall(r'data-yt="([^"]*)"', doc):
            if not re.match(r"^[A-Za-z0-9_-]{11}$", vid):
                bad.append("%s: malformed video id %r" % (fn, vid))
        ids = re.findall(r'<h2 id="([^"]+)"', doc)
        navs = re.findall(r'<nav class="pxnav">.*?</nav>', doc, re.S)
        if not navs or re.findall(r'href="#([^"]+)"', navs[0]) != ids:
            bad.append("%s: nav does not match its sections" % fn)
        # Every outbound link must open in a new window and drop the referrer
        # chain - these pages link to programme sites the reader may not want
        # to be identified to.
        for m in re.finditer(r'<a [^>]*href="https?://[^"]+"([^>]*)>', doc):
            if "noopener" not in m.group(1) or 'target="_blank"' not in m.group(1):
                bad.append("%s: an external link does not open safely" % fn)
                break
        if fn != HUB and HUB not in doc:
            bad.append("%s: no link back to the hub" % fn)

    # The ledger is the reason this section exists. A programme page that lost
    # it would still look complete, which is exactly why it is guarded.
    for p in PROGS:
        doc = dict(written)[slugfile(p["slug"])]
        sc = p.get("scope") or {}
        if (sc.get("can") or sc.get("cannot")) and 'id="what-it-lets-you-do"' not in doc:
            bad.append("%s: scope researched but no ledger rendered" % p["slug"])
        for line in (sc.get("can") or []) + (sc.get("cannot") or []):
            if esc(line) not in doc:
                bad.append("%s: a scope line did not reach the page" % p["slug"])
                break
        # No page may invent a price.
        c = cost_str(p)
        if c and c not in doc:
            bad.append("%s: published cost missing from the page" % p["slug"])
        if not c and "publishes no figure" not in doc:
            bad.append("%s: no cost and no statement saying so" % p["slug"])
        # A state approval is a checkable fact and must not be softened.
        if sc.get("or_licensure") == "yes" and "Oregon approved" not in doc:
            bad.append("%s: Oregon approval not shown" % p["slug"])

    hubdoc = dict(written)[HUB]
    for p in PROGS:
        if ('href="%s"' % slugfile(p["slug"])) not in hubdoc:
            bad.append("hub does not link to %s" % p["slug"])
    for s in LAND.get("sections") or []:
        if esc(s["title"]) not in hubdoc:
            bad.append("hub is missing the %s section of the law" % s["id"])
    if re.search(r'class="[^"]*\b(rank|score|stars?)\b', hubdoc) \
       or re.search(r"\bbest\s+(training|programme|program)\b", hubdoc, re.I):
        bad.append("the hub appears to rank something")

    if bad:
        sys.exit("build_psy: " + "; ".join(bad[:8]))

    tot = sum(len(d) for _f, d in written)
    n_or = sum(1 for p in PROGS if (p.get("scope") or {}).get("or_licensure") == "yes")
    n_co = sum(1 for p in PROGS if (p.get("scope") or {}).get("co_licensure") == "yes")
    print("%d pages (1 hub + %d programmes) · %.2f MB"
          % (len(written), len(PROGS), tot / 1e6))
    print("   with a published cost: %d/%d   modules: %d   voices: %d   video: %d"
          % (sum(1 for p in PROGS if cost_num(p)), len(PROGS),
             sum(len(p.get("curriculum") or []) for p in PROGS),
             sum(len(p.get("voices") or []) for p in PROGS),
             sum(1 for p in PROGS if p.get("video"))))
    print("   Oregon-approved: %d   Colorado-approved: %d   law sections: %d"
          % (n_or, n_co, len(LAND.get("sections") or [])))


if __name__ == "__main__":
    main()
