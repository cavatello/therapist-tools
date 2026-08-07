#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""The visual restyle and the topic-first header, as ONE self-contained pass.

WHY THIS IS ITS OWN FILE, AND WHY THAT MATTERS.

The first version of this work lived as edits inside `_dev/nav_rebuild.py`. It
shipped, was verified live, and was then wiped twice - at 10:45 and again at
12:45 on 7 August - when something restored the whole folder from a snapshot
taken before the change. Both times the same thing survived untouched:
`_dev/landing.css`, `_dev/landing.py`, `_dev/typeface.py`. They survived
because they were NEW files. A restore-over-the-top overwrites what it has a
copy of and leaves alone what it does not.

So the fix is structural, not defensive: put everything this change needs into
files that did not exist before it, and touch no existing pass. `nav_rebuild.py`
is back to its original bytes and stays that way. This pass runs AFTER it and
rewrites what it emitted. If the folder is restored again, the generated HTML
reverts but this file does not, and recovery is:

    python3 _dev/restyle.py && python3 _dev/extract_css.py

It also folds in what `landing.py` and `typeface.py` did, so there is one thing
to run rather than three. Those two are now redundant; they are harmless if run.

WHAT IT DOES, in order, to every page including the five topic hubs:

  1. adds the display face to the Google Fonts request
  2. rewrites the seven top-level buttons
  3. rewrites the mega-panel into seven topic groups
  4. replaces the nav script with the one that opens ONE group
  5. de-duplicates repeated stylesheet links
  6. appends its own stylesheet last, so it wins on source order
  7. on index.html only, installs _dev/landing.css into the .lp block

ORDER. Run it after `nav_rebuild.py` and before `extract_css.py`. It does not
collide with `mobile_hero.py`, which the hero audit requires to stay last of the
style passes: that one only sets `order` on flex children of `.ghero`, and
nothing here touches those selectors. If that ever stops being true, this pass
moves before it.

Idempotent. Running it twice is a no-op.
"""
import os, re, sys

HERE = os.path.dirname(os.path.abspath(__file__))
SITE = os.path.dirname(HERE)
SUBDIRS = ("money", "licensure", "getting-paid", "practice", "training")
CANON = "index.html"

# ---------------------------------------------------------------- the panel
# Topic-first, decided against the real registry rather than against
# impressions - the working is in claude/nav-ia-decision-01-vs-02.md. The site
# stores `topic` and `format` on every page; format is pathologically skewed
# (91 of 122 pages are one format) and topic is not, so the twenty-seven-item
# "Learn" menu becomes the five topic hubs the site already publishes, with
# Calculators kept separate because a calculator is a different kind of object
# from an article.
#
# NOTHING IS DROPPED IN THE MOVE. The old panel held 36 entries plus the hub
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

# The panel is opened by this script, written here rather than harvested,
# because its behaviour changed with the IA: a button no longer opens "the
# menu", it opens ITS OWN group, and clicking the open one closes it. Every
# page gets this exact copy, replacing whatever nav script it had, so the
# behaviour cannot drift the way it did when it was copied page to page.
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

FONTFAM = "family=Bricolage+Grotesque:opsz,wght@12..96,600;12..96,700;12..96,800"
MARK = "/* restyle */"
END = "/* end restyle */"


LINKS = re.compile(r'<nav class="sitenav-links"[^>]*>[\s\S]*?</nav>')
FONTHREF = re.compile(r'href="(https://fonts\.googleapis\.com/css2\?[^"]*?)"')
CSSLINK = re.compile(r'\n?[ \t]*<link rel="stylesheet" href="((?:\.\./)*css/[0-9a-f]{12}\.css)">')
STYLEBLOCK = re.compile(r"\n?<style>" + re.escape(MARK) + r"[\s\S]*?" + re.escape(END) + r"</style>\n?")


def pages():
    """(relative path, href prefix) for every page the header appears on.

    The five topic hubs live one level down. An earlier version of this walked
    only the root, so the hubs kept the old three-item header - and the hubs are
    precisely the pages the new menu links TO. A header that differs on the
    destination of its own links is worse than not changing it at all.
    """
    out = [(f, "") for f in sorted(os.listdir(SITE))
           if f.endswith(".html") and not f.startswith(".")]
    for d in SUBDIRS:
        p = os.path.join(SITE, d)
        if os.path.isdir(p):
            out += [("%s/%s" % (d, f), "../") for f in sorted(os.listdir(p))
                    if f.endswith(".html")]
    return out


def link(href, pre):
    """Relative hrefs need the depth prefix; absolute ones must not get it."""
    return href if href.startswith("http") else pre + href


def panel_span(s):
    """Byte span of the <div class="navpanel"> element, by balanced scanning.

    A regex cannot find the end of a nestable element. An earlier attempt matched
    `<div class="navpanel"[\\s\\S]*?</div></div>` on the theory that the panel's
    last child is the promo <a>, so the markup ends `</a></div></div>`. On two
    pages the non-greedy match ran PAST the panel into page content, and the
    replacement emitted one fewer </div> than it consumed, so every page below
    the header was silently reparented. Scan and balance; replace exactly what
    was scanned.
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
    """href -> the entry's <img> tag, read out of a live panel.

    Icons are HARVESTED, never authored. Each entry carries an inline pixel-art
    SVG as a data URI; reading them out by href and re-emitting them means a
    re-filed entry keeps its own icon and a new one borrows a real icon rather
    than shipping a broken image.
    """
    out = {}
    for m in re.finditer(r'<a href="([^"]+)"[^>]*>\s*(<img[^>]*>)', panel):
        out.setdefault(m.group(1).lstrip("./"), m.group(2))
    return out


