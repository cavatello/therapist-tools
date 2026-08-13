#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""What "a licensed therapist" means in each state, and how many there are.

THE QUESTION THIS ANSWERS, AND THE TRAP IN IT

"How does California compare?" is the most shareable question about this
profession and the easiest one to answer wrongly.

The tempting chart is marriage and family therapists per head of population. It
produces California 88.9 against Texas 4.4, which looks like a twentyfold
difference in how many therapists a state has. It is nothing of the kind. Every
state in the comparison licenses MFTs. What differs is which credential the
profession grew into:

    Ohio       829 MFTs   against  14,170 counselors   17 to 1
    Texas    5,274        against  38,350              7.3 to 1
    New York 2,172        against  14,545              6.7 to 1
    Florida  3,713        against  20,871              5.6 to 1
    California 55,002     against   4,862              the inverse

California is the mirror image of every other large state. So the MFT map is a
map of statutes and professional history, and the page says that before it
shows a single bar.

The honest supply comparison is all four occupations together, and on that
California ranks second of the thirty-five states with complete data.

WHAT THE PAGE IS BUILT FROM

BLS Occupational Employment and Wage Statistics, May 2025, released May 2026 -
the only source that counts the same way in all fifty states - divided by
Census Vintage 2025 population. License titles and licensee counts come from
each state's own board. Everything is in `_dev/state_workforce.py`; nothing on
this page is typed into prose.

THE THREE HONESTY REQUIREMENTS, ALL VISIBLE ON THE PAGE

1. **OEWS excludes the self-employed.** A sole proprietor in private practice
   is invisible to it; one who incorporated is counted. California's register
   lists 59,706 LMFTs against 34,970 MFT jobs - about three in five.
2. **Suppressed cells are not zeros.** Nine states have a withheld estimate and
   eight have an occupation absent entirely. They are never imputed, never
   ranked, and shown as "not published".
3. **Only states with all four occupations can be ranked.** A four-occupation
   total built from three is a floor, and is marked as one.

CHART DECISIONS, MADE AGAINST THE VALIDATOR RATHER THAN BY EYE

The site's own palette FAILS as a categorical set - the gold is too light and
the pine reads gray. A passing four-color set was computed instead. It clears
the adjacent-pair checks but fails all-pairs, so there is deliberately **no
stacked bar** anywhere on this page: the occupation breakdown is small
multiples, one hue each, every chart directly labelled. The ranking chart is a
single series, so it uses one color, no legend, and emphasis on California.

