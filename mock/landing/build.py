#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Three home-page concepts, built as real pages.

The brief, accumulated across several messages:
  - an actual landing page, not the simulator. Explain the site before doing
    anything with it.
  - AIDA: attention, interest, desire, action. The h1 is attention, the deck
    and the three proof figures are interest, "who this is for" is desire, one
    primary CTA is action.
  - the h1 must be SEO-bearing, so someone arriving cold knows exactly where
    they are and search knows what the page is about.
  - the brand stays Therapist Support.
  - the bolder visual energy of the old purple chapter hero is welcome.

Only the HERO differs between the three. Everything below the fold is identical,
on purpose: the decision here is about the first screen, and holding the rest
constant is what makes the comparison honest.
"""
import os, re, base64

HERE = os.path.dirname(os.path.abspath(__file__))
import content as C
from css import CSS

# ---------------------------------------------------------------- chrome ---
CH = os.path.join(HERE, "..", "amft")
chrome_css = open(os.path.join(CH, "_chrome_css.txt")).read()
chrome_hdr = open(os.path.join(CH, "_chrome_hdr.txt")).read()
chrome_js = open(os.path.join(CH, "_chrome_js.txt")).read().split("\n/*---*/\n")[0]
# home-page mock-ups: no nav entry is current
chrome_hdr = re.sub(r'(<a href="[^"]*") class="on"', r'\1', chrome_hdr)
assert 'class="on"' not in chrome_hdr

FONTS = os.path.join(HERE, "..", "tree5", "fonts")


def inline_fonts():
    css = open(os.path.join(FONTS, "fonts.css")).read()
    keep = [b for b in re.split(r"(?=/\* )", css) if b.strip().startswith("/* latin */")]
    assert len(keep) >= 6
    def sub(m):
        with open(os.path.join(FONTS, "f", m.group(1)), "rb") as f:
            return "url(data:font/woff2;base64," + base64.b64encode(f.read()).decode() + ")"
    return re.sub(r"url\(\./f/([^)]+)\)", sub, "".join(keep))


FONT_CSS = inline_fonts()


def classes(css, bare_only=False):
    out = set()
    for sel, _ in re.findall(r"([^{}]+)\{([^{}]*)\}", css):
        for part in sel.split(","):
            part = part.strip()
            if bare_only and not re.fullmatch(r"\.[A-Za-z0-9_-]+", part):
                continue
            out |= set(re.findall(r"\.([A-Za-z][A-Za-z0-9_-]*)", part))
    return out


bad = classes(CSS, bare_only=True) & classes(chrome_css)
assert not bad, "bare rules collide with the lifted chrome: %s" % sorted(bad)
stray = {c for c in classes(CSS) if not c.startswith("l")}
assert not stray, "classes outside the l- namespace: %s" % sorted(stray)


def esc(s):
    return s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")


# ------------------------------------------------------------- the heroes ---
PROOF = [("$138,365", "what a $250,000 practice actually pays you, after every "
                      "running cost and every tax"),
         ("8", "places priced against California, on your own profit"),
         ("3,000", "associate hours, projected week by week")]

WHO = ("<p class='lwho'>For <b>LMFTs</b>, <b>LCSWs</b>, <b>LPCCs</b>, "
       "<b>psychologists</b> and <b>registered associates</b> "
       "&mdash; California only.</p>")


def proof(cls=""):
    return ('<div class="lproof">'
            + "".join('<div><b>%s</b><em>%s</em></div>' % (a, b) for a, b in PROOF)
            + "</div>")


# ---- the hero proof panel -------------------------------------------------
# NOT round numbers chosen to look good. Every figure below was read out of
# TREE on practice-simulator.html for one scenario, which the panel header
# states: rate 200, 25 sessions a week, 2 weeks off (= $250,000 gross), and
# $35,400 a year of typed running costs plus 2.5% card processing ($6,250),
# = $41,650. The engine returned net 138,940, tax 69,410, optional 18,244.
# Re-run /tmp/proof4.mjs if any of the 2026 rates change.
PANEL_H = "A $250,000 practice &middot; $41,650 of running costs"
PANEL = [
    ("Take-home", "$138,940", "after every cost and every tax"),
    ("Tax on it", "$69,410", "and $18,244 of that is optional"),
    ("What a client is worth", "$4,800", "24 sessions at $200, not one at $200"),
]


def panel():
    return ('<div class="lhdp"><p class="lhdph">%s</p>' % PANEL_H
            + "".join('<div class="lhdr"><span class="lhdlab">%s</span>'
                      '<span class="lhdval"><b>%s</b><em>%s</em></span></div>' % r
                      for r in PANEL)
            + '</div>')


def acts(primary="Open the practice simulator", secondary="See all the tools"):
    return ('<div class="lacts">'
            '<a class="lcta" href="%s">%s &rarr;</a>'
            '<a class="lghost" href="%s">%s</a></div>'
            % (C.SIM, primary, C.TOOLS, secondary))


HEROES = {
 # ------------------------------------------------------------------ A ------
 "a": dict(
   name="Calm authority",
   why="The site introduces itself plainly and the h1 carries the subject. "
       "Safest, most credible, least likely to be misread by anyone. The risk "
       "is that it looks like every other professional-services site.",
   html="""
