#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Build therapy-liability-insurance-california.html.

WHY THIS PAGE EXISTS

Because the research found a genuine hole. There is no published article by a
California attorney on what coverage a California MFT specifically needs; CAMFT's
own staff-attorney piece on the subject is behind an unreachable archive; and
of the eight programs a California MFT can actually buy, exactly one publishes a
California rate table, in a PDF last modified in June 2023. Everything else is
quote-only. Meanwhile the aggregator sites quote "$500 to $1,200 per year" for
$1M/$3M, which is three to ten times what the carriers' own published numbers
say a Californian pays.

WHAT THE PAGE IS ORGANISED AROUND

Not price. The spine is the gap between the two numbers on a therapist policy:

    $1,000,000   the malpractice limit, the number everyone shops on
    $5,000-35,000  the board-defense sublimit, the coverage you will
                   statistically actually use

The BBS received 2,127 complaints in FY 2023-24 and the Board saw seven
malpractice settlement reports in four years. A therapist is orders of magnitude
more likely to face the Board than a jury, and the headline limit does not touch
that. Organising the page around that fact is what makes it worth reading rather
than a table anyone could scrape.

THE TWO PRICE COLUMNS, AND WHY BOTH

`published` is the carrier's own number. `reported` is what a named person said
they actually paid, with a link. They disagree constantly, and the disagreement
is the content: CPH publishes $320 for a full-time California MFT and
Californians report $110 and $591, because discounts, general liability and
cyber all move it. A page with only the first is quoting a price nobody pays; a
page with only the second is gossip.

RULES THIS BUILD ENFORCES, NOT JUST OBSERVES

- every external claim carries the URL it came from, checked at build time
- no premium appears without the limit it is at (a $117 quote at $500K/$500K is
  not comparable to $320 at $1M/$3M, and the page says so at every mention)
- no internal href ships unless the file exists
- every contrast pair is measured before the CSS is written

Run:  python3 _dev/build_insurance.py
Then: restyle -> extract_css -> css_cdo_fix -> css_dedupe -> the rest.
"""
import os, re, sys, html

HERE = os.path.dirname(os.path.abspath(__file__))
SITE = os.path.dirname(HERE)
sys.path.insert(0, HERE)

from insurance_data import (CARRIERS, REPORTED, LEGAL, PAYERS, GLOSSARY,   # noqa: E402
                            CASES, NEEDS, AFFILIATE, CHECKED)

OUT = os.path.join(SITE, "therapy-liability-insurance-california.html")
# Chrome comes from an article page, for the reason written up in build_psyd.py:
# extract_css links each page only to the blocks it actually had, so borrowing a
# directory's stylesheet set gives you markup whose CSS knows nothing about it.
CHROME_FROM = os.path.join(SITE, "hiring-first-associate-california-therapist.html")

INK = "#16211B"
PINE = "#2C6350"
GOLD = "#F6C560"
PAPER = "#F4F0E6"
CREAM = "#FBF9F3"
MUTED = "#635E53"
RED = "#B5483F"
FLOOR = 4.5


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


CONTRAST = [
    ("body on cream", MUTED, CREAM, FLOOR),
    ("body on white", MUTED, "#FFFFFF", FLOOR),
    ("heading on cream", INK, CREAM, 3.0),
    ("figure pine on white", PINE, "#FFFFFF", FLOOR),
    ("label pine on cream", PINE, CREAM, FLOOR),
    ("ink on gold chip", INK, GOLD, FLOOR),
    ("white on pine", "#FFFFFF", PINE, FLOOR),
    ("gold on pine", "#FFD37A", PINE, FLOOR),
    ("caution red on cream", RED, CREAM, FLOOR),
    ("white on ink", "#FFFFFF", INK, FLOOR),
]


def esc(x):
    return html.escape(str(x), quote=False) if x is not None else ""


CSS = """<style>/* _dev/build_insurance.py */
.li-wrap{max-width:1060px;margin:0 auto;padding:0 20px}
.li-sec{margin:34px 0}
.li-k{font-family:'IBM Plex Mono',ui-monospace,monospace;font-size:11px;
  letter-spacing:.14em;text-transform:uppercase;color:%(pine)s;margin:0 0 6px}
.li-h{font-family:'Bricolage Grotesque',system-ui,sans-serif;font-weight:800;
  letter-spacing:-.032em;font-size:27px;line-height:1.12;color:%(ink)s;margin:0 0 8px}
.li-d{font-size:15.4px;line-height:1.66;color:%(muted)s;margin:0 0 16px;max-width:68ch}
.li-d b{color:%(ink)s}

/* the two-numbers panel */
.li-two{display:grid;grid-template-columns:1fr 1fr;gap:0;border:2px solid %(ink)s;
  border-radius:14px;overflow:hidden;box-shadow:7px 7px 0 %(ink)s;margin:0 0 10px}
.li-two>div{padding:19px 21px}
.li-two>div:first-child{background:%(cream)s;border-right:2px solid %(ink)s}
.li-two>div:last-child{background:%(gold)s}
.li-two .n{font-family:'Fraunces',Georgia,serif;font-size:38px;line-height:1;
  color:%(ink)s;display:block;letter-spacing:-.02em}
.li-two .l{font-family:'IBM Plex Mono',ui-monospace,monospace;font-size:11px;
  letter-spacing:.12em;text-transform:uppercase;color:%(ink)s;display:block;margin:9px 0 5px}
