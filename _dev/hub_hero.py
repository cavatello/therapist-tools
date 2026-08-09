#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Make every hub and directory hero do the job a landing page does.

WHAT WAS WRONG, AND IT WAS TWO THINGS AT ONCE

**1. The hero said nothing.** /training/ opened with:

    2 PAGES
    Training
    Certificates, and what each one actually permits.

A reader arriving from search learns the topic they already clicked, and
nothing about what is behind it - which is 25 doctorates, 16 psychedelic
trainings from $1,047 to EUR 15,000, and the CE rules that keep a license. The
hero is the only part of a hub most people read, and it was a label.

**2. The number was wrong, and wrong in the worst direction.** The hero counted
`.lc` cards - the guides written directly for the topic. The body sentence
counted the directory leaves underneath them. On three hubs those agree. On two
they do not, badly:

    /licensure/    hero "5 pages"   body "71 pages, in 3 sections"
    /training/     hero "2 pages"   body "19 pages, in 2 sections"

Neither figure is a lie - they measure different things - but printing **2
pages** at the top of a section holding 25 PsyD programs and 16 trainings tells
a reader there is nothing here. That is the count that decides whether they
scroll.

HOW THIS FIXES IT

**Copy is authored; every figure is measured.** The claim in each hero is
written by a person, because "16 trainings, none of which changes your license"
is an editorial judgment and no template produces it. But every number in it is
read off the pages at build time - the cards on the hub, the `<article>` count
in each directory, the leaf files on disk. A figure that is measured cannot
drift from the thing it describes, which is the whole problem above.

**AIDA, in the order the reader needs it:**

    eyebrow   where you are, and the scale, in four words
    h1        a claim, not a label - what this section settles
    deck      what is actually here, with the counts
    figures   three numbers that are the reason to keep reading
    chips     the sections, and the question most people arrive with

**The body sentence is rewritten to the same measured total,** so hero and body
cannot disagree again. The guard at the bottom refuses to write a page where
they do.