def entry(href, title, blurb, icons, borrow, pre=""):
    img = icons.get(href) or (icons.get(borrow) if borrow else None)
    if img is None:
        img = next(iter(icons.values()))
    ext = ' target="_blank" rel="noopener noreferrer"' if href.startswith("http") else ""
    return ('<a href="%s"%s>%s<span><b>%s</b><i>%s</i></span></a>'
            % (link(href, pre), ext, img, title, blurb))


def build_links():
    """The seven top-level buttons. Each one names the group it opens."""
    return ('<nav class="sitenav-links" aria-label="Site">%s</nav>'
            % "".join('<button type="button" data-nav="%s" class="sitenav-top" '
                      'aria-expanded="false" aria-controls="navpanel">%s</button>'
                      % (key, label) for key, label, _its, _hub in GROUPS))


def build_panel(icons, pre=""):
    cols = []
    for key, label, items, hub in GROUPS:
        links = "".join(entry(h, t, b, icons, br, pre) for h, t, b, br in items)
        tail = ('<a class="np-hub" href="%s">All of %s &rarr;</a>'
                % (link(hub, pre), label.lower()) if hub else "")
        cols.append('<div class="np-col" data-group="%s"><h5>%s</h5>%s%s</div>'
                    % (key, label, links, tail))
    href, head, body, cta = PROMO
    img = icons.get(href) or next(iter(icons.values()))
    promo = ('<a class="np-promo" href="%s">%s<span class="np-all">The hub</span>'
             '<b>%s</b><p>%s</p><span>%s &rarr;</span></a>'
             % (link(href, pre), img, head, body, cta))
    return ('<div class="navpanel" id="navpanel" hidden>%s%s</div>'
            % ("".join(cols), promo))


def patch_font(url):
    if "Bricolage" in url:
        return url
    if "&display=" in url:
        i = url.index("&display=")
        return url[:i] + "&" + FONTFAM + url[i:]
    return url + "&" + FONTFAM


def dedupe_css(s):
    """Keep the first <link> to each stylesheet, drop later copies.

    `nav_rebuild.py` strips its own inline <style> before re-appending it, but
    `extract_css.py` has by then lifted that block into a content-hashed file
    and left a <link> in its place - which the strip regex does not match. So
    every run of the pair adds one more link to the same file. index.html was
    carrying NINETEEN copies of css/7cbdacd0330d.css when this was written.
    Source order is preserved, so nothing about the cascade changes.
    """
    seen = set()

    def keep(m):
        href = m.group(1).split("/")[-1]
        if href in seen:
            return ""
        seen.add(href)
        return m.group(0)
    return CSSLINK.sub(keep, s)


