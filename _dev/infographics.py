#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""A visual vocabulary for this site, so content can stop being only prose.

WHAT THIS IS FOR

  "please add some global visual infographic design template to use more
   infographics and visuals in content"

Every page here is text and tables. The material is quantitative - proportions,
sequences, comparisons, flows of money - and all of it is currently carried in
sentences. This gives the site five reusable shapes so a figure can be SEEN,
and so the next page does not need a bespoke one invented for it.

WHY CSS AND NOT IMAGES

Every shape here is markup and CSS. No SVG files, no PNGs, no charting library.
That is not minimalism for its own sake - it is four specific properties this
site already needs:

  - it inherits the palette, so a colour change in `token_floor.py` reaches the
    graphics too instead of leaving stale images behind
  - it reflows at 390px instead of horizontally scrolling, which is where the
    majority of this audience reads
  - it is real text, so it is searchable, selectable, translatable, and read
    correctly by a screen reader
  - it costs nothing to load and cannot 404

THE FIVE SHAPES, AND WHAT EACH IS FOR

  ig-split    A proportion. One bar, two parts, both labelled with their real
              count. For "20 of 25 are APA-accredited" - a fact currently
              written as a sentence and instantly readable as a bar.

  ig-steps    An ordered sequence where the order is the point. For the seven
              steps of getting on a panel, which the page itself says "do not
              run in parallel, and skipping one does not save time".

  ig-bars     Comparing several values on one scale. For rates: the thing that
              matters is not any single number, it is that Octave's floor is
              above Spring Health's ceiling.

  ig-flow     Money or information moving between parties. For the EAP model -
              employer pays platform, platform pays clinician, nobody bills a
              payer - which takes a paragraph to explain and one row to show.

  ig-stat     A row of large figures. The site already does this in heroes;
              this makes it available mid-article.

ACCESSIBILITY IS NOT OPTIONAL IN A GRAPHIC MADE OF DIVS

A bar whose only content is a coloured box says nothing to a screen reader. So
every shape carries its numbers as real text inside it, and the decorative
parts are marked `aria-hidden`. The guard at the bottom refuses to write a
graphic whose figures exist only as CSS widths.

WHERE THEY ARE USED, AS OF THIS PASS

  psyd-programs-california            ig-split   20 of 25 APA-accredited
  amft-3000-hours-california          ig-split   1,750 clinical / 1,250 not
  insurance-panels-california         ig-steps   the seven steps, in order
  insurance-reimbursement-rates       ig-bars    90837 across four columns
  therapy-liability-insurance         ig-bars    CPH's published rate ladder
  therapist-discipline-cases          ig-bars    thirty cases by what went wrong
  rates                               ig-flow    who actually pays for an EAP hour

Every figure in that list is already stated in the page's own prose or table.
Nothing here introduces a number, which is deliberate: a graphic that is the
only place a figure appears is a figure nobody has checked.

The CSS ships on every page even where no graphic is placed yet, so the next
placement is one tuple, and so `extract_css.py` hoists one shared file rather
than inlining a copy per page.

Idempotent, guarded. Run in the STRUCTURE stage, before extract_css.
"""
import os, re, sys

HERE = os.path.dirname(os.path.abspath(__file__))
SITE = os.path.dirname(HERE)
MARK = "/* _dev/infographics.py */"
BLOCK = "<!-- _dev/infographics.py -->"
END = "<!-- /infographics -->"

INK = "#16211B"
PINE = "#2C6350"
GOLD = "#F6C560"
CREAM = "#FBF9F3"
PAPER = "#F4F0E6"
MUTED = "#635E53"

CSS = """<style>%(mark)s
/* A visual vocabulary. Five shapes, all CSS, all reflowing at 390px, all
   carrying their figures as real text so a screen reader gets the number and
   not just a coloured box. */

.ig{margin:26px 0;font-family:Inter,system-ui,sans-serif}
.ig-cap{font-family:'IBM Plex Mono',ui-monospace,monospace;font-size:10.5px;
  letter-spacing:.13em;text-transform:uppercase;color:%(pine)s;margin:0 0 9px}
