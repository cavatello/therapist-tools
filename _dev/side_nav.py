#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""A fixed section nav in the gutter, for the pages the grid template cannot take.

`_dev/legal_rails.py` and `_dev/doc_rails.py` restructure a page into a three
column grid. That only works where the content is ONE column: terms, privacy and
rates all are.

The tax page and the working-remotely page are not. Their sections are separate
`<section>` blocks, each with its own centered wrap, and on the tax page they are
full-bleed coloured slabs — pine, carbon, brick, indigo, gold. Forcing those into
a 68ch grid track would destroy the design they were built around. My own
template matrix said Option 2 for both; that was wrong, and this is the correction.

So: no restructuring at all. A `position:fixed` nav lives in the gutter that
already exists to the left of the centered wrap, and appears only once the
viewport is wide enough to hold it without overlapping anything —
`(viewport - wrap) / 2 > nav + margin`. Below that width it is simply absent, and
the page is byte-for-byte what it renders today.

Section ids and labels are read from the page. A section without an id gets one
slugged from its own h2, so the anchors survive a rebuild.
"""
import os, re

HERE = os.path.dirname(os.path.abspath(__file__))
SITE = os.path.dirname(HERE)
MARK = "/* _dev/side_nav.py */"
OPEN, CLOSE = "<!-- side-nav -->", "<!-- /side-nav -->"

# slug -> (wrap max-width in px, short labels keyed by section id where the h2
# is too long to sit in a 190px rail)
PAGES = {
    "therapist-tax-strategy-california.html": dict(wrap=1060, short={
        "profit": "Your profit", "why": "Why it is optional", "plan": "The plan",
        "which": "Which account", "structure": "Sole prop or corp",
        "remote": "Working remotely", "ss": "Social Security"}),
    "therapist-working-remotely-california.html": dict(wrap=1020, short={}),
}


def css(wrap):
    """Position the nav from the wrap width that is ACTUALLY in effect.

    First attempt hard-coded the page's base wrap (1060px) and computed
    `left: (100vw - 1060)/2 - 214`. But `_dev/widen.py` scales these containers
    to 1320px at >=1500 and 1560px at >=1900 - so on a 2560 display the real
    gutter was 500px while the nav was placed as though it were 750, and the nav
    sat ON TOP of the content. The variable below steps with widen.py, and the
    reveal breakpoint is derived from it rather than guessed.
    """
    W1, W2 = 1320, 1560          # must match _dev/widen.py STEP1/STEP2
    NAV, GAP = 190, 34   # 190 incl. panel padding, 34 of air           # nav width, and the air between nav and content
    need = lambda w: w + 2 * (NAV + GAP + 12)
    return """
/* A section nav in the gutter. No layout change anywhere: it is fixed, and it
   exists only inside the width bands where the gutter can actually hold it.
   THREE bands, not one: the wrap itself steps at 1500 and 1900 (widen.py), so a
   single reveal breakpoint computed from the base wrap showed the nav at 2000px
   where the wrap had already grown to 1560 and the gutter was 220 - the nav ran
   off the left edge of the window. Each band carries its own wrap width and its
   own minimum. */
.sdnav{display:none;position:fixed;top:50%%;transform:translateY(-50%%);
  width:%(nav)dpx;z-index:20;max-height:76vh;overflow:auto}
@media (min-width:%(a0)dpx) and (max-width:1499px){
  .sdnav{display:block;left:calc((100vw - %(w0)dpx)/2 - %(off)dpx)}}
@media (min-width:%(a1)dpx) and (max-width:1899px){
  .sdnav{display:block;left:calc((100vw - %(w1)dpx)/2 - %(off)dpx)}}
@media (min-width:%(a2)dpx){
  .sdnav{display:block;left:calc((100vw - %(w2)dpx)/2 - %(off)dpx)}}
/* The nav is FIXED, so it floats over whatever the page happens to be showing:
   a near-black hero band at the top of this page, paper below it. `color:inherit`
   therefore resolved to the body ink and the nav was unreadable against the dark
   half - the text was there, it just could not be seen.
   It gets its own surface instead: a paper panel with a soft edge, so it is
   legible over any background the page scrolls past. */
