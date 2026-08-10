#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Concept 06 - the stage router, built as a tab control over the section that
already half-existed.

WHAT WAS THERE

`resources.html` already carries **Where you are right now**: three situations -
Pre-licensed, Newly licensed, Running a practice - three links each, with a
standfirst that argues for the restraint: *"the commonest way to lose a reader
is to hand them the right answer to somebody else's question."* Nine curated
entry points into 131 pages.

The instinct is to add a second, bigger router. That is the mistake concept 04
made on the hubs, where the literal reading printed the same destination twice
in two card styles twenty pixels apart. So this pass **upgrades the section that
exists** and adds nothing beside it.

WHY MORE LINKS IS NOT A REVERSAL OF THAT ARGUMENT

The three-each rule comes from Hick's law, and the content-block doc states it
precisely: *"Hick's law bites on options presented **together**."* That is the
whole load-bearing word. A tab control never presents them together - a reader
sees one situation and six links, never six situations and thirty-six. It is
why Kitces can run seven tabs of six on a single widget and why we could not run
six cards of six as a wall.

So the restraint is kept and the coverage triples: six situations, five or six
pages each, one visible at a time.

The three original situations were also load-bearing in the wrong direction:
they start at *pre-licensed*, so someone still choosing between an MFT and a
PsyD - the largest single body of pages on this site, 78 schools and 25
doctorates - had no entry at all, and someone deciding whether to leave
California had none either.

EVERY LABEL IS THE DESTINATION'S OWN WORDS

Rule three of the content-block system: scent breaks when the card label and the
landing h1 disagree. Every card here prints the destination page's own
`ts:question` and its own `ts:number` - the same fields that drive the library
and the hub insights - so the label cannot drift from the page. Nothing is
retyped here, which means nothing here can go stale independently. The build
refuses to run if any listed page is missing either field.

LINKABLE

`#where=<key>` selects a tab on load, and choosing one rewrites the hash. That
is what lets the home page's three audience cards point *into* this widget
rather than duplicating it.

PROGRESSIVE ENHANCEMENT

The panels ship visible. The script hides all but one. With JavaScript off the
section degrades to the long list it replaced - more than the reader needed, but
never less, and every link still works. Arrow keys move between tabs; the
tablist is a real ARIA tablist rather than a set of divs.

