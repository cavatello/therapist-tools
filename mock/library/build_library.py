#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Build the content library: a front door, five topic hubs, and three indexes.

WHY THE HUB IS BEING REBUILT. resources.html worked as a flat question index at
twenty-four rows and it will not work at three hundred. The failure is specific
and it is not aesthetic: the page's promise is completeness - "everything in one
place, indexed by the question you arrived with" - and at three hundred pages
that promise silently becomes false. The reader cannot tell the difference
between "this site does not cover that" and "it is not on this screen", which is
exactly the trust the site is built on.

So the hub stops being the library and becomes the front door. Its job is to get
a reader into one of five topics, one of seven calculators, or one of two
directories inside one screen and one click. Everything exhaustive moves one
level down, where it can be exhaustive honestly.

WHAT WAS TAKEN FROM THE STUDY OF HELP SCOUT AND FOUR OTHERS (work/hubstudy.md):

  - Two taxonomy axes, topic and format, and NO tags. None of the five reference
    sites studied runs a general tag vocabulary; tags on a library this size
    produce one term per article and two hundred thin pages.
  - A category page is not an archive page. Help Scout's /growth/ shows three
    posts and claims nothing; /growth/all-posts/ shows all sixty-two and claims
    only completeness. That split is the whole answer.
  - Calculators sit on their topic hub AND get one flat index, because on this
    site the calculators are the product.
  - No thumbnail images. Help Scout's resource cards are 60% abstract brand art
    carrying zero information; Ahrefs ships no images on its index at all and is
    denser and faster.
  - No reading time, no publish date, no author. A correct page dated 2024 looks
    worse than a wrong page dated last week, so this site stamps CHECKED rather
    than published - which none of the five exemplars does, and which is the
    site's actual competitive claim.
  - No chronological feed. Every exemplar has one because they are publishers.
    We are a reference. Recency here means "is this number still right", so the
    feed is a log of numbers that moved, not of pages that shipped.

