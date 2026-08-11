#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""The shared surface for the research pages, so five builders are one design.

WHY THIS EXISTS

`_dev/build_assocpay.py` was the first page on this site written whole by a
builder rather than assembled by decorating a hand-written file, and it works.
It also carries about 600 lines of CSS and a chrome-borrowing routine that has
nothing to do with associate pay, and the next five pages needed all of it.

Copying that block five times would have produced five design systems that
looked identical on the day they shipped and diverged the first time anyone
touched one of them. `_dev/extract_css.py` would then have hoisted five
near-identical style blocks and `_dev/css_dedupe.py` would have deduplicated
exactly none of them, because near-identical is not identical.

So the CSS lives here once, under a `pk-` prefix, and every builder that
imports it emits a byte-identical `<style>` block. The dedupe pass collapses
them to one. Change a colour here and it changes on every page at once, which
is the point.

WHAT IS DELIBERATELY NOT HERE

Content. No page's words, figures or structure live in this file - only the
shell they are rendered into. A helper that decided what a section should say
would make the builders harder to read than the HTML they replace.

And no state, no analytics, nothing that leaves the page. The site's printed
promise is that nothing a reader types is sent anywhere; a shared kit is
exactly where that promise would be broken by accident.
"""
import os, re, sys

HERE = os.path.dirname(os.path.abspath(__file__))
SITE = os.path.dirname(HERE)

INK = "#16211B"
PINE = "#2C6350"
GOLD = "#F6C560"
PAPER = "#F4F0E6"
CREAM = "#FBF9F3"
MUTED = "#635E53"
RED = "#B5483F"

# Not the site gold. #F6C560 on pine measures 4.35:1, under the 4.5 floor every
# other pass on this site enforces. #FFD37A is the lighter gold the hero kicker
# already uses on that background, so this borrows from the palette rather than
# inventing. On ink panels plain GOLD clears the floor and is left alone.
GOLD_ON_PINE = "#FFD37A"

CHECKED = "August 2026"


# --------------------------------------------------------------- small things
def esc(x):
    return (str(x).replace("&", "&amp;").replace("<", "&lt;")
            .replace(">", "&gt;").replace('"', "&quot;"))


def money(n):
    return "$" + format(int(round(n)), ",d")


def pct(n, places=0):
    return ("%." + str(places) + "f%%") % n


# ------------------------------------------------------------------- chrome
def chrome_parts(donor_filename):
    """Head, header, footer, stylesheet links and inline scripts from a donor.

    A builder writes a page that does not exist yet, so it has no chrome of its
    own and no pass has run over it. It borrows a built page's chrome, stripped
    of everything that identifies that page - title, description, canonical,
    Open Graph, the `ts:` metadata, the JSON-LD block and the pass markers -
    and keeps everything that is genuinely shared: fonts, the masthead, the nav
    script, the footer.

    Every STRUCTURE pass afterwards then decorates the result like any other
    page, which is why this has to strip rather than keep. A leftover canonical
    from the donor is a page that tells search engines it is a different page.
    """
    path = os.path.join(SITE, donor_filename)
    if not os.path.exists(path):
        sys.exit("pagekit: the chrome donor %s is missing" % donor_filename)
    chrome = open(path, encoding="utf-8").read()

    head = chrome[:chrome.index("</head>")]
    head = re.sub(r"<title>[\s\S]*?</title>", "", head)
    head = re.sub(r'<meta name="description"[^>]*>', "", head)
    head = re.sub(r'<meta property="og:[^>]*>', "", head)
    head = re.sub(r'<meta name="twitter:[^>]*>', "", head)
    head = re.sub(r'<link rel="canonical"[^>]*>', "", head)
    head = re.sub(r'<meta name="ts:[^>]*>', "", head)
    head = re.sub(r'<script type="application/ld\+json">[\s\S]*?</script>', "",
                  head)
    head = re.sub(r"<!-- _dev/[\s\S]*?-->", "", head)

    body_open_end = chrome.index(">", chrome.index("<body")) + 1
    header_end = chrome.index("</header>") + len("</header>")
    header = chrome[body_open_end:header_end]
    foot_start = chrome.rindex("<footer")
    footer = chrome[foot_start:chrome.index("</footer>", foot_start)
                    + len("</footer>")]
    links = re.findall(r'<link rel="stylesheet" href="css/[0-9a-f]{12}\.css">',
                       chrome)
    tail = chrome[chrome.index("</footer>", foot_start) + len("</footer>"):]
    scripts = re.findall(r"<script(?![^>]*\bsrc=)[^>]*>[\s\S]*?</script>", tail)
    if not scripts:
        sys.exit("pagekit: %s yielded no inline scripts, so the nav panel on "
                 "any page built from it would not open" % donor_filename)
    return head, header, footer, links, scripts


# --------------------------------------------------------------- the sections
def hero(kicker, h1, lede, figs, jumps):
    """The pine hero: kicker, headline, one sentence, four figures, jump nav.

    `figs` is a list of (number, label). Four is the shape the grid was built
    for; three and five both render, five wraps badly under 900px.
    `jumps` is a list of (href, label) and every href must be an id that the
    body actually emits - the builders' guards check that, because a jump nav
    of dead buttons is the kind of thing that ships silently.
    """
    o = ['<section class="pk-hero">']
    o.append('<p class="hk">%s</p>' % kicker)
    o.append("<h1>%s</h1>" % h1)
    o.append('<p class="hl">%s</p>' % lede)
    if figs:
        o.append('<div class="pk-figs">')
        for n, l in figs:
            o.append('<div><span class="n">%s</span>'
                     '<span class="l">%s</span></div>' % (n, l))
        o.append("</div>")
    if jumps:
        o.append('<p class="hj">')
        for href, label in jumps:
            o.append('<a href="#%s">%s</a>' % (href, label))
        o.append("</p>")
    o.append("</section>")
    return "".join(o)


def quote(label, paras):
    """The cream panel that carries the question in the reader's own words."""
    o = ['<div class="pk-q"><p class="ql">%s</p>' % label]
    for p in paras:
        o.append("<p>%s</p>" % p)
    o.append("</div>")
    return "".join(o)