Idempotent, guarded.
"""
import os, re, sys

HERE = os.path.dirname(os.path.abspath(__file__))
SITE = os.path.dirname(HERE)
PAGE = os.path.join(SITE, "resources.html")
HOME = os.path.join(SITE, "index.html")
MARK = "<!-- _dev/stage_router.py -->"
END = "<!-- /stage_router -->"

INK = "#16211B"
PINE = "#2C6350"
GOLD = "#F6C560"
CREAM = "#FBF9F3"
WHITE = "#FFFFFF"
MUTED = "#635E53"
FLOOR = 4.5

TOOLS = {
    "practice-simulator.html", "therapist-tax-strategy-california.html",
    "grow-your-therapy-practice.html", "associate-mft-job-advisor.html",
    "amft-3000-hours-california.html", "therapist-cost-of-living-california.html",
    "therapist-working-remotely-california.html",
}
DIRECTORIES = {"mft-programs-california.html", "psyd-programs-california.html",
               "psychedelic-therapy-training-california.html"}

# (key, tab label, panel heading, one line on who this is)
# then the pages, in the order a person in that situation meets them.
STAGES = [
    ("program", "Choosing a program",
     "You have not started yet",
     "Deciding between an MFT and a doctorate, between schools, and whether "
     "California arithmetic works at all.",
     ["mft-programs-california.html",
      "psyd-programs-california.html",
      "become-an-mft-california.html",
      "psychedelic-therapy-training-california.html",
      "therapist-cost-of-living-california.html"]),
    ("assoc", "Accruing hours",
     "Registered, and counting",
     "An AMFT, ASW or APCC weighing a placement against a license date.",
     ["amft-3000-hours-california.html",
      "associate-mft-job-advisor.html",
      "become-an-mft-california.html",
      "bbs-fees-california-2026.html",
      "continuing-education-california-lmft.html"]),
    ("newly", "Newly licensed",
     "First year on your own license",
     "The practice exists on paper. Now it needs a structure, a system and "
     "somebody to pay it.",
     ["practice-simulator.html",
      "therapist-llc-california.html",
      "cost-of-incorporating-california-therapist.html",
      "insurance-panels-california-therapist.html",
      "superbills-good-faith-estimate-california-therapist.html",
      "simplepractice-california-therapists.html"]),
    ("caseload", "Filling the week",
     "The license is fine; the calendar is not",
     "Empty hours, and the question of what to charge for the full ones.",
     ["grow-your-therapy-practice.html",
      "rates.html",
      "insurance-reimbursement-rates-california-therapist.html",
      "headway-for-california-therapists.html",
      "headway-alma-grow-therapy-compared-california.html"]),
    ("tax", "Paying too much tax",
     "The practice works, the bill hurts",
     "A profitable year, and the growing suspicion that some of the tax on it "
     "was optional.",
     ["therapist-tax-strategy-california.html",
      "solo-401k-sep-simple-california-therapist.html",
      "therapist-tax-deductions-california.html",
      "s-corp-sdi-california-therapist.html",
      "home-office-deduction-california-therapist.html",
      "quarterly-estimated-taxes-california-therapist.html"]),
    ("beyond", "Growing, or leaving",
     "Past what one person can see",
     "Employing somebody, changing the software under the practice, or running "
     "the whole thing from somewhere else.",
     ["hiring-first-associate-california-therapist.html",
      "therapynotes-vs-simplepractice-california.html",
      "therapist-working-remotely-california.html",
      "s-corp-salary-social-security-therapist.html",
      "therapist-cost-of-living-california.html"]),
]

# The home page's three audience cards point into the matching tab instead of
# repeating the list.
# Four, not three. The first three all assume the reader is already in the
# profession - registered, licensed, or growing - and the site's largest body of
# work by page count is the 66 school pages, the two programme directories and
# the route guide, which serve somebody who has not started. That audience had
# no door on the home page at all, while the router has had a "Choosing a
# programme" stage for it the whole time. The card was the missing half.
HOME_ROUTES = [
    ("Considering the path", "program"),
    ("Registered associates", "assoc"),
    ("Solo private practice", "newly"),
    ("Practices with room to grow", "tax"),
]


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
    ("tab label, resting", MUTED, CREAM, FLOOR),
    ("tab label, selected", "#FFFFFF", PINE, FLOOR),
    ("card question on white", INK, WHITE, FLOOR),
    ("card figure on white", PINE, WHITE, FLOOR),
    ("panel standfirst on cream", MUTED, CREAM, FLOOR),
    ("kind chip on gold", INK, GOLD, FLOOR),
]

CSS = """<style>/* _dev/stage_router.py */
.srtabs{display:flex;gap:7px;overflow-x:auto;padding:2px 2px 9px;margin:0 0 14px;
  scrollbar-width:none;-webkit-overflow-scrolling:touch;scroll-snap-type:x proximity}
.srtabs::-webkit-scrollbar{display:none}
.srtab{flex:0 0 auto;scroll-snap-align:start;font-family:'IBM Plex Mono',ui-monospace,monospace;
  font-size:12.5px;letter-spacing:.01em;font-weight:500;color:%(muted)s;background:%(cream)s;
  border:2px solid %(ink)s;border-radius:9px;padding:8px 12px;cursor:pointer;
  box-shadow:3px 3px 0 %(ink)s;white-space:nowrap}
