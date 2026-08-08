#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Concept 03, second half: the seven calculators as a sequence, not a pile.

WHAT WAS ALREADY DONE, AND WHAT WAS NOT

Concept 03 had two parts. The first - `Calculators` as a top-level nav item,
coequal with the directory and the editorial - shipped with the nav rebuild and
is live: it is the first of the seven groups in `restyle.py`. Student Doctor
Network is the only site in the IA survey that gives calculators a nav slot; it
has four and we have seven, so the slot was the easy call.

The part that did not ship is the one that actually changes behaviour. SDN also
publishes a **recommended order** - LizzyM Score, then WARS list builder, then
Application Cost, then Student Loan Debt - so the tools read as a workflow
rather than as an unordered menu. Ours were grouped by subject (Money,
Licensure, Practice), which tells a reader what each tool is ABOUT and nothing
at all about which one to open first.

WHY TWO SEQUENCES AND NOT ONE

A single chain would be wrong for half the audience. An associate three hundred
hours into three thousand and a licensed owner deciding whether to incorporate
do not share a first step, and pretending they do would put the Practice
Simulator - which asks for a rate you do not set - in front of someone who
cannot answer its first question.

    still accruing hours   3,000 Hours -> Job Advisor -> Cost of Living
    running a practice     Simulator -> Tax & Retirement -> Grow -> Cost of Living

Both end in the same place, because "what does a month here actually cost" is
the question underneath both, and both have the same optional coda - Working
Remotely, which reprices whatever you just worked out in eight other places.

THE HAND-OFF IS LIVE, NOT A LINK

Rule six of the content-block system: a block carries the reader's setup in the
href, so nothing is retyped. Every one of the seven tools already writes its own
state to `location.hash` on each keystroke, and every one filters what it reads
back against its own key list - so relaying the whole bag is safe: the target
takes `rate`, `sessions`, `weeksOff`, `filing` if it knows them and silently
drops the rest.

Six of the seven use a plain `k=v&k=v` hash. The Practice Simulator uses
`#s=<base64 of the whole state object>`, so the relay decodes it on the way out
and re-encodes on the way in. That is the only special case, and it is handled
in eleven lines rather than by coupling the pass to any page's internals.

The links update on `hashchange`, so a reader who types a rate and then looks
down finds it already in the link.

WHAT THIS PASS DOES NOT TOUCH

`practice-simulator.html` already has a richer hand-off - the `#nextroutes`
block, with three routes and live figures. Building a second one twenty pixels
away would repeat the mistake concept 04 made on the hubs, where the literal
reading of the concept printed the same destination twice in two card styles.
The simulator gets the sequence rail only, not the Next card.

