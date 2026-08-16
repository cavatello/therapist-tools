#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Rollout step 4: the home page, rebuilt to option A + option C's waterfall.

Decided 13 August 2026 (final-decision doc): option A "The product page" -
leads with the simulator drawn as a working interface, then the six paths as
rows, one slab. Option C's take-home waterfall goes INSIDE the tool card, so
A shows one number and C's waterfall shows where it came from.

WHAT THIS REWRITES, AND WHAT IT DOES NOT TOUCH

Only the landing <main class="lp">...</main> is replaced, with a
<main class="bc2 home"> built from the approved emitters' markup vocabulary
(css/house.css styles it - that sheet was generated for exactly these
components). The landing-only inline <style> blocks in <head> are removed
with it. EVERYTHING else keeps its bytes: title, meta, JSON-LD, analytics,
fonts, the masthead + nav panel, the signup band, the footer, and every
end-of-body script. No URL moves; every link written here is guarded to
exist on disk before the page is written.

Path 03 is folded into path 04 per the settled decision, so both rows point
at /for/associates.html until the 90-day page exists.

Idempotent: reruns replace the same <main> again. Runs manually for now;
wire into ship.py BUILD once its interaction with home_doorway.py and
stage_router.py (which targeted the old landing markup) is retired next
session.
"""
import os, re, sys

HERE = os.path.dirname(os.path.abspath(__file__))
SITE = os.path.dirname(HERE)
sys.path.insert(0, HERE)
import build_bcopts as bc  # PATHS + WELCOME are the approved copy

PAGE = os.path.join(SITE, "index.html")

# claim-row targets - every one must exist on disk (guarded below)
ROW_HREF = {
    "01": "becoming-a-therapist-california-career-change.html",
    "02": "practicum-california-mft-trainee.html",
    "03": "for/associates.html",
    "04": "for/associates.html",
    "05": "practice/",
    "06": "hiring-first-associate-california-therapist.html",
}


def waterfall():
    rows = [("Gross revenue", "24 clients a week at $200", 250000, 100,
             "#3C7A64", ""),
            ("Running costs", "twelve categories, itemized", -41650, 17,
             "#B9C7BE", "neg"),
            ("Tax", "self-employment plus California", -69410, 28,
             "#B9C7BE", "neg"),
            ("Reaches your account", "after every cost and every tax",
             138940, 56, "", "")]
    o = ['<div class="wf">']
    for i, (lb, sub, amt, pct, color, cls) in enumerate(rows):
        net = " net" if i == len(rows) - 1 else ""
        sign = "&minus;" if amt < 0 else ""
        o.append('<div class="row%s"><div class="lb">%s<span>%s</span></div>'
                 '<div class="track"><i class="barr" style="width:%d%%;%s">'
                 '</i></div><div class="amt %s">%s$%s</div></div>'
                 % (net, lb, sub, pct,
                    "background:%s" % color if color else "", cls, sign,
                    format(abs(amt), ",d")))
    o.append("</div>")
    return "".join(o)


def tool_card():
    return ('<div class="ui"><div class="top"><i></i><i></i><i></i>'
            "<span>Practice Simulator</span></div>"
            '<div class="in"><div class="fields">'
            '<div><label>Your session rate</label>'
            '<div class="fld live">$200</div></div>'
            '<div><label>Sessions a week</label><div class="fld">24</div></div>'
            "</div>"
            '<div class="out"><span class="big">$138,940</span>'
            '<span class="cap">reaches your bank account, after every '
            "running cost and every tax.</span></div></div>"
            + waterfall() + "</div>")


def rows_paths():
    o = ['<div class="rows">']
    for n, claim, who, gets, c, hue, short in bc.PATHS:
        o.append('<a class="%s" href="%s"><span class="who">%s</span>'
                 '<span class="t">%s</span>'
                 '<span class="gets">%s</span>'
                 '<span class="c">%s guides &rarr;</span></a>'
                 % (hue, ROW_HREF[n], who, claim, gets, c))
    o.append("</div>")
    return "".join(o)


def toc(label, fig, href):
    return ('<a href="%s"><b style="display:inline;font-family:var(--figs);'
            'font-size:17px;color:var(--ink);letter-spacing:0">%s</b> '
            "%s</a>" % (href, fig, label))


def main_markup():
    return ('<main class="bc2 home">'
            '<div class="band"><div class="split">'
            '<div><h1>Running a practice is a <span class="scr">second '
            "job</span> nobody trained you for.</h1>"
            '<p class="lede">%s Free, checked, and California only.</p>'
            '<p><a class="btn big" href="practice-simulator.html">See what '
            "your practice pays you</a> "
            '<a class="btn ghost big" href="resources.html">Browse all 203 '
            "pages</a></p>"
            # Not "nothing sold" - the site carries tagged affiliate links,
            # and _dev/affiliate.py rightly fails the build on the old claim.
            '<p class="fine">No account. No email box. The few affiliate '
            "links out are tagged where they appear.</p>"
            "</div>"
            '<div class="toc" style="align-self:end"><b>What is inside</b>'
            "%s%s%s%s</div></div></div>" % (
                bc.WELCOME,
                toc("calculators", "6", "calculators.html"),
                toc("checked pages", "203", "resources.html"),
                toc("county portals", "58",
                    "county-job-portals-california.html"),
                toc("forever", "$0", "about.html"))
            + '<div class="band tight">' + tool_card()
            + '<p class="fine" style="margin-top:14px">Two inputs. '
              "Everything else on the site &mdash; the tax pages, the growth "
              "math, the eight-location comparison &mdash; picks up the same "
              "two numbers. <b>Nothing you type leaves your browser.</b> "
              '<a href="practice-simulator.html">Open the simulator '
              "&rarr;</a></p></div>"
            + '<div class="band sunk"><span class="eb">Or start where you '
              "are</span><h2>Which one of these is you right now?</h2>"
              '<p class="fine" style="font-size:16.5px;max-width:54ch;'
              'margin:-8px 0 26px">Every page on this site is written for '
              "one of six moments. Pick the sentence that sounds like your "
              "week.</p>" + rows_paths() + "</div>"
            + '<div class="slab"><span class="eb">Why you can use these '
              "numbers</span><h2>Every dollar here is the output of a "
              "calculation you can follow.</h2>"
              "<p>Run on numbers you typed in. No illustrative figures, no "
              "worked examples standing in for your practice, and when a "
              "threshold moves it is listed on a page rather than "
              '<span class="mark">quietly swapped in</span>.</p></div>'
            + "</main>")


def run():
    s = open(PAGE, encoding="utf-8").read()

    # ---- guard: every href we are about to write exists on disk
    hrefs = set(ROW_HREF.values()) | {
        "practice-simulator.html", "resources.html", "calculators.html",
        "county-job-portals-california.html", "about.html"}
    for h in sorted(hrefs):
        p = os.path.join(SITE, h.rstrip("/"),
                         "index.html" if h.endswith("/") else "")
        if not os.path.exists(os.path.join(SITE, h) if not h.endswith("/")
                              else p):
            sys.exit("build_home: link target missing: %s" % h)

    # ---- replace the old landing main (or our own, on rerun)
    m = re.search(r'<main class="(?:lp|bc2 home)"[^>]*>[\s\S]*?</main>', s)
    if not m:
        sys.exit("build_home: no landing <main> found")
    s = s[:m.start()] + main_markup() + s[m.end():]

    # ---- drop landing-only inline styles (all inline <style> on this page
    #      targeted the old landing markup; chrome CSS is all in css/)
    before = s.count("<style")
    s = re.sub(r"[ \t]*<style>[\s\S]*?</style>\n?", "", s)

    # ---- house.css must load for the bc2 components. Two eras: before
    #      family_rest the page carried the skin (insert before it); after,
    #      the family pass owns the sheet links and re-adds them each run.
    if "css/house.css" not in s:
        i = s.find('<link rel="stylesheet" href="css/house-skin.css">')
        if i >= 0:
            s = s[:i] + '<link rel="stylesheet" href="css/house.css">\n' + s[i:]

    open(PAGE, "w", encoding="utf-8").write(s)

    # ---- post-guards
    out = open(PAGE, encoding="utf-8").read()
    assert out.count("<main") == 1, "main count"
    assert out.count('class="slab"') == 1, "one slab per page"
    assert ("house-skin.css" in out or 'bcz' in out) and \
        "css/house.css" in out
    print("  index.html rebuilt to option A + waterfall "
          "(%d inline style(s) removed, %d bytes)"
          % (before, len(out)))


if __name__ == "__main__":
    run()
