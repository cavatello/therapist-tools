#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Hero lab — four fixes for three measured defects.

The measurements that prompted this, taken at real usable heights (browser
chrome subtracted) on the live page:

  every desktop width   the h1 occupies 43% of the column. 644px of dead space
                        to the right of it, on a 1440 screen.
  laptop 1440x780       the three proof figures are cut off at the fold
  laptop 1280x700       they are below it entirely
  phone 375x600         THE CTA IS BELOW THE FOLD. The primary action is not
                        visible without scrolling, which is the worst thing a
                        landing page can do.

So every variant here has to: use the horizontal space, and get the CTA and at
least one proof figure above the fold at 375x600. Colour is the second question,
and it is asked separately from layout so the two do not get confused.
"""
import os, re, base64, json

HERE = os.path.dirname(os.path.abspath(__file__))
import content as C

CH = os.path.join(HERE, "..", "amft")
chrome_css = open(os.path.join(CH, "_chrome_css.txt")).read()
chrome_hdr = re.sub(r'(<a href="[^"]*") class="on"', r"\1",
                    open(os.path.join(CH, "_chrome_hdr.txt")).read())
chrome_js = open(os.path.join(CH, "_chrome_js.txt")).read().split("\n/*---*/\n")[0]
FONTS = os.path.join(HERE, "..", "tree5", "fonts")


def inline_fonts():
    css = open(os.path.join(FONTS, "fonts.css")).read()
    keep = [b for b in re.split(r"(?=/\* )", css) if b.strip().startswith("/* latin */")]
    def sub(m):
        with open(os.path.join(FONTS, "f", m.group(1)), "rb") as f:
            return "url(data:font/woff2;base64," + base64.b64encode(f.read()).decode() + ")"
    return re.sub(r"url\(\./f/([^)]+)\)", sub, "".join(keep))


BASE = """
.hx{--paper:#FBF9F3;--white:#fff;--ink:#26241E;--muted:#6E695E;--line:#E7E2D6;
  --pine:#2C6350;--gold:#B08430;--pop:#F6C560;--pos:#3F9577;
  font-family:Inter,system-ui,sans-serif;-webkit-font-smoothing:antialiased;color:var(--ink)}
.hx *,.hx *::before,.hx *::after{box-sizing:border-box}
.hxw{max-width:1160px;margin:0 auto;padding:0 26px}
@media (max-width:520px){.hxw{padding:0 18px}}
.hx h1{font-family:Fraunces,Georgia,serif;font-weight:700;letter-spacing:-.02em;
  line-height:1.06;margin:0 0 .3em}
.hx p{margin:0 0 1em}
.hxkick{font-family:'IBM Plex Mono',monospace;font-size:10.5px;font-weight:600;
  letter-spacing:.14em;text-transform:uppercase;margin:0 0 14px}
.hxdeck{font-size:clamp(15.5px,1.25vw,18px);line-height:1.55;margin:0 0 22px}
.hxacts{display:flex;gap:10px;flex-wrap:wrap}
.hxcta{display:inline-flex;align-items:center;min-height:48px;padding:0 22px;
  border-radius:999px;font-weight:700;font-size:15.5px;text-decoration:none}
.hxghost{display:inline-flex;align-items:center;min-height:48px;padding:0 20px;
  border-radius:999px;border:1.5px solid;font-weight:600;font-size:15px;
  text-decoration:none;background:transparent}

/* THE LAYOUT FIX: two columns from 900px up, so the 644px of dead space to the
   right of the h1 carries the proof figures instead of nothing - which also
   lifts them above the fold on every laptop. */
.hxgrid{display:grid;grid-template-columns:minmax(0,1.05fr) minmax(300px,.95fr);
  gap:clamp(26px,4vw,60px);align-items:center}
@media (max-width:900px){.hxgrid{grid-template-columns:minmax(0,1fr);gap:24px}}

.hxpanel{border-radius:16px;padding:22px 24px}
.hxpanel .row{display:flex;align-items:baseline;justify-content:space-between;gap:14px;
  padding:11px 0;border-bottom:1px solid rgba(255,255,255,.14)}
.hxpanel .row:last-child{border-bottom:0}
.hxpanel b{font-family:Fraunces,Georgia,serif;font-size:clamp(22px,2.1vw,28px);
  line-height:1;white-space:nowrap}