Idempotent, guarded: every href is resolved against the filesystem before the
run is allowed to finish, and every colour is measured against the surface it
lands on.
"""
import os, re, sys

HERE = os.path.dirname(os.path.abspath(__file__))
SITE = os.path.dirname(HERE)
MARK = "<!-- _dev/tool_chain.py -->"
END = "<!-- /tool_chain -->"

INK = "#16211B"
PINE = "#2C6350"
GOLD = "#F6C560"
PAPER = "#F4F0E6"
CREAM = "#FBF9F3"
WHITE = "#FFFFFF"
MUTED = "#635E53"
FLOOR = 4.5

# (href, short name, what you put in, what it hands the next one)
SIM = ("practice-simulator.html", "Practice Simulator",
       "a rate and a caseload",
       "a real net figure, and twelve expense categories")
TAX = ("therapist-tax-strategy-california.html", "Tax &amp; Retirement",
       "that profit",
       "how much of the tax bill was optional")
GROW = ("grow-your-therapy-practice.html", "Grow Your Practice",
        "the rate, and how long a client stays",
        "what one client is worth, and the leakiest channel")
HOURS = ("amft-3000-hours-california.html", "3,000 Hours",
         "your working week",
         "the gate that is actually holding you, and a date")
ADVISOR = ("associate-mft-job-advisor.html", "Associate Job Advisor",
           "two offers",
           "take-home, real hourly worth, and which one licenses you sooner")
COL = ("therapist-cost-of-living-california.html", "Cost of Living",
       "what you earn",
       "one break-even figure for a month")
REMOTE = ("therapist-working-remotely-california.html", "Working Remotely",
          "the practice you just priced",
          "the same practice priced in eight places")

TRACKS = [
    ("assoc", "If you are still accruing hours",
     "You have a license date you cannot see and an offer you cannot compare. "
     "Both are arithmetic.",
     [HOURS, ADVISOR, COL]),
    ("owner", "If you are running a practice",
     "You know what you charge. Everything else &mdash; what it leaves you, what "
     "the tax bill did not have to be, where the next client comes from &mdash; "
     "follows from it.",
     [SIM, TAX, GROW, COL]),
]
CODA = REMOTE

# Which page hands off to which, and under which track's heading. The simulator
# is absent on purpose: it already has #nextroutes.
NEXT_OF = {
    HOURS[0]:   (ADVISOR, "assoc"),
    ADVISOR[0]: (COL,     "assoc"),
    TAX[0]:     (GROW,    "owner"),
    GROW[0]:    (COL,     "owner"),
    COL[0]:     (CODA,    "coda"),
}

TRACK_NAME = {"assoc": "still accruing hours",
              "owner": "running a practice",
              "coda": "wherever you landed"}


# ---------------------------------------------------------------- contrast

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


CHECKS = [
    ("track heading on cream", INK, CREAM, 3.0),
    ("step body on white", MUTED, WHITE, FLOOR),
    ("step body on cream", MUTED, CREAM, FLOOR),
    ("step name on white", INK, WHITE, FLOOR),
    ("hand-off label on white", PINE, WHITE, FLOOR),
    ("step number on pine", "#FFFFFF", PINE, FLOOR),
    ("coda ink on gold", INK, GOLD, FLOOR),
]

# ---------------------------------------------------------------- markup

CSS = """<style>/* _dev/tool_chain.py */
.tcseq{margin:26px 0 8px}
.tcseq .tck{font-family:'IBM Plex Mono',ui-monospace,monospace;font-size:11px;
  letter-spacing:.14em;text-transform:uppercase;color:%(muted)s;margin:0 0 6px}
.tcseq .tch{font-family:'Bricolage Grotesque',system-ui,sans-serif;font-weight:800;
  letter-spacing:-.032em;font-size:25px;line-height:1.14;color:%(ink)s;margin:0 0 6px}
.tcseq .tcd{font-size:15px;line-height:1.62;color:%(muted)s;margin:0 0 18px;max-width:62ch}
.tctrack{border:2px solid %(ink)s;border-radius:12px;background:#fff;
  box-shadow:6px 6px 0 %(ink)s;padding:17px 19px 15px;margin:0 0 20px}
.tctrack>h3{font-family:'Bricolage Grotesque',system-ui,sans-serif;font-weight:800;
  letter-spacing:-.028em;font-size:18px;color:%(ink)s;margin:0 0 5px;line-height:1.2}