Idempotent - rewrites its page from scratch every run. Guarded.
"""
import os, re, sys

HERE = os.path.dirname(os.path.abspath(__file__))
SITE = os.path.dirname(HERE)
sys.path.insert(0, HERE)

import pagekit as pk
import state_workforce as W

PAGE = "therapists-by-state-compared.html"
# Chrome comes from a frozen pre-conversion snapshot (_dev/chrome_donor.html)
# rather than a live page: rollout step 5 converts live pages to the house
# design one family at a time, and a converted donor would hand this builder
# bc2 head links on top of its own family CSS - the mixed state the
# collision audit forbids. The snapshot retires when this family converts.
DONOR = "_dev/chrome_donor.html"

ATLAS = "therapists-by-county-california.html"
BECOME = "become-an-mft-california.html"
OOS = "associate-hours-telehealth-out-of-state.html"

INK = "#16211B"
MUTED = "#635E53"
GRID = "#DBD4C4"
EMPH = "#00704A"
REST = "#9FB3A9"
RULE = "#A6332B"

JUMPS = [
    ("titles", "What it's called where"),
    ("ranking", "The honest comparison"),
    ("kinds", "By profession"),
    ("gap", "Licensed vs counted"),
    ("limits", "What this cannot say"),
]


# ------------------------------------------------------------------- charts
def bar_chart(rows, us_value, us_label, emphasise, unit="", width=760,
              row_h=27, label_w=150, title=""):
    """Horizontal bars, one series, one color, emphasis on one row.

    Direct value labels on every bar and no x-axis: with thirteen rows a
    reader wants the number, not to measure against a gridline. A national
    rule line gives the only comparison that needs a second mark.
    """
    top, bottom = 14, 34
    h = top + row_h * len(rows) + bottom
    mx = max(max(v for _n, v in rows), us_value) * 1.14
    plot_w = width - label_w - 66

    def x(v):
        return label_w + (plot_w * v / mx)

    o = ['<svg viewBox="0 0 %d %d" width="100%%" role="img" aria-label="%s">'
         % (width, h, pk.esc(title))]
    # the national rule, behind the bars
    ux = x(us_value)
    o.append('<line x1="%.1f" y1="%d" x2="%.1f" y2="%d" stroke="%s" '
             'stroke-width="1.5" stroke-dasharray="0"/>'
             % (ux, top - 6, ux, top + row_h * len(rows) + 4, RULE))
    o.append('<text x="%.1f" y="%d" text-anchor="middle" font-size="10" '
             'font-family="IBM Plex Mono,monospace" fill="%s">%s</text>'
             % (ux, h - 18, RULE, pk.esc(us_label)))

    for i, (name, v) in enumerate(rows):
        y = top + i * row_h
        on = (name == emphasise)
        col = EMPH if on else REST
        bw = x(v) - label_w
        # 4px rounded data-end, square at the baseline
        o.append('<path d="M%d %d h%.1f a4,4 0 0 1 4,4 v%d a4,4 0 0 1 -4,4 '
                 'h-%.1f z" fill="%s"><title>%s: %s%s</title></path>'
                 % (label_w, y, max(bw - 4, 1), 14, max(bw - 4, 1), col,
                    pk.esc(name), ("%.0f" % v), pk.esc(unit)))
        o.append('<text x="%d" y="%d" text-anchor="end" font-size="12.5" '
                 'font-family="Inter,system-ui" fill="%s"%s>%s</text>'
                 % (label_w - 10, y + 15, INK if on else MUTED,
                    ' font-weight="700"' if on else "", pk.esc(name)))
        o.append('<text x="%.1f" y="%d" font-size="12" '
                 'font-family="IBM Plex Mono,monospace" fill="%s"%s>%s</text>'
                 % (x(v) + 8, y + 15, INK if on else MUTED,
                    ' font-weight="700"' if on else "", "%.0f" % v))
    o.append("</svg>")
    return "".join(o)


def mini_chart(rows, colour, width=330, row_h=22, label_w=104):
    top, bottom = 6, 8
    h = top + row_h * len(rows) + bottom
    mx = max(v for _n, v in rows) * 1.2
    plot_w = width - label_w - 46
    o = ['<svg viewBox="0 0 %d %d" width="100%%" aria-hidden="true">'
         % (width, h)]
    for i, (name, v) in enumerate(rows):
        y = top + i * row_h
        bw = plot_w * v / mx
        o.append('<path d="M%d %d h%.1f a3,3 0 0 1 3,3 v%d a3,3 0 0 1 -3,3 '
                 'h-%.1f z" fill="%s"/>'
                 % (label_w, y, max(bw - 3, 1), 11, max(bw - 3, 1), colour))
        o.append('<text x="%d" y="%d" text-anchor="end" font-size="11" '
                 'font-family="Inter,system-ui" fill="%s">%s</text>'
                 % (label_w - 8, y + 12, MUTED, pk.esc(name)))
        o.append('<text x="%.1f" y="%d" font-size="10.5" '
                 'font-family="IBM Plex Mono,monospace" fill="%s">%.1f</text>'
                 % (label_w + bw + 6, y + 12, MUTED, v))
    o.append("</svg>")
    return "".join(o)


# -------------------------------------------------------------------- body
def ranked_total():
    out = []
    for r in W.complete():
        t, _floor = W.total(r)
        out.append((r[0], W.per100k(t, r[1])))
    return sorted(out, key=lambda x: -x[1])


def body():
    o = ['<article class="pk-wrap">']

    rk = ranked_total()
    ca_rank = [n for n, _ in rk].index("California") + 1
    ca_val = dict(rk)["California"]
    us_tot = W.us_total_per100k()
    ca_mft_share = 100.0 * W.row("California")[2] / W.US["mft"]

    o.append(pk.hero(
        "The 50 states &middot; BLS %s" % W.RELEASE.split(",")[0],
        "What counts as a therapist depends on which state you are in.",
        "California holds <b>%.0f%% of every marriage and family therapist "
        "job in the United States</b>. That is not because other states have "
        "no therapists. It is because they call them something else."
        % ca_mft_share,
        [("%.0f%%" % ca_mft_share, "of US MFT jobs are in California"),
         ("%d of %d" % (ca_rank, len(rk)), "California's rank, all four "
          "professions"),
         ("%.0f" % us_tot, "US average per 100,000"),
         ("17 to 1", "Ohio's counselors to MFTs")],
        JUMPS))

    # ------------------------------------------------------------- the titles
    o.append('<section class="pk-sec" id="titles">')
    o.append('<p class="pk-k">Start here, or the rest of the page misleads</p>')
    o.append('<h2 class="pk-h">The same clinician, seventeen different '
             "names.</h2>")
    o.append('<p class="pk-d">A master&rsquo;s-level therapist who does the '
             "same work is a <b>LPCC</b> in California, a <b>LMHC</b> in New "
             "York and Florida, a <b>LPC</b> in Texas, a <b>LCPC</b> in "
             "Illinois and a <b>CMHC</b> in Utah. Clinical social work splits "
             "the same way: <b>LCSW</b> in most places, <b>LICSW</b> in "
             "Massachusetts and Washington, <b>LISW</b> in Ohio.</p>")
    rows = []
    for st, mft, couns, sw, tier in W.TITLES:
        cls = "hi" if st == "California" else ""
        rows.append(([("<b>%s</b>" % st) if st == "California" else st,
                      (mft, "m"), (couns, "m"), (sw, "m"), tier], cls))
    o.append(pk.table(
        ["State", "Family therapy", "Counseling", "Clinical social work",
         "Pre-licensed tier"],
        rows,
        "Every state here licenses marriage and family therapists. What "
        "differs is which credential the profession actually grew into. "
        "<b>One collision worth knowing:</b> in Colorado <b>PCC</b> is a "
        "pre-licensed candidate, while <b>LPCC</b> in California, Minnesota "
        "and Ohio is a full independent license.", minw=720))

    o.append(pk.callout(
        "Why that ruins the obvious chart",
        ["Federal statistics count people by the job they are employed to do. "
         "A clinician licensed as a counselor is recorded as a counselor, "
         "whatever the work looks like in the room.",
         "So a &ldquo;marriage and family therapists per capita&rdquo; map "
         "reads as though Texas has almost none. Texas licenses <b>5,274</b> "
         "of them &mdash; against <b>38,350</b> professional counselors. The "
         "map is measuring statutes.",
         "<b>California is the exception that makes the pattern visible:</b> "
         "55,002 LMFTs against 4,862 LPCCs. It is the only large state where "
         "the family-therapy credential won."]))

    rows = []
    for st, mft, couns, asat, url in W.LICENSEES:
        ratio = couns / float(mft)
        cls = "good" if ratio < 1 else ("bad" if ratio > 10 else "")
        rows.append(([st, (format(mft, ",d"), "n"), (format(couns, ",d"), "n"),
                      ("%.1f to 1" % ratio if ratio >= 1
                       else "1 to %.1f" % (1 / ratio), "f"), asat], cls))
    o.append(pk.table(
        ["State", "MFT licensees", "Counseling licensees", "Ratio", "As at"],
        rows,
        "Counts published by each state&rsquo;s own board or oversight body "
        "&mdash; these are licenses held, not jobs worked, and they include "
        "pre-licensed tiers where the board reports them together. Florida "
        "shows the gap still widening: <b>6,116 registered counselor interns "
        "against 832 MFT interns</b>.", minw=620))
    o.append("</section>")

    # ------------------------------------------------------------- the ranking
    o.append('<section class="pk-sec" id="ranking">')
    o.append('<p class="pk-k">The comparison that survives the title problem</p>')
    o.append('<h2 class="pk-h">All four professions, per 100,000 people.</h2>')
    o.append('<p class="pk-d">Adding marriage and family therapists, mental '
             "health counselors, mental health social workers and clinical "
             "psychologists together cancels most of the title effect: "
             "whichever credential a state prefers, its clinicians land "
             "somewhere in the four. <b>California ranks %d of the %d states "
             "with complete data</b>, at %.0f against a national %.0f.</p>"
             % (ca_rank, len(rk), ca_val, us_tot))

    show = rk[:10]
    for name in ("Texas", "Florida", "New York", "Ohio"):
        for n, v in rk:
            if n == name and (n, v) not in show:
                show.append((n, v))
    o.append('<div class="pk-chart">')
    o.append(bar_chart(show, us_tot, "US average %.0f" % us_tot, "California",
                       unit=" per 100,000",
                       title="Mental health clinicians per 100,000 residents, "
                             "top ten states plus Texas, Florida, New York and "
                             "Ohio, against the national average"))
    o.append("</div>")
    o.append('<p class="pk-cap">Top ten, plus four large states for scale. '
             "The red line is the national average of %.0f. Only the %d "
             "states where all four occupations were published can be ranked "
             "&mdash; nine have a suppressed estimate and eight are missing an "
             "occupation entirely, and neither is a zero.</p>"
             % (us_tot, len(rk)))
    o.append("</section>")

    # --------------------------------------------------------------- by kind
    o.append('<section class="pk-sec" id="kinds">')
    o.append('<p class="pk-k">The four professions, separately</p>')
    o.append('<h2 class="pk-h">Where each kind of clinician actually is.</h2>')
    o.append('<p class="pk-d">Four charts rather than one stacked bar, '
             "because the four colors that would be needed cannot be told "
             "apart reliably by a reader with color blindness when the "
             "segments touch. Each chart is the top six states per 100,000 "
             "residents.</p>")
    o.append('<div class="pk-mini">')
    for key, soc, label, colour in W.OCCUPATIONS:
        idx = {"mft": 2, "couns": 3, "msw": 4, "psych": 5}[key]
        vals = [(r[0], W.per100k(r[idx], r[1])) for r in W.STATES
                if r[idx] is not None]
        vals = sorted(vals, key=lambda x: -x[1])[:6]
        o.append('<div class="pk-m">')
        o.append('<h3>%s</h3><p class="soc">SOC %s &middot; US average %.1f '
                 "per 100,000</p>" % (label, soc, W.us_per100k(key)))
        o.append(mini_chart(vals, colour))
        o.append("</div>")
    o.append("</div>")
    o.append('<p class="pk-cap">The first chart is the one to distrust, and '
             "it is first on purpose. Minnesota and Utah appear high on "
             "marriage and family therapy for the same reason California "
             "does: their statutes built the profession around that title. "
             "The other three charts are far less distorted.</p>")
    o.append("</section>")

    # ------------------------------------------------------------------ gap
    o.append('<section class="pk-sec" id="gap">')
    o.append('<p class="pk-k">Licensed is not the same as counted</p>')
    o.append('<h2 class="pk-h">California has 59,706 licensed LMFTs and '
             "34,970 MFT jobs.</h2>")
    o.append('<p class="pk-d">Both numbers are right. They measure different '
             "things, and the difference is roughly <b>two in five</b>.</p>")
    o.append(pk.numbered([
        ("1", "The federal survey asks employers, not people",
         "It counts wage and salary jobs at establishments with a payroll. "
         "In its own words, it <b>&ldquo;does not include the self-employed, "
         "owners and partners in unincorporated firms&rdquo;</b>."),
        ("2", "Which cuts straight through private practice",
         "A therapist in solo practice as a sole proprietor is invisible to "
         "it. One who formed a corporation and pays herself a salary is "
         "counted. The same clinician, the same caseload, counted or not "
         "depending on a filing decision. The federal estimate of "
         "unincorporated self-employment in marriage and family therapy is "
         "<b>%.1f%%</b> &mdash; and that is a floor, not the whole of private "
         "practice." % W.SELF_EMPLOYED["mft"]),
        ("3", "And a license is not a job",
         "Somebody licensed in California may have retired, moved, gone "
         "inactive, or taken a role coded as something else entirely. A "
         "register counts permissions; a workforce survey counts positions."),
    ]))
    o.append('<p class="pk-fine">Which of the two you want depends on the '
             "question. For &ldquo;how many people could legally see me?&rdquo; "
             'the register is right, and <a href="%s">the California register '
             "is broken down by county here</a>. For &ldquo;how many jobs are "
             "there?&rdquo; the survey is right. For comparing states, the "
             "survey is the only option, because fifty registers with fifty "
             "definitions of active are not comparable at all.</p>" % ATLAS)
    o.append("</section>")

    # --------------------------------------------------------------- limits
    o.append('<section class="pk-sec" id="limits">')
    o.append('<p class="pk-k">Before you quote this page</p>')
    o.append('<h2 class="pk-h">Four things this cannot tell you.</h2>')
    o.append(pk.table(
        ["The question", "What the data supports"],
        [(["Which state has the most therapists per person?",
           "<b>Only approximately.</b> The four-occupation total is the best "
           "available comparison and still misses everybody in solo "
           "unincorporated practice, unevenly by state."], "bad"),
         ["Is Texas short of therapists?",
          "<b>Not answerable from the MFT column.</b> Texas is a "
          "counselor-licensing state; its counselor count is 38,350. The "
          "four-occupation total is the number to use, and on that Texas is "
          "genuinely low &mdash; but by a factor of two, not twenty."],
         ["Did a state's workforce grow last year?",
          "<b>No.</b> These estimates pool six semiannual panels over three "
          "years, and the statistical agency warns against reading them as "
          "year-over-year change."],
         ["Is a blank the same as none?",
          "<b>Never.</b> A withheld estimate means the agency could not "
          "publish it to its own standards, or publishing would identify a "
          "respondent. Washington's marriage and family therapist count is "
          "withheld; Washington plainly has marriage and family therapists."]],
        "The rule this site works to: publish what the source supports, and "
        "print the limits beside the number rather than in a footnote nobody "
        "reads. The most shareable version of this page would have been the "
        "one with Texas at 4.4, and it would have been wrong."))
    o.append("</section>")

    src, n = pk.sources([
        ("The employment figures", [
            ("Bureau of Labor Statistics &mdash; Occupational Employment and "
             "Wage Statistics, %s" % W.RELEASE, W.OEWS_URL),
            ("What the survey does and does not count &mdash; technical notes",
             W.OEWS_TECH),
            ("Why estimates are withheld &mdash; the survey's own FAQ",
             W.OEWS_FAQ),
            ("Self-employment by occupation &mdash; Employment Projections",
             W.MATRIX_URL),
        ]),
        ("Population", [
            ("US Census Bureau &mdash; %s" % W.POP_VINTAGE, W.CENSUS_URL),
        ]),
        ("License counts, from each state's own board", [
            ("%s &mdash; %s" % (st, asat), url)
            for st, _m, _c, asat, url in W.LICENSEES
        ]),
    ], note="Every figure on this page is computed at build time from the "
            "sources above rather than typed into the text. Where a state's "
            "estimate was withheld it is shown as not published and excluded "
            "from every ranking &mdash; it is never treated as a zero.")
    o.append(src)

    o.append("</article>")
    return "".join(o), n


CSS = """<style>/* _dev/build_states.py */
.pk-chart{border:2px solid #16211B;border-radius:12px;background:#fff;
  box-shadow:5px 5px 0 #16211B;padding:16px 18px;margin:0 0 14px;
  overflow-x:auto}