def numbered(items):
    """The numbered verdict stack. `items` is (n, title, html)."""
    o = ['<div class="pk-v">']
    for n, t, p in items:
        o.append('<div><span class="vn">%s</span><span class="vt">%s</span>'
                 "<p>%s</p></div>" % (n, t, p))
    o.append("</div>")
    return "".join(o)


def table(headers, rows, caption=None, minw=560):
    """A bordered table. Each row is a list of cells, or (cells, row-class).

    A cell may be a plain string, or ("text", "class") to get the Fraunces
    figure treatment (`f`) or the mono treatment (`m`).
    """
    o = ['<div class="pk-tw"><table class="pk-t" style="min-width:%dpx">' % minw]
    o.append("<tr>" + "".join("<th>%s</th>" % h for h in headers) + "</tr>")
    for row in rows:
        cls = ""
        if isinstance(row, tuple):
            row, cls = row
        o.append('<tr class="%s">' % cls if cls else "<tr>")
        for c in row:
            if isinstance(c, tuple):
                o.append('<td class="%s">%s</td>' % (c[1], c[0]))
            else:
                o.append("<td>%s</td>" % c)
        o.append("</tr>")
    o.append("</table></div>")
    if caption:
        o.append('<p class="pk-cap">%s</p>' % caption)
    return "".join(o)


def callout(kicker, paras, big=None):
    """The ink panel. One per section at most; it stops working past that."""
    o = ['<div class="pk-call"><h3>%s</h3>' % kicker]
    if big:
        o.append('<span class="big">%s</span>' % big)
    for p in paras:
        o.append("<p>%s</p>" % p)
    o.append("</div>")
    return "".join(o)


def checklist(title, items):
    o = ['<div class="pk-ask"><h3>%s</h3><ul>' % title]
    for i in items:
        o.append("<li>%s</li>" % i)
    o.append("</ul></div>")
    return "".join(o)


