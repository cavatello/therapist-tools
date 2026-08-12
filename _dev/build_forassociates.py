#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""/for/associates - the first stage door, built as the Ledger.

WHY THIS DESIGN AND NOT THE OTHER TWO

Three variants were drawn for this door. The Desk opens with six live tiles;
the Three Questions opens with the loudest threads verbatim; the Ledger opens
with one horizontal bar and the sub-gates marked. The Ledger won on a single
constraint: a large share of this traffic arrives on a phone, from a link
posted in a group, and one bar with a marked gate survives a 390px first
screen where six tiles do not. The other two are not discarded - the Desk's
detail is what the bar expands into, and the Questions sit directly beneath
it.

THE GATE THAT LEADS

Of the four sub-totals inside the 3,000, the one people miss is the 500
relational hours - counselling couples, families and children. Somebody can
reach 3,000 total and 1,750 direct and still not be finished. So the
relational gate is the highest-contrast element on the page, not a footnote in
the fourth tile.

NOTHING IS SENT ANYWHERE, AND THAT IS SAID IN THE HERO

Every figure is computed in the browser. There is no storage, no share hash,
no query string and no network call - which matters twice over, because the
site's analytics guard fails the build if tracking can read a typed value, and
because the promise is worth nothing if a reader has to find it in the footer.

THE SHELF IS BUILT FROM stage_note, NOT FROM TITLES

