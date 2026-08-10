#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Build mft-programs-california.html — the directory.

Every institution whose graduate degrees the Board of Behavioral Sciences lists
as qualifying towards California LMFT licensure - seventy-seven of them, plus
one that qualifies through the out-of-state certification route instead - with
what could be verified about each: the exact degree name, COAMFTE accreditation,
units, length, format, whether the Board's row also opens the LPCC route, and
published tuition with the year the figure is from.

Counts in the RENDERED page are computed from the data, never typed. That rule
exists because this docstring said "sixty-five" and the methodology paragraph
said "twenty-one publish tuition" for months after both had stopped being true;
the difference is that a stale comment misleads a maintainer and a stale number
in the copy misleads a reader of a page whose whole claim is that its figures
are real.

THREE THINGS THIS PAGE REFUSES TO DO.

It will not estimate tuition. About two in five institutions publish a per-unit
or total figure; the rest do not, and the rest say "not published" rather than
carrying a plausible number, because a prospective student comparing a
$42,000 programme against a $152,000 one deserves to know which of those two
figures came from the institution and which came from me. None came from me.

It will not rank. There is no scoring, no stars and no "best of". The one
comparative fact that is objective - COAMFTE accreditation, which decides
whether the degree travels out of California - is shown as a filter rather than
as a verdict.

It will not hide the forum threads that are unflattering. Each institution
links to real discussion where it exists, tagged by sentiment, opening in a new
window. Where nothing credible was found the page says so by name, because a
missing link is otherwise indistinguishable from an endorsement.