<section class="lheroA"><div class="lwrap">
  <p class="leyebrow">Free &middot; nothing saved &middot; 2026 California rates</p>
  <h1>The money side of a California therapy practice.</h1>
  <p class="ldeck">Free tools and plain-language research for California LMFTs,
    LCSWs, LPCCs and psychologists &mdash; what your practice really pays you,
    what your tax bill could be, and what a client is worth. Every figure worked
    from your own numbers, with the rule it came from linked underneath.</p>
  %(acts)s
  %(who)s
  %(proof)s
</div></section>"""),

 # ------------------------------------------------------------------ B ------
 "b": dict(
   name="The bold chapter",
   why="Carries the purple slab energy from the old bonus-level hero, which is "
       "the most striking thing this site has ever had on screen. Highest "
       "attention, most memorable, and it makes the site feel like it was made "
       "by someone rather than assembled. The risk is tone: money advice in a "
       "game palette has to earn its seriousness back immediately, which the "
       "three figures underneath are there to do.",
   html="""
<section class="lheroB"><div class="lwrap">
  <p class="leyebrow">For California therapists</p>
  <h1>Running a practice is a <em>second job</em> nobody trained you for.</h1>
  <p class="ldeck">This site does that job's arithmetic. What your practice
    actually pays you, how much of your tax bill is optional, what an associate
    placement is really worth, and where your next ten clients come from &mdash;
    worked from your own numbers, free, with nothing saved.</p>
  %(acts)s
  %(who)s
  %(proof)s
</div></section>"""),

 # ------------------------------------------------------------------ C ------
 "c": dict(
   name="Recognition first",
   why="Opens on the reader's own sentence rather than on the site's name, so "
       "the first thing they feel is being understood. Strongest for a cold "
       "visitor arriving from search with a specific worry. Weakest for "
       "someone who already knows the site and just wants the tool.",
   html="""
<section class="lheroC"><div class="lwrap">
  <p class="lquote">&ldquo;I have no idea whether I am charging enough.&rdquo;</p>
  <p class="leyebrow">Therapist Support &middot; California</p>
  <h1>Free money tools for California therapists.</h1>
  <p class="ldeck">Nobody teaches this part. What the practice pays you after
    twelve running costs and self-employment tax, whether to incorporate, what a
    client is worth over their whole time with you, and whether that associate
    job is what it looks like. Worked from your numbers, cited to the rule.</p>
  %(acts)s
  %(who)s
  %(proof)s