def sources(groups, note=None):
    """Numbered, linked sources, grouped. `groups` is (heading, [(text, url)]).

    A source with no URL renders as bold plain text rather than a dead link,
    which is the pattern the rest of the site uses for anything that cannot be
    linked safely. A wrong direct link is worse than no link.
    """
    o = ['<section class="pk-sec" id="sources">']
    o.append('<p class="pk-k">Where every figure came from</p>')
    o.append('<h2 class="pk-h">Sources.</h2>')
    n = 0
    for heading, items in groups:
        o.append('<div class="pk-src"><h3>%s</h3><ol>' % heading)
        for item in items:
            n += 1
            text, url = item[0], item[1]
            if url:
                o.append('<li><a href="%s" rel="nofollow noopener" '
                         'target="_blank">%s</a></li>' % (url, text))
            else:
                o.append("<li><b>%s</b></li>" % text)
        o.append("</ol></div>")
    if note:
        o.append('<p class="pk-fine">%s</p>' % note)
    o.append("</section>")
    return "".join(o), n


# ------------------------------------------------------------------- the CSS
_CSS = """<style>/* _dev/pagekit.py */
.pk-wrap{max-width:1040px;margin:0 auto;padding:0 20px}
.pk-sec{margin:36px 0}
.pk-k{font-family:'IBM Plex Mono',ui-monospace,monospace;font-size:11px;
  letter-spacing:.14em;text-transform:uppercase;color:%(pine)s;margin:0 0 6px}
.pk-h{font-family:'Bricolage Grotesque',system-ui,sans-serif;font-weight:800;
  letter-spacing:-.032em;font-size:27px;line-height:1.12;color:%(ink)s;
  margin:0 0 10px}
.pk-h3{font-family:'Bricolage Grotesque',system-ui,sans-serif;font-weight:800;
  letter-spacing:-.028em;font-size:20px;line-height:1.18;color:%(ink)s;
  margin:30px 0 8px}
.pk-d{font-size:15.4px;line-height:1.68;color:%(muted)s;margin:0 0 16px;
  max-width:68ch}
.pk-d b{color:%(ink)s}
.pk-d i{color:%(ink)s;font-style:italic}
.pk-d a{color:%(pine)s}

/* -------------------------------------------------------------- the hero */
.pk-hero{border:2px solid %(ink)s;border-radius:16px;box-shadow:8px 8px 0 %(ink)s;
  background:%(pine)s;color:#fff;padding:30px 30px 26px;margin:0 0 26px}
.pk-hero .hk{font-family:'IBM Plex Mono',ui-monospace,monospace;font-size:11px;
  letter-spacing:.15em;text-transform:uppercase;color:%(gp)s;margin:0 0 12px}
.pk-hero h1{font-family:'Bricolage Grotesque',system-ui,sans-serif;font-weight:800;
  letter-spacing:-.034em;font-size:41px;line-height:1.03;color:#fff;
  margin:0 0 14px;max-width:20ch}
.pk-hero .hl{font-size:17px;line-height:1.6;color:rgba(255,255,255,.92);
  margin:0 0 18px;max-width:64ch}
.pk-hero .hl b{color:%(gp)s}
.pk-hero .hl a{color:%(gp)s}
.pk-figs{display:grid;grid-template-columns:repeat(auto-fit,minmax(150px,1fr));
  gap:0;border:2px solid %(ink)s;border-radius:12px;overflow:hidden;
  margin:0 0 18px;background:%(ink)s}
.pk-figs>div{background:%(cream)s;padding:14px 15px}
.pk-figs .n{font-family:Fraunces,Georgia,serif;font-weight:600;font-size:29px;
  line-height:1;color:%(ink)s;display:block;letter-spacing:-.02em}
.pk-figs .l{font-family:'IBM Plex Mono',ui-monospace,monospace;font-size:10.5px;
  letter-spacing:.1em;text-transform:uppercase;color:%(pine)s;display:block;
  margin:8px 0 0;line-height:1.5}
.pk-hero .hj{display:flex;flex-wrap:wrap;gap:9px;margin:0}
.pk-hero .hj a{display:inline-block;font-family:'IBM Plex Mono',ui-monospace,
  monospace;font-size:11.5px;letter-spacing:.08em;text-transform:uppercase;
  text-decoration:none;border:2px solid %(ink)s;border-radius:999px;
  padding:8px 14px;background:%(gold)s;color:%(ink)s;box-shadow:3px 3px 0 %(ink)s}
.pk-hero .hj a:hover{transform:translate(1px,1px);box-shadow:2px 2px 0 %(ink)s}

/* ------------------------------------------------------------ the question */
.pk-q{border:2px solid %(ink)s;border-left-width:9px;border-radius:12px;
  background:%(cream)s;padding:19px 21px;margin:0 0 26px;
  box-shadow:4px 4px 0 %(gold)s}
.pk-q .ql{font-family:'IBM Plex Mono',ui-monospace,monospace;font-size:10.5px;
  letter-spacing:.13em;text-transform:uppercase;color:%(pine)s;margin:0 0 10px}
.pk-q p{font-size:15.6px;line-height:1.7;color:#3A3529;margin:0 0 11px;
  max-width:68ch}
.pk-q p:last-child{margin:0}
.pk-q p b{color:%(ink)s}

/* ---------------------------------------------------------------- verdicts */
.pk-v{border:2px solid %(ink)s;border-radius:12px;background:#fff;
  box-shadow:5px 5px 0 %(ink)s;overflow:hidden;margin:0 0 24px}
.pk-v>div{padding:16px 19px;border-bottom:1.5px solid #E6E0D2}
.pk-v>div:last-child{border-bottom:0}
.pk-v .vn{font-family:Fraunces,Georgia,serif;font-weight:600;font-size:26px;
  line-height:1;color:%(pine)s;display:block;margin:0 0 7px;letter-spacing:-.02em}
.pk-v .vt{font-family:'Bricolage Grotesque',system-ui,sans-serif;font-weight:800;
  letter-spacing:-.024em;font-size:17.5px;line-height:1.25;color:%(ink)s;
  display:block;margin:0 0 7px}
.pk-v p{font-size:15px;line-height:1.66;color:%(muted)s;margin:0;max-width:70ch}
.pk-v p b{color:%(ink)s}
.pk-v p a{color:%(pine)s}

/* ------------------------------------------------------------- the tables */
.pk-tw{overflow-x:auto;border:2px solid %(ink)s;border-radius:12px;
  box-shadow:5px 5px 0 %(ink)s;background:#fff;margin:0 0 14px}
.pk-t{border-collapse:collapse;width:100%%}
.pk-t th,.pk-t td{text-align:left;padding:11px 14px;
  border-bottom:1.5px solid #E6E0D2;font-size:14px;line-height:1.55;
  color:#3A3529;vertical-align:top;overflow-wrap:break-word}
.pk-t th{font-family:'IBM Plex Mono',ui-monospace,monospace;font-size:10.5px;
  letter-spacing:.11em;text-transform:uppercase;color:%(pine)s;
  background:%(cream)s;white-space:nowrap}
.pk-t tr:last-child td{border-bottom:0}
.pk-t td.f{font-family:Fraunces,Georgia,serif;font-weight:600;font-size:17px;
  color:%(ink)s;white-space:nowrap}
.pk-t td.m{font-family:'IBM Plex Mono',ui-monospace,monospace;font-size:12.5px;
  color:%(ink)s;white-space:nowrap}
.pk-t td.n{font-family:'IBM Plex Mono',ui-monospace,monospace;font-size:13px;
  color:%(ink)s;white-space:nowrap;text-align:right}
.pk-t tr.bad td{background:#FCF1EF}
.pk-t tr.bad td.f{color:%(red)s}
.pk-t tr.good td{background:#F2F7F4}
.pk-t tr.hi td{background:%(paper)s}
.pk-cap{font-size:13.2px;line-height:1.65;color:%(muted)s;margin:0 0 26px;
  max-width:74ch}
.pk-cap b{color:%(ink)s}
.pk-cap a{color:%(pine)s}

/* ------------------------------------------------------------ the callout */
.pk-call{border:2px solid %(ink)s;border-radius:14px;background:%(ink)s;
  color:#fff;padding:22px 25px;margin:0 0 26px}
.pk-call h3{font-family:'IBM Plex Mono',ui-monospace,monospace;font-size:11px;
  letter-spacing:.15em;text-transform:uppercase;color:%(gold)s;margin:0 0 10px;
  font-weight:400}
.pk-call p{font-size:16.2px;line-height:1.62;color:#fff;margin:0 0 12px;
  max-width:66ch}
.pk-call p:last-child{margin:0}
.pk-call p b{color:%(gold)s}
.pk-call p a{color:%(gold)s}
.pk-call .big{font-family:Fraunces,Georgia,serif;font-weight:600;font-size:34px;
  color:%(gold)s;display:block;line-height:1.1;margin:2px 0 4px}

/* ---------------------------------------------------------- the checklist */
.pk-ask{border:2px solid %(ink)s;border-radius:12px;background:%(paper)s;
  box-shadow:5px 5px 0 %(pine)s;padding:20px 22px;margin:0 0 20px}
.pk-ask h3{font-family:'Bricolage Grotesque',system-ui,sans-serif;font-weight:800;
  letter-spacing:-.026em;font-size:19px;color:%(ink)s;margin:0 0 10px}
.pk-ask ul{margin:0;padding:0 0 0 19px}
.pk-ask li{font-size:15.2px;line-height:1.68;color:%(muted)s;margin:0 0 10px;
  max-width:68ch}
.pk-ask li:last-child{margin:0}
.pk-ask li b{color:%(ink)s}
.pk-ask li a{color:%(pine)s}

/* --------------------------------------------------------- the calculator */
.pk-calc{border:2px solid %(ink)s;border-radius:14px;background:%(cream)s;
  box-shadow:6px 6px 0 %(gold)s;padding:22px 24px;margin:0 0 20px}
.pk-cg{display:grid;grid-template-columns:1fr 1fr;gap:22px;margin:0 0 20px}
.pk-cc h3{font-family:'Bricolage Grotesque',system-ui,sans-serif;font-weight:800;
  letter-spacing:-.026em;font-size:18px;color:%(ink)s;margin:0 0 12px}
.pk-fl{display:block;font-family:'IBM Plex Mono',ui-monospace,monospace;
  font-size:10.5px;letter-spacing:.1em;text-transform:uppercase;color:%(pine)s;
  margin:0 0 5px}
.pk-calc input,.pk-calc select{width:100%%;box-sizing:border-box;
  font-family:'IBM Plex Mono',ui-monospace,monospace;font-size:15px;
  color:%(ink)s;background:#fff;border:2px solid %(ink)s;border-radius:8px;
  padding:9px 11px;margin:0 0 13px}
.pk-calc input:focus,.pk-calc select:focus{outline:3px solid %(gold)s;
  outline-offset:1px}
.pk-out{border:2px solid %(ink)s;border-radius:12px;background:#fff;
  overflow:hidden}
.pk-out .r{display:grid;grid-template-columns:1fr auto;gap:12px;
  padding:12px 16px;border-bottom:1.5px solid #E6E0D2;align-items:baseline}
.pk-out .r:last-child{border-bottom:0}
.pk-out .r.hd{background:%(cream)s}
.pk-out .r.tot{background:%(paper)s}
.pk-out .r.hd span{font-family:'IBM Plex Mono',ui-monospace,monospace;
  font-size:10.5px;letter-spacing:.11em;text-transform:uppercase;color:%(pine)s}
.pk-out .lbl{font-size:14.4px;line-height:1.5;color:#3A3529}
.pk-out .va{font-family:Fraunces,Georgia,serif;font-weight:600;font-size:18px;
  color:%(ink)s;text-align:right;min-width:104px}
.pk-note{font-size:13.2px;line-height:1.65;color:%(muted)s;margin:14px 0 0;
  max-width:72ch}
.pk-note b{color:%(ink)s}
.pk-note a{color:%(pine)s}

/* ------------------------------------------------------------- the sources */
.pk-src{border:2px solid %(ink)s;border-radius:12px;background:#fff;
  padding:20px 22px;margin:0 0 18px;box-shadow:5px 5px 0 %(ink)s}
.pk-src h3{font-family:'IBM Plex Mono',ui-monospace,monospace;font-size:11px;
  letter-spacing:.13em;text-transform:uppercase;color:%(pine)s;margin:0 0 11px;
  font-weight:400}
.pk-src ol{margin:0;padding:0 0 0 20px}
.pk-src li{font-size:14.2px;line-height:1.62;color:%(muted)s;margin:0 0 8px}
.pk-src li:last-child{margin:0}
.pk-src a{color:%(pine)s}

.pk-fine{font-size:13.4px;line-height:1.68;color:%(muted)s;margin:26px 0 0;
  max-width:74ch}
.pk-fine b{color:%(ink)s}
.pk-fine a{color:%(pine)s}

@media (max-width:900px){
  .pk-figs{grid-template-columns:1fr 1fr}
  .pk-hero h1{font-size:32px}
  .pk-cg{grid-template-columns:1fr;gap:8px}
}
@media (max-width:640px){
  .pk-hero{padding:22px 20px 20px}
  .pk-hero h1{font-size:27px;max-width:none}
  .pk-h{font-size:23px}
  .pk-calc{padding:18px 17px}
  .pk-t th,.pk-t td{padding:10px 11px;font-size:13.4px;overflow-wrap:break-word}
  .pk-tw table{min-width:520px}
}
</style>"""


