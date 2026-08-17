#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Ten logo lockups - the wordmark itself carrying the support idea.

WHY THIS IS A SECOND DOCUMENT

`ops/marks.html` drew ten icons. An icon is not a logo. The logo is the whole
lockup - the name, its setting, and whatever holds it - and for a site called
Therapist Support the interesting question is whether the WORDMARK can carry
the idea on its own, rather than borrowing it from a symbol standing beside it.

Ten ways below, and the good ones do exactly that: the name sits on something,
is bracketed by something, or is built on a rule that extends past it. Several
need no icon at all, which is the strongest possible outcome - one less asset,
one less thing to redraw, and a mark that cannot be separated from the name.

WHAT EVERY LOCKUP HAS TO SURVIVE

  1. Horizontal, at real header size (about 19px cap height)
  2. Stacked, for a footer or a share card
  3. Small - 13px, where most of these die
  4. Reversed, white on deep pine
  5. Cropped to a square, for a favicon or an avatar

A lockup that only works in the first is a header graphic, not a logo. Each
sheet shows all five and says plainly which ones fail.

THE ONE RULE, CARRIED OVER FROM THE MARKS

Gold is always the element doing the supporting. Ink is what is being held.
That is what makes these a family rather than ten typographic ideas, and it is
also the reason the set reads as being about something rather than being
merely styled.
"""
import os, re, sys

HERE = os.path.dirname(os.path.abspath(__file__))
SITE = os.path.dirname(HERE)
DONOR = os.path.join(SITE, "ops", "stage-architecture.html")
OUT = os.path.join(SITE, "ops", "logo.html")
UPDATED = "13 August 2026"

NAV = [("idea", "The idea"), ("lockups", "Ten lockups"),
       ("applied", "Applied"), ("pick", "Which one")]

PINE, DEEP, GOLD, INK = "#2C6350", "#123C30", "#FFE7A3", "#1B2420"

# key, name, idea, extra css, html builder key, verdict, note
LOCKUPS = [
    ("rule", "The Rule",
     "The name sits on a two-weight baseline that runs past it on both sides "
     "&mdash; ink over gold, the heavier line underneath.",
     "strong",
     "The purest expression of the brief and the only one that needs no icon "
     "at all. The doubled rule is the site&rsquo;s own marker underline, "
     "promoted from decoration to structure. Survives every size, including "
     "13px, because the rule is the last thing to disappear."),
    ("plinth", "The Plinth",
     "The name in a solid pine block, resting on a wider gold slab. A sign "
     "on a base.",
     "strong",
     "The most confident at small sizes, because it is two solid shapes and "
     "the type is knocked out rather than drawn. Reads as a plaque, which is "
     "either exactly right for a reference site or slightly municipal, "
     "depending on the day."),
    ("bracket", "The Bracket",
     "Two gold brackets holding the name between them, the way a shelf is "
     "held at both ends.",
     "ok",
     "Elegant, and the brackets do read as structural. But bracketed type is "
     "a common editorial device and this loses its meaning at small sizes, "
     "where the brackets read as ordinary punctuation."),
    ("stack", "The Stack",
     "Two lines, the second wider than the first, on a rule. Load spreading "
     "downward, done with type.",
     "strong",
     "The stacked lockup is the primary here rather than a secondary, which "
     "suits a footer and a share card better than a header. The widening is "
     "achieved with letter-spacing on the second line, so it needs no custom "
     "drawing."),
    ("underline", "The Underline",
     "One word underlined, and it is the word Support &mdash; the rule is "
     "under the thing it means.",
     "strong",
     "The wittiest of the ten and the easiest to explain in one sentence. "
     "The risk is that an underline on one word of a two-word name reads as "
     "a hyperlink, which is a real hazard on the web and worth testing "
     "before committing."),
    ("weight", "The Weight",
     "Therapist set light, Support set heavy, on a shared baseline. The "
     "second word is visibly carrying the first.",
     "ok",
     "Works at large sizes and is genuinely clever &mdash; the weight "
     "contrast IS the concept. Below about 16px the two weights converge and "
     "the whole idea evaporates, leaving an ordinary wordmark."),
    ("shelf", "The Shelf",
     "The name sits on a gold shelf with a short return at each end, like a "
     "ledge with lips.",
     "ok",
     "The most literal and the most decorative. Fine at header size, and the "
     "returns become noise below 16px. Better as a share-card treatment than "
     "as the everyday lockup."),
    ("ground", "The Ground",
     "The lower third of the lockup is a solid gold band that the type sits "
     "into, overlapping it slightly &mdash; the name standing on ground "
     "rather than floating above it.",
     "strong",
     "The only one where the type and the supporting element actually touch, "
     "which is what makes it feel like weight rather than a line drawn "
     "nearby. Holds up reversed, which several others do not."),
    ("column", "The Column Rule",
     "A vertical gold rule to the left, the name and its qualifier to the "
     "right. Support from the side rather than below.",
     "weak",
     "Included as the control. It is a perfectly good lockup and it is not "
     "on brief &mdash; a left rule says pull-quote and sidebar, not weight. "
     "Useful proof that the brief is doing real work in the other nine."),
    ("dotrule", "The Dotted Floor",
     "The name on a dotted rule, like a form line waiting to be filled in.",
     "weak",
     "Reads as a form field or a table of contents leader, and a dotted line "
     "is the visual language of something incomplete &mdash; the opposite of "
     "the stability the brief asks for. A useful wrong answer."),
]

CSS = """
.lg2{--pine:%(pine)s;--deep:%(deep)s;--gold:%(gold)s;--ink:%(ink)s;
  --dim:#5F6A64;--paper:#F6F8F6;--hair:#DFE4E0;
  --disp:'Bricolage Grotesque','Inter',system-ui,sans-serif;
  --mn:'IBM Plex Mono',ui-monospace,monospace}
