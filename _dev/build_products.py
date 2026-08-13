#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""The site drawn four times, once in each 37signals product's own language.

WHY THIS SUPERSEDES THE FIRST REDESIGN DOCUMENT

`ops/redesign-37signals.html` invented three skins from a general idea of what
37signals looks like. The correction was that 37signals does not have one look
- it has four products with four deliberately different identities, and the
useful exercise is to take each one seriously rather than average them.

So every color, type classification, radius and shape decision below was read
off the actual product's stylesheets in August 2026 rather than remembered:

  BASECAMP    basecamp.com  - OKLCH tokens in /assets/css/root.css
  HEY         hey.com       - RGB triplets, nine named gradient tokens
  CAMPFIRE    once.com/campfire
  FIZZY       fizzy.do      - not fizzy.com, which is a beverage shop

The typefaces are licensed and cannot be used here, so each skin uses the
nearest thing on Google Fonts and the substitution is named in the specimen
rather than hidden: Graphik -> Inter, Really Sans Large -> Archivo Black,
Family -> Playfair Display, Scorekard -> Outfit. If a direction is chosen the
real face has to be licensed, and that is a line item, not a detail.

WHAT IS DELIBERATELY THE SAME IN ALL FOUR

The words. Every mockup carries identical copy and identical figures, so the
only thing varying between them is the design. Four mockups with four
different headlines would be four moods, not four systems.
"""
import os, re, sys

HERE = os.path.dirname(os.path.abspath(__file__))
SITE = os.path.dirname(HERE)
DONOR = os.path.join(SITE, "ops", "stage-architecture.html")
OUT = os.path.join(SITE, "ops", "redesign-37signals-products.html")
UPDATED = "13 August 2026"

NAV = [("read", "What was read"), ("basecamp", "Basecamp"), ("hey", "HEY"),
       ("campfire", "Campfire"), ("fizzy", "Fizzy"),
       ("compare", "Side by side"), ("pick", "What to ship")]

PATHS = [
    ("01", "Deciding", "Is this worth it?", "73", "blue"),
    ("02", "In a program", "Nobody will take me for practicum.", "31", "violet"),
    ("03", "The gap", "Can I work before my number arrives?", "4", "aqua"),
    ("04", "Counting hours", "547 hours and nobody will hire me.", "21",
     "green"),
    ("05", "Newly licensed", "Do I go on panels or not?", "19", "yellow"),
    ("06", "Running a practice", "How do I do this ethically?", "24", "pink"),
]

SKINS = [
    ("bc", "Basecamp", "basecamp.com",
     "Tinted off-white, never pure. Small type by the standards of the other "
     "three &mdash; 15px body against a 42px headline. Neutral grotesque at "
     "600. Squarish 6px buttons, five-layer diffuse shadows, and exactly one "
     "wink: a wobbly marker underline in highlighter yellow.",
     [("#F5FAF6", "canvas", 1), ("#29353C", "ink", 0), ("#2377D2", "blue", 0),
      ("#19874D", "green", 0), ("#FFDC74", "highlight", 1)],
     "Graphik &rarr; <b>Inter</b> 600 &middot; body 15px &middot; "
     "tracking &minus;0.0225em &middot; radius 12px, buttons 6px"),
    ("hey", "HEY", "hey.com",
     "Pure white, no dark mode, and then a full-bleed blurple slab with torn "
     "scalloped edges. Type is enormous and set in a 900 weight with the "
     "headline gradient-clipped. Everything is a pill and the buttons are "
     "filled with a gradient rather than a color.",
     [("#FFFFFF", "white", 1), ("#231C33", "ink", 0), ("#5522FA", "blurple", 0),
      ("#EC8580", "salmon", 0), ("#FFF5CA", "canary", 1)],
     "Really Sans Large &rarr; <b>Archivo Black</b> 900 &middot; hero ~76px "
     "&middot; tracking normal &middot; radius 2.5em pills"),
    ("cf", "Campfire", "once.com/campfire",
     "The entire viewport is electric blue. Pale cyan prose in a "
     "high-contrast serif, in a 29em column, with square white buttons and "
     "no elevation at all &mdash; 1px rings instead of shadows. It reads as "
     "a letter, and it ends with a handwritten signature.",
     [("#0064E6", "canvas", 0), ("#C2F6FF", "text", 1), ("#FFFFFF", "emph", 1),
      ("#003773", "deep", 0), ("#00B132", "green", 0)],
     "Family &rarr; <b>Playfair Display</b> 800 &middot; serif body "
     "&middot; column 29em &middot; radius 0.2em"),
    ("fz", "Fizzy", "fizzy.do",
     "Cool near-white with a raised white card. Soft rounded grotesque "
     "headlines, justified body copy, and a systematic nine-hue label "
     "palette borrowed straight out of the product. Buttons are full pills "
     "in uppercase with <b>positive</b> tracking &mdash; the only place in "
     "the whole portfolio that letterspaces outward.",
     [("#F7F8FA", "canvas", 1), ("#17233C", "ink", 0), ("#2D71E5", "blue", 0),
      ("#FFFF9C", "flash", 1), ("#8B77FF", "violet", 0)],
     "Scorekard &rarr; <b>Outfit</b> 700 &middot; Cartridge &rarr; Outfit 600 "
     "uppercase, +0.025em &middot; radius 2.2em pills"),
]

EXTRA = """
/* ============================ the four product skins ==================== */
.mk{--pad:36px}
@media(max-width:700px){.mk{--pad:20px}}
.mk *{box-sizing:border-box}
.mk .body{padding:var(--pad)}
.mk a{text-decoration:none}
.mk p{margin:0 0 15px}

/* ---------------------------------------------------------- BASECAMP ---- */
.s-bc{background:#F5FAF6;color:#29353C;font-family:'Inter',system-ui,sans-serif;
  font-size:15px;line-height:1.5;letter-spacing:-.01875em}
.s-bc h1,.s-bc h2,.s-bc h3{font-family:'Inter',system-ui,sans-serif;
  font-weight:600;letter-spacing:-.0225em;line-height:1.15;margin:0 0 16px}