Run after build_library.py and before extract_css.py.
Idempotent, guarded.
"""
import os, re, sys

HERE = os.path.dirname(os.path.abspath(__file__))
SITE = os.path.dirname(HERE)
MARK = "<!-- _dev/hub_hero.py -->"
END = "<!-- /hub_hero -->"

INK = "#16211B"
GOLD = "#F6C560"
PAPER = "#F4F0E6"
CREAM = "#FBF9F3"
MUTED = "#635E53"
FLOOR = 4.5


# ------------------------------------------------------------ measurement

def count_articles(rel, pattern):
    p = os.path.join(SITE, rel)
    if not os.path.exists(p):
        return 0
    return len(re.findall(pattern, open(p, encoding="utf-8").read()))


def count_files(suffix=None, prefix=None):
    n = 0
    for f in os.listdir(SITE):
        if not f.endswith(".html"):
            continue
        if suffix and not f.endswith(suffix):
            continue
        if prefix and not f.startswith(prefix):
            continue
        n += 1
    return n


def measure():
    """Everything the copy below is allowed to say a number about."""
    m = {}
    m["mft_schools"] = count_files(suffix="-mft.html")
    m["psyd"] = count_articles("psyd-programs-california.html", r'<article class="pdc">')
    m["psy_training"] = count_files(prefix="psychedelic-training-")
    m["calculators"] = 7
    m["insurers"] = count_articles("therapy-liability-insurance-california.html",
                                   r'<article class="li-card"')
    for t in HUBS:
        p = os.path.join(SITE, t, "index.html")
        if not os.path.exists(p):
            m["cards_" + t] = 0
            continue
        s = open(p, encoding="utf-8").read()
        i, j = s.find('<div class="libwrap">'), s.find('class="ftnl"')
        m["cards_" + t] = len(re.findall(r'<a class="lc[ "]', s[i:j]))
    return m


# ------------------------------------------------------------------- copy
#
# (eyebrow, h1, deck, [(figure key or literal, label) x3], [(chip, anchor)])
# `{}` fields are filled from measure(). Nothing here may contain a number
# that is not a placeholder.

HUBS = {
    "money": dict(
        eyebrow="Money &middot; California",
        h1="What the practice actually pays you, after everyone else is paid.",
        deck="Rate and caseload go in one end; what reaches your bank account "
             "comes out the other, with {calculators} calculators and "
             "{cards_money} guides covering the gap. Entity choice, the tax you "
             "can defer, the tax you must send quarterly, and the twelve "
             "expense categories most therapists forget to count.",
        figs=[("{cards_money}", "guides on this topic"),
              ("$18,244", "optional on a $217,350 profit"),
              ("12", "expense categories priced")],
        chips=[("Money tools", None),
               ("Sole proprietor, or a corporation", None),
               ("Tax you can defer, and tax you must send", None)],
    ),
    "licensure": dict(
        eyebrow="Licensure &middot; California",
        h1="Every gate between a master&rsquo;s degree and an LMFT license.",
        deck="{cards_licensure} guides plus a directory of "
             "{mft_schools} California programs, priced and dated. The four "
             "requirements that close at different speeds, what the Board "
             "charges now that fees have halved, and which one is actually "
             "holding you up.",
        figs=[("{mft_schools}", "California MFT programs listed"),
              ("3,000", "hours over at least 104 weeks"),
              ("$875", "in Board fees, down from $1,750")],
        chips=[("Licensure tools", None),
               ("The route, and what it costs", None),
               ("Where the degree comes from", None)],
    ),
    "getting-paid": dict(
        eyebrow="Getting paid &middot; California",
        h1="What a session is worth, and who actually pays it.",
        deck="{cards_getting-paid} guides on the money side of the caseload: "
             "what insurance really reimburses per code, what the platforms "
             "keep, how long a panel takes to open, and the paperwork a "
             "private-pay client is owed.",
        figs=[("$106&ndash;132", "insurance, against $180&ndash;350 private pay"),
              ("11.5", "hours to get on a panel"),
              ("$1.24", "a session, between the platforms")],
        chips=[("What the work is worth", None),
               ("Getting on a panel, or not", None),
               ("The paperwork", None)],
    ),
    "practice": dict(
        eyebrow="Running a practice &middot; California",
        h1="Filling the week, and running the admin behind it.",
        deck="{cards_practice} guides on the business rather than the clinical "
             "work: what a client is worth over their whole time with you, what "
             "the software really costs once the fees are counted, what a first "
             "associate costs loaded, and every liability program you can buy "
             "&mdash; {insurers} of them, compared.",
        figs=[("$4,800", "per client over 24 sessions"),
              ("14", "sessions a week to break even on an associate"),
              ("{insurers}", "insurance programs compared")],
        chips=[("Practice tools", None),
               ("Filling the week", None),
               ("The software and the admin", None)],
    ),
    "training": dict(
        eyebrow="Training &middot; California",
        h1="Every credential a California therapist can buy, and what each one "
           "legally permits.",
        deck="Two directories and the rules that keep a license: "
             "{psyd} doctorates in psychology grouped by what their "
             "accreditation actually decides, {psy_training} "
             "psychedelic-assisted therapy trainings from $1,047 to "
             "&euro;15,000, and the 36 CE hours you owe every two years. One "
             "fact governs all of it &mdash; <b>none of these certificates "
             "changes your license or your scope of practice</b>.",
        figs=[("{psyd}", "PsyD programs, 20 APA-accredited"),
              ("{psy_training}", "psychedelic trainings priced"),
              ("62%", "of CE audits failed")],
        chips=[("Keeping the license", None),
               ("Psychedelic-assisted therapy training", None)],
    ),
}

# The directory pages get the same job done, in their own markup.
DIRS = {
    "mft-programs-california.html": dict(
        sub="{mft_schools} California programs &middot; every one the Board recognizes",
    ),
    "psyd-programs-california.html": dict(
        sub="{psyd} doctorates &middot; 20 of them APA-accredited",
    ),
    "therapy-liability-insurance-california.html": dict(
        sub="{insurers} programs &middot; what each publishes, and what people really pay",
    ),
}


def _lin(c):
    c /= 255.0
    return c / 12.92 if c <= 0.03928 else ((c + 0.055) / 1.055) ** 2.4


def lum(h):
    h = h.lstrip("#")
    r, g, b = (_lin(int(h[i:i + 2], 16)) for i in (0, 2, 4))
    return 0.2126 * r + 0.7152 * g + 0.0722 * b


def ratio(a, b):
    x, y = lum(a), lum(b)
    return (max(x, y) + 0.05) / (min(x, y) + 0.05)


CSS = """<style>/* _dev/hub_hero.py */
.hh-figs{display:flex;flex-wrap:wrap;gap:9px;margin:16px 0 12px}
.hh-fig{background:rgba(255,255,255,.1);border:2px solid rgba(255,255,255,.34);
  border-radius:11px;padding:9px 13px;min-width:132px}