.hxpanel em{font-style:normal;font-size:12.6px;line-height:1.4;text-align:right}
.hxpanel .lab{font-size:13.4px;font-weight:600}

/* NOT flex. Flex made every <b> a flex item and every bare "&middot;" text node
   an anonymous one, so the separators spaced wrongly and "California only"
   orphaned onto its own line. It is a sentence; let it set as a sentence. */
.hxwho{margin:18px 0 0;font-size:13px;line-height:1.6;max-width:34em}
.hxwho b{font-weight:600}
.hxnote{margin:26px 0 0;padding:10px 14px;border-radius:10px;font-size:12.6px;
  font-family:'IBM Plex Mono',monospace;letter-spacing:.03em}

/* 375x600 is the last failure: stacked, the panel's first row falls below the
   fold. Three changes, all mobile-only - a smaller h1, a tighter rhythm, and
   the panel promoted ABOVE the audience line, because a figure earns more of
   that space than a list of licence types does. */
@media (max-width:560px){
  .hx h1{font-size:26px !important;line-height:1.08;max-width:none}
  .hxdeck{font-size:15px;line-height:1.5;margin-bottom:16px}
  .hxkick{margin-bottom:10px}
  .hxgrid{gap:16px}
  .hxpanel{order:-1;padding:14px 16px}
  /* One figure, not three. A 201px panel on a 375px screen pushed the CTA
     35px past the fold; the strongest number earns that space and the other
     two are a scroll away. */
  /* side-by-side, the label wrapped to two lines and the caption to two more,
     making one row 140px tall on a 375px screen. Stack it: label, figure,
     caption, all left-aligned, and it fits in a third of that. */
  .hxpanel .row{padding:2px 0;display:block;border-bottom:0}
  .hxpanel .row .lab{display:block;margin-bottom:2px}
  .hxpanel .row>span:last-child,.hxpanel em{text-align:left !important}
  .hxpanel .row:nth-child(n+2){display:none}
  .hxpanel b{font-size:20px}
  .hxpanel em{font-size:11.5px}
  .hxwho{margin-top:14px;font-size:12.2px}
  .hxnote{margin-top:16px}
  .hx section{padding-top:22px !important}
}
@media (max-width:560px){
  /* the panel is a grid child, so ordering it needs the grid to own it */
  .hxgrid{display:flex;flex-direction:column}
}
"""

# --- the four ------------------------------------------------------------
VARIANTS = [
 ("v1", "Two-column, deep pine",
  "The layout fix on the site's own primary colour. Pine is already the brand, "
  "already on the masthead, and reads as calm and financial rather than as a "
  "game. Least risk, best contrast, and the panel fills the dead space.",
  """