.sdnav{background:rgba(251,249,243,.92);-webkit-backdrop-filter:blur(9px);
  backdrop-filter:blur(9px);border:1px solid rgba(38,36,30,.1);border-radius:14px;
  padding:13px 14px;box-shadow:0 6px 24px rgba(38,36,30,.1);color:#26241E}
.sdnav p.t{font-family:'IBM Plex Mono',monospace;font-size:9.4px;letter-spacing:.13em;
  text-transform:uppercase;opacity:.55;margin:0 0 8px;color:#26241E}
.sdnav a{display:block;font-size:12.2px;line-height:1.3;padding:7px 0 7px 12px;
  min-height:32px;text-decoration:none;color:#26241E;opacity:.62;
  border-left:2px solid rgba(38,36,30,.16);transition:opacity .12s}
.sdnav a:hover{opacity:.9}
.sdnav a.on{opacity:1;font-weight:600;border-left-color:currentColor}
.sdnav a:focus-visible{outline:2px solid currentColor;outline-offset:2px}
@media print{.sdnav{display:none}}
""" % dict(w0=wrap, w1=W1, w2=W2, nav=NAV, off=NAV + GAP,
           a0=need(wrap), a1=need(W1), a2=need(W2))


JS = """
(function(){
  var nav=document.querySelector('.sdnav'); if(!nav) return;
  var links=[].slice.call(nav.querySelectorAll('a'));
  var secs=links.map(function(a){
    return document.getElementById(a.getAttribute('href').slice(1)); }).filter(Boolean);
  if(!secs.length) return;
  function mark(id){ links.forEach(function(a){
    a.classList.toggle('on', a.getAttribute('href')==='#'+id); }); }
  /* The trigger line sits near the top of the viewport, so the marked entry is
     the section being read - not whichever one is sliding in at the bottom. */
  var io=new IntersectionObserver(function(es){
    es.forEach(function(e){ if(e.isIntersecting) mark(e.target.id); });
  }, {rootMargin:'-10% 0px -78% 0px', threshold:0});
  secs.forEach(function(x){ io.observe(x); });
  mark(secs[0].id);
})();
"""


def slugify(t):
    t = re.sub(r"<[^>]+>", "", t)
    t = re.sub(r"&[a-z]+;", " ", t)
    return re.sub(r"[^a-z0-9]+", "-", t.lower()).strip("-")[:40]


def sections(s):
    """(id, label) for every <section> that carries an h2, adding ids as needed."""
    out, edits = [], []
    for m in re.finditer(r"<section\b([^>]*)>", s):
        attrs, start = m.group(1), m.end()
        end = s.find("<section", start)
        body = s[start:end if end > 0 else start + 12000]
        h2 = re.search(r"<h2[^>]*>(.*?)</h2>", body, re.S)
        if not h2:
            continue
        label = re.sub(r"\s+", " ", re.sub(r"<[^>]+>", "", h2.group(1))).strip()
        idm = re.search(r'id="([^"]+)"', attrs)
        if idm:
            out.append((idm.group(1), label))
        else:
            sid = slugify(label)
            edits.append((m.start(), m.end(), '<section%s id="%s">' % (attrs, sid)))
            out.append((sid, label))
    for a, b, rep in reversed(edits):
        s = s[:a] + rep + s[b:]
    return s, out


def main():
    for slug, cfg in sorted(PAGES.items()):
        path = os.path.join(SITE, slug)
        s = open(path, encoding="utf-8").read()

        s = re.sub(re.escape(OPEN) + r".*?" + re.escape(CLOSE), "", s, flags=re.S)
        s = re.sub(r"\n?<style>" + re.escape(MARK) + r".*?/\* end sd \*/</style>\n?",
                   "", s, flags=re.S)
        s = re.sub(r"\n?<script>" + re.escape(MARK) + r".*?/\* end sd \*/</script>\n?",
                   "", s, flags=re.S)

        s, secs = sections(s)
        assert len(secs) >= 3, "%s: only %d sections with an h2" % (slug, len(secs))
        ids = [i for i, _ in secs]
        assert len(set(ids)) == len(ids), "%s: duplicate section ids %s" % (slug, ids)

        items = "".join(
            '<a href="#%s">%s</a>' % (i, cfg["short"].get(i, lab))
            for i, lab in secs)
        nav = (OPEN + '<nav class="sdnav" aria-label="Sections">'
               '<p class="t">On this page</p>' + items + "</nav>" + CLOSE)

        s = s.replace("</body>", nav + "\n<style>" + MARK + css(cfg["wrap"])
                      + "/* end sd */</style>\n<script>" + MARK + JS
                      + "/* end sd */</script>\n</body>", 1)
        open(path, "w", encoding="utf-8").write(s)
        print("%-44s %d sections" % (slug, len(secs)))

    for slug in PAGES:
        s = open(os.path.join(SITE, slug), encoding="utf-8").read()
        assert s.count('class="sdnav"') == 1, slug
        assert s.count("<h1") == 1, slug


if __name__ == "__main__":
    main()