def css():
    """One byte-identical style block per page, so css_dedupe can collapse them."""
    return _CSS % {"ink": INK, "pine": PINE, "gold": GOLD, "paper": PAPER,
                   "cream": CREAM, "muted": MUTED, "red": RED, "gp": GOLD_ON_PINE}


# ------------------------------------------------------------------- assembly
def assemble(head, meta, header, body_html, footer, links, scripts, extra=""):
    return ('<!DOCTYPE html>\n<html lang="en">\n' + head + meta + "</head>\n"
            "<body>" + header + "<main>" + body_html + "</main>" + footer
            + "\n" + "\n".join(links) + "\n" + css()
            + ("\n" + extra if extra else "")
            + "\n" + "\n".join(scripts) + "\n</body>\n</html>\n")


def meta_block(page, title, description, topic, fmt, question, outcome,
               number, weight=5):
    """Head metadata, including the `ts:` fields the library hubs read.

    `ts:stale` is misnamed and it matters. It does not mean "this page has gone
    stale" - mock/library/build_library.py reads it as the flag that PRINTS the
    "Checked <month>" badge on the page's hub card. Setting it false on a page
    built this month is the opposite of what it looks like.
    """
    return ("<title>%s</title>\n"
            '<meta name="description" content="%s" />\n'
            '<link rel="canonical" href="https://therapistsupport.org/%s">\n'
            '<meta name="ts:topic" content="%s">\n'
            '<meta name="ts:format" content="%s">\n'
            '<meta name="ts:question" content="%s">\n'
            '<meta name="ts:outcome" content="%s">\n'
            '<meta name="ts:number" content="%s">\n'
            '<meta name="ts:weight" content="%d">\n'
            '<meta name="ts:stale" content="true">\n'
            % (title, description, page, topic, fmt, question, outcome,
               number, weight))