.srtab:hover{background:#F1EDE0}
.srtab[aria-selected="true"]{background:%(pine)s;color:#fff;box-shadow:3px 3px 0 %(ink)s}
.srpanel{border:2px solid %(ink)s;border-radius:12px;background:%(cream)s;
  box-shadow:6px 6px 0 %(ink)s;padding:16px 18px 15px}
.srpanel+.srpanel{margin-top:14px}
.srph{font-family:'Bricolage Grotesque',system-ui,sans-serif;font-weight:800;
  letter-spacing:-.028em;font-size:19px;color:%(ink)s;margin:0 0 4px;line-height:1.2}
.srps{font-size:14px;line-height:1.58;color:%(muted)s;margin:0 0 14px;max-width:62ch}
.srg{display:grid;grid-template-columns:repeat(auto-fit,minmax(240px,1fr));gap:11px}
.src{display:block;background:#fff;border:2px solid %(ink)s;border-radius:10px;
  padding:12px 13px 11px;text-decoration:none;box-shadow:4px 4px 0 %(ink)s}
.src:hover{transform:translate(-2px,-2px);box-shadow:6px 6px 0 %(ink)s}
.src b{display:block;font-family:'Bricolage Grotesque',system-ui,sans-serif;
  font-weight:800;letter-spacing:-.02em;font-size:15px;line-height:1.24;color:%(ink)s}
.src .srn{display:block;font-family:'Fraunces',Georgia,serif;font-size:14.5px;
  color:%(pine)s;margin-top:6px;line-height:1.3}
.src .srk{display:inline-block;margin-top:9px;font-family:'IBM Plex Mono',ui-monospace,monospace;
  font-size:10.5px;letter-spacing:.12em;text-transform:uppercase;color:%(ink)s;
  background:%(gold)s;border:1.5px solid %(ink)s;border-radius:5px;padding:2px 6px}
.src .srk.srk-read{background:#EAF3DE}
.src .srk.srk-dir{background:#E6EFF6}
@media (max-width:640px){
  .srpanel{padding:14px 14px 13px}
  .srg{grid-template-columns:1fr}
}
</style>"""

SCRIPT = """<script>/* _dev/stage_router.py */
(function(){
  var list = document.querySelector('.srtabs');
  if (!list) return;
  var tabs = [].slice.call(list.querySelectorAll('.srtab'));
  var panels = [].slice.call(document.querySelectorAll('.srpanel'));
  if (!tabs.length || tabs.length !== panels.length) return;
  function select(key, focus){
    var hit = false;
    tabs.forEach(function(t, i){
      var on = t.getAttribute('data-sr') === key;
      if (on) hit = true;
      t.setAttribute('aria-selected', on ? 'true' : 'false');
      t.setAttribute('tabindex', on ? '0' : '-1');
      panels[i].hidden = !on;
    });
    if (!hit) return select(tabs[0].getAttribute('data-sr'), focus);
    if (focus){
      var el = list.querySelector('[aria-selected="true"]');
      if (el) el.focus();
    }
  }
  tabs.forEach(function(t, i){
    t.addEventListener('click', function(){
      var k = t.getAttribute('data-sr');
      select(k, false);
      try { history.replaceState(null, '', '#where=' + k); } catch (e) {}
    });
    t.addEventListener('keydown', function(e){
      var d = e.key === 'ArrowRight' ? 1 : e.key === 'ArrowLeft' ? -1 : 0;
      if (!d) return;
      e.preventDefault();
      var n = (i + d + tabs.length) % tabs.length;
      select(tabs[n].getAttribute('data-sr'), true);
    });
  });
  function fromHash(){
    var m = /[#&]where=([a-z]+)/.exec(location.hash);
    return m ? m[1] : tabs[0].getAttribute('data-sr');
  }
  select(fromHash(), false);
  window.addEventListener('hashchange', function(){ select(fromHash(), false); });
})();
</script>"""


def meta(rel, name):
    p = os.path.join(SITE, rel)
    if not os.path.exists(p):
        return None
    s = open(p, encoding="utf-8").read()
    m = re.search(r'name="ts:%s"\s+content="([^"]*)"' % name, s)
    return m.group(1) if m else None


def kind(rel):
    if rel in TOOLS:
        return ("Calculator", "")
    if rel in DIRECTORIES:
        return ("Directory", " srk-dir")
    return ("Read", " srk-read")


def build():
    tabs, panels = [], []
    for i, (key, tablabel, heading, who, pages) in enumerate(STAGES):
        tabs.append(
            '<button class="srtab" type="button" role="tab" id="srt-%s" '
            'data-sr="%s" aria-controls="srp-%s" aria-selected="%s">%s</button>'
            % (key, key, key, "true" if i == 0 else "false", tablabel))
        cards = []
        for rel in pages:
            q, n = meta(rel, "question"), meta(rel, "number")
            k, cls = kind(rel)
            cards.append(
                '<a class="src" href="%s"><b>%s</b>'
                '<span class="srn">%s</span>'
                '<span class="srk%s">%s</span></a>' % (rel, q, n, cls, k))
        panels.append(
            '<div class="srpanel" role="tabpanel" id="srp-%s" '
            'aria-labelledby="srt-%s"><h3 class="srph">%s</h3>'
            '<p class="srps">%s</p><div class="srg">%s</div></div>'
            % (key, key, heading, who, "".join(cards)))
    return (MARK
            + '<div class="srtabs" role="tablist" aria-label="Where you are">%s</div>'
            % "".join(tabs)
            + "".join(panels) + END)


SUB_NEW = ('<p class="sub">An associate and someone eight years into a practice '
           'need different pages, and the commonest way to lose a reader is to '
           'hand them the right answer to somebody else&rsquo;s question. Pick '
           'the one that describes this week; the rest stay out of the way.</p>')


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

    # Refuse to build a card whose label would have to be invented.
    missing = []
    for _k, _t, _h, _w, pages in STAGES:
        for rel in pages:
            if not os.path.exists(os.path.join(SITE, rel)):
                missing.append("%s does not exist" % rel)
                continue
            for f in ("question", "number"):
                if not meta(rel, f):
                    missing.append("%s has no ts:%s" % (rel, f))
    if missing:
        for m in sorted(set(missing)):
            print("  MISSING %s" % m)
        sys.exit("refusing to run: %d card(s) would need invented copy"
                 % len(set(missing)))

    s = open(PAGE, encoding="utf-8").read()
    orig = s
    s = re.sub(re.escape(MARK) + r"[\s\S]*?" + re.escape(END), "", s)
    s = re.sub(r"\n?<style>/\* _dev/stage_router\.py \*/[\s\S]*?</style>\n?", "", s)
    s = re.sub(r"\n?<script>/\* _dev/stage_router\.py \*/[\s\S]*?</script>\n?", "", s)

    i = s.find("Where you are right now")
    if i < 0:
        sys.exit("stage_router: resources.html no longer has the section to upgrade")
    a = s.find('<div class="rail">', i)
    b = s.find('<div class="hubnl">', i)
    if a < 0 or b < 0 or b < a:
        # Already upgraded on a previous run: our own block sits between the
        # standfirst and the newsletter card.
        a = s.find('<p class="sub">', i)
        a = s.find("</p>", a) + len("</p>")
        b = s.find('<div class="hubnl">', i)
        if a < len("</p>") or b < 0:
            sys.exit("stage_router: cannot find where the rails end and the "
                     "newsletter card begins")
    s = s[:a] + build() + "\n" + s[b:]

    # The standfirst argued for three-each. It now has to argue for a control.
    j = s.find("Where you are right now")
    k0 = s.find('<p class="sub">', j)
    k1 = s.find("</p>", k0) + len("</p>")
    if k0 > 0:
        s = s[:k0] + SUB_NEW + s[k1:]
    # "Three each, on purpose" is no longer true.
    s = s.replace("<span>Three each, on purpose</span>",
                  "<span>One situation at a time</span>", 1)

    e = s.lower().rfind("</body>")
    s = s[:e] + (CSS % {"ink": INK, "pine": PINE, "gold": GOLD,
                        "muted": MUTED, "cream": CREAM}) + "\n" + SCRIPT + "\n" + s[e:]
    if s != orig:
        open(PAGE, "w", encoding="utf-8").write(s)
        print("\nresources.html: %d situations, %d cards"
              % (len(STAGES), sum(len(p) for *_x, p in STAGES)))

    # Home page: point the three audience cards into the matching tab rather
    # than growing a second router underneath them.
    h = open(HOME, encoding="utf-8").read()
    horig = h
    n = 0

    # THE BUG THIS REPLACES, BECAUSE IT WAS VISIBLE AND UGLY.
    #
    # The extra link used to be inserted as a SIBLING of the audience card. The
    # cards are direct children of `.lgrid.lg3`, a three-column grid - so adding
    # one sibling per card gave the grid six children, and they flowed
    #
    #     row 1:  card 1   link 1   card 2
    #     row 2:  link 2   card 3   link 3
    #
    # Every link ended up in a different cell from the card it belonged to, with
    # a large hole in the middle of the section. Nothing errored: the markup was
    # valid, the links worked, and the only symptom was that it looked broken.
    #
    # `.laud` is itself an <a>, so the link cannot be nested inside it. The card
    # and its link are therefore wrapped in a div, and THAT is the grid child.
    #
    # Stripped first, both shapes, so this is idempotent over the old output.
    h = re.sub(r'<a class="srmore"[^>]*>[\s\S]*?</a>', "", h)
    h = re.sub(r'<div class="srpair">([\s\S]*?)</div>', r"\1", h)

    for label, key in HOME_ROUTES:
        # The card is the <a class="laud"> whose own text carries the label.
        m = None
        for c in re.finditer(r'<a class="laud"[^>]*>[\s\S]*?</a>', h):
            if label in c.group(0):
                m = c
                break
        if not m:
            continue
        h = (h[:m.start()]
             + '<div class="srpair">' + m.group(0)
             + '<a class="srmore" href="resources.html#where=%s">'
               'Everything for this situation &rarr;</a>' % key
             + "</div>"
             + h[m.end():])
        n += 1

    h = re.sub(r"\n?<style>/\* _dev/stage_router\.py \*/[\s\S]*?</style>\n?", "", h)
    if n:
        e = h.lower().rfind("</body>")
        h = h[:e] + ('<style>/* _dev/stage_router.py */\n'
                     '/* The pair is the grid child, not the card. See the note '
                     'in the pass. */\n'
                     '.srpair{display:flex;flex-direction:column;align-items:stretch}\n'
                     '.srpair>.laud{flex:1 1 auto}\n'
                     '.srmore{display:block;margin-top:9px;font-size:13px;'
                     'color:%s;text-decoration:none;border-bottom:1px solid #D8D0BC;'
                     'width:max-content}\n'
                     '.srmore:hover{border-bottom-color:%s}\n</style>\n'
                     % (PINE, PINE)) + h[e:]
    if h != horig:
        open(HOME, "w", encoding="utf-8").write(h)
    print("index.html: %d audience card(s) routed into the widget" % n)

    # -------------------------------------------------------------- guards
    bad = 0
    s = open(PAGE, encoding="utf-8").read()
    if s.count(MARK) != 1 or s.count(END) != 1:
        print("GUARD resources.html: %d marks / %d ends" % (s.count(MARK), s.count(END)))
        bad += 1
    body = re.search(re.escape(MARK) + r"([\s\S]*?)" + re.escape(END), s)
    if not body:
        print("GUARD: block missing")
        bad += 1
    else:
        blk = body.group(1)
        for h2 in re.findall(r'class="src" href="([^"]+)"', blk):
            if not os.path.exists(os.path.join(SITE, h2)):
                print("GUARD: %s does not resolve" % h2)
                bad += 1
        ntab = len(re.findall(r'role="tab"', blk))
        npan = len(re.findall(r'role="tabpanel"', blk))
        if ntab != npan or ntab != len(STAGES):
            print("GUARD: %d tabs, %d panels, %d stages" % (ntab, npan, len(STAGES)))
            bad += 1
        for key, _t, _h, _w, _p in STAGES:
            if ('id="srt-%s"' % key) not in blk or ('id="srp-%s"' % key) not in blk:
                print("GUARD: tab/panel pair %s incomplete" % key)
                bad += 1
    if "Three each, on purpose" in s:
        print("GUARD: the old 'three each' promise survives a six-tab widget")
        bad += 1
    hh = open(HOME, encoding="utf-8").read()
    for _label, key in HOME_ROUTES:
        if ("resources.html#where=%s" % key) not in hh:
            print("GUARD index.html: no route to #where=%s" % key)
            bad += 1
    if hh.count("_dev/stage_router.py") > 1:
        print("GUARD index.html: style block duplicated")
        bad += 1
    if bad:
        sys.exit("\n%d problem(s)" % bad)
    print("guards clean")


if __name__ == "__main__":
    main()