WHAT IS GENERATED, NOT HAND-MAINTAINED. Every listing on every page here comes
from registry.json, which carries one record per page. That is the fix for the
maintenance failure: under a hand-written index a page only exists if someone
writes a row for it, so long-tail articles arrive faster than rows and become
orphans reachable only from the sitemap.
"""
import os, re, sys, json, html

HERE = os.path.dirname(os.path.abspath(__file__))
WORK = os.path.dirname(HERE)
# The repo used to be work/stage2 alongside work/mock; it was flattened,
# and this line was not - so every run since has died looking for
# `mock/../stage2/mock/library/registry.json`. SITE is the repo root.
# This builder only READS from SITE (registry.json and the chrome donor);
# it writes to mock/library/out/, so a run cannot touch the live site.
SITE = os.path.dirname(WORK)
CHROME = os.path.join(SITE, "resources.html")
OUT = os.path.join(HERE, "out")
BASE = "https://therapistsupport.org/"
UPDATED = "6 August 2026"
CHECKED = "Aug 2026"

# The SITE's copy, not a second one under work/. There were two identical
# registry.json files for a while - one here, one in the site - kept in step by
# remembering to copy. That is the same hand-maintained duplication the whole
# registry_meta/registry_sync handover exists to remove, and it would have gone
# wrong the first time a pass wrote to one of them and not the other.
# registry_sync.py writes the site's copy; this reads it.
REG = json.load(open(os.path.join(SITE, "mock", "library", "registry.json"),
                     encoding="utf-8"))
PAGES = {p["file"]: p for p in REG["pages"]}
TOPICS = REG["topics"]
CHANGES = REG["changes"]

ORDER = ["money", "licensure", "getting-paid", "practice", "training"]
FMT = {"calculator": "Calculator", "guide": "Guide", "answer": "Answer",
       "directory": "Directory", "reference": "Reference"}


def esc(x):
    return html.escape(str(x)) if x is not None else ""


# ---------------------------------------------------------------- chrome

def balanced(s, tag, start=0):
    i = s.find("<" + tag, start)
    if i < 0:
        return None
    d = 0
    for m in re.finditer(r"<%s\b|</%s>" % (tag, tag), s[i:]):
        d += 1 if m.group(0).startswith("<" + tag) else -1
        if d == 0:
            return (i, i + m.end())
    return None


src = open(CHROME, encoding="utf-8").read()
_he = src.find("</head>")
LINKS = "\n".join(m.group(0) for m in re.finditer(r"<link\b[^>]*>", src[:_he])
                  if 'rel="stylesheet"' in m.group(0) or "fonts." in m.group(0)
                  or 'rel="preconnect"' in m.group(0))
# The shared CSS was extracted out of every page into css/<hash>.css, so the
# chrome now arrives as <link> tags rather than <style> blocks. Lift whichever
# form the source page is currently in - a builder that assumed one and got the
# other would silently ship an unstyled page.
STYLES = "\n".join(re.findall(r"<style>.*?</style>", src, re.S))
CSSLINKS = "\n".join(re.findall(r'<link rel="stylesheet" href="css/[^"]+">', src))
assert STYLES or CSSLINKS, "no stylesheet lifted - the page would render bare"
_h = balanced(src, "header")
HEADER = re.sub(r'(<a href="[^"]*") class="on"', r"\1", src[_h[0]:_h[1]])
_f = balanced(src, "footer")
FOOTER = re.sub(r'(<a href="[^"]*") class="on"', r"\1", src[_f[0]:_f[1]])
NAVSCRIPT = ""
for m in re.finditer(r"<script>([\s\S]*?)</script>", src):
    if "navpanel" in m.group(1):
        NAVSCRIPT = m.group(0)
assert NAVSCRIPT, "no nav script in the chrome - the header would be dead"


def lift_section(heading):
    """Carry a hand-written section of the old hub forward, verbatim.

    The reference list is seventy-eight outbound links that were checked by
    hand. Regenerating the hub must not throw that away, and rewriting it from
    scratch would be a fabrication of work already done - so the section is
    lifted out of the published page and re-emitted unchanged.
    """
    i = src.find(">" + heading + "<")
    if i < 0:
        return ""
    j = src.rfind("<section", 0, i)
    span = balanced(src, "section", j)
    return src[span[0]:span[1]] if span else ""


STAGE = lift_section("Where you are right now")
REFLIST = lift_section("The reference list")
PROVENANCE = lift_section("Where numbers come from")
assert REFLIST, "the reference list did not lift - 78 checked links would be lost"


# ---------------------------------------------------------------- registry

def leaves(t=None):
    return [p for p in REG["pages"] if p.get("leaf")
            and (t is None or p["topic"] == t)]


def topic_pages(t, include_skipped=False):
    out = []
    for c in TOPICS[t]["clusters"]:
        for f in c["files"]:
            p = PAGES.get(f)
            if p and (include_skipped or not p.get("skip")):
                out.append(p)
    return out


def hub_path(t):
    return "%s/" % t


def card(p, show_topic=False, up=""):
    """The content card. Five fields, and a deliberate list of omissions.

    `up` IS NOT OPTIONAL DECORATION. Every page this site generates lives at the
    root except the five topic hubs, which live in subdirectories. A bare
    relative href on one of those resolves against the subdirectory, so
    `amft-3000-hours-california.html` linked from /licensure/ points at
    /licensure/amft-3000-hours-california.html, which has never existed. That
    shipped, and it broke EVERY article link on ALL FIVE hubs - thirty-nine
    dead links, including the ones to privacy, terms and the affiliate
    disclosure.

    It survived because the guard below had an explicit clause skipping bare
    hrefs on subdirectory pages, which is precisely and only where the bug can
    occur. A guard with an exemption for the failure case is worse than no
    guard: it reports clean and it is believed.

    Format chip first because on this site the format gap is enormous - one
    card leads to something that computes your tax, the next to a paragraph -
    and the card almost always already sits under a topic heading.

    The outcome line is mandatory. Help Scout makes its description optional and
    eleven of twenty-three cards carry one; the rest ship an explicit
    `no-description` class. Optional descriptions produce ragged grids and let
    weak entries hide behind a title.
    """
    bits = ['<span class="fchip f-%s">%s</span>'
            % (p["format"], FMT.get(p["format"], p["format"]))]
    if show_topic:
        bits.append('<span class="tchip">%s</span>' % esc(TOPICS[p["topic"]]["name"]))
    if p.get("stale"):
        bits.append('<span class="chk">Checked %s</span>' % CHECKED)
    num = ('<span class="cnum">%s</span>' % esc(p["number"])) if p.get("number") else ""
    return ('<a class="lc" href="%s%s"><span class="lch">%s</span>'
            "<b>%s</b><span class=\"lco\">%s</span>%s</a>"
            % (up, esc(p["file"]), "".join(bits), esc(p["question"]),
               esc(p["outcome"]), num))


def row(p, show_topic=False):
    """The compact variant, for exhaustive lists. Two variants ship, not ten.

    Help Scout's category page carries ten card variants - DEFAULT,
    FEATURED_HORIZONTAL, HORIZONTAL, L, LARGE, LARGE_WITH_DESCRIPTION,
    FEATURED, WITH_FEATURED, OUTLINE, COMPACT - which is a component that grew a
    variant per layout accident.
    """
    return ('<a class="lr" href="%s"><span class="fchip f-%s">%s</span>'
            "<b>%s</b>%s%s</a>"
            % (esc(p["file"]), p["format"], FMT.get(p["format"], p["format"]),
               esc(p["question"]),
               ('<span class="tchip">%s</span>' % esc(TOPICS[p["topic"]]["name"]))
               if show_topic else "",
               ('<span class="chk">%s</span>' % CHECKED) if p.get("stale") else ""))


def _rel(markup, up):
    """Re-root root-relative hrefs for a page that sits in a subdirectory."""
    if not up:
        return markup
    return re.sub(r'(href|src)="(?!https?:|//|#|data:|/)', r'\1="' + up, markup)


def page(title, desc, canon, depth, band, body, crumbs):
    """`depth` is how many directories deep the file sits, so relative links
    from a topic hub at /money/ resolve back to the root pages."""
    up = "../" * depth
    h, f = _rel(HEADER, up), _rel(FOOTER, up)
    return """<!doctype html>