</div></section>"""),

 # ------------------------------------------------------------------ D ------
 # THE ONE THAT SHIPS. B's hook on A's palette, in the two-column layout that
 # puts the proof panel in the 644px of dead space the old h1 left empty -
 # which is also what lifts a figure above the fold on every laptop and phone.
 "d": dict(
   name="Light hero, coloured panel",
   why="Paper ground, ink type, colour concentrated in the panel, so the hero "
       "matches the rest of the site instead of announcing itself. The bold "
       "hook survives because the typography carries it, not the background.",
   html="""
<section class="lheroD"><div class="lwrap"><div class="lhd">
  <div>
    <p class="leyebrow">For California therapists &middot; 2026 rates</p>
    <h1>Running a practice is a <em>second job</em> nobody trained you for.</h1>
    <p class="ldeck">Free tools for the business side of a practice &mdash; what you keep,
      what you owe, and what a client is worth. Your own numbers, nothing saved.</p>
    %(acts)s
    %(who)s
  </div>
  %(panel)s
</div>
</div></section>"""),
}


# ------------------------------------------------------------ below fold ---
def below(promote=False):
    """promote=True is the iteration: every section routes somewhere else.

    The five Help Scout habits, applied - see the note at the foot of
    content.py for what was taken and what was deliberately not."""
    s = []
    A = s.append

    def kick(key, h2, lede=None):
        k = C.KICKERS.get(key) if promote else None
        A('<div class="lkick"><div><h2>%s</h2>%s</div>%s</div>'
          % (esc(h2),
             ('<p class="llede">%s</p>' % esc(lede)) if lede else "",
             ('<a class="lkicka" href="%s"><span>%s &rarr;</span></a>' % (k[1], esc(k[0]))) if k else ""))

    def kind(k):
        return ('<p class="lkind" data-kind="%s">%s</p>' % (k, esc(C.KIND[k]))) if promote else ""

    # The answer grid. NOT .lnarrow any more - the prose it replaced was
    # deliberately a narrow measure, which is exactly what left the right half
    # of the page empty. A four-card grid wants the full wrap.
    A('<section class="lsec"><div class="lwrap lwhy">')
    A('<p class="leyebrow">Why this exists</p><h2>%s</h2>' % esc(C.WHY_H))
    A('<p class="llede">%s</p>' % C.WHY_LEDE)
    A('<div class="lans">')
    for q, body, cta, href in C.ANSWERS:
        A('<a class="lansc" href="%s"><q class="lansq">%s</q>'
          '<span class="lansb">%s</span><span class="lansg">%s &rarr;</span></a>'
          % (href, esc(q), body, cta))
    A('</div></div></section>')

    A('<section class="lsec lpaper"><div class="lwrap"><div class="lgrid lg3">')
    for p_ in C.PROMISES:
        A('<div class="lpromise"><h3>%s</h3><p>%s</p></div>'
          % (esc(p_["title"]), esc(p_["body"])))
    A('</div></div></section>')

    A('<section class="lsec"><div class="lwrap">')
    kick("audience", C.AUDIENCE_H)
    A('<div class="lgrid lg3">')
    for a in C.AUDIENCE:
        A('<a class="laud" href="%s"><b>%s</b><span>%s</span><em>%s &rarr;</em></a>'
          % (a["href"], esc(a["label"]), esc(a["body"]), esc(a["cta"])))
    A('</div></div></section>')

    # --- the mid-page band. Second of the three binary CTAs.
    if promote:
        A('<section class="lmid"><div class="lwrap">')
        A('<p class="leyebrow">%s</p><h2>%s</h2><p>%s</p>' %
          (esc(C.MID["eyebrow"]), esc(C.MID["h"]), esc(C.MID["body"])))
        A('<div class="lacts"><a class="lcta" href="%s">%s &rarr;</a>'
          '<a class="lghost" href="%s">%s</a></div>'
          % (C.SIM, esc(C.MID["cta"]), C.TOOLS, esc(C.MID["cta2"])))
        A('</div></section>')

    A('<section class="lsec lpaper"><div class="lwrap">')
    kick("tools", C.TOOLS_H, C.TOOLS_LEDE)
    ACC = {"sim": "pine", "tax": "gold", "amft": "indigo", "grow": "pine"}
    A('<div class="lgrid">')
    for t in C.TOOL_BLOCKS:
        bul = ('<ul class="lbul">' + "".join("<li>%s</li>" % esc(x) for x in t["bullets"])
               + "</ul>") if t["bullets"] else ""
        pair = ""
        if promote and t["k"] in C.PAIRS:
            pk, pt, pb, ph = C.PAIRS[t["k"]]
            pair = ('<span class="lpair"><i>&rarr;</i><span><b>Next: %s</b>'
                    '<span>%s</span></span></span>' % (esc(pt), pb))
        A('<a class="ltool" data-accent="%s" href="%s">'
          '<div>%s<p class="ltag">%s</p><h3>%s</h3><p class="lbody">%s</p>%s'
          '<p class="lname">%s &rarr;</p></div>'
          '<div class="lfig"><b>%s</b><em>%s</em>%s</div></a>'
          % (ACC[t["k"]], t["href"], kind("tool"), esc(t["tag"]), esc(t["q"]),
             esc(t["body"]), bul, esc(t["title"]),
             esc(t["stat"][0]), esc(t["stat"][1]), pair))
    A('</div></div></section>')

    A('<section class="lsec"><div class="lwrap">')
    kick("reading", C.READING_H)
    A('<div class="lgrid lg2">')
    for r in C.READING:
        A('<a class="lread" href="%s">%s<b>%s</b><span>%s</span></a>'
          % (r["href"], kind("notes"), esc(r["title"]), esc(r["body"])))
    A('</div></div></section>')

    # --- the named hub. Help Scout's "Support Toolkit" pattern.
    if promote:
        A('<section class="lsec lpaper"><div class="lwrap"><div class="lkit">')
        A('<h2>%s</h2><p>%s</p>' % (esc(C.TOOLKIT["name"]), C.TOOLKIT["promise"]))
        A('<div class="lkitrows">')
        for b_, d in C.TOOLKIT["items"]:
            A('<div><b>%s</b><span>%s</span></div>' % (esc(b_), esc(d)))
        A('</div>')
        A('<a class="lcta" href="%s">Open the toolkit &rarr;</a>' % C.TOOLKIT["href"])
        A('</div></div></section>')

    A('<section class="lsec"><div class="lwrap lnarrow">')
    A('<div class="lhead"><h2>%s</h2></div>' % esc(C.HOW_H))
    A('<ul class="lhow">')
    for t, b_ in C.HOW:
        A('<li><div><b>%s</b><span>%s</span></div></li>' % (esc(t), esc(b_)))
    A('</ul></div></section>')

    A('<section class="lsec lpaper"><div class="lwrap lnarrow labout">')
    A('<div class="lhead"><h2>%s</h2></div>' % esc(C.ABOUT_H))
    A('<p>%s</p>' % esc(C.ABOUT_BODY))
    A('<p class="lnote">%s</p>' % esc(C.ABOUT_NOTE))
    A('</div></section>')

    A('<section class="lnews"><div class="lwrap lnarrow">')
    A('<p class="leyebrow">Stay updated</p><h2>New tools, as they land</h2>')
    A('<p class="llede">What has been added or changed here, plus rate and rule '
      'updates that move a figure you rely on. One email a month.</p>')
    A('<form class="lnewsrow" onsubmit="return false">'
      '<input type="email" placeholder="you@practice.com" aria-label="Your email address">'
      '<button class="lcta" type="submit">Stay updated</button></form>')
    A('<label class="lconsent"><input type="checkbox"><span>Also send me occasional '
      'notes about new tools on this site. Optional, separate from the monthly email, '
      'and you can stop either at any time.</span></label>')
    A('</div></section>')
    return "\n".join(s)


SWITCH_CSS = """
.lmsw{position:sticky;top:0;z-index:60;display:flex;gap:8px;flex-wrap:wrap;align-items:center;
  background:#26241E;color:#CFC7B3;padding:8px 16px;font-family:'IBM Plex Mono',monospace;
  font-size:11px;letter-spacing:.08em;text-transform:uppercase}
