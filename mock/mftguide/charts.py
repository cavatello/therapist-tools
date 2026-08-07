# -*- coding: utf-8 -*-
"""Infographics for the programme directory, computed from programs.json.

NOTHING HERE IS DRAWN FROM A NUMBER A HUMAN TYPED. Every bar, dot and count is
derived from the same records the cards below it are built from, so a chart
cannot drift out of step with the table it sits above - which is the usual way
an infographic on a data page becomes a lie.

TWO KINDS OF COST FIGURE, MARKED DIFFERENTLY. Some institutions publish a
total. Others publish a per-unit rate and a unit count, from which a total
follows by multiplication - that is arithmetic on their own published numbers,
not an estimate, but it is still a different kind of claim and it is hatched
differently in the bar and labelled in the legend. The rest publish nothing at
all, and the chart says so in words rather than leaving a gap the eye reads as
zero. No count is written here in words: this file has already outlived one
set of them, and a comment that says "seven" beside code that says len() is a
comment that will be wrong before it is read.

NO RANKING. The bars sort by value because an unsorted bar chart is unreadable,
not to award positions. Nothing here is scored, starred or ordered by quality,
and the directory's own guard refuses to ship a page that looks like it does.
"""
import html
import re

QUARTER_TO_SEM = 2.0 / 3.0


def esc(x):
    return html.escape(str(x)) if x is not None else ""


# ---------------------------------------------------------------- derivation

# The smallest credible qualifying total, in semester-equivalent units. The
# Board requires 60 semester units for an MFT degree, so anything reading below
# 40 is not a degree total - it is a per-course figure, a non-standard unit, or
# a base degree that is not the qualifying one. Rejecting those is better than
# carrying them: a wrong unit count multiplies into a wrong computed tuition.
MIN_UNITS = 40.0


def units_of(p):
    """(count, system) from the units field, or (None, None).

    PREFERS `units_n` WHERE IT EXISTS. The `units` field is prose written for a
    reader - "43 units base MS; 60 units with MFT and/or PCC concentration",
    "Quarter system; 4.5 quarter units per course; total not stated" - and
    parsing prose for arithmetic is how a chart quietly acquires a wrong number.
    Where the first number in the sentence is not the qualifying total,
    `units_n` carries the machine-readable one and the prose is left alone.

    Three real failures this now catches, all found by a derived line on a card
    reading "the smallest unit requirement on the list, at Quarter system":

      Palo Alto  4.5  - units PER COURSE, and the string says "total not stated"
      Northwestern 25 - a non-standard Northwestern quarter unit, not comparable
      Dominican  43   - the base MS, where the MFT-qualifying degree is 60

    None of the three drove a computed cost, because none publishes a per-unit
    rate. That was luck, not design, and it is what MIN_UNITS is for.
    """
    lo = (p.get("units") or "").lower()
    sysm = ("quarter" if "quarter" in lo else
            "semester" if ("semester" in lo or "unit" in lo or "credit" in lo)
            else None)
    if p.get("units_n"):
        return float(p["units_n"]), (p.get("units_sys") or sysm or "semester")
    m = re.search(r"\d+(?:\.\d+)?", lo)
    if not m:
        return None, None
    n = float(m.group(0))
    equiv = n * (QUARTER_TO_SEM if sysm == "quarter" else 1)
    if equiv < MIN_UNITS:
        return None, None
    return n, sysm


def cost_of(p):
    """(dollars, kind) where kind is 'published' or 'computed', else (None,None)."""
    if p.get("total"):
        return int(p["total"]), "published"
    if p.get("per_unit"):
        n, _sys = units_of(p)
        if n:
            return int(round(float(p["per_unit"]) * n)), "computed"
    return None, None


YEARS = [("Two years", lambda y: y is not None and y < 2.25),
         ("Two and a half", lambda y: y is not None and 2.25 <= y < 2.75),
         ("Three years", lambda y: y is not None and 2.75 <= y < 3.25),
         ("More than three", lambda y: y is not None and y >= 3.25)]


# A master's degree takes between one and six years. Anything outside that is
# a misparse, not a programme - "90 quarter units in 6 quarters" reads as 30
# years if the quarter branch grabs the unit count. Same principle as
# MIN_UNITS: a parser reading prose should fail to an honest "not published"
# rather than to a confident absurdity.
YEARS_MIN, YEARS_MAX = 1.0, 6.0