# --------------------------------------------------------------------- guards
BRITISH = (("license", "se", "ce"), ("labor", "or", "our"),
           ("behavior", "or", "our"), ("defense", "se", "ce"),
           ("offense", "se", "ce"), ("practice", "ice", "ise"),
           ("practicing", "cing", "sing"),
           ("counseling", "el", "ell"), ("traveling", "l", "ll"),
           ("modeling", "l", "ll"), ("labeled", "eled", "elled"),
           ("canceled", "eled", "elled"),
           ("organiz", "z", "s"), ("realize", "ze", "se"),
           ("recogniz", "z", "s"), ("authoriz", "z", "s"),
           ("summariz", "z", "s"),
           # These take the full ending rather than the stem. The stem
           # forms collide with correct American words: the -s stem of
           # "analyze" is inside "analysis", the -s stem of "criticize"
           # is inside "criticism", the -s stem of "realize" is inside
           # "realistic", and the -s stem of "specialize" is inside
           # "specialist". "enrollment" is here for the same reason one line
           # down: the British "enrol" is a substring of "enrolled". A guard that fires on "analysis" gets
           # switched off, which is worse than a guard that misses a word.
           ("analyze", "ze", "se"), ("criticize", "ze", "se"),
           ("emphasize", "ze", "se"), ("apologize", "ze", "se"),
           ("utiliz", "z", "s"), ("specialize", "ze", "se"),
           ("prioritiz", "z", "s"),
           ("judgment", "dgm", "dgem"), ("favor", "or", "our"),
           ("color", "or", "our"), ("center", "er", "re"),
           ("program", "", "me"), ("toward", "", "s"),
           ("while", "e", "st"), ("among", "", "st"),
           ("enrollment", "ll", "l"),
           # "fulfil" is inside the correct American "fulfilling" and
           # "fulfilled", so the bare stem fires on prose that is right.
           # The only forms that actually differ are the bare verb and
           # the noun; the noun is the one that appears in prose.
           ("fulfillment", "ll", "l"))


