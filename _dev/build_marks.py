#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Ten marks for Therapist Support, all built on the same idea: bearing weight.

THE BRIEF

The word in the name is Support, and the meaning wanted is not the customer
service sense - it is the structural one. Something underneath, holding. A
plinth, a bracket, a floor, a baseline. Gravity and the thing that resists it.

That is a genuinely good brief for this site, because it is also literally
true of what the site does: it puts a floor under people who are otherwise
standing on other people's guesses.

THE CONSTRAINTS, WHICH ARE THE 37SIGNALS ONES

  - Monoline. One stroke weight per mark, 2.6 units on a 32 grid.
  - Flat. No gradients, no shadows, no depth. Two colors at most, and the
    second one is used once.
  - Legible at 16px, because that is a favicon and a browser tab.
  - Constructed from primitives - rectangles, circles, straight lines, one
    arc. Nothing hand-drawn, nothing that needs an illustrator to redraw.
  - It has to work knocked out white on deep pine for the footer, which
    kills anything relying on a light fill.

Every mark below is inline SVG with `currentColor`, so the same markup is the
header logo, the footer logo, the favicon and the app icon - and none of them
is a separate file that can drift from the others.

WHAT IS BEING TESTED, AND HOW

Each mark is shown five ways, because a mark that only works at one size is
not a mark: at 44px, at 16px next to a browser tab, in the header lockup, in
the footer reversed out, and as a rounded app square. A mark that survives all
five is a candidate; several below plainly do not, and the notes say so.
"""
import os, re, sys

HERE = os.path.dirname(os.path.abspath(__file__))
SITE = os.path.dirname(HERE)
DONOR = os.path.join(SITE, "ops", "stage-architecture.html")
OUT = os.path.join(SITE, "ops", "marks.html")
UPDATED = "13 August 2026"

NAV = [("brief", "The brief"), ("marks", "Ten marks"),
       ("usage", "In use"), ("pick", "Which three")]

PINE = "#26604C"
DEEP = "#0F3227"
GOLD = "#FFD976"

# Every mark: (key, name, idea, svg-body, verdict, note)
# The svg body is drawn on a 32x32 grid, stroke 2.6, currentColor, and the
# gold accent is applied with a literal fill/stroke so it survives reversal.
MARKS = [
    ("plinth", "The Plinth",
     "A block sitting on a wider base. The oldest way to say &ldquo;this is "
     "held up.&rdquo;",
     '<rect x="9" y="7" width="14" height="12" rx="2" fill="none" '
     'stroke="currentColor" stroke-width="2.6"/>'
     '<rect x="4" y="23" width="24" height="4.4" rx="2.2" fill="%s"/>' % GOLD,
     "strong",
     "The clearest reading of the brief and the best at 16px &mdash; the gold "
     "bar survives when the outline above it starts to close up. It is also "
     "the least distinctive: a rounded square on a bar is a shape many things "
     "already use."),
    ("bracket", "The Bracket",
     "A shelf bracket. A right angle doing structural work, with the diagonal "
     "that makes it hold.",
     '<path d="M8 5 V27 H27" fill="none" stroke="currentColor" '
     'stroke-width="2.6" stroke-linecap="round" stroke-linejoin="round"/>'
     '<path d="M8 27 L26 9" fill="none" stroke="%s" stroke-width="2.6" '
     'stroke-linecap="round"/>' % GOLD,
     "strong",
     "The most literal piece of hardware in the set, and the diagonal reads "
     "as both a brace and a rising line &mdash; hours accumulating on a "
     "floor. Risk: at small sizes it can read as a plain chart axis."),
    ("cradle", "The Cradle",
     "An open arc holding a circle above it. Two elements, one carrying the "
     "other.",
     '<circle cx="16" cy="12" r="4.6" fill="none" stroke="currentColor" '
     'stroke-width="2.6"/>'
     '<path d="M5 20 a11 11 0 0 0 22 0" fill="none" stroke="%s" '
     'stroke-width="2.6" stroke-linecap="round"/>' % GOLD,
     "strong",
     "The warmest of the ten, and the only one that reads as a person being "
     "held rather than an object being propped. The arc is doing the "
     "supporting, which is the brief exactly. Weakest at 16px, where the gap "
     "between circle and arc fills in."),
    ("foundation", "The Foundation",
     "Three bars, each wider than the one above. Load spreading downward.",
     '<rect x="12" y="6" width="8" height="4" rx="2" fill="currentColor"/>'
     '<rect x="8" y="13.5" width="16" height="4" rx="2" fill="currentColor"/>'
     '<rect x="4" y="21" width="24" height="4.6" rx="2.3" fill="%s"/>' % GOLD,
     "strong",
     "Reads instantly at every size, including 16px, because it is three "
     "solid shapes and no strokes. Doubles as a chart, which suits a site "
     "made of figures. The most reproducible mark here &mdash; anyone can "
     "redraw it from a description."),
    ("baseline", "The Baseline",
     "A typographic baseline: the letter sits on a rule that extends past it, "
     "doubled the way the site&rsquo;s marker underline is.",
     '<text x="16" y="21" text-anchor="middle" font-family="Bricolage '
     'Grotesque, Inter, sans-serif" font-weight="800" font-size="17" '
     'fill="currentColor" letter-spacing="-1">TS</text>'
     '<rect x="3" y="24" width="26" height="2.6" rx="1.3" '
     'fill="currentColor"/>'
     '<rect x="6" y="28" width="20" height="2.2" rx="1.1" fill="%s"/>' % GOLD,
     "ok",
     "The only mark that carries the initials, which makes it the easiest to "
     "connect to the name and the hardest to use alongside the wordmark "
     "&mdash; you get TS twice. Best used as the favicon for a lockup whose "
     "primary mark is something else."),
    ("keystone", "The Keystone",
     "An arch with its keystone picked out. The one piece that stops the "
     "whole thing falling in.",
     '<path d="M5 26 V17 a11 11 0 0 1 22 0 V26" fill="none" '
     'stroke="currentColor" stroke-width="2.6" stroke-linecap="round"/>'
     '<path d="M13.4 6.6 L18.6 6.6 L20 12 L12 12 Z" fill="%s"/>' % GOLD,
     "weak",
     "The best story in the set and the worst execution. Below about 28px the "
     "keystone becomes a smudge and the arch becomes a croquet hoop. Included "
     "because the idea is worth keeping even though this drawing is not."),
    ("scaffold", "The Scaffold",
     "A frame around a rising line. Temporary structure that lets something "
     "be built.",
     '<rect x="4.5" y="4.5" width="23" height="23" rx="3" fill="none" '
     'stroke="currentColor" stroke-width="2.6"/>'
     '<path d="M10 22 L15 16 L20 19 L25 11" fill="none" stroke="%s" '
     'stroke-width="2.6" stroke-linecap="round" stroke-linejoin="round"/>'
     % GOLD,
     "weak",
     "Honest about what the site is &mdash; scaffolding you use and then stop "
     "needing. But a rounded square with a line chart in it is the single "
     "most common software mark in existence, and this one has no way to "
     "escape looking like an analytics product."),
    ("shelf", "The Shelf",
     "A flat plane with three things resting on it. The floor is the mark.",
     '<rect x="3" y="19" width="26" height="3.4" rx="1.7" fill="%s"/>'
     '<rect x="7" y="9" width="4.6" height="10" rx="2.3" '
     'fill="currentColor"/>'
     '<rect x="13.7" y="5" width="4.6" height="14" rx="2.3" '
     'fill="currentColor"/>'
     '<rect x="20.4" y="12" width="4.6" height="7" rx="2.3" '
     'fill="currentColor"/>' % GOLD,
     "strong",
     "The closest to the mark the site already uses, and the only one where "
     "the supporting element is the colored one &mdash; the floor is gold and "
     "everything standing on it is ink. Six bars would map to the six paths "
     "if that were ever wanted; three is more legible."),
    ("column", "The Column",
     "Cap, shaft, base. The oldest drawing of stability there is.",
     '<rect x="7" y="5" width="18" height="3.6" rx="1.8" '
     'fill="currentColor"/>'
     '<rect x="13" y="10" width="6" height="12" rx="1" fill="currentColor"/>'
     '<rect x="5" y="23.5" width="22" height="4.2" rx="2.1" fill="%s"/>'
     % GOLD,
     "ok",
     "Unmistakably about support, and unmistakably institutional &mdash; it "
     "reads bank, courthouse, university. That is wrong for a site whose "
     "whole posture is one person checking things rather than an "
     "institution."),
    ("bridge", "The Bridge",
     "A deck carried by two piers, with the span picked out. Something you "
     "cross on because somebody built it.",
     '<rect x="3" y="12" width="26" height="3.2" rx="1.6" fill="%s"/>'
     '<path d="M9 15 V27 M23 15 V27" stroke="currentColor" '
     'stroke-width="2.6" stroke-linecap="round"/>'
     '<path d="M9 12 a7 7 0 0 1 14 0" fill="none" stroke="currentColor" '
     'stroke-width="2.6"/>' % GOLD,
     "ok",
     "The most narratively apt &mdash; the site is a crossing, not a "
     "destination. Three elements is one too many for 16px, and the arch "
     "above the deck is the first thing to go."),
]

VERDICT = {"strong": ("Candidate", "win"), "ok": ("Possible", ""),
           "weak": ("Not recommended", "no")}

CSS = """
.mk2{--pine:%(pine)s;--deep:%(deep)s;--gold:%(gold)s;--paper:#F4F7F4;
  --hair:#DDE4DE;--ink:#161F1B;--dim:#5B665F;
  --disp:'Bricolage Grotesque','Inter',system-ui,sans-serif;
  --body:'Inter',system-ui,sans-serif;
  --mn:'IBM Plex Mono',ui-monospace,monospace}

