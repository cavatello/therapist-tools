#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Option 2, the three-rail document, applied to terms.html and privacy.html.

The audit reported both at **49% of a 1440 laptop** and about 28% of a 5K
display. That is not a measure bug — a 66ch column is correct for a document
somebody has to read carefully, and widening it would be worse. The problem is
that the page has nothing else to put in the remaining width, so it reads as
broken rather than as typeset.

These two pages are also the cheapest possible place to prove the pattern,
because they already carry the hardest part: a hand-built "On this page" list.
That list becomes the sticky left rail. All this adds is a right rail carrying
the three things a reader of a legal page actually wants next — the plain-English
summary of what the page means, the other legal page, and a route back into the
tools — and the grid to hold them.

Below 1100px nothing changes: the rails collapse and the page is exactly what it
is today, TOC on top and prose beneath.
"""
import os, re

HERE = os.path.dirname(os.path.abspath(__file__))
SITE = os.path.dirname(HERE)
MARK = "/* _dev/legal_rails.py */"
TAG = "<!-- legal-rail -->"

PAGES = {
    "terms.html": dict(
        other=("privacy.html", "Privacy", "what is collected, by whom, and how to stop it"),
        gist="Everything here is arithmetic and reference material, not advice. It is free, "
             "provided as-is, and you are responsible for what you decide with it."),
    "privacy.html": dict(
        other=("terms.html", "Terms of Use", "what this site is, and what it is not"),
        gist="No account, and nothing you type into a calculator is sent anywhere. Your "
             "setup lives in the address bar of your own browser."),
}

TOOLS = [("practice-simulator.html", "Practice simulator"),
         ("therapist-tax-strategy-california.html", "Tax &amp; retirement"),
         ("tools.html", "All free tools")]

CSS = """
/* THREE RAILS, from 1100px up. The reading measure does not change - it is
   correct at 66ch and always was. What changes is that the width either side of
   it stops being empty: the page's own "On this page" list becomes a sticky rail
   on the left, and a second rail on the right carries the summary, the sibling
   legal page and the way back into the tools.
   Below 1100px every rule here is inert and the page is what it was. */
@media (min-width:1100px){
  .lgbody > .lgwrap{
    max-width:1240px;
    display:grid;
    /* the MIDDLE column is capped in ch, not in fr. With 1fr the reading column
       grew to ~84ch on a 5K display - the rails stopped the page looking broken
       but the prose got harder to read, which is the thing this was protecting
       in the first place. */
    grid-template-columns:210px minmax(0,68ch) 250px;
    grid-template-rows:auto;
    justify-content:center;
    gap:0 clamp(36px,4vw,72px);
    align-items:start}
  /* grid-row:1/-1, not row 1. With the rails on row 1 only, every prose section
     after the first was pushed down to row 2 - which starts below the TALLEST
     row-1 item, i.e. below the whole table of contents. That left a screen of
     empty space between section 1 and section 2. Spanning all rows and sticking
     inside the span is the correct shape. */
  .lgbody > .lgwrap > .lgtoc{grid-column:1;align-self:start;position:sticky;top:22px;margin:0;padding:0;border:0;background:none}
  /* the TOC ships as a two-column list, which is right at full width and wrong
     in a 210px rail - every entry wrapped to three lines. */
  .lgbody > .lgwrap > .lgtoc ol{columns:1 !important;column-count:1 !important;
    display:block !important;grid-template-columns:none !important}
  .lgbody > .lgwrap > .lgtoc h2{font-size:11px;letter-spacing:.12em;
    text-transform:uppercase;font-family:'IBM Plex Mono',monospace;font-weight:600;
    opacity:.6;margin:0 0 10px}
  .lgbody > .lgwrap > .lgtoc ol{margin:0;padding:0 0 0 1.35em}
  .lgbody > .lgwrap > .lgtoc li{margin:0 0 2px;font-size:12.6px;line-height:1.35}
  .lgbody > .lgwrap > .lgtoc a{display:block;padding:5px 0;min-height:30px}
  /* the prose is ONE grid child, not N. `grid-row:1/-1` on the rails spans a
     single row when the grid has no explicit rows, so with every section as its
     own child the second section landed on row 2 - which starts below the whole
     table of contents, leaving 351px of white space mid-document. Wrapping the
     sections makes the grid exactly three children in one row. */
  .lgbody > .lgwrap > .lgmain{grid-column:2;min-width:0}
  .lgrail{grid-column:3;align-self:start;position:sticky;top:22px;
    display:grid;gap:12px}
}
@media (max-width:1099px){.lgrail{display:none}}
@media (min-width:1600px){.lgbody > .lgwrap{max-width:1400px}}