def spelling(html):
    """British spellings in prose, with the guard immune to its own literals.

    Every wrong spelling below is DERIVED from the right one at run time, so no
    British string exists anywhere in this file. That matters because the first
    version of this guard was written with the British forms as literals, and a
    blanket search-and-replace across `_dev/` then corrected the guard into
    uselessness - it was checking for spellings it no longer contained.

    Script and style bodies are stripped first. A JavaScript identifier is not
    prose, and a guard that fires on `colour` inside a comment teaches whoever
    hits it to stop trusting the guard.
    """
    text = re.sub(r"<(script|style)\b[\s\S]*?</\1>", " ", html, flags=re.I)
    text = re.sub(r"<[^>]+>", " ", text).lower()
    found = []
    for right, cut, paste in BRITISH:
        wrong = right.replace(cut, paste) if cut else right + paste
        if wrong in text:
            found.append(wrong)
    return found


def article(html):
    """Just the part a builder wrote, without the borrowed chrome.

    Guards that run over the whole document find things the builder is not
    responsible for and cannot fix. The first version of the LLC guard on
    `build_unpaid.py` fired on the nav panel's link to the page explaining
    that a California therapist cannot form one - a correct link, on every
    page of the site, reported as a defect. Scope the content guards here.
    """
    i = html.find('<article class="pk-wrap">')
    if i < 0:
        return ""
    j = html.rfind("</article>")
    return html[i:j] if j > i else html[i:]