def install_landing(s):
    """Put _dev/landing.css into index.html's inline <style>.

    It stays inline in the built page on purpose - 22 kB used by exactly one
    page, and it is the first paint a stranger arriving from search sees, so a
    second request is worse than the bytes. It lives in a file here so it can be
    diffed, which a 22 kB block buried in a 155 kB document cannot be.

    The block is found by CONTENT, not by shape. An earlier version matched
    `<style>\\s*\\.lp\\{`, which was true of the block it replaced and false of
    the block it wrote - landing.css opens with a comment - so the install
    succeeded and the guard then reported zero blocks. Whatever identifies the
    block has to survive the edit.
    """
    css = open(os.path.join(HERE, "landing.css"), encoding="utf-8").read()
    cand = [m for m in re.finditer(r"<style>[\s\S]*?</style>", s) if ".lp{" in m.group(0)]
    if len(cand) != 1:
        sys.exit("restyle: %d style blocks contain .lp{ in index.html" % len(cand))
    m = cand[0]
    new = "<style>" + css + "</style>"
    return s if m.group(0) == new else s[:m.start()] + new + s[m.end():]


# ---------------------------------------------------------------- the footer
# Cut from 48 links to 23, on request: "footer is a huge mess, keep it simple
# down there, good SEO, but not 50 options."
#
# WHAT WAS DROPPED AND WHY IT IS SAFE. The old "Learn" (13) and "Browse" (21)
# columns listed the leaf articles. Every one of those 36 pages sits in the
# mega-panel in the HEADER of all 133 pages, so each keeps a sitewide internal
# link and nothing becomes an orphan. What the footer repeats now is the five
# topic hubs and the three indexes - the structure a crawler should see on
# every page - rather than the leaf list, which it already sees above.
#
# The Terms / Privacy / report-a-figure column is captured from the page and
# re-emitted verbatim, so the legal small print is never rewritten by this pass.
FOOT = [
    ("Tools", [("practice-simulator.html", "Practice Simulator"),
               ("therapist-tax-strategy-california.html", "Tax &amp; Retirement"),
               ("grow-your-therapy-practice.html", "Grow Your Practice"),
               ("associate-mft-job-advisor.html", "Associate Job Advisor"),
               ("amft-3000-hours-california.html", "3,000 Hours"),
               ("therapist-cost-of-living-california.html", "Cost of Living")]),
    ("Topics", [("money/", "Money"),
                ("licensure/", "Licensure"),
                ("getting-paid/", "Getting paid"),
                ("practice/", "Running a practice"),
                ("training/", "Training")]),
    ("Browse", [("resources.html", "Everything"),
                ("questions.html", "Every question"),
                ("calculators.html", "All the calculators"),
                ("changes.html", "What changed")]),
    ("About", [("about.html", "What this is"),
               ("newsletter.html", "Stay updated"),
               ("contact.html", "Contact"),
               ("affiliate-disclosure.html", "Affiliate disclosure")]),
]
FOOT_HREFS = {h for _n, its in FOOT for h, _t in its}


def build_footcols(small_print, pre=""):
    cols = []
    for name, items in FOOT:
        links = "".join('<a href="%s">%s</a>' % (link(h, pre), t) for h, t in items)
        cols.append("<div><h5>%s</h5>%s</div>" % (name, links))
    cols.append(small_print)
    return '<div class="ftcols">%s</div>' % "".join(cols)


ALL_ENTRIES = [e for _k, _l, its, _h in GROUPS for e in its]
KEYS = [k for k, _l, _i, _h in GROUPS]


