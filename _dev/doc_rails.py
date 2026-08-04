#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Option 2, the three-rail document, applied to rates.html.

rates.html is the site's one true editorial page: a 900px `.article`, five h2
sections, citation-dense, meant to be read start to finish. It is also the page
`_dev/widen.py` deliberately did NOT touch, because 900px is a correct reading
measure and stretching it would make the piece worse.

So it has the terms.html problem in its purest form: nothing wrong with the
column, everything wrong with the two-thirds of a wide display sitting empty
either side of it.

Unlike terms.html it does not ship a table of contents, and its h2s have no ids
— so this generates both. Slugs come from the heading text, which means a
reworded heading changes its own anchor; that is the right trade for a page
whose headings are the outline.

The tax page is NOT a candidate for this treatment, despite being long and
cited: its sections are full-bleed coloured slabs, not a prose column, and
squeezing them into a 68ch grid track would wreck the design it was built
around. It wants Option 1 or 3.
"""
import os, re

HERE = os.path.dirname(os.path.abspath(__file__))
SITE = os.path.dirname(HERE)
SLUG = "rates.html"
MARK = "/* _dev/doc_rails.py */"
OPEN, CLOSE = "<!-- doc-rails -->", "<!-- /doc-rails -->"

ROUTES = [
    ("What this means for your own week", "practice-simulator.html",
     "Practice simulator", "put a rate and a caseload in, get what actually lands"),
    ("If the rate is not the problem", "grow-your-therapy-practice.html",
     "Grow your practice", "what a client is worth, and where the next one comes from"),
    ("Paid on a fee split?", "associate-mft-job-advisor.html",
     "Job advisor", "what the practice bills for your hour against what it pays you"),
]

CSS = """
/* THREE RAILS on the editorial page, from 1100px up.
   The measure stays where it was - this is a piece to be read, and 900px of
   .article is about 72ch, which is right. What changes is that the space either
   side of it carries the outline and the routes out instead of nothing.
   Below 1100px every rule here is inert. */
.drwrap{max-width:900px;margin:0 auto}
@media (min-width:1100px){
  .drwrap{max-width:1240px;display:grid;
    grid-template-columns:200px minmax(0,900px) 240px;
    justify-content:center;gap:0 clamp(28px,3vw,56px);align-items:start}
  .drnav{grid-column:1;align-self:start;position:sticky;top:22px}
  .drwrap > .article{grid-column:2;min-width:0;padding-left:0;padding-right:0}
  .drrail{grid-column:3;align-self:start;position:sticky;top:22px;display:grid;gap:12px}
}
@media (min-width:1700px){.drwrap{max-width:1400px}}
@media (max-width:1099px){.drnav,.drrail{display:none}}

.drnav p.t{font-family:'IBM Plex Mono',monospace;font-size:9.8px;letter-spacing:.12em;
  text-transform:uppercase;opacity:.6;margin:0 0 9px}
.drnav a{display:block;font-size:12.6px;line-height:1.34;padding:7px 0 7px 11px;
  min-height:34px;text-decoration:none;color:inherit;opacity:.66;
  border-left:2px solid rgba(0,0,0,.1)}
.drnav a:hover{opacity:1}
.drnav a.on{opacity:1;font-weight:600;border-left-color:currentColor}
.drrail .c{border:1px solid rgba(0,0,0,.11);border-radius:14px;padding:14px 16px;
  background:rgba(255,255,255,.62)}
.drrail .c p.t{font-family:'IBM Plex Mono',monospace;font-size:9.6px;letter-spacing:.11em;
  text-transform:uppercase;opacity:.7;margin:0 0 6px}
.drrail .c b{display:block;font-size:15.5px;font-weight:700;line-height:1.2;margin:0 0 3px}
.drrail .c span{display:block;font-size:12.2px;line-height:1.5;opacity:.72;margin:0 0 8px}
.drrail .c a{display:flex;align-items:center;min-height:44px;font-size:12.6px;
  font-weight:700;text-decoration:none;color:inherit}
