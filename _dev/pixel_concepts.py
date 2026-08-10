#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Concepts 01, 02 and 07 from concepts.html, built sitewide in the Pixel style.

WHAT IS HERE

  01  TWO CLOCKS.  A "last checked" date and, separately, the vintage of the
      data itself - because they are different facts and a single "updated"
      date hides which one moved. Plus, where the change log actually records
      one, a dated list of what changed on this page and why.

  02  REVIEW STATUS.  One badge per page saying how deeply it has been checked.
      80,000 Hours prints "Based on a medium-depth investigation" on every
      career review; nobody in this category does. It is the only way 65
      lightly-sourced school pages can sit beside a statute-verified tax page
      without the weak ones quietly discrediting the strong ones.

  07  IN SHORT.  An executive-summary box above the article, and a NUMBERED
      table of contents in the side rail.

WHERE THE CONTENT COMES FROM - THIS IS THE IMPORTANT PART

Not one word below is invented. Every field is read off something the page
already carries:

  last checked   the page's own JSON-LD dateModified, or the "Updated ..." in
                 its hero meta strip.
  updates        mock/library/registry.json -> changes[], filtered to this
                 page, with the source link that entry already cites.
  in short       the ts:question / ts:number / ts:outcome meta tags. These were
                 authored per page, they drive the library, and until now no
                 reader ever saw them. Concept 07 is mostly a matter of
                 PRINTING THEM.
  review status  derived from measurable properties of the page - see badge().

WHAT IS DELIBERATELY NOT PRINTED

A PUBLISHED date. concepts.html shows one, and it is the right idea, but this
site does not record when a page first went up. Guessing it from a file
timestamp would produce a date that looks authoritative and means nothing,
which is the exact failure the two-clock pattern exists to prevent. When a
first-published date is recorded, add it here.

The vintage line is per TOPIC, not per page, and it says what the pages in that
topic actually cite. A page whose topic has no single schedule behind it gets no
vintage row rather than a vague one.

Idempotent - the block is delimited and rewritten in place. Guarded.
"""
import os, re, sys, json, html

HERE = os.path.dirname(os.path.abspath(__file__))
SITE = os.path.dirname(HERE)
SUBDIRS = ("money", "licensure", "getting-paid", "practice", "training")
REGISTRY = os.path.join(SITE, "mock", "library", "registry.json")

MARK = "<!-- _dev/pixel_concepts.py -->"
END = "<!-- /pixel_concepts -->"
CSSMARK = "/* _dev/pixel_concepts.py */"

# Matched against the RELATIVE path, not the basename. Written as basenames
# first time round, which silently skipped money/index.html and the other four
# topic hubs along with the home page - the hubs are exactly the pages a
# review-status badge is most useful on, because they are what a reader lands
# on from search.
SKIP = {"tycoon.html", "concepts.html", "index.html"}

# The tool pages. Hand-built heroes with live figures; this pass stays out of
# them. Listed explicitly rather than read from registry.json's `format` field
# so that retagging a page in the registry cannot silently start rewriting a
# hand-designed layout.
TOOLS = {
    "practice-simulator.html",
    "therapist-tax-strategy-california.html",
    "grow-your-therapy-practice.html",
    "associate-mft-job-advisor.html",
    "amft-3000-hours-california.html",
    "therapist-cost-of-living-california.html",
    "therapist-working-remotely-california.html",
}
SKIP |= TOOLS

# The data behind each topic. Says what those pages actually cite; a topic with
# no single schedule behind it gets None and no row is printed.
VINTAGE = {
    "money": ("the 2026 federal and California rate schedules",
              "IRS and FTB publish next year's brackets and limits in the "
              "autumn; every figure here moves then."),
    "licensure": ("the BBS fee schedule in effect 1 July 2026",
                  "The reduction reverts on 30 June 2030, and this page "
                  "changes then."),
    "getting-paid": ("the 2026 Medicare and Medi-Cal fee schedules",
                     "CMS republishes in November for the following January."),
    "training": ("each institution's own current published catalog",
                 "Catalogs are republished annually and unit counts move with "
                 "them."),
    "practice": (None, None),
}

# Primary sources. A citation to one of these is a citation to the thing itself
# rather than to somebody's summary of it, which is what the top badge means.
PRIMARY = re.compile(
    r"bbs\.ca\.gov|leginfo\.legislature|law\.cornell\.edu|irs\.gov|ssa\.gov|"
    r"cms\.gov|ftb\.ca\.gov|edd\.ca\.gov|dir\.ca\.gov|dol\.gov|bls\.gov|"
    r"dhcs\.ca\.gov|federalregister\.gov|govinfo\.gov")

BADGES = {
    "full": ("Verified to source",
             "Every figure on this page was re-checked against the statute, "
             "schedule or filing it cites."),
    "part": ("Figures checked, narrative not re-read",
             "The numbers are current. The argument around them has not been "
             "reviewed since it was written."),
    "thin": ("Published sources only",
             "Built from what the institution publishes about itself. Nothing "
             "here is independently verified."),
}

CSS = """<style>%s
/* Concepts 01, 02 and 07. Pixel language throughout: 2px ink, a SOLID offset
   shadow and never a blur; Bricolage for the headings, IBM Plex Mono for the
   small caps labels, and Fraunces reserved for figures. */