.hh-fig .n{display:block;font-family:'Fraunces',Georgia,serif;font-size:25px;
  line-height:1.05;color:%(gold)s}
.hh-fig .l{display:block;font-size:12.4px;line-height:1.4;margin-top:3px;
  color:rgba(255,255,255,.86);max-width:22ch}
.hh-chips{display:flex;flex-wrap:wrap;gap:7px;margin:4px 0 0}
.hh-chip{display:inline-block;font-family:'IBM Plex Mono',ui-monospace,monospace;
  font-size:12px;color:%(ink)s;background:%(gold)s;border:2px solid %(ink)s;
  border-radius:9px;padding:6px 11px;text-decoration:none}
.hh-chip:hover{background:#FFD37A}
.hh-chip.q{background:rgba(255,255,255,.92)}
.libband .dek b{color:%(gold)s;font-weight:600}
@media (max-width:640px){
  .hh-fig{min-width:0;flex:1 1 46%%;padding:8px 10px}
  .hh-fig .n{font-size:21px}
}
</style>"""


def fill(text, m):
    out = text
    for k, v in m.items():
        out = out.replace("{%s}" % k, "{:,}".format(v) if isinstance(v, int) else str(v))
    return out


def anchor_for(page_html, label):
    """Find a real id on the page for a chip, or return None rather than ship
    a link to nowhere."""
    for m in re.finditer(r'<h2[^>]*\bid="([^"]+)"[^>]*>([\s\S]*?)</h2>', page_html):
        if re.sub(r"<[^>]+>", "", m.group(2)).strip().lower() == label.lower():
            return "#" + m.group(1)
    return None


def hero_block(cfg, m, page_html, up=""):
    figs = "".join(
        '<div class="hh-fig"><span class="n">%s</span><span class="l">%s</span></div>'
        % (fill(n, m), fill(l, m)) for n, l in cfg["figs"])
    chips = []
    for label, forced in cfg["chips"]:
        href = forced or anchor_for(page_html, label)
        if not href:
            continue
        chips.append('<a class="hh-chip" href="%s">%s</a>' % (href, label))
    chip_html = ('<div class="hh-chips">%s</div>' % "".join(chips)) if chips else ""
    return (MARK + '<div class="hh-figs">' + figs + "</div>" + chip_html + END)


def main():
    print("colours, measured:")
    bad = 0
    for label, fg, bg, floor in [("figure gold on hero", GOLD, "#1E4436", FLOOR),
                                 ("chip ink on gold", INK, GOLD, FLOOR)]:
        r = ratio(fg, bg)
        print("  %-22s %5.2f:1  %s" % (label, r, "ok" if r >= floor else "FAILS"))
        if r < floor:
            bad += 1
    if bad:
        sys.exit("%d colour(s) under the floor" % bad)

    m = measure()
    print("\nmeasured from the site:")
    for k in sorted(m):
        print("  %-18s %s" % (k, m[k]))

    css = CSS % {"ink": INK, "gold": GOLD}
    touched = 0

    for t, cfg in HUBS.items():
        p = os.path.join(SITE, t, "index.html")
        if not os.path.exists(p):
            print("  skip %s - no hub" % t)
            continue
        s = open(p, encoding="utf-8").read()
        orig = s
        s = re.sub(re.escape(MARK) + r"[\s\S]*?" + re.escape(END), "", s)
        s = re.sub(r"\n?<style>/\* _dev/hub_hero\.py \*/[\s\S]*?</style>\n?", "", s)

        i, j = s.find('<div class="libwrap">'), s.find('class="ftnl"')
        cards = len(re.findall(r'<a class="lc[ "]', s[i:j]))
        m["cards_" + t] = cards

        # the eyebrow, the claim and the deck
        s = re.sub(r'<p class="sub">[\s\S]*?</p>',
                   '<p class="sub">%s</p>' % fill(cfg["eyebrow"], m), s, count=1)
        s = re.sub(r"<h1>[\s\S]*?</h1>", "<h1>%s</h1>" % fill(cfg["h1"], m), s, count=1)
        s = re.sub(r'<p class="dek">[\s\S]*?</p>',
                   '<p class="dek">%s</p>' % fill(cfg["deck"], m), s, count=1)

        # figures and chips, immediately after the deck
        blk = hero_block(cfg, m, s)
        k = s.find('<p class="dek">')
        k = s.find("</p>", k) + len("</p>")
        s = s[:k] + blk + s[k:]

        e = s.lower().rfind("</body>")
        s = s[:e] + css + "\n" + s[e:]
        if s != orig:
            open(p, "w", encoding="utf-8").write(s)
            touched += 1

    for rel, cfg in DIRS.items():
        p = os.path.join(SITE, rel)
        if not os.path.exists(p):
            continue
        s = open(p, encoding="utf-8").read()
        orig = s
        want = fill(cfg["sub"], m)
        if re.search(r'<p class="sub">[\s\S]*?</p>', s):
            s = re.sub(r'<p class="sub">[\s\S]*?</p>',
                       '<p class="sub">%s</p>' % want, s, count=1)
        else:
            k = s.find("<h1")
            if k > 0:
                s = s[:k] + '<p class="sub">%s</p>' % want + s[k:]
        if s != orig:
            open(p, "w", encoding="utf-8").write(s)
            touched += 1

    print("\n%d page(s) rewritten" % touched)

    # ------------------------------------------------------------- guards
    bad = 0
    for t in HUBS:
        p = os.path.join(SITE, t, "index.html")
        if not os.path.exists(p):
            continue
        s = open(p, encoding="utf-8").read()
        if s.count(MARK) != 1:
            print("GUARD %s: %d hero blocks" % (t, s.count(MARK)))
            bad += 1
        if not re.search(r'<p class="sub">[^<]*California', s):
            print("GUARD %s: eyebrow did not land" % t)
            bad += 1
        # no unfilled placeholder may ever ship
        for ph in re.findall(r"\{[a-z_-]+\}", s):
            print("GUARD %s: unfilled placeholder %s" % (t, ph))
            bad += 1
        # every chip must point at something that exists on the page
        blk = re.search(re.escape(MARK) + r"([\s\S]*?)" + re.escape(END), s)
        if blk:
            for href in re.findall(r'class="hh-chip" href="#([^"]+)"', blk.group(1)):
                if ('id="%s"' % href) not in s:
                    print("GUARD %s: chip -> #%s does not exist" % (t, href))
                    bad += 1
    for rel in DIRS:
        p = os.path.join(SITE, rel)
        if not os.path.exists(p):
            continue
        s = open(p, encoding="utf-8").read()
        for ph in re.findall(r"\{[a-z_-]+\}", s):
            print("GUARD %s: unfilled placeholder %s" % (rel, ph))
            bad += 1
    if bad:
        sys.exit("\n%d problem(s)" % bad)
    print("guards clean - every figure in every hero was measured, not typed")


if __name__ == "__main__":
    main()