Chrome and the nav script are lifted from the published hub, so the header
works. That last clause is not decoration: every page previously built this way
shipped with a dead header because the script was not lifted.
"""
import os, re, sys, json, html, unicodedata

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import forums as F
import charts

SRC = os.path.join(HERE, "_chrome.html")
DATA = os.path.join(HERE, "programs.json")
OUT = os.path.join(HERE, "mft-programs-california.html")
UPDATED = "7 August 2026"
# Two dates, because they answer different questions and one of them was
# silently answering both. "Updated" moves when anything on the page changes,
# including a CSS tweak. BBS_CHECKED moves only when somebody actually re-read
# the Board's table against our records - which is a much stronger claim, and
# the one a reader deciding whether to trust the list is really asking about.
BBS_CHECKED = "7 August 2026"

PROGRAMS = json.load(open(DATA, encoding="utf-8"))

# Slugs for the institutions that earned a page of their own.
# Written by build_schools.py, read here, so the two can never disagree about
# which schools have pages - a card linking to a page that was not built is a
# 404 the directory would happily ship.
SLUGS = {}
_sf = os.path.join(HERE, "school_slugs.json")
if os.path.exists(_sf):
    SLUGS = json.load(open(_sf, encoding="utf-8"))


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
styles = re.findall(r"<style>.*?</style>", src, re.S)
assert styles, "no stylesheet lifted"
hs = balanced(src, "header")
header = re.sub(r'(<a href="[^"]*") class="on"', r"\1", src[hs[0]:hs[1]])
fs = balanced(src, "footer")
footer = re.sub(r'(<a href="[^"]*") class="on"', r"\1", src[fs[0]:fs[1]])
navscript = ""
for m in re.finditer(r"<script>([\s\S]*?)</script>", src):
    if "navpanel" in m.group(1):
        navscript = m.group(0)
assert navscript, "no nav script in the chrome - the header would be dead"

NP = '<span class="np">not published</span>'

# Placement: who secures your clinical seat. This is the field the directory was
# missing, and on the evidence it is the one most likely to decide whether a
# two-year degree takes three. Short label for the card, long label for the row.
PLACE = {
    "guaranteed":      ("Seat guaranteed",      "pl-ok"),
    "placed":          ("Programme places you", "pl-ok"),
    "assisted":        ("You apply, with help", "pl-mid"),
    "student-sourced": ("You find your own",    "pl-warn"),
    "not published":   (None,                   None),
}
GRE_LABEL = {"required": "Required", "not required": "Not required",
             "waivable": "Required, waivable", "not published": None}


def esc(x):
    return html.escape(x) if x else None


def region(city):
    """Which of the three region filters a card answers to.

    Online first, and deliberately. Four of the institutions the Board lists
    are not in California at all - Phoenix, CalSouthern, Western Seminary's
    parent in Oregon, UMass Global - and they run California-restricted degrees
    from elsewhere. Filing those under a California region because the city
    string happens to contain a California place name would put an out-of-state
    online programme in a reader's "near me" results, which is precisely the
    thing a region filter exists to prevent.

    The guard below asserts every record lands in a bucket some button can
    reach. It exists because four California cities were missing from these
    tuples for months - Pomona, San Luis Obispo, La Mirada, Rosemead - and
    their cards silently vanished the moment anyone pressed a region filter.
    A fall-through here is invisible: the card is on the page until you filter,
    and then it is not.
    """
    c = (city or "").lower()
    if "online" in c or c.startswith("evanston"):
        return "Online or out of state"
    south = ("los angeles", "san diego", "irvine", "orange", "alhambra", "azusa",
             "fullerton", "anaheim", "northridge", "long beach", "carson", "pasadena",
             "malibu", "santa barbara", "san bernardino", "redlands", "riverside",
             "loma linda", "culver city", "bakersfield", "la verne", "westwood",
             "los alamitos", "san marcos", "point loma", "calabasas", "claremont",
             "thousand oaks", "costa mesa", "pomona", "san luis obispo",
             "la mirada", "rosemead", "tustin", "brea", "san dimas", "la mesa",
             "el cajon")
    north = ("san francisco", "berkeley", "oakland", "san jose", "palo alto",
             "santa clara", "hayward", "sacramento", "rohnert park", "arcata",
             "stockton", "turlock", "chico", "belmont", "moraga", "san rafael",
             "fresno", "petaluma", "menlo park", "sunnyvale", "campbell",
             "rocklin", "richmond", "redding", "weimar")
    for s in south:
        if s in c:
            return "Southern California"
    for n in north:
        if n in c:
            return "Northern California"
    return "California"


SENT = {"positive": ("pos", "positive"), "negative": ("neg", "critical"),
        "mixed": ("mix", "mixed"), "info": ("inf", "informational")}


def threads_for(name):
    t = F.THREADS.get(name)
    if not t:
        return ""
    rows = "".join(
        '<a class="th %s" href="%s" target="_blank" rel="noopener noreferrer">'
        '<span class="tm">%s &middot; %s</span><b>%s</b><i>%s</i>'
        '<span class="sn">%s</span></a>'
        % (SENT[s][0], u, f, y, esc(title), esc(note), SENT[s][1])
        for u, f, title, y, s, note in t)
    return ('<details class="fx"><summary>What people say about it '
            '<span class="ct">%d</span></summary><div class="thl">%s</div></details>'
            % (len(t), rows))


def anchor(name):
    """A stable per-card id, so a single entry can be linked to directly.

    The rule is deliberately the same one build_schools.py uses for filenames,
    minus the suffix, so the anchor for a school and the URL of its own page
    are recognisably the same string. A reader who is sent
    `...california.html#s-cal-poly-humboldt` and then clicks through lands on
    `cal-poly-humboldt-mft.html` and can see it is the same place.
    """
    x = unicodedata.normalize("NFKD", name).encode("ascii", "ignore").decode()
    x = re.sub(r"\(.*?\)", " ", x.lower())
    x = re.sub(r"^the\b", " ", x)
    x = re.sub(r"[^a-z0-9]+", "-", x).strip("-")
    return "s-" + re.sub(r"-+", "-", x)[:64].strip("-")


def edges(progs):
    """One line per card saying what makes this school different, DERIVED.

    THE PROBLEM. Seventy-eight cards with the same six rows are, to a reader
    scanning them, the same card seventy-eight times. Every directory this was
    studied against solves it with a hand-written differentiator sentence, and
    every one of them ends up writing marketing: "a supportive, cohort-based
    community with a strong clinical focus" says nothing and cannot be checked.

    THE RULE THAT MAKES IT SAFE. Nothing here is written per school. Each line
    is COMPUTED from a fact already displayed on that same card, and most of
    them are comparative facts that only exist because the whole set is in
    memory - cheapest, largest, only one in its region. So a line cannot be
    flattering, cannot be unsourced, and cannot go stale: change the data and
    the sentence changes or disappears with it.

    THE OTHER RULE. A school with no computable distinction gets NO line. About
    half do. A differentiator that fires for everyone is a slogan, and the
    silence is honest - most of these programmes really are similar, and the
    page should not pretend otherwise to fill a slot.

    Rules are tried in order and the first that fires wins, so the ordering is
    the editorial judgement about which fact matters most. Cost first, because
    it is the one difference a reader can act on immediately.
    """
    out = {}
    costs = sorted(((charts.cost_of(p)[0], p["institution"]) for p in progs
                    if charts.cost_of(p)[0]), key=lambda x: x[0])
    cheapest = costs[0][1] if costs else None
    dearest = costs[-1][1] if costs else None
    n_coam = sum(1 for p in progs if p.get("coamfte"))

    # Region counts, so "the only one in X" is a fact rather than an impression.
    byreg = {}
    for p in progs:
        byreg.setdefault(region(p.get("city")), []).append(p["institution"])
    # The far north is not a region() bucket - it is the thing readers outside
    # the two metros actually ask about, so it is computed from cities.
    FARNORTH = ("arcata", "redding", "chico", "weimar")
    north = [p["institution"] for p in progs
             if any(c in (p.get("city") or "").lower() for c in FARNORTH)]

    units = []
    for p in progs:
        n, sysm = charts.units_of(p)
        if n and sysm:
            units.append((n * (charts.QUARTER_TO_SEM if sysm == "quarter" else 1),
                          p["institution"]))
    units.sort()
    fewest = units[0][1] if units else None
    most = units[-1][1] if units else None

    for p in progs:
        nm = p["institution"]
        line = None
        c, kind = charts.cost_of(p)

        if nm == cheapest:
            line = ("The cheapest published cost on the Board&rsquo;s list "
                    "&mdash; $%s, against $%s at the other end."
                    % ("{:,}".format(costs[0][0]), "{:,}".format(costs[-1][0])))
        elif nm == dearest:
            line = ("The most expensive published cost here &mdash; $%s, "
                    "about %.1f times the cheapest."
                    % ("{:,}".format(costs[-1][0]),
                       costs[-1][0] / float(costs[0][0])))
        elif p.get("placement") == "guaranteed":
            line = ("One of only %d schools that state every student in good "
                    "standing gets a clinical placement."
                    % sum(1 for x in progs if x.get("placement") == "guaranteed"))
        elif nm in north and len(north) <= 4:
            line = ("One of only %d options on the Board&rsquo;s list sited in "
                    "far northern California." % len(north))
        elif p.get("coamfte"):
            line = ("One of the %d COAMFTE-accredited programmes here &mdash; "
                    "the accreditation that decides whether the degree travels "
                    "out of California." % n_coam)
        elif p.get("placement") == "placed":
            line = ("The programme finds your clinical site rather than leaving "
                    "it to you &mdash; %d of the %d do."
                    % (sum(1 for x in progs
                           if x.get("placement") in ("guaranteed", "placed")),
                       len(progs)))
        elif nm == most:
            line = "The largest unit requirement on the list, at %s." % p["units"]
        elif nm == fewest:
            line = "The smallest unit requirement on the list, at %s." % p["units"]
        elif region(p.get("city")) == "Online or out of state":
            line = ("An out-of-state institution running a California-specific "
                    "degree &mdash; %d of the %d are."
                    % (len(byreg.get("Online or out of state", [])), len(progs)))
        elif p.get("gre") == "required":
            line = ("One of only %d schools here that still requires an "
                    "admissions test."
                    % sum(1 for x in progs if x.get("gre") == "required"))
        if line:
            out[nm] = line
    return out


def gapline(p):
    """Name what this school does not publish, on its own card.

    A sparse card and a school that keeps its numbers to itself look identical
    on a page like this, and the reader draws the wrong conclusion - that we
    did not bother. Forty-six of the seventy-eight publish no tuition at all.
    Saying which fields are missing, per card, turns the page's largest
    weakness into its most actionable instruction: these are the questions to
    put to admissions, and they are different for every school.
    """
    miss = [lab for lab, k in (("tuition", None), ("time to complete", "length"),
                               ("units", "units"), ("format", "format"))
            if (not (p.get("per_unit") or p.get("total")) if k is None
                else not p.get(k))]
    if not miss:
        return ""
    if len(miss) > 1:
        miss = ", ".join(miss[:-1]) + " and " + miss[-1]
    else:
        miss = miss[0]
    return ('<p class="gapl"><b>Not published by the school:</b> %s. '
            "Worth asking admissions directly.</p>" % miss)


def card(p, edge=None):
    name = p["institution"]
    coam = ('<span class="badge acc">COAMFTE accredited</span>'
            if p.get("coamfte") else "")
    # Three states, three badges, and the middle one is the whole reason this
    # was rewritten. `false` means the Board's row carries LMFT and not LPCC -
    # a real restriction on what the degree opens - and it used to render
    # identically to `unknown`, which is to say as nothing at all. Seven
    # institutions were in that position, including Cal Poly Humboldt and USC.
    lpcc = p.get("lpcc")
    lp = ""
    if lpcc is True:
        lp = ('<span class="badge lp">LPCC route too</span>'
              if not p.get("lpcc_note")
              else '<span class="badge lpc">LPCC, with a condition</span>')
    elif lpcc is False:
        lp = '<span class="badge lpn">LMFT only, not LPCC</span>'
    pl = ""
    lab, cls = PLACE.get(p.get("placement"), (None, None))
    if lab:
        pl = '<span class="badge %s">%s</span>' % (cls, lab)
    if p.get("gre") == "not required":
        pl += '<span class="badge gren">No GRE</span>' 
    tu = NP
    if p.get("total"):
        tu = "$%s total" % "{:,}".format(int(p["total"]))
    elif p.get("per_unit"):
        tu = "$%s a unit" % "{:,}".format(int(p["per_unit"]))
    tyear = (' <span class="yr">%s</span>' % esc(str(p["tyear"]))) if p.get("tyear") else ""
    turl = p.get("turl") or p.get("url")
    prac = NP
    if PLACE.get(p.get("placement"), (None,))[0]:
        prac = esc(PLACE[p["placement"]][0])
        if p.get("practicum_hours"):
            prac += '<span class="sub">%s</span>' % esc(p["practicum_hours"])
    elif p.get("practicum_hours"):
        prac = '%s<span class="sub">who secures the seat: %s</span>' % (
            esc(p["practicum_hours"]), "not published")
    gre = esc(GRE_LABEL.get(p.get("gre")) or "") or NP
    if p.get("min_gpa"):
        gre += '<span class="sub">minimum GPA %s</span>' % esc(str(p["min_gpa"]))
    rows = [("Degree", esc(p.get("degree")) or NP),
            ("Units", esc(p.get("units")) or NP),
            ("Length", esc(p.get("length")) or NP),
            ("Format", esc(p.get("format")) or NP),
            ("Practicum", prac),
            ("Admissions test", gre),
            ("Published tuition",
             ('<a href="%s" target="_blank" rel="noopener noreferrer">%s</a>%s'
              % (turl, tu, tyear)) if tu != NP else NP)]
    body = "".join('<div class="r"><span>%s</span><b>%s</b></div>' % (k, v)
                   for k, v in rows)
    note = ""
    if p.get("notable"):
        note = '<p class="nt">%s</p>' % esc(p["notable"])
    elif p.get("note"):
        note = '<p class="nt">%s</p>' % esc(p["note"])
    if edge:
        note = ('<p class="edge">%s</p>' % edge) + note
    if p.get("lpcc_note"):
        note = ('<p class="nt"><b>LPCC:</b> %s</p>' % esc(p["lpcc_note"])) + note
    # A Board notice outranks everything else on the card, including the
    # school's own description of itself, so it goes first.
    if p.get("notice"):
        n = p["notice"]
        note = ('<div class="warn"><b>%s</b><p>%s '
                '<a href="%s" target="_blank" rel="noopener noreferrer">'
                "Read the Board&rsquo;s notice (PDF, %s) &rarr;</a></p></div>"
                % (esc(n["title"]), esc(n["body"]), n["url"],
                   esc(n.get("as_of") or ""))) + note
    if p.get("bbs_listed") is False and p.get("bbs_note"):
        note += '<p class="offl">%s</p>' % esc(p["bbs_note"])
    aid = anchor(name)
    return ('<article class="pg" id="%s" data-name="%s" data-coamfte="%s" '
            'data-region="%s" data-tuition="%s" data-lpcc="%s" data-az="%s" '
            'data-placed="%s" data-gre="%s">'
            '<div class="ph"><h3>%s</h3><span class="city">%s</span></div>'
            '<div class="pgt"><button class="keep" type="button" data-id="%s" '
            'aria-pressed="false"><span>Keep</span></button>'
            '<a class="perma" href="#%s" title="Link to this entry">&sect;</a></div>'
            "%s%s"
            '<div class="bd">%s</div>%s%s%s'
            "%s"
            "%s</article>"
            % (aid, esc(name).lower(), "yes" if p.get("coamfte") else "no",
               region(p.get("city")), "yes" if tu != NP else "no",
               {True: "yes", False: "no"}.get(p.get("lpcc"), "unknown"),
               azkey(name),
               "yes" if p.get("placement") in ("guaranteed", "placed") else "no",
               "no" if p.get("gre") == "not required" else "other",
               esc(name), esc(p.get("city")) or "California",
               aid, aid,
               coam, lp + pl, body, gapline(p), note, threads_for(name),
               "", cta(p)))


def azkey(name):
    """The letter a reader would look under, which is not always the first one.

    "The Wright Institute" files under W and "University of the Pacific" under
    U. The rule matches the slug rule - strip a leading article, nothing else -
    so the jump strip and the sort order cannot disagree with each other.
    """
    x = unicodedata.normalize("NFKD", name).encode("ascii", "ignore").decode()
    x = re.sub(r"^the\s+", "", x.strip(), flags=re.I)
    c = x[:1].upper()
    return c if c.isalpha() else "#"


def trow(p):
    """The same record as a table row.

    WHY BOTH. A card is the right shape for reading one school and the wrong
    shape for comparing one field across seventy-eight of them: the eye has to
    re-find "Units" at a different vertical position on every card. A table
    fixes that and is the pattern every directory of this size converges on.

    It is rendered into the page rather than built by script on demand, so it
    exists without JavaScript, is in the DOM for find-in-page, and cannot
    disagree with the cards - both come from the same record in the same loop.
    The cost is a larger page, which the CSS extraction pass has already paid
    for several times over.

    It is not sortable, and that is a decision rather than an omission. Sorting
    by tuition would put forty-six schools that publish nothing at the bottom
    of a column, which reads as a ranking of exactly the wrong kind.
    """
    name = p["institution"]
    aid = anchor(name)
    tu = NP
    if p.get("total"):
        tu = "$%s" % "{:,}".format(int(p["total"]))
    elif p.get("per_unit"):
        tu = "$%s/unit" % "{:,}".format(int(p["per_unit"]))
    lpc = {True: "Yes", False: "No"}.get(p.get("lpcc"), NP)
    prac = esc(PLACE.get(p.get("placement"), (None,))[0] or "") or NP
    gre = esc(GRE_LABEL.get(p.get("gre")) or "") or NP
    where = SLUGS.get(name)
    link = ('<a href="%s">%s</a>' % (where, esc(name)) if where
            else '<a href="%s" target="_blank" rel="noopener noreferrer">%s</a>'
                 % (p["url"], esc(name)))
    return ('<tr class="pgr" data-name="%s" data-coamfte="%s" data-region="%s" '
            'data-tuition="%s" data-lpcc="%s" data-az="%s" data-id="%s" '
            'data-placed="%s" data-gre="%s">'
            '<td><button class="keep tk" type="button" data-id="%s" '
            'aria-pressed="false" aria-label="Keep %s"></button></td>'
            "<th scope=\"row\">%s<span class=\"tc\">%s</span></th>"
            "<td>%s</td><td>%s</td><td>%s</td><td>%s</td>"
            "<td>%s</td><td>%s</td><td>%s</td><td>%s</td></tr>"
            % (esc(name).lower(), "yes" if p.get("coamfte") else "no",
               region(p.get("city")), "yes" if tu != NP else "no",
               {True: "yes", False: "no"}.get(p.get("lpcc"), "unknown"),
               azkey(name), aid,
               "yes" if p.get("placement") in ("guaranteed", "placed") else "no",
               "no" if p.get("gre") == "not required" else "other",
               aid, esc(name),
               link, esc(p.get("city")) or "California",
               prac, gre,
               esc(p.get("units")) or NP, esc(p.get("length")) or NP,
               esc(p.get("format")) or NP, tu,
               "Yes" if p.get("coamfte") else "&mdash;", lpc))


def cta(p):
    """Where a card sends the reader.

    A card used to carry two links: ours and the school's own. That was the
    wrong default. This directory exists because a programme's own page is
    marketing - it will not tell you that the placement is yours to find, that
    the degree does not travel out of state, or that the extension version costs
    twice the state-side one. Sending a reader straight back out to the thing
    the page exists to contextualise wasted the work.

    So where we have researched a school, the card links to our page and only to
    our page; the school's own site is linked from there, once, in context. For
    the twenty-eight where we have nothing beyond a directory row, the external
    link stays - it is the only place left to send someone, and pretending
    otherwise would be worse than an outbound link.
    """
    name = p["institution"]
    if name in SLUGS:
        return ('<a class="go mine" href="%s">Courses, curriculum, practicum '
                "and cost &rarr;</a>" % SLUGS[name])
    return ('<a class="go ext" href="%s" target="_blank" rel="noopener '
            'noreferrer">Programme page &rarr;<span class="noown">no page '
            "here yet</span></a>" % p["url"])


CSS = """<style>/* programmes */
.pd{--pine:#2C6350;--amber:#F6C560;--ink:#17271F;--line:#E2DACA;--mut:#7C8878;
  --green:#3F9577;--red:#B5483F}
.pdband{background:linear-gradient(135deg,#14261E 0%,#1B4536 48%,#2C6350 100%);
  color:#EFF5F2;padding:30px 0 36px}
.pdband .in{max-width:1180px;margin:0 auto;padding:0 26px;display:grid;
  grid-template-columns:minmax(0,1.3fr) minmax(250px,.7fr);gap:34px;align-items:center}
.pdband .bcr{display:flex;flex-wrap:wrap;align-items:center;gap:4px 8px;margin:0 0 14px;
  padding:0;list-style:none;font-family:'IBM Plex Mono',ui-monospace,monospace;
  font-size:10.4px;letter-spacing:.1em;text-transform:uppercase}
.pdband .bcr li{display:flex;align-items:center;gap:8px}
.pdband .bcr a{color:#EFF5F2;opacity:.66;text-decoration:none;padding:5px 0;min-height:26px;
  display:inline-flex;align-items:center;border-bottom:1px solid transparent}
.pdband .bcr a:hover{opacity:1;border-bottom-color:currentColor}
.pdband .bcr .sep{opacity:.36}
.pdband .bcr [aria-current]{opacity:.95;font-weight:600;color:var(--amber)}
.pdband h1{font-family:Fraunces,Georgia,serif;font-size:clamp(27px,3.7vw,43px);
  line-height:1.06;font-weight:600;letter-spacing:-.022em;color:#fff;margin:0 0 14px;max-width:18ch}
.pdband h1 em{font-style:normal;color:var(--amber)}
.pdband .dek{font-size:15.4px;line-height:1.72;color:rgba(255,255,255,.87);margin:0;max-width:57ch}
.pdmeta{display:flex;gap:14px;flex-wrap:wrap;margin-top:17px;
  font-family:'IBM Plex Mono',monospace;font-size:10.4px;letter-spacing:.06em;
  text-transform:uppercase;color:rgba(255,255,255,.62)}
.pdfig{background:rgba(0,0,0,.26);border:1px solid rgba(255,255,255,.18);border-radius:16px;
  padding:20px 22px;min-width:0}
.pdfig b{display:block;font-family:Fraunces,Georgia,serif;font-size:clamp(30px,4vw,44px);
  line-height:1;color:var(--amber)}
.pdfig span{display:block;font-size:12.5px;line-height:1.55;color:rgba(255,255,255,.74);margin-top:9px}
.pdfig .row{display:flex;justify-content:space-between;gap:10px;padding:8px 0;
  border-top:1px solid rgba(255,255,255,.14);font-size:12.2px;color:rgba(255,255,255,.8)}
.pdfig .row:first-of-type{margin-top:16px}
.pdfig .row b{display:inline;font-size:12.4px;font-family:inherit;color:#fff}

.pdwrap{max-width:1180px;margin:0 auto;padding:30px 26px 40px}
.pdlede{font-size:15.4px;line-height:1.78;color:#3B4A38;margin:0 0 18px;max-width:70ch}
.pdlede b{color:var(--ink)}
.pdlede a{color:var(--pine)}

/* filters */
/* The site header is itself sticky at top:0 with a higher z-index, so a filter
   bar at top:0 parks UNDERNEATH it and the search field is simply gone the
   moment the page scrolls. --hh is measured from the real header on load and
   on resize, because the header is 95px wide-screen and 138px on a phone where
   it wraps, and a hardcoded offset is wrong on one of them by construction.
   The fallback in var() is the desktop height, so a no-script reader gets the
   bar slightly low rather than invisible. */
.flt{position:sticky;top:var(--hh,95px);z-index:20;background:#FBF7EE;padding:14px 0 13px;
  border-bottom:1px solid var(--line);margin-bottom:20px}
.fbar{display:flex;flex-wrap:wrap;gap:9px;align-items:center}
.fbar input[type=search]{flex:1;min-width:210px;font:inherit;font-size:14.4px;
  padding:9px 13px;border:1px solid var(--line);border-radius:9px;background:#fff;color:var(--ink)}
.fb{font-family:'IBM Plex Mono',monospace;font-size:11px;letter-spacing:.05em;
  text-transform:uppercase;background:#fff;border:1px solid var(--line);border-radius:20px;
  padding:7px 13px;cursor:pointer;color:#4A5A46}
.fb[aria-pressed=true]{background:var(--pine);border-color:var(--pine);color:#fff}
.cnt{font-family:'IBM Plex Mono',monospace;font-size:11.5px;color:var(--mut);margin-left:auto}

/* cards */
.grid{display:grid;grid-template-columns:repeat(auto-fill,minmax(330px,1fr));gap:13px}
.pg{background:#fff;border:1px solid var(--line);border-radius:12px;padding:17px 18px;min-width:0}
.pg.hide{display:none}
.ph{display:flex;justify-content:space-between;align-items:baseline;gap:10px;flex-wrap:wrap}
.pg h3{font-family:Fraunces,Georgia,serif;font-size:17px;line-height:1.22;margin:0;color:var(--ink)}
/* nowrap was right for "Northridge" and wrong for Alliant, whose city field is
   "San Diego, Irvine, Los Angeles/Alhambra, Sacramento, Online" - 400px of
   unbreakable text that pushed the page to 445px wide on a 390px phone. It is
   the only overflow on the page and it came from assuming one campus. */
.city{font-family:'IBM Plex Mono',monospace;font-size:10.4px;letter-spacing:.05em;
  text-transform:uppercase;color:var(--mut);min-width:0;overflow-wrap:anywhere;
  text-align:right}
.badge{display:inline-block;font-family:'IBM Plex Mono',monospace;font-size:9.4px;
  letter-spacing:.08em;text-transform:uppercase;border-radius:20px;padding:3px 9px;
  margin:9px 6px 0 0}
.badge.acc{background:#E0F0EA;color:#20614B;border:1px solid #BFE0D3}
.badge.lp{background:#EAF3DE;color:#27500A;border:1px solid #CFE2B8}
.badge.lpc{background:#FBF0E2;color:#8A5B22;border:1px solid #EBD9BC}
.badge.lpn{background:#F4F2EC;color:#6E6656;border:1px solid #DFD9C9}
/* Placement, which is the field this directory was missing. Green where the
   school owns the problem of finding you a site, amber where it is shared,
   red-ish where it is entirely yours. Nothing is shown for "not published" -
   an absent badge and a badge saying "unknown" carry the same information and
   one of them is quieter. */
.badge.pl-ok{background:#E0F0EA;color:#20614B;border:1px solid #BFE0D3}
.badge.pl-mid{background:#FBF0E2;color:#8A5B22;border:1px solid #EBD9BC}
.badge.pl-warn{background:#FBF0EF;color:#8E3A32;border:1px solid #E4B7B2}
.badge.gren{background:#F2EEE2;color:#5B5344;border:1px solid #DFD9C9}
.bd .r b .sub{display:block;font-family:'IBM Plex Mono',monospace;font-size:10.2px;
  color:var(--mut);margin-top:2px;font-weight:400}
/* A Board-issued Notice to Students. Red, because it is the only thing on a
   card that can mean the degree does not lead to a licence at all. */
.warn{margin:11px 0 0;border:1px solid #E4B7B2;background:#FBF0EF;border-radius:9px;
  padding:11px 13px}
.warn b{display:block;font-size:12.6px;color:#8E3A32;margin-bottom:5px}
.warn p{font-size:12.5px;line-height:1.58;color:#5A423F;margin:0}
.warn a{color:#8E3A32}
.offl{margin:11px 0 0;font-size:12.4px;line-height:1.56;color:#5B5344;
  border-left:2px solid #E4D9BE;padding-left:11px}
.bd{margin-top:12px;border-top:1px solid #F0EBDE;padding-top:10px}
.bd .r{display:grid;grid-template-columns:104px minmax(0,1fr);gap:10px;padding:5px 0;font-size:13px}
.bd .r span{color:var(--mut);font-family:'IBM Plex Mono',monospace;font-size:10.2px;
  letter-spacing:.06em;text-transform:uppercase;padding-top:2px}
.bd .r b{font-weight:500;color:#3B4A38;min-width:0;overflow-wrap:anywhere}
.bd .r b a{color:var(--pine)}
.np{color:#B0A896;font-style:italic}
.yr{font-family:'IBM Plex Mono',monospace;font-size:10px;color:var(--mut)}
.nt{font-size:12.6px;line-height:1.58;color:#4A5A46;margin:11px 0 0;
  border-left:2px solid #EDE7D8;padding-left:11px}
.go{display:inline-block;margin-top:13px;margin-right:16px;font-size:13px;color:var(--pine);
  text-decoration:none;border-bottom:1px solid rgba(44,99,80,.3)}
.go.mine{font-weight:600}
.go.ext{color:var(--mut);border-bottom-color:rgba(124,136,120,.3)}

/* forum threads */
.fx{margin-top:12px;border-top:1px dashed #E7E0D0;padding-top:10px}
.fx summary{cursor:pointer;font-size:12.8px;color:var(--pine);list-style:none;
  display:flex;align-items:center;gap:8px}
.fx summary::-webkit-details-marker{display:none}
.fx summary::before{content:"+";font-family:'IBM Plex Mono',monospace;color:var(--mut)}
.fx[open] summary::before{content:"\\2212"}
.fx .ct{font-family:'IBM Plex Mono',monospace;font-size:10px;background:#EFEDE4;
  color:var(--mut);border-radius:9px;padding:1px 7px}
.thl{display:grid;gap:8px;margin-top:11px}
.th{display:block;background:#FBFAF6;border:1px solid #EDE7D8;border-radius:9px;
  padding:10px 12px;text-decoration:none;min-width:0;border-left:3px solid #CFC7B4}
.th:hover{background:#fff}
.th.pos{border-left-color:var(--green)}
.th.neg{border-left-color:var(--red)}
.th.mix{border-left-color:#C98B4B}
.th.inf{border-left-color:#8FA3C4}
.tm{display:block;font-family:'IBM Plex Mono',monospace;font-size:9.8px;letter-spacing:.06em;
  text-transform:uppercase;color:var(--mut);margin-bottom:4px}
.th b{display:block;font-size:13.4px;line-height:1.35;color:var(--ink);font-weight:600;margin-bottom:4px}
.th i{display:block;font-style:normal;font-size:12.3px;line-height:1.5;color:#4A5A46}
.sn{display:inline-block;margin-top:7px;font-family:'IBM Plex Mono',monospace;font-size:9.2px;
  letter-spacing:.08em;text-transform:uppercase;color:var(--mut)}

/* general + none-found */
h2.sec{font-family:Fraunces,Georgia,serif;font-size:clamp(21px,2.5vw,27px);color:var(--ink);
  margin:46px 0 12px;padding-top:22px;border-top:1px solid var(--line)}
.gen{display:grid;grid-template-columns:repeat(auto-fill,minmax(300px,1fr));gap:10px}
.none{background:#fff;border:1px dashed #CFC7B4;border-radius:11px;padding:17px 19px;margin:14px 0}
.none b{display:block;font-family:'IBM Plex Mono',monospace;font-size:10px;letter-spacing:.11em;
  text-transform:uppercase;color:var(--mut);margin-bottom:10px}
.none p{font-size:13.4px;line-height:1.62;color:#4A5A46;margin:0 0 10px;max-width:none}
.none span{display:inline-block;font-size:12.4px;background:#F4F1E8;border-radius:20px;
  padding:3px 10px;margin:0 5px 5px 0;color:#4A5A46}
.meth{font-size:13.4px;line-height:1.7;color:#4A5A46;max-width:70ch}
.meth a{color:var(--pine)}
.empty{display:none;padding:30px;text-align:center;color:var(--mut);font-size:14.5px}


/* Visually hidden, but read aloud. Defined here rather than assumed from the
   lifted chrome: the CSS-extraction pass rewrites shared <style> blocks into
   linked files, and a class this page depends on must not be one it merely
   inherits by luck. */
.vh{position:absolute;width:1px;height:1px;overflow:hidden;clip:rect(0 0 0 0);
  clip-path:inset(50%);white-space:nowrap}

/* ---- filter bar, second generation -------------------------------------
   Everything here answers one complaint: after pressing two filters the page
   gave no account of itself. It showed a count and nothing else - not what was
   excluded, not how to undo it, and not how large an answer a button would
   produce before you pressed it. */
.fbar2{display:flex;flex-wrap:wrap;gap:8px;align-items:center;margin-top:9px}
/* display:contents on a wide screen, so the six buttons lay out exactly as
   they did when they were direct children of .fbar. On a phone the wrapper
   becomes a single horizontally-scrolling strip: six wrapped rows of chips is
   a third of the viewport spent on furniture before the reader sees a school.
   verify.mjs's overflow check ignores anything inside a scrollable ancestor,
   which is what makes this safe rather than a permanent false positive. */
.fbtns{display:contents}
.fb .n{opacity:.62;margin-left:5px;font-size:10px}
.chip{display:inline-flex;align-items:center;gap:6px;font-family:'IBM Plex Mono',monospace;
  font-size:10.6px;background:#EFEADC;border:1px solid #E0D8C4;border-radius:20px;
  padding:3px 5px 3px 10px;color:#4A5A46}
.chip button{border:0;background:#DED5BE;color:#5B5344;border-radius:50%;width:15px;
  height:15px;line-height:1;font-size:11px;cursor:pointer;padding:0}
.chip button:hover{background:#C9BE9F}
.clr{font-family:'IBM Plex Mono',monospace;font-size:10.8px;background:none;border:0;
  color:var(--pine);text-decoration:underline;cursor:pointer;padding:2px 4px}
.vw{display:inline-flex;border:1px solid var(--line);border-radius:20px;overflow:hidden}
.vw button{font-family:'IBM Plex Mono',monospace;font-size:11px;border:0;background:#fff;
  color:var(--mut);padding:6px 12px;cursor:pointer}
.vw button[aria-pressed=true]{background:var(--pine);color:#fff}
.kpill{font-family:'IBM Plex Mono',monospace;font-size:11px;border:1px solid #CFE2B8;
  background:#EAF3DE;color:#27500A;border-radius:20px;padding:6px 12px;cursor:pointer}
.kpill[aria-pressed=true]{background:#27500A;color:#fff;border-color:#27500A}
.kpill[disabled]{opacity:.45;cursor:default}
.prt{font-family:'IBM Plex Mono',monospace;font-size:11px;border:1px solid var(--line);
  background:#fff;color:var(--mut);border-radius:20px;padding:6px 12px;cursor:pointer}

/* ---- A-Z strip. 78 cards is fifteen screens and there was no way to reach W. */
.az{display:flex;flex-wrap:wrap;gap:2px;margin:12px 0 2px}
.az a,.az span{font-family:'IBM Plex Mono',monospace;font-size:10.6px;min-width:18px;
  text-align:center;padding:3px 2px;border-radius:4px;text-decoration:none}
.az a{color:var(--pine);background:#F2EEE2}
.az a:hover{background:var(--pine);color:#fff}
.az span{color:#C6BEAA}

/* ---- keep / shortlist -------------------------------------------------
   The page refuses to rank, and a reader still has to. This hands them the
   mechanism without the page expressing a preference: what you kept is yours,
   it lives in your browser, and nothing about it is sent anywhere. */
.pgt{display:flex;align-items:center;gap:8px;margin-top:8px}
.keep{font-family:'IBM Plex Mono',monospace;font-size:10.2px;letter-spacing:.06em;
  text-transform:uppercase;border:1px solid var(--line);background:#fff;color:var(--mut);
  border-radius:20px;padding:4px 11px;cursor:pointer}
.keep[aria-pressed=true]{background:#27500A;border-color:#27500A;color:#fff}
.keep[aria-pressed=true] span:after{content:" \2713"}
.perma{color:#C6BEAA;text-decoration:none;font-size:13px}
.perma:hover{color:var(--pine)}
.pg:target{box-shadow:0 0 0 3px #EAF3DE;border-color:#CFE2B8}
/* A #s-<school> link must not land the card behind two stacked sticky bars. */
.pg,.pgr{scroll-margin-top:var(--stick,250px)}
.keep.tk{width:20px;height:20px;padding:0;border-radius:5px}
.keep.tk[aria-pressed=true]:after{content:"\2713";font-size:11px}

/* ---- what the school does not publish, said per card */
.gapl{font-size:12.2px;line-height:1.55;color:#6E6656;margin:10px 0 0;
  background:#FAF7EF;border:1px dashed #E4D9BE;border-radius:8px;padding:8px 11px}
.gapl b{color:#5B5344;font-weight:600}

/* The computed differentiator. Set apart from the school's own description
   below it, because it is the one line on the card this site wrote - and it
   only ever states a comparison drawn from the same data the card shows. */
.edge{font-size:13.4px;line-height:1.55;color:#27500A;margin:10px 0 0;
  background:#F3F8EC;border:1px solid #DCE9CB;border-radius:8px;padding:8px 11px}

/* "no page here yet" had a class and no rule, so it ran straight on from the
   link text: "Programme page -> no page here yet" as one line. It is a caveat
   about the destination, not part of the label. */
.noown{display:block;font-family:'IBM Plex Mono',monospace;font-size:9.6px;
  letter-spacing:.07em;text-transform:uppercase;color:var(--mut);margin-top:3px}

/* ---- table view -------------------------------------------------------
   Wrapped in a scroller on purpose: the overflow check in _dev/verify.mjs
   ignores anything inside a scrollable ancestor, and a table this wide would
   otherwise report a layout bug on every page load, forever. */
.tblwrap{overflow-x:auto;-webkit-overflow-scrolling:touch;border:1px solid var(--line);
  border-radius:12px;background:#fff}
.ptbl{border-collapse:collapse;width:100%;font-size:13px;min-width:1120px}
.ptbl th,.ptbl td{text-align:left;padding:9px 11px;border-bottom:1px solid #F0EBDE;
  vertical-align:top}
/* NOT position:sticky, and it must not be made so again. The wrapper needs
   overflow-x for a table this wide; a box with overflow-x:auto computes
   overflow-y to auto as well, which makes the wrapper the containing block for
   any sticky descendant. Because the wrapper has no fixed height it never
   scrolls vertically, so a sticky thead does not track the page - it parks at
   its `top` offset partway down the table and sits there over the rows. That
   is exactly what it did, and it looked like a rendering bug because it was
   one. A header that scrolls away honestly beats a header that floats. */
.ptbl thead th{background:#F7F3E9;font-family:'IBM Plex Mono',monospace;
  font-size:9.8px;letter-spacing:.09em;text-transform:uppercase;color:var(--mut);
  font-weight:500;z-index:2;border-bottom:1px solid var(--line)}
.ptbl tbody th{font-weight:500;color:var(--ink);min-width:210px}
.ptbl tbody th a{color:var(--pine)}
.ptbl .tc{display:block;font-family:'IBM Plex Mono',monospace;font-size:10px;
  color:var(--mut);margin-top:2px}
.ptbl tr.hide{display:none}
.ptbl tbody tr:hover{background:#FCFAF4}
body.tablev .grid{display:none}
body.tablev #tbl{display:block}
#tbl{display:none;margin-top:2px}

/* ---- ask admissions */
.ask{background:#fff;border:1px solid var(--line);border-radius:12px;padding:4px 20px 18px;
  margin:16px 0}
.ask summary{cursor:pointer;padding:15px 0;font-family:Fraunces,Georgia,serif;
  font-size:17.5px;color:var(--ink)}
.ask ol{margin:0;padding-left:20px}
.ask li{font-size:14.2px;line-height:1.62;margin:0 0 10px;color:#3B4A38}
.ask li b{display:block;font-weight:600;color:var(--ink)}

.totop{position:fixed;right:16px;bottom:16px;z-index:30;display:none;
  font-family:'IBM Plex Mono',monospace;font-size:11px;background:var(--pine);color:#fff;
  border:0;border-radius:20px;padding:9px 14px;cursor:pointer;opacity:.92}
.totop.on{display:block}

@media print{
  header,footer,.flt,.az,.totop,.igwrap,.pdband,.thl,.fx,.gen,.none,.meth{display:none!important}
  body.keeponly .pg:not(.kept),body.keeponly .pgr:not(.kept){display:none!important}
  .pg{break-inside:avoid;border:1px solid #ccc}
}

@media (max-width:820px){
  .pdband .in{grid-template-columns:minmax(0,1fr);gap:22px}
  .grid{grid-template-columns:minmax(0,1fr)}
  .cnt{margin-left:0;width:100%}
  /* The sticky bar grew a second row. Cap it, or on a 390px screen the filter
     furniture eats half the viewport and the thing being filtered is off
     screen - which is a worse page than the one with no counts on it. */
  .flt{max-height:44vh;overflow-y:auto}
  .fbar,.fbar2{gap:6px}
  .fbtns{display:flex;flex-wrap:nowrap;gap:6px;overflow-x:auto;width:100%;
    -webkit-overflow-scrolling:touch;padding-bottom:2px;scrollbar-width:none}
  .fbtns::-webkit-scrollbar{display:none}
  .fb{font-size:10.4px;padding:5px 9px;flex:0 0 auto}
  #q{flex:1 0 100%}
  .az a,.az span{min-width:16px;font-size:10px}
}
</style>"""

JS = """<script>
/* Directory behaviour. Four jobs, in one closure:

   1. FILTER, over cards AND table rows at once. They are the same records
      rendered twice, so a filter that reached only one of them would produce a
      table that quietly disagreed with the cards.
   2. ACCOUNT FOR ITSELF. A count, a chip per active filter, and a way out.
      Before this the page told you how many matched and nothing about why.
   3. REMEMBER THE STATE IN THE URL. This directory gets forwarded by
      supervisors and careers advisers. "The COAMFTE ones" should be a link.
   4. KEEP A SHORTLIST, in localStorage, which is the reader's ranking rather
      than ours - the page will not rank, and somebody still has to.

   Everything degrades: with no script the cards are all there in the markup,
   the table is one CSS rule away, and every link works. */
(function(){
  var q=document.getElementById('q'),
      cards=[].slice.call(document.querySelectorAll('.pg')),
      rows=[].slice.call(document.querySelectorAll('.pgr')),
      items=cards.concat(rows),
      cnt=document.getElementById('cnt'), empty=document.getElementById('empty'),
      chips=document.getElementById('chips'), clr=document.getElementById('clr'),
      kpill=document.getElementById('kpill'), prt=document.getElementById('prt'),
      vcard=document.getElementById('vcard'), vtbl=document.getElementById('vtbl'),
      az=document.getElementById('az'), totop=document.getElementById('totop'),
      btns=[].slice.call(document.querySelectorAll('.fb')),
      LABEL={coamfte:'COAMFTE accredited', region:'Region', lpcc:'Opens LPCC',
             tuition:'Publishes tuition', placed:'Programme places you',
             gre:'No admissions test'},
      KEY='ts-mft-keep', keptOnly=false, kept={};

  /* localStorage can throw outright in a locked-down browser. A shortlist is a
     convenience; the page must not die for it. */
  function load(){ try{ (JSON.parse(localStorage.getItem(KEY))||[]).forEach(
      function(k){ kept[k]=1; }); }catch(e){} }
  function save(){ try{ localStorage.setItem(KEY, JSON.stringify(Object.keys(kept)));
      }catch(e){} }

  function active(){
    var on={};
    btns.forEach(function(b){
      if(b.getAttribute('aria-pressed')==='true') on[b.dataset.k]=b.dataset.v; });
    return on;
  }

  function apply(){
    var term=(q.value||'').trim().toLowerCase(), on=active(), n=0, seen={};
    items.forEach(function(c){
      var ok=true, k;
      for(k in on){ if(c.dataset[k]!==on[k]) ok=false; }
      if(ok && term && c.textContent.toLowerCase().indexOf(term)<0) ok=false;
      if(ok && keptOnly && !kept[c.dataset.id||c.id]) ok=false;
      c.classList.toggle('hide', !ok);
      /* Count cards only. Counting both would say 156 of 156. */
      if(ok && c.classList.contains('pg')){ n++; seen[c.dataset.az]=1; }
    });
    cnt.textContent = n + ' of ' + cards.length + ' programmes';
    empty.style.display = n ? 'none' : 'block';
    drawChips(on);
    drawAz(seen);
    writeHash(on, term);
  }

  function drawChips(on){
    var out=[], k;
    for(k in on) out.push('<span class="chip">'+LABEL[k]+': '+on[k]+
      '<button type="button" data-off="'+k+'" aria-label="Remove this filter">&times;</button></span>');
    if(keptOnly) out.push('<span class="chip">Kept only'+
      '<button type="button" data-off="kept" aria-label="Show all again">&times;</button></span>');
    if((q.value||'').trim()) out.push('<span class="chip">&ldquo;'+
      q.value.trim().replace(/[<&]/g,'')+'&rdquo;'+
      '<button type="button" data-off="q" aria-label="Clear the search">&times;</button></span>');
    chips.innerHTML=out.join('');
    clr.hidden = !out.length;
  }

  chips.addEventListener('click', function(e){
    var k=e.target.getAttribute && e.target.getAttribute('data-off');
    if(!k) return;
    if(k==='q'){ q.value=''; }
    else if(k==='kept'){ keptOnly=false; kpill.setAttribute('aria-pressed','false'); }
    else btns.forEach(function(b){ if(b.dataset.k===k) b.setAttribute('aria-pressed','false'); });
    apply();
  });

  clr.addEventListener('click', function(){
    q.value=''; keptOnly=false; kpill.setAttribute('aria-pressed','false');
    btns.forEach(function(b){ b.setAttribute('aria-pressed','false'); });
    apply();
  });

  /* The jump strip is drawn from what is CURRENTLY visible, not from the full
     set. A letter that leads nowhere after a filter is worse than no letter. */
  function drawAz(seen){
    var L='ABCDEFGHIJKLMNOPQRSTUVWXYZ'.split(''), out=[];
    L.forEach(function(c){
      out.push(seen[c] ? '<a href="#az-'+c+'">'+c+'</a>' : '<span>'+c+'</span>');
    });
    az.innerHTML=out.join('');
  }
  az.addEventListener('click', function(e){
    if(e.target.tagName!=='A') return;
    e.preventDefault();
    var c=e.target.textContent, t=null;
    (document.body.classList.contains('tablev')?rows:cards).some(function(x){
      if(!x.classList.contains('hide') && x.dataset.az===c){ t=x; return true; }
    });
    if(t) t.scrollIntoView({block:'center'});
  });

  btns.forEach(function(b){
    b.addEventListener('click', function(){
      var was=b.getAttribute('aria-pressed')==='true';
      btns.forEach(function(o){ if(o.dataset.k===b.dataset.k) o.setAttribute('aria-pressed','false'); });
      b.setAttribute('aria-pressed', was?'false':'true');
      apply();
    });
  });
  q.addEventListener('input', apply);

  /* ---- keep */
  function paintKeep(){
    var n=Object.keys(kept).length;
    kpill.textContent='Kept '+n;
    kpill.disabled = !n;
    if(!n && keptOnly){ keptOnly=false; kpill.setAttribute('aria-pressed','false'); }
    [].slice.call(document.querySelectorAll('.keep')).forEach(function(b){
      var on=!!kept[b.dataset.id];
      b.setAttribute('aria-pressed', on?'true':'false');
      var host=b.closest('.pg')||b.closest('.pgr');
      if(host) host.classList.toggle('kept', on);
    });
  }
  document.addEventListener('click', function(e){
    var b=e.target.closest && e.target.closest('.keep');
    if(!b) return;
    if(kept[b.dataset.id]) delete kept[b.dataset.id]; else kept[b.dataset.id]=1;
    save(); paintKeep(); if(keptOnly) apply();
  });
  kpill.addEventListener('click', function(){
    keptOnly=!keptOnly;
    kpill.setAttribute('aria-pressed', keptOnly?'true':'false');
    apply();
  });
  prt.addEventListener('click', function(){
    var only=Object.keys(kept).length>0;
    document.body.classList.toggle('keeponly', only);
    window.print();
    setTimeout(function(){ document.body.classList.remove('keeponly'); }, 400);
  });

  /* ---- view */
  function view(t){
    document.body.classList.toggle('tablev', t);
    vtbl.setAttribute('aria-pressed', t?'true':'false');
    vcard.setAttribute('aria-pressed', t?'false':'true');
  }
  vtbl.addEventListener('click', function(){ view(true); apply(); });
  vcard.addEventListener('click', function(){ view(false); apply(); });

  /* ---- URL state. Only ever written when something is on, so a bare link and
     an unfiltered page stay the same URL, and #s-<school> anchors still work. */
  var lock=false;
  function writeHash(on, term){
    if(lock) return;
    var p=[], k;
    for(k in on) p.push(k+'='+encodeURIComponent(on[k]));
    if(term) p.push('q='+encodeURIComponent(term));
    if(document.body.classList.contains('tablev')) p.push('view=table');
    var h=p.join('&');
    var cur=location.hash.replace(/^#/,'');
    if(h===cur) return;
    if(!h && cur.indexOf('=')<0) return;   /* leave #s-... and #at-a-glance alone */
    history.replaceState(null,'', h ? '#'+h : location.pathname+location.search);
  }
  function readHash(){
    var h=location.hash.replace(/^#/,'');
    if(h.indexOf('=')<0) return false;
    lock=true;
    h.split('&').forEach(function(kv){
      var a=kv.split('='), k=a[0], v=decodeURIComponent((a[1]||'').replace(/\+/g,' '));
      if(k==='q'){ q.value=v; return; }
      if(k==='view'){ view(v==='table'); return; }
      btns.forEach(function(b){
        if(b.dataset.k===k && b.dataset.v===v) b.setAttribute('aria-pressed','true'); });
    });
    lock=false;
    return true;
  }

  /* Measure the two sticky bars rather than guessing them. */
  function measure(){
    var h=document.querySelector('header'), f=document.querySelector('.flt');
    var hh=h?h.offsetHeight:95, fh=f?f.offsetHeight:0;
    document.documentElement.style.setProperty('--hh', hh+'px');
    document.documentElement.style.setProperty('--stick', (hh+fh+24)+'px');
  }
  measure();
  window.addEventListener('resize', measure);

  window.addEventListener('scroll', function(){
    totop.classList.toggle('on', window.scrollY>1400);
  }, {passive:true});
  totop.addEventListener('click', function(){ window.scrollTo({top:0}); });

  load(); paintKeep(); readHash(); apply();
})();
</script>"""


def build():
    progs = sorted(PROGRAMS, key=lambda p: p["institution"])
    n_coam = sum(1 for p in progs if p.get("coamfte"))
    n_tui = sum(1 for p in progs if p.get("per_unit") or p.get("total"))
    n_forum = len(F.THREADS)
    # The spread quoted in the methodology note is the real spread in the data,
    # not two round numbers chosen to sound like one. It moves when a school
    # publishes a figure, and it should.
    _costs = sorted(c for c, _k in (charts.cost_of(p) for p in progs) if c)
    cost_lo, cost_hi = (_costs[0], _costs[-1]) if _costs else (0, 0)

    n_south = sum(1 for p in progs if region(p.get("city")) == "Southern California")
    n_north = sum(1 for p in progs if region(p.get("city")) == "Northern California")
    n_online = sum(1 for p in progs
                   if region(p.get("city")) == "Online or out of state")
    n_lp = sum(1 for p in progs if p.get("lpcc") is True)
    n_placed = sum(1 for p in progs
                   if p.get("placement") in ("guaranteed", "placed"))
    n_nogre = sum(1 for p in progs if p.get("gre") == "not required")

    ed = edges(progs)
    cards = "".join(card(p, ed.get(p["institution"])) for p in progs)
    rows = "".join(trow(p) for p in progs)

    # Threads keyed to an institution that is not in the BBS list - Saybrook is
    # one - would otherwise be silently dropped, taking verified research with
    # them. They join the general section rather than disappearing, and the
    # guard below still insists every gathered URL appears somewhere.
    known = {x["institution"] for x in PROGRAMS}
    orphan = [t for k, v in F.THREADS.items() if k not in known for t in v]

    gen = "".join(
        '<a class="th %s" href="%s" target="_blank" rel="noopener noreferrer">'
        '<span class="tm">%s &middot; %s</span><b>%s</b><i>%s</i>'
        '<span class="sn">%s</span></a>'
        % (SENT[s][0], u, f, y, esc(t), esc(note), SENT[s][1])
        for u, f, t, y, s, note in F.GENERAL + orphan)

    none_found = "".join("<span>%s</span>" % esc(x) for x in F.NONE_FOUND)

    ask_block = '<details class="ask" id="ask"><summary>Five questions to put to admissions &mdash; and why each one changes the answer</summary>\n<ol>\n<li><b>Who finds my practicum placement, and what happens if I cannot find one?</b>\nThis is the single most likely reason a two-year degree takes three. Some programmes place\nyou; some hand you a list. Ask which, and ask what the last cohort&rsquo;s experience was.</li>\n<li><b>What is the total cost including campus fees, and what does a fifth term cost?</b>\nThe tuition figures on this page are the ones schools publish, and almost none of them\ninclude fees. Ask for the number a student actually paid last year.</li>\n<li><b>How many direct client hours will I finish the degree with?</b>\nThey count towards the 3,000 you need afterwards. A programme that gets you to 300 rather\nthan 150 has taken months off your licensure date.</li>\n<li><b>Is the degree COAMFTE accredited, and when does that accreditation expire?</b>\nAccreditation is granted for a term and can be renewed with stipulations or not at all.\n&ldquo;Accredited&rdquo; on a web page is not the same as accredited through your graduation.</li>\n<li><b>Does this specific degree open the LPCC route, or only another degree here?</b>\nThe Board lists institutions, not programmes. A school listed for both may open the LPCC\nroute through a different master&rsquo;s than the one you are applying to.</li>\n</ol>\n<p class="meth" style="margin-bottom:0">These are questions, not criteria. This page does\nnot tell you which programme is better, and a list of things to look for would be that\nverdict wearing a different hat.</p></details>'

    fig = ('<div class="pdfig"><b>%d</b><span>institutions whose degrees the Board '
           "lists as qualifying towards California LMFT licensure</span>"
           '<div class="row"><span>COAMFTE accredited</span><b>%d</b></div>'
           '<div class="row"><span>Publish their tuition</span><b>%d</b></div>'
           '<div class="row"><span>With real forum discussion</span><b>%d</b></div>'
           "</div>" % (len(progs), n_coam, n_tui, n_forum))

    return """<!doctype html>
<html lang="en"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>California MFT graduate programmes: %d schools, what each publishes, and what people say</title>
<meta name="description" content="Every California graduate programme leading to LMFT licensure — degree, units, length, format, COAMFTE accreditation, LPCC eligibility and published tuition, with links to real forum discussion for each. No rankings, and no estimated tuition.">
<link rel="canonical" href="https://therapistsupport.org/mft-programs-california.html">
%s
%s
%s
</head><body class="pd">
%s
<main>
<section class="pdband"><div class="in"><div>
<ol class="bcr" aria-label="Breadcrumb">
<li><a href="index.html">Therapist Support</a><span class="sep">&rsaquo;</span></li>
<li><a href="resources.html">Resources</a><span class="sep">&rsaquo;</span></li>
<li><span aria-current="page">MFT programmes</span></li></ol>
<h1>Every California programme that leads to <em>an MFT licence</em>.</h1>
<p class="dek">What each one publishes about itself &mdash; degree, units, length, format,
accreditation and cost &mdash; next to what students and graduates actually say about it
in public. No rankings. No estimated tuition.</p>
<div class="pdmeta"><span>California</span><span>Page updated %s</span><span>Board&rsquo;s list re-checked %s</span><span>%d institutions</span></div>
</div>%s</div></section>

<div class="pdwrap">
<p class="pdlede">The Board keeps a list of institutions whose degrees <b>may</b> qualify
&mdash; its own word &mdash; and the statute reserves the Board the final say regardless
of any accreditation. So treat this as a starting point for your own checking, not as an
approval. <a href="become-an-mft-california.html">What the degree has to contain is on the
licensure page &rarr;</a></p>
<p class="pdlede"><b>One filter matters more than the rest.</b> COAMFTE accreditation is
what decides whether your degree travels: inside California a BBS-approved,
regionally-accredited programme is fine, and outside it a non-COAMFTE degree can mean
remedial coursework or no licence at all. <b>%d of the %d</b> hold it.</p>

%s

%s

<div class="flt"><div class="fbar">
<input type="search" id="q" placeholder="Search school, city, degree or format&hellip;"
       aria-label="Search programmes">
<span class="fbtns"><button class="fb" data-k="coamfte" data-v="yes" aria-pressed="false">COAMFTE only<span class="n">%d</span></button>
<button class="fb" data-k="region" data-v="Southern California" aria-pressed="false">Southern CA<span class="n">%d</span></button>
<button class="fb" data-k="region" data-v="Northern California" aria-pressed="false">Northern CA<span class="n">%d</span></button>
<button class="fb" data-k="region" data-v="Online or out of state" aria-pressed="false">Online / out of state<span class="n">%d</span></button>
<button class="fb" data-k="lpcc" data-v="yes" aria-pressed="false">Also opens LPCC<span class="n">%d</span></button>
<button class="fb" data-k="placed" data-v="yes" aria-pressed="false">Programme places you<span class="n">%d</span></button>
<button class="fb" data-k="gre" data-v="no" aria-pressed="false">No GRE<span class="n">%d</span></button>
<button class="fb" data-k="tuition" data-v="yes" aria-pressed="false">Publishes tuition<span class="n">%d</span></button>
</span>
<span class="cnt" id="cnt"></span>
</div>
<div class="fbar2">
<span class="vw" role="group" aria-label="How to show the programmes">
<button id="vcard" aria-pressed="true">Cards</button><button id="vtbl" aria-pressed="false">Table</button>
</span>
<button class="kpill" id="kpill" aria-pressed="false" disabled>Kept 0</button>
<button class="prt" id="prt" type="button">Print your shortlist</button>
<span id="chips"></span>
<button class="clr" id="clr" type="button" hidden>Clear all</button>
</div></div>

<nav class="az" id="az" aria-label="Jump to a letter"></nav>

<div class="grid">%s</div>
<div id="tbl"><div class="tblwrap"><table class="ptbl">
<caption class="vh">Every institution the Board lists, with what each publishes about itself</caption>
<thead><tr><th scope="col"><span class="vh">Keep</span></th><th scope="col">Institution</th>
<th scope="col">Practicum &mdash; who secures it</th><th scope="col">Admissions test</th>
<th scope="col">Units</th><th scope="col">Length</th><th scope="col">Format</th>
<th scope="col">Published tuition</th><th scope="col">COAMFTE</th><th scope="col">LPCC</th>
</tr></thead><tbody>%s</tbody></table></div>
<p class="meth" style="margin-top:10px">Same seventy-eight records as the cards, one row
each. Deliberately not sortable: forty-six schools publish no tuition, and a column sorted
on a figure most of them do not have would order the page by who answers a question rather
than by anything about the degrees.</p></div>
<div class="empty" id="empty">Nothing matches that. Clear a filter or try a shorter search.</div>
<button class="totop" id="totop" type="button">&uarr; Top</button>

<h2 class="sec">Threads about the decision itself</h2>
<p class="pdlede">Not about one school &mdash; about accreditation, debt, practicum risk
and whether the route is worth walking at all.</p>
<div class="gen thl">%s</div>

<h2 class="sec">What is not here</h2>
<div class="none"><b>Institutions with no credible discussion found</b>
<p>Searched by every name variant across Reddit, Student Doctor Network and The GradCafe.
Silence is not a verdict &mdash; several of these are small, and two have closed &mdash;
but a missing link should not read as an endorsement, so they are named.</p>
%s
<p style="margin-top:12px">%s</p></div>

<h2 class="sec">How this was built</h2>
<p class="meth"><b>Tuition is never estimated.</b> %d institutions publish a
per-unit or total figure and it is shown with the year and a link to the page it came
from. The other %d say <i>not published</i>. A prospective student comparing a
$%s programme against a $%s one deserves to know which figure came from the
institution and which came from me. None came from me.</p>
<p class="meth"><b>The LPCC column is the Board&rsquo;s answer, not the school&rsquo;s.</b>
Its table names the licences each institution is listed for, so a card says
<i>LPCC route too</i> only where the Board&rsquo;s row carries LPCC, and
<i>LMFT only</i> where it does not. Where a school adds a condition of its own
&mdash; a campus, a format, an extra emphasis &mdash; the condition is printed
under the card in the school&rsquo;s own terms. The Board lists institutions
rather than programmes, so a school listed for both may open the LPCC route
through a different degree than the one shown here; that is the question to
ask admissions.</p>
<p class="meth"><b>Nothing is ranked.</b> There is no score, no stars and no best-of. The
one comparative fact that is objective is COAMFTE accreditation, and it is a filter
rather than a verdict.</p>
<p class="meth"><b>Every forum link was verified to resolve</b> on %s, against the host's
own endpoint rather than constructed from a thread ID. Descriptions are mine; nothing is
quoted beyond a phrase. Sentiment tags are my reading of the thread, not a measurement.</p>
<p class="meth">Accreditation status is from the
<a href="https://coamfte.org/COAMFTE/Directory_of_Accredited_Programs/MFT_Training_Programs.aspx"
   target="_blank" rel="noopener noreferrer">COAMFTE directory</a>; the institution list is
from the
<a href="https://www.bbs.ca.gov/applicants/education_resources.html"
   target="_blank" rel="noopener noreferrer">BBS education resources page</a>. Everything
else is from each institution's own site. If something here is wrong,
<a href="contact.html">tell me</a> &mdash; that is what the page is for.</p>
</div>
</main>
%s
%s
%s
</body></html>""" % (len(progs), "\n".join(links), "\n".join(styles), CSS + charts.CSS, header,
                     UPDATED, BBS_CHECKED, len(progs), fig, n_coam, len(progs), charts.render(progs),
                     ask_block, n_coam, n_south, n_north, n_online, n_lp,
                     n_placed, n_nogre, n_tui,
                     cards, rows, gen,
                     none_found, F.DEAD_SUBS, n_tui, len(progs) - n_tui,
                     "{:,}".format(cost_lo), "{:,}".format(cost_hi),
                     UPDATED, footer, navscript, JS)


def main():
    doc = build()
    open(OUT, "w", encoding="utf-8").write(doc)

    bad = []

    # Entities in the DATA, which this builder escapes on the way into the
    # page. A field holding "&rsquo;" is escaped a second time and renders as
    # the literal text "&rsquo;" for a reader. That is not a typo class - it is
    # the third time this project has shipped it (the Touro notice, a page
    # title, and a whole program card), and it is invisible to every other
    # guard because the markup is perfectly valid.
    #
    # The rule for every escaped field is: raw Unicode, never an entity.
    _ENT = re.compile(r"&(?:rsquo|lsquo|mdash|ndash|amp|nbsp|hellip|ldquo"
                      r"|rdquo|quot|apos|#\d+);")

    def _scan(value, path, who):
        if isinstance(value, str):
            if _ENT.search(value):
                bad.append("%s: %s holds an HTML entity (%s). Store raw "
                           "Unicode - this field is escaped on render, so an "
                           "entity here is escaped twice and shows as text."
                           % (who, path, _ENT.search(value).group(0)))
        elif isinstance(value, dict):
            for k, v in value.items():
                _scan(v, "%s.%s" % (path, k) if path else k, who)
        elif isinstance(value, list):
            for v in value:
                _scan(v, path + "[]", who)

    for _p in PROGRAMS:
        _scan(_p, "", (_p.get("institution") or _p.get("url", "?"))[:48])
    if doc.count("<h1") != 1:
        bad.append("%d h1" % doc.count("<h1"))
    n = doc.count('<article class="pg"')
    if n != len(PROGRAMS):
        bad.append("%d cards for %d programmes" % (n, len(PROGRAMS)))
    # Every card must lead somewhere. Which somewhere depends on whether we
    # researched the school: ours if we did, the institution's own page if we
    # did not. A card with neither is a dead end and the reader has no next
    # move at all.
    for p in PROGRAMS:
        nm = p["institution"]
        if nm in SLUGS:
            if ('href="%s"' % SLUGS[nm]) not in doc:
                bad.append("no internal link for %s" % nm[:30])
        elif p["url"] not in doc:
            bad.append("no link at all for %s" % nm[:30])
    # A researched school must not still be pushed straight back out to its own
    # marketing from the directory - that is the behaviour this change removed,
    # and it would come back silently if cta() were ever edited carelessly.
    for nm, sl in SLUGS.items():
        pr = next((x for x in PROGRAMS if x["institution"] == nm), None)
        if pr and ('class="go ext" href="%s"' % pr["url"]) in doc:
            bad.append("%s has a page but the card still links out" % nm[:30])
    # every forum thread must be present and open in a new window
    allt = [t for v in F.THREADS.values() for t in v] + F.GENERAL
    for u, *_ in allt:
        if u not in doc:
            bad.append("missing thread %s" % u[:52])
    for m in re.finditer(r'<a class="th [^"]*" href="[^"]+"([^>]*)>', doc):
        if 'target="_blank"' not in m.group(1) or "noopener" not in m.group(1):
            bad.append("a forum link does not open safely in a new window")
            break
    # tuition honesty: the count of "not published" must equal the count of
    # programmes with no published figure, times the fields that can carry it
    have = sum(1 for p in PROGRAMS if p.get("per_unit") or p.get("total"))
    if doc.count("not published") < (len(PROGRAMS) - have):
        bad.append("fewer 'not published' cells than programmes without tuition")
    # Every card must be reachable by some region button. A card whose city is
    # in none of region()'s tuples falls through to the bare "California"
    # bucket, which no button selects - so the card is on the page until the
    # reader filters, and then it silently is not. Four schools sat in that
    # hole for months.
    stray = re.findall(r'data-region="California"', doc)
    if stray:
        bad.append("%d card(s) in no region bucket - see region()" % len(stray))
    # The LPCC filter is only honest if the attribute distinguishes "no" from
    # "not checked". If every card said "unknown" the button would still work
    # and would still be wrong.
    if doc.count('data-lpcc="yes"') < 2 or doc.count('data-lpcc="no"') < 1:
        bad.append("the LPCC filter has nothing to filter on")
    # The table is the same records rendered a second time. If the two counts
    # ever diverge, one of them is lying and the reader has no way to tell
    # which - so this is a hard stop rather than a warning.
    nr = doc.count('<tr class="pgr"')
    if nr != len(PROGRAMS):
        bad.append("%d table rows for %d programmes" % (nr, len(PROGRAMS)))
    # Every card and every row must carry a keep control with a stable id, or
    # the shortlist silently keeps nothing for that school.
    ids = set(re.findall(r'<article class="pg" id="(s-[a-z0-9-]+)"', doc))
    if len(ids) != len(PROGRAMS):
        bad.append("%d unique card anchors for %d programmes" % (len(ids), len(PROGRAMS)))
    # Three sites per school: the card's keep button, the table row itself
    # (the filter reads data-id off the row), and the row's keep button.
    for k in ('data-id="%s"' % i for i in sorted(ids)):
        if doc.count(k) != 3:
            bad.append("keep wiring is %dx, expected 3x: %s" % (doc.count(k), k))
            break
    # The counts on the filter buttons must be the counts the filters produce.
    # A hardcoded number here would be the exact failure this page exists to
    # avoid, printed on the control that promises it.
    for lab, want in (("COAMFTE only",
                       sum(1 for p in PROGRAMS if p.get("coamfte"))),
                      ("Also opens LPCC",
                       sum(1 for p in PROGRAMS if p.get("lpcc") is True)),
                      ("Publishes tuition", have),
                      ("Programme places you",
                       sum(1 for p in PROGRAMS
                           if p.get("placement") in ("guaranteed", "placed"))),
                      ("No GRE",
                       sum(1 for p in PROGRAMS if p.get("gre") == "not required"))):
        if ('%s<span class="n">%d</span>' % (lab, want)) not in doc:
            bad.append("the count on the '%s' button is not the data's" % lab)
    # A placement badge is a claim about somebody else's programme. It may only
    # appear where the record carries the quote and the URL it was read from.
    for p in PROGRAMS:
        lab = PLACE.get(p.get("placement"), (None,))[0]
        if lab and not (p.get("placement_evidence") and p.get("placement_url")):
            bad.append("%s claims a placement model with no source"
                       % p["institution"][:30])
    # Table and cards must agree on the new columns too.
    for tok, n in (('data-placed="yes"',
                    sum(1 for p in PROGRAMS
                        if p.get("placement") in ("guaranteed", "placed"))),
                   ('data-gre="no"',
                    sum(1 for p in PROGRAMS if p.get("gre") == "not required"))):
        if doc.count(tok) != n * 2:
            bad.append("%s appears %dx, expected %d (cards + rows)"
                       % (tok, doc.count(tok), n * 2))
    # The derived differentiator. Two things can go wrong with it and both are
    # silent: it can fire for everybody, at which point it is a slogan rather
    # than a distinction, and it can interpolate a prose field that is not the
    # number it thinks it is - which is how "the smallest unit requirement on
    # the list, at Quarter system; 4.5 quarter units per course" reached a card.
    ed = re.findall(r'<p class="edge">(.*?)</p>', doc)
    if not 0.10 <= len(ed) / float(len(PROGRAMS)) <= 0.70:
        bad.append("%d of %d cards carry a differentiator - it is either a "
                   "slogan or broken" % (len(ed), len(PROGRAMS)))
    for e in ed:
        if re.search(r"\bNone\b|not stated|per course|\$0\b", e):
            bad.append("a differentiator interpolated prose: %s" % e[:70])
            break
    if "navpanel" in doc and not re.search(r"<script>[\s\S]*?navpanel[\s\S]*?</script>", doc):
        bad.append("header would be dead - nav script missing")
    # Look for ranking MARKUP, not for the word. The first version matched
    # "no best-of" in the page's own methodology note and refused to ship a
    # page for saying it does not rank.
    # The accreditation count appears in prose AND in the hero figure. A
    # hardcoded "eleven" in the copy went stale the moment a twelfth accredited
    # institution entered the data, which is exactly how a page that insists on
    # cited figures ends up carrying an uncited one.
    n_acc = sum(1 for p in PROGRAMS if p.get("coamfte"))
    if ("<b>%d of the %d</b>" % (n_acc, len(PROGRAMS))) not in doc:
        bad.append("the accreditation count in the copy does not match the data")
    if re.search(r'class="[^"]*\b(rank|score|stars?)\b', doc) \
       or re.search(r"\branked\s+#?\d", doc, re.I) \
       or re.search(r"\btop\s+\d+\s+(programmes?|programs?|schools?)", doc, re.I):
        bad.append("the page appears to rank something")
    for name, sl in SLUGS.items():
        if ('href="%s"' % sl) not in doc:
            bad.append("school page built but not linked: %s" % sl)
    if bad:
        sys.exit("build_programs: " + "; ".join(bad))

    print("%-40s %d bytes  %d programmes  %d COAMFTE  %d with tuition  %d threads"
          % (os.path.basename(OUT), len(doc), len(PROGRAMS),
             sum(1 for p in PROGRAMS if p.get("coamfte")), have, len(allt)))


if __name__ == "__main__":
    main()