.v1{background:linear-gradient(158deg,#2C6350 0%,#1F4C3C 62%,#183F31 100%);color:#F4F1E8;
  padding:clamp(34px,4.2vw,62px) 0 clamp(30px,3.6vw,52px)}
.v1 .hxkick{color:#9FC4B4}
.v1 h1{font-size:clamp(29px,3.6vw,46px);color:#FFFDF6;max-width:15ch}
.v1 h1 em{font-style:normal;color:var(--pop)}
.v1 .hxdeck{color:#C9DED5;max-width:44ch}
.v1 .hxcta{background:var(--pop);color:#173B2F}
.v1 .hxghost{border-color:rgba(255,255,255,.34);color:#D7E7E0}
.v1 .hxpanel{background:rgba(0,0,0,.20);border:1px solid rgba(255,255,255,.16)}
.v1 .hxpanel b{color:var(--pop)}
.v1 .hxpanel em,.v1 .hxwho{color:#9FC4B4}
.v1 .hxpanel .lab,.v1 .hxwho b{color:#F4F1E8}
.v1 .hxnote{background:rgba(0,0,0,.22);color:#9FC4B4}
"""),

 ("v2", "Two-column, ink and gold",
  "Near-black with gold. The most serious of the four and the most confident — "
  "it stops looking like a product page and starts looking like a reference. "
  "Gold does the work the purple was trying to do, without the game association.",
  """
.v2{background:#1B1A17;color:#EDE8DC;padding:clamp(34px,4.2vw,62px) 0 clamp(30px,3.6vw,52px);
  position:relative;overflow:hidden}
.v2::after{content:"";position:absolute;inset:auto -10% -60% 40%;height:120%;
  background:radial-gradient(ellipse at center,rgba(176,132,48,.16),transparent 62%)}
.v2 > *{position:relative}
.v2 .hxkick{color:var(--pop)}
.v2 h1{font-size:clamp(29px,3.6vw,46px);color:#FFFDF6;max-width:15ch}
.v2 h1 em{font-style:normal;color:var(--pop)}
.v2 .hxdeck{color:#B8B1A2;max-width:44ch}
.v2 .hxcta{background:var(--pop);color:#1B1A17}
.v2 .hxghost{border-color:rgba(255,255,255,.26);color:#B8B1A2}
.v2 .hxpanel{background:rgba(255,255,255,.045);border:1px solid rgba(255,255,255,.12)}
.v2 .hxpanel b{color:var(--pop)}
.v2 .hxpanel em,.v2 .hxwho{color:#8F887A}
.v2 .hxpanel .lab,.v2 .hxwho b{color:#EDE8DC}
.v2 .hxnote{background:rgba(255,255,255,.05);color:#8F887A}
"""),

 ("v3", "Light hero, coloured panel",
  "Inverts the problem: paper ground, ink type, and the colour concentrated in "
  "the panel on the right. The lightest and the fastest to read, and it matches "
  "the rest of the site instead of announcing itself. The bold hook survives "
  "because the typography carries it rather than the background.",
  """
.v3{background:var(--paper);color:var(--ink);border-bottom:1px solid var(--line);
  padding:clamp(32px,4vw,58px) 0 clamp(28px,3.4vw,48px)}
.v3 .hxkick{color:var(--muted)}
.v3 h1{font-size:clamp(29px,3.7vw,48px);max-width:15ch}
.v3 h1 em{font-style:normal;color:var(--pine);
  background:linear-gradient(transparent 66%,#F6C56066 66%)}
.v3 .hxdeck{color:#4A453B;max-width:44ch}
.v3 .hxcta{background:var(--pine);color:#fff}
.v3 .hxghost{border-color:var(--line);color:var(--muted)}
.v3 .hxpanel{background:#20503F;color:#F4F1E8}
.v3 .hxpanel b{color:var(--pop)}
.v3 .hxpanel em{color:#9FC4B4}
.v3 .hxpanel .lab{color:#F4F1E8}
.v3 .hxwho{color:var(--muted)}
.v3 .hxwho b{color:var(--ink)}
.v3 .hxnote{background:var(--white);border:1px solid var(--line);color:var(--muted)}
"""),

 ("v4", "Two-column, aubergine — the purple, fixed",
  "If the purple stays, this is the version that works: a warmer, deeper "
  "aubergine instead of the flat indigo, with real contrast between the ground "
  "and the panel. The flat #2B2150 read as heavy because nothing on top of it "
  "was darker or lighter by much.",
  """
.v4{background:linear-gradient(155deg,#3B2450 0%,#2A1A3A 60%,#221530 100%);color:#EFE7F5;
  padding:clamp(34px,4.2vw,62px) 0 clamp(30px,3.6vw,52px)}
.v4 .hxkick{color:#E0B7F0}
.v4 h1{font-size:clamp(29px,3.6vw,46px);color:#FFFDF6;max-width:15ch}
.v4 h1 em{font-style:normal;color:var(--pop)}
.v4 .hxdeck{color:#C6B4D4;max-width:44ch}
.v4 .hxcta{background:var(--pop);color:#2A1A3A}
.v4 .hxghost{border-color:rgba(255,255,255,.28);color:#C6B4D4}
.v4 .hxpanel{background:rgba(0,0,0,.26);border:1px solid rgba(255,255,255,.14)}
.v4 .hxpanel b{color:var(--pop)}
.v4 .hxpanel em,.v4 .hxwho{color:#B39EC4}
.v4 .hxpanel .lab,.v4 .hxwho b{color:#EFE7F5}
.v4 .hxnote{background:rgba(0,0,0,.28);color:#B39EC4}
"""),
]

# All three are business-side figures now. The AMFT hours row went: it is a
# licensure milestone, not a business number, and it made the panel read as a
# grab-bag of everything the site does rather than as one argument.
PROOF = [("$138,365", "Take-home", "on a $250,000 practice, after every cost and tax"),
         ("$69,061", "Tax on it", "and how much of that is optional"),
         ("$4,800", "What a client is worth", "your rate \u00d7 how long they stay, not one session")]


def hero(key):
    rows = "".join(
        '<div class="row"><span class="lab">%s</span><span style="text-align:right">'
        '<b>%s</b><em style="display:block">%s</em></span></div>' % (lab, big, sub)
        for big, lab, sub in PROOF)
    return """
<section class="%(k)s"><div class="hxw"><div class="hxgrid">
  <div>
    <p class="hxkick">For California therapists</p>
    <h1>Running a practice is a <em>second job</em> nobody trained you for.</h1>
    <p class="hxdeck">Free tools for the business side of a practice &mdash; what you keep,
      what you owe, and what a client is worth. Your own numbers, nothing saved.</p>
    <div class="hxacts">
      <a class="hxcta" href="practice-simulator.html">Open the simulator &rarr;</a>
      <a class="hxghost" href="tools.html">All seven tools</a>
    </div>
    <p class="hxwho">For <b>LMFTs</b>, <b>LCSWs</b>, <b>LPCCs</b>, <b>psychologists</b>
      and <b>registered associates</b> &mdash; California only.</p>
  </div>
  <div class="hxpanel">%(rows)s</div>
</div>
<p class="hxnote">Nothing saved &middot; no account &middot; 2026 federal and California rates</p>
</div></section>""" % {"k": key, "rows": rows}


SHELL = """<!doctype html>
<html lang="en"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<meta name="robots" content="noindex, nofollow">
<title>Hero %(n)s — %(name)s</title>
<style>%(fonts)s</style><style>%(chrome_css)s</style>
<style>%(sw)s%(base)s%(css)s</style>
</head><body>
%(switch)s
<div class="hxwhy"><b>%(name)s.</b> %(why)s</div>
%(hdr)s
<main class="hx">%(hero)s
<div class="hxfold"><span>the fold, at 1440&times;780</span></div>
<div style="height:520px;background:#fff"></div>
</main>
<script>%(js)s</script></body></html>"""

SW = """
.hxsw{position:sticky;top:0;z-index:60;display:flex;gap:8px;flex-wrap:wrap;align-items:center;
  background:#26241E;color:#CFC7B3;padding:8px 16px;font-family:'IBM Plex Mono',monospace;
  font-size:11px;letter-spacing:.07em;text-transform:uppercase}
.hxsw a{color:#CFC7B3;text-decoration:none;border:1px solid #4A463C;border-radius:999px;
  padding:6px 11px;min-height:32px;display:inline-flex;align-items:center}
.hxsw a.on{background:#B08430;border-color:#B08430;color:#17181A;font-weight:600}
.hxwhy{background:#F4F0E4;border-bottom:1px solid #E7E2D6;padding:11px 16px;font-size:13.4px;
  line-height:1.55;color:#4A453B}
.hxwhy b{font-family:Fraunces,Georgia,serif}
.hxfold{border-top:2px dashed #B5483F;position:relative;height:0}
.hxfold span{position:absolute;right:10px;top:-9px;background:#B5483F;color:#fff;
  font-family:'IBM Plex Mono',monospace;font-size:9.5px;letter-spacing:.1em;
  text-transform:uppercase;padding:2px 8px;border-radius:4px}
"""


def main():
    fonts = inline_fonts()
    for i, (k, name, why, css) in enumerate(VARIANTS):
        sw = ('<div class="hxsw"><span style="opacity:.6">Hero</span>'
              + "".join('<a href="hero-%s.html"%s>%s &middot; %s</a>'
                        % (x, ' class="on"' if x == k else "", x.upper(), n2.split(",")[0])
                        for x, n2, _, _ in VARIANTS) + "</div>")
        html = SHELL % dict(n=k.upper(), name=name, why=why, fonts=fonts,
                            chrome_css=chrome_css, sw=SW, base=BASE, css=css,
                            switch=sw, hdr=chrome_hdr, hero=hero(k), js=chrome_js)
        open(os.path.join(HERE, "hero-%s.html" % k), "w", encoding="utf-8").write(html)
        print("wrote hero-%s.html  %d kB  (%s)" % (k, len(html) // 1024, name))


if __name__ == "__main__":
    main()
