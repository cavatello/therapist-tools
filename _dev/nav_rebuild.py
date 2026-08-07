#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Make the header work everywhere, and put the hub where a reader can find it.

TWO SEPARATE BUGS, ONE ROOT.

The mega-panel is opened by a small inline script that toggles `hidden` on
`#navpanel`. resources.html never carried that script. The markup is there, the
styling is there, the panel simply never opens - a reader clicking "Tools" on
the hub gets nothing at all. It was reported as "header does not work on all
pages", which is exactly right.

Then it spread. The article template and the licensure guide both lift their
chrome from the published resources.html at build time, precisely so the nav
cannot drift - and inherited the missing script along with everything else. Six
pages ended up with a dead header:

    resources.html, become-an-mft-california.html,
    therapist-llc-california.html, s-corp-sdi-california-therapist.html,
    bbs-fees-california-2026.html, tools.html

The lesson is about lifting rather than about this script. Copying markup and
styles but not behaviour produces a page that looks right in every screenshot
and does nothing when clicked; no static check catches it, because nothing is
missing from the DOM. The guard at the bottom of this file therefore checks for
the script by its behaviour-bearing substring, and the Playwright pass that
follows actually clicks it on every page.

THE PANEL'S CONTENTS were also a year out of date. Cost of Living sat under
"Learn" while being a sixteen-input calculator. The licensure guide, the rate
research and all three articles were absent entirely. And the hub - the page
every other page now links to, the answer to "where is everything?" - was the
sixth item in the Tools list wearing the same icon as the 3,000 Hours
calculator.

So the hub becomes the panel's promo card: the one visually distinct thing in
the menu, on the right, where the newsletter used to sit. The newsletter keeps
its place under About. A reader who opens the menu looking for "everything"
now finds a card that says so.

Icons are HARVESTED, not authored. Each existing entry carries an inline
pixel-art SVG as a data URI; this pass reads them out of the live panel keyed
by href and re-emits them, so a new entry reuses a real icon rather than
shipping a broken image. Entries with no icon of their own borrow a named one.