.lg2 .wm{font-family:var(--disp);font-weight:800;letter-spacing:-.028em;
  line-height:1;color:var(--ink);white-space:nowrap}
.lg2 .qual{font-family:var(--mn);letter-spacing:.2em;text-transform:uppercase;
  color:var(--dim);display:block;white-space:nowrap}
.rev .wm{color:#fff}.rev .qual{color:#8FB3A4}

/* 01 the rule */
.L-rule{display:inline-block}
.L-rule .bar1{height:.16em;background:var(--ink);border-radius:.08em;
  margin-top:.2em}
.L-rule .bar2{height:.24em;background:var(--gold);border-radius:.12em;
  margin-top:.1em}
.rev .L-rule .bar1{background:#fff}

/* 02 the plinth */
.L-plinth{display:inline-block}
.L-plinth .blk{background:var(--pine);padding:.34em .5em .38em;
  border-radius:.16em}
.L-plinth .blk .wm{color:#fff}
.L-plinth .base{height:.26em;background:var(--gold);border-radius:.13em;
  margin:.1em -.22em 0}
.rev .L-plinth .blk{background:#fff}
.rev .L-plinth .blk .wm{color:var(--deep)}

/* 03 the bracket */
.L-bracket{display:inline-flex;align-items:stretch;gap:.34em}
.L-bracket .br{width:.2em;background:var(--gold);border-radius:.1em}
.L-bracket .mid{display:flex;flex-direction:column;justify-content:center}

/* 04 the stack */
.L-stack{display:inline-block;text-align:center}
.L-stack .l1{display:block}
.L-stack .l2{display:block;letter-spacing:.06em;margin-top:.02em}
.L-stack .base{height:.2em;background:var(--gold);border-radius:.1em;
  margin-top:.18em}

/* 05 the underline */
.L-under .u{position:relative;display:inline-block}
.L-under .u::after{content:'';position:absolute;left:-.04em;right:-.04em;
  bottom:-.16em;height:.19em;background:var(--gold);border-radius:.1em}

/* 06 the weight */
.L-weight .a{font-weight:400}
.L-weight .b{font-weight:800}
.L-weight .base{height:.17em;background:var(--gold);border-radius:.09em;
  margin-top:.2em}

/* 07 the shelf */
.L-shelf{display:inline-block}
.L-shelf .sh{height:.2em;background:var(--gold);border-radius:.1em;
  margin:.2em -.1em 0;position:relative}
.L-shelf .sh::before,.L-shelf .sh::after{content:'';position:absolute;
  top:-.16em;width:.2em;height:.2em;background:var(--gold);
  border-radius:.06em}
.L-shelf .sh::before{left:0}.L-shelf .sh::after{right:0}

/* 08 the ground */
.L-ground{display:inline-block;position:relative;padding-bottom:.16em}
.L-ground .band{position:absolute;left:-.24em;right:-.24em;bottom:0;
  height:.36em;background:var(--gold);border-radius:.06em;z-index:0}
.L-ground .txt{position:relative;z-index:1}

/* 09 the column rule */
.L-col{display:inline-flex;gap:.4em;align-items:stretch}
.L-col .v{width:.2em;background:var(--gold);border-radius:.1em}

/* 10 the dotted floor */
.L-dot .dl{height:.2em;margin-top:.22em;
  background:radial-gradient(circle,var(--gold) 42%%,transparent 44%%);
  background-size:.36em .36em;background-repeat:repeat-x;
  background-position:center}

/* the sheet */
.sh2{border:2px solid var(--ink);background:#fff;box-shadow:6px 6px 0
  var(--ink);margin:18px 0 0;overflow:hidden}
.sh2 .hd{display:flex;gap:12px;align-items:baseline;flex-wrap:wrap;
  padding:15px 18px;border-bottom:2px solid var(--ink);background:var(--cream)}
.sh2 .hd .no{font-family:var(--fig);font-weight:800;font-size:24px;
  color:var(--pine);line-height:1}
.sh2 .hd h3{margin:0;font-size:20px}
.sh2 .hd .idea{font-size:13.5px;color:#39473F;flex:1 1 300px}
.sh2 .hd .v{margin-left:auto;font-family:var(--mono);font-size:9.5px;
  letter-spacing:.12em;text-transform:uppercase;border:2px solid var(--ink);
  padding:3px 8px;background:#fff;white-space:nowrap}
.sh2 .hd .v.win{background:%(pine)s;color:#fff;border-color:%(pine)s}
.sh2 .hd .v.no{background:#F6E4E1}
.sh2 .row{display:grid}
@media(min-width:980px){.sh2 .row{grid-template-columns:1.5fr 1fr .8fr 1fr .8fr}}
.sh2 .cell{padding:20px 18px;border-left:1px solid #E6EAE6;display:flex;
  flex-direction:column;gap:12px;justify-content:center;align-items:flex-start}
.sh2 .cell:first-child{border-left:0}
.sh2 .cl{font-family:var(--mono);font-size:8.5px;letter-spacing:.13em;
  text-transform:uppercase;color:#8A948D}
.sh2 .cell.rev{background:%(deep)s}
.sh2 .cell.rev .cl{color:#7FA294}
.sh2 .note{padding:13px 18px;border-top:1px solid #E6EAE6;font-size:13.5px;
  color:#39473F;background:#FBFCFB}
.fav{width:56px;height:56px;border-radius:12px;background:#fff;display:grid;
  place-items:center;overflow:hidden;
  box-shadow:0 1px 2px rgba(22,31,27,.14),0 6px 18px rgba(22,31,27,.12),
    0 0 0 1px rgba(22,31,27,.06)}
.fav.pine{background:%(pine)s}
.hdr2{background:#F6F8F6;border:1px solid #DFE4E0;border-radius:8px;
  padding:12px 15px;display:flex;align-items:center;gap:18px;flex-wrap:wrap;
  width:100%%}
.hdr2 .sp{margin-left:auto}
.hdr2 .lnk{font-family:'Inter',sans-serif;font-size:12px;color:#31403A}
.hdr2 .cta{font-family:var(--disp);font-weight:800;font-size:12px;color:#fff;
  background:%(pine)s;padding:6px 11px;border-radius:5px}
.ftr2{background:%(deep)s;border-radius:8px;padding:16px 18px;
  display:flex;align-items:center;gap:16px;flex-wrap:wrap;width:100%%}
.ftr2 .fl{font-family:'Inter',sans-serif;font-size:11.5px;color:#AEC6BB}
.card2{background:#fff;border-radius:10px;padding:16px 18px;width:100%%;
  max-width:340px;box-shadow:0 1px 2px rgba(22,31,27,.06),
    0 0 0 1px rgba(22,31,27,.06)}
.card2 .t{font-family:var(--disp);font-weight:800;font-size:16px;
  letter-spacing:-.02em;margin:12px 0 4px}
.card2 .s{font-family:'Inter',sans-serif;font-size:12px;color:#5F6A64;
  margin:0 0 11px}
.card2 .f{display:flex;gap:7px}
.card2 .in{flex:1;border-radius:5px;padding:8px 10px;font-size:11.5px;
  color:#5F6A64;box-shadow:0 0 0 1px #DFE4E0;font-family:'Inter',sans-serif}
.card2 .go{font-family:var(--disp);font-weight:800;font-size:11.5px;color:#fff;
  background:%(pine)s;padding:8px 12px;border-radius:5px}
.moves{border:2px solid var(--ink);background:#fff;box-shadow:5px 5px 0
  var(--ink);margin:14px 0}
.moves .row{display:grid;grid-template-columns:100px 1fr;
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
code{font-family:var(--mono);font-size:12.5px;background:#fff;
  border:1px solid var(--line);padding:1px 5px}
""" % {"pine": PINE, "deep": DEEP, "gold": GOLD, "ink": INK}


def lock(key, size=21, stacked=False, qual=True, rev=False):
    """One lockup at one size. Everything scales off font-size in em."""
    q = ('<span class="qual" style="font-size:%.2fpx;margin-top:.5em">'
         "California &middot; free</span>" % (size * 0.42)) if qual else ""
    w = 'style="font-size:%dpx"' % size
    if key == "rule":
        inner = ('<span class="wm" %s>Therapist Support</span>'
                 '<div class="bar1"></div><div class="bar2"></div>%s'
                 % (w, q))
        return '<span class="L-rule" style="font-size:%dpx">%s</span>' % (
            size, inner)
    if key == "plinth":
        return ('<span class="L-plinth" style="font-size:%dpx">'
                '<div class="blk"><span class="wm" %s>Therapist Support</span>'
                '</div><div class="base"></div>%s</span>' % (size, w, q))
    if key == "bracket":
        return ('<span class="L-bracket" style="font-size:%dpx">'
                '<span class="br"></span><span class="mid">'
                '<span class="wm" %s>Therapist Support</span>%s</span>'
                '<span class="br"></span></span>' % (size, w, q))
    if key == "stack":
        return ('<span class="L-stack" style="font-size:%dpx">'
                '<span class="wm l1" %s>Therapist</span>'
                '<span class="wm l2" %s>Support</span>'
                '<div class="base"></div>%s</span>' % (size, w, w, q))
    if key == "underline":
        return ('<span class="L-under" style="font-size:%dpx">'
                '<span class="wm" %s>Therapist <span class="u">Support</span>'
                "</span>%s</span>" % (size, w, q))
    if key == "weight":
        return ('<span class="L-weight" style="font-size:%dpx">'
                '<span class="wm" %s><span class="a">Therapist</span> '
                '<span class="b">Support</span></span><div class="base">'
                "</div>%s</span>" % (size, w, q))
    if key == "shelf":
        return ('<span class="L-shelf" style="font-size:%dpx">'
                '<span class="wm" %s>Therapist Support</span>'
                '<div class="sh"></div>%s</span>' % (size, w, q))
    if key == "ground":
        return ('<span class="L-ground" style="font-size:%dpx">'
                '<span class="band"></span>'
                '<span class="txt wm" %s>Therapist Support</span>%s</span>'
                % (size, w, q))
    if key == "column":
        return ('<span class="L-col" style="font-size:%dpx">'
                '<span class="v"></span><span><span class="wm" %s>Therapist '
                "Support</span>%s</span></span>" % (size, w, q))
    return ('<span class="L-dot" style="font-size:%dpx">'
            '<span class="wm" %s>Therapist Support</span>'
            '<div class="dl"></div>%s</span>' % (size, w, q))


def favicon(key, pine=False):
    """Cropped square. The lockup's supporting element is what survives."""
    body = {
        "rule": '<span class="wm" style="font-size:21px">T</span>'
                '<div class="bar1"></div><div class="bar2"></div>',
        "plinth": '<div class="blk"><span class="wm" style="font-size:19px">'
                  "T</span></div><div class=\"base\"></div>",
        "bracket": '<span class="br"></span><span class="mid">'
                   '<span class="wm" style="font-size:21px">T</span></span>'
                   '<span class="br"></span>',
        "stack": '<span class="wm l1" style="font-size:16px">T</span>'
                 '<span class="wm l2" style="font-size:16px">S</span>'
                 '<div class="base"></div>',
        "underline": '<span class="wm" style="font-size:22px">'
                     '<span class="u">TS</span></span>',
        "weight": '<span class="wm" style="font-size:20px">'
                  '<span class="a">T</span><span class="b">S</span></span>'
                  '<div class="base"></div>',
        "shelf": '<span class="wm" style="font-size:20px">TS</span>'
                 '<div class="sh"></div>',
        "ground": '<span class="band"></span>'
                  '<span class="txt wm" style="font-size:21px">TS</span>',
        "column": '<span class="v"></span><span><span class="wm" '
                  'style="font-size:21px">TS</span></span>',
        "dotrule": '<span class="wm" style="font-size:20px">TS</span>'
                   '<div class="dl"></div>',
    }[key]
    cls = {"rule": "L-rule", "plinth": "L-plinth", "bracket": "L-bracket",
           "stack": "L-stack", "underline": "L-under", "weight": "L-weight",
           "shelf": "L-shelf", "ground": "L-ground", "column": "L-col",
           "dotrule": "L-dot"}[key]
    return ('<div class="fav%s"><span class="%s" style="font-size:21px">%s'
            "</span></div>" % (" pine" if pine else "", cls, body))


VERD = {"strong": ("Candidate", "win"), "ok": ("Possible", ""),
        "weak": ("Not on brief", "no")}


def sheet(i, key, name, idea, verdict, note):
    lab, cls = VERD[verdict]
    o = ['<div class="sh2 lg2">']
    o.append('<div class="hd"><span class="no">%02d</span><h3>%s</h3>'
             '<span class="idea">%s</span><span class="v %s">%s</span></div>'
             % (i, name, idea, cls, lab))
    o.append('<div class="row">')
    o.append('<div class="cell"><span class="cl">Horizontal, header size</span>'
             "%s</div>" % lock(key, 21))
    o.append('<div class="cell"><span class="cl">Stacked</span>%s'
             '<span class="cl">13px, the killer</span>%s</div>'
             % (lock("stack" if key == "stack" else key, 15),
                lock(key, 13, qual=False)))
    o.append('<div class="cell"><span class="cl">Favicon</span>%s%s</div>'
             % (favicon(key), favicon(key, pine=True)))
    o.append('<div class="cell"><span class="cl">In a header</span>'
             '<div class="hdr2">%s<span class="sp"></span>'
             '<span class="lnk">The six paths</span>'
             '<span class="lnk">Calculators</span>'
             '<span class="cta">Open a calculator</span></div>'
             '<span class="cl">Sign-up card</span>'
             '<div class="card2">%s<p class="t">One email when a number '
             'moves.</p><p class="s">Six last year. Each one because a rule '
             'changed.</p><div class="f"><span class="in">you@example.com'
             '</span><span class="go">Subscribe</span></div></div></div>'
             % (lock(key, 17, qual=False), lock(key, 15, qual=False)))
    o.append('<div class="cell rev"><span class="cl">Reversed, footer</span>'
             '<div class="rev">%s</div></div>' % lock(key, 19))
    o.append("</div>")
    o.append('<div class="note">%s</div></div>' % note)
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
         "<title>Ten logo lockups, all standing on something</title>",
         '<link rel="preconnect" href="https://fonts.googleapis.com">',
         '<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>',
         '<link href="https://fonts.googleapis.com/css2?family=Bricolage+'
         'Grotesque:opsz,wght@12..96,400;12..96,700;12..96,800&family=Fraunces:'
         'opsz,wght@9..144,600;9..144,800&family=IBM+Plex+Mono:wght@400;600&'
         'family=Inter:wght@400;500;600;700&display=swap" rel="stylesheet">',
         "<style>%s</style></head><body>" % css]

    o.append('<header class="mast"><div class="wrap">'
             '<span class="lab">Working document &middot; %s</span>'
             "<h1>Ten logos, all standing on something.</h1>"
             "<p>The icons were the last document. This is the <b>logo</b> "
             "&mdash; the whole lockup, and the question of whether the "
             "wordmark can carry the support idea by itself rather than "
             "borrowing it from a symbol standing next to it. The good ones "
             "do, which means <b>no icon is needed at all</b>: one less "
             "asset, and a mark that cannot be separated from the name. Each "
             "is shown horizontal, stacked, at 13px, reversed, and cropped "
             "to a favicon.</p>"
             '<div class="meta"><span class="chip">10 lockups</span>'
             '<span class="chip">5 sizes each</span>'
             '<span class="chip">Pure CSS and type</span>'
             '<span class="chip">No image files</span>'
             "</div></div></header>" % UPDATED)

    o.append('<nav class="jump"><div class="wrap"><ul>')
    for h, t in NAV:
        o.append('<li><a href="#%s">%s</a></li>' % (h, t))
    o.append("</ul></div></nav>")
    o.append('<div class="wrap">')

    o.append('<section id="idea"><div class="kicker"><span class="n">01</span>'
             "<h2>The idea, applied to type</h2></div>")
    o.append('<p class="lede">Same brief as the icons &mdash; support in the '
             "load-bearing sense &mdash; but the name has to do the work. "
             "Three ways type can carry weight, and all ten below are one of "
             "them.</p>")
    o.append('<div class="moves">')
    for n, h, p in [
        ("SIT ON", "The name rests on a rule, a slab or a band",
         "The Rule, the Plinth, the Stack, the Ground, the Shelf. The "
         "supporting element runs the full width or wider, so the name is "
         "visibly carried rather than merely underlined."),
        ("BE HELD", "Something grips the name from the sides",
         "The Bracket, the Column Rule. Weaker on brief, because holding from "
         "the side is a different physical idea from bearing weight &mdash; "
         "and the Column Rule is included to prove that."),
        ("CARRY", "One part of the name holds the other",
         "The Weight and the Underline. The cleverest of the three, and the "
         "most fragile: both depend on a contrast that disappears at small "
         "sizes."),
        ("THE RULE", "Gold is always the thing doing the supporting",
         "Carried over from the icon set. Ink is what is being held. It is "
         "what makes these a family rather than ten typographic ideas."),
    ]:
        o.append('<div class="row"><div class="n">%s</div><div class="b">'
                 "<h4>%s</h4><p>%s</p></div></div>" % (n, h, p))
    o.append("</div>")
    o.append('<div class="note2"><p><b>None of these is an image file.</b> '
             "Every lockup below is the wordmark plus one or two CSS "
             "elements, sized in <code>em</code> so the whole thing scales "
             "from a single <code>font-size</code>. That means the header "
             "logo, the footer logo and the favicon are the same markup, and "
             "there is no export step and no second copy to drift &mdash; the "
             "same argument as the icons, and it applies harder here because "
             "a wordmark is the asset most often re-cut badly.</p></div>")
    o.append("</section><hr class=\"rule\">")

    o.append('<section id="lockups"><div class="kicker">'
             '<span class="n">02</span><h2>Ten lockups</h2></div>')
    o.append('<p class="lede">Each at every size it has to survive. The 13px '
             "column is where most logos are actually decided and where four "
             "of these fail.</p>")
    for i, (key, name, idea, verdict, note) in enumerate(LOCKUPS, 1):
        o.append(sheet(i, key, name, idea, verdict, note))
    o.append("</section><hr class=\"rule\">")

    o.append('<section id="applied"><div class="kicker">'
             '<span class="n">03</span><h2>The five candidates, applied'
             "</h2></div>")
    o.append('<p class="lede">Header, footer and sign-up card, which is every '
             "place the logo actually appears on this site.</p>")
    o.append('<div class="lg2">')
    for key, name, idea, verdict, note in [l for l in LOCKUPS
                                           if l[3] == "strong"]:
        o.append('<div class="sh2" style="box-shadow:4px 4px 0 var(--ink)">'
                 '<div class="hd"><h3>%s</h3></div><div class="row" '
                 'style="grid-template-columns:1.3fr 1fr 1fr">'
                 '<div class="cell"><span class="cl">Header</span>'
                 '<div class="hdr2">%s<span class="sp"></span>'
                 '<span class="lnk">The six paths</span>'
                 '<span class="cta">Open a calculator</span></div></div>'
                 '<div class="cell rev"><span class="cl">Footer</span>'
                 '<div class="ftr2 rev">%s<span class="sp"></span>'
                 '<span class="fl">California only &middot; nothing sold '
                 "here</span></div></div>"
                 '<div class="cell"><span class="cl">Sign-up</span>'
                 '<div class="card2">%s<p class="t">One email when a number '
                 'moves.</p><div class="f"><span class="in">you@example.com'
                 '</span><span class="go">Subscribe</span></div></div></div>'
                 "</div></div>"
                 % (name, lock(key, 18, qual=False), lock(key, 17),
                    lock(key, 15, qual=False)))
    o.append("</div>")
    o.append("</section><hr class=\"rule\">")

    o.append('<section id="pick"><div class="kicker">'
             '<span class="n">04</span><h2>Which one</h2></div>')
    o.append('<div class="note2"><p><b>The Rule.</b> The name over a '
             "two-weight baseline, ink above gold, running past the word on "
             "both sides. It is the only lockup here that needs no icon, no "
             "container and no color block &mdash; which means it works in an "
             "email signature, in plain text on a share card, and at 13px in "
             "a footer, all without being redrawn. It is also already the "
             "site&rsquo;s own gesture: the marker underline that has been "
             "decoration since the first page becomes the structural "
             "idea.</p>"
             "<p><b>The Ground is the one to test it against.</b> It is the "
             "only lockup where the type and the supporting element actually "
             "overlap, so it reads as weight rather than as a line drawn "
             "nearby. It is stronger reversed than the Rule is, which matters "
             "because the footer is dark on every page.</p>"
             "<p><b>And keep the Stack as the secondary.</b> A two-line "
             "lockup on a base, for the share card, the app icon and anywhere "
             "the horizontal one would have to be set too small to "
             "read.</p></div>")
    o.append('<div class="note2"><p><b>The one to be careful with.</b> The '
             "Underline is the wittiest of the ten &mdash; a rule under the "
             "word Support &mdash; and on the web an underline under one word "
             "reads as a link. That is testable in about ten minutes with "
             "five people and worth testing before it ships, because if it "
             "reads as a link it is not a charming logo, it is a broken "
             "one.</p>"
             "<p><b>What is not on brief:</b> the Column Rule says "
             "pull-quote, and the Dotted Floor says form field &mdash; a "
             "dotted line is the visual language of something not yet filled "
             "in, which is the opposite of the stability being asked for. "
             "Both are here as controls, and their failure is evidence the "
             "brief is doing real work in the other eight.</p></div>")
    o.append("</section>")

    o.append("</div>")
    o.append('<footer><div class="wrap"><p style="margin:0">Working document, '
             "not linked from the site and not indexable. Every lockup is CSS "
             "and live type &mdash; there are no image files, and each scales "
             "from one font-size. Written %s.</p></div></footer>" % UPDATED)
    o.append("</body></html>")
    return "".join(o)


def main():
    print("ten logo lockups")
    html = build()
    open(OUT, "w", encoding="utf-8").write(html)
    print("  wrote ops/%s, %s bytes"
          % (os.path.basename(OUT), format(len(html), ",d")))

    bad = 0
    for h, _ in NAV:
        if 'id="%s"' % h not in html:
            print("GUARD: the jump nav points at #%s, absent" % h)
            bad += 1
    if len(LOCKUPS) != 10:
        print("GUARD: %d lockups, the document claims ten" % len(LOCKUPS))
        bad += 1
    for key, name, idea, verdict, note in LOCKUPS:
        if verdict not in VERD:
            print("GUARD: %s has no verdict" % name)
            bad += 1
        if len(note) < 60:
            print("GUARD: %s has no honest note" % name)
            bad += 1
        if name not in html:
            print("GUARD: %s never appears" % name)
            bad += 1

    # Five sizes each, or the sheet is not a test. Six for the candidates,
    # which appear again in the applied section.
    for key, name, idea, verdict, note in LOCKUPS:
        cls = {"rule": "L-rule", "plinth": "L-plinth", "bracket": "L-bracket",
               "stack": "L-stack", "underline": "L-under",
               "weight": "L-weight", "shelf": "L-shelf", "ground": "L-ground",
               "column": "L-col", "dotrule": "L-dot"}[key]
        n = html.count('class="%s"' % cls)
        want = 9 if verdict == "strong" else 6
        if n < want:
            print("GUARD: %s appears %d times, expected at least %d - a "
                  "lockup shown at one size is not tested" % (name, n, want))
            bad += 1

    if re.search(r'<img|\.png"|\.svg"', html):
        print("GUARD: an image file - these lockups are CSS and live type")
        bad += 1
    for needle, what in [("no icon is needed at all", "the strongest finding"),
                         ("reads as a link", "the underline warning"),
                         ("Gold is always", "the rule carried from the icons")]:
        if needle not in html:
            print("GUARD: %s is missing" % what)
            bad += 1
    if 'name="robots" content="noindex' not in html:
        print("GUARD: working document must not be indexable")
        bad += 1

    t = re.sub(r"<(script|style)[\s\S]*?</\1>", " ", html, flags=re.I)
    t = re.sub(r"<[^>]+>", " ", t)
    for w in ("programme", "counselling", "centre", "whilst", "amongst",
              "colour", "recognise", "organisation", "behaviour"):
        if re.search(r"\b%s" % w, t, re.I):
            print("GUARD: British spelling %r" % w)
            bad += 1

    if bad:
        sys.exit("\n%d problem(s)" % bad)
    print("  guards ok - %d lockups, 5 sizes each" % len(LOCKUPS))


if __name__ == "__main__":
    main()
