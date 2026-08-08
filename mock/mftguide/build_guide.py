#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Build become-an-mft-california.html.

The reference page for anyone considering the MFT track in California: what
the Board actually requires, in what order, at what cost, and the specific
places the requirement is not what people assume it is.

Two design commitments.

FIGURES ARE DRAWN, NOT LISTED. The 3,000 hours are not a sentence saying
"3,000 hours"; they are a bar with 1,750 and 1,250 in proportion and the 500
relational hours drawn *inside* the 1,750, because that inside-ness is the
thing people get wrong. Same for the pre/post-degree split. A reader should be
able to see the shape of the requirement before reading a word of it.

EVERY NUMBER CARRIES ITS SECTION. Not a footnote marker resolving to a list at
the bottom - the actual section number, inline, next to the figure. This page
is about a regulator's rules; a figure without its rule is a rumour. Where the
Board publishes nothing, the page says so in its own section rather than
quietly omitting the question.

Chrome is lifted from the published resources.html at build time so the nav
cannot drift out of sync.
"""
import os, re, sys, html

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import content as C

SRC = os.path.join(HERE, "_chrome.html")
OUT = os.path.join(HERE, "become-an-mft-california.html")
UPDATED = "6 August 2026"


def balanced(s, tag):
    i = s.find("<" + tag)
    if i < 0:
        return None
    d = 0
    for m in re.finditer(r"<%s\b|</%s>" % (tag, tag), s[i:]):
        d += 1 if m.group(0).startswith("<" + tag) else -1
        if d == 0:
            return (i, i + m.end())
    return None


src = open(SRC, encoding="utf-8").read()
head_end = src.find("</head>")
links = [m.group(0) for m in re.finditer(r"<link\b[^>]*>", src[:head_end])
         if 'rel="stylesheet"' in m.group(0) or "fonts." in m.group(0)
         or 'rel="preconnect"' in m.group(0)]
# every <style>, not just the ones in <head> - several _dev passes append
# theirs before </body>, and a head-only lift silently drops them
styles = re.findall(r"<style>.*?</style>", src, re.S)
assert styles, "no stylesheet lifted from the chrome"
hs = balanced(src, "header")
header = re.sub(r'(<a href="[^"]*") class="on"', r"\1", src[hs[0]:hs[1]])
fs = balanced(src, "footer")
footer = re.sub(r'(<a href="[^"]*") class="on"', r"\1", src[fs[0]:fs[1]])


def cite(t):
    """A statute reference, rendered as one."""
    return '<span class="cx">%s</span>' % t


CSS = """<style>/* mft guide */
.mg{--pine:#2C6350;--deep:#1B4536;--amber:#F6C560;--ink:#17271F;--line:#E2DACA;
  --paper:#FBF7EE;--mut:#7C8878}
.mg .cx{font-family:'IBM Plex Mono',ui-monospace,monospace;font-size:10.6px;
  letter-spacing:.03em;color:var(--mut);white-space:nowrap}
.mgband{background:linear-gradient(135deg,#14261E 0%,#1B4536 48%,#2C6350 100%);
  color:#EFF5F2;padding:30px 0 36px}
.mgband .in{max-width:1180px;margin:0 auto;padding:0 26px;display:grid;
  grid-template-columns:minmax(0,1.3fr) minmax(250px,.7fr);gap:34px;align-items:center}
.mgband .bcr{display:flex;flex-wrap:wrap;align-items:center;gap:4px 8px;margin:0 0 14px;
  padding:0;list-style:none;font-family:'IBM Plex Mono',ui-monospace,monospace;
  font-size:10.4px;letter-spacing:.1em;text-transform:uppercase}
.mgband .bcr li{display:flex;align-items:center;gap:8px}
.mgband .bcr a{color:#EFF5F2;opacity:.66;text-decoration:none;padding:5px 0;min-height:26px;
  display:inline-flex;align-items:center;border-bottom:1px solid transparent}
.mgband .bcr a:hover{opacity:1;border-bottom-color:currentColor}
.mgband .bcr .sep{opacity:.36}
.mgband .bcr [aria-current]{opacity:.95;font-weight:600;color:var(--amber)}
.mgband h1{font-family:Fraunces,Georgia,serif;font-size:clamp(27px,3.7vw,43px);
  line-height:1.06;font-weight:600;letter-spacing:-.022em;color:#fff;margin:0 0 14px;max-width:18ch}
.mgband h1 em{font-style:normal;color:var(--amber)}
.mgband .dek{font-size:15.4px;line-height:1.72;color:rgba(255,255,255,.87);margin:0;max-width:56ch}
.mgmeta{display:flex;gap:14px;flex-wrap:wrap;margin-top:17px;
  font-family:'IBM Plex Mono',monospace;font-size:10.4px;letter-spacing:.06em;
  text-transform:uppercase;color:rgba(255,255,255,.62)}
.mgfig{background:rgba(0,0,0,.26);border:1px solid rgba(255,255,255,.18);border-radius:16px;
  padding:20px 22px;min-width:0}
.mgfig b{display:block;font-family:Fraunces,Georgia,serif;font-size:clamp(31px,4.2vw,46px);
  line-height:1;color:var(--amber)}
.mgfig span{display:block;font-size:12.5px;line-height:1.55;color:rgba(255,255,255,.74);margin-top:9px}
.mgfig .row{display:flex;justify-content:space-between;gap:10px;padding:8px 0;
  border-top:1px solid rgba(255,255,255,.14);font-size:12.2px;color:rgba(255,255,255,.8)}
.mgfig .row:first-of-type{margin-top:16px}
.mgfig .row b{display:inline;font-size:12.6px;font-family:inherit;color:#fff}

.mgwrap{max-width:1180px;margin:0 auto;padding:34px 26px 20px;display:grid;
  grid-template-columns:214px minmax(0,1fr);gap:40px;align-items:start}
.mgnav{position:sticky;top:16px;min-width:0}
.mgnav b{display:block;font-family:'IBM Plex Mono',monospace;font-size:10px;
  letter-spacing:.13em;text-transform:uppercase;color:var(--mut);margin-bottom:11px}
.mgnav a{display:block;font-size:13.1px;line-height:1.42;color:#4A5A46;text-decoration:none;
  padding:6px 0 6px 12px;border-left:2px solid var(--line)}
.mgnav a:hover{color:var(--ink);border-left-color:#B9AE93}
.mgnav a.on{color:var(--pine);border-left-color:var(--pine);font-weight:600}
.mgbody{min-width:0}
.mgbody h2{font-family:Fraunces,Georgia,serif;font-size:clamp(21px,2.5vw,27px);
  line-height:1.2;font-weight:600;letter-spacing:-.016em;color:var(--ink);
  margin:44px 0 14px;scroll-margin-top:20px}
.mgbody h2:first-child{margin-top:0}
.mgbody h3{font-family:Fraunces,Georgia,serif;font-size:17.5px;margin:26px 0 9px;color:var(--ink)}
.mgbody p{font-size:15.4px;line-height:1.78;color:#3B4A38;margin:0 0 15px;max-width:68ch}
.mgbody p b{color:var(--ink)}
.mgbody a{color:var(--pine)}

/* the five gates */
.gates{display:grid;gap:9px;margin:6px 0 22px}
.gate{display:grid;grid-template-columns:44px minmax(0,1fr);gap:14px;background:#fff;
  border:1px solid var(--line);border-left:3px solid var(--pine);border-radius:10px;
  padding:14px 16px;min-width:0}
.gate .n{font-family:'IBM Plex Mono',monospace;font-size:15px;color:var(--amber);
  font-weight:600;padding-top:2px}
.gate h4{font-family:Fraunces,Georgia,serif;font-size:16.5px;margin:0 0 4px;color:var(--ink)}
.gate p{font-size:13.7px;line-height:1.6;color:#4A5A46;margin:0 0 5px;max-width:none}
.gate em{font-style:normal;border-bottom:2px solid var(--amber)}

/* the hours bar */
.hbar{margin:8px 0 6px}
.hstack{display:flex;height:74px;border-radius:10px;overflow:hidden;border:1px solid var(--line)}
.hseg{position:relative;display:flex;flex-direction:column;justify-content:center;
  padding:0 16px;min-width:0;color:#fff}
.hseg.a{background:linear-gradient(150deg,#2C6350,#1F4C3C)}
.hseg.b{background:#EDE7D8;color:#3B4A38}
.hseg b{font-family:Fraunces,Georgia,serif;font-size:22px;line-height:1}
.hseg span{font-size:11.5px;line-height:1.35;margin-top:4px;opacity:.9}
.hsub{display:flex;margin-top:7px}
.hsub .in500{background:var(--amber);color:#3A2A08;border-radius:8px;padding:9px 14px;
  min-width:0}
.hsub .in500 b{font-family:Fraunces,Georgia,serif;font-size:17px}
.hsub .in500 span{font-size:11.4px;display:block;margin-top:2px}
.hnote{font-size:13.2px;line-height:1.65;color:#4A5A46;margin:12px 0 0;max-width:68ch}
.hnote .cx{display:inline}

/* split bars */
.split{display:grid;gap:10px;margin:14px 0 6px}
.sp{background:#fff;border:1px solid var(--line);border-radius:10px;padding:13px 15px;min-width:0}
.sp .top{display:flex;justify-content:space-between;align-items:baseline;gap:12px}
.sp h4{font-family:Fraunces,Georgia,serif;font-size:15.5px;margin:0;color:var(--ink)}
.sp .v{font-family:Fraunces,Georgia,serif;font-size:21px;color:var(--pine)}
.sp .track{height:9px;border-radius:6px;background:#EDE7D8;margin:9px 0 8px;overflow:hidden}
.sp .fill{height:100%;background:linear-gradient(90deg,#2C6350,#3F9577)}
.sp .fill.cap{background:linear-gradient(90deg,#B5843F,#D8AC63)}
.sp p{font-size:12.9px;line-height:1.6;color:#4A5A46;margin:0;max-width:none}
.tagcap,.tagfloor{font-family:'IBM Plex Mono',monospace;font-size:9.6px;letter-spacing:.09em;
  text-transform:uppercase;padding:2px 7px;border-radius:20px}
.tagcap{background:#FBF0E2;color:#8A5B22}
.tagfloor{background:#E7F0DC;color:#27500A}

/* rule grid */
.rules{display:grid;grid-template-columns:repeat(auto-fit,minmax(215px,1fr));gap:10px;margin:8px 0 6px}
.rule{background:#fff;border:1px solid var(--line);border-radius:10px;padding:14px 15px;min-width:0}
.rule b{display:block;font-family:Fraunces,Georgia,serif;font-size:27px;line-height:1;color:var(--pine)}
.rule i{display:block;font-style:normal;font-size:12.4px;font-weight:600;color:var(--ink);margin:5px 0 6px}
.rule p{font-size:12.5px;line-height:1.55;color:#4A5A46;margin:0 0 6px;max-width:none}

/* exams */
.ex{background:#fff;border:1px solid var(--line);border-radius:10px;padding:16px 17px;
  margin-bottom:10px;min-width:0}
.ex h4{font-family:Fraunces,Georgia,serif;font-size:17px;margin:0 0 3px;color:var(--ink)}
.ex .len{font-family:'IBM Plex Mono',monospace;font-size:10.6px;color:var(--mut);
  letter-spacing:.05em;text-transform:uppercase}
.ex p{font-size:13.3px;line-height:1.62;color:#4A5A46;margin:9px 0 12px;max-width:none}
.pr{display:grid;gap:9px}
.prow{display:grid;grid-template-columns:118px minmax(0,1fr) 50px;gap:11px;align-items:center;
  font-size:12.6px}
.prow .lab{color:#4A5A46}
.prow .tr{height:15px;border-radius:5px;background:#EDE7D8;overflow:hidden}
.prow .fi{height:100%;background:linear-gradient(90deg,#2C6350,#3F9577)}
.prow .pc{font-family:Fraunces,Georgia,serif;font-size:16px;color:var(--pine);text-align:right}

/* fees */
.tw{overflow-x:auto;-webkit-overflow-scrolling:touch;margin:8px 0 6px}
table.fee{border-collapse:collapse;width:100%;font-size:13.6px;min-width:520px}
table.fee th{text-align:left;font-family:'IBM Plex Mono',monospace;font-size:10px;
  letter-spacing:.1em;text-transform:uppercase;color:var(--mut);padding:0 12px 8px 0;
  border-bottom:1px solid var(--line);font-weight:500}
table.fee td{padding:10px 12px 10px 0;border-bottom:1px solid #F0EBDE;vertical-align:top;color:#3B4A38}
table.fee td.was{color:#9A9280;text-decoration:line-through}
table.fee td.now{font-family:Fraunces,Georgia,serif;font-size:17px;color:var(--pine)}
table.fee tr.tot td{border-bottom:0;padding-top:13px;font-weight:600;color:var(--ink)}
table.fee tr.tot td.now{font-size:20px}

/* traps */
.traps{display:grid;gap:9px;margin:8px 0 6px;counter-reset:tp}
.trap{background:#fff;border:1px solid var(--line);border-left:3px solid #B5483F;
  border-radius:10px;padding:14px 16px;min-width:0}
.trap h4{font-family:Fraunces,Georgia,serif;font-size:16px;margin:0 0 5px;color:var(--ink)}
.trap p{font-size:13.5px;line-height:1.62;color:#4A5A46;margin:0 0 6px;max-width:none}

/* processing */
.proc{display:grid;grid-template-columns:repeat(auto-fit,minmax(250px,1fr));gap:10px;margin:8px 0}
.pc2{background:#fff;border:1px solid var(--line);border-radius:10px;padding:15px 16px;min-width:0}
.pc2 h4{font-family:Fraunces,Georgia,serif;font-size:15.5px;margin:0 0 10px;color:var(--ink)}
.pc2 .bar{display:flex;align-items:center;gap:9px;margin-bottom:7px;font-size:12.4px}
.pc2 .bar span:first-child{width:62px;color:#4A5A46}
.pc2 .bar .t{flex:1;height:13px;border-radius:5px;background:#EDE7D8;overflow:hidden;min-width:0}
.pc2 .bar .f{height:100%}
.pc2 .bar .f.ok{background:#3F9577}
.pc2 .bar .f.bad{background:#C98B4B}
.pc2 .bar .d{width:54px;text-align:right;font-family:'IBM Plex Mono',monospace;font-size:11.6px;color:var(--ink)}

/* callout + sources */
.call{background:#FBF0E2;border:1px solid #EBD9BC;border-left:3px solid var(--amber);
  border-radius:10px;padding:16px 18px;margin:16px 0;min-width:0}
.call p{margin:0;font-size:14px;line-height:1.7;color:#4A3A1E;max-width:none}
.chips{display:flex;flex-wrap:wrap;gap:7px;margin:10px 0 18px}
.chip2{font-size:12.4px;background:#fff;border:1px solid var(--line);border-radius:20px;
  padding:5px 12px;color:#3B4A38}
.mgsrc{margin-top:46px;padding-top:22px;border-top:1px solid var(--line)}
.mgsrc h2{margin-top:0}
.mgsrc ol{padding-left:20px;margin:0}
.mgsrc li{font-size:13.4px;line-height:1.68;color:#4A5A46;margin-bottom:11px}
.mgsrc li a{color:var(--pine)}
.nv{background:#fff;border:1px dashed #CFC7B4;border-radius:10px;padding:15px 17px;margin:14px 0}
.nv b{display:block;font-family:'IBM Plex Mono',monospace;font-size:10px;letter-spacing:.11em;
  text-transform:uppercase;color:var(--mut);margin-bottom:9px}
.nv li{font-size:13.2px;line-height:1.62;color:#4A5A46;margin-bottom:7px}

@media (max-width:900px){
  .mgwrap{grid-template-columns:minmax(0,1fr);gap:20px;padding-top:22px}
  .mgnav{position:static;display:flex;gap:7px;overflow-x:auto;padding-bottom:5px;
    -webkit-overflow-scrolling:touch}
  .mgnav b{display:none}
  .mgnav a{border-left:0;border:1px solid var(--line);border-radius:20px;padding:6px 12px;
    white-space:nowrap;font-size:12.3px}
  .mgnav a.on{border-color:var(--pine);background:#EAF3DE}
  .mgband .in{grid-template-columns:minmax(0,1fr);gap:22px}
}
@media (max-width:560px){
  .gate{grid-template-columns:30px minmax(0,1fr);gap:10px;padding:12px 13px}
  .hstack{height:auto;flex-direction:column}
  .hseg{padding:12px 14px}
  .prow{grid-template-columns:96px minmax(0,1fr) 44px;gap:8px;font-size:11.8px}
  .mgbody p{font-size:14.8px}
}
</style>"""

JS = """<script>
(function(){
  var links=[].slice.call(document.querySelectorAll('.mgnav a'));
  var secs=links.map(function(a){return document.querySelector(a.getAttribute('href'))})
                .filter(Boolean);
  if(!links.length||!secs.length)return;
  links[0].classList.add('on');
  if(!('IntersectionObserver'in window))return;
  var io=new IntersectionObserver(function(es){
    es.forEach(function(e){
      if(!e.isIntersecting)return;
      links.forEach(function(a){
        a.classList.toggle('on',a.getAttribute('href')==='#'+e.target.id);
      });
    });
  },{rootMargin:'-12% 0px -80% 0px'});
  secs.forEach(function(s){io.observe(s)});
})();
</script>"""


# --------------------------------------------------------------- renderers
def gates():
    return '<div class="gates">' + "".join(
        '<div class="gate"><div class="n">%s</div><div><h4>%s</h4><p>%s</p>%s</div></div>'
        % (n, t, d, cite(c)) for n, t, d, c in C.GATES) + "</div>"


def hours_bar():
    tot = float(C.HOURS_TOTAL)
    segs = "".join(
        '<div class="hseg %s" style="flex:%s"><b>%s</b><span>%s</span></div>'
        % ("a" if k == "min" else "b", v / tot, "{:,}".format(v), lab)
        for lab, v, k, _n, _c in C.HOURS)
    inside = "".join(
        '<div class="hsub"><div class="in500" style="width:%.2f%%"><b>%s</b>'
        '<span>%s</span></div></div>' % (v / tot * 100, "{:,}".format(v), lab)
        for lab, v, _n, _c in C.HOURS_INSIDE)
    # Each note names the figure it belongs to. Without that, the notes render
    # in a column beneath a bar and a chip, and the eye attaches the first note
    # to the chip directly above it rather than to the segment it describes -
    # which on this particular graphic means attaching "a minimum, not a target"
    # to the 500 instead of the 1,750. Labelling costs four words and removes
    # the ambiguity completely.
    notes = "".join('<p class="hnote"><b>%s</b> &mdash; %s %s</p>'
                    % ("{:,}".format(v), n, cite(c))
                    for _l, v, _k, n, c in C.HOURS)
    notes += "".join('<p class="hnote"><b>%s</b> &mdash; %s %s</p>'
                     % ("{:,}".format(v), n, cite(c))
                     for _l, v, n, c in C.HOURS_INSIDE)
    return ('<div class="hbar"><div class="hstack">%s</div>%s%s</div>'
            % (segs, inside, notes))


def split():
    tot = float(C.HOURS_TOTAL)
    out = []
    for lab, v, kind, note, c in C.HOURS_SPLIT:
        tag = ('<span class="tagcap">ceiling</span>' if kind == "ceiling"
               else '<span class="tagfloor">floor</span>')
        out.append(
            '<div class="sp"><div class="top"><h4>%s %s</h4><span class="v">%s</span></div>'
            '<div class="track"><div class="fill %s" style="width:%.1f%%"></div></div>'
            '<p>%s %s</p></div>'
            % (lab, tag, "{:,}".format(v), "cap" if kind == "ceiling" else "",
               v / tot * 100, note, cite(c)))
    return '<div class="split">' + "".join(out) + "</div>"


def rules():
    return '<div class="rules">' + "".join(
        '<div class="rule"><b>%s</b><i>%s</i><p>%s</p>%s</div>' % (n, lab, note, cite(c))
        for n, lab, note, c in C.WEEKLY) + "</div>"


def exams():
    out = []
    for name, ft, fp, at, ap, mins, note, c in C.EXAMS:
        f1 = round(fp / ft * 100)
        a1 = round(ap / at * 100)
        out.append(
            '<div class="ex"><h4>%s</h4><div class="len">%d minutes</div>'
            '<p>%s %s</p><div class="pr">'
            '<div class="prow"><span class="lab">First-time takers</span>'
            '<div class="tr"><div class="fi" style="width:%d%%"></div></div>'
            '<span class="pc">%d%%</span></div>'
            '<div class="prow"><span class="lab">All takers</span>'
            '<div class="tr"><div class="fi" style="width:%d%%"></div></div>'
            '<span class="pc">%d%%</span></div></div>'
            '<p style="margin:11px 0 0;font-size:12.4px;color:#7C8878">'
            '%s of %s first-timers passed; %s of %s across all attempts. '
            'Ninety days between attempts.</p></div>'
            % (name, mins, note, cite(c), f1, f1, a1, a1,
               "{:,}".format(fp), "{:,}".format(ft),
               "{:,}".format(ap), "{:,}".format(at)))
    return "".join(out)


def fees():
    rows = "".join(
        '<tr><td>%s</td><td class="was">$%d</td><td class="now">$%d</td>'
        '<td>%s</td></tr>' % (lab, was, now, cite(c))
        for lab, was, now, c in C.FEES)
    was_t = sum(w for _l, w, _n, _c in C.FEES)
    now_t = sum(n for _l, _w, n, _c in C.FEES)
    # This sums one of every row, including the ANNUAL associate renewal - so
    # it is the cost of a route with exactly one renewal, i.e. the fastest
    # legal path, not "every fee once". Saying "once" understated it for
    # everyone who takes longer than a year, which is everyone.
    rows += ('<tr class="tot"><td>The fastest legal route &mdash; one of each, '
             'with a single annual renewal</td>'
             '<td class="was">$%s</td><td class="now">$%s</td><td></td></tr>'
             % ("{:,}".format(was_t), "{:,}".format(now_t)))
    rows += ('<tr class="tot"><td>The six-year ceiling &mdash; five renewals, '
             'the most the Board permits</td>'
             '<td class="was">$%s</td><td class="now">$%s</td>'
             '<td>BPC &sect;4984.01</td></tr>'
             % ("{:,}".format(was_t + 4 * 150), "{:,}".format(now_t + 4 * 75)))
    other = "".join(
        '<tr><td>%s</td><td colspan="2" class="now" style="font-size:15px">%s</td>'
        '<td>%s</td></tr>' % (lab, amt, note) for lab, amt, note in C.FEES_OTHER)
    return ('<div class="tw"><table class="fee">'
            '<tr><th>Board fee</th><th>Before 1 Jul 2026</th><th>Now</th><th>Regulation</th></tr>'
            '%s</table></div>'
            '<h3>What the Board does not charge you</h3>'
            '<div class="tw"><table class="fee">'
            '<tr><th>Cost</th><th colspan="2">Amount</th><th>Who takes it</th></tr>'
            '%s</table></div>' % (rows, other))


def processing():
    out = []
    mx = float(max(max(a, b) for _n, a, b, _u in C.PROCESSING))
    for name, clean, deficient, unit in C.PROCESSING:
        out.append(
            '<div class="pc2"><h4>%s</h4>'
            '<div class="bar"><span>Clean</span><div class="t"><div class="f ok" '
            'style="width:%.0f%%"></div></div><span class="d">%d %s</span></div>'
            '<div class="bar"><span>Deficient</span><div class="t"><div class="f bad" '
            'style="width:%.0f%%"></div></div><span class="d">%d %s</span></div></div>'
            % (name, clean / mx * 100, clean, unit,
               deficient / mx * 100, deficient, unit))
    return '<div class="proc">' + "".join(out) + "</div>"


def traps():
    return '<div class="traps">' + "".join(
        '<div class="trap"><h4>%s</h4><p>%s</p>%s</div>' % (t, b, cite(c))
        for t, b, c in C.TRAPS) + "</div>"


def degree_block():
    chips = "".join('<span class="chip2">%s</span>' % t for t in C.DEGREE_TITLES)
    rows = "".join(
        '<div class="rule"><b>%s</b><i>%s</i>%s</div>' % (amt, what, cite(c))
        for amt, what, c in C.CONTENT_AREAS)
    return ('<div class="chips">%s</div><div class="rules">%s</div>' % (chips, rows))


def sources():
    items = "".join('<li><a href="%s" target="_blank" rel="noopener noreferrer">%s</a> '
                    '&mdash; %s</li>' % (u, t, n) for t, u, n in C.SOURCES)
    nv = "".join("<li>%s</li>" % x for x in C.NOT_VERIFIED)
    return ('<div class="mgsrc" id="sources"><h2>Sources</h2><ol>%s</ol>'
            '<div class="nv"><b>What is not on this page, and why</b><ul>%s</ul></div>'
            '<p style="font-size:13px;color:#7C8878;margin-top:14px">This is a summary '
            'of published requirements, not legal advice, and the Board is the only '
            'authority on your particular file. Where a figure here and the Board '
            'disagree, the Board is right and this page is out of date &mdash; '
            '<a href="contact.html">tell me</a> and I will fix it.</p></div>'
            % (items, nv))


SECTIONS = [
    ("the-five-gates", "The five gates", lambda: (
        "<p>There is no discretion in any of this. Five requirements, each defined by "
        "a section of the Business and Professions Code, and the Board checks all five "
        "against paperwork you have been carrying for years. The order matters, "
        "because three of them have deadlines that start running the moment the one "
        "before it finishes.</p>" + gates() +
        '<div class="call"><p><b>The single most expensive mistake on this page</b> is '
        "gate three. The Board must <b>receive</b> your associate application within 90 "
        "days of your degree being granted. Not postmark. Receive. Every post-degree "
        "hour you work before the registration issues depends on it.</p></div>")),

    ("the-degree", "The degree", lambda: (
        "<p>Sixty semester units, or ninety quarter units. The Board accepts several "
        "degree titles, so the name on your diploma matters less than the content "
        "behind it. " + cite("&sect;4980.36(b), (d)") + "</p>"
        "<p>Any of these titles will do:</p>" + degree_block() +
        "<p>Two of those &mdash; suicide risk and telehealth &mdash; are certified "
        "separately when you apply, not inferred from your transcript. Programmes vary "
        "in whether they hand you the certificate, so ask.</p>"
        "<p>The institution must be approved by the Bureau for Private Postsecondary "
        "Education, accredited by COAMFTE, or accredited by a regional or national "
        "agency the US Department of Education recognises. And the statute reserves the "
        "last word: the Board <b>&ldquo;has the authority to make the final "
        "determination as to whether a degree meets all requirements, regardless of "
        "accreditation or approval&rdquo;</b>. " + cite("&sect;4980.36(b)") + "</p>"
        '<p><a href="mft-programs-california.html">Every California programme that '
        "leads here &rarr;</a></p>")),

    ("practicum", "Practicum, before you graduate", lambda: (
        "<p>Six semester units of supervised placement, at least 150 hours face to "
        "face with clients, plus 75 more of either client-centred advocacy or more "
        "counselling. " + cite("&sect;4980.36(d)(1)(B)") + "</p>"
        "<p>What surprises people is how much of the 3,000 you can bank as a student "
        "&mdash; and how tightly it is capped.</p>" + split() +
        "<p>A trainee may not work in a private practice or a professional corporation "
        "at all, may not be an independent contractor, and may not take money from "
        "clients. " + cite("&sect;4980.43.3") + " Supervision runs at one hour for "
        "every five hours of counselling. " + cite("&sect;4980.43.2(a)(2)") + "</p>")),

    ("the-hours", "The 3,000 hours", lambda: (
        "<p>Everyone knows the number. Almost nobody arrives knowing its shape, and "
        "the shape is what decides whether you finish on time.</p>" + hours_bar() +
        "<p>Read that again, because it is the thing people get wrong: the 500 "
        "relational hours are <b>carved out of the 1,750, not added to it</b>. An "
        "associate at an agency that sees mostly individual adults can reach 3,000 "
        "total, 1,750 clinical, and still not be licensable.</p>"
        "<h3>And the weekly arithmetic</h3>" + rules() +
        '<div class="call"><p>The 40-hour weekly ceiling is theoretical. The binding '
        "constraint is the 1,750 clinical minimum: at twenty billable hours a week "
        "that is 87.5 weeks; at fifteen it is 117 &mdash; which is past the 104-week "
        "floor on its own. Your caseload, not the calendar, sets your date.</p></div>")),

    ("supervision", "Supervision", lambda: (
        "<p>One hour of direct supervisor contact in every week you claim, in every "
        "setting you claim it. Two hours of group counts as one. Fifty-two of the 104 "
        "weeks must be individual or triadic. " + cite("&sect;4980.43.2") + "</p>"
        "<p>A supervisor must have held an active licence for at least two of the last "
        "five years, have practised psychotherapy or supervised it for two of them, "
        "have completed supervision training, hold a licence not under suspension or "
        "probation, never have been your own therapist, and be neither a relative nor "
        "your domestic partner. " + cite("&sect;4980.03(g)") + "</p>"
        '<div class="call"><p>If any one of those fails, <b>your</b> hours do not '
        "count. Not theirs. The regulations make you sign a statement confirming you "
        "understand that. " + cite("16 CCR &sect;1833(c)(3)") + "</p></div>"
        "<p>Supervision by two-way real-time video is permanent now &mdash; the sunset "
        "date that used to hang over it was removed in the January 2026 statutes. "
        + cite("&sect;4980.43.2(b)(2)") + "</p>")),

    ("exams", "The two exams", lambda: (
        "<p>Both are administered by Pearson VUE for the Board, and both are already "
        "paid for by the time you sit down &mdash; the test centre takes nothing.</p>"
        + exams() +
        "<p>Pass rates are the Board's own, for calendar year 2025, published by "
        'school as well as statewide. <a href="' + C.EXAM_SRC + '" target="_blank" '
        'rel="noopener noreferrer">The full report breaks both exams down by the '
        "programme you graduated from</a>, which is worth reading before you choose "
        "one.</p>"
        "<p>Failing is expensive in time rather than money: ninety days before you can "
        "sit again, one year from the failure notice before you must file a brand-new "
        "application at current requirements and full fees. " + cite("&sect;4984.72(a)")
        + "</p>")),

    ("the-money", "What the Board charges", lambda: (
        "<p>" + C.FEE_NOTE + " " + cite("16 CCR &sect;&sect;1816&ndash;1816.4") +
        "</p>" + fees() +
        "<p>The table is Board fees only, once each. The associate renewal repeats "
        "every year you stay registered, so a two-year associateship pays it twice and "
        "a five-year one pays it five times.</p>"
        '<p style="font-size:13.4px;color:#7C8878">Not counted here: continuing '
        "education, remediation coursework if your degree is short a required area, "
        "credential evaluation if your degree is from outside the United States, and "
        "exam preparation, which is not required at all. None of those are Board fees "
        "and none are published, so this page does not invent a figure for them.</p>")),

    ("how-long", "How long it actually takes", lambda: (
        "<p><b>The Board does not publish an average.</b> I looked &mdash; the 2025 "
        "sunset review and the Board's own licensing updates report processing times "
        "and backlogs, but not time-to-licence. So rather than repeat a number from a "
        "content farm, here is what can be computed from the rules themselves.</p>"
        "<p>After the degree, the 104-week floor binds unless you banked serious "
        "pre-degree hours. Add the Board's current processing times and the honest "
        "post-graduation minimum is <b>about 28 months</b> &mdash; two years of "
        "supervised experience, roughly two and a half months of licensure review, and "
        "about six weeks to issue. If you maxed the 1,300 pre-degree hours across at "
        "least 61 weeks, and could log forty countable hours every week afterwards, "
        "the floor drops to about fourteen months. Nobody does that.</p>"
        "<h3>And the Board's own processing times</h3>" + processing() +
        "<p>Those are calendar days as of 29 January 2026. The gap between the two "
        "bars is the entire argument for filing a complete application: a deficient "
        "licensure file costs <b>54 extra days</b>, and the Board's five-year average "
        "sits at 99 business days against its own 60-business-day target. "
        + cite("BBS Licensing Update, Feb 2026") + "</p>")),

    ("traps", "Where people lose hours", lambda: (
        "<p>Every one of these has cost somebody a year. They are in the code, they "
        "are not hidden, and they are almost never mentioned by the people selling you "
        "a programme.</p>" + traps())),
]


def build():
    nav = '<nav class="mgnav"><b>On this page</b>%s<a href="#sources">Sources</a></nav>' % (
        "".join('<a href="#%s">%s</a>' % (i, t) for i, t, _f in SECTIONS))
    body = "".join('<h2 id="%s">%s</h2>%s' % (i, t, f()) for i, t, f in SECTIONS)

    fig = ('<div class="mgfig"><b>3,000</b><span>supervised hours, over at least 104 '
           'weeks, before you may be licensed</span>'
           '<div class="row"><span>Direct clinical, minimum</span><b>1,750</b></div>'
           '<div class="row"><span>Relational, inside that</span><b>500</b></div>'
           '<div class="row"><span>Bankable before the degree</span><b>1,300</b></div>'
           '<div class="row"><span>Board fees, whole route</span><b>$575&ndash;$875</b></div>'
           '</div>')

    doc = """<!doctype html>
<html lang="en"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>Becoming an LMFT in California: every requirement, with the section it comes from</title>
<meta name="description" content="The full route to California LMFT licensure — degree, practicum, the 3,000 hours, supervision, both exams, every Board fee at the 2026 reduced rates, and the rules that most often cost people a year. Every figure cited to the Board or the code.">
<link rel="canonical" href="https://therapistsupport.org/become-an-mft-california.html">
%s
%s
%s
</head><body class="mg">
%s
<main>
<section class="mgband"><div class="in"><div>
<ol class="bcr" aria-label="Breadcrumb">
<li><a href="index.html">Therapist Support</a><span class="sep">&rsaquo;</span></li>
<li><a href="resources.html">Resources</a><span class="sep">&rsaquo;</span></li>
<li><span aria-current="page">Becoming an MFT</span></li></ol>
<h1>Becoming an LMFT in California, <em>with the section it comes from</em>.</h1>
<p class="dek">Every requirement the Board of Behavioral Sciences actually imposes &mdash;
the degree, the practicum, the 3,000 hours, supervision, both exams, and every fee at
the rates that took effect on 1 July 2026. Where the Board publishes nothing, this page
says so rather than guessing.</p>
<div class="mgmeta"><span>California</span><span>Updated %s</span><span>Reading time about 12 minutes</span></div>
</div>%s</div></section>
<div class="mgwrap">%s<article class="mgbody">%s%s</article></div>
</main>
%s
%s
</body></html>""" % ("\n".join(links), "\n".join(styles), CSS, header, UPDATED,
                     fig, nav, body, sources(), footer, JS)
    return doc


def main():
    doc = build()
    open(OUT, "w", encoding="utf-8").write(doc)

    # ---- guards. Refuse to ship a page that quietly loses its own content.
    bad = []
    if doc.count("<h1") != 1:
        bad.append("%d h1" % doc.count("<h1"))
    for i, t, _f in SECTIONS:
        if ('id="%s"' % i) not in doc:
            bad.append("section %s missing" % i)
        if ('href="#%s"' % i) not in doc:
            bad.append("section %s not in nav" % i)
    # every headline figure must actually appear in the body
    for n in ("3,000", "1,750", "1,250", "500", "1,300", "104"):
        if n not in doc:
            bad.append("figure %s absent" % n)
    # every statute reference rendered must be a real section-looking token
    cites = re.findall(r'<span class="cx">(.*?)</span>', doc)
    if len(cites) < 25:
        bad.append("only %d citations" % len(cites))
    for c in cites:
        if not re.search(r"&sect;|CCR|BBS|B&amp;P", c):
            bad.append("citation without a section: %r" % c[:40])
    # the sources block must carry a working-looking URL for each entry
    for _t, u, _n in C.SOURCES:
        if u not in doc:
            bad.append("source url missing: %s" % u[:50])
    # arithmetic the page asserts
    if sum(v for _l, v, _k, _n, _c in C.HOURS) != C.HOURS_TOTAL:
        bad.append("hours segments do not sum to %d" % C.HOURS_TOTAL)
    if sum(v for _l, v, _k, _n, _c in C.HOURS_SPLIT) != C.HOURS_TOTAL:
        bad.append("pre/post split does not sum to %d" % C.HOURS_TOTAL)
    for _l, v, _n, _c in C.HOURS_INSIDE:
        if v > C.HOURS[0][1]:
            bad.append("inside figure %d exceeds its container" % v)
    if bad:
        sys.exit("build_guide: " + "; ".join(bad))

    print("%-40s %d bytes  %d sections  %d citations  %d sources"
          % (os.path.basename(OUT), len(doc), len(SECTIONS), len(cites), len(C.SOURCES)))


if __name__ == "__main__":
    main()