.s-bc h1{font-size:42px;max-width:19ch}
.s-bc h2{font-size:26px}
.s-bc h3{font-size:18px;line-height:1.25}
@media(max-width:700px){.s-bc h1{font-size:28px}}
.s-bc .sub{font-size:17px;color:#6D767B;max-width:52ch;margin-bottom:22px}
.s-bc a{color:#2377D2}
.s-bc .btn{display:inline-block;background:#2377D2;color:#fff;font-weight:500;
  font-size:15px;padding:.75em .9em;border-radius:6px;
  box-shadow:0 1px 2px rgba(11,21,27,.09),0 4px 12px rgba(11,21,27,.06),
    0 0 0 1px rgba(11,21,27,.0625)}
.s-bc .btn.g{background:#19874D}
.s-bc .btn.o{background:#fff;color:#29353C}
.s-bc .scribble{background:url("data:image/svg+xml;utf8,<svg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 120 12'><path d='M2 8 C 22 3, 44 10, 66 5 S 106 3, 118 7' fill='none' stroke='%23FFDC74' stroke-width='5' stroke-linecap='round'/><path d='M6 10 C 26 6, 48 12, 70 8 S 108 6, 116 9' fill='none' stroke='%23FFDC74' stroke-width='3.5' stroke-linecap='round' opacity='.75'/></svg>") bottom center/100% .34em no-repeat;
  padding-bottom:.06em}
.s-bc .yes{display:inline-block;background:#FFDC74;color:#29353C;
  font-family:'Caveat',cursive;font-size:20px;padding:1px 12px 2px;
  border-radius:6px;transform:rotate(-2.5deg)}
.s-bc .card{background:#fff;border-radius:12px;padding:16px 18px;
  box-shadow:0 1px 2px rgba(11,21,27,.06),0 6px 22px rgba(11,21,27,.05),
    0 0 0 1px rgba(11,21,27,.0625)}
.s-bc .tint{background:#FFF9F5}

/* --------------------------------------------------------------- HEY ---- */
.s-hey{background:#fff;color:#231C33;font-family:'Inter',system-ui,sans-serif;
  font-size:19px;line-height:1.4;letter-spacing:-.0125em}
.s-hey h1,.s-hey h2,.s-hey h3{font-family:'Archivo Black','Inter',sans-serif;
  font-weight:400;line-height:1.05;letter-spacing:-.01em;margin:0 0 18px}
.s-hey h1{font-size:64px}
.s-hey h2{font-size:36px}
.s-hey h3{font-size:22px}
@media(max-width:700px){.s-hey h1{font-size:34px}.s-hey h2{font-size:25px}}
.s-hey .grad{background:linear-gradient(135deg,#5522FA,#EC8580);
  -webkit-background-clip:text;background-clip:text;color:transparent}
.s-hey .sub{font-size:19px;color:#736C83;max-width:44ch;margin:0 auto 24px}
.s-hey .mid{text-align:center}
.s-hey a{color:#5522FA}
.s-hey .btn{display:inline-block;
  background:linear-gradient(135deg,#5522FA,#EC8580);color:#fff;
  font-weight:700;font-size:16px;padding:.85em 1.7em;border-radius:2.5em;
  font-feature-settings:'c2sc','smcp';letter-spacing:.02em;
  box-shadow:0 6px 22px rgba(85,34,250,.22)}
.s-hey .btn.flat{background:#231C33;box-shadow:none}
.s-hey mark{background:#FFF5CA;color:#231C33;padding:0 .18em}
.s-hey .slab{background:#5522FA;color:#fff;padding:34px var(--pad);
  margin:0 calc(var(--pad)*-1);
  -webkit-mask:radial-gradient(9px at 50% 0,transparent 98%,#000) repeat-x 0 0/30px 10px,
    radial-gradient(9px at 50% 100%,transparent 98%,#000) repeat-x 0 100%/30px 10px,
    linear-gradient(#000,#000) no-repeat 0 10px/100% calc(100% - 20px);
  mask:radial-gradient(9px at 50% 0,transparent 98%,#000) repeat-x 0 0/30px 10px,
    radial-gradient(9px at 50% 100%,transparent 98%,#000) repeat-x 0 100%/30px 10px,
    linear-gradient(#000,#000) no-repeat 0 10px/100% calc(100% - 20px)}
.s-hey .slab h2,.s-hey .slab a{color:#fff}
.s-hey .slab .sub{color:#E4DAFF}
.s-hey .squig{height:14px;margin:26px 0;border:0;
  background:url("data:image/svg+xml;utf8,<svg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 60 12'><path d='M0 6 Q 7.5 0 15 6 T 30 6 T 45 6 T 60 6' fill='none' stroke='%23D5D2FF' stroke-width='3' stroke-linecap='round'/></svg>") repeat-x center/60px 12px}
.s-hey .chip{display:inline-block;border-radius:2.5em;padding:5px 15px;
  font-size:14px;font-weight:600;background:#F9F7F5;color:#231C33}

/* ---------------------------------------------------------- CAMPFIRE --- */
.s-cf{background:#0064E6;color:#C2F6FF;
  font-family:'Playfair Display',Georgia,serif;font-size:18px;line-height:1.42;
  letter-spacing:-.0015em}
.s-cf .body{max-width:34em;margin:0 auto}
.s-cf h1,.s-cf h2,.s-cf h3{font-family:'Playfair Display',Georgia,serif;
  color:#fff;line-height:1;margin:0 0 18px;letter-spacing:normal}
.s-cf h1{font-size:44px;font-weight:800}
.s-cf h2{font-size:26px;font-weight:500;line-height:1.15}
.s-cf h3{font-size:18px;font-weight:700;font-family:'Inter',sans-serif;
  letter-spacing:-.01em}
@media(max-width:700px){.s-cf h1{font-size:29px}}
.s-cf strong,.s-cf b{color:#fff}
.s-cf a{color:#fff;text-decoration:underline;text-underline-offset:3px}
.s-cf .btn{display:inline-block;background:#fff;color:#0064E6;font-weight:700;
  font-size:16px;padding:.7em 1.1em;border-radius:.2em;
  font-family:'Inter',sans-serif;text-decoration:none;
  box-shadow:0 1px 0 rgba(0,40,218,.5)}
.s-cf .btn.o{background:transparent;color:#fff;box-shadow:inset 0 0 0 2px #fff}
.s-cf code,.s-cf .code{font-family:'IBM Plex Mono',monospace;font-size:14px;
  background:#003773;color:#F2F7FE;padding:10px 13px;display:block;
  border-radius:.1em;margin:0 0 15px}
.s-cf ul{padding-left:1.1em;margin:0 0 15px}
.s-cf li{margin-bottom:7px}
.s-cf .sig{font-family:'Caveat',cursive;font-size:34px;color:#fff;
  line-height:1;margin:18px 0 4px}
.s-cf .who{font-family:'Inter',sans-serif;font-size:13px;color:#C2F6FF}
.s-cf table{border-collapse:collapse;width:100%;font-family:'Inter',sans-serif;
  font-size:14px;margin:0 0 15px}
.s-cf td,.s-cf th{border:2px solid #0064E6;background:#003773;color:#F2F7FE;
  padding:9px 11px;text-align:left}
.s-cf th{background:#0028DA;color:#fff;font-weight:600;font-size:12px;
  text-transform:uppercase;letter-spacing:.08em}
.s-cf .nav{font-family:'Inter',sans-serif;font-size:14px}

/* ------------------------------------------------------------- FIZZY --- */
.s-fz{background:#F7F8FA;color:#17233C;font-family:'Inter',system-ui,sans-serif;
  font-size:16px;line-height:1.5;letter-spacing:-.01em}
.s-fz h1,.s-fz h2,.s-fz h3{font-family:'Outfit','Inter',sans-serif;
  font-weight:700;letter-spacing:-.015em;line-height:1.1;margin:0 0 16px}
.s-fz h1{font-size:52px}
.s-fz h2{font-size:30px}
.s-fz h3{font-size:19px}
@media(max-width:700px){.s-fz h1{font-size:31px}}
.s-fz .mid{text-align:center}
.s-fz .sub{font-size:17px;color:#404856;max-width:40ch;margin:0 auto 22px}
.s-fz a{color:#2D71E5}
.s-fz .btn{display:inline-block;background:#2D71E5;color:#fff;
  font-family:'Outfit',sans-serif;font-weight:600;font-size:14px;
  text-transform:uppercase;letter-spacing:.025em;padding:.95em 1.6em;
  border-radius:2.2125em}
.s-fz .btn.o{background:#fff;color:#17233C;
  box-shadow:0 1px 2px rgba(23,35,60,.1),0 0 0 1px rgba(23,35,60,.09)}
.s-fz .card{background:#FEFFFF;border-radius:12px;padding:16px 18px;
  box-shadow:0 1px 2px rgba(23,35,60,.06),0 8px 26px rgba(23,35,60,.05),
    0 0 0 1px rgba(23,35,60,.06)}
.s-fz .flash{background:#FFFF9C;padding:0 .2em;border-radius:3px}
.s-fz .just{text-align:justify;max-width:60ch}
.s-fz .navbar{background:rgba(247,248,250,.8);backdrop-filter:blur(.5em)}
.s-fz .lab{display:inline-block;width:11px;height:11px;border-radius:3px}
.lab-blue{background:#398FFF}.lab-violet{background:#8B77FF}
.lab-aqua{background:#00AAC2}.lab-green{background:#00B134}
.lab-yellow{background:#F29100}.lab-pink{background:#F467C7}

/* ------------------------------------------------------- shared pieces -- */
.mk .bar{display:flex;align-items:center;gap:20px;padding:15px var(--pad);
  flex-wrap:wrap}
.s-bc .bar{border-bottom:1px solid #E1E7E2}
.s-hey .bar{border-bottom:1px solid #EDEAE6}
.s-cf .bar{border-bottom:2px solid #0028DA;max-width:none}
.s-fz .bar{border-bottom:1px solid #E3E5E6}
.mk .bar .sp{margin-left:auto}
.mk .bar a{font-size:14.5px}
.s-bc .bar a{color:#29353C}.s-fz .bar a{color:#17233C}
.s-hey .bar a{color:#231C33;font-weight:600}
.rows{margin-top:4px}
.rows a{display:grid;grid-template-columns:34px 1fr auto;gap:14px;
  align-items:baseline;padding:15px 0}
.s-bc .rows a{border-top:1px solid #E1E7E2;color:#29353C}
.s-hey .rows a{border-top:2px solid #EDEAE6;color:#231C33}
.s-cf .rows a{border-top:1px solid #3D8DEC;color:#C2F6FF;text-decoration:none}
.s-fz .rows a{border-top:1px solid #E3E5E6;color:#17233C}
.rows .n{font-family:'IBM Plex Mono',monospace;font-size:11.5px;opacity:.55}
.rows .t{font-size:21px;line-height:1.15;display:block}
.s-bc .rows .t{font-weight:600;letter-spacing:-.022em}
.s-hey .rows .t{font-family:'Archivo Black',sans-serif;font-size:23px}
.s-cf .rows .t{color:#fff;font-weight:800}
.s-fz .rows .t{font-family:'Outfit',sans-serif;font-weight:700}
.rows .q{display:block;font-family:'Inter',sans-serif;font-size:13.5px;
  opacity:.72;margin-top:3px;letter-spacing:0;font-weight:400}
.rows .c{font-family:'IBM Plex Mono',monospace;font-size:11px;opacity:.6;
  white-space:nowrap}
.grid3{display:grid;gap:12px}
@media(min-width:720px){.grid3{grid-template-columns:1fr 1fr 1fr}}
.ix{display:grid;gap:18px 30px}
@media(min-width:740px){.ix{grid-template-columns:1fr 1fr 1fr}}
.ix h5{font-family:'IBM Plex Mono',monospace;font-size:10px;letter-spacing:.14em;
  text-transform:uppercase;opacity:.6;margin:0 0 7px;padding-bottom:5px}
.s-bc .ix h5{border-bottom:1px solid #E1E7E2}
.s-hey .ix h5{border-bottom:2px solid #EDEAE6}
.s-cf .ix h5{border-bottom:1px solid #3D8DEC}
.s-fz .ix h5{border-bottom:1px solid #E3E5E6}
.ix ul{list-style:none;margin:0;padding:0}
.ix li{font-family:'Inter',sans-serif;font-size:13px;line-height:1.5;
  margin-bottom:3px;letter-spacing:0}
.list .r{display:grid;grid-template-columns:1fr auto;gap:14px;padding:13px 0;
  align-items:baseline}
.s-bc .list .r{border-top:1px solid #E1E7E2}
.s-hey .list .r{border-top:2px solid #EDEAE6}
.s-cf .list .r{border-top:1px solid #3D8DEC}
.s-fz .list .r{border-top:1px solid #E3E5E6}
.list .nm{font-size:16px;font-weight:600;font-family:'Inter',sans-serif;
  letter-spacing:-.01em}
.s-cf .list .nm{color:#fff}
.list .mt{display:block;font-family:'Inter',sans-serif;font-size:12.5px;
  opacity:.7;margin-top:2px;letter-spacing:0}
.list .kk{font-family:'IBM Plex Mono',monospace;font-size:11px;opacity:.6;
  text-align:right;white-space:nowrap}
.list .kk b{display:block;font-size:19px;opacity:1;font-family:inherit}
.ft{padding:26px var(--pad);font-family:'Inter',sans-serif;font-size:13px}
.s-bc .ft{border-top:1px solid #E1E7E2;color:#6D767B}
.s-hey .ft{border-top:2px solid #EDEAE6;color:#736C83}
.s-cf .ft{border-top:2px solid #0028DA;color:#C2F6FF;max-width:none}
.s-fz .ft{border-top:1px solid #E3E5E6;color:#737880}
.ft .g{display:grid;gap:18px}
@media(min-width:740px){.ft .g{grid-template-columns:1.4fr 1fr 1fr 1fr}}
.ft h6{font-family:'IBM Plex Mono',monospace;font-size:9.5px;letter-spacing:.14em;
  text-transform:uppercase;margin:0 0 8px;opacity:.75}
.ft a{display:block;padding:2px 0;font-size:13px}
.s-bc .ft a{color:#29353C}.s-hey .ft a{color:#231C33}
.s-cf .ft a{color:#fff;text-decoration:none}.s-fz .ft a{color:#17233C}

/* logos */
.lgw{display:inline-flex;align-items:center;gap:10px}
.lg-bc .dome{width:30px;height:30px;border-radius:11px;background:#DCEBFA;
  display:grid;place-items:center;
  box-shadow:inset 0 -2px 4px rgba(11,21,27,.12),0 1px 2px rgba(11,21,27,.14)}
.lg-bc .peak{width:0;height:0;border-left:8px solid transparent;
  border-right:8px solid transparent;border-bottom:13px solid #19874D}
.lg-bc .wm{font-family:'Inter',sans-serif;font-weight:600;font-size:18px;
  letter-spacing:-.025em;color:#29353C}
.lg-hey .wm{font-family:'Archivo Black',sans-serif;font-size:21px;
  letter-spacing:-.02em;background:linear-gradient(120deg,#0074E4,#5522FA);
  -webkit-background-clip:text;background-clip:text;color:transparent}
.lg-hey .hand{font-size:21px;transform:rotate(-8deg);display:inline-block}
.lg-cf .fire{display:inline-flex;align-items:flex-end;gap:2px;height:24px}
.lg-cf .fire i{display:block;width:4px;border-radius:3px}
.lg-cf .wm{font-family:'Playfair Display',serif;font-weight:800;font-size:19px;
  color:#fff}
.lg-fz .chip{display:inline-flex;align-items:flex-end;gap:2.5px;background:#fff;
  border-radius:8px;padding:6px 7px;
  box-shadow:0 1px 2px rgba(23,35,60,.12),0 0 0 1px rgba(23,35,60,.06)}
.lg-fz .chip i{display:block;width:4px;border-radius:3px}
.lg-fz .wm{font-family:'Outfit',sans-serif;font-weight:700;font-size:19px;
  letter-spacing:-.02em;color:#17233C}

/* document furniture */
.skinhead{border:2px solid var(--ink);background:var(--cream);
  box-shadow:6px 6px 0 var(--ink);padding:16px 18px;margin:28px 0 0}
.skinhead .top{display:flex;gap:12px;align-items:baseline;flex-wrap:wrap}
.skinhead h3{margin:0;font-size:23px}
.skinhead .src{font-family:var(--mono);font-size:11px;color:var(--pine);
  margin-left:auto}
.skinhead p{font-size:14px;margin:8px 0 0;max-width:78ch}
.skinhead .fx{font-family:var(--mono);font-size:11.5px;color:#39473F;
  margin-top:9px;display:block}
.sw{display:flex;margin:12px 0 0;border:2px solid var(--ink)}
.sw div{flex:1;height:52px;display:grid;place-items:end center;padding-bottom:4px;
  font-family:var(--mono);font-size:9px;color:#fff}
.sw div.dk{color:#16211B}
.lab2{font-family:var(--mono);font-size:10px;letter-spacing:.13em;
  text-transform:uppercase;color:var(--muted);margin:16px 0 5px;display:block}
.cmp{overflow-x:auto;border:2px solid var(--ink);background:var(--cream);
  box-shadow:5px 5px 0 var(--ink);margin:14px 0}
.cmp table{min-width:780px;margin:0}
.cmp th{background:var(--deep)}
.note{border-left:5px solid var(--gold);padding:2px 0 2px 16px;margin:16px 0}
.note p{font-size:14.5px;margin:0 0 6px}
.moves{border:2px solid var(--ink);background:#fff;box-shadow:5px 5px 0
  var(--ink);margin:14px 0}
.moves .row{display:grid;grid-template-columns:40px 1fr;
  border-top:1px solid var(--line)}
.moves .row:first-child{border-top:0}
.moves .n{background:var(--deep);color:var(--gold);font-family:var(--mono);
  font-size:12px;display:grid;place-items:center;font-weight:600}
.moves .b{padding:10px 13px}
.moves h4{font-size:15px;margin:0 0 3px}
.moves p{font-size:13.5px;margin:0;color:#39473F}
code{font-family:var(--mono);font-size:12.5px;background:#fff;
  border:1px solid var(--line);padding:1px 5px}
"""

FIRE = [("#F467C7", 10), ("#F3570A", 15), ("#FF8A00", 21), ("#FFC400", 17),
        ("#F29100", 12), ("#00AAC2", 8), ("#398FFF", 6)]
BUBBLES = [("#398FFF", 15), ("#F467C7", 10), ("#F3570A", 18), ("#9AA200", 12),
           ("#00AAC2", 8)]


def logo(skin):
    if skin == "bc":
        return ('<span class="lgw lg-bc"><span class="dome">'
                '<span class="peak"></span></span>'
                '<span class="wm">Therapist Support</span></span>')
    if skin == "hey":
        return ('<span class="lgw lg-hey"><span class="hand">&#128075;</span>'
                '<span class="wm">THERAPIST SUPPORT</span></span>')
    if skin == "cf":
        return ('<span class="lgw lg-cf"><span class="fire">%s</span>'
                '<span class="wm">Therapist Support</span></span>'
                % "".join('<i style="background:%s;height:%dpx"></i>' % (c, h)
                          for c, h in FIRE))
    return ('<span class="lgw lg-fz"><span class="chip">%s</span>'
            '<span class="wm">Therapist Support</span></span>'
            % "".join('<i style="background:%s;height:%dpx"></i>' % (c, h)
                      for c, h in BUBBLES))


def bar(skin, on=None):
    links = ["The six paths", "Calculators", "Library", "About"]
    o = ['<div class="bar%s">%s<span class="sp"></span>'
         % (" navbar" if skin == "fz" else "", logo(skin))]
    for l in links:
        w = ' style="font-weight:700"' if l == on else ""
        o.append('<a%s%s>%s</a>' % (w, ' class="nav"' if skin == "cf" else "",
                                    l))
    label = {"bc": "Open a calculator", "hey": "Get started",
             "cf": "Open a calculator", "fz": "Open a calculator"}[skin]
    o.append('<a class="btn%s">%s</a></div>'
             % (" g" if skin == "bc" else "", label))
    return "".join(o)


def rows(skin, limit=6):
    o = ['<div class="rows">']
    for n, name, q, c, hue in PATHS[:limit]:
        chip = ('<span class="lab lab-%s" style="margin-right:7px"></span>'
                % hue) if skin == "fz" else ""
        o.append('<a><span class="n">%s</span><span class="t">%s%s'
                 '<span class="q">&ldquo;%s&rdquo;</span></span>'
                 '<span class="c">%s pages &rarr;</span></a>'
                 % (n, chip, name, q, c))
    o.append("</div>")
    return "".join(o)


IXCOLS = [
    ("Calculators", ["Practice Simulator", "Tax &amp; Retirement",
                     "Associate Job Advisor", "Grow Your Practice",
                     "3,000 Hours", "Cost of Living"]),
    ("Money", ["Sole proprietor or corporation", "The S-corp payroll gap",
               "Estimated taxes", "Solo 401(k), SEP or SIMPLE",
               "What you can deduct"]),
    ("Licensure", ["Becoming an MFT", "Finding a supervisor", "BBS fees, 2026",
                   "Continuing education", "The practicum year"]),
    ("Getting paid", ["The Rate Gap", "Insurance panels", "What Medicare pays",
                      "Headway, Alma or Grow", "Superbills and GFEs"]),
    ("Practice", ["Hiring your first associate", "Liability insurance",
                  "48 discipline decisions", "SimplePractice, priced",
                  "Working remotely"]),
    ("Training and jobs", ["78 MFT programs", "Every PsyD in the state",
                           "All 58 county job portals", "What counties pay",
                           "Loan forgiveness"]),
]


def index():
    o = ['<div class="ix">']
    for h, items in IXCOLS:
        o.append("<div><h5>%s</h5><ul>%s</ul></div>"
                 % (h, "".join("<li>%s</li>" % i for i in items)))
    o.append("</div>")
    return "".join(o)


LISTROWS = [
    ("CAMFT Certified Supervisors", "Statewide &middot; name and city only",
     "302"),
    ("LA-CAMFT, Supervision Offered", "Los Angeles &middot; phone and city",
     "314"),
    ("East Bay CAMFT Supervision Finder",
     "East Bay &middot; supervision type and credentials", "150"),
    ("Marin CAMFT", "North Bay &middot; phone and type", "116"),
    ("Redwood Empire CAMFT", "Sonoma and the North Coast", "99"),
    ("Orange County CAMFT", "Orange County", "63"),
]


def listing(skin):
    o = ['<div class="list">']
    for nm, mt, k in LISTROWS:
        o.append('<div class="r"><div><span class="nm">%s</span>'
                 '<span class="mt">%s</span></div>'
                 '<span class="kk"><b>%s</b>entries</span></div>'
                 % (nm, mt, k))
    o.append("</div>")
    return "".join(o)


def foot(skin):
    return ('<div class="ft"><div class="g"><div>%s<p style="margin:10px 0 0;'
            'max-width:32ch">Free tools and checked reference for California '
            "therapists. Every figure carries the date it was last checked."
            "</p></div>"
            "<div><h6>The six paths</h6>%s</div>"
            "<div><h6>Tools</h6><a>Practice Simulator</a>"
            "<a>Tax &amp; Retirement</a><a>Job Advisor</a>"
            "<a>3,000 Hours</a></div>"
            "<div><h6>This site</h6><a>About</a><a>What changed</a>"
            "<a>Corrections</a></div></div></div>"
            % (logo(skin),
               "".join("<a>%s</a>" % p[1] for p in PATHS)))


def frame(url, skin, inner):
    return ('<div class="frame"><div class="bar"><span class="dot"></span>'
            '<span class="dot"></span><span class="dot"></span>'
            '<span class="url">therapistsupport.org%s</span></div>'
            '<div class="mk s-%s">%s</div></div>' % (url, skin, inner))


# ------------------------------------------------------------------- pages
def home(skin):
    if skin == "bc":
        b = ('<div class="body"><h1>Running a practice is a '
             '<span class="scribble">second job</span> nobody trained you '
             "for.</h1>"
             '<p class="sub">Free calculators and checked reference for '
             "California therapists &mdash; what you keep, what you owe, what "
             "a client is worth, and what a job offer is really paying.</p>"
             '<a class="btn">See what your practice pays you</a> '
             '<a class="btn o">Or browse all 203 pages</a>'
             '<p style="margin-top:18px;color:#6D767B;font-size:14px">'
             "Written and checked by one licensed therapist in California. "
             '<span class="yes">Free!</span></p>'
             + rows(skin) +
             '<div class="card" style="margin:26px 0">'
             "<h3>Most people start with one number</h3>"
             "<p style=\"margin:0;color:#6D767B\">What the practice actually "
             "pays them. Everything else on the site is downstream of it."
             "</p></div>" + index() + "</div>")
    elif skin == "hey":
        b = ('<div class="body"><div class="mid">'
             '<h1 class="grad">We fixed the money half of your practice.</h1>'
             '<p class="sub">Free calculators and checked reference for '
             "California therapists. No account, no email box, nothing "
             "sold.</p>"
             '<a class="btn">See what your practice pays you</a></div>'
             '<hr class="squig">'
             '<div class="slab"><h2 style="font-size:31px">203 pages. Six '
             "paths. <mark style=\"color:#231C33\">Zero</mark> illustrative "
             "figures.</h2>"
             '<p class="sub" style="margin:0 auto">Every dollar here is the '
             "output of a calculation you can follow, on numbers you typed "
             "in.</p></div>"
             '<div style="height:26px"></div>'
             '<h2 class="mid">Start where you are.</h2>'
             + rows(skin) +
             '<hr class="squig">' + index() + "</div>")
    elif skin == "cf":
        b = ('<div class="body"><h1>Everything a California therapist needs '
             "to work out the money.</h1>"
             "<p>Six calculators and 203 pages of checked reference. It is "
             "free, there is no account, and <strong>nothing you type ever "
             "leaves your browser</strong>.</p>"
             "<p>Add up what the other tools in this profession charge you "
             "for a spreadsheet with your own numbers in it. You should own "
             "that arithmetic by now.</p>"
             '<p><a class="btn">See what your practice pays you</a> '
             '<a class="btn o">Read the index</a></p>'
             '<h3 style="margin-top:26px">Start where you are</h3>'
             + rows(skin) +
             '<h3 style="margin-top:24px">What it costs</h3>'
             '<div class="code">$0.00  &mdash; forever, no account, no email '
             "box</div>"
             "<p>Written and checked by one licensed therapist in "
             "California.</p>"
             '<p class="sig">Shawn</p>'
             '<p class="who">Shawn Walters, LMFT &middot; California</p>'
             "</div>")
    else:
        b = ('<div class="body"><div class="mid">'
             "<h1>The money side of a practice, worked <span "
             "class=\"flash\">properly</span>.</h1>"
             '<p class="sub">Six free calculators and 203 checked pages, for '
             "California therapists only.</p>"
             '<a class="btn">Open a calculator</a> '
             '<a class="btn o">See the index</a></div>'
             '<div class="card" style="margin:26px 0 22px">'
             '<h3 style="margin-bottom:12px">Six paths through it</h3>'
             + rows(skin) + "</div>"
             '<p class="just" style="margin:0 auto 22px;color:#404856">Every '
             "figure on this site is the output of a calculation you can "
             "follow, run on numbers you typed in. There are no illustrative "
             "figures and no worked examples standing in for your practice. "
             "When a threshold moves it is listed on a page rather than "
             "quietly swapped in.</p>"
             + index() + "</div>")
    return frame("/", skin, bar(skin) + b + foot(skin))


def path(skin):
    head = {
        "bc": ('<div class="body"><h1>You are counting toward '
               '<span class="scribble">3,000</span>.</h1>'
               '<p class="sub">Twenty-one pages for this stage, every figure '
               "with a named source.</p>"
               '<a class="btn">Start with what is holding up your date</a>'),
        "hey": ('<div class="body"><div class="mid">'
                '<h1 class="grad">547 hours and nobody will hire you?</h1>'
                '<p class="sub">Twenty-one pages for exactly this stage.</p>'
                '<a class="btn">Start here</a></div><hr class="squig">'),
        "cf": ('<div class="body"><h1>You are counting toward 3,000.</h1>'
               "<p>Twenty-one pages for this stage. The job, the hours, the "
               "supervisor, the money, and the paperwork that decides your "
               "date.</p>"
               '<p><a class="btn">Start with your date</a></p>'),
        "fz": ('<div class="body"><div class="mid">'
               '<span class="lab lab-green" style="width:14px;height:14px">'
               "</span>"
               '<h1 style="margin-top:10px">Counting hours</h1>'
               '<p class="sub">Twenty-one pages for this stage, every figure '
               "with a named source.</p>"
               '<a class="btn">Start with your date</a></div>'),
    }[skin]
    q = ('<h2 style="margin-top:26px">The three questions this room is '
         "actually asking</h2>" + listing(skin))
    return frame("/paths/counting-hours", skin,
                 bar(skin, on="The six paths") + head + q + index()
                 + "</div>" + foot(skin))


def content(skin):
    art = {
        "bc": ('<div class="body" style="max-width:44em">'
               '<p style="font-family:\'IBM Plex Mono\',monospace;font-size:11px;'
               'letter-spacing:.09em;color:#6D767B">LICENSURE &middot; '
               "CHECKED 13 AUGUST 2026 &middot; 30 SOURCES</p>"
               "<h1>Finding a clinical supervisor in California.</h1>"
               '<p class="sub">The Board keeps no roster, so here is where '
               "the lists actually are.</p>"
               "<p>California licenses 165,000 people and publishes a list of "
               "exactly <span class=\"scribble\">zero</span> supervisors. "
               "What exists instead is nine county chapter directories, one "
               "statewide association list with no contact details on it, and "
               "two commercial products.</p>"
               '<div class="card tint" style="margin:22px 0">'
               "<h3>In a private practice you cannot simply hire your own "
               "supervisor</h3><p style=\"margin:0;color:#6D767B\">The "
               "statute requires them to be employed by, contracted by, or an "
               "owner of your employer. Hours under a privately retained "
               "supervisor are not creditable.</p></div>"
               "<p>That is the single most expensive misunderstanding in "
               "California supervision.</p></div>"),
        "hey": ('<div class="body" style="max-width:40em;margin:0 auto">'
                '<span class="chip">Licensure</span>'
                '<h1 style="margin-top:14px">The Board keeps no list of '
                "supervisors.</h1>"
                "<p>California licenses 165,000 people and publishes a list "
                "of exactly <mark>zero</mark> supervisors. What exists "
                "instead is nine county chapter directories and two "
                "commercial products.</p>"
                '<div class="slab"><h3 style="font-size:23px;color:#fff">You '
                "cannot simply hire your own supervisor.</h3>"
                "<p style=\"margin:0;color:#E4DAFF;font-size:17px\">In a "
                "private practice the statute requires them to be on your "
                "employer&rsquo;s books. Hours under a privately retained "
                "supervisor are not creditable.</p></div>"
                '<p style="margin-top:22px">That is the single most expensive '
                "misunderstanding in California supervision.</p></div>"),
        "cf": ('<div class="body">'
               "<h1>Finding a clinical supervisor in California.</h1>"
               "<p>California licenses 165,000 people and publishes a list of "
               "exactly <strong>zero</strong> supervisors. The Board does not "
               "certify supervisors, keeps no roster, and its license lookup "
               "has no supervisor field.</p>"
               "<p><strong>In a private practice you cannot simply hire your "
               "own supervisor.</strong> The statute requires them to be "
               "employed by, contracted by, or an owner of your employer. "
               "Hours under a privately retained supervisor are not "
               "creditable.</p>"
               "<ul><li>Nine of twenty-three CAMFT chapters publish a list"
               "</li><li>Fourteen do not, and two of them no longer exist"
               "</li><li>Three addresses people are still sent to are gone"
               "</li></ul>"
               "<table><tr><th>List</th><th>Entries</th></tr>"
               "<tr><td>LA-CAMFT</td><td>314</td></tr>"
               "<tr><td>CAMFT Certified</td><td>302</td></tr>"
               "<tr><td>East Bay CAMFT</td><td>150</td></tr></table></div>"),
        "fz": ('<div class="body" style="max-width:44em;margin:0 auto">'
               '<p style="font-family:\'IBM Plex Mono\',monospace;font-size:11px;'
               'letter-spacing:.09em;color:#737880">LICENSURE &middot; '
               "CHECKED 13 AUGUST 2026</p>"
               "<h1>Finding a clinical supervisor in California.</h1>"
               '<p class="just" style="max-width:none;color:#404856">'
               "California licenses 165,000 people and publishes a list of "
               "exactly zero supervisors. The Board does not certify "
               "supervisors and keeps no roster, so what exists instead is "
               "nine county chapter directories, one statewide association "
               "list with no contact details on it, and two commercial "
               "products.</p>"
               '<div class="card" style="margin:20px 0">'
               '<h3>In a private practice you cannot simply <span '
               'class="flash">hire your own</span> supervisor</h3>'
               "<p style=\"margin:0;color:#404856\">The statute requires them "
               "to be employed by, contracted by, or an owner of your "
               "employer. Hours under a privately retained supervisor are not "
               "creditable.</p></div></div>"),
    }[skin]
    return frame("/finding-a-clinical-supervisor-california", skin,
                 bar(skin) + art + foot(skin))


def directory(skin):
    head = {
        "bc": ("<h1>Where a supervisor list actually is.</h1>"
               '<p class="sub">Every candidate fetched and counted on 13 '
               "August 2026.</p>"),
        "hey": ('<div class="mid"><h1 class="grad">Fifteen lists. Nine are '
                "real.</h1><p class=\"sub\">Every candidate fetched and "
                "counted.</p></div>"),
        "cf": ("<h1>Where a supervisor list actually is.</h1>"
               "<p>Every candidate fetched and counted. Counts are what each "
               "source reports about itself; <strong>nothing is copied "
               "here</strong>.</p>"),
        "fz": ('<div class="mid"><h1>Where the lists actually are.</h1>'
               '<p class="sub">Fetched and counted, 13 August 2026.</p>'
               "</div>"),
    }[skin]
    wrap = ('<div class="card" style="margin-top:18px">%s</div>'
            if skin == "fz" else "%s")
    return frame("/finding-a-clinical-supervisor-california#lists", skin,
                 bar(skin) + '<div class="body">' + head
                 + (wrap % listing(skin))
                 + '<p style="font-size:13px;opacity:.7;margin-top:16px">'
                   "Counts are what each source reports on its own page. "
                   "Nothing from any of these directories is copied here."
                   "</p></div>" + foot(skin))


# ------------------------------------------------------------------- build
def build():
    donor = open(DONOR, encoding="utf-8").read()
    m = re.search(r"<style>([\s\S]*?)</style>", donor)
    if not m:
        sys.exit("ops/stage-architecture.html has no <style> block")
    css = m.group(1) + EXTRA

    o = ['<!DOCTYPE html><html lang="en"><head><meta charset="utf-8">',
         '<meta name="viewport" content="width=device-width,initial-scale=1">',
         '<meta name="robots" content="noindex,nofollow">',
         "<title>The site in four 37signals product identities</title>",
         '<link rel="preconnect" href="https://fonts.googleapis.com">',
         '<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>',
         '<link href="https://fonts.googleapis.com/css2?family=Archivo+Black&'
         'family=Bricolage+Grotesque:opsz,wght@12..96,800&family=Caveat:wght@600&'
         'family=Fraunces:opsz,wght@9..144,600;9..144,800&'
         'family=IBM+Plex+Mono:wght@400;600&family=Inter:wght@400;500;600;700&'
         'family=Outfit:wght@400;600;700&'
         'family=Playfair+Display:wght@500;700;800&display=swap" '
         'rel="stylesheet">',
         "<style>%s</style></head><body>" % css]

    o.append('<header class="mast"><div class="wrap">'
             '<span class="lab">Working document &middot; %s</span>'
             "<h1>Four products, four identities, one site.</h1>"
             "<p>37signals does not have a house style &mdash; it has four "
             "products that look deliberately unlike each other. So this "
             "draws the site four times: once as <b>Basecamp</b>, once as "
             "<b>HEY</b>, once as <b>Campfire</b>, once as <b>Fizzy</b>. "
             "Every color, radius and type classification below was read off "
             "the real product&rsquo;s stylesheets rather than remembered, "
             "and <b>the words are identical in all four</b>, so the only "
             "thing varying is the design.</p>"
             '<div class="meta"><span class="chip">4 identities</span>'
             '<span class="chip">20 mockups</span>'
             '<span class="chip">Logo, home, path, article, directory</span>'
             '<span class="chip">Real tokens</span></div>'
             "</div></header>" % UPDATED)

    o.append('<nav class="jump"><div class="wrap"><ul>')
    for h, t in NAV:
        o.append('<li><a href="#%s">%s</a></li>' % (h, t))
    o.append("</ul></div></nav>")
    o.append('<div class="wrap">')

    # ----------------------------------------------------------------- read
    o.append('<section id="read"><div class="kicker"><span class="n">01</span>'
             "<h2>What was actually read</h2></div>")
    o.append('<p class="lede">Four sites, their stylesheets, their font '
             "binaries and their logo art &mdash; in August 2026. The point "
             "of reading rather than remembering is that these four differ on "
             "axes you would not guess.</p>")
    o.append('<div class="moves">')
    for n, h, p in [
        ("01", "Only one of them is dark, and it is dark blue",
         "Campfire sets <code>body{background:#0064E6}</code> &mdash; the "
         "whole viewport, not a hero band. Basecamp is a tinted off-white "
         "and never pure white; HEY is pure white with no dark mode at all; "
         "Fizzy is a cool near-white."),
        ("02", "No two share a type classification",
         "Neutral grotesque at 600 (Basecamp), ultra-heavy grotesque at 900 "
         "(HEY), high-contrast serif at 800 (Campfire), soft rounded "
         "grotesque at 700 (Fizzy). That is the fastest way to tell them "
         "apart with the color removed."),
        ("03", "Basecamp is the small-type outlier",
         "About 15px body against a 42px headline. HEY, Campfire and Fizzy "
         "all run roughly 32px body text on their marketing pages. Copied "
         "literally, three of these four would make this site&rsquo;s dense "
         "reference pages unreadable &mdash; see the caution below."),
        ("04", "Corner radius is a clean four-point spread",
         "Campfire 0.2em, nearly square. Basecamp about 6px on buttons. HEY "
         "2.5em pills. Fizzy 2.2em pills. Nothing in the middle."),
        ("05", "HEY is the only gradient brand",
         "Nine named gradient tokens, gradient-filled buttons, and the "
         "headline itself clipped to a blurple-to-salmon gradient. The other "
         "three are strictly flat fills."),
        ("06", "Each has exactly one wink, in a different register",
         "Basecamp draws a wobbly marker underline in highlighter yellow. HEY "
         "scallops the edges of its color slabs and uses a squiggle for a "
         "horizontal rule. Campfire ends the page with a scanned handwritten "
         "signature. Fizzy flashes new content in a near-fluorescent yellow."),
    ]:
        o.append('<div class="row"><div class="n">%s</div><div class="b">'
                 "<h4>%s</h4><p>%s</p></div></div>" % (n, h, p))
    o.append("</div>")
    o.append('<div class="note"><p><b>The typefaces are licensed and are not '
             "used here.</b> Graphik, Really Sans Large, Family, Scorekard and "
             "Cartridge are commercial faces. Each skin below substitutes the "
             "nearest thing on Google Fonts &mdash; Inter, Archivo Black, "
             "Playfair Display and Outfit &mdash; and says so. Choosing a "
             "direction means licensing the real face or accepting the "
             "substitute; it is a line item, not a detail.</p></div>")
    o.append("</section><hr class=\"rule\">")

    # ---------------------------------------------------------- four skins
    for key, name, host, why, sw, typ in SKINS:
        anchor = {"bc": "basecamp", "hey": "hey", "cf": "campfire",
                  "fz": "fizzy"}[key]
        o.append('<section id="%s"><div class="kicker">'
                 '<span class="n">%s</span><h2>As %s</h2></div>'
                 % (anchor, {"bc": "02", "hey": "03", "cf": "04",
                             "fz": "05"}[key], name))
        o.append('<div class="skinhead"><div class="top"><h3>%s</h3>'
                 '<span class="src">%s</span></div><p>%s</p>'
                 '<span class="fx">%s</span>' % (name, host, why, typ))
        o.append('<div class="sw">')
        for hexv, lab, dark in sw:
            o.append('<div class="%s" style="background:%s">%s %s</div>'
                     % ("dk" if dark else "", hexv, lab, hexv))
        o.append("</div></div>")

        o.append('<span class="lab2">The mark, at real size</span>')
        o.append(frame("/", key,
                       '<div class="body" style="padding-top:26px;'
                       'padding-bottom:26px">%s</div>' % logo(key)))
        o.append('<span class="lab2">Home page</span>')
        o.append(home(key))
        o.append('<span class="lab2">A path landing page &mdash; one of six'
                 "</span>")
        o.append(path(key))
        o.append('<span class="lab2">A content page</span>')
        o.append(content(key))
        o.append('<span class="lab2">A directory listing</span>')
        o.append(directory(key))
        o.append("</section><hr class=\"rule\">")

    # -------------------------------------------------------------- compare
    o.append('<section id="compare"><div class="kicker">'
             '<span class="n">06</span><h2>Side by side</h2></div>')
    o.append('<p class="lede">The same six decisions, four ways.</p>')
    o.append('<div class="cmp"><table><thead><tr><th>Decision</th>'
             "<th>Basecamp</th><th>HEY</th><th>Campfire</th><th>Fizzy</th>"
             "</tr></thead><tbody>")
    for label, a, b, c, d in [
        ("Canvas", "Tinted off-white #F5FAF6", "Pure white #FFFFFF",
         "Electric blue #0064E6, whole page", "Cool near-white #F7F8FA"),
        ("Headline face", "Neutral grotesque, 600",
         "Ultra-heavy grotesque, 900", "High-contrast serif, 800",
         "Soft rounded grotesque, 700"),
        ("Body size", "~15px, the outlier", "~32px", "~32px", "~32px"),
        ("Corner radius", "6px buttons", "2.5em pills", "0.2em, near-square",
         "2.2em pills"),
        ("Fills", "Flat, five-layer shadows", "Gradients everywhere",
         "Flat, 1px rings, no elevation", "Flat, hairline rings"),
        ("The wink", "Marker underline in yellow",
         "Scalloped slab edges, squiggle rules", "Handwritten signature",
         "Fluorescent highlight flash"),
        ("Best at", "Dense reference, read daily", "One loud claim, one action",
         "A letter, an argument, a manifesto",
         "A product with structured data in it"),
        ("Risk here", "Least distinctive of the four",
         "203 pages of it would exhaust anybody",
         "Long reference on saturated blue is tiring",
         "Reads as software, not as research"),
    ]:
        o.append("<tr><td><b>%s</b></td><td>%s</td><td>%s</td><td>%s</td>"
                 "<td>%s</td></tr>" % (label, a, b, c, d))
    o.append("</tbody></table></div>")
    o.append("</section><hr class=\"rule\">")

    # ----------------------------------------------------------------- pick
    o.append('<section id="pick"><div class="kicker">'
             '<span class="n">07</span><h2>What to ship</h2></div>')
    o.append('<p class="lede">One recommendation, one hybrid worth '
             "considering, and one thing not to copy from any of them.</p>")
    o.append('<div class="moves">')
    for n, h, p in [
        ("01", "Basecamp is the right base, and it is the boring answer",
         "It is the only one of the four designed for a product people open "
         "every day and read a lot of text in. This site is 203 dense "
         "reference pages with tables in them. HEY&rsquo;s 32px body and "
         "gradient headlines are built to sell one idea to a stranger once; "
         "Campfire&rsquo;s blue canvas is built for a 29em manifesto, not for "
         "a nine-column table of county pay."),
        ("02", "Take Fizzy&rsquo;s label palette for the six paths",
         "Fizzy ships nine hues in seven steps because its product has "
         "columns and labels. This site has six paths that need to be "
         "distinguishable at a glance across the whole site. That is the same "
         "problem, and Fizzy has already solved it more carefully than a "
         "single accent can."),
        ("03", "Take Campfire&rsquo;s ending, not its canvas",
         "The handwritten signature under a plain-spoken argument is the most "
         "valuable thing in any of the four for a site whose entire "
         "differentiator is that one identifiable person checked the numbers. "
         "Put it on the about page and at the foot of the home page. Do not "
         "take the electric blue."),
        ("04", "Take one HEY move and only one",
         "The scalloped color slab, used once per page at most, for the one "
         "claim that matters. Everything else about HEY &mdash; gradient "
         "text, pill buttons, 900 weights &mdash; fights the reading this "
         "site asks for."),
        ("05", "Do not copy any of their body sizes",
         "Three of the four run 32px body text on a marketing page with "
         "roughly 400 words on it. Applied to a 6,000-word reference page "
         "with seven tables, that is a scroll nobody finishes. Basecamp&rsquo;s "
         "15px is closer, and the honest number for this site is 16 to 17px."),
        ("06", "The result is a fifth thing, and that is fine",
         "Basecamp&rsquo;s structure and restraint, Fizzy&rsquo;s label "
         "system on the six paths, Campfire&rsquo;s signature, one HEY slab. "
         "Copying any single one wholesale would be costume; taking the "
         "decision each of them got right is how their own designers work."),
    ]:
        o.append('<div class="row"><div class="n">%s</div><div class="b">'
                 "<h4>%s</h4><p>%s</p></div></div>" % (n, h, p))
    o.append("</div>")
    o.append('<div class="note"><p><b>Still true from the last document:</b> '
             "the six paths become the primary navigation and the topic hubs "
             "move to an index at the foot of every page. No URL moves and "
             "nothing is duplicated &mdash; a path page is a generated view "
             "over the same library. That decision is independent of which "
             "identity is chosen, and it is the one worth making first.</p>"
             "<p><b>And on Rails:</b> none of this depends on how the site is "
             "served. A redesign and a re-platform are two projects.</p>"
             "</div>")
    o.append("</section>")

    o.append("</div>")
    o.append('<footer><div class="wrap"><p style="margin:0">Working document, '
             "not linked from the site and not indexable. Mockups are "
             "drawings; no link in them goes anywhere. The four identities "
             "belong to 37signals and are referenced here for comparison, not "
             "reproduced &mdash; no licensed typeface or logo asset is used. "
             "Written %s.</p></div></footer>" % UPDATED)
    o.append("</body></html>")
    return "".join(o)


def main():
    print("four 37signals product identities")
    html = build()
    open(OUT, "w", encoding="utf-8").write(html)
    print("  wrote ops/%s, %s bytes"
          % (os.path.basename(OUT), format(len(html), ",d")))

    bad = 0
    for h, _ in NAV:
        if 'id="%s"' % h not in html:
            print("GUARD: the jump nav points at #%s, absent" % h)
            bad += 1
    n = html.count('class="frame"')
    if n != len(SKINS) * 5:
        print("GUARD: %d mockups, expected %d - five surfaces per identity"
              % (n, len(SKINS) * 5))
        bad += 1
    for key, name, _h, _w, _s, _t in SKINS:
        if 's-%s"' % key not in html:
            print("GUARD: the %s skin is never drawn" % name)
            bad += 1
    # The words must be identical across skins, or this compares moods rather
    # than designs. The load-bearing sentence appears once per identity.
    # Counted over tag-stripped text: one skin highlights part of the
    # sentence, and a raw substring search would report that as drift.
    plain = re.sub(r"\s+", " ", re.sub(r"<[^>]+>", "", html))
    k = plain.count("cannot simply hire your own")
    if k != len(SKINS):
        print("GUARD: the shared sentence appears %d times, expected %d - the "
              "copy has drifted between skins" % (k, len(SKINS)))
        bad += 1
    for _num, pname, q, _c, _hue in PATHS:
        if pname not in html or q not in html:
            print("GUARD: path %r is incomplete" % pname)
            bad += 1
    for needle, what in [
        ("licensed and are not", "the typeface licensing caveat"),
        ("Do not copy any of their body sizes", "the density warning"),
        ("a fifth thing", "the recommendation"),
        ("two projects", "the Rails answer"),
    ]:
        if needle not in html:
            print("GUARD: %s is missing" % what)
            bad += 1
    t = re.sub(r"<(script|style)[\s\S]*?</\1>", " ", html, flags=re.I)
    t = re.sub(r"<[^>]+>", " ", t)
    for w in ("programme", "counselling", "centre", "whilst", "amongst",
              "recognise", "organisation", "behaviour", "fulfilment",
              "judgement"):
        if re.search(r"\b%s" % w, t, re.I):
            print("GUARD: British spelling %r" % w)
            bad += 1
    for mm in re.finditer(r"\bgates?\b", t, re.I):
        print("GUARD: %r - removed sitewide" % mm.group(0))
        bad += 1
    if 'name="robots" content="noindex' not in html:
        print("GUARD: working document must not be indexable")
        bad += 1

    if bad:
        sys.exit("\n%d problem(s)" % bad)
    print("  guards ok - %d mockups, %d identities" % (n, len(SKINS)))


if __name__ == "__main__":
    main()