Idempotent. Run after the page builders and before linkcheck.
"""
import os, re, sys

HERE = os.path.dirname(os.path.abspath(__file__))
SITE = os.path.dirname(HERE)
CANON = "index.html"          # the page whose header is the reference copy

# ---------------------------------------------------------------- the panel
# (href, title, blurb, icon-source-href)  -- icon-source is the entry whose
# harvested icon this one should use; None means "use your own".
# ---------------------------------------------------------------- the panel
# Topic-first, decided 7 August 2026 against the real registry rather than
# against impressions - the working is in claude/nav-ia-decision-01-vs-02.md.
# The short version: the site stores `topic` and `format` on every page, format
# is pathologically skewed (91 of 122 pages are one format) and topic is not, so
# the twenty-seven-item "Learn" menu is replaced by the five topic hubs the site
# already publishes, with Calculators kept as its own menu because a calculator
# is a different kind of object from an article.
#
# NOTHING WAS DROPPED IN THE MOVE. The old panel held 36 entries plus the hub
# promo; this one holds the same 36 hrefs plus the same promo, re-filed. The
# guard at the bottom counts them. Each topic column additionally links to its
# hub page, which is new but additive.
#
# (href, title, blurb, icon-source-href)  -- icon-source is the entry whose
# harvested icon this one should use; None means "use your own".

CALCS = [
    ("practice-simulator.html", "Practice Simulator",
     "what a California practice actually pays", None),
    ("therapist-tax-strategy-california.html", "Tax &amp; Retirement",
     "how much of your tax bill is optional", None),
    ("grow-your-therapy-practice.html", "Grow Your Practice",
     "what a client is worth, and where they come from", None),
    ("associate-mft-job-advisor.html", "Associate Job Advisor",
     "compare AMFT jobs, pay and your 3,000 hours", None),
    ("amft-3000-hours-california.html", "3,000 Hours",
     "which gate is actually holding you", None),
    # moved out of "Learn" long ago: sixteen inputs and a computed answer is a
    # calculator, whatever the URL says
    ("therapist-cost-of-living-california.html", "Cost of Living",
     "what a month costs, and what is left", None),
    ("calculators.html", "All the calculators",
     "seven, grouped by what they are about",
     "practice-simulator.html"),
]
MONEY = [
    ("therapist-llc-california.html", "Sole prop or corporation",
     "why a California therapist cannot form an LLC",
     "therapist-working-remotely-california.html"),
    ("s-corp-sdi-california-therapist.html", "The S-corp payroll gap",
     "the $1,248 most comparisons leave out",
     "therapist-cost-of-living-california.html"),
    ("cost-of-incorporating-california-therapist.html", "Cost of incorporating",
     "$800 before you see a client",
     "therapist-cost-of-living-california.html"),
    ("quarterly-estimated-taxes-california-therapist.html", "Estimated taxes",
     "four dates, and one of them is zero",
     "therapist-working-remotely-california.html"),
    ("backdoor-roth-pro-rata-therapist.html", "The backdoor Roth",
     "and the balance that ruins it",
     "therapist-cost-of-living-california.html"),
    ("solo-401k-sep-simple-california-therapist.html", "Solo 401(k) or SEP",
     "which plan lets you put away more",
     "therapist-cost-of-living-california.html"),
    ("therapist-tax-deductions-california.html", "What you can deduct",
     "and the four things that do not work",
     "therapist-working-remotely-california.html"),
    ("home-office-deduction-california-therapist.html", "The home office",
     "both methods, worked, for telehealth",
     "therapist-cost-of-living-california.html"),
    ("s-corp-salary-social-security-therapist.html", "The pension you give up",
     "what a low S-corp salary costs later",
     "therapist-working-remotely-california.html"),
]
LICENSURE = [
    ("become-an-mft-california.html", "Becoming an MFT",
     "every licensure requirement, with its code section",
     "therapist-working-remotely-california.html"),
    ("bbs-fees-california-2026.html", "BBS fees, 2026",
     "halved in July, and reverting in 2030",
     "therapist-working-remotely-california.html"),
    ("continuing-education-california-lmft.html", "Continuing education",
     "36 hours, and the 62% that fail the audit",
     "become-an-mft-california.html"),
]
PAID = [
    ("rates.html", "The Rate Gap",
     "what insurance pays against private pay",
     "therapist-cost-of-living-california.html"),
    ("insurance-panels-california-therapist.html", "Insurance panels",
     "the 60-day rule, and which panels are open",
     "headway-for-california-therapists.html"),
    ("insurance-reimbursement-rates-california-therapist.html", "What insurance pays",
     "Medicare and Medi-Cal, computed per code",
     "therapist-cost-of-living-california.html"),
    ("headway-for-california-therapists.html", "Headway",
     "what it pays, and what it keeps",
     "therapist-cost-of-living-california.html"),
    ("headway-alma-grow-therapy-compared-california.html", "Headway, Alma or Grow",
     "four routes priced at three caseloads",
     "headway-for-california-therapists.html"),
    ("superbills-good-faith-estimate-california-therapist.html", "Superbills and GFEs",
     "the paperwork a private-pay practice owes",
     "therapist-working-remotely-california.html"),
]
PRACTICE = [
    ("therapist-working-remotely-california.html", "Working Remotely",
     "the same practice, run from eight places", None),
    ("hiring-first-associate-california-therapist.html", "Hiring an associate",
     "the loaded cost and the break-even",
     "therapist-cost-of-living-california.html"),
    ("simplepractice-california-therapists.html", "SimplePractice",
     "what the software actually costs, all in",
     "headway-for-california-therapists.html"),
    ("therapynotes-vs-simplepractice-california.html", "TherapyNotes or SimplePractice",
     "priced properly, including the hidden fees",
     "headway-for-california-therapists.html"),
]
TRAINING = [
    ("mft-programs-california.html", "MFT programmes",
     "65 California schools, and what people say",
     "therapist-working-remotely-california.html"),
    ("psychedelic-therapy-training-california.html", "Psychedelic training",
     "16 certificates, and what each one lets you do",
     "become-an-mft-california.html"),
]
# "Put Everything / Every question / What changed in the About panel rather than
# a seventh top-level item" - the decision doc. Everything itself stays the
# promo card, where it has been since the panel was rebuilt.
ABOUT = [
    ("about.html", "What this is", "tools, reference and support for CA MFTs", None),
    ("questions.html", "Every question",
     "the complete index, phrased as people ask it", "resources.html"),
    ("changes.html", "What changed", "the numbers that moved, with sources",
     "bbs-fees-california-2026.html"),
    ("newsletter.html", "Stay updated", "new tools and what changed in the numbers", None),
    ("contact.html", "Contact", "bugs, ideas, corrections", None),
]

# (key, label, entries, hub href or None). The key is what the button carries in
# data-nav and what the column carries in data-group; they must agree or the
# menu opens onto nothing.
GROUPS = [
    ("calculators", "Calculators", CALCS, None),
    ("money", "Money", MONEY, "money/"),
    ("licensure", "Licensure", LICENSURE, "licensure/"),
    ("getting-paid", "Getting paid", PAID, "getting-paid/"),
    ("practice", "Practice", PRACTICE, "practice/"),
    ("training", "Training", TRAINING, "training/"),
    ("about", "About", ABOUT, None),
]

PROMO = ("resources.html", "Everything in one place",
         "Every calculator, every article, and 72 checked links to the Board, the "
         "payers and the associations &mdash; indexed by the question you arrived with.",
         "Tools &amp; resources")

# The panel is opened by this script, and it is written here rather than
# harvested from index.html because its behaviour changed with the IA: a button
# no longer opens "the menu", it opens ITS OWN group, and clicking the open one
# again closes it. Every page gets this exact copy, replacing whatever nav
# script it had, so behaviour cannot drift the way it did when it was copied.
SCRIPT = """<script>
(function(){
  var bar = document.querySelector('.sitenav'),
      panel = document.getElementById('navpanel');
  if(!bar || !panel) return;
  var btns = [].slice.call(bar.querySelectorAll('[data-nav]')),
      cols = [].slice.call(panel.querySelectorAll('.np-col')),
      cur = null;
  function show(g){
    cur = g;
    cols.forEach(function(c){
      c.hidden = (g !== null && c.getAttribute('data-group') !== g);
    });
    btns.forEach(function(b){
      var on = (b.getAttribute('data-nav') === g);
      b.classList.toggle('on', on);
      b.setAttribute('aria-expanded', on ? 'true' : 'false');
    });
    panel.hidden = (g === null);
    bar.classList.toggle('open', g !== null);
  }
  btns.forEach(function(b){
    b.addEventListener('click', function(e){
      e.preventDefault();
      var g = b.getAttribute('data-nav');
      show(cur === g ? null : g);
    });
  });
  document.addEventListener('keydown', function(e){ if(e.key === 'Escape') show(null); });
  document.addEventListener('click', function(e){
    if(!panel.hidden && !bar.contains(e.target)) show(null);
  });
})();
</script>"""

CSS = """
/* ---------------------------------------------------------------- the header
   Two changes ship together here, and they are separable in principle but not
   in practice: the menu became topic-first (seven items, not three) and the
   whole site took the "Pixel" visual treatment - hard 2px edges and solid
   offset shadows instead of blurs.

   This block is appended AFTER the shared chrome sheet on every page, so it
   overrides by source order and the shared sheet does not have to be touched.
   That matters: the shared sheet is content-hashed and referenced by 127
   documents. */