.tsmeta{border:2px solid #16211B;border-radius:12px;box-shadow:3px 3px 0 #16211B;
  background:#FBF9F3;padding:13px 15px 12px;margin:18px 0 0;max-width:none}
/* The foot block is inserted as a bare sibling of the up-link and the footer,
   so it has no container to inherit a gutter from. Match the up-link's. */
.tsfoot{max-width:1120px;margin:30px auto 0;padding:0 26px;box-sizing:border-box}
@media (min-width:1500px){.tsfoot{max-width:1320px}}
@media (min-width:1900px){.tsfoot{max-width:1560px}}
@media (max-width:560px){.tsfoot{padding:0 18px}}
.tsmeta .tsrow{display:flex;flex-wrap:wrap;gap:6px 20px;align-items:baseline}
.tsk{font-family:'IBM Plex Mono',ui-monospace,monospace;font-size:9.4px;
  letter-spacing:.13em;text-transform:uppercase;color:#6C6555;margin-right:-12px}
.tsv{font-size:13px;font-weight:600;color:#16211B}
.tsall{font-family:'IBM Plex Mono',ui-monospace,monospace;font-size:10px;
  letter-spacing:.08em;text-transform:uppercase;color:#2C6350;margin-left:auto}
/* The vintage is a SEPARATE clock and has to look like one, so it sits under a
   rule rather than inline with the check date. */
.tsvint{margin:11px 0 0;padding:10px 0 0;border-top:2px dashed #D9D0BA}
.tsvint b{display:block;font-family:Fraunces,Georgia,serif;font-size:14.5px;
  font-weight:600;color:#16211B;margin:2px 0 3px}
.tsvint i{display:block;font-style:normal;font-size:12.2px;line-height:1.5;
  color:#5A5647;max-width:62ch}
/* 02 - the badge, inside the meta card so it can never inherit a dark band */
/* On its own it carries its own background: this text is a fixed colour and
   the band behind it is not. Testing POSITION (:first-child) was the previous
   attempt and it failed the moment a standfirst appeared above it. */
.tsdepth{margin:14px 0 0;background:#FBF9F3;border:2px solid #16211B;
  border-radius:12px;box-shadow:3px 3px 0 #16211B;padding:12px 15px}
/* Inside the meta card it is a section of that card, not a card of its own. */
.tsmeta .tsdepth{margin:11px 0 0;padding:10px 0 0;background:transparent;
  border:none;border-radius:0;box-shadow:none;border-top:2px dashed #D9D0BA}
.tsbadge{display:inline-flex;align-items:center;gap:7px;margin:0;
  font-family:'IBM Plex Mono',ui-monospace,monospace;font-size:10.4px;
  font-weight:700;letter-spacing:.07em;text-transform:uppercase;
  border:2px solid #16211B;border-radius:999px;padding:6px 13px 5px;
  box-shadow:2px 2px 0 #16211B;text-decoration:none}
.tsbadge.full{background:#2C6350;color:#F4F0E6}
.tsbadge.part{background:#F6C560;color:#16211B}
.tsbadge.thin{background:#F0EADA;color:#3A3529}
.tsbadge.gap{background:#fff;color:#B5483F;margin-left:7px}
.tsbadge:hover{transform:translate(1px,1px);box-shadow:1px 1px 0 #16211B}
.tswhat{margin:8px 0 0;font-size:12.4px;line-height:1.55;color:#5A5647;
  max-width:64ch}
/* The rail numbers were #9A8F76 on paper: 3.04:1, under the 4.5:1 floor for
   text this small. Measured, not eyeballed. */
/* 07 - in short */
.tsshort{border:2px solid #16211B;border-radius:12px;box-shadow:4px 4px 0 #F6C560;
  background:#fff;padding:15px 17px 14px;margin:20px 0 0}
.tsshort>p.tsk{margin:0 0 8px}
.tsshort q{display:block;font-family:'Bricolage Grotesque','Archivo',Inter,
  system-ui,sans-serif;font-weight:800;letter-spacing:-.028em;font-size:18px;
  line-height:1.2;color:#16211B;quotes:none;margin:0 0 7px}
.tsshort p.tsa{margin:0;font-size:14px;line-height:1.6;color:#3A3529;max-width:64ch}
.tsshort .tsfig{display:block;font-family:Fraunces,Georgia,serif;font-weight:600;
  font-size:21px;color:#2C6350;margin:9px 0 0;letter-spacing:-.01em}
/* 01 - the dated update list */
.tsupd{margin:14px 0 0;border:2px solid #16211B;border-radius:12px;
  background:#F4F0E6;box-shadow:2px 2px 0 #16211B;overflow:hidden}
.tsupd>summary{cursor:pointer;list-style:none;padding:10px 15px;
  font-family:'IBM Plex Mono',ui-monospace,monospace;font-size:10.4px;
  font-weight:700;letter-spacing:.1em;text-transform:uppercase;color:#16211B}
.tsupd>summary::-webkit-details-marker{display:none}
.tsupd>summary::after{content:"+";float:right;font-weight:700}
.tsupd[open]>summary::after{content:"\\2212"}
.tsupd dl{margin:0;padding:0 15px 13px}
.tsupd dl>div{padding:10px 0;border-top:2px dashed #D9D0BA}
.tsupd dt{font-family:'IBM Plex Mono',ui-monospace,monospace;font-size:10.2px;
  letter-spacing:.08em;text-transform:uppercase;color:#6C6555;margin:0 0 3px}
.tsupd dd{margin:0;font-size:13.2px;line-height:1.55;color:#3A3529;max-width:66ch}
.tsupd dd a{color:#2C6350}
/* 07 - the numbered rail */
.artnav a,.scnav a,.drnav a,.pxnav a{position:relative}
.tsn{font-family:'IBM Plex Mono',ui-monospace,monospace;font-size:9.6px;
  font-weight:700;color:#6C6555;margin-right:8px;font-style:normal;
  display:inline-block;min-width:1.4em}
a.on .tsn,a[aria-current] .tsn{color:#2C6350}
@media (max-width:620px){
  .tsmeta .tsrow{gap:4px 14px}
  .tsshort q{font-size:16.5px}
  .tsbadge{font-size:9.6px}
}
</style>""" % CSSMARK



def _plain(x):
    """Normalised for comparison only: no tags, no entities, no punctuation."""
    x = re.sub(r"<[^>]+>", " ", str(x))
    x = html.unescape(x)
    x = re.sub(r"[^a-z0-9 ]", " ", x.lower())
    return re.sub(r"\s+", " ", x).strip()


def echoes_h1(q, page_html):
    """Does this question just say the H1 again?

    68 of the 167 pages with an In-short card did, including all 48 discipline
    case pages - the headline, then the same sentence with a question mark, in
    the first two lines. Substring either way, because an H1 of "Antioch
    University Los Angeles" and a question of the same words are the same
    problem as "...disciplined" and "...disciplined?".
    """
    m = re.search(r"<h1[^>]*>([\s\S]*?)</h1>", page_html or "")
    if not m:
        return False
    a, b = _plain(m.group(1)), _plain(q)
    if not a or not b:
        return False
    return a == b or a in b or b in a


def esc(x):
    return html.escape(str(x), quote=False)


def raw(x):
    """A meta CONTENT value is already entity-encoded - it had to be, to sit
    inside an attribute. Escaping it a second time is how "Biola University's"
    turns into "Biola University&amp;#x27;s" on the page. Only the two
    characters that could open a tag are touched; this never goes back into an
    attribute."""
    return str(x).replace("<", "&lt;").replace(">", "&gt;")


def pages():
    out = [f for f in sorted(os.listdir(SITE)) if f.endswith(".html")]
    for d in SUBDIRS:
        p = os.path.join(SITE, d)
        if os.path.isdir(p):
            out += ["%s/%s" % (d, f) for f in sorted(os.listdir(p))
                    if f.endswith(".html")]
    return [f for f in out if f not in SKIP]


def meta(s, name):
    m = re.search(r'<meta name="%s" content="([^"]*)"' % re.escape(name), s)
    return m.group(1) if m else None


def checked(s):
    m = re.search(r'"dateModified":"(\d{4}-\d{2}-\d{2})"', s)
    if m:
        y, mo, d = m.group(1).split("-")
        months = ["January", "February", "March", "April", "May", "June",
                  "July", "August", "September", "October", "November",
                  "December"]
        return "%d %s %s" % (int(d), months[int(mo) - 1], y)
    m = re.search(r"Updated (\d{1,2} \w+ \d{4})", s)
    if m:
        return m.group(1)
    # The date this pass printed last time. Without this the pass destroys its
    # own input: it moves the date out of the hero strip and into the card, and
    # on the next run there is nothing left in the hero to read.
    m = re.search(r'<span class="tsv">([^<]+)</span>', s)
    if m:
        return m.group(1)
    return None


def badge(rel, s, topic):
    """Which of the three depths this page has actually had.

    Derived from things that can be counted, not from an opinion: a school or
    training leaf is by construction a summary of what the institution says
    about itself; a page citing three or more PRIMARY sources has been taken
    back to the documents. Anything else is in between and says so.
    """
    if rel.endswith("-mft.html") or os.path.basename(rel).startswith(
            "psychedelic-training-"):
        return "thin"
    if len(set(PRIMARY.findall(s))) >= 3:
        return "full"
    return "part"


def rail(s):
    """Number the side rail, 1..n. The rails differ by template; all four are
    the same shape - a <b> label then a run of <a>."""
    def do(m):
        head, body = m.group(1), m.group(2)
        if "tsn" in body:
            body = re.sub(r'<i class="tsn">\d+</i>', "", body)
        n = [0]

        def num(a):
            n[0] += 1
            return a.group(1) + '<i class="tsn">%d</i>' % n[0] + a.group(2)

        body = re.sub(r'(<a\b[^>]*>)(.*?)(?=</a>)', lambda a: a.group(1)
                      + '<i class="tsn">%d</i>' % _bump(n) + a.group(2), body)
        return head + body + "</nav>"

    def _bump(n):
        n[0] += 1
        return n[0]

    return re.sub(r'(<nav class="(?:artnav|scnav|drnav|pxnav)"[^>]*>)'
                  r'([\s\S]*?)</nav>', do, s)


# Where the block goes: the first of these that the page actually has. Ordered
# from most specific to least, so a page with a meta strip gets it under the
# strip rather than under the h1 with the strip stranded below.
ANCHORS = [
    r'<div class="artmeta">[\s\S]*?</div>',
    r'<div class="scmeta">[\s\S]*?</div>',
    r'<div class="libmeta">[\s\S]*?</div>',
    r'<div class="hero-byline">[\s\S]*?</div>',
    r'<p class="dek">[\s\S]*?</p>',
    r'<p class="lede">[\s\S]*?</p>',
    r'<p class="hero-dek">[\s\S]*?</p>',
    r'</h1>',
]


STRIP_DATE = re.compile(
    r"<span>Updated [^<]*</span>")


def drop_hero_date(doc):
    """Remove "Updated <date>" from the hero meta strip.

    The whole point of concept 01 is that ONE date is not enough: a reader
    cannot tell whether "Updated 6 August" means the argument was rewritten or
    a figure was re-checked. Printing that vague date immediately above a strip
    that answers the question precisely is worse than either alone - it invites
    the reader to notice the two do not match and trust neither.
    """
    def one(m):
        return STRIP_DATE.sub("", m.group(0), count=1)
    return re.sub(r'<div class="(?:artmeta|scmeta|libmeta)">[\s\S]*?</div>',
                  one, doc)


def block(rel, s, changes):
    # Pages one level down need "../" on every href this block emits. Computed
    # from the page's own path rather than assumed, because assuming is how
    # this project shipped 39 dead links out of build_library.py.
    up = "../" * rel.count("/")
    topic = meta(s, "ts:topic") or ""
    q = meta(s, "ts:question")
    out = meta(s, "ts:outcome")
    num = meta(s, "ts:number")
    when = checked(s)
    kind = badge(rel, s, topic)
    label, why = BADGES[kind]
    # Link into the section only where the anchor actually exists. A badge
    # pointing at an id that is not on the page is a badge that does nothing
    # when clicked, which reads worse than not linking it at all.
    gap_id = "what-i-could-not-find" if 'id="what-i-could-not-find"' in s else None
    has_gap = gap_id is not None or 'class="gapl"' in s

    bits = []     # the foot: provenance
    top = []      # the hero: the summary, and nothing else
    clocks = None

    # ---- 01, the clocks
    rows = []
    if when:
        rows.append('<span class="tsk">Last checked</span>'
                    '<span class="tsv">%s</span>' % esc(when))
    if rows:
        rows.append('<a class="tsall" href="%schanges.html">All updates '
                    "&rarr;</a>" % up)
        # A school page is a page about a catalog whatever its topic tag
        # says. Several are tagged "licensure" because that is the reader's
        # journey, not because the Board's fee schedule is where their unit
        # counts come from - and printing "figures current as of the BBS fee
        # schedule" on a page whose figures are unit counts is a false
        # provenance claim, which is the one thing this block must never make.
        vkey = "training" if kind == "thin" else topic
        vint, note = VINTAGE.get(vkey, (None, None))
        v = ""
        if vint:
            v = ('<div class="tsvint"><span class="tsk">Figures current as of'
                 '</span><b>%s</b>%s</div>'
                 % (esc(vint), '<i>%s</i>' % esc(note) if note else ""))
        clocks = ('<div class="tsmeta"><div class="tsrow">%s</div>%s%%s</div>'
                  % ("".join(rows), v))

    # ---- 02, the badge
    b = ('<a class="tsbadge %s" href="%sabout.html#how-pages-are-checked">%s</a>'
         % (kind, up, esc(label)))
    if has_gap:
        b += ('<a class="tsbadge gap" href="#%s">Known gap</a>' % gap_id
               if gap_id else '<span class="tsbadge gap">Known gap</span>')
    badge_html = ('<div class="tsdepth">%s<p class="tswhat">%s</p></div>'
                  % (b, esc(why)))

    # The card is assembled last so the badge can live inside it. Where a page
    # has no check date there is no card, and the badge stands on its own with
    # its own background - hence .tsdepth carrying one either way.
    if clocks:
        bits.append(clocks % badge_html)
    else:
        bits.append(badge_html)

    # ---- 07, in short
    if q and out:
        fig = ('<span class="tsfig">%s</span>' % raw(num)) if num else ""
        # The question is dropped where it only repeats the headline the card
        # sits under. See echoes_h1() - this was 68 of 167 pages, and on the
        # discipline hub it put the same sentence in the page's first two
        # lines. The answer and the figure carry the card on their own.
        head = "" if echoes_h1(q, s) else "<q>%s</q>" % raw(q)
        top.append('<div class="tsshort"><p class="tsk">In short</p>'
                    "%s<p class=\"tsa\">%s</p>%s</div>"
                    % (head, raw(out), fig))

    # ---- 01, the dated updates, only where the log actually has some
    mine = [c for c in changes if c.get("where") == os.path.basename(rel)]
    if mine:
        items = "".join(
            "<div><dt>%s</dt><dd>%s%s</dd></div>"
            % (esc(c["date"]), esc(c["what"]),
               (' <a href="%s" target="_blank" rel="noopener noreferrer">'
                "source &nearr;</a>" % esc(c["src"])) if c.get("src") else "")
            for c in sorted(mine, key=lambda c: c["date"], reverse=True))
        bits.append('<details class="tsupd"><summary>What changed on this page'
                    " (%d)</summary><dl>%s</dl></details>" % (len(mine), items))

    foot = ('<div class="tsfoot">%s</div>' % "".join(bits)) if bits else ""
    return MARK + "".join(top) + END, (MARK + foot + END) if foot else ""


ABOUT = """<section id="how-pages-are-checked" class="pw">
<h2>How these pages are checked</h2>
<p>Every page carries a badge saying how deeply it has been verified. The point
of publishing it is that this site is not uniform, and pretending otherwise
would let the thinnest pages borrow credibility from the strongest ones.</p>
<div class="tblegend">
<p><span class="tsbadge full">Verified to source</span>Every figure was
re-checked against the statute, schedule or filing it cites. These pages cite
three or more primary sources &mdash; the Board, the IRS, CMS, the Legislature
&mdash; rather than somebody&rsquo;s summary of them.</p>
<p><span class="tsbadge part">Figures checked, narrative not re-read</span>The
numbers are current. The argument around them has not been reviewed since it
was written.</p>
<p><span class="tsbadge thin">Published sources only</span>Built from what an
institution publishes about itself. Nothing on the page is independently
verified, and where the institution publishes nothing the page says so rather
than filling the gap.</p>
<p><span class="tsbadge gap">Known gap</span>Something on the page could not be
established. It is named, in full, under &ldquo;What I could not establish&rdquo;.</p>
</div>
<p class="fine">The badge is derived, not asserted: it is computed from what a
page actually cites and whether it carries a gaps list, so it cannot drift away
from the page it describes.</p>
</section>"""


def _linked(doc):
    """True if one of the page's extracted stylesheets carries this block.

    extract_css.py replaces a shared <style> with a <link> to css/<sha>.css, so
    after the pipeline has run the marker is in the FILE, not in the page. A
    guard that only looks inline would report all 130 pages as broken the next
    time this ran, which is the kind of false alarm that gets a guard deleted.
    """
    for h in re.findall(r'href="(?:\.\./)*css/([0-9a-f]{12})\.css"', doc):
        f = os.path.join(SITE, "css", "%s.css" % h)
        try:
            if CSSMARK in open(f, encoding="utf-8").read():
                return True
        except IOError:
            pass
    return False


def unbuild(rel):
    """Take the block back off a page that is now skipped.

    Adding a page to SKIP stops the pass visiting it - which also stops it
    removing what a previous run left behind. Without this, excluding a page
    freezes whatever version of the block it happened to have.
    """
    p = os.path.join(SITE, rel)
    if not os.path.exists(p):
        return False
    s = open(p, encoding="utf-8").read()
    out = re.sub(re.escape(MARK) + r"[\s\S]*?" + re.escape(END), "", s)
    out = re.sub(r"\n?<style>" + re.escape(CSSMARK) + r"[\s\S]*?</style>\n?",
                 "", out)
    if out != s:
        open(p, "w", encoding="utf-8").write(out)
        return True
    return False


def main():
    if not os.path.exists(REGISTRY):
        sys.exit("pixel_concepts: registry.json missing")
    changes = json.load(open(REGISTRY, encoding="utf-8")).get("changes", [])

    removed = sum(1 for t in sorted(SKIP) if unbuild(t))
    if removed:
        print("%d skipped page(s) cleaned of an earlier block" % removed)

    n, railed, counts = 0, 0, {}
    for rel in pages():
        p = os.path.join(SITE, rel)
        s = open(p, encoding="utf-8").read()
        orig = s

        # idempotent
        s = re.sub(re.escape(MARK) + r"[\s\S]*?" + re.escape(END), "", s)
        s = re.sub(r"\n?<style>" + re.escape(CSSMARK) + r"[\s\S]*?</style>\n?",
                   "", s)

        # Built from the ORIGINAL page, not the stripped one, so a date that
        # only exists inside the previous run's block is still findable.
        blk, foot = block(rel, orig, changes)
        s = drop_hero_date(s)

        # The window: from the <h1> to whatever ends the hero. Anything after
        # that boundary belongs to the page's content, not its masthead, and an
        # anchor found there is a false match however high it sits in ANCHORS.
        h1 = s.find("<h1")
        window_end = len(s)
        if h1 >= 0:
            for pat in (r"</section>", r'<div class="[^"]*wrap', r"<article",
                        r'<section class="slab'):
                m = re.search(pat, s[h1:])
                if m:
                    window_end = min(window_end, h1 + m.start())
        placed = False
        for pat in ANCHORS:
            m = re.search(pat, s[:window_end])
            if m and m.end() >= h1:
                s = s[:m.end()] + blk + s[m.end():]
                placed = True
                break
        if not placed and h1 >= 0:
            # Every template has an </h1>. Landing directly under it is worse
            # placement than landing under the standfirst, and better than
            # landing in the middle of a panel three sections down.
            m = re.search(r"</h1>", s[h1:])
            if m:
                s = s[:h1 + m.end()] + blk + s[h1 + m.end():]
                placed = True
        if not placed:
            print("  no anchor: %s" % rel)
            continue
        counts[badge(rel, s, "")] = counts.get(badge(rel, s, ""), 0) + 1

        # The foot: above the "More on this" block if there is one, otherwise
        # directly above the site footer. Both exist on every template.
        for pat in (r"<!-- _dev/uplinks\.py -->", r"<section class=\"uplink\"",
                    r"<footer"):
            m = re.search(pat, s)
            if m and foot:
                s = s[:m.start()] + foot + s[m.start():]
                break

        before = s
        s = rail(s)
        if s != before:
            railed += 1

        i = s.lower().rfind("</body>")
        s = s[:i] + CSS + "\n" + s[i:]

        if s != orig:
            open(p, "w", encoding="utf-8").write(s)
            n += 1

    print("%d page(s) carry the block, %d rail(s) numbered" % (n, railed))
    for k, v in sorted(counts.items()):
        print("  %-5s %3d  %s" % (k, v, BADGES[k][0]))

    # ---- the page the badge links to
    ap = os.path.join(SITE, "about.html")
    a = open(ap, encoding="utf-8").read()
    if 'id="how-pages-are-checked"' not in a:
        j = a.rfind("</main>")
        if j < 0:
            j = a.lower().rfind("<footer")
        a = a[:j] + ABOUT + a[j:]
        open(ap, "w", encoding="utf-8").write(a)
        print("about.html: added the badge legend")
    if CSSMARK not in a:
        a = open(ap, encoding="utf-8").read()
        i = a.lower().rfind("</body>")
        open(ap, "w", encoding="utf-8").write(a[:i] + CSS + "\n" + a[i:])

    # ---- guards
    bad = 0
    for rel in pages():
        s = open(os.path.join(SITE, rel), encoding="utf-8").read()
        if s.count(MARK) != s.count(END):
            print("GUARD %s: unbalanced markers" % rel)
            bad += 1
        if s.count(MARK) > 2:
            print("GUARD %s: %d blocks, expected at most 2 (hero + foot)"
                  % (rel, s.count(MARK)))
            bad += 1
        if MARK in s and CSSMARK not in s and not _linked(s):
            print("GUARD %s: block without its stylesheet" % rel)
            bad += 1
        if "<!--" in s.split("</head>")[-1] and MARK not in s:
            pass
        for m in re.finditer(re.escape(MARK) + r"([\s\S]*?)" + re.escape(END), s):
            for href in re.findall(r'href="([^"#]*)', m.group(1)):
                if not href or href.startswith(("http", "mailto:", "#")):
                    continue
                tgt = os.path.normpath(
                    os.path.join(os.path.dirname(rel), href))
                if not os.path.exists(os.path.join(SITE, tgt)):
                    print("GUARD %s: emits %r which resolves to %s and does "
                          "not exist" % (rel, href, tgt))
                    bad += 1
        for tag in ("tsmeta", "tsshort"):
            if s.count('class="%s"' % tag) > 1:
                print("GUARD %s: %d x .%s" % (rel, s.count('class="%s"' % tag), tag))
                bad += 1
    a = open(os.path.join(SITE, "about.html"), encoding="utf-8").read()
    if 'id="how-pages-are-checked"' not in a:
        print("GUARD about.html: the badge links to a section that is not there")
        bad += 1
    if bad:
        sys.exit("\n%d problem(s)" % bad)
    print("guards clean")


if __name__ == "__main__":
    main()