.lmsw span{opacity:.6;margin-right:6px}
.lmsw a{color:#CFC7B3;text-decoration:none;border:1px solid #4A463C;border-radius:999px;
  padding:6px 11px;min-height:32px;display:inline-flex;align-items:center}
.lmsw a:hover{border-color:#B08430;color:#fff}
.lmsw a.lmon{background:#B08430;border-color:#B08430;color:#17181A;font-weight:600}
.lmwhy{background:#F4F0E4;border-bottom:1px solid #E7E2D6;padding:12px 16px;
  font-size:13.5px;line-height:1.55;color:#4A453B}
.lmwhy b{font-family:Fraunces,Georgia,serif}
@media print{.lmsw,.lmwhy{display:none}}
"""

SHELL = """<!doctype html>
<html lang="en"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<meta name="robots" content="noindex, nofollow">
<title>Home concept %(letter)s — %(name)s</title>
<style>%(fonts)s</style>
<style>%(chrome_css)s</style>
<style>%(sw)s%(css)s</style>
</head><body>
%(switch)s
<div class="lmwhy"><b>%(name)s.</b> %(why)s</div>
%(chrome_hdr)s
<main class="lp">
%(hero)s
%(below)s
</main>
<script>%(chrome_js)s</script>
</body></html>
"""


HEROES["b2"] = dict(
    name="B, iterated",
    why="The B hero, with every section below it turned into something that "
        "promotes something else \u2014 a link beside each heading, a category "
        "chip on every card, a \u201cnext\u201d line under each tool handing you "
        "the reading that pairs with it, a mid-page band repeating the binary "
        "CTA, and a named toolkit block. Five habits taken from Help Scout.",
    html=HEROES["b"]["html"])


def main():
    keys = list(HEROES.keys())
    plain = below(promote=False)
    rich = below(promote=True)
    for k in keys:
        h = HEROES[k]
        switch = ('<div class="lmsw"><span>Home concept</span>'
                  + "".join('<a href="home-%s.html"%s>%s &middot; %s</a>'
                            % (x, ' class="lmon"' if x == k else "", x.upper(),
                               esc(HEROES[x]["name"]))
                            for x in keys) + "</div>")
        body = rich if k == "b2" else plain
        # D takes a panel where A/B/C take the three-figure proof strip, so the
        # substitution dict carries both and each template uses what it names.
        hero = h["html"] % {"acts": acts(), "who": WHO, "proof": proof(),
                            "panel": panel()}
        html = SHELL % {"letter": k.upper(), "name": esc(h["name"]), "why": esc(h["why"]),
                        "fonts": FONT_CSS, "chrome_css": chrome_css, "css": CSS,
                        "sw": SWITCH_CSS, "switch": switch, "chrome_hdr": chrome_hdr,
                        "hero": hero, "below": body, "chrome_js": chrome_js}
        for href in re.findall(r'href="([^"#?]+)', hero + body):
            if href.startswith(("http", "mailto", "#")):
                continue
            assert os.path.exists(os.path.join(HERE, "..", "..", "site", href)), \
                "concept %s links to a missing file: %s" % (k, href)
        p = os.path.join(HERE, "home-%s.html" % k)
        open(p, "w", encoding="utf-8").write(html)
        print("wrote home-%s.html  %d kB  (%s)" % (k, len(html) // 1024, h["name"]))


# ==========================================================================
# SHIP: B2 becomes index.html.
#
# Concept B's hero with the promoting body - the arrangement chosen after the
# four were compared. Differences from the mock-up:
#   - real <head>: title, description, canonical, OG, JSON-LD
#   - the site footer, so it matches every other page
#   - the switcher and the "why this concept" strip are gone
#   - no noindex
# ==========================================================================
SHIP_TITLE = ("Free money tools for California therapists \u2014 Therapist Support")
SHIP_DESC = ("Free calculators and plain-language research for California LMFTs, LCSWs, "
             "LPCCs and psychologists. What your practice actually pays you, how much of "
             "your tax bill is optional, what an associate job is really worth, and where "
             "your next clients come from. Nothing saved, no account.")
SITE_URL = "https://cavatello.github.io/therapist-tools"

SHIP_SHELL = """<!doctype html>
<html lang="en"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>%(title)s</title>
<meta name="description" content="%(desc)s" />
<link rel="canonical" href="%(site)s/" />
<meta property="og:title" content="%(title)s" />
<meta property="og:description" content="%(desc)s" />
<meta property="og:type" content="website" />
<meta property="og:url" content="%(site)s/" />
<meta property="og:image" content="%(site)s/og-image.png" />
<meta name="twitter:card" content="summary_large_image" />
%(head)s
<style>%(chrome_css)s</style>
<style>%(css)s</style>
<script type="application/ld+json">%(ld)s</script>
</head><body>
%(hdr)s
<main class="lp">
%(hero)s
%(below)s
</main>
%(ftr)s
<script>%(js)s</script>
</body></html>
"""


def ship():
    import json
    chrome_head = open(os.path.join(CH, "_chrome_head.txt")).read()
    chrome_ftr = open(os.path.join(CH, "_chrome_ftr.txt")).read()
    hdr = chrome_hdr
    ld = json.dumps([
      {"@context":"https://schema.org","@type":"WebSite","name":"Therapist Support",
       "url":SITE_URL + "/","description":SHIP_DESC,
       "publisher":{"@type":"Organization","name":"Cavatello"}},
      {"@context":"https://schema.org","@type":"ItemList",
       "name":"Free tools for California therapists",
       "itemListElement":[
         {"@type":"ListItem","position":i+1,"name":t["title"],
          "url":"%s/%s" % (SITE_URL, t["href"])}
         for i, t in enumerate(C.TOOL_BLOCKS)]}], separators=(",", ":"))
    # D, not B. The measurements that decided it are in css.py above .lheroD.
    hero = HEROES["d"]["html"] % {"acts": acts("Open the simulator", "All the tools"),
                                  "who": WHO, "panel": panel()}
    html = SHIP_SHELL % dict(title=SHIP_TITLE, desc=SHIP_DESC, site=SITE_URL,
                             head=chrome_head, chrome_css=chrome_css, css=CSS,
                             ld=ld, hdr=hdr, hero=hero, below=below(promote=True),
                             ftr=chrome_ftr, js=chrome_js)
    assert html.count("<h1") == 1, "exactly one h1"
    assert html.count("<footer") == 1, "exactly one footer"
    assert 'href="terms.html"' in html and 'href="privacy.html"' in html
    assert "noindex" not in html, "the real home page must be indexable"
    assert "lmsw" not in html, "the mock-up switcher must not ship"
    for href in re.findall(r'href="([^"#?]+)', html):
        if href.startswith(("http", "mailto", "#", "data:")):
            continue
        assert os.path.exists(os.path.join(HERE, "..", "..", "site", href)), \
            "home links to a missing file: " + href
    open(os.path.join(HERE, "index.html"), "w", encoding="utf-8").write(html)
    print("wrote index.html  %d kB  (concept B2, shipped)" % (len(html) // 1024))


if __name__ == "__main__":
    main()
    ship()