def check_page(path, must_have, jump_ids):
    """The checks every builder here runs, so none of them can forget one.

    Returns the number of problems, having printed each. The jump-anchor check
    is the one this project keeps relearning: `node --check` passing, or a file
    being written at all, says nothing about whether the element a link points
    at is present. A hero full of dead buttons ships silently.
    """
    bad = 0
    s = open(path, encoding="utf-8").read()

    for what, needle in (("the masthead", "sitenav"),
                         ("the footer", "<footer"),
                         ("a stylesheet link", 'href="css/'),
                         ("the shared style block", "_dev/pagekit.py"),
                         ("exactly one h1", None)):
        if needle is None:
            if s.count("<h1") != 1:
                print("GUARD: %d h1 elements, expected 1" % s.count("<h1"))
                bad += 1
        elif needle not in s:
            print("GUARD: %s is missing from the written page" % what)
            bad += 1

    for what, needle in must_have:
        if needle not in s:
            print("GUARD: %s is missing from the written page" % what)
            bad += 1

    for anchor in jump_ids:
        if 'id="%s"' % anchor not in s:
            print("GUARD: the hero links to #%s and no element has that id"
                  % anchor)
            bad += 1

    art = article(s)
    if not art:
        print("GUARD: the page has no <article class=\"pk-wrap\"> body")
        bad += 1
    for wrong in spelling(art):
        print("GUARD: British spelling %r in the prose" % wrong)
        bad += 1

    # An unclosed section swallows everything after it and still renders.
    for tag in ("section", "div", "table", "article"):
        o = len(re.findall(r"<%s\b" % tag, s))
        c = len(re.findall(r"</%s>" % tag, s))
        if o != c:
            print("GUARD: %d <%s> against %d </%s>" % (o, tag, c, tag))
            bad += 1

    return bad