def main():
    sheet = open(os.path.join(HERE, "restyle.css"), encoding="utf-8").read()
    block = "\n<style>" + MARK + "\n" + sheet.rstrip() + "\n" + END + "</style>\n"

    canon = open(os.path.join(SITE, CANON), encoding="utf-8").read()
    sp = panel_span(canon)
    if not sp:
        sys.exit("restyle: cannot find the reference panel in " + CANON)
    icons = harvest_icons(canon[sp[0]:sp[1]])
    if len(icons) < 8:
        sys.exit("restyle: harvested only %d icons - the panel shape changed" % len(icons))

    panel = {p: build_panel(icons, p) for p in ("", "../")}
    links = build_links()

    def delta(t):
        nos = re.sub(r"<script[\s\S]*?</script>", "", t)
        return len(re.findall(r"<div\b", nos)) - len(re.findall(r"</div>", nos))

    pre_delta, pre_words = {}, {}
    n_font = n_links = n_panel = n_script = n_dupe = n_foot = 0

    for f, pre in pages():
        path = os.path.join(SITE, f)
        s = open(path, encoding="utf-8").read()
        before = s
        pre_delta[f] = delta(s)
        pre_words[f] = words(s)

        # ---- 1. the font request
        s2 = FONTHREF.sub(lambda m: 'href="%s"' % patch_font(m.group(1)), s)
        if s2 != s:
            n_font += 1
        s = s2

        # ---- 2. the seven buttons. <nav> is not nestable here, so a regex is
        #        honest; the panel below is, which is why it is not.
        lm = LINKS.search(s)
        if lm and lm.group(0) != links:
            s = s[:lm.start()] + links + s[lm.end():]
            n_links += 1

        # ---- 3. the panel
        sp2 = panel_span(s)
        if sp2 and s[sp2[0]:sp2[1]] != panel[pre]:
            s = s[:sp2[0]] + panel[pre] + s[sp2[1]:]
            n_panel += 1

        # ---- 4. the script. REPLACED, not merely inserted when absent: the
        #        behaviour changed with the IA, and a page keeping the old
        #        script would show a panel whose groups never unhide - a menu
        #        that opens onto nothing, with no error anywhere.
        # The test is `id="navpanel"`, not the bare word. This pass appends a
        # stylesheet that mentions `.navpanel` in a selector, so after step 6 a
        # substring test for "navpanel" is true of every page it has touched -
        # including ones with no header at all. A guard that cannot tell a panel
        # from a mention of a panel fails the wrong pages.
        if 'id="navpanel"' in s:
            found = [m for m in re.finditer(r"<script>[\s\S]*?</script>", s)
                     if "navpanel" in m.group(0)]
            if found and found[0].group(0) != SCRIPT:
                m = found[0]
                s = s[:m.start()] + SCRIPT + s[m.end():]
                n_script += 1
            elif not found:
                s = s.replace("</body>", SCRIPT + "\n</body>", 1)
                n_script += 1

        # ---- 5. the footer columns. The small-print column is lifted out of
        #        the page and handed back unchanged - this pass rewrites the
        #        navigation columns and never the legal text.
        fm = re.search(r'<div class="ftcols">[\s\S]*?</div></div>', s)
        if fm:
            spm = re.search(r"<div><h5>The small print</h5>[\s\S]*?</div>", fm.group(0))
            if spm:
                nf = build_footcols(spm.group(0), pre)
                if fm.group(0) != nf:
                    s = s[:fm.start()] + nf + s[fm.end():]
                    n_foot += 1

        # ---- 6. duplicate stylesheet links
        s2 = dedupe_css(s)
        if s2 != s:
            n_dupe += 1
        s = s2

        # ---- 7. this pass's own stylesheet, last
        s = STYLEBLOCK.sub("", s)
        for name in mine():
            s = re.sub(r'\n?[ \t]*<link rel="stylesheet" href="(?:\.\./)*css/%s">' % name, "", s)
        # Only pages carrying the site masthead. tycoon.html is a standalone
        # mockup with its own visual language and no site chrome; giving it the
        # site's heading face would be a change nobody asked for.
        if 'class="sitenav"' in s:
            s = s.replace("</body>", block + "</body>", 1)

        # ---- 8. the landing stylesheet
        if f == CANON:
            s = install_landing(s)

        if s != before:
            open(path, "w", encoding="utf-8").write(s)

    print("font requests   %d" % n_font)
    print("buttons         %d" % n_links)
    print("panels          %d" % n_panel)
    print("scripts         %d" % n_script)
    print("footers          %d" % n_foot)
    print("duplicate links %d page(s) cleaned" % n_dupe)

    guard(pre_delta, pre_words, delta)


def words(s):
    """Visible words in the page CONTENT - header and footer excluded.

    The parity guard exists to catch a restyle that silently eats a sentence of
    the article. It must not fire when the chrome changes on purpose, which it
    now does: the footer went from 48 links to 23. So measure between the
    header and the footer, and check the chrome separately - the footer has its
    own guard below, which asserts the exact link set rather than a word count.
    """
    body = s[s.index("<body"):] if "<body" in s else s
    body = re.sub(r"<header[\s\S]*?</header>", "", body)
    body = re.sub(r"<footer[\s\S]*?</footer>", "", body)
    t = re.sub(r"<style[\s\S]*?</style>", "", re.sub(r"<script[\s\S]*?</script>", "", body))
    return len(re.sub(r"\s+", " ", re.sub(r"<[^>]+>", " ", t)).strip().split())