def _yrs(v):
    return v if YEARS_MIN <= v <= YEARS_MAX else None


def years_of(p):
    """Years to complete, from the free-text length field.

    Handles "3 years", "2.5-3 years" (takes the low end), "5 semesters" and
    "2 years (~5 semesters)". Returns None when the field is absent or says
    something a number cannot represent, and None is rendered as its own bar
    rather than dropped - a fifth of these programmes do not publish a length
    and that is itself worth seeing.
    """
    L = (p.get("length") or "").lower()
    if not L:
        return None
    # "2-year or 2.5-year tracks", "Three-year or four-year pathway",
    # "Two-year full-time track ... or three-year". Five schools published a
    # length in one of these shapes and were being counted as "not published"
    # on the time chart - which is the chart telling a reader a school is silent
    # when the school is not. The low end is taken, matching the range rule
    # everywhere else: a school offering a two-year and a three-year track does
    # take two years if you take the two-year track.
    WORD = {"one": 1, "two": 2, "three": 3, "four": 4, "five": 5, "six": 6}
    # The separator between the number and "year" may be a space OR a hyphen.
    # "2-year or 2.5-year tracks" failed the original pattern because after the
    # hyphen it expected a second NUMBER (the "2.5-3 years" range case) and
    # found the word "year" instead - so two schools that publish a length were
    # counted as silent.
    m = re.search(r"(\d+(?:\.\d+)?)\s*(?:[-–]\s*\d+(?:\.\d+)?)?[-\s]*year", L)
    if m:
        return _yrs(float(m.group(1)))
    m = re.search(r"\b(one|two|three|four|five|six)[-\s]year", L)
    if m:
        return _yrs(float(WORD[m.group(1)]))
    # Months BEFORE term counts, and this ordering is load-bearing. A term count
    # only converts to years by assuming how many terms a school runs a year,
    # and that assumption is wrong for any school on a year-round calendar:
    # Antioch Santa Barbara says "8 quarters (24 months)", which the quarter
    # branch turned into 2.67 years on a 3-quarters-a-year assumption when the
    # school had already stated 24 months. An explicit duration beats an
    # inference from the school's own sentence every time.
    m = re.search(r"(\d+(?:\.\d+)?)\s*month", L)
    if m:
        return _yrs(float(m.group(1)) / 12.0)
    m = re.search(r"(\d+(?:\.\d+)?)\s*semester", L)
    if m:
        return _yrs(float(m.group(1)) / 2.0)
    m = re.search(r"(\d+(?:\.\d+)?)\s*quarter", L)
    if m:
        return _yrs(float(m.group(1)) / 3.0)
    return None


def format_of(p):
    f = (p.get("format") or "").lower()
    if not f:
        return None
    online = "online" in f or "distance" in f or "100%" in f or "remote" in f
    # "in person" without the hyphen was not matched, so "In person, with
    # evening and part-time options" read as no information at all. Nor were
    # "on-ground", "in class" or "on site", all of which state delivery
    # unambiguously.
    #
    # What is deliberately still NOT matched: "Evening and daytime cohorts" and
    # "Cohort model; daytime and weekend schedules". Those describe a TIMETABLE,
    # not a delivery mode, and a reader could hold either of them while studying
    # entirely online. Guessing "in person" from a schedule would be inventing
    # the one fact the field exists to carry.
    campus = ("in-person" in f or "in person" in f or "on-campus" in f
              or "on campus" in f or "campus" in f or "classroom" in f
              or "residential" in f or "face-to-face" in f or "on-ground" in f
              or "on ground" in f or "in class" in f or "on site" in f
              or "on-site" in f)
    if "hybrid" in f or "blended" in f or "low-residency" in f or (online and campus):
        return "Hybrid or low-residency"
    if online:
        return "Fully online"
    if campus:
        return "In person"
    return None


# ---------------------------------------------------------------- rendering