Each page below is annotated with what it tells THIS reader, at THIS stage,
read from the registry field written by _dev/stage_tags.py. That is the whole
difference between a stage hub and a re-listed topic hub, and a guard here
refuses to print a page that has no note.
"""
import json, os, sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import pagekit as pk

SITE = pk.SITE
PAGE = "for/associates.html"
# THE DONOR MUST ALREADY LIVE ONE LEVEL DOWN. Borrowing chrome from a page at
# the site root gives you a masthead and footer whose links are bare
# ("contact.html"), which resolve to /for/contact.html from here and are dead.
# Some of them get depth-corrected by a later pass and some do not, so the
# result is a footer that is half right - which is worse than one that is
# uniformly wrong, because it looks fine. A topic hub is the correct donor:
# it sits at the same depth and its links are already relative to it.
DONOR = "licensure/index.html"
REG = os.path.join(SITE, "mock", "library", "registry.json")
STAGE = "associate"

# Everything on this page sits one directory down, so every internal link
# needs to climb. Getting this wrong produces a hub of dead links, which is
# the one thing a hub may not be - the guard below checks every one resolves
# to a file that exists.
UP = "../"

JUMPS = [("ledger", "Where you are"),
         ("asking", "What this room asks"),
         ("shelf", "Everything for this stage"),
         ("sources", "The rules behind it")]

# The three loudest threads in the community analysis, de-identified - no
# name, no group, no quotable handle. The wording is the recurring shape of
# the question rather than any one person's post.
ASKING = [
    ("&ldquo;Hundreds of hours in, and nobody will hire me.&rdquo;",
     "It is a billing rule, not your hour count.",
     "Medi-Cal names registered associates as a billable staff type. Most "
     "commercial payers do not, which is why the jobs are concentrated where "
     "they are &mdash; and it has nothing to do with how far along you are.",
     "getting-hired-as-a-california-associate.html"),
    ("&ldquo;Am I supposed to be doing this unpaid?&rdquo;",
     "The wage claim is a real one, and the Board is not where you file it.",
     "Non-clinical time an employer requires is time worked. The claim goes to "
     "the Labor Commissioner, there is a form, and there is a deadline.",
     "associate-unpaid-hours-california.html"),
    ("&ldquo;Will hours from another state count?&rdquo;",
     "Yes, with conditions &mdash; and the Board has answered this five times.",
     "The answer sits in a PDF nobody links to. What travels, what does not, "
     "and what your supervisor has to be.",
     "associate-hours-telehealth-out-of-state.html"),
]

CSS = """<style>/* _dev/build_forassociates.py - the ledger */
.lg{border:2px solid var(--pk-ink,#16211B);background:#fff;padding:18px 18px 20px;
 box-shadow:5px 5px 0 var(--pk-ink,#16211B);margin:0 0 20px}
.lg-in{display:grid;gap:12px;margin-bottom:18px}
@media(min-width:660px){.lg-in{grid-template-columns:repeat(4,1fr)}}
.lg-in label{display:block;font-family:'IBM Plex Mono',ui-monospace,monospace;
 font-size:10.5px;letter-spacing:.13em;text-transform:uppercase;color:#635E53;
 margin-bottom:5px}
.lg-in input{width:100%;font-family:'Fraunces',Georgia,serif;font-weight:800;
 font-size:20px;padding:8px 10px;background:#FBF6E9;border:2px solid #E4D9BE;
 color:#16211B}
.lg-in input:focus{outline:3px solid #F6C560;outline-offset:1px;border-color:#16211B}
.lg-bar{position:relative;height:34px;border:2px solid #16211B;background:#F4F0E6;
 overflow:hidden;margin:6px 0 4px}
.lg-bar i{display:block;height:100%;background:#2C6350;width:0;transition:width .25s}
.lg-mk{position:relative;height:26px;margin-bottom:14px}
.lg-mk span{position:absolute;top:0;font-family:'IBM Plex Mono',ui-monospace,monospace;
 font-size:10px;color:#635E53;white-space:nowrap;transform:translateX(-50%);padding-top:3px}
.lg-mk span::before{content:"";position:absolute;left:50%;top:-4px;width:2px;height:5px;
 background:#16211B}
.lg-g{display:grid;gap:10px}
@media(min-width:560px){.lg-g{grid-template-columns:repeat(4,1fr)}}
.lg-g div{border:2px solid #16211B;background:#FBF9F3;padding:10px 12px;
 box-shadow:3px 3px 0 #16211B}
.lg-g .k{font-family:'IBM Plex Mono',ui-monospace,monospace;font-size:9.5px;
 letter-spacing:.13em;text-transform:uppercase;color:#635E53;display:block}
.lg-g .v{font-family:'Fraunces',Georgia,serif;font-weight:800;font-size:23px;
 color:#16211B;line-height:1.1;margin:3px 0 2px;font-variant-numeric:tabular-nums}
.lg-g .s{font-size:11.5px;color:#635E53;line-height:1.35}
.lg-g.gate div.hot{background:#F6C560;border-color:#16211B}
.lg-g div.done{background:#EAF3DE}
.lg-note{font-size:12.5px;color:#635E53;margin:14px 0 0}
.lg-priv{font-family:'IBM Plex Mono',ui-monospace,monospace;font-size:10.5px;
 letter-spacing:.1em;text-transform:uppercase;color:#2C6350;margin:0 0 10px}
.ask{border:2px solid #16211B;background:#fff;padding:14px 16px;margin:0 0 12px;
 box-shadow:4px 4px 0 #16211B}
.ask q{display:block;font-family:'Fraunces',Georgia,serif;font-size:20px;
 font-weight:700;line-height:1.25;color:#16211B;quotes:none}
.ask .an{font-family:'Bricolage Grotesque','Archivo',Inter,sans-serif;font-weight:800;
 font-size:15px;margin:9px 0 5px;color:#2C6350}
.ask p{font-size:14.5px;margin:0 0 9px}
.ask a{font-family:'IBM Plex Mono',ui-monospace,monospace;font-size:11px;
 letter-spacing:.1em;text-transform:uppercase}
.shelf{display:grid;gap:12px}
@media(min-width:720px){.shelf{grid-template-columns:1fr 1fr}}
.shelf a.card{display:block;border:2px solid #16211B;background:#FBF9F3;padding:13px 15px;
 box-shadow:4px 4px 0 #16211B;text-decoration:none;color:inherit}
.shelf a.card:hover{background:#F6C560}
.shelf .t{font-family:'Bricolage Grotesque','Archivo',Inter,sans-serif;font-weight:800;
 font-size:15.5px;line-height:1.25;margin-bottom:5px}
.shelf .n{font-size:13.5px;color:#3A4A42;line-height:1.45}
</style>"""

JS = """<script>/* the ledger. Everything here stays in this browser: no storage,
   no hash, no query string, no network. */
(function(){
 var $=function(i){return document.getElementById(i)};
 var F=["lgTotal","lgDirect","lgRel","lgWeeks","lgRate"];
 function num(id){var e=$(id);if(!e)return 0;var v=parseFloat(e.value);
   return (isNaN(v)||v<0)?0:v}
 function money(n){return n.toLocaleString("en-US")}
 function draw(){
  var tot=num("lgTotal"),dir=num("lgDirect"),rel=num("lgRel"),
      wk=num("lgWeeks"),rate=num("lgRate");
  var pct=Math.max(0,Math.min(100,tot/3000*100));
  $("lgFill").style.width=pct.toFixed(1)+"%";
  $("lgPct").textContent=Math.round(pct)+"%";
  $("lgTot").textContent=money(Math.round(tot))+" / 3,000";
  set("gDirect",dir,1750,"direct clinical hours");
  set("gRel",rel,500,"relational hours");
  set("gWeeks",wk,104,"weeks elapsed");
  var left=Math.max(0,3000-tot);
  var wks=rate>0?Math.ceil(left/rate):0;
  var need=Math.max(wks,Math.max(0,104-wk));
  var e=$("gWhen");
  if(rate>0&&tot>0){
    e.querySelector(".v").textContent=need+" wk";
    e.querySelector(".s").textContent=need>0
      ? "at "+rate+" h a week, and the 104-week floor"
      : "both the hours and the weeks are met";
    e.className=need>0?"":"done";
  }else{
    e.querySelector(".v").textContent="\\u2014";
    e.querySelector(".s").textContent="enter hours and a weekly rate";
    e.className="";
  }
 }
 function set(id,have,need,label){
  var e=$(id);
  e.querySelector(".v").textContent=money(Math.round(have))+" / "+money(need);
  var short=Math.max(0,need-have);
  e.querySelector(".s").textContent=short>0
    ? money(Math.round(short))+" still to find"
    : label+" met";
  e.className=short>0?(id==="gRel"?"hot":""):"done";
 }
 for(var i=0;i<F.length;i++){
  var el=$(F[i]);
  if(el){el.addEventListener("input",draw);el.addEventListener("change",draw)}
 }
 draw();
})();
</script>"""


def body(shelf):
    o = ['<article class="pk-wrap">']

    o.append(pk.hero(
        "You are counting toward 3,000",
        "One bar. Four gates. Nothing you type here leaves this browser.",
        "Written for AMFTs. Where a rule differs for an ASW or an APCC it says "
        "so and links to the difference. Everything below is computed on this "
        "page &mdash; there is no account, no database and no share link that "
        "could carry your figures anywhere.",
        [("3,000", "hours in total"),
         ("1,750", "direct clinical"),
         ("500", "relational &mdash; the gate"),
         ("104", "weeks minimum")],
        JUMPS))

    # ---------------------------------------------------------------- ledger
    o.append('<section class="pk-sec" id="ledger">')
    o.append('<p class="pk-k">Where you are</p>')
    o.append('<h2 class="pk-h">The whole requirement, in one line.</h2>')
    o.append('<p class="pk-d">Four numbers off your own log. The bar is the '
             "3,000; the tiles are the sub-totals underneath it, and one of "
             "them stops more people than the rest.</p>")

    o.append('<div class="lg">')
    o.append('<p class="lg-priv">Stays in this browser &middot; nothing is sent</p>')
    o.append('<div class="lg-in">')
    for fid, lab, ph in [
        ("lgTotal", "Hours logged, total", "1284"),
        ("lgDirect", "Of those, direct clinical", "742"),
        ("lgRel", "Of those, relational", "228"),
        ("lgWeeks", "Weeks since you registered", "61"),
    ]:
        o.append('<div><label for="%s">%s</label>'
                 '<input id="%s" type="number" min="0" step="1" '
                 'inputmode="numeric" placeholder="%s"></div>' % (fid, lab, fid, ph))
    o.append("</div>")

    o.append('<div class="lg-bar"><i id="lgFill"></i></div>')
    o.append('<div class="lg-mk"><span style="left:58.3%">1,750 direct</span>'
             '<span style="left:99%">3,000</span></div>')
    o.append('<div class="lg-g gate">')
    for gid, k in [("gDirect", "Direct clinical"), ("gRel", "Relational"),
                   ("gWeeks", "Weeks"), ("gWhen", "Weeks still to go")]:
        o.append('<div id="%s"><span class="k">%s</span>'
                 '<span class="v">&mdash;</span>'
                 '<span class="s">&nbsp;</span></div>' % (gid, k))
    o.append("</div>")
    o.append('<div class="lg-in" style="margin:14px 0 0;grid-template-columns:1fr">'
             '<div><label for="lgRate">Hours you log in a typical week</label>'
             '<input id="lgRate" type="number" min="0" step="1" '
             'inputmode="numeric" placeholder="18"></div></div>')
    o.append('<p class="lg-note"><b id="lgTot">&mdash;</b> &middot; '
             '<span id="lgPct">0%</span> of the way. The relational gate is '
             "marked because it is the one people reach 3,000 without: 500 "
             "hours with couples, families and children, inside the 1,750. "
             "Everything here is your arithmetic, not the Board&rsquo;s "
             "record.</p>")
    o.append("</div>")

    o.append(pk.callout(
        "The four numbers, and where they come from",
        ["<b>3,000</b> hours over at least <b>104 weeks</b>, of which at least "
         "<b>1,750</b> are direct clinical counseling and at least <b>500</b> "
         "of those are with couples, families and children. No more than 40 "
         "hours in any seven days, and no more than 1,250 of nonclinical time.",
         'All of it is &sect;&thinsp;4980.43(c). The full arithmetic, including '
         'what happens to hours gained before your degree, is on '
         '<a href="%samft-3000-hours-california.html">the calculator</a> and '
         '<a href="%spracticum-california-mft-trainee.html">the practicum '
         "page</a>." % (UP, UP)]))
    o.append("</section>")

    # --------------------------------------------------------------- asking
    o.append('<section class="pk-sec" id="asking">')
    o.append('<p class="pk-k">What this room asks</p>')
    o.append('<h2 class="pk-h">Three questions, and the pages that answer '
             "them.</h2>")
    o.append('<p class="pk-d">Taken from the shape of what actually gets '
             "posted in the pre-licensed groups, not from a taxonomy. Nobody "
             "is quoted and nobody is identified.</p>")
    for q, ans, expl, href in ASKING:
        o.append('<div class="ask"><q>%s</q><p class="an">%s</p><p>%s</p>'
                 '<a href="%s%s">Read it &rarr;</a></div>'
                 % (q, ans, expl, UP, href))
    o.append("</section>")

    # ---------------------------------------------------------------- shelf
    o.append('<section class="pk-sec" id="shelf">')
    o.append('<p class="pk-k">Everything for this stage</p>')
    o.append('<h2 class="pk-h">%d pages, each with what it tells you '
             "here.</h2>" % len(shelf))
    o.append('<p class="pk-d">The line under each title is not the page&rsquo;s '
             "summary &mdash; it is what that page tells somebody at this "
             "stage specifically. The same page says something different to a "
             "student or to a licensed therapist.</p>")
    o.append('<div class="shelf">')
    for f, title, note in shelf:
        o.append('<a class="card" href="%s%s"><span class="t">%s</span>'
                 '<span class="n">%s</span></a>' % (UP, f, pk.esc(title),
                                                    pk.esc(note)))
    o.append("</div>")
    o.append("</section>")

    src, nsrc = pk.sources([
        ("The rule behind the bar", [
            ("Business and Professions Code &sect;&thinsp;4980.43 &mdash; the "
             "3,000 hours, the 104 weeks, and every sub-total on this page",
             "https://leginfo.legislature.ca.gov/faces/codes_displaySection."
             "xhtml?lawCode=BPC&sectionNum=4980.43."),
            ("&sect;&thinsp;4980.43.2 &mdash; the supervision each of those "
             "hours needs",
             "https://leginfo.legislature.ca.gov/faces/codes_displaySection."
             "xhtml?lawCode=BPC&sectionNum=4980.43.2."),
        ]),
    ], note="This page is a door, not a record. <b>Every figure you enter is "
            "computed in your browser and nothing is stored or sent</b> "
            "&mdash; reload the page and it is gone. It is your arithmetic "
            "against the statute, and it is not the Board&rsquo;s count of "
            "your hours; only your supervisor&rsquo;s signed forms are that. "
            "Written for AMFTs, with the differences for ASWs and APCCs on the "
            "pages linked above. Nothing here is legal advice.")
    o.append(src)

    o.append("</article>")
    return "".join(o), nsrc


META = pk.meta_block(
    PAGE,
    "For California associates: everything for counting your 3,000 hours",
    "One page for registered associates - where you are against the 3,000 "
    "hours and all four gates inside them, the three questions the "
    "pre-licensed groups actually ask, and every page written for this stage.",
    "licensure", "reference",
    "What do I need while I am a registered associate in California?",
    "The whole requirement in one bar, and every page on this site written "
    "for somebody counting hours",
    "500 relational hours is the gate people reach 3,000 without",
    weight=5)


def main():
    print("the associates door")

    reg = json.load(open(REG, encoding="utf-8"))
    shelf = []
    for p in reg["pages"]:
        if STAGE not in p.get("stages", []):
            continue
        note = (p.get("stage_note") or {}).get(STAGE, "").strip()
        if not note:
            sys.exit("%s is tagged %r with no stage_note. A hub entry with "
                     "nothing to say at this stage is the thin duplicate this "
                     "whole design exists to avoid." % (p["file"], STAGE))
        shelf.append((p["file"], p["title"], note))
    shelf.sort(key=lambda r: r[1])

    if len(shelf) < 5:
        sys.exit("only %d page(s) tagged %r - a hub this thin fails the test "
                 "it was built to pass" % (len(shelf), STAGE))

    head, header, footer, links, scripts = pk.chrome_parts(DONOR)
    html_body, nsrc = body(shelf)
    html = pk.assemble(head, META, header, html_body, footer, links, scripts,
                       extra=CSS + JS)

    os.makedirs(os.path.join(SITE, "for"), exist_ok=True)
    p = os.path.join(SITE, PAGE)
    open(p, "w", encoding="utf-8").write(html)
    print("  wrote %s, %s bytes, %d shelf pages, %d sources"
          % (PAGE, format(len(html), ",d"), len(shelf), nsrc))

    bad = pk.check_page(p, [
        ("the privacy promise in the hero", "leaves this browser"),
        ("the relational gate", "reach 3,000 without"),
        ("the not-the-Board caveat", "not the Board&rsquo;s count"),
    ], [j[0] for j in JUMPS])

    s = open(p, encoding="utf-8").read()
    art = pk.article(s)

    # Every link must climb out of /for/ and land on a file that exists. A hub
    # of dead links is the one thing a hub may not be, and the depth prefix is
    # exactly the kind of thing that is wrong everywhere or nowhere.
    import re
    for href in set(re.findall(r'href="(\.\./[^"#]+)"', art)):
        target = os.path.normpath(os.path.join(SITE, "for", href))
        if not os.path.exists(target):
            print("GUARD: %s does not resolve to a file" % href)
            bad += 1
    if 'href="../' not in art:
        print("GUARD: no link climbs out of /for/ - the depth prefix is gone")
        bad += 1

    # The ledger must not persist or transmit anything. The site's promise is
    # the reason anybody types a number into it at all.
    for pat, why in ((r"localStorage", "browser storage"),
                     (r"sessionStorage", "browser storage"),
                     (r"location\.hash\s*=", "a share hash"),
                     (r"\bfetch\s*\(", "a network call"),
                     (r"XMLHttpRequest", "a network call"),
                     (r"navigator\.sendBeacon", "a network call")):
        if re.search(pat, JS):
            print("GUARD: the ledger uses %s, and the hero promises it does "
                  "not" % why)
            bad += 1

    for w in pk.spelling(s):
        print("GUARD: British spelling %r" % w)
        bad += 1

    if bad:
        sys.exit("\n%d problem(s)" % bad)
    print("  guards ok - %d shelf entries, every link resolves" % len(shelf))


if __name__ == "__main__":
    main()