def mine():
    """css/*.css files this pass is the author of, by marker not by hash.

    The hash changes every time restyle.css is edited, so the only stable
    identifier is the comment the file opens with.
    """
    out = []
    d = os.path.join(SITE, "css")
    if os.path.isdir(d):
        for n in sorted(os.listdir(d)):
            if n.endswith(".css") and MARK in open(os.path.join(d, n), encoding="utf-8").read(64):
                out.append(re.escape(n))
    return out


def guard(pre_delta, pre_words, delta):
    bad = 0
    for f, pre in pages():
        s = open(os.path.join(SITE, f), encoding="utf-8").read()
        if 'id="navpanel"' not in s:
            continue
        want = {link(h, pre) for h, _t, _b, _br in ALL_ENTRIES} | {link(PROMO[0], pre)}

        # behaviour, not markup: the panel must have something that opens it
        if not re.search(r"<script>[\s\S]*?navpanel[\s\S]*?</script>", s):
            print("GUARD %s: panel present, nothing to open it" % f); bad += 1
        sp = panel_span(s)
        if not sp:
            print("GUARD %s: panel markup unreadable" % f); bad += 1
            continue
        pan = s[sp[0]:sp[1]]

        missing = want - set(re.findall(r'<a[^>]+href="([^"]+)"', pan))
        if missing:
            print("GUARD %s: panel missing %s" % (f, ", ".join(sorted(missing)))); bad += 1
        if pan.count("<img") != len(ALL_ENTRIES) + 1:
            print("GUARD %s: %d icons, expected %d"
                  % (f, pan.count("<img"), len(ALL_ENTRIES) + 1)); bad += 1

        # A button whose data-nav names no column opens onto an empty panel, and
        # a column no button names is unreachable. Both look fine in the markup.
        btn = set(re.findall(r'data-nav="([^"]+)"', s))
        col = set(re.findall(r'class="np-col" data-group="([^"]+)"', pan))
        if btn != set(KEYS) or col != set(KEYS):
            print("GUARD %s: buttons %s, columns %s, expected %s"
                  % (f, sorted(btn), sorted(col), sorted(KEYS))); bad += 1

        for h in set(re.findall(r'<a[^>]+href="([^"]+)"', pan)):
            if h.startswith("http") or "#" in h:
                continue
            p = os.path.normpath(os.path.join(SITE, os.path.dirname(f), h))
            if not (os.path.exists(p) or os.path.isdir(p.rstrip("/"))):
                print("GUARD %s: panel links to missing %s" % (f, h)); bad += 1

        if s.count('id="navpanel"') != 1:
            print("GUARD %s: %d panels" % (f, s.count('id="navpanel"'))); bad += 1

        # This pass replaces a nestable element in place. If the replacement ever
        # closes a different number of divs than it opened, everything below the
        # header is silently reparented. Compare the balance BEFORE and AFTER,
        # not against zero: five pages carry a genuine unclosed div in their
        # markup, on the live site, today, with nothing to do with this pass.
        # What THIS pass must guarantee is that it does not make things worse.
        if f in pre_delta and delta(s) != pre_delta[f]:
            print("GUARD %s: div balance moved %+d -> %+d"
                  % (f, pre_delta[f], delta(s))); bad += 1

        # The footer, by link set rather than by count. A column silently
        # dropped looks identical to a column deliberately dropped.
        fm = re.search(r'<div class="ftcols">[\s\S]*?</div></div>', s)
        if fm:
            got = {h[len(pre):] if pre and h.startswith(pre) else h
                   for h in re.findall(r'<a href="([^"]+)"', fm.group(0))}
            missing = FOOT_HREFS - got
            if missing:
                print("GUARD %s: footer missing %s" % (f, ", ".join(sorted(missing)))); bad += 1
            if "terms.html" not in got or "privacy.html" not in got:
                print("GUARD %s: footer lost the small print" % f); bad += 1

        # Content parity. A restyle that loses a sentence is not a restyle.
        if f in pre_words and words(s) < pre_words[f] - 3:
            print("GUARD %s: words %d -> %d" % (f, pre_words[f], words(s))); bad += 1

    if bad:
        sys.exit("restyle: %d guard failure(s)" % bad)
    print("guards clean")


if __name__ == "__main__":
    main()