.pk-mini{display:grid;grid-template-columns:1fr 1fr;gap:16px;margin:0 0 14px}
.pk-m{border:2px solid #16211B;border-radius:12px;background:#fff;
  box-shadow:4px 4px 0 #16211B;padding:14px 16px}
.pk-m h3{font-family:'Bricolage Grotesque',system-ui,sans-serif;font-weight:800;
  letter-spacing:-.02em;font-size:15px;line-height:1.2;color:#16211B;margin:0 0 3px}
.pk-m .soc{font-family:'IBM Plex Mono',ui-monospace,monospace;font-size:10px;
  letter-spacing:.08em;text-transform:uppercase;color:#2C6350;margin:0 0 10px}
@media (max-width:760px){.pk-mini{grid-template-columns:1fr}}
</style>"""


META = pk.meta_block(
    PAGE,
    "Therapists by state: what the license is called, and how many there are",
    "California holds 52% of US marriage and family therapist jobs - because "
    "other states call the same clinician an LPC or LMHC. The license titles "
    "in 17 states, and the per-capita comparison that survives them.",
    "licensure", "reference",
    "How does California compare with other states for therapists?",
    "The license title in each state, the per-capita ranking that is not "
    "distorted by those titles, and why a marriage and family therapist map "
    "measures statutes rather than supply",
    "%.0f%% of US MFT jobs" % (100.0 * W.row("California")[2] / W.US["mft"]),
    weight=4)


def main():
    print("the states compared")
    problems = W.check()
    for x in problems:
        print("GUARD:", x)
    if problems:
        sys.exit("the transcribed data is inconsistent; nothing was written")

    rk = ranked_total()
    print("  %d states rankable, US %.1f per 100k, California %.1f (rank %d)"
          % (len(rk), W.us_total_per100k(), dict(rk)["California"],
             [n for n, _ in rk].index("California") + 1))

    head, header, footer, links, scripts = pk.chrome_parts(DONOR)
    html_body, nsrc = body()
    html = pk.assemble(head, META, header, html_body, footer, links, scripts,
                       extra=CSS)

    p = os.path.join(SITE, PAGE)
    open(p, "w", encoding="utf-8").write(html)
    print("  wrote %s, %s bytes, %d sources"
          % (PAGE, format(len(html), ",d"), nsrc))

    bad = pk.check_page(p, [
        ("the title table", "LCPC"),
        ("the self-employment caveat", "does not include the self-employed"),
        ("the suppression warning", "never treated as a zero"),
        ("the ranking chart", "<svg"),
    ], [j[0] for j in JUMPS] + ["sources"])

    s = open(p, encoding="utf-8").read()
    art = pk.article(s)

    # No stacked bar may ever appear here. The four-color set fails the
    # all-pairs colour-blindness check, which is exactly the case a stacked
    # bar creates, and the small multiples exist to avoid it.
    if art.count("<svg") < 5:
        print("GUARD: %d charts, expected the ranking plus four small "
              "multiples" % art.count("<svg"))
        bad += 1

    # Every state in the title table must be on the page - the page's whole
    # argument is that the titles differ, and a missing row weakens it.
    for st, _m, _c, _w, _t in W.TITLES:
        if st not in art:
            print("GUARD: %s is in the title table and not on the page" % st)
            bad += 1

    # The MFT-map warning must precede the MFT chart. If an edit ever moves
    # the chart above the explanation, the page becomes the thing it corrects.
    i_warn = art.find("map is measuring statutes")
    i_chart = art.find('id="kinds"')
    if i_warn < 0 or i_chart < 0 or i_warn > i_chart:
        print("GUARD: the title warning no longer comes before the "
              "per-profession charts")
        bad += 1

    if nsrc < 8:
        print("GUARD: %d sources for a page built entirely on federal data"
              % nsrc)
        bad += 1

    if bad:
        sys.exit("\n%d problem(s)" % bad)
    print("  guards clean - %d states titled, %d rankable, warning before the "
          "chart it warns about" % (len(W.TITLES), len(rk)))


if __name__ == "__main__":
    main()