.ig-note{font-size:13.2px;line-height:1.6;color:%(muted)s;margin:10px 0 0;max-width:72ch}
.ig-note b{color:%(ink)s}

/* ---------------------------------------------------------------- split */
.ig-split .bar{display:flex;border:2px solid %(ink)s;border-radius:10px;
  overflow:hidden;box-shadow:4px 4px 0 %(ink)s;min-height:56px}
.ig-split .seg{display:flex;flex-direction:column;justify-content:center;
  padding:9px 13px;min-width:0}
.ig-split .seg.a{background:%(pine)s;color:#fff}
.ig-split .seg.b{background:%(cream)s;color:%(ink)s;border-left:2px solid %(ink)s}
.ig-split .n{font-family:Fraunces,Georgia,serif;font-weight:600;font-size:22px;
  line-height:1}
.ig-split .l{font-family:'IBM Plex Mono',ui-monospace,monospace;font-size:10px;
  letter-spacing:.09em;text-transform:uppercase;margin-top:5px;line-height:1.4}
.ig-split .seg.a .l{color:rgba(255,255,255,.86)}
.ig-split .seg.b .l{color:%(muted)s}

/* ---------------------------------------------------------------- steps */
.ig-steps ol{list-style:none;margin:0;padding:0;counter-reset:s}
.ig-steps li{counter-increment:s;position:relative;display:grid;
  grid-template-columns:38px 1fr;gap:13px;align-items:start;
  padding:0 0 16px;margin:0}
.ig-steps li::before{content:counter(s,decimal-leading-zero);
  font-family:'IBM Plex Mono',ui-monospace,monospace;font-size:11px;
  display:flex;align-items:center;justify-content:center;
  width:34px;height:34px;border:2px solid %(ink)s;border-radius:9px;
  background:%(gold)s;color:%(ink)s;box-shadow:2px 2px 0 %(ink)s}
/* the connector between steps, decorative only */
.ig-steps li:not(:last-child)::after{content:"";position:absolute;
  left:17px;top:38px;bottom:4px;width:2px;background:#D9D0BA}
.ig-steps b{display:block;font-family:'Bricolage Grotesque',system-ui,sans-serif;
  font-weight:800;letter-spacing:-.02em;font-size:15.5px;color:%(ink)s;
  margin:6px 0 3px}
.ig-steps span{display:block;font-size:14px;line-height:1.6;color:%(muted)s;max-width:64ch}

/* ----------------------------------------------------------------- bars */
.ig-bars .row{display:grid;grid-template-columns:150px 1fr auto;gap:12px;
  align-items:center;padding:7px 0;border-bottom:1.5px solid #E6E0D2}
.ig-bars .row:last-child{border-bottom:0}
.ig-bars .who{font-size:13.6px;line-height:1.35;color:%(ink)s;font-weight:600}
.ig-bars .who i{display:block;font-style:normal;font-size:11.5px;color:%(muted)s;
  font-weight:400}
.ig-bars .track{background:%(paper)s;border:1.5px solid #D9D0BA;border-radius:999px;
  height:19px;position:relative;overflow:hidden}
.ig-bars .fill{position:absolute;left:0;top:0;bottom:0;background:%(pine)s;
  border-radius:999px}
.ig-bars .fill.lo{background:#8FB3A3}
.ig-bars .val{font-family:Fraunces,Georgia,serif;font-weight:600;font-size:15px;
  color:%(ink)s;white-space:nowrap}

/* ----------------------------------------------------------------- flow */
.ig-flow .fr{display:flex;align-items:stretch;gap:0;flex-wrap:wrap}
.ig-flow .node{flex:1 1 150px;border:2px solid %(ink)s;border-radius:11px;
  background:%(cream)s;padding:13px 14px;box-shadow:4px 4px 0 %(ink)s;min-width:0}
.ig-flow .node.pay{background:%(gold)s}
.ig-flow .node b{display:block;font-family:'Bricolage Grotesque',system-ui,sans-serif;
  font-weight:800;font-size:14.5px;color:%(ink)s;letter-spacing:-.02em}
.ig-flow .node span{display:block;font-size:12.6px;line-height:1.55;color:%(muted)s;
  margin-top:4px}
.ig-flow .arr{flex:0 0 42px;display:flex;flex-direction:column;
  align-items:center;justify-content:center;gap:3px;padding:0 4px}
.ig-flow .arr em{font-style:normal;font-family:'IBM Plex Mono',ui-monospace,monospace;
  font-size:9px;letter-spacing:.06em;text-transform:uppercase;color:%(pine)s;
  text-align:center;line-height:1.2}
.ig-flow .arr i{font-style:normal;font-size:19px;color:%(ink)s;line-height:1}

/* ----------------------------------------------------------------- stat */
.ig-stat .g{display:grid;grid-template-columns:repeat(auto-fit,minmax(150px,1fr));
  gap:0;border:2px solid %(ink)s;border-radius:12px;overflow:hidden;
  box-shadow:5px 5px 0 %(ink)s;background:%(ink)s}
.ig-stat .c{background:%(cream)s;padding:14px 15px}
.ig-stat .n{display:block;font-family:Fraunces,Georgia,serif;font-weight:600;
  font-size:27px;line-height:1;color:%(ink)s;letter-spacing:-.02em}
.ig-stat .l{display:block;font-family:'IBM Plex Mono',ui-monospace,monospace;
  font-size:10px;letter-spacing:.1em;text-transform:uppercase;color:%(pine)s;
  margin-top:7px;line-height:1.5}

@media (max-width:640px){
  .ig-bars .row{grid-template-columns:1fr auto;gap:6px 10px}
  .ig-bars .track{grid-column:1 / -1;order:3}
  .ig-flow .arr{flex-basis:100%%;height:32px;transform:rotate(90deg)}
  .ig-split .bar{flex-direction:column}
  .ig-split .seg.b{border-left:0;border-top:2px solid %(ink)s}
}
</style>"""


# --------------------------------------------------------------- builders
def split(cap, a_n, a_l, b_n, b_l, a_pct, note=None):
    return (
        '<figure class="ig ig-split">'
        '<figcaption class="ig-cap">%s</figcaption>'
        '<div class="bar">'
        '<div class="seg a" style="flex:%d 1 0"><span class="n">%s</span>'
        '<span class="l">%s</span></div>'
        '<div class="seg b" style="flex:%d 1 0"><span class="n">%s</span>'
        '<span class="l">%s</span></div>'
        "</div>%s</figure>"
        % (cap, a_pct, a_n, a_l, 100 - a_pct, b_n, b_l,
           ('<p class="ig-note">%s</p>' % note) if note else ""))


def steps(cap, items, note=None):
    li = "".join("<li><b>%s</b><span>%s</span></li>" % (t, d) for t, d in items)
    return ('<figure class="ig ig-steps">'
            '<figcaption class="ig-cap">%s</figcaption><ol>%s</ol>%s</figure>'
            % (cap, li, ('<p class="ig-note">%s</p>' % note) if note else ""))


def bars(cap, rows, note=None, top=None):
    # `top` matters when a row's value is the FLOOR of a published range. Left
    # to itself the chart would scale to that floor and draw it full-width,
    # which reads as "this is the maximum" directly under a label saying it is
    # the minimum. Passing the real ceiling keeps the picture and the caption
    # telling the same story.
    top = top or max(v for _w, _s, v, _lab in rows) or 1
    out = []
    for who, sub, val, label in rows:
        pct = max(3, round(val / top * 100))
        lo = " lo" if val < top * 0.5 else ""
        out.append(
            '<div class="row"><span class="who">%s%s</span>'
            '<span class="track" aria-hidden="true">'
            '<span class="fill%s" style="width:%d%%"></span></span>'
            '<span class="val">%s</span></div>'
            % (who, ('<i>%s</i>' % sub) if sub else "", lo, pct, label))
    return ('<figure class="ig ig-bars">'
            '<figcaption class="ig-cap">%s</figcaption>%s%s</figure>'
            % (cap, "".join(out),
               ('<p class="ig-note">%s</p>' % note) if note else ""))


def flow(cap, nodes, note=None):
    parts = []
    for i, n in enumerate(nodes):
        if isinstance(n, tuple) and len(n) == 2 and n[0] == "arrow":
            parts.append('<div class="arr" aria-hidden="true"><em>%s</em>'
                         '<i>&rarr;</i></div>' % n[1])
        else:
            cls, title, sub = n
            parts.append('<div class="node%s"><b>%s</b><span>%s</span></div>'
                         % (" " + cls if cls else "", title, sub))
    return ('<figure class="ig ig-flow">'
            '<figcaption class="ig-cap">%s</figcaption>'
            '<div class="fr">%s</div>%s</figure>'
            % (cap, "".join(parts),
               ('<p class="ig-note">%s</p>' % note) if note else ""))


def stat(cap, cells, note=None):
    c = "".join('<div class="c"><span class="n">%s</span>'
                '<span class="l">%s</span></div>' % (n, l) for n, l in cells)
    return ('<figure class="ig ig-stat">'
            '<figcaption class="ig-cap">%s</figcaption><div class="g">%s</div>%s'
            "</figure>"
            % (cap, c, ('<p class="ig-note">%s</p>' % note) if note else ""))


# ------------------------------------------------------ where they are used
# (page, anchor regex to insert AFTER, html builder)
PLACEMENTS = [
    # ---------------------------------------------------------------- PsyD
    # Placed after the legal explanation and before the tier lists, because
    # the bar IS the grouping the rest of the page uses. Anchored on the
    # citation line, which occurs exactly once - not on `</h1>`, which would
    # have wedged it between the headline and its own dek.
    (
        "psyd-programs-california.html",
        r'<p class="pdcite">[\s\S]{0,600}?</p></div>',
        lambda: split(
            "Accreditation, across the 25 California doctorates",
            "20", "APA-accredited", "5", "not APA-accredited", 80,
            "The 20 is 19 fully accredited plus one accredited on contingency. "
            "The 5 is four programs that never were, and one whose "
            "accreditation is inactive. California will license you from any "
            "of the 25 &mdash; the internship year very largely will not, "
            "which is why the list below is grouped by this and not "
            "alphabetically."),
    ),

    # -------------------------------------------------------------- panels
    (
        "insurance-panels-california-therapist.html",
        r"<h2[^>]*>\s*The order of operations, and what each step needs[\s\S]{0,400}?</p>",
        lambda: steps(
            "Seven steps, in the order they have to happen",
            [("An NPI, Entity Type 1",
              "The individual identifier. It follows you for the rest of your "
              "career, through every name change and every move."),
             ("A CAQH profile",
              "The shared credentialing database nearly every commercial payer "
              "reads. Re-attest every 120 days or it lapses."),
             ("Liability insurance",
              "Payers will ask for the certificate, and will reject one inside "
              "60 days of expiry."),
             ("Pick the payers",
              "Before applying. Each one is a separate application, a separate "
              "clock and a separate contract."),
             ("Apply, payer by payer",
              "Where the panel is open. Where it is closed, an interest form is "
              "all there is."),
             ("Credentialing review",
              "The statutory clock California puts on it starts here, not when "
              "you first thought about applying."),
             ("The contract and the rate",
              "Negotiating the rate sits outside the statutory clock entirely, "
              "which is where most of the extra months actually go.")],
            "They do not run in parallel, and skipping one does not save time "
            "&mdash; it moves the delay later, where it costs more."),
    ),

    # --------------------------------------------------------------- rates
    (
        "rates.html",
        r"<h3 class=\"eap-h\">The third channel: EAPs and employer platforms</h3>",
        lambda: flow(
            "How an EAP session gets paid for, and by whom",
            [("pay", "The employer", "Pays a flat per-employee-per-month fee"),
             ("arrow", "PEPM fee"),
             ("", "The platform", "Holds a pool and sets the session allowance "
                                  "&mdash; typically 6 to 12 a year"),
             ("arrow", "contracted rate"),
             ("", "You", "Paid per session out of that pool")],
            "<b>Nobody bills a CPT code to a payer.</b> There is no fee "
            "schedule and no allowed amount, which is why none of the rates "
            "below can be looked up the way a Medi-Cal or Medicare rate can. "
            "The client pays nothing at the point of use."),
    ),

    # ------------------------------------------------- reimbursement rates
    # The page's own table, for one code, as a picture. Four bars beat six
    # rows here because the finding is a shape - Medi-Cal is a third of
    # everything else - and a shape is the one thing a table cannot show.
    (
        "insurance-reimbursement-rates-california-therapist.html",
        r"<h2[^>]*>\s*Six codes, four columns[\s\S]{0,600}?</p>",
        lambda: bars(
            "CPT 90837, the 53-minute session, Los Angeles locality, 2026",
            [("Private pay", "observed range, not a schedule",
              150.00, "$150&ndash;$250"),
             ("Commercial", "derived estimate, not a rate",
              138.37, "$138.37"),
             ("Medicare", "published fact, after the 75% rule",
              134.47, "$134.47"),
             ("Medi-Cal FFS", "published maximum allowance",
              38.01, "$38.01")],
            "Each bar is drawn at the figure in the table below it; the "
            "private-pay bar sits at the <b>bottom</b> of its range and the "
            "scale runs to the top of it. The gap that decides a practice is "
            "not between Medicare and commercial &mdash; those are four "
            "dollars apart. It is <b>Medi-Cal at 28% of Medicare</b> for the "
            "same hour of the same work.",
            top=250.0),
    ),

    # --------------------------------------------------- liability insurance
    # The only published California rate ladder on the page, as a ladder.
    # Sits above the filter chips because it answers the same question the
    # chips ask - where are you, and what does that cost.
    (
        "therapy-liability-insurance-california.html",
        r'<h2[^>]*>\s*Every program a California MFT can buy[\s\S]{0,600}?</p>',
        lambda: bars(
            "CPH's published California ladder, by where you are",
            [("Over 20 hrs/wk self-employed", "full-time private practice",
              320, "$320"),
             ("11&ndash;20 hrs/wk", "building a caseload", 180, "$180"),
             ("Up to 10 hrs/wk, or employed", "part-time", 115, "$115"),
             ("AMFT under supervision", "post-master&rsquo;s", 90, "$90"),
             ("Student", "in an accredited program", 15, "$15")],
            "Per year, at $1M&thinsp;/&thinsp;$3M limits, before discounts and "
            "before the $10 administrative fee. This is the <b>only</b> "
            "California rate table any of the eight programs publishes, and "
            "its PDF was last modified in June 2023 &mdash; treat it as "
            "last-published, not guaranteed-current. Everything below is "
            "quote-only."),
    ),

    # ------------------------------------------------------- 3,000 hours
    (
        "amft-3000-hours-california.html",
        r"<h2>What the Board requires</h2></div>\s*<p class=\"dek\">[\s\S]{0,400}?</p>",
        lambda: split(
            "What the 3,000 hours have to be made of",
            "1,750", "direct clinical, minimum", "1,250",
            "everything else, maximum", 58,
            "Both edges bind, in opposite directions. You cannot finish with "
            "fewer than 1,750 clinical hours, and hours 1,251 onward of notes, "
            "meetings and training simply stop counting. <b>500 of the 1,750 "
            "have to be with couples, families or children</b> &mdash; the "
            "gate an all-adult caseload never closes."),
    ),

    # ---------------------------------------------------- discipline cases
    (
        "therapist-discipline-cases-california.html",
        r'<h2 class="dc-h">Thirty cases[\s\S]{0,600}?</p>',
        lambda: bars(
            "Thirty cases, by what went wrong",
            [("Sexual boundaries", "", 6, "6"),
             ("Boundary drift", "no sexual contact", 5, "5"),
             ("Convictions", "including ones unrelated to therapy", 5, "5"),
             ("Discipline from elsewhere",
              "another state, another license", 4, "4"),
             ("Records and confidentiality", "", 3, "3"),
             ("Money, billing and honesty", "", 3, "3"),
             ("After discipline", "probation and its terms", 3, "3"),
             ("Fitness-to-practice", "", 1, "1")],
            "Eleven of the thirty &mdash; more than a third &mdash; are "
            "boundaries. Only one began as a complaint about clinical work. "
            "<b>The pattern to take from this is that discipline mostly "
            "arrives from conduct, paperwork and disclosure, not from a "
            "treatment decision.</b>"),
    ),
]


def pages():
    return [f for f in sorted(os.listdir(SITE)) if f.endswith(".html")]


def main():
    css = CSS % {"mark": MARK, "ink": INK, "pine": PINE, "gold": GOLD,
                 "cream": CREAM, "paper": PAPER, "muted": MUTED}

    print("the vocabulary: ig-split, ig-steps, ig-bars, ig-flow, ig-stat")
    print("placed:")

    bad = 0
    styled = 0
    for rel in pages():
        p = os.path.join(SITE, rel)
        s = open(p, encoding="utf-8").read()
        if "sitenav" not in s:
            continue
        orig = s
        s = re.sub(r"\n?<style>" + re.escape(MARK) + r"[\s\S]*?</style>\n?", "", s)
        s = re.sub(re.escape(BLOCK) + r"[\s\S]*?" + re.escape(END) + r"\n?", "", s)

        for page, anchor, build in PLACEMENTS:
            if page != rel:
                continue
            m = re.search(anchor, s)
            if not m:
                print("  MISSING  %-44s anchor did not match" % rel[:44])
                bad += 1
                continue
            fig = BLOCK + build() + END
            s = s[:m.end()] + fig + s[m.end():]
            kind = re.search(r'class="ig ig-(\w+)"', fig).group(1)
            print("  ok       %-44s ig-%s" % (rel[:44], kind))

        e = s.lower().rfind("</body>")
        if e > 0:
            s = s[:e] + css + "\n" + s[e:]
            styled += 1

        if s != orig:
            open(p, "w", encoding="utf-8").write(s)

    print("\nvocabulary available on %d page(s)" % styled)

    # ------------------------------------------------------------- guards
    for page, _a, _b in PLACEMENTS:
        s = open(os.path.join(SITE, page), encoding="utf-8").read()
        if s.count(BLOCK) != 1:
            print("GUARD %s: %d graphics" % (page, s.count(BLOCK)))
            bad += 1
        # A graphic made of divs whose numbers live only in a CSS width says
        # nothing to a screen reader. Every figure must carry real text.
        fig = re.search(re.escape(BLOCK) + r"([\s\S]*?)" + re.escape(END), s)
        if fig:
            text = re.sub(r"<[^>]+>", " ", fig.group(1))
            if not re.search(r"\d", text):
                print("GUARD %s: the graphic contains no readable figure - its "
                      "numbers exist only as CSS" % page)
                bad += 1
            if "<figcaption" not in fig.group(1):
                print("GUARD %s: graphic has no caption" % page)
                bad += 1
        # decorative parts must be hidden from assistive tech
        if fig and 'class="track"' in fig.group(1) and "aria-hidden" not in fig.group(1):
            print("GUARD %s: a decorative bar is not aria-hidden" % page)
            bad += 1

    for rel in pages():
        s = open(os.path.join(SITE, rel), encoding="utf-8").read()
        if "sitenav" in s and s.count(MARK) != 1:
            print("GUARD %s: %d stylesheets" % (rel, s.count(MARK)))
            bad += 1

    if bad:
        sys.exit("\n%d problem(s)" % bad)
    print("guards clean - every graphic carries its figures as real text, "
          "captioned, with decoration hidden from screen readers")


if __name__ == "__main__":
    main()