def _bars(items, total_label, fmt=str, kinds=None):
    if not items:
        return ""
    top = max(v for _l, v in items) or 1
    out = []
    for lab, val in items:
        k = (kinds or {}).get(lab, "")
        out.append('<div class="ig-b%s"><span class="ig-l">%s</span>'
                   '<span class="ig-t"><i style="width:%.4f%%"></i></span>'
                   '<span class="ig-v">%s</span></div>'
                   % (" " + k if k else "", esc(lab), 100.0 * val / top,
                      esc(fmt(val))))
    return ('<div class="ig-bars">%s</div>'
            '<p class="ig-n">%s</p>' % ("".join(out), total_label))


def dots(progs):
    """One dot per institution, filled where COAMFTE accredits it.

    A percentage would round the point away. The reader's actual question is
    "how likely is it that the school I am looking at has this", and a grid of
    every institution in the data answers it at a glance in a way "18%" does
    not.
    """
    n = len(progs)
    acc = sum(1 for p in progs if p.get("coamfte"))
    cells = "".join(
        '<span class="ig-d%s" title="%s"></span>'
        % (" on" if p.get("coamfte") else "", esc(p["institution"]))
        for p in sorted(progs, key=lambda x: (not x.get("coamfte"), x["institution"])))
    return ('<div class="ig-dots">%s</div>'
            '<p class="ig-n"><b>%d of the %d</b> institutions on the '
            "Board&rsquo;s list hold COAMFTE accreditation. It is the "
            "accreditation that decides whether the degree travels out of "
            "California; inside California it is not required, and the other "
            "%d license graduates every year.</p>" % (cells, acc, n, n - acc))


def costs(progs):
    rows, kinds = [], {}
    for p in progs:
        c, kind = cost_of(p)
        if c:
            lab = p["institution"]
            lab = re.sub(r"\s*\(.*?\)\s*", " ", lab).strip()
            if len(lab) > 34:
                lab = lab[:33].rstrip(" ,") + "…"
            while lab in kinds:
                lab += " "
            kinds[lab] = "pub" if kind == "published" else "cmp"
            rows.append((lab, c))
    rows.sort(key=lambda r: -r[1])
    none = len(progs) - len(rows)
    note = ('Solid bars are a total the institution publishes itself. Hatched '
            'bars are its own published per-unit rate multiplied by its own '
            'published unit count &mdash; arithmetic on its figures, not an '
            'estimate of mine. <b>%d of the %d publish neither</b>, so they are '
            "not on this chart at all; that is a fair thing to ask admissions "
            "directly. None of these figures include campus fees, books, or "
            "the years of living costs that dwarf them."
            % (none, len(progs)))
    return _bars(rows, note, lambda v: "$%s" % "{:,}".format(v), kinds)


def lengths(progs):
    ys = [years_of(p) for p in progs]
    rows = [(lab, sum(1 for y in ys if fn(y))) for lab, fn in YEARS]
    rows.append(("Not published", sum(1 for y in ys if y is None)))
    rows = [r for r in rows if r[1]]
    return _bars(rows, "Time to the degree only. The 3,000 associate hours "
                       "that follow it take most people a further two to three "
                       "years, and part-time study stretches both ends.",
                 lambda v: "%d" % v)


def formats(progs):
    fs = [format_of(p) for p in progs]
    order = ["In person", "Hybrid or low-residency", "Fully online"]
    rows = [(k, sum(1 for f in fs if f == k)) for k in order]
    rows.append(("Not published", sum(1 for f in fs if f is None)))
    rows = [r for r in rows if r[1]]
    return _bars(rows, "Delivery format is the field most loosely worded in "
                       "programme marketing, and these are my reading of each "
                       "programme&rsquo;s own words. Whatever it says, the "
                       "clinical placement happens in a room with real clients "
                       "near where you live &mdash; no format changes that.",
                 lambda v: "%d" % v)