<html lang="en"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>%s</title>
<meta name="description" content="%s">
<link rel="canonical" href="%s%s">
%s
%s
%s
<script type="application/ld+json">%s</script>
</head><body class="lib">
%s
<main>%s%s</main>
%s
%s
</body></html>""" % (esc(title), esc(desc), BASE, canon,
                     _rel(LINKS + "\n" + CSSLINKS, up),
                     STYLES, CSS, crumbs_ld(crumbs), h, band, body, f, NAVSCRIPT)


def crumbs_ld(items):
    return json.dumps({
        "@context": "https://schema.org", "@type": "BreadcrumbList",
        "itemListElement": [
            {"@type": "ListItem", "position": i + 1, "name": n,
             **({"item": BASE + u} if u else {})}
            for i, (n, u) in enumerate(items)]}, separators=(",", ":"))


def crumbs_html(items, up=""):
    out = []
    for i, (n, u) in enumerate(items):
        sep = '<span class="sep">&rsaquo;</span>' if i < len(items) - 1 else ""
        if u:
            out.append('<li><a href="%s%s">%s</a>%s</li>' % (up, esc(u), esc(n), sep))
        else:
            out.append('<li><span aria-current="page">%s</span></li>' % esc(n))
    return '<ol class="bcr" aria-label="Breadcrumb">%s</ol>' % "".join(out)


def band(kicker, h1, dek, crumbs, meta, up=""):
    return ('<section class="libband"><div class="in">%s<p class="sub">%s</p>'
            "<h1>%s</h1><p class=\"dek\">%s</p>"
            '<div class="libmeta">%s</div></div></section>'
            % (crumbs_html(crumbs, up), esc(kicker), h1, dek,
               "".join("<span>%s</span>" % esc(m) for m in meta)))


# ---------------------------------------------------------------- pages

def changes_block(n=4, up=""):
    rows = "".join(
        '<li><time>%s</time><span>%s</span>'
        '<a href="%s%s">what it changes &rarr;</a></li>'
        % (esc(c["date"]), esc(c["what"]), up, esc(c["where"]))
        for c in CHANGES[:n])
    return '<ul class="chg">%s</ul>' % rows


def build_hub():
    calcs = sorted((p for p in REG["pages"]
                    if p["format"] == "calculator" and not p.get("skip")),
                   key=lambda p: -p["weight"])
    dirs = [p for p in REG["pages"] if p["format"] == "directory"]
    qs = sorted((p for p in REG["pages"]
                 if not p.get("skip") and p["format"] != "reference"
                 and not p.get("leaf")),
                key=lambda p: (-p["weight"], p["question"]))[:20]

    tcards = []
    for t in ORDER:
        ps = topic_pages(t)
        samples = sorted(ps, key=lambda p: -p["weight"])[:3]
        tcards.append(
            '<a class="tcard t-%s" href="%s"><b>%s</b>'
            '<span class="tt">%s</span><span class="tn">%d page%s</span>'
            "<ul>%s</ul><span class=\"go\">Browse %s &rarr;</span></a>"
            % (t, hub_path(t), esc(TOPICS[t]["name"]), esc(TOPICS[t]["tagline"]),
               len(ps), "" if len(ps) == 1 else "s",
               "".join("<li>%s</li>" % esc(s["question"]) for s in samples),
               esc(TOPICS[t]["name"].lower())))

    body = """<div class="libwrap">
<section class="promise"><h2 id="what-moved">What moved, and when</h2>
<p>This site is a reference, so the useful kind of recency is not
&ldquo;what did you publish this week&rdquo; &mdash; it is
<b>which numbers have changed under you</b>. Every page carries the month it was
last checked. These are the figures that actually moved.</p>
%s
<p><a href="changes.html">The whole log, with sources &rarr;</a></p></section>

<section class="sec"><h2 id="calculators">Start with a number</h2>
<p>Seven calculators. You type your own figures in; nothing is stored, nothing
is sent anywhere, and every result traces to a rate or a statute you can click
through to.</p>
<div class="lcg">%s</div>
<p><a href="calculators.html">All seven, with what each one needs from you
&rarr;</a></p></section>