/* Seven buttons will not fit a three-column grid. A wrapping flex row does,
   and on a phone it becomes a single scrollable line rather than three stacked
   rows of stubs. */
.sitenav-links{display:flex;flex-wrap:wrap;justify-content:center;gap:3px;
  background:rgba(0,0,0,.24);border-radius:14px;padding:4px;max-width:none;
  border:2px solid rgba(0,0,0,.34)}
.sitenav-top{font-size:12.5px;font-weight:600;padding:7px 11px;border-radius:10px;
  min-height:36px;white-space:nowrap;overflow:visible;text-overflow:clip;flex:0 0 auto}
.sitenav-top.on{background:#fff;color:#1E4436;box-shadow:2px 2px 0 rgba(0,0,0,.4)}
.sitenav-in{border-radius:18px}
.sitenav-cta{border:2px solid rgba(0,0,0,.34);border-radius:12px;
  box-shadow:3px 3px 0 rgba(10,30,22,.45)}
.sitenav-cta:active{transform:translate(3px,3px);box-shadow:0 0 0 rgba(10,30,22,.45)}
@media (max-width:1180px){
  .sitenav-top{font-size:12px;padding:7px 8px}
}
/* Below the point where the bar stacks, the seven become one scrolling line.
   flex-wrap:wrap would give three ragged rows and a 130px-tall header. */
@media (max-width:900px){
  .sitenav-links{flex-wrap:nowrap;overflow-x:auto;justify-content:flex-start;
    scrollbar-width:none;-ms-overflow-style:none;scroll-snap-type:x proximity}
  .sitenav-links::-webkit-scrollbar{display:none}
  .sitenav-top{scroll-snap-align:start}
  /* the affordance. Seven items do not fit 390px and four of them are off the
     right edge; a hard clip reads as "that is all there is". Fading the last
     18px says there is more without adding a control. */
  .sitenav-links{-webkit-mask-image:linear-gradient(90deg,#000 calc(100% - 18px),transparent);
    mask-image:linear-gradient(90deg,#000 calc(100% - 18px),transparent)}
}

/* ---- the panel. One group at a time, so a menu holding 36 destinations never
   shows more than nine. The promo card is outside the groups and always on. */
.navpanel{grid-template-columns:minmax(0,1fr) 250px;gap:20px;
  border:3px solid #16211B;border-radius:16px;
  box-shadow:8px 8px 0 rgba(22,33,27,.9);padding:18px}
.np-col{display:grid;grid-template-columns:repeat(auto-fill,minmax(232px,1fr));
  gap:2px 14px;align-content:start}
.np-col[hidden]{display:none}
/* the label spans the sub-columns rather than sitting in the first of them */
.np-col h5{grid-column:1/-1;margin:0 0 8px;font-size:9.5px;font-weight:800;
  letter-spacing:.13em;text-transform:uppercase;color:#16211B;
  background:#F6C560;border:2px solid #16211B;border-radius:999px;
  padding:4px 10px 3px;justify-self:start}
.np-col a{border:2px solid transparent;border-radius:10px}
.np-col a:hover{background:#F4F0E6;border-color:#16211B}
/* the hub link that closes each topic column */
.np-hub{grid-column:1/-1;justify-self:start;margin-top:8px;
  font-family:'IBM Plex Mono',ui-monospace,monospace;font-size:11px;font-weight:700;
  letter-spacing:.04em;text-decoration:none;color:#16211B;
  border:2px solid #16211B;border-radius:999px;padding:7px 13px;
  box-shadow:2px 2px 0 #16211B;background:#fff}
.np-hub:hover{background:#F6C560}
.np-promo{border:2px solid #16211B;box-shadow:4px 4px 0 #16211B}
.navpanel .np-promo b{letter-spacing:-.02em;font-family:'Bricolage Grotesque',
  Fraunces,serif;font-weight:800;font-size:16px}
.np-promo .np-all{display:block;font-family:'IBM Plex Mono',ui-monospace,monospace;
  font-size:9.6px;letter-spacing:.13em;text-transform:uppercase;opacity:.62;
  margin-bottom:7px}
.np-promo span:last-child{border:2px solid #16211B;box-shadow:2px 2px 0 #16211B}
@media (max-width:820px){
  .navpanel{grid-template-columns:minmax(0,1fr)}
  .np-col{grid-template-columns:minmax(0,1fr)}
}
/* A phone cannot show 250px of promo card under nine links without burying it,
   and the panel is already scrollable there. */
@media (max-width:640px){
  .navpanel{max-height:70vh;overflow-y:auto;box-shadow:5px 5px 0 rgba(22,33,27,.9)}
}

/* ---------------------------------------------------------------- the footer
   Same treatment, no change of contents: every link that was in it is still in
   it, in the same order, under the same five headings. */
.sitefoot{border-top:4px solid #16211B}
.sitefoot h5{color:#16211B;background:#F6C560;border:2px solid #16211B;
  border-radius:999px;padding:4px 10px 3px;display:inline-block}
.ftcols a{border-bottom:2px solid transparent}
.ftcols a:hover{border-bottom-color:#F6C560}
/* ------------------------------------------------------- the display face
   "Much bolder typography" was the brief. Bricolage Grotesque at 800, tracked
   to -.032em, replaces Fraunces on headings sitewide; _dev/typeface.py adds it
   to the font request on every page. Fraunces stays loaded and still sets the
   FIGURES - a serif numeral reads as a quantity, a grotesque one reads as a
   headline - so do not drop it from the request.

   The [class] duplicate is not padding. Bare `h1` is (0,0,1) and loses to the
   scoped `.sc h1` / `.lib h2` rules the article and directory templates carry;
   `[class] h1` is (0,1,1), ties with them, and wins on source order because
   this sheet is appended last on every page. A page whose heading is styled at
   (0,2,1) or higher keeps its own face on purpose. */
h1,h2,h3,[class] h1,[class] h2,[class] h3,
.sitenav-wordmark,.np-col b,.ftcols h5{
  font-family:'Bricolage Grotesque','Archivo',Inter,system-ui,sans-serif;
  letter-spacing:-.032em}
h1,h2,[class] h1,[class] h2{font-weight:800}
h3,[class] h3{font-weight:700}
.sitenav-wordmark{font-weight:800;letter-spacing:-.03em;font-size:16px}
.np-col b{letter-spacing:-.02em}
.ftcols h5{letter-spacing:.1em}

"""

# ---------------------------------------------------------------- the footer
FOOT = [
    ("Tools", [("practice-simulator.html", "Practice Simulator"),
               ("therapist-tax-strategy-california.html", "Tax &amp; Retirement"),
               ("grow-your-therapy-practice.html", "Grow Your Practice"),
               ("associate-mft-job-advisor.html", "Associate Job Advisor"),
               ("amft-3000-hours-california.html", "3,000 Hours"),
               ("therapist-cost-of-living-california.html", "Cost of Living")]),
    ("Learn", [("resources.html", "Tools &amp; resources"),
               ("become-an-mft-california.html", "Becoming an MFT"),
               ("rates.html", "The Rate Gap"),
               ("therapist-working-remotely-california.html", "Working Remotely"),
               ("therapist-llc-california.html", "Sole prop or corporation"),
               ("s-corp-sdi-california-therapist.html", "The S-corp payroll gap"),
               ("bbs-fees-california-2026.html", "BBS fees, 2026"),
               ("headway-for-california-therapists.html", "Headway"),
               ("mft-programs-california.html", "MFT programmes"),
               ("cost-of-incorporating-california-therapist.html",
                "Cost of incorporating"),
               ("quarterly-estimated-taxes-california-therapist.html",
                "Estimated taxes"),
               ("backdoor-roth-pro-rata-therapist.html", "The backdoor Roth"),
               ("psychedelic-therapy-training-california.html",
                "Psychedelic training")]),
    ("Browse", [("resources.html", "Everything"),
                ("questions.html", "Every question"),
                ("calculators.html", "All the calculators"),
                ("changes.html", "What changed"),
                ("simplepractice-california-therapists.html", "SimplePractice"),
                ("solo-401k-sep-simple-california-therapist.html", "Solo 401(k) or SEP"),
                ("therapist-tax-deductions-california.html", "What you can deduct"),
                ("home-office-deduction-california-therapist.html", "The home office"),
                ("s-corp-salary-social-security-therapist.html", "The pension you give up"),
                ("hiring-first-associate-california-therapist.html", "Hiring an associate"),
                ("insurance-panels-california-therapist.html", "Insurance panels"),
                ("insurance-reimbursement-rates-california-therapist.html",
                 "What insurance pays"),
                ("headway-alma-grow-therapy-compared-california.html",
                 "Headway, Alma or Grow"),
                ("superbills-good-faith-estimate-california-therapist.html",
                 "Superbills and GFEs"),
                ("continuing-education-california-lmft.html", "Continuing education"),
                ("therapynotes-vs-simplepractice-california.html",
                 "TherapyNotes or SimplePractice"),
                ("money/", "Money"),
                ("licensure/", "Licensure"),
                ("getting-paid/", "Getting paid"),
                ("practice/", "Running a practice"),
                ("training/", "Training")]),
    ("About", [("about.html", "What this is"),
               ("affiliate-disclosure.html", "Affiliate disclosure"),
               ("newsletter.html", "Stay updated"),
               ("contact.html", "Contact"),
               ("https://cavatello.github.io/therapist-tycoon/tycoon.html", "Tycoon")]),
]


def panel_span(s):
    """Byte span of the <div class="navpanel"> element, by balanced scanning.

    The first version matched `<div class="navpanel"[\\s\\S]*?</div></div>`,
    reasoning that the panel's last child is a promo <a> and so the markup ends
    `</a></div></div>` - panel, then wrapper. Two things went wrong. The
    replacement I emitted closed only the panel, so every rewritten page lost a
    </div> and the header wrapper never closed. And on contact.html and
    newsletter.html the non-greedy match ran PAST the panel into page content,
    which is how a guard counting icons caught it: 17 and 21 where 16 were
    expected. Both symptoms, one cause - a regex cannot find the end of a
    nestable element.

    So: scan and balance, and replace exactly what was scanned.
    """
    i = s.find('<div class="navpanel"')
    if i < 0:
        return None
    d = 0
    for m in re.finditer(r"<div\b|</div>", s[i:]):
        d += 1 if m.group(0).startswith("<div") else -1
        if d == 0:
            return (i, i + m.end())
    return None


LINKS = re.compile(r'<nav class="sitenav-links"[^>]*>[\s\S]*?</nav>')


def harvest_icons(panel):
    """href -> the entry's <img> tag, read out of the live panel."""
    out = {}
    for m in re.finditer(r'<a href="([^"]+)"[^>]*>\s*(<img[^>]*>)', panel):
        out.setdefault(m.group(1), m.group(2))
    return out


def entry(href, title, blurb, icons, borrow):
    img = icons.get(href) or (icons.get(borrow) if borrow else None)
    if img is None:
        img = next(iter(icons.values()))
    ext = ' target="_blank" rel="noopener noreferrer"' if href.startswith("http") else ""
    return ('<a href="%s"%s>%s<span><b>%s</b><i>%s</i></span></a>'
            % (href, ext, img, title, blurb))


def build_links():
    """The seven top-level buttons. Each one names the group it opens."""
    return ('<nav class="sitenav-links" aria-label="Site">%s</nav>'
            % "".join('<button type="button" data-nav="%s" class="sitenav-top" '
                      'aria-expanded="false" aria-controls="navpanel">%s</button>'
                      % (key, label) for key, label, _its, _hub in GROUPS))


def build_panel(icons):
    cols = []
    for key, label, items, hub in GROUPS:
        links = "".join(entry(h, t, b, icons, br) for h, t, b, br in items)
        tail = ('<a class="np-hub" href="%s">All of %s &rarr;</a>' % (hub, label.lower())
                if hub else "")
        cols.append('<div class="np-col" data-group="%s"><h5>%s</h5>%s%s</div>'
                    % (key, label, links, tail))
    href, head, body, cta = PROMO
    img = icons.get(href) or next(iter(icons.values()))
    promo = ('<a class="np-promo" href="%s">%s<span class="np-all">The hub</span>'
             '<b>%s</b><p>%s</p><span>%s &rarr;</span></a>' % (href, img, head, body, cta))
    return ('<div class="navpanel" id="navpanel" hidden>%s%s</div>'
            % ("".join(cols), promo))


def build_footcols(small_print):
    cols = []
    for name, items in FOOT:
        links = "".join(
            '<a href="%s"%s>%s</a>'
            % (h, ' target="_blank" rel="noopener noreferrer"' if h.startswith("http") else "", t)
            for h, t in items)
        cols.append("<div><h5>%s</h5>%s</div>" % (name, links))
    cols.append(small_print)
    return '<div class="ftcols">%s</div>' % "".join(cols)


ALL_ENTRIES = [e for _k, _l, its, _h in GROUPS for e in its]


def main():
    canon = open(os.path.join(SITE, CANON), encoding="utf-8").read()

    sp = panel_span(canon)
    if not sp:
        sys.exit("nav_rebuild: cannot find the reference panel in " + CANON)
    icons = harvest_icons(canon[sp[0]:sp[1]])
    if len(icons) < 8:
        sys.exit("nav_rebuild: harvested only %d icons - the panel shape changed"
                 % len(icons))

    panel = build_panel(icons)
    links = build_links()

    def delta(t):
        nos = re.sub(r"<script[\s\S]*?</script>", "", t)
        return len(re.findall(r"<div\b", nos)) - len(re.findall(r"</div>", nos))

    # Files in css/ that this pass wrote (via extract_css). Identified by the
    # marker comment they open with, not by hash, because the hash changes every
    # time the CSS above is edited.
    mine = []
    cssdir = os.path.join(SITE, "css")
    if os.path.isdir(cssdir):
        for n in sorted(os.listdir(cssdir)):
            if not n.endswith(".css"):
                continue
            head = open(os.path.join(cssdir, n), encoding="utf-8").read(64)
            if "/* nav_rebuild */" in head:
                mine.append(re.escape(n))
    print("own stylesheets  %d" % len(mine))

    pre_delta = {}
    fixed_script = fixed_panel = fixed_foot = fixed_links = 0
    for f in sorted(os.listdir(SITE)):
        if not f.endswith(".html"):
            continue
        path = os.path.join(SITE, f)
        s = open(path, encoding="utf-8").read()
        before = s
        pre_delta[f] = delta(s)

        # ---- 1. the panel
        sp2 = panel_span(s)
        if sp2 and s[sp2[0]:sp2[1]] != panel:
            s = s[:sp2[0]] + panel + s[sp2[1]:]
            fixed_panel += 1

        # ---- 2. the top-level buttons. <nav> is not nestable here, so a regex
        #        is honest; the panel above is, which is why it is not.
        lm = LINKS.search(s)
        if lm and lm.group(0) != links:
            s = s[:lm.start()] + links + s[lm.end():]
            fixed_links += 1

        # ---- 3. the script that makes it open. REPLACED, not merely inserted
        #        when absent: the behaviour changed with the IA, and a page
        #        keeping the old script would show a panel whose groups never
        #        unhide - a menu that opens onto nothing. That is precisely the
        #        class of failure the module docstring is about.
        if "navpanel" in s:
            found = [m for m in re.finditer(r"<script>[\s\S]*?</script>", s)
                     if "navpanel" in m.group(0)]
            if found:
                m = found[0]
                if m.group(0) != SCRIPT:
                    s = s[:m.start()] + SCRIPT + s[m.end():]
                    fixed_script += 1
            else:
                s = s.replace("</body>", SCRIPT + "\n</body>", 1)
                fixed_script += 1

        # ---- 4. the footer columns
        fm = re.search(r'<div class="ftcols">[\s\S]*?</div></div>', s)
        if fm:
            spm = re.search(r"<div><h5>The small print</h5>[\s\S]*?</div>", fm.group(0))
            if spm:
                new_foot = build_footcols(spm.group(0))
                if fm.group(0) != new_foot:
                    s = s[:fm.start()] + new_foot + s[fm.end():]
                    fixed_foot += 1

        # ---- 5. stylesheet.
        # Removing the inline block is not enough. _dev/extract_css.py lifts
        # this block into a content-hashed css/<hash>.css and leaves a <link>
        # in its place - after which the regex below matches nothing, this pass
        # appends a fresh block, extract_css lifts THAT one too, and the page
        # accumulates a link per run. index.html was carrying sixteen copies of
        # the same stylesheet when this was found. So: strip the inline block
        # AND every link to a file this pass is the author of.
        s = re.sub(r"\n?<style>/\* nav_rebuild \*/[\s\S]*?/\* end nav \*/</style>\n?", "", s)
        for name in mine:
            s = re.sub(r'\n?<link rel="stylesheet" href="(?:\.\./)*css/%s">' % name, "", s)
        if 'class="np-promo"' in s:
            s = s.replace("</body>", "\n<style>/* nav_rebuild */" + CSS
                          + "/* end nav */</style>\n</body>", 1)

        if s != before:
            open(path, "w", encoding="utf-8").write(s)

    print("panels rebuilt   %d" % fixed_panel)
    print("buttons rebuilt  %d" % fixed_links)
    print("scripts replaced %d" % fixed_script)
    print("footers rebuilt  %d" % fixed_foot)

    # ---- guards
    bad = 0
    want = {h for h, _t, _b, _br in ALL_ENTRIES} | {PROMO[0]}
    keys = [k for k, _l, _i, _h in GROUPS]
    for f in sorted(os.listdir(SITE)):
        if not f.endswith(".html"):
            continue
        s = open(os.path.join(SITE, f), encoding="utf-8").read()
        if "navpanel" not in s:
            continue
        # behaviour, not markup: the panel must have something that toggles it
        if not re.search(r"<script>[\s\S]*?navpanel[\s\S]*?</script>", s):
            print("GUARD %s: panel present, no script to open it" % f); bad += 1
        sp3 = panel_span(s)
        if not sp3:
            print("GUARD %s: panel markup unreadable" % f); bad += 1
            continue
        pan = s[sp3[0]:sp3[1]]
        got = set(re.findall(r'<a[^>]+href="([^"]+)"', pan))
        missing = want - got
        if missing:
            print("GUARD %s: panel missing %s" % (f, ", ".join(sorted(missing)))); bad += 1
        if pan.count("<img") != len(ALL_ENTRIES) + 1:
            print("GUARD %s: %d icons, expected %d"
                  % (f, pan.count("<img"), len(ALL_ENTRIES) + 1)); bad += 1
        # A button whose data-nav names no column opens onto an empty panel, and
        # a column no button names is unreachable. Both look fine in the markup.
        btn = set(re.findall(r'data-nav="([^"]+)"', s))
        col = set(re.findall(r'class="np-col" data-group="([^"]+)"', pan))
        if btn != set(keys) or col != set(keys):
            print("GUARD %s: buttons %s, columns %s, expected %s"
                  % (f, sorted(btn), sorted(col), sorted(keys))); bad += 1
        # every target must exist on disk
        for h in got:
            if h.startswith("http") or "#" in h:
                continue
            p = os.path.join(SITE, h)
            if not (os.path.exists(p) or os.path.isdir(p.rstrip("/"))):
                print("GUARD %s: panel links to missing %s" % (f, h)); bad += 1
        if s.count('id="navpanel"') != 1:
            print("GUARD %s: %d panels" % (f, s.count('id="navpanel"'))); bad += 1
        # This pass replaces a nestable element in place. If the replacement
        # ever closes a different number of divs than it opened, every page
        # below the header is silently reparented. Cheap to check, and it is
        # the failure that actually happened.
        # Compare the div balance BEFORE and AFTER this pass, not against zero.
        # Two earlier versions of this guard were wrong in different ways. The
        # first counted raw text and failed five pages that build DOM in
        # JavaScript with template strings containing a bare "<div". The second
        # stripped scripts and still failed the same five - because those pages
        # carry a genuine unclosed div in their markup, on the live site, today,
        # with nothing to do with this pass. An absolute balance check is a
        # different bug report; what THIS pass must guarantee is that it does
        # not make things worse. So: the delta must be unchanged.
        if f in pre_delta and delta(s) != pre_delta[f]:
            print("GUARD %s: div balance moved %+d -> %+d"
                  % (f, pre_delta[f], delta(s))); bad += 1
    if bad:
        sys.exit("nav_rebuild: %d guard failure(s)" % bad)
    print("guards clean")


if __name__ == "__main__":
    main()