def units(progs):
    sem = [n for n, s in map(units_of, progs) if n and s == "semester"]
    qtr = [n for n, s in map(units_of, progs) if n and s == "quarter"]
    if not sem or not qtr:
        return ""
    qs = sorted(round(n * QUARTER_TO_SEM) for n in qtr)
    ss = sorted(sem)

    def med(a):
        return a[len(a) // 2]
    return ('<div class="ig-cmp"><div><b>%d</b><span>semester units, median of '
            "the %d programmes on a semester calendar</span></div>"
            "<div><b>%d</b><span>quarter units, median of the %d on a quarter "
            "calendar &mdash; about %d semester units</span></div></div>"
            '<p class="ig-n">Unit totals are not comparable across calendars. '
            "Three quarter units are roughly two semester units, so a 90-unit "
            "quarter programme and a 60-unit semester one are the same size. "
            "Comparing the raw numbers makes quarter-system schools look half "
            "again as long as they are.</p>"
            % (med(ss), len(ss), med(sorted(qtr)), len(qtr), med(qs)))


PANELS = [("Accreditation", "How many degrees travel", dots),
          ("Cost", "What the degree costs, where a figure exists", costs),
          ("Time", "How long it takes", lengths),
          ("Format", "How you would study", formats),
          ("Size", "Why unit counts do not compare", units)]


def render(progs):
    out = []
    for i, (kicker, title, fn) in enumerate(PANELS):
        body = fn(progs)
        if not body:
            continue
        out.append('<section class="ig" id="ig-%d"><p class="ig-k">%s</p>'
                   "<h3>%s</h3>%s</section>" % (i, esc(kicker), esc(title), body))
    if not out:
        return ""
    return ('<div class="igwrap"><h2 id="at-a-glance">All %d, at a glance</h2>'
            '<p class="ig-i">Every figure below is computed from the same '
            "records as the cards further down this page, so the two cannot "
            "disagree. Nothing here is a ranking and nothing is scored &mdash; "
            "bars are sorted by size only because an unsorted bar chart cannot "
            "be read.</p>%s</div>" % (len(progs), "".join(out)))


CSS = """<style>/* infographics */
.igwrap{margin:26px 0 34px}
.igwrap h2{scroll-margin-top:16px}
.ig-i{max-width:66ch}
.ig{background:#fff;border:1px solid var(--line);border-radius:13px;
  padding:20px 22px;margin:0 0 13px}
.ig-k{font-family:'IBM Plex Mono',ui-monospace,monospace;font-size:9.8px;
  letter-spacing:.12em;text-transform:uppercase;color:var(--mut);margin:0 0 6px}
.ig h3{font-family:Fraunces,Georgia,serif;font-size:19px;line-height:1.25;
  font-weight:600;color:var(--ink);margin:0 0 15px}
.ig-bars{display:grid;gap:5px}
.ig-b{display:grid;grid-template-columns:minmax(96px,190px) minmax(0,1fr) 74px;
  gap:11px;align-items:center}
.ig-l{font-size:12.4px;line-height:1.35;color:#3B4A38;overflow-wrap:anywhere}
.ig-t{display:block;height:15px;background:#F4F1E7;border-radius:4px;overflow:hidden}
.ig-t i{display:block;height:100%;background:var(--pine);border-radius:4px;
  min-width:2px}
.ig-b.cmp .ig-t i{background:repeating-linear-gradient(115deg,#2C6350 0 6px,
  #6E9587 6px 12px)}
.ig-v{font-family:'IBM Plex Mono',monospace;font-size:11.4px;color:var(--ink);
  text-align:right;white-space:nowrap}
.ig-n{font-size:13.2px;line-height:1.68;color:#4A5A46;margin:14px 0 0;max-width:70ch}
.ig-n b{color:var(--ink)}
.ig-dots{display:flex;flex-wrap:wrap;gap:6px}
.ig-d{width:15px;height:15px;border-radius:50%;background:#EDE8DA;
  border:1px solid #DFD7C4}
.ig-d.on{background:var(--pine);border-color:var(--pine)}
.ig-cmp{display:grid;grid-template-columns:repeat(auto-fit,minmax(210px,1fr));gap:13px}
.ig-cmp>div{background:#FBF6E9;border-radius:10px;padding:15px 17px}
.ig-cmp b{display:block;font-family:Fraunces,Georgia,serif;font-size:34px;
  line-height:1;color:var(--pine)}
.ig-cmp span{display:block;font-size:12.8px;line-height:1.55;color:#4A5A46;margin-top:7px}
@media (max-width:640px){
  .ig-b{grid-template-columns:minmax(0,1fr) 68px;gap:4px 9px}
  .ig-l{grid-column:1/-1}
  .ig{padding:16px 15px}
}
</style>"""