<section class="sec alt"><h2 id="questions">Or start with the question</h2>
<p>The twenty questions people arrive with most often. <b>This is a selection,
not the whole list</b> &mdash; there are %d pages on this site, and the honest
place to see all of them is the full index.</p>
<div class="lcg two">%s</div>
<p><a href="questions.html">All %d questions &rarr;</a></p></section>

<section class="sec"><h2 id="topics">Or browse by what you are dealing with</h2>
<p>Five areas. Every page on the site sits in exactly one of them, so a topic
page is the complete answer to &ldquo;what do you have on this?&rdquo;</p>
<div class="tcg">%s</div></section>

%s
<section class="sec alt"><h2 id="directories">Two directories</h2>
<p>Where a set is large enough that a list beats an article, it gets its own
filterable directory rather than a paragraph.</p>
<div class="lcg">%s</div></section>
%s
%s
</div>""" % (changes_block(4),
             "".join(card(p) for p in calcs),
             len([p for p in REG["pages"] if not p.get("skip")]),
             "".join(row(p, show_topic=True) for p in qs),
             len([p for p in REG["pages"] if not p.get("skip")
                  and p["format"] != "reference"]),
             "".join(tcards),
             STAGE,
             "".join(card(p) for p in dirs),
             '<section class="sec"><h2 id="reference">The reference list</h2>'
             "<p>Seventy-eight outbound links, checked by hand: the Board, the "
             "payers, the associations, the statutes. Collapsed because most "
             "people want one of them, not all of them.</p>"
             '<details class="reffold"><summary>Open the reference list'
             "</summary>%s</details></section>" % REFLIST,
             PROVENANCE)

    b = band("Everything on this site",
             "Start with a number, a question, or the thing "
             "<em>you are actually dealing with</em>.",
             "Seven calculators, two directories and %d pages of California-"
             "specific reference &mdash; each one stamped with the month it was "
             "last checked against the source."
             % len([p for p in REG["pages"] if not p.get("skip")]),
             [("Therapist Support", "index.html"), ("Everything", None)],
             ["California", "Updated " + UPDATED,
              "%d pages" % len([p for p in REG["pages"] if not p.get("skip")])])
    return page(
        "Everything on Therapist Support: calculators, guides and directories "
        "for California therapists",
        "Seven calculators, 65 graduate programmes, 16 psychedelic-assisted "
        "therapy trainings and California-specific reference on money, "
        "licensure, getting paid, running a practice and training — each page "
        "stamped with the month it was last checked.",
        "resources.html", 0, b, body,
        [("Therapist Support", "index.html"), ("Everything", "resources.html")])


def build_topic(t):
    T = TOPICS[t]
    ps = topic_pages(t)
    calcs = [p for p in ps if p["format"] == "calculator"]
    secs = []
    if calcs:
        secs.append('<section class="sec"><h2 id="tools">%s tools</h2>'
                    '<div class="lcg">%s</div></section>'
                    % (esc(T["name"]),
                       "".join(card(p, up="../") for p in calcs)))
    for c in T["clusters"]:
        items = [PAGES[f] for f in c["files"]
                 if f in PAGES and not PAGES[f].get("skip")]
        items = [p for p in items if p["format"] != "calculator"]
        if not items:
            continue
        secs.append('<section class="sec alt"><h2 id="%s">%s</h2>'
                    '<div class="lcg">%s</div></section>'
                    % (re.sub(r"[^a-z0-9]+", "-", c["name"].lower()).strip("-"),
                       esc(c["name"]),
                       "".join(card(p, up="../") for p in items)))

    others = "".join(
        '<a class="xt" href="../%s"><b>%s</b><span>%s</span></a>'
        % (hub_path(o), esc(TOPICS[o]["name"]), esc(TOPICS[o]["tagline"]))
        for o in ORDER if o != t)

    body = ('<div class="libwrap"><section class="intro">%s</section>%s'
            '<section class="sec"><h2 id="elsewhere">The other four areas</h2>'
            '<div class="xtg">%s</div>'
            '<p><a href="../resources.html">Everything on the site &rarr;</a> '
            '&middot; <a href="../questions.html">Every question &rarr;</a></p>'
            "</section></div>"
            % ("".join("<p>%s</p>" % esc(x) for x in T["intro"]),
               "".join(secs), others))

    b = band("%d pages" % len(ps), esc(T["name"]), esc(T["tagline"]),
             [("Therapist Support", "index.html"),
              ("Everything", "resources.html"), (T["name"], None)],
             ["California", "Updated " + UPDATED], up="../")
    return page(
        "%s for California therapists — %s" % (T["name"], T["tagline"]),
        "%s %s" % (T["tagline"], T["intro"][0][:150]),
        hub_path(t), 1, b, body,
        [("Therapist Support", "index.html"),
         ("Everything", "resources.html"), (T["name"], hub_path(t))])


def build_questions():
    groups = []
    for t in ORDER:
        ps = sorted(topic_pages(t), key=lambda p: p["question"].lower())
        if not ps:
            continue
        groups.append('<section class="sec"><h2 id="%s">%s <span class="ct">%d'
                      "</span></h2><p>%s</p>"
                      '<p><a href="%s">The %s hub, with orientation and the '
                      'calculators &rarr;</a></p><div class="lrg">%s</div>'
                      "</section>"
                      % (t, esc(TOPICS[t]["name"]), len(ps),
                         esc(TOPICS[t]["tagline"]), hub_path(t),
                         esc(TOPICS[t]["name"].lower()),
                         "".join(row(p) for p in ps)))
    dirs = [p for p in REG["pages"] if p["format"] == "directory"]
    groups.append(
        '<section class="sec"><h2 id="directories">The two directories '
        '<span class="ct">%d</span></h2>'
        "<p>Eighty-one pages sit inside the two directories &mdash; one per "
        "graduate programme and one per training. They are not listed "
        "individually here because a list of sixty-five schools is a directory, "
        "not an index; the directories themselves filter and compare them, "
        "which is what you actually want.</p>"
        '<div class="lcg">%s</div></section>'
        % (len(leaves()), "".join(card(p) for p in dirs)))
    n = sum(len(topic_pages(t)) for t in ORDER) + len(leaves())
    body = ('<div class="libwrap"><section class="intro">'
            "<p>Every page on this site, phrased as the question it answers, "
            "grouped by area and alphabetical within each. <b>This list is "
            "complete</b> &mdash; that is the only thing it is for. If a "
            "question you have is not here, the site does not answer it yet, "
            'and <a href="contact.html">that is worth telling me</a>.</p>'
            "</section>%s</div>" % "".join(groups))
    b = band("Complete index", "Every question this site answers.",
             "All %d pages, phrased as the question people arrive with." % n,
             [("Therapist Support", "index.html"),
              ("Everything", "resources.html"), ("Every question", None)],
             ["%d questions" % n, "Updated " + UPDATED])
    return page(
        "Every question answered on Therapist Support — the complete index",
        "The complete index of every page on Therapist Support, phrased as the "
        "question it answers and grouped by area. %d pages." % n,
        "questions.html", 0, b, body,
        [("Therapist Support", "index.html"), ("Everything", "resources.html"),
         ("Every question", "questions.html")])


def build_calculators():
    calcs = sorted((p for p in REG["pages"]
                    if p["format"] == "calculator" and not p.get("skip")),
                   key=lambda p: (p["topic"], -p["weight"]))
    secs = []
    for t in ORDER:
        ps = [p for p in calcs if p["topic"] == t]
        if ps:
            secs.append('<section class="sec"><h2 id="%s">%s</h2>'
                        '<div class="lcg">%s</div></section>'
                        % (t, esc(TOPICS[t]["name"]), "".join(card(p) for p in ps)))
    body = ('<div class="libwrap"><section class="intro">'
            "<p>Seven calculators, grouped by what they are about. All of them "
            "run entirely in your browser: nothing you type is stored, nothing "
            "is sent anywhere, and there is no account. Every figure they "
            "produce traces back to a published rate, limit or statute that is "
            "linked from the tool itself.</p>"
            "<p>They are the reason most people come back, which is why they "
            "have a page of their own rather than being scattered through the "
            "reference.</p></section>%s"
            '<p><a href="resources.html">Everything on the site &rarr;</a></p>'
            "</div>" % "".join(secs))
    b = band("%d calculators" % len(calcs),
             "The calculators.",
             "Your own numbers in, a real figure out &mdash; and a link to the "
             "rate or statute behind every line.",
             [("Therapist Support", "index.html"),
              ("Everything", "resources.html"), ("Calculators", None)],
             ["California", "Updated " + UPDATED])
    return page(
        "Free calculators for California therapists — take-home, tax, "
        "cost of living and practice growth",
        "Seven free calculators for California therapists: practice take-home, "
        "tax and retirement strategy, cost of living, the 3,000 associate "
        "hours, and what a client is worth. Nothing stored, nothing sent.",
        "calculators.html", 0, b, body,
        [("Therapist Support", "index.html"), ("Everything", "resources.html"),
         ("Calculators", "calculators.html")])


def build_changes():
    rows = "".join(
        '<li><time>%s</time><div><p>%s</p>'
        '<a href="%s">the page that carries it &rarr;</a>%s</div></li>'
        % (esc(c["date"]), esc(c["what"]), esc(c["where"]),
           (' <a href="%s" target="_blank" rel="noopener noreferrer">source '
            "&nearr;</a>" % esc(c["src"])) if c.get("src") else "")
        for c in CHANGES)
    body = ('<div class="libwrap"><section class="intro">'
            "<p>A log of <b>numbers that moved</b> &mdash; fees, limits, rates, "
            "panel status, accreditation actions &mdash; not a list of pages "
            "that were published. On a site whose whole claim is that the "
            "figures are checked, this is the proof of the claim.</p>"
            "<p>Every entry links to the page that carries the number and, "
            "where one exists, to the primary source. If you spot something "
            'that has moved and is not here, <a href="contact.html">tell '
            "me</a>.</p></section>"
            '<section class="sec"><ol class="chglog">%s</ol></section>'
            '<p><a href="resources.html">Everything on the site &rarr;</a></p>'
            "</div>" % rows)
    b = band("Changelog", "What changed, and when.",
             "The figures on this site that have moved, most recent first, "
             "each with the page it affects and the source it came from.",
             [("Therapist Support", "index.html"),
              ("Everything", "resources.html"), ("What changed", None)],
             ["%d entries" % len(CHANGES), "Updated " + UPDATED])
    return page(
        "What changed: fees, limits and rates that moved for California therapists",
        "A log of the numbers that have moved — BBS fees, contribution limits, "
        "SDI rates, insurance panel status — each with the page it affects and "
        "its source.",
        "changes.html", 0, b, body,
        [("Therapist Support", "index.html"), ("Everything", "resources.html"),
         ("What changed", "changes.html")])


CSS = """<style>/* library */
.lib{--pine:#2C6350;--amber:#F6C560;--ink:#17271F;--line:#E2DACA;--mut:#7C8878;
  --green:#3F9577}
.libband{background:linear-gradient(135deg,#14261E 0%,#1B4536 48%,#2C6350 100%);
  color:#EFF5F2;padding:32px 0 38px}
.libband .in{max-width:1120px;margin:0 auto;padding:0 26px}
.libband .bcr{display:flex;flex-wrap:wrap;align-items:center;gap:4px 8px;margin:0 0 14px;
  padding:0;list-style:none;font-family:'IBM Plex Mono',ui-monospace,monospace;
  font-size:10.4px;letter-spacing:.1em;text-transform:uppercase}
.libband .bcr li{display:flex;align-items:center;gap:8px}
.libband .bcr a{color:#EFF5F2;opacity:.66;text-decoration:none;padding:5px 0;
  min-height:26px;display:inline-flex;align-items:center;border-bottom:1px solid transparent}
.libband .bcr a:hover{opacity:1;border-bottom-color:currentColor}
.libband .bcr .sep{opacity:.36}
.libband .bcr [aria-current]{opacity:.95;font-weight:600;color:var(--amber)}
.libband .sub{font-family:'IBM Plex Mono',monospace;font-size:11px;letter-spacing:.11em;
  text-transform:uppercase;color:var(--amber);margin:0 0 12px}
.libband h1{font-family:Fraunces,Georgia,serif;font-size:clamp(26px,3.6vw,41px);
  line-height:1.07;font-weight:600;letter-spacing:-.02em;color:#fff;margin:0 0 13px;
  max-width:19ch}
.libband h1 em{font-style:normal;color:var(--amber)}
.libband .dek{font-size:15.4px;line-height:1.72;color:rgba(255,255,255,.87);margin:0;
  max-width:62ch}
.libmeta{display:flex;gap:14px;flex-wrap:wrap;margin-top:18px;
  font-family:'IBM Plex Mono',monospace;font-size:10.4px;letter-spacing:.06em;
  text-transform:uppercase;color:rgba(255,255,255,.62)}

.libwrap{max-width:1120px;margin:0 auto;padding:8px 26px 20px}
.lib .sec,.lib .intro,.lib .promise{padding:30px 0 6px;border-top:1px solid #EFEADC}
.lib .intro,.lib .promise{border-top:0;padding-top:28px}
.lib h2{font-family:Fraunces,Georgia,serif;font-size:clamp(21px,2.5vw,27px);
  line-height:1.2;font-weight:600;color:var(--ink);margin:0 0 12px;scroll-margin-top:18px}
.lib h2 .ct{font-family:'IBM Plex Mono',monospace;font-size:12px;color:var(--mut);
  margin-left:8px;vertical-align:middle}
.lib p{font-size:15.4px;line-height:1.78;color:#3B4A38;margin:0 0 15px;max-width:68ch}
.lib .libwrap>p,.lib .sec>p{max-width:68ch}
.lib a{color:var(--pine)}

.lcg{display:grid;grid-template-columns:repeat(auto-fill,minmax(268px,1fr));gap:11px;
  margin:14px 0 8px}
.lcg.two{grid-template-columns:repeat(auto-fill,minmax(330px,1fr))}
.lc{display:flex;flex-direction:column;background:#fff;border:1px solid var(--line);
  border-radius:12px;padding:15px 17px;text-decoration:none;min-width:0}
.lc:hover{background:#FBFAF6;border-color:#CFC7B4}
.lch{display:flex;flex-wrap:wrap;align-items:center;gap:6px;margin-bottom:8px}
.lc b{font-family:Fraunces,Georgia,serif;font-size:16.5px;line-height:1.28;
  font-weight:600;color:var(--ink);margin-bottom:6px}
.lco{font-size:13.4px;line-height:1.6;color:#4A5A46;flex:1}
.cnum{display:inline-block;margin-top:9px;font-family:'IBM Plex Mono',monospace;
  font-size:11.6px;color:var(--pine);background:#EAF3DE;padding:4px 9px;border-radius:5px;
  align-self:flex-start}
.fchip{font-family:'IBM Plex Mono',monospace;font-size:9.2px;letter-spacing:.09em;
  text-transform:uppercase;padding:4px 8px;border-radius:5px;white-space:nowrap}
.f-calculator{background:#EAF3DE;color:#27500A}
.f-guide{background:#E8EFF6;color:#2A4C6B}
.f-answer{background:#F3EFE4;color:#7A6B4A}
.f-directory{background:#FBF0E2;color:#8A5A22}
.f-reference{background:#EFEDE7;color:#6B6A63}
.tchip{font-family:'IBM Plex Mono',monospace;font-size:9.2px;letter-spacing:.08em;
  text-transform:uppercase;color:var(--mut)}
.chk{margin-left:auto;font-family:'IBM Plex Mono',monospace;font-size:9.2px;
  letter-spacing:.06em;text-transform:uppercase;color:#A79E88;white-space:nowrap}

.lrg{display:grid;gap:5px;margin:12px 0 6px}
.lr{display:flex;align-items:center;flex-wrap:wrap;gap:9px;background:#fff;
  border:1px solid var(--line);border-radius:9px;padding:11px 14px;text-decoration:none;
  min-width:0}
.lr:hover{background:#FBFAF6}
.lr b{flex:1;min-width:180px;font-size:14.6px;line-height:1.4;color:var(--ink);
  font-weight:500}

.tcg{display:grid;grid-template-columns:repeat(auto-fill,minmax(258px,1fr));gap:12px;
  margin:14px 0 8px}
.tcard{display:block;background:#fff;border:1px solid var(--line);border-radius:13px;
  padding:18px 20px;text-decoration:none;min-width:0;border-top:3px solid var(--pine)}
.tcard:hover{background:#FBFAF6}
.tcard.t-money{border-top-color:#3F9577}
.tcard.t-licensure{border-top-color:#2C6350}
.tcard.t-getting-paid{border-top-color:#C98B4B}
.tcard.t-practice{border-top-color:#5B7FA6}
.tcard.t-training{border-top-color:#8A6BA6}
.tcard>b{display:block;font-family:Fraunces,Georgia,serif;font-size:20px;
  color:var(--ink);margin-bottom:5px}
.tcard .tt{display:block;font-size:13.6px;line-height:1.55;color:#4A5A46;margin-bottom:9px}
.tcard .tn{display:block;font-family:'IBM Plex Mono',monospace;font-size:9.6px;
  letter-spacing:.09em;text-transform:uppercase;color:var(--mut);margin-bottom:10px}
.tcard ul{margin:0 0 12px;padding:0;list-style:none;border-top:1px solid #F0EBDE}
.tcard li{font-size:13px;line-height:1.5;color:#5A6A56;padding:7px 0;
  border-bottom:1px solid #F6F3EA}
.tcard li:last-child{border-bottom:0}
.tcard .go{font-size:13px;color:var(--pine);font-weight:500}

.xtg{display:grid;grid-template-columns:repeat(auto-fit,minmax(210px,1fr));gap:10px;
  margin:12px 0}
.xt{display:block;background:#fff;border:1px solid var(--line);border-radius:10px;
  padding:13px 15px;text-decoration:none;min-width:0}
.xt:hover{background:#FBFAF6}
.xt b{display:block;font-family:Fraunces,Georgia,serif;font-size:15.5px;color:var(--ink);
  margin-bottom:3px}
.xt span{display:block;font-size:12.6px;line-height:1.5;color:#4A5A46}

.chg{list-style:none;margin:12px 0;padding:0;display:grid;gap:8px}
.chg li{display:grid;grid-template-columns:92px minmax(0,1fr);gap:14px;
  background:#FBF6E9;border-radius:10px;padding:13px 16px;align-items:baseline}
.chg time{font-family:'IBM Plex Mono',monospace;font-size:11px;color:#8A7B58;
  letter-spacing:.04em}
.chg span{font-size:14.2px;line-height:1.6;color:#3B4A38}
.chg a{display:block;margin-top:5px;font-family:'IBM Plex Mono',monospace;
  font-size:9.6px;letter-spacing:.07em;text-transform:uppercase}
.chglog{list-style:none;margin:12px 0;padding:0;display:grid;gap:9px}
.chglog li{display:grid;grid-template-columns:104px minmax(0,1fr);gap:16px;
  border-left:3px solid var(--amber);background:#fff;border-radius:0 10px 10px 0;
  padding:14px 17px}
.chglog time{font-family:'IBM Plex Mono',monospace;font-size:11.4px;color:var(--mut)}
.chglog p{margin:0 0 6px;font-size:14.6px;line-height:1.66}
.chglog a{font-family:'IBM Plex Mono',monospace;font-size:9.6px;letter-spacing:.07em;
  text-transform:uppercase;margin-right:10px}

.reffold{border:1px solid var(--line);border-radius:11px;background:#fff;margin:12px 0}
.reffold summary{cursor:pointer;padding:15px 18px;font-family:'IBM Plex Mono',monospace;
  font-size:10.6px;letter-spacing:.09em;text-transform:uppercase;color:var(--pine)}
.reffold[open] summary{border-bottom:1px solid #F0EBDE}
.reffold .sec{border-top:0;padding-top:12px}

@media (max-width:560px){
  .lcg,.lcg.two,.tcg{grid-template-columns:minmax(0,1fr)}
  .chg li,.chglog li{grid-template-columns:minmax(0,1fr);gap:5px}
  .chk{margin-left:0}
}
</style>"""


# ---------------------------------------------------------------- main

def main():
    os.makedirs(OUT, exist_ok=True)
    written = [("resources.html", build_hub()),
               ("questions.html", build_questions()),
               ("calculators.html", build_calculators()),
               ("changes.html", build_changes())]
    for t in ORDER:
        d = os.path.join(OUT, t)
        os.makedirs(d, exist_ok=True)
        written.append(("%s/index.html" % t, build_topic(t)))
    for fn, doc in written:
        open(os.path.join(OUT, fn), "w", encoding="utf-8").write(doc)

    bad = []
    live = {f for f in os.listdir(SITE) if f.endswith(".html")}
    for fn, doc in written:
        if doc.count("<h1") != 1:
            bad.append("%s: %d h1" % (fn, doc.count("<h1")))
        if not re.search(r"<script>[\s\S]*?navpanel[\s\S]*?</script>", doc):
            bad.append("%s: dead header" % fn)
        if '"@type":"BreadcrumbList"' not in doc:
            bad.append("%s: no breadcrumb data" % fn)
        # Nothing may link to a page that does not exist. A generated listing
        # makes this failure silent and site-wide rather than local.
        depth = fn.count("/")
        for href in re.findall(r'href="([^"#?]+\.html)(?:[#?][^"]*)?"', doc):
            if href.startswith("http"):
                continue
            # On a subdirectory page a bare relative href does not resolve to
            # the root - it resolves to a sibling that does not exist. The old
            # version of this loop `continue`d on exactly this case, which
            # exempted the only place the bug could happen. Flag it instead.
            if depth and not href.startswith("../"):
                bad.append("%s: bare relative href %r - from a subdirectory "
                           "this resolves to a sibling, not the root" % (fn, href))
                break
            tgt = href[3:] if href.startswith("../") else href
            if "/" in tgt:
                continue
            if tgt not in live and tgt not in [w[0] for w in written]:
                bad.append("%s: links to missing %s" % (fn, tgt))
                break
    # Every non-skipped page must be reachable from questions.html. That is the
    # whole point of it, and an orphan is invisible to a reader and nearly
    # invisible to a crawler.
    q = dict(written)["questions.html"]
    for p in REG["pages"]:
        if p.get("skip") or p.get("leaf"):
            continue
        if ('href="%s"' % p["file"]) not in q:
            bad.append("questions.html does not reach %s" % p["file"])
    # The hub must not claim completeness - that is the promise it can no
    # longer keep, and the reason it was rebuilt.
    hub = dict(written)["resources.html"]
    if "This is a selection" not in hub:
        bad.append("the hub no longer says its question list is a selection")
    if bad:
        sys.exit("build_library: " + "; ".join(sorted(set(bad))[:8]))

    n = len([p for p in REG["pages"] if not p.get("skip")])
    print("%d pages built · %d registered pages · %d topics · %d changes"
          % (len(written), n, len(ORDER), len(CHANGES)))
    for t in ORDER:
        print("   %-14s %2d pages, %d clusters"
              % (TOPICS[t]["name"], len(topic_pages(t)), len(TOPICS[t]["clusters"])))


if __name__ == "__main__":
    main()