/* the specimen sheet */
.sheet{border:2px solid var(--ink);background:#fff;box-shadow:6px 6px 0
  var(--ink);margin:16px 0 0;overflow:hidden}
.sheet .hd{display:flex;gap:12px;align-items:baseline;flex-wrap:wrap;
  padding:15px 18px;border-bottom:2px solid var(--ink);background:var(--cream)}
.sheet .hd .no{font-family:var(--fig);font-weight:800;font-size:24px;
  color:var(--pine);line-height:1}
.sheet .hd h3{margin:0;font-size:20px}
.sheet .hd .idea{font-size:13.5px;color:#39473F;flex:1 1 320px}
.sheet .hd .v{margin-left:auto;font-family:var(--mono);font-size:9.5px;
  letter-spacing:.12em;text-transform:uppercase;border:2px solid var(--ink);
  padding:3px 8px;background:#fff;white-space:nowrap}
.sheet .hd .v.win{background:%(pine)s;color:#fff;border-color:%(pine)s}
.sheet .hd .v.no{background:#F6E4E1}
.sheet .row{display:grid;gap:0}
@media(min-width:900px){.sheet .row{grid-template-columns:126px 116px 1fr 1fr 122px}}
.sheet .cell{padding:18px;border-left:1px solid #E6EAE6;
  display:flex;flex-direction:column;gap:10px;justify-content:center}
.sheet .cell:first-child{border-left:0}
.sheet .cell .cl{font-family:var(--mono);font-size:8.5px;letter-spacing:.13em;
  text-transform:uppercase;color:#8A948D}
.sheet .cell.rev{background:%(deep)s}
.sheet .cell.rev .cl{color:#7FA294}
.sheet .note{padding:13px 18px;border-top:1px solid #E6EAE6;font-size:13.5px;
  color:#39473F;background:#FBFCFB}

/* the marks themselves */
.mark{display:block;color:%(pine)s}
.mark.rev{color:#fff}
.tabrow{display:flex;align-items:center;gap:8px;background:#EDF1EE;
  border-radius:6px 6px 0 0;padding:5px 9px;width:100%%;max-width:190px}
.tabrow .ttl{font-family:var(--body);font-size:10.5px;color:#4A544D;
  white-space:nowrap;overflow:hidden;text-overflow:ellipsis}
.lock{display:inline-flex;align-items:center;gap:10px}
.lock .wm{font-family:var(--disp);font-weight:800;font-size:19px;
  letter-spacing:-.024em;color:%(ink)s;line-height:1.03;display:block}
.lock .sub{font-family:var(--mn);font-size:8.5px;letter-spacing:.18em;
  text-transform:uppercase;color:%(dim)s;display:block}
.lock.rev .wm{color:#fff}.lock.rev .sub{color:#7FA294}
.appsq{width:62px;height:62px;border-radius:14px;background:#fff;
  display:grid;place-items:center;box-shadow:0 1px 2px rgba(22,31,27,.14),
    0 6px 18px rgba(22,31,27,.14),0 0 0 1px rgba(22,31,27,.06)}
.appsq.pine{background:%(pine)s}
.hdr{background:#F4F7F4;border:1px solid #DDE4DE;border-radius:8px;
  padding:11px 14px;display:flex;align-items:center;gap:16px;flex-wrap:wrap}
.hdr .sp{margin-left:auto}
.hdr .lnk{font-family:var(--body);font-size:12px;color:#31403A}
.hdr .cta{font-family:var(--disp);font-weight:800;font-size:12px;color:#fff;
  background:%(pine)s;padding:6px 11px;border-radius:5px}
.ftr{background:%(deep)s;border-radius:8px;padding:14px 16px;
  display:flex;align-items:center;gap:14px;flex-wrap:wrap}
.ftr .fl{font-family:var(--body);font-size:11.5px;color:#AEC6BB}
.signup{background:#fff;border-radius:10px;padding:16px 18px;
  box-shadow:0 1px 2px rgba(22,31,27,.06),0 0 0 1px rgba(22,31,27,.06);
  max-width:330px}
.signup .t{font-family:var(--disp);font-weight:800;font-size:16px;
  letter-spacing:-.02em;margin:10px 0 4px}
.signup .s{font-size:12px;color:%(dim)s;margin:0 0 11px}
.signup .f{display:flex;gap:7px}
.signup .in{flex:1;border-radius:5px;padding:8px 10px;font-size:11.5px;
  color:%(dim)s;box-shadow:0 0 0 1px #DDE4DE}
.signup .go{font-family:var(--disp);font-weight:800;font-size:11.5px;
  color:#fff;background:%(pine)s;padding:8px 12px;border-radius:5px}
.grid10{display:grid;gap:12px;margin:14px 0}
@media(min-width:700px){.grid10{grid-template-columns:repeat(5,1fr)}}
.grid10 div{border:2px solid var(--ink);background:#fff;padding:16px 8px;
  text-align:center}
.grid10 .nm{font-family:var(--mono);font-size:9.5px;letter-spacing:.1em;
  text-transform:uppercase;color:#5B665F;margin-top:9px;display:block}
.moves{border:2px solid var(--ink);background:#fff;box-shadow:5px 5px 0
  var(--ink);margin:14px 0}
.moves .row{display:grid;grid-template-columns:112px 1fr;
  border-top:1px solid var(--line)}
.moves .row:first-child{border-top:0}
.moves .n{background:var(--deep);color:var(--gold);font-family:var(--mono);
  font-size:10.5px;display:grid;place-items:center;font-weight:600;
  letter-spacing:.09em;padding:8px 4px;text-align:center}
.moves .b{padding:11px 14px}
.moves h4{font-size:15px;margin:0 0 3px}
.moves p{font-size:13.5px;margin:0;color:#39473F}
.note2{border-left:5px solid var(--gold);padding:2px 0 2px 16px;margin:16px 0}
.note2 p{font-size:14.5px;margin:0 0 6px}
""" % {"pine": PINE, "deep": DEEP, "gold": GOLD, "ink": "#161F1B",
       "dim": "#5B665F"}


def svg(body, size=44, rev=False):
    return ('<svg class="mark%s" width="%d" height="%d" viewBox="0 0 32 32" '
            'fill="none" xmlns="http://www.w3.org/2000/svg" '
            'aria-hidden="true">%s</svg>'
            % (" rev" if rev else "", size, size, body))


def lockup(body, size=30, rev=False, sub=True):
    return ('<span class="lock%s">%s<span><span class="wm">Therapist Support'
            "</span>%s</span></span>"
            % (" rev" if rev else "", svg(body, size, rev),
               '<span class="sub">California &middot; free</span>'
               if sub else ""))


def sheet(i, key, name, idea, body, verdict, note):
    lab, cls = VERDICT[verdict]
    o = ['<div class="sheet mk2">']
    o.append('<div class="hd"><span class="no">%02d</span><h3>%s</h3>'
             '<span class="idea">%s</span><span class="v %s">%s</span></div>'
             % (i, name, idea, cls, lab))
    o.append('<div class="row">')
    o.append('<div class="cell"><span class="cl">Mark, 44px</span>%s'
             '<span class="cl">16px</span>%s</div>'
             % (svg(body, 44), svg(body, 16)))
    o.append('<div class="cell"><span class="cl">App icon</span>'
             '<div class="appsq">%s</div>'
             '<div class="appsq pine">%s</div></div>'
             % (svg(body, 34), svg(body, 34, rev=True)))
    o.append('<div class="cell"><span class="cl">Header</span>'
             '<div class="hdr">%s<span class="sp"></span>'
             '<span class="lnk">The six paths</span>'
             '<span class="lnk">Calculators</span>'
             '<span class="cta">Open a calculator</span></div>'
             '<span class="cl">Browser tab</span>'
             '<div class="tabrow">%s<span class="ttl">Therapist Support '
             "&mdash; free tools for California therapists</span></div></div>"
             % (lockup(body, 30), svg(body, 15)))
    o.append('<div class="cell"><span class="cl">Sign-up card</span>'
             '<div class="signup">%s<p class="t">One email when a number '
             'moves.</p><p class="s">Six last year. Each one because a rule '
             'changed.</p><div class="f"><span class="in">you@example.com'
             '</span><span class="go">Subscribe</span></div></div></div>'
             % svg(body, 26))
    o.append('<div class="cell rev"><span class="cl">Footer, reversed</span>'
             "%s</div>" % lockup(body, 28, rev=True))
    o.append("</div>")
    o.append('<div class="note">%s</div>' % note)
    o.append("</div>")
    return "".join(o)


def build():
    donor = open(DONOR, encoding="utf-8").read()
    m = re.search(r"<style>([\s\S]*?)</style>", donor)
    if not m:
        sys.exit("no donor style block")
    css = m.group(1) + CSS

    o = ['<!DOCTYPE html><html lang="en"><head><meta charset="utf-8">',
         '<meta name="viewport" content="width=device-width,initial-scale=1">',
         '<meta name="robots" content="noindex,nofollow">',
         "<title>Ten marks, all about bearing weight</title>",
         '<link rel="preconnect" href="https://fonts.googleapis.com">',
         '<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>',
         '<link href="https://fonts.googleapis.com/css2?family=Bricolage+'
         'Grotesque:opsz,wght@12..96,700;12..96,800&family=Fraunces:opsz,'
         'wght@9..144,600;9..144,800&family=IBM+Plex+Mono:wght@400;600&'
         'family=Inter:wght@400;500;600;700&display=swap" rel="stylesheet">',
         "<style>%s</style></head><body>" % css]

    o.append('<header class="mast"><div class="wrap">'
             '<span class="lab">Working document &middot; %s</span>'
             "<h1>Ten ways to draw a floor.</h1>"
             "<p>The word in the name is <b>Support</b>, and the meaning "
             "wanted is the structural one &mdash; something underneath, "
             "holding. Ten marks on that idea, each drawn as inline SVG on a "
             "32-unit grid, and each shown <b>five ways</b>: at 44px, at "
             "16px, in the header lockup, reversed out in the footer, and as "
             "an app square. A mark that only works at one size is not a "
             "mark.</p>"
             '<div class="meta"><span class="chip">10 marks</span>'
             '<span class="chip">5 usages each</span>'
             '<span class="chip">Inline SVG, currentColor</span>'
             '<span class="chip">No image files</span>'
             "</div></div></header>" % UPDATED)

    o.append('<nav class="jump"><div class="wrap"><ul>')
    for h, t in NAV:
        o.append('<li><a href="#%s">%s</a></li>' % (h, t))
    o.append("</ul></div></nav>")
    o.append('<div class="wrap">')

    o.append('<section id="brief"><div class="kicker"><span class="n">01</span>'
             "<h2>The brief, and the constraints</h2></div>")
    o.append('<p class="lede">Support in the load-bearing sense, not the '
             "customer-service one. Which is also literally what the site "
             "does: it puts a floor under people who are otherwise standing "
             "on other people&rsquo;s guesses.</p>")
    o.append('<div class="moves">')
    for n, h, p in [
        ("MONOLINE", "One stroke weight, 2.6 units on a 32 grid",
         "Every mark is the same weight as every other, so they can be judged "
         "against each other rather than against how heavily each was drawn."),
        ("FLAT", "Two colors, and the second is used once",
         "Pine and one gold element. No gradients, no shadow, no depth. The "
         "gold is always the part doing the supporting, which is the one "
         "consistent rule across all ten."),
        ("SMALL FIRST", "It has to survive 16px",
         "That is a favicon and a browser tab, and it is where six of these "
         "ten start to fail. Every sheet below shows the 16px version beside "
         "the 44px one for exactly that reason."),
        ("REVERSIBLE", "White on deep pine, for the footer",
         "Which rules out anything that depends on a light fill or on a thin "
         "counter staying open."),
        ("ONE FILE", "Inline SVG using currentColor",
         "The header logo, the footer logo, the favicon and the app icon are "
         "the same markup at different sizes and colors. Nothing to export, "
         "and no second copy that can drift from the first."),
    ]:
        o.append('<div class="row"><div class="n">%s</div><div class="b">'
                 "<h4>%s</h4><p>%s</p></div></div>" % (n, h, p))
    o.append("</div>")
    o.append('<div class="mk2"><div class="grid10">')
    for key, name, idea, body, verdict, note in MARKS:
        o.append("<div>%s<span class=\"nm\">%s</span></div>"
                 % (svg(body, 38), name.replace("The ", "")))
    o.append("</div></div>")
    o.append('<p class="pk-d" style="font-size:13.5px;color:#39473F">All ten '
             "at 38px, for comparison. Five of them are clearly the same "
             "family &mdash; a horizontal element carrying something above it "
             "&mdash; which is what makes this a set rather than ten "
             "sketches.</p>")
    o.append("</section><hr class=\"rule\">")

    o.append('<section id="marks"><div class="kicker">'
             '<span class="n">02</span><h2>Ten marks</h2></div>')
    o.append('<p class="lede">Each one at every size it would actually be '
             "used at, with an honest note. Three are candidates, three are "
             "possible, and two are here because the idea is worth keeping "
             "even though the drawing is not.</p>")
    for i, (key, name, idea, body, verdict, note) in enumerate(MARKS, 1):
        o.append(sheet(i, key, name, idea, body, verdict, note))
    o.append("</section><hr class=\"rule\">")

    o.append('<section id="usage"><div class="kicker">'
             '<span class="n">03</span><h2>In use, side by side</h2></div>')
    o.append('<p class="lede">The four strongest, in the three places that '
             "actually decide it: the header, the footer, and a browser "
             "tab.</p>")
    strong = [m for m in MARKS if m[4] == "strong"]
    o.append('<div class="mk2">')
    for key, name, idea, body, verdict, note in strong:
        o.append('<div class="sheet" style="box-shadow:4px 4px 0 var(--ink)">'
                 '<div class="hd"><h3>%s</h3></div>'
                 '<div class="row" style="grid-template-columns:1fr 1fr 200px">'
                 '<div class="cell"><span class="cl">Header</span>'
                 '<div class="hdr">%s<span class="sp"></span>'
                 '<span class="lnk">The six paths</span>'
                 '<span class="cta">Open a calculator</span></div></div>'
                 '<div class="cell"><span class="cl">Footer</span>'
                 '<div class="ftr">%s<span class="sp"></span>'
                 '<span class="fl">California only &middot; nothing sold '
                 "here</span></div></div>"
                 '<div class="cell"><span class="cl">Tab</span>'
                 '<div class="tabrow">%s<span class="ttl">Therapist Support'
                 "</span></div></div></div></div>"
                 % (name, lockup(body, 28), lockup(body, 26, rev=True),
                    svg(body, 15)))
    o.append("</div>")
    o.append("</section><hr class=\"rule\">")

    o.append('<section id="pick"><div class="kicker">'
             '<span class="n">04</span><h2>Which three to test</h2></div>')
    o.append('<div class="note2"><p><b>The Foundation, first.</b> Three solid '
             "bars, each wider than the one above. It is the only mark here "
             "that is exactly as legible at 16px as at 44px, because it has "
             "no strokes and no counters to close up &mdash; and it doubles "
             "as a chart, which suits a site made entirely of figures. It is "
             "also the one a stranger could redraw from a sentence, which is "
             "the real test of a mark.</p>"
             "<p><b>The Shelf, second</b>, because it inverts the color rule "
             "in a way the others do not: the floor is gold and everything "
             "standing on it is ink, so the supporting element is literally "
             "the thing you see first. If the six paths ever want to be in "
             "the mark, six bars fit here and nowhere else.</p>"
             "<p><b>The Cradle, third and the outside bet.</b> It is the only "
             "one of the ten that reads as a person being held rather than an "
             "object being propped, which is closer to what a therapist would "
             "want from the word. It is also the weakest at 16px, so it wins "
             "only if the favicon can be a simplified version of it &mdash; "
             "which is allowed, and is what most good marks do.</p></div>")
    o.append('<div class="note2"><p><b>What I would not ship.</b> The Column '
             "reads bank and courthouse, which is wrong for a site whose "
             "whole posture is one person checking things rather than an "
             "institution. The Scaffold is a rounded square with a line chart "
             "in it, which is the most common software mark in existence. And "
             "the Keystone has the best story of the ten and the worst "
             "drawing &mdash; below 28px it becomes a croquet hoop. The idea "
             "deserves a second attempt; this execution does not.</p>"
             "</div>")
    o.append('<div class="note2"><p><b>Next step, if one of these is '
             "chosen:</b> the mark is already inline SVG using "
             "<code>currentColor</code>, so shipping it is one partial in the "
             "chrome pass plus a favicon route. There is no export step and "
             "no image file, which also means there is no second copy to "
             "drift.</p></div>")
    o.append("</section>")

    o.append("</div>")
    o.append('<footer><div class="wrap"><p style="margin:0">Working document, '
             "not linked from the site and not indexable. Every mark is drawn "
             "in SVG on this page &mdash; there are no image files. Written "
             "%s.</p></div></footer>" % UPDATED)
    o.append("</body></html>")
    return "".join(o)


def main():
    print("ten marks")
    html = build()
    open(OUT, "w", encoding="utf-8").write(html)
    print("  wrote ops/%s, %s bytes"
          % (os.path.basename(OUT), format(len(html), ",d")))

    bad = 0
    for h, _ in NAV:
        if 'id="%s"' % h not in html:
            print("GUARD: the jump nav points at #%s, absent" % h)
            bad += 1
    if len(MARKS) != 10:
        print("GUARD: %d marks, the document claims ten" % len(MARKS))
        bad += 1

    # Every mark must appear in all five usages, or the sheet is not a test.
    # Five renders per sheet, plus the comparison grid, plus the header/footer/
    # tab strip for the strong ones.
    for key, name, idea, body, verdict, note in MARKS:
        n = html.count(body)
        want = 8 if verdict == "strong" else 5
        if n < want:
            print("GUARD: %s appears %d times, expected at least %d - a mark "
                  "shown at one size is not tested" % (name, n, want))
            bad += 1
        if verdict not in VERDICT:
            print("GUARD: %s has no verdict" % name)
            bad += 1
        if not note or len(note) < 60:
            print("GUARD: %s has no honest note" % name)
            bad += 1

    # The one consistent rule across the set: gold is always the supporting
    # element. If a mark has no gold, it is not on the brief.
    for key, name, idea, body, verdict, note in MARKS:
        if GOLD not in body:
            print("GUARD: %s has no gold element, so nothing in it is doing "
                  "the supporting" % name)
            bad += 1

    # No image files. The whole point is one markup, four uses.
    if re.search(r'<img|\.png|\.svg"', html):
        print("GUARD: an image file reference - these marks are inline SVG")
        bad += 1

    for needle, what in [("bearing weight", "the brief in one phrase"),
                         ("What I would not ship", "the honest rejections"),
                         ("currentColor", "the one-file argument")]:
        if needle not in html:
            print("GUARD: %s is missing" % what)
            bad += 1

    t = re.sub(r"<(script|style)[\s\S]*?</\1>", " ", html, flags=re.I)
    t = re.sub(r"<[^>]+>", " ", t)
    for w in ("programme", "counselling", "centre", "whilst", "amongst",
              "recognise", "organisation", "behaviour", "colour",
              "fulfilment", "judgement"):
        if re.search(r"\b%s" % w, t, re.I):
            print("GUARD: British spelling %r" % w)
            bad += 1
    if 'name="robots" content="noindex' not in html:
        print("GUARD: working document must not be indexable")
        bad += 1

    if bad:
        sys.exit("\n%d problem(s)" % bad)
    print("  guards ok - %d marks, 5 usages each" % len(MARKS))


if __name__ == "__main__":
    main()