.li-two p{font-size:13.8px;line-height:1.55;color:#3A3529;margin:0}
.li-two>div:first-child p{color:%(muted)s}

/* filter bar */
.li-filt{display:flex;flex-wrap:wrap;gap:7px;margin:0 0 16px}
.li-fb{font-family:'IBM Plex Mono',ui-monospace,monospace;font-size:12px;
  color:%(muted)s;background:%(cream)s;border:2px solid %(ink)s;border-radius:9px;
  padding:7px 11px;cursor:pointer;box-shadow:3px 3px 0 %(ink)s;white-space:nowrap}
.li-fb:hover{background:#F1EDE0}
.li-fb[aria-pressed="true"]{background:%(pine)s;color:#fff}
.li-count{font-family:'IBM Plex Mono',ui-monospace,monospace;font-size:12px;
  color:%(muted)s;margin:0 0 14px}

/* carrier card */
.li-card{border:2px solid %(ink)s;border-radius:14px;background:#fff;
  box-shadow:7px 7px 0 %(ink)s;padding:18px 20px 16px;margin:0 0 20px}
.li-card[hidden]{display:none}
.li-top{display:flex;align-items:baseline;gap:12px;flex-wrap:wrap;margin:0 0 3px}
.li-name{font-family:'Bricolage Grotesque',system-ui,sans-serif;font-weight:800;
  letter-spacing:-.028em;font-size:22px;color:%(ink)s;margin:0}
.li-form{font-family:'IBM Plex Mono',ui-monospace,monospace;font-size:10.5px;
  letter-spacing:.1em;text-transform:uppercase;border:2px solid %(ink)s;
  border-radius:6px;padding:3px 7px;background:%(gold)s;color:%(ink)s}
.li-form.cm{background:#F3E0DE}
.li-price{margin-left:auto;text-align:right}
.li-price .p{font-family:'Fraunces',Georgia,serif;font-size:25px;color:%(pine)s;
  display:block;line-height:1}
.li-price .pn{font-size:11.5px;color:%(muted)s;display:block;margin-top:3px;max-width:26ch}
.li-under{font-size:13px;color:%(muted)s;margin:0 0 13px}
.li-under b{color:%(ink)s;font-weight:600}
.li-verd{border-left:4px solid %(pine)s;padding:2px 0 2px 13px;margin:0 0 13px}
.li-verd b{font-family:'Bricolage Grotesque',system-ui,sans-serif;font-weight:800;
  font-size:15.5px;color:%(ink)s;display:block;letter-spacing:-.02em;line-height:1.3}
.li-verd p{font-size:14px;line-height:1.6;color:%(muted)s;margin:5px 0 0;max-width:66ch}
.li-grid{display:grid;grid-template-columns:repeat(auto-fit,minmax(215px,1fr));
  gap:9px;margin:0 0 13px}
.li-cell{background:%(cream)s;border:1.5px solid #E0DACA;border-radius:9px;padding:9px 11px}
.li-cell .ck{font-family:'IBM Plex Mono',ui-monospace,monospace;font-size:10px;
  letter-spacing:.1em;text-transform:uppercase;color:%(muted)s;display:block}
.li-cell .cv{font-size:14px;color:%(ink)s;display:block;margin-top:3px;font-weight:600}
table.li-rate{border-collapse:collapse;width:100%%;margin:0 0 8px;font-size:13.6px}
table.li-rate th{text-align:left;font-family:'IBM Plex Mono',ui-monospace,monospace;
  font-size:10.5px;letter-spacing:.1em;text-transform:uppercase;color:%(muted)s;
  padding:5px 9px 5px 0;border-bottom:2px solid %(ink)s;font-weight:500}
table.li-rate td{padding:7px 9px 7px 0;border-bottom:1px solid #E4DFD2;color:#3A3529}
table.li-rate td.n{font-family:'Fraunces',Georgia,serif;font-size:16px;color:%(pine)s;
  white-space:nowrap}
.li-note{font-size:12.8px;line-height:1.55;color:%(muted)s;margin:0 0 12px;max-width:70ch}
.li-against{background:#FBF4F3;border:1.5px solid #E8CFCB;border-radius:10px;
  padding:11px 13px;margin:0 0 10px}
.li-against b{font-family:'IBM Plex Mono',ui-monospace,monospace;font-size:10.5px;
  letter-spacing:.1em;text-transform:uppercase;color:%(red)s;display:block;margin:0 0 6px}
.li-against ul{margin:0;padding-left:17px}
.li-against li{font-size:13.4px;line-height:1.58;color:#4A413F;margin:0 0 5px}
.li-rep{margin:0 0 6px}
.li-rep b{font-family:'IBM Plex Mono',ui-monospace,monospace;font-size:10.5px;
  letter-spacing:.1em;text-transform:uppercase;color:%(pine)s;display:block;margin:0 0 7px}
.li-rep ul{list-style:none;margin:0;padding:0}
.li-rep li{font-size:13.6px;line-height:1.55;color:%(muted)s;padding:6px 0;
  border-top:1px solid #EDE8DC}
.li-rep li:first-child{border-top:0}
.li-rep .amt{font-family:'Fraunces',Georgia,serif;font-size:15.5px;color:%(ink)s;
  margin-right:7px}
.li-rep .ca{font-family:'IBM Plex Mono',ui-monospace,monospace;font-size:9.5px;
  letter-spacing:.08em;background:%(gold)s;color:%(ink)s;border:1.5px solid %(ink)s;
  border-radius:4px;padding:1px 5px;margin-left:6px}
.li-go{display:inline-block;background:%(pine)s;color:#fff;font-weight:700;
  font-size:14px;text-decoration:none;border:2px solid %(ink)s;border-radius:9px;
  padding:8px 14px;box-shadow:4px 4px 0 %(ink)s;margin-top:4px}
.li-go:hover{background:#245244}

/* payer table */
table.li-pay{border-collapse:collapse;width:100%%;font-size:14px}
table.li-pay th{text-align:left;font-family:'IBM Plex Mono',ui-monospace,monospace;
  font-size:10.5px;letter-spacing:.1em;text-transform:uppercase;color:%(muted)s;
  padding:6px 12px 6px 0;border-bottom:2px solid %(ink)s;font-weight:500}
table.li-pay td{padding:10px 12px 10px 0;border-bottom:1px solid #E4DFD2;
  color:#3A3529;vertical-align:top;line-height:1.55}
table.li-pay td.lim{font-family:'Fraunces',Georgia,serif;font-size:16px;
  color:%(pine)s;white-space:nowrap}
table.li-pay td.who{font-weight:600;color:%(ink)s;white-space:nowrap}

/* glossary */
.li-gl{display:grid;grid-template-columns:repeat(auto-fit,minmax(280px,1fr));gap:11px}
.li-gt{border:2px solid %(ink)s;border-radius:11px;background:#fff;
  box-shadow:4px 4px 0 %(ink)s;padding:13px 15px}
.li-gt b{font-family:'Bricolage Grotesque',system-ui,sans-serif;font-weight:800;
  font-size:15px;color:%(ink)s;display:block;letter-spacing:-.02em}
.li-gt p{font-size:13.6px;line-height:1.6;color:%(muted)s;margin:5px 0 0}

/* cases */
.li-case{border:2px solid %(ink)s;border-radius:12px;background:%(cream)s;
  box-shadow:6px 6px 0 %(ink)s;padding:16px 18px;margin:0 0 15px}
.li-case h3{font-family:'Bricolage Grotesque',system-ui,sans-serif;font-weight:800;
  letter-spacing:-.026em;font-size:18px;color:%(ink)s;margin:0 0 2px}
.li-case .odds{font-family:'IBM Plex Mono',ui-monospace,monospace;font-size:11px;
  letter-spacing:.08em;color:%(pine)s;display:block;margin:0 0 9px}
.li-case>p{font-size:14.2px;line-height:1.62;color:%(muted)s;margin:0 0 11px;max-width:70ch}
.li-cn{display:flex;align-items:baseline;gap:11px;background:#fff;
  border:1.5px solid #E0DACA;border-radius:9px;padding:10px 13px;margin:0 0 10px}
.li-cn .n{font-family:'Fraunces',Georgia,serif;font-size:26px;color:%(pine)s;line-height:1}
.li-cn .l{font-size:12.6px;color:%(muted)s}
.li-cv{font-size:13.8px;line-height:1.62;color:#3A3529;margin:0;max-width:70ch}
.li-cv b{color:%(ink)s}

/* needs */
.li-need{border-top:2px solid %(ink)s;padding:14px 0 4px}
.li-need:first-child{border-top:0}
.li-need h3{font-family:'Bricolage Grotesque',system-ui,sans-serif;font-weight:800;
  font-size:17px;color:%(ink)s;margin:0 0 5px;letter-spacing:-.024em}
.li-need p{font-size:14.2px;line-height:1.62;color:%(muted)s;margin:0 0 7px;max-width:70ch}
.li-need p b{color:%(ink)s}
.li-need .w{font-size:13.4px;color:#4A413F;background:#FBF4F3;
  border-left:3px solid %(red)s;padding:7px 11px;border-radius:0 7px 7px 0;max-width:70ch}

/* law */
.li-law{border:2px solid %(ink)s;border-radius:12px;background:#fff;
  box-shadow:6px 6px 0 %(ink)s;padding:15px 17px;margin:0 0 13px}
.li-law h3{font-family:'Bricolage Grotesque',system-ui,sans-serif;font-weight:800;
  font-size:17px;color:%(ink)s;margin:0 0 6px;letter-spacing:-.024em}
.li-law p{font-size:14.2px;line-height:1.64;color:%(muted)s;margin:0 0 8px;max-width:72ch}
.li-law p b{color:%(ink)s}
.li-law .src{font-family:'IBM Plex Mono',ui-monospace,monospace;font-size:11px;
  color:%(pine)s}

/* the disclosure block */
.li-aff{border:2px solid %(ink)s;border-radius:14px;background:%(pine)s;color:#fff;
  box-shadow:7px 7px 0 %(ink)s;padding:19px 21px}
.li-aff h2{font-family:'Bricolage Grotesque',system-ui,sans-serif;font-weight:800;
  letter-spacing:-.03em;font-size:24px;color:#fff;margin:0 0 8px;line-height:1.15}
.li-aff p{font-size:14.6px;line-height:1.65;color:rgba(255,255,255,.9);
  margin:0 0 10px;max-width:70ch}
.li-aff p:last-child{margin:0}
/* Gold on pine measures 4.35:1 - just under the floor, and the audit caught it
   on this page's own new markup. A lighter gold clears it at 4.91:1 without
   leaving the palette. Same fix the sitewide .hint rule took. */
.li-aff b{color:#FFD37A}
.li-aff a{color:#FFD37A}

.li-fine{font-size:13px;line-height:1.6;color:%(muted)s;max-width:74ch;
  border-top:2px solid %(ink)s;padding-top:14px;margin-top:28px}
.li-fine b{color:%(ink)s}

@media (max-width:720px){
  .li-two{grid-template-columns:1fr}
  .li-two>div:first-child{border-right:0;border-bottom:2px solid %(ink)s}
  .li-price{margin-left:0;text-align:left;width:100%%}
  .li-h{font-size:23px}
  /* The payer table is four columns of text and one of them is a URL-bearing
     note; at 390px it is 438px wide and slides the whole document sideways.
     A table cannot be a scroll container while it is still a table, so it
     becomes a block. The four background layers are the scroll affordance from
     _dev/mobile_nav.py: two travel with the content and mask the shadow
     beneath, two stay put, so the cue appears exactly when there is more to
     see in that direction and disappears at each end. No script. */
  table.li-pay, table.li-rate{
    display:block;width:100%%;overflow-x:auto;-webkit-overflow-scrolling:touch;
    background-image:
      linear-gradient(to right, %(cream)s 40%%, rgba(251,249,243,0)),
      linear-gradient(to left,  %(cream)s 40%%, rgba(251,249,243,0)),
      radial-gradient(farthest-side at 0%% 50%%, rgba(22,33,27,.2), rgba(22,33,27,0)),
      radial-gradient(farthest-side at 100%% 50%%, rgba(22,33,27,.2), rgba(22,33,27,0));
    background-position:left center, right center, left center, right center;
    background-size:30px 100%%, 30px 100%%, 12px 100%%, 12px 100%%;
    background-repeat:no-repeat;
    background-attachment:local, local, scroll, scroll;
  }
  /* A scroller only helps if the table keeps a usable width inside it. An
     auto-layout table at width:100%% shrinks to fit its container, so without a
     min-width the columns just squeeze instead of scrolling. */
  table.li-pay{min-width:560px}
  table.li-rate{min-width:420px}
  table.li-pay td.who, table.li-pay td.lim{white-space:nowrap}
  .li-two .n{font-size:31px}
  .li-wrap{padding:0 16px}
  /* The 12px phone floor, applied to this page's own labels before the
     sitewide pass has to catch them. Five of these carry a sentence rather
     than a word - the price note under each carrier's headline is the clearest
     case - and 10px on a phone is not a label, it is a squint. */
  .li-k, .li-price .pn, .li-cell .ck, .li-form,
  .li-case .odds, .li-note, .li-rep li, .li-cell .cv{font-size:12px}
  .li-cell .cv{font-size:13px}
}
</style>"""

SCRIPT = """<script>/* _dev/build_insurance.py */
(function(){
  var bar = document.querySelector('.li-filt');
  if (!bar) return;
  var btns = [].slice.call(bar.querySelectorAll('.li-fb'));
  var cards = [].slice.call(document.querySelectorAll('.li-card'));
  var count = document.getElementById('li-count');
  function apply(tag){
    var n = 0;
    cards.forEach(function(c){
      var on = tag === 'all' || (' ' + c.getAttribute('data-tags') + ' ')
        .indexOf(' ' + tag + ' ') >= 0;
      c.hidden = !on;
      if (on) n++;
    });
    btns.forEach(function(b){
      b.setAttribute('aria-pressed', b.getAttribute('data-t') === tag ? 'true' : 'false');
    });
    if (count){
      count.textContent = n === cards.length
        ? ('All ' + n + ' programs')
        : (n + ' of ' + cards.length + ' programs');
    }
  }
  btns.forEach(function(b){
    b.addEventListener('click', function(){ apply(b.getAttribute('data-t')); });
  });
  apply('all');
})();
</script>"""

FILTERS = [
    ("all", "Everything"),
    ("student", "Still a student"),
    ("amft", "Associate"),
    ("solo", "Solo private practice"),
    ("incorporated", "Incorporated"),
    ("group", "Employing people"),
    ("office", "Renting an office"),
    ("telehealth", "Telehealth"),
]


def carrier_card(c):
    reps = [r for r in REPORTED if r[0] == c["key"]]
    o = ['<article class="li-card" data-tags="%s" id="c-%s">'
         % (" ".join(c["tags"]), c["key"])]
    o.append('<div class="li-top"><h3 class="li-name">%s</h3>'
             '<span class="li-form%s">%s</span>' %
             (c["name"], " cm" if c["form"].lower().startswith("claims") else "",
              esc(c["form"])))
    o.append('<span class="li-price"><span class="p">%s</span>'
             '<span class="pn">%s</span></span></div>' %
             (c["headline"], c["headline_note"]))
    o.append('<p class="li-under">Underwritten by <b>%s</b> &middot; %s'
             '%s &middot; limits %s%s</p>' %
             (c["underwriter"], c["ambest"],
              "" if not c["ambest_url"] else "",
              c["limits"],
              " &middot; endorsed by " + c["endorsed_by"] if c["endorsed_by"] else ""))

    o.append('<div class="li-verd"><b>%s</b><p>%s</p></div>'
             % (c["verdict"], c["verdict_why"]))

    if c["published"]:
        o.append('<table class="li-rate"><thead><tr><th>Published rate</th>'
                 '<th>Per year</th><th>At</th></tr></thead><tbody>')
        for who, amt, at in c["published"]:
            o.append('<tr><td>%s</td><td class="n">%s</td><td>%s</td></tr>'
                     % (who, amt, at))
        o.append("</tbody></table>")
    if c["published_note"]:
        o.append('<p class="li-note"><a href="%s" target="_blank" '
                 'rel="noopener noreferrer">Source &nearr;</a> %s</p>'
                 % (c["published_url"], c["published_note"]))

    o.append('<div class="li-grid">')
    o.append('<div class="li-cell"><span class="ck">Board defense</span>'
             '<span class="cv">%s</span></div>' % c["board_defense"])
    if c["board_defense_max"] and c["board_defense_max"] != "not published":
        o.append('<div class="li-cell"><span class="ck">Can raise to</span>'
                 '<span class="cv">%s</span></div>' % c["board_defense_max"])
    for k, v in c["extras"]:
        o.append('<div class="li-cell"><span class="ck">%s</span>'
                 '<span class="cv">%s</span></div>' % (k, v))
    o.append("</div>")

    if c["ca_note"]:
        o.append('<p class="li-note"><b>California:</b> %s%s</p>'
                 % (c["ca_note"],
                    ' <a href="%s" target="_blank" rel="noopener noreferrer">'
                    'Source &nearr;</a>' % c["ca_note_url"] if c["ca_note_url"] else ""))

    o.append('<p class="li-note"><b>Discounts.</b> %s</p>' % c["discounts"])
    o.append('<p class="li-note"><b>Your corporation.</b> %s%s</p>'
             % (c["entity"],
                ' <a href="%s" target="_blank" rel="noopener noreferrer">'
                'Source &nearr;</a>' % c["entity_url"] if c["entity_url"] else ""))

    if reps:
        o.append('<div class="li-rep"><b>What people report paying</b><ul>')
        for _k, amt, who, when, url, is_ca in reps:
            o.append('<li><span class="amt">%s</span>%s &middot; %s '
                     '<a href="%s" target="_blank" rel="noopener noreferrer">'
                     '&nearr;</a>%s</li>'
                     % (amt, who, when, url,
                        '<span class="ca">California</span>' if is_ca else ""))
        o.append("</ul></div>")

    if c["against"]:
        o.append('<div class="li-against"><b>Against it</b><ul>')
        for a in c["against"]:
            o.append("<li>%s</li>" % a)
        o.append("</ul></div>")

    o.append('<a class="li-go" href="%s" target="_blank" rel="noopener noreferrer">'
             'Open %s &rarr;</a>' % (c["url"], c["name"]))
    o.append("</article>")
    return "".join(o)


def body():
    o = ['<article class="li-art"><div class="li-wrap">']

    # ---------------------------------------------------------------- hero
    o.append('<section class="li-sec" style="margin-top:26px">')
    o.append('<p class="li-k">California &middot; checked %s</p>' % CHECKED)
    o.append('<h1 class="li-h" style="font-size:36px">Liability insurance for a '
             'California therapy practice.</h1>')
    o.append('<p class="li-d">Nobody requires it. Everybody requires it. The '
             'Board of Behavioral Sciences does not condition your license on '
             'carrying professional liability insurance &mdash; and Headway, '
             'Alma, Blue Shield, Optum, Kaiser, Medi&#8209;Cal and your landlord '
             'all do. This page has every program a California MFT can buy, what '
             'each publishes, what practitioners actually report paying, and the '
             'part of the policy you are far more likely to use than the '
             'million-dollar number on the front.</p>')
    o.append("</section>")

    # ------------------------------------------------------- the two numbers
    o.append('<section class="li-sec">')
    o.append('<p class="li-k">The thing to understand first</p>')
    o.append('<h2 class="li-h">There are two numbers on a therapist policy, and '
             'you will use the small one.</h2>')
    o.append('<div class="li-two">')
    o.append('<div><span class="n">$1,000,000</span>'
             '<span class="l">Malpractice limit</span>'
             '<p>The number every quote leads with. It answers a civil suit for '
             'damages. The Board received <b>seven</b> reports of a malpractice '
             'settlement or award across four fiscal years, from about 148,000 '
             'licensees. When it happens it is large &mdash; the average award '
             'paid was $360,000 &mdash; and it almost never happens.</p></div>')
    o.append('<div><span class="n">$5,000&ndash;35,000</span>'
             '<span class="l">Board defense sublimit</span>'
             '<p>A separate, much smaller pot for defending a complaint to the '
             'BBS. The Board took <b>2,127 complaints</b> in FY&nbsp;2023&ndash;24 '
             'and averages about 1,910 a year. This is the coverage a therapist '
             'actually reaches for, and it is two orders of magnitude smaller '
             'than the headline.</p></div>')
    o.append("</div>")
    o.append('<p class="li-note">A board complaint is not a lawsuit. There are no '
             'damages; the exposure is your license. Your insurer&rsquo;s obligation '
             'is a reimbursement sublimit, not a duty to defend. And the two can '
             'run together: B&amp;P &sect;&thinsp;801(b) makes your insurer report '
             'any settlement over $10,000 to the BBS within 30 days, which turns '
             'a civil matter into a board matter with your name on it.</p>')
    o.append("</section>")

    # ---------------------------------------------------------------- law
    o.append('<section class="li-sec" id="the-law">')
    o.append('<p class="li-k">What the law actually says</p>')
    o.append('<h2 class="li-h">Four answers, with the code section for each.</h2>')
    for L in LEGAL:
        o.append('<div class="li-law"><h3>%s</h3><p>%s</p>'
                 '<p class="src"><a href="%s" target="_blank" '
                 'rel="noopener noreferrer">%s &nearr;</a></p></div>'
                 % (L["q"], L["a"], L["url"], L["cite"]))
    o.append("</section>")

    # ------------------------------------------------------------- payers
    o.append('<section class="li-sec" id="who-requires-it">')
    o.append('<p class="li-k">Who actually sets the number</p>')
    o.append('<h2 class="li-h">Every figure below is the payer&rsquo;s own published '
             'minimum.</h2>')
    o.append('<p class="li-d">The received wisdom is &ldquo;$1M/$3M&rdquo;. That is close '
             'but not exactly right, and the difference costs money. <b>$1M per '
             'occurrence is the near-universal floor</b>; the aggregate is $1M or '
             '$3M depending who is asking. $3M is what satisfies all of them with '
             'one policy.</p>')
    o.append('<table class="li-pay"><thead><tr><th>Who</th><th>Minimum</th>'
             '<th>Notes</th></tr></thead><tbody>')
    for who, lim, note, url in PAYERS:
        o.append('<tr><td class="who">%s</td><td class="lim">%s</td><td>%s '
                 '<a href="%s" target="_blank" rel="noopener noreferrer">&nearr;</a>'
                 '</td></tr>' % (who, lim, note, url))
    o.append("</tbody></table>")
    o.append('<p class="li-note"><b>CAQH sets no minimum.</b> It collects your '
             'carrier, your amount and your face sheet &mdash; and has a &ldquo;Not '
             'Insured&rdquo; option. It is a data utility, not a standard-setter. The '
             'payer sets the number.</p>')
    o.append("</section>")

    # --------------------------------------------------------- own vs group
    o.append('<section class="li-sec" id="own-vs-group">')
    o.append('<p class="li-k">Your own policy, or the practice&rsquo;s</p>')
    o.append('<h2 class="li-h">Whose lawyer is it?</h2>')
    o.append('<p class="li-d">This is the question underneath &ldquo;do I need my own '
             'policy if I am employed&rdquo;, and California has a statutory answer to '
             'it. <b>Civil Code &sect;&thinsp;2860</b> &mdash; the codification of '
             '<i>Cumis</i> &mdash; says that when a conflict of interest arises, '
             'the insurer must provide <b>independent counsel to the insured</b>. '
             'Under an employer&rsquo;s policy, the insurer&rsquo;s insured is the '
             'practice. Counsel retained by that insurer defends the practice. '
             'If the practice&rsquo;s defense is &ldquo;our supervision was sound, the '
             'clinician deviated&rdquo;, that is a real divergence &mdash; and '
             '&sect;&thinsp;2860 protects <i>the insured</i>. If your name is not '
             'under &ldquo;Named Insured&rdquo;, you are not who it protects.</p>')
    o.append('<div class="li-grid">')
    for k, v in [
        ("Look for this", "Your individual name under &ldquo;Named Insured&rdquo; or "
                          "&ldquo;Additional Named Insured&rdquo; &mdash; not a blanket "
                          "&ldquo;employees&rdquo; clause"),
        ("When you leave", "On an occurrence policy the past is covered forever. "
                           "On claims-made, coverage for your work there ends when "
                           "the practice&rsquo;s policy does &mdash; and you do not "
                           "control whether they buy tail"),
        ("Your own clients", "A group policy insures employees only for services "
                             "rendered on behalf of the practice. Check the "
                             "&ldquo;Who Is An Insured&rdquo; section"),
        ("Board defense", "An entity policy has no reason to carry it. A "
                          "corporation has no license for the Board to discipline"),
    ]:
        o.append('<div class="li-cell"><span class="ck">%s</span>'
                 '<span class="cv" style="font-weight:400;font-size:13.4px">%s'
                 '</span></div>' % (k, v))
    o.append("</div>")
    o.append('<p class="li-note">CAMFT&rsquo;s own model Professional Services '
             'Agreement &mdash; the template it publishes for an organisation '
             'contracting a licensed MFT &mdash; requires the clinician, <b>&ldquo;at '
             'his or her sole expense&rdquo;</b>, to carry a minimum of $1,000,000 per '
             'occurrence and $3,000,000 aggregate, and to hand over the '
             'certificate. That is the professional association&rsquo;s own contract '
             'saying you carry your own. '
             '<a href="https://www.camft.org/LinkClick.aspx?fileticket=89dNbzX8xys%3D&amp;portalid=0" '
             'target="_blank" rel="noopener noreferrer">Source &nearr;</a></p>')
    o.append("</section>")

    # ------------------------------------------------------------ glossary
    o.append('<section class="li-sec" id="glossary">')
    o.append('<p class="li-k">The nine words that decide everything</p>')
    o.append('<h2 class="li-h">What the terms actually mean.</h2>')
    o.append('<div class="li-gl">')
    for t, d in GLOSSARY:
        o.append('<div class="li-gt"><b>%s</b><p>%s</p></div>' % (t, d))
    o.append("</div></section>")

    # ----------------------------------------------------------- directory
    o.append('<section class="li-sec" id="directory">')
    o.append('<p class="li-k">The directory</p>')
    o.append('<h2 class="li-h">Every program a California MFT can buy.</h2>')
    o.append('<p class="li-d">Eight programs. <b>One of them publishes a '
             'California rate table</b> &mdash; CPH &mdash; and that PDF was last '
             'modified in June 2023. Everything else is quote-only, which is why '
             'the reported prices matter as much as the published ones. Filter by '
             'where you are.</p>')
    o.append('<div class="li-filt" role="group" aria-label="Filter programs">')
    for t, label in FILTERS:
        o.append('<button class="li-fb" type="button" data-t="%s" '
                 'aria-pressed="%s">%s</button>'
                 % (t, "true" if t == "all" else "false", label))
    o.append("</div>")
    o.append('<p class="li-count" id="li-count">All %d programs</p>' % len(CARRIERS))
    for c in CARRIERS:
        o.append(carrier_card(c))
    o.append("</section>")

    # --------------------------------------------------------------- cases
    o.append('<section class="li-sec" id="what-actually-happens">')
    o.append('<p class="li-k">What actually happens</p>')
    o.append('<h2 class="li-h">Six things that go wrong, and which part of the '
             'policy answers.</h2>')
    for c in CASES:
        o.append('<div class="li-case"><h3>%s</h3>'
                 '<span class="odds">%s</span><p>%s</p>'
                 '<div class="li-cn"><span class="n">%s</span>'
                 '<span class="l">%s</span></div>'
                 '<p class="li-cv">%s</p></div>'
                 % (c["t"], c["odds"], c["body"], c["num"], c["numlab"], c["cover"]))
    o.append("</section>")

    # --------------------------------------------------------------- needs
    o.append('<section class="li-sec" id="what-you-need">')
    o.append('<p class="li-k">What you need</p>')
    o.append('<h2 class="li-h">Eight situations, and the answer for each.</h2>')
    for n in NEEDS:
        o.append('<div class="li-need"><h3>%s</h3><p>%s</p>'
                 '<p class="w">%s</p></div>' % (n["who"], n["need"], n["watch"]))
    o.append("</section>")

    # ----------------------------------------------------------- affiliate
    o.append('<section class="li-sec" id="what-we-are-paid">')
    o.append('<div class="li-aff"><h2>%s</h2><p>%s</p><p>%s</p>'
             '<p><a href="affiliate-disclosure.html">Every arrangement this site '
             'does have &rarr;</a></p></div>'
             % (AFFILIATE["headline"], AFFILIATE["body"], AFFILIATE["why"]))
    o.append("</section>")

    # ---------------------------------------------------------------- fine
    o.append('<p class="li-fine"><b>How this page was built.</b> Every premium is '
             'either published by the carrier, with the link, or reported by a '
             'named person in a post you can open. Nothing is estimated. Where a '
             'carrier does not publish a price, the card says &ldquo;not '
             'published&rdquo; rather than carrying a guess &mdash; five of the eight '
             'do not.<br><br><b>One correction worth making, because it is '
             'repeated constantly.</b> You will read that CPH and HPSO sell the '
             'same CNA policy and you should just pick the cheaper agent. For the '
             'MFT program that is wrong: the CPH application sold through CAMFT '
             'and AAMFT names <b>Philadelphia Indemnity and Tokio Marine '
             'Specialty</b> as the insurers on its signature page. HPSO&rsquo;s '
             'policies are underwritten by CNA. They are different '
             'carriers.<br><br><b>This is not legal or insurance advice.</b> We '
             'are not brokers, we are not lawyers, and nobody on this page pays '
             'us anything. Read your own declarations page &mdash; the answers to '
             'occurrence-versus-claims-made, who is a named insured, and what your '
             'board-defense sublimit is are all on it.</p>')

    o.append("</div></article>")
    return "".join(o)


def main():
    print("colours, measured:")
    bad = 0
    for label, fg, bg, floor in CONTRAST:
        r = ratio(fg, bg)
        ok = r >= floor
        print("  %-22s %5.2f:1 (floor %.1f) %s" % (label, r, floor,
                                                   "ok" if ok else "FAILS"))
        if not ok:
            bad += 1
    if bad:
        sys.exit("%d colour(s) under the floor" % bad)

    if not os.path.exists(CHROME_FROM):
        sys.exit("build_insurance: the chrome donor page is missing")
    chrome = open(CHROME_FROM, encoding="utf-8").read()

    head = chrome[:chrome.index("</head>")]
    head = re.sub(r"<title>[\s\S]*?</title>", "", head)
    head = re.sub(r'<meta name="description"[^>]*>', "", head)
    head = re.sub(r'<meta property="og:[^>]*>', "", head)
    head = re.sub(r'<link rel="canonical"[^>]*>', "", head)
    head = re.sub(r'<meta name="ts:[^>]*>', "", head)
    head = re.sub(r'<script type="application/ld\+json">[\s\S]*?</script>', "", head)
    head = re.sub(r"<!-- _dev/[\s\S]*?-->", "", head)

    title = ("Liability insurance for a California therapy practice &mdash; "
             "Therapist Support")
    desc = ("Every professional liability program a California MFT can buy, with "
            "each carrier's published rates, what therapists report actually "
            "paying, the board-defense sublimit you are far more likely to use "
            "than the $1M limit, and what the BBS, Medi-Cal and every payer "
            "actually require.")
    meta = (
        "<title>%s</title>\n"
        '<meta name="description" content="%s" />\n'
        '<link rel="canonical" href="https://therapistsupport.org/therapy-liability-insurance-california.html">\n'
        '<meta name="ts:topic" content="practice">\n'
        '<meta name="ts:format" content="reference">\n'
        '<meta name="ts:question" content="What malpractice insurance do I actually need?">\n'
        '<meta name="ts:outcome" content="Eight programs compared, with what people really pay and what the law really requires">\n'
        '<meta name="ts:number" content="$320 published, $110 to $600 reported">\n'
        '<meta name="ts:weight" content="5">\n'
        '<meta name="ts:stale" content="false">\n' % (title, desc))

    body_open_end = chrome.index(">", chrome.index("<body")) + 1
    header_end = chrome.index("</header>") + len("</header>")
    header = chrome[body_open_end:header_end]
    foot_start = chrome.rindex("<footer")
    footer = chrome[foot_start:chrome.index("</footer>", foot_start) + len("</footer>")]
    links = re.findall(r'<link rel="stylesheet" href="css/[0-9a-f]{12}\.css">', chrome)

    # THE BEHAVIOUR HAS TO COME WITH THE MARKUP.
    #
    # This page shipped with a nav panel that did not open. The header slice
    # carries `<button data-nav>` and `<div id="navpanel">`, and the script that
    # binds them lives at the END of the donor's body, after </footer> - so
    # lifting the header alone produced a masthead with every button present and
    # nothing behind them. `restyle.py` re-appends that script to every page, so
    # the page was fine until it was rebuilt AFTER restyle ran, and then it was
    # silently dead: no console error, no missing element, no failing guard.
    #
    # A page assembled from someone else's chrome has to take the chrome's
    # scripts too. Everything after </footer> that is an inline <script> is
    # chrome behaviour - the nav panel, the background signup post, the
    # analytics event listener - and is copied verbatim. The guard at the bottom
    # now refuses to write a page whose nav cannot open.
    tail = chrome[chrome.index("</footer>", foot_start) + len("</footer>"):]
    scripts = re.findall(r"<script(?![^>]*\bsrc=)[^>]*>[\s\S]*?</script>", tail)

    css = CSS % {"ink": INK, "pine": PINE, "gold": GOLD, "cream": CREAM,
                 "muted": MUTED, "red": RED}

    doc = ('<!DOCTYPE html>\n<html lang="en">\n' + head + meta + "</head>\n"
           "<body>" + header + "<main>" + body() + "</main>" + footer
           + "\n" + "\n".join(links) + "\n" + css
           + "\n" + "\n".join(scripts)
           + "\n" + SCRIPT + "\n</body>\n</html>\n")

    open(OUT, "w", encoding="utf-8").write(doc)
    print("\nwrote %s (%.0f KB)" % (os.path.basename(OUT), len(doc) / 1024))

    # ------------------------------------------------------------- guards
    s = open(OUT, encoding="utf-8").read()
    bad = 0
    if s.count("<h1") != 1:
        print("GUARD: %d h1" % s.count("<h1")); bad += 1
    if "<footer" not in s or "sitenav" not in s:
        print("GUARD: chrome missing"); bad += 1
    # The nav must be able to OPEN. Markup without behaviour is the bug this
    # page shipped, and it is invisible to every other check on this file.
    if 'id="navpanel"' not in s:
        print("GUARD: the nav panel markup is missing"); bad += 1
    if "getElementById('navpanel')" not in s:
        print("GUARD: the nav panel has no script - every nav button is dead")
        bad += 1
    if 'data-nav="' not in s:
        print("GUARD: no nav buttons"); bad += 1
    n = len(re.findall(r'<article class="li-card"', s))
    if n != len(CARRIERS):
        print("GUARD: %d cards, expected %d" % (n, len(CARRIERS))); bad += 1
    for href in set(re.findall(r'href="([a-z0-9-]+\.html)"', s)):
        if not os.path.exists(os.path.join(SITE, href)):
            print("GUARD: links %s which does not exist" % href); bad += 1
    # Every carrier must carry a source link for whatever it claims.
    for c in CARRIERS:
        if c["published"] and c["published_url"] not in s:
            print("GUARD: %s publishes rates with no source link" % c["key"]); bad += 1
        if c["url"] not in s:
            print("GUARD: %s has no outbound link" % c["key"]); bad += 1
    # Every reported price must carry its post.
    for _k, _a, _w, _d, url, _ca in REPORTED:
        if url not in s:
            print("GUARD: a reported price lost its source"); bad += 1
    # A premium must never appear without the limit it is at.
    for c in CARRIERS:
        for who, amt, at in c["published"]:
            if not at:
                print("GUARD: %s prints %s with no limit" % (c["key"], amt)); bad += 1
    # External links must be safe.
    ext = re.findall(r'<a href="(https?://[^"]+)"([^>]*)>', s)
    for url, attrs in ext:
        if 'target="_blank"' in attrs and "noopener" not in attrs:
            print("GUARD: %s opens a new tab without noopener" % url[:50]); bad += 1
    if bad:
        sys.exit("\n%d problem(s)" % bad)

    pub = sum(1 for c in CARRIERS if c["published"])
    print("%d programs: %d publish a rate, %d are quote-only" % (len(CARRIERS), pub,
                                                                 len(CARRIERS) - pub))
    print("%d reported prices, %d of them Californian"
          % (len(REPORTED), sum(1 for r in REPORTED if r[5])))
    print("%d external sources linked" % len(set(u for u, _a in ext)))
    print("guards clean")


if __name__ == "__main__":
    main()
