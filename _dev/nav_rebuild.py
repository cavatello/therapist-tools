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
TOOLS = [
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
    # moved out of "Learn": sixteen inputs and a computed answer is a calculator
    ("therapist-cost-of-living-california.html", "Cost of Living",
     "what a month costs, and what is left", None),
]
LEARN = [
    ("become-an-mft-california.html", "Becoming an MFT",
     "every licensure requirement, with its code section",
     "therapist-working-remotely-california.html"),
    ("rates.html", "The Rate Gap",
     "what insurance pays against private pay",
     "therapist-cost-of-living-california.html"),
    ("therapist-working-remotely-california.html", "Working Remotely",
     "the same practice, run from eight places", None),
    ("therapist-llc-california.html", "Sole prop or corporation",
     "why a California therapist cannot form an LLC",
     "therapist-working-remotely-california.html"),
    ("s-corp-sdi-california-therapist.html", "The S-corp payroll gap",
     "the $1,248 most comparisons leave out",
     "therapist-cost-of-living-california.html"),
    ("bbs-fees-california-2026.html", "BBS fees, 2026",
     "halved in July, and reverting in 2030",
     "therapist-working-remotely-california.html"),
    ("headway-for-california-therapists.html", "Headway",
     "what it pays, and what it keeps",
     "therapist-cost-of-living-california.html"),
    ("mft-programs-california.html", "MFT programmes",
     "65 California schools, and what people say",
     "therapist-working-remotely-california.html"),
    ("cost-of-incorporating-california-therapist.html", "Cost of incorporating",
     "$800 before you see a client",
     "therapist-cost-of-living-california.html"),
    ("quarterly-estimated-taxes-california-therapist.html", "Estimated taxes",
     "four dates, and one of them is zero",
     "therapist-working-remotely-california.html"),
    ("backdoor-roth-pro-rata-therapist.html", "The backdoor Roth",
     "and the balance that ruins it",
     "therapist-cost-of-living-california.html"),
    ("psychedelic-therapy-training-california.html", "Psychedelic training",
     "16 certificates, and what each one lets you do",
     "become-an-mft-california.html"),
]
ABOUT = [
    ("about.html", "What this is", "tools, reference and support for CA MFTs", None),
    ("newsletter.html", "Stay updated", "new tools and what changed in the numbers", None),
    ("contact.html", "Contact", "bugs, ideas, corrections", None),
]
PROMO = ("resources.html", "Everything in one place",
         "Every calculator, every article, and 72 checked links to the Board, the "
         "payers and the associations &mdash; indexed by the question you arrived with.",
         "Tools &amp; resources")

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
    ("About", [("about.html", "What this is"),
               ("newsletter.html", "Stay updated"),
               ("contact.html", "Contact"),
               ("https://cavatello.github.io/therapist-tycoon/tycoon.html", "Tycoon")]),
]

CSS = """
/* The hub's promo card. Same slot the newsletter used, one weight louder,
   because "where is everything?" is the question a menu exists to answer. */
.navpanel .np-promo b{letter-spacing:-.01em}
.np-promo .np-all{display:block;font-family:'IBM Plex Mono',ui-monospace,monospace;
  font-size:9.6px;letter-spacing:.13em;text-transform:uppercase;opacity:.62;
  margin-bottom:7px}
"""


def panel_span(s):
    """Byte span of the <div class="navpanel"> element, by balanced scanning.

    The first version matched `<div class="navpanel"[\s\S]*?</div></div>`,
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


def build_panel(icons):
    cols = []
    for name, items in (("Tools", TOOLS), ("Learn", LEARN), ("About", ABOUT)):
        cols.append('<div class="np-col"><h5>%s</h5>%s</div>'
                    % (name, "".join(entry(h, t, b, icons, br) for h, t, b, br in items)))
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


def main():
    canon = open(os.path.join(SITE, CANON), encoding="utf-8").read()

    sp = panel_span(canon)
    if not sp:
        sys.exit("nav_rebuild: cannot find the reference panel in " + CANON)
    icons = harvest_icons(canon[sp[0]:sp[1]])
    if len(icons) < 8:
        sys.exit("nav_rebuild: harvested only %d icons - the panel shape changed"
                 % len(icons))

    sm = [m for m in re.finditer(r"<script>([\s\S]*?)</script>", canon)
          if "navpanel" in m.group(1)]
    if not sm:
        sys.exit("nav_rebuild: no nav script in " + CANON)
    SCRIPT = sm[0].group(0)

    panel = build_panel(icons)

    def delta(t):
        nos = re.sub(r"<script[\s\S]*?</script>", "", t)
        return len(re.findall(r"<div\b", nos)) - len(re.findall(r"</div>", nos))

    pre_delta = {}
    fixed_script = fixed_panel = fixed_foot = 0
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

        # ---- 2. the script that makes it open
        if "navpanel" in s and not re.search(r"<script>[\s\S]*?navpanel[\s\S]*?</script>", s):
            s = s.replace("</body>", SCRIPT + "\n</body>", 1)
            fixed_script += 1

        # ---- 3. the footer columns
        fm = re.search(r'<div class="ftcols">[\s\S]*?</div></div>', s)
        if fm:
            spm = re.search(r"<div><h5>The small print</h5>[\s\S]*?</div>", fm.group(0))
            if spm:
                new_foot = build_footcols(spm.group(0))
                if fm.group(0) != new_foot:
                    s = s[:fm.start()] + new_foot + s[fm.end():]
                    fixed_foot += 1

        # ---- 4. stylesheet
        s = re.sub(r"\n?<style>/\* nav_rebuild \*/[\s\S]*?/\* end nav \*/</style>\n?", "", s)
        if 'class="np-promo"' in s:
            s = s.replace("</body>", "\n<style>/* nav_rebuild */" + CSS
                          + "/* end nav */</style>\n</body>", 1)

        if s != before:
            open(path, "w", encoding="utf-8").write(s)

    print("panels rebuilt   %d" % fixed_panel)
    print("scripts restored %d" % fixed_script)
    print("footers rebuilt  %d" % fixed_foot)

    # ---- guards
    bad = 0
    want = {h for h, _t, _b, _br in TOOLS + LEARN + ABOUT} | {PROMO[0]}
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
        if pan.count("<img") != len(TOOLS) + len(LEARN) + len(ABOUT) + 1:
            print("GUARD %s: %d icons, expected %d"
                  % (f, pan.count("<img"),
                     len(TOOLS) + len(LEARN) + len(ABOUT) + 1)); bad += 1
        # every target must exist on disk
        for h in got:
            if h.startswith("http") or "#" in h:
                continue
            if not os.path.exists(os.path.join(SITE, h)):
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