.drrail .c a:hover{text-decoration:underline}
"""

# Scroll-spy. No library, no dependency: an IntersectionObserver over the same
# headings the nav was generated from.
JS = """
(function(){
  var nav = document.querySelector('.drnav'); if(!nav) return;
  var links = [].slice.call(nav.querySelectorAll('a'));
  var map = {};
  links.forEach(function(a){ map[a.getAttribute('href').slice(1)] = a; });
  var heads = links.map(function(a){
    return document.getElementById(a.getAttribute('href').slice(1)); }).filter(Boolean);
  if (!heads.length) return;
  function mark(id){ links.forEach(function(a){
    a.classList.toggle('on', a.getAttribute('href') === '#' + id); }); }
  /* rootMargin pins the trigger line near the top of the viewport, so the
     highlighted entry is the section you are reading, not the one scrolling
     into the bottom of the screen. */
  var io = new IntersectionObserver(function(es){
    es.forEach(function(e){ if (e.isIntersecting) mark(e.target.id); });
  }, {rootMargin: '-12% 0px -80% 0px', threshold: 0});
  heads.forEach(function(h){ io.observe(h); });
  mark(heads[0].id);
})();
"""


def slugify(t):
    t = re.sub(r"<[^>]+>", "", t)
    t = re.sub(r"&[a-z]+;", " ", t)
    return re.sub(r"[^a-z0-9]+", "-", t.lower()).strip("-")[:48]


def main():
    path = os.path.join(SITE, SLUG)
    s = open(path, encoding="utf-8").read()

    # idempotent
    s = re.sub(re.escape(OPEN) + r".*?" + re.escape(CLOSE), "", s, flags=re.S)
    s = re.sub(r"\n?<style>" + re.escape(MARK) + r".*?/\* end doc \*/</style>\n?",
               "", s, flags=re.S)
    s = re.sub(r"\n?<script>" + re.escape(MARK) + r".*?/\* end doc \*/</script>\n?",
               "", s, flags=re.S)
    s = re.sub(r'(<h2)\s+id="[^"]*"', r"\1", s)

    heads = []

    def tag(m):
        inner = m.group(2)
        sid = slugify(inner)
        heads.append((sid, re.sub(r"<[^>]+>", "", inner).strip()))
        return '<h2%s id="%s">%s</h2>' % (m.group(1), sid, inner)

    s = re.sub(r"<h2([^>]*)>(.*?)</h2>", tag, s, flags=re.S)
    assert len(heads) >= 4, "expected the article's five h2s, found %d" % len(heads)
    assert len(set(h[0] for h in heads)) == len(heads), "duplicate heading slugs: %s" % heads

    nav = ('<nav class="drnav" aria-label="On this page"><p class="t">On this page</p>'
           + "".join('<a href="#%s">%s</a>' % (i, t) for i, t in heads) + "</nav>")
    rail = ('<aside class="drrail" aria-label="Where to next">'
            + "".join('<div class="c"><p class="t">%s</p><b>%s</b><span>%s</span>'
                      '<a href="%s">Open it &rarr;</a></div>' % (k, lab, d, h)
                      for k, h, lab, d in ROUTES)
            + "</aside>")

    a = s.index('<div class="article">')
    # the article closes immediately before the colophon
    c = s.index('<div class="colophon">')
    close = s.rfind("</div>", a, c) + len("</div>")
    s = (s[:a] + OPEN + '<div class="drwrap">' + nav + s[a:close] + rail
         + "</div>" + CLOSE + s[close:])

    s = s.replace("</body>", "\n<style>" + MARK + CSS + "/* end doc */</style>\n"
                             "<script>" + MARK + JS + "/* end doc */</script>\n</body>", 1)
    open(path, "w", encoding="utf-8").write(s)

    assert s.count('class="drnav"') == 1 and s.count('class="drrail"') == 1
    assert s.count("<h1") == 1
    print("rates.html: %d sections -> %s" % (len(heads), ", ".join(h[0] for h in heads)))


if __name__ == "__main__":
    main()