.tctrack>p.tcw{font-size:14px;line-height:1.6;color:%(muted)s;margin:0 0 14px;max-width:60ch}
.tcsteps{list-style:none;margin:0;padding:0;counter-reset:tcs}
.tcstep{display:grid;grid-template-columns:30px 1fr;gap:12px;align-items:start;
  padding:11px 0;border-top:1px solid #E4DFD2}
.tcstep:first-child{border-top:0;padding-top:2px}
.tcnum{width:26px;height:26px;border-radius:50%%;background:%(pine)s;color:#fff;
  display:flex;align-items:center;justify-content:center;font-weight:700;font-size:13px;
  font-family:'IBM Plex Mono',ui-monospace,monospace}
.tcstep a{font-family:'Bricolage Grotesque',system-ui,sans-serif;font-weight:800;
  letter-spacing:-.02em;font-size:16px;color:%(ink)s;text-decoration:none;
  border-bottom:2px solid %(gold)s}
.tcstep a:hover{border-bottom-color:%(pine)s}
.tcstep p{font-size:13.6px;line-height:1.58;color:%(muted)s;margin:3px 0 0;max-width:58ch}
.tcstep .tcio{display:block;font-family:'IBM Plex Mono',ui-monospace,monospace;
  font-size:11.5px;letter-spacing:.02em;color:%(muted)s;margin-top:4px}
.tcstep .tcio b{color:%(ink)s;font-weight:600}
.tccoda{border:2px solid %(ink)s;border-radius:12px;background:%(gold)s;
  box-shadow:6px 6px 0 %(ink)s;padding:14px 17px;margin:0 0 6px}
.tccoda b{font-family:'Bricolage Grotesque',system-ui,sans-serif;font-weight:800;
  letter-spacing:-.02em;font-size:16px;color:%(ink)s;display:block}
.tccoda p{font-size:13.6px;line-height:1.56;color:%(ink)s;margin:3px 0 0;max-width:60ch}
.tccoda a{color:%(ink)s}
/* the per-tool hand-off */
.tcnext{border:2px solid %(ink)s;border-radius:12px;background:%(cream)s;
  box-shadow:6px 6px 0 %(ink)s;padding:17px 19px;margin:26px auto 4px;max-width:960px}
.tcnext .tck{font-family:'IBM Plex Mono',ui-monospace,monospace;font-size:11px;
  letter-spacing:.14em;text-transform:uppercase;color:%(pine)s;margin:0 0 6px}
.tcnext h2{font-family:'Bricolage Grotesque',system-ui,sans-serif;font-weight:800;
  letter-spacing:-.03em;font-size:21px;line-height:1.18;color:%(ink)s;margin:0 0 6px}
.tcnext p{font-size:14.4px;line-height:1.6;color:%(muted)s;margin:0 0 12px;max-width:62ch}
.tcnext .tcgo{display:inline-block;background:%(pine)s;color:#fff;font-weight:700;
  font-size:14.5px;text-decoration:none;border:2px solid %(ink)s;border-radius:9px;
  padding:9px 15px;box-shadow:4px 4px 0 %(ink)s}
.tcnext .tcgo:hover{background:#245244}
.tcnext .tcall{display:inline-block;margin-left:13px;font-size:13.6px;color:%(pine)s}
@media (max-width:640px){
  .tcstep{grid-template-columns:24px 1fr;gap:9px}
  .tcnum{width:22px;height:22px;font-size:12px}
  .tcseq .tch{font-size:21px}
}
</style>"""


# The relay. Reads whatever the current page has put in its own hash, hands it
# to the next tool in the form that tool reads.
SCRIPT = """<script>/* _dev/tool_chain.py */
(function(){
  var SIM = "practice-simulator.html";
  function bagFromHash(){
    var raw = location.hash.replace(/^#/, "");
    var bag = {};
    if (!raw) return bag;
    var m = /^s=([A-Za-z0-9\\-_]+)$/.exec(raw);
    if (m){
      /* The simulator keeps its whole state as one base64 blob. Unpack it so
         the flat tools can read the handful of keys they share. */
      try {
        var o = JSON.parse(decodeURIComponent(atob(
          m[1].replace(/-/g, "+").replace(/_/g, "/"))));
        Object.keys(o).forEach(function(k){
          var v = o[k];
          if (v === null || v === undefined || v === "") return;
          if (typeof v === "object") return;
          bag[k] = String(v);
        });
      } catch (e) {}
      return bag;
    }
    raw.split("&").forEach(function(p){
      var i = p.indexOf("="); if (i < 0) return;
      bag[p.slice(0, i)] = decodeURIComponent(p.slice(i + 1));
    });
    return bag;
  }
  function encodeFor(href, bag){
    var keys = Object.keys(bag);
    if (!keys.length) return href;
    if (href.indexOf(SIM) === 0){
      try {
        return href + "#s=" + btoa(encodeURIComponent(JSON.stringify(bag)))
          .replace(/\\+/g, "-").replace(/\\//g, "_").replace(/=+$/, "");
      } catch (e) { return href; }
    }
    return href + "#" + keys.map(function(k){
      return k + "=" + encodeURIComponent(bag[k]);
    }).join("&");
  }
  function paint(){
    var bag = bagFromHash();
    var links = document.querySelectorAll("a[data-tcto]");
    for (var i = 0; i < links.length; i++){
      links[i].setAttribute("href", encodeFor(links[i].getAttribute("data-tcto"), bag));
    }
  }
  paint();
  /* Every tool writes its state with history.replaceState, and replaceState
     does NOT fire hashchange - so listening for that alone captured whatever
     was in the URL at load and then went stale the moment anyone typed.
     Repainting on input and change covers all seven, because all seven rebind
     on exactly those events. */
  window.addEventListener("hashchange", paint);
  document.addEventListener("input", paint, true);
  document.addEventListener("change", paint, true);
})();
</script>"""


def esc(s):
    return s


def step_html(n, entry, up=""):
    href, name, takes, gives = entry
    return (
        '<li class="tcstep"><span class="tcnum" aria-hidden="true">%d</span>'
        '<div><a href="%s%s" data-tcto="%s%s">%s</a>'
        '<span class="tcio">takes <b>%s</b> &middot; hands on <b>%s</b></span>'
        '</div></li>' % (n, up, href, up, href, name, takes, gives))


def sequence_block(up=""):
    parts = [MARK, '<section class="tcseq" id="in-what-order">',
             '<p class="tck">In what order</p>',
             '<h2 class="tch">Seven tools, two sequences.</h2>',
             '<p class="tcd">Grouped by subject above, because that is how you '
             'find one. Here is the order they are actually useful in &mdash; and '
             'what each one hands the next. Whatever you type travels in the '
             'link, so nothing is entered twice.</p>']
    for _key, heading, why, steps in TRACKS:
        parts.append('<div class="tctrack"><h3>%s</h3><p class="tcw">%s</p>'
                     '<ol class="tcsteps">' % (heading, why))
        for i, st in enumerate(steps, 1):
            parts.append(step_html(i, st, up))
        parts.append('</ol></div>')
    parts.append(
        '<div class="tccoda"><b>Either way, one more:</b>'
        '<p><a href="%s%s" data-tcto="%s%s">%s</a> takes whatever you just '
        'worked out and reprices it in eight places, California included &mdash; '
        'the Board&rsquo;s own answer on who you may see from where, then the '
        'arithmetic.</p></div>'
        % (up, CODA[0], up, CODA[0], CODA[1]))
    parts.append('</section>')
    parts.append(END)
    return "".join(parts)


def next_block(this_href):
    nxt, track = NEXT_OF[this_href]
    href, name, takes, gives = nxt
    return "".join([
        MARK,
        '<section class="tcnext" aria-labelledby="tcnext-h">',
        '<p class="tck">Next, if you are %s</p>' % TRACK_NAME[track],
        '<h2 id="tcnext-h">%s</h2>' % name,
        '<p>It takes %s and gives you %s. What you have typed here travels in '
        'the link &mdash; you will not enter it twice.</p>' % (takes, gives),
        '<a class="tcgo" href="%s" data-tcto="%s">Open %s &rarr;</a>' % (href, href, name),
        '<a class="tcall" href="calculators.html#in-what-order">See the whole sequence</a>',
        '</section>', END])


def strip(s):
    return re.sub(re.escape(MARK) + r"[\s\S]*?" + re.escape(END), "", s)


def strip_css(s):
    return re.sub(r"\n?<style>/\* _dev/tool_chain\.py \*/[\s\S]*?</style>\n?", "", s) \
             .replace("\n" + SCRIPT, "").replace(SCRIPT, "")


def main():
    print("colours, measured:")
    bad = 0
    for label, fg, bg, floor in CHECKS:
        r = ratio(fg, bg)
        ok = r >= floor
        print("  %-24s %5.2f:1 (floor %.1f) %s" % (label, r, floor, "ok" if ok else "FAILS"))
        if not ok:
            bad += 1
    if bad:
        sys.exit("%d colour(s) under the floor" % bad)

    css = CSS % {"ink": INK, "pine": PINE, "gold": GOLD, "muted": MUTED,
                 "cream": CREAM}

    targets = ["calculators.html"] + sorted(NEXT_OF)
    for rel in targets:
        p = os.path.join(SITE, rel)
        if not os.path.exists(p):
            sys.exit("tool_chain: %s is missing - refusing to run" % rel)

    n = 0
    for rel in targets:
        p = os.path.join(SITE, rel)
        s = open(p, encoding="utf-8").read()
        orig = s
        s = strip_css(strip(s))

        if rel == "calculators.html":
            # After the intro prose, before the subject groups: a reader who has
            # just been told these are grouped by subject is exactly the reader
            # who should next be told what order to open them in.
            anchor = re.search(r'</section><section class="sec">', s)
            if not anchor:
                sys.exit("tool_chain: calculators.html has changed shape - "
                         "no </section><section class=\"sec\"> to insert before")
            i = anchor.start() + len("</section>")
            block = sequence_block()
        else:
            anchor = s.find('<!-- _dev/footer_band.py -->')
            if anchor < 0:
                anchor = s.lower().rfind("<footer")
            if anchor < 0:
                sys.exit("tool_chain: %s has no place to put the hand-off" % rel)
            i = anchor
            block = next_block(rel)

        s = s[:i] + block + s[i:]
        j = s.lower().rfind("</body>")
        s = s[:j] + css + "\n" + SCRIPT + "\n" + s[j:]
        if s != orig:
            open(p, "w", encoding="utf-8").write(s)
            n += 1
    print("\n%d page(s) written" % n)

    # ------------------------------------------------------------- guards
    bad = 0
    seen_hrefs = set()
    for rel in targets:
        s = open(os.path.join(SITE, rel), encoding="utf-8").read()
        if s.count(MARK) != 1 or s.count(END) != 1:
            print("GUARD %s: %d marks / %d ends" % (rel, s.count(MARK), s.count(END)))
            bad += 1
        body = re.search(re.escape(MARK) + r"([\s\S]*?)" + re.escape(END), s)
        if not body:
            print("GUARD %s: block missing" % rel)
            bad += 1
            continue
        for h in re.findall(r'data-tcto="([^"#]+)', body.group(1)):
            seen_hrefs.add(h)
            if not os.path.exists(os.path.join(os.path.dirname(os.path.join(SITE, rel)), h)):
                print("GUARD %s: data-tcto -> %s does not resolve" % (rel, h))
                bad += 1
        for h in re.findall(r'href="([^"#]+)\.html', body.group(1)):
            if not os.path.exists(os.path.join(os.path.dirname(os.path.join(SITE, rel)), h + ".html")):
                print("GUARD %s: href -> %s.html does not resolve" % (rel, h))
                bad += 1

    # Every one of the seven must appear somewhere in the sequence, or the page
    # claims "seven tools" and shows six.
    all_seven = {SIM[0], TAX[0], GROW[0], HOURS[0], ADVISOR[0], COL[0], REMOTE[0]}
    seq = open(os.path.join(SITE, "calculators.html"), encoding="utf-8").read()
    seqbody = re.search(re.escape(MARK) + r"([\s\S]*?)" + re.escape(END), seq).group(1)
    missing = sorted(h for h in all_seven if h not in seqbody)
    if missing:
        print("GUARD: the sequence does not mention %s" % ", ".join(missing))
        bad += 1

    if bad:
        sys.exit("\n%d problem(s)" % bad)
    print("guards clean - %d destinations, all resolving; all seven in the sequence"
          % len(seen_hrefs))


if __name__ == "__main__":
    main()