.lgrail .c{border:1px solid var(--line,#E7E2D6);border-radius:14px;padding:15px 17px;
  background:#fff}
.lgrail .c > p:first-child{font-family:'IBM Plex Mono',monospace;font-size:9.8px;
  letter-spacing:.11em;text-transform:uppercase;margin:0 0 7px;opacity:.7}
.lgrail .c b{display:block;font-family:Fraunces,Georgia,serif;font-size:16.5px;
  font-weight:600;line-height:1.2;margin:0 0 4px}
.lgrail .c span{display:block;font-size:12.4px;line-height:1.5;opacity:.72}
.lgrail .c .gist{font-size:12.8px;line-height:1.6;margin:0}
.lgrail a{display:flex;align-items:center;min-height:44px;font-size:12.8px;
  font-weight:700;text-decoration:none;border-top:1px dashed var(--fline,#E4D9BE)}
.lgrail a:first-of-type{border-top:0}
.lgrail a:hover{text-decoration:underline}
"""


def rail(cfg):
    oh, ol, od = cfg["other"]
    return (TAG + '<aside class="lgrail" aria-label="Related">'
            '<div class="c"><p>In plain English</p>'
            '<p class="gist">' + cfg["gist"] + '</p></div>'
            '<div class="c"><p>The other one</p><b>' + ol + '</b>'
            '<span>' + od + '</span><a href="' + oh + '">Read it &rarr;</a></div>'
            '<div class="c"><p>Back to the point</p>'
            + "".join('<a href="%s">%s &rarr;</a>' % (h, l) for h, l in TOOLS)
            + '</div></aside>')


def main():
    for slug, cfg in sorted(PAGES.items()):
        path = os.path.join(SITE, slug)
        s = open(path, encoding="utf-8").read()

        s = re.sub(re.escape(TAG) + r'<aside class="lgrail".*?</aside>', "", s, flags=re.S)
        s = re.sub(r"\n?<style>" + re.escape(MARK) + r".*?/\* end rails \*/</style>\n?",
                   "", s, flags=re.S)

        # the rail is the LAST child of .lgbody > .lgwrap, so it lands in the grid
        # alongside the TOC rather than after the prose.
        i = s.find('<div class="lgbody"><div class="lgwrap">')
        assert i >= 0, "legal body not found in " + slug
        # close of that inner .lgwrap: the last </div></div> before </main>
        end = s.find("</main>", i)
        assert end > 0, slug
        close = s.rfind("</div></div>", i, end)
        assert close > i, "could not find the wrap close in " + slug
        # wrap every section between the TOC and the close in one .lgmain
        toc_end = s.index("</nav>", i) + len("</nav>")
        s = (s[:toc_end] + '<div class="lgmain">' + s[toc_end:close]
             + "</div>" + rail(cfg) + s[close:])

        s = s.replace("</body>", "\n<style>" + MARK + CSS + "/* end rails */</style>\n</body>", 1)
        open(path, "w", encoding="utf-8").write(s)
        print("%-16s rail added" % slug)

    for slug in PAGES:
        s = open(os.path.join(SITE, slug), encoding="utf-8").read()
        assert s.count('class="lgrail"') == 1, slug
        assert s.count('class="lgmain"') == 1, slug
        assert s.count(MARK) == 1, slug
        assert s.count("<h1") == 1, slug


if __name__ == "__main__":
    main()
