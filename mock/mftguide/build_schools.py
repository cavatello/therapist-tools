#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Build one page per California MFT programme worth a page of its own.

WHY NOT ALL OF THEM. A school gets a page when there is enough verified
substance to fill one: a named degree, units, length, format, an accreditation
status that means something, a published cost, or real discussion about it. The
rest have a name, a city and a URL, and a page built from that is a doorway page
- built to rank rather than to inform - which would dilute every page it sits
beside. They stay in the directory, where a row is exactly the right amount of
space for what is known.

The threshold is scored rather than hand-picked, so it stays honest as the data
improves: three points for real forum discussion, two for COAMFTE, two for
published tuition, one each for degree, units, length, format and a distinctive
feature. Six qualifies. A school that publishes more next year earns a page
without anyone deciding it deserves one. The thirteen institutions the Board
lists that were added in the BBS reconciliation are all below it today, which is
the rule working rather than the rule failing: the Board corroborates that they
are listed and nothing else, and a page cannot be built out of that alone.

WHAT EACH PAGE ANSWERS, in this order:

  1. Will this degree let me practise where I intend to? Accreditation first,
     because it is the only irreversible decision on the page. A non-COAMFTE
     California degree is fine in California and can mean remedial coursework
     or no licence at all elsewhere - and nobody discovers that until they try
     to move.
  2. What is it, concretely? Degree name, units, length, format.
  3. What does it cost? The published figure with its year and a link, or
     "not published" - never an estimate.
  4. What do people actually say? Real threads, sentiment-tagged, in new
     windows, including the unflattering ones.
  5. What should I check before applying? The questions whose answers are not
     on any programme page.

Chrome and the nav script are lifted from the published hub. The script matters:
every page previously built this way shipped with a header that did nothing.
"""
import os, re, sys, json, html, unicodedata

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import forums as F
import depth_render as D
from depth_css import DEPTH_CSS, DEPTH_JS

SRC = os.path.join(HERE, "_chrome.html")
DATA = os.path.join(HERE, "programs.json")
OUTDIR = os.path.join(HERE, "schools")
UPDATED = "6 August 2026"
MIN_SCORE = 6

PROGRAMS = json.load(open(DATA, encoding="utf-8"))


def _load(path, default):
    try:
        return json.load(open(os.path.join(HERE, path), encoding="utf-8"))
    except (IOError, ValueError):
        return default


VIDEOS = _load("videos.json", {})
PHOTOS_EXTRA = _load("photos_extra.json", {})

# Deep research, one file per school, keyed by slug. Absent files are normal -
# every renderer in depth_render degrades to "" - so a school researched later
# starts appearing on its own page the moment its file lands, with no code
# change. See DEPTH_SPEC.md for the schema.
DEPTH = {}
_dd = os.path.join(HERE, "depth")
if os.path.isdir(_dd):
    for _f in sorted(os.listdir(_dd)):
        if _f.endswith(".json"):
            try:
                _rec = json.load(open(os.path.join(_dd, _f), encoding="utf-8"))
            except ValueError:
                sys.exit("build_schools: depth/%s is not valid JSON" % _f)
            DEPTH[_f[:-5]] = _rec
else:
    # The repo carries one combined file rather than thirty-seven, because
    # thirty-seven blobs review badly and move badly. A working copy may
    # explode it back into depth/, and if it has, the directory wins.
    DEPTH = _load("depth_all.json", {})


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

N_ALL = len(PROGRAMS)
N_COAM = sum(1 for _p in PROGRAMS if _p.get("coamfte"))
N_TU = sum(1 for _p in PROGRAMS if _p.get("per_unit") or _p.get("total"))

NP = '<span class="np">not published</span>'
SENT = {"positive": ("pos", "positive"), "negative": ("neg", "critical"),
        "mixed": ("mix", "mixed"), "info": ("inf", "informational")}


def esc(x):
    return html.escape(x) if x else None


def library_meta(p):
    """The ts:* block, emitted by the builder rather than backfilled.

    THIS CLOSES A LOOP THAT WAS STILL OPEN. registry_meta.py writes each page's
    library metadata into the page and registry_sync.py reads it back, so the
    page is the source of truth and nobody has to edit a central file. But
    school pages never emitted their own meta - the existing sixty-five got
    theirs from a registry that had been seeded by hand long before. So the
    first genuinely new school page, Kaiser Permanente, built fine, deployed
    fine, and was invisible to the library: no question index entry, no
    up-link, nothing. Exactly the orphan the handover was built to prevent.

    It was caught only because registry_meta.py NAMES the pages it cannot place
    instead of skipping them quietly. That backstop is the reason this was a
    five-minute fix rather than a page nobody found for a year.

    Everything below is derived from the record, so a school added next year
    joins the library on the next build with no central edit and no hand-written
    metadata.
    """
    q = "What is %s's MFT programme like?" % p["institution"].split(" (")[0]
    bits = []
    if p.get("units"):
        bits.append(esc(p["units"]))
    if p.get("coamfte"):
        # Qualified where a qualifier exists. This line feeds the
        # In-short card, ts:outcome and the hub card - the three
        # places a reader meets the claim before the verdict block
        # that was already fixed.
        bits.append("COAMFTE accredited"
                    + (" (%s)" % p["coamfte_note"]
                       if p.get("coamfte_note") else ""))
    out = ("What it costs, how practicum works, and what people say"
           if not bits else
           "%s — what it costs, how practicum works, and what people say"
           % ", ".join(bits))
    n = esc(p.get("units")) or (esc(p.get("degree")) or "")[:40] or None
    rows = [("topic", "licensure"), ("format", "answer"),
            ("question", esc(q)), ("outcome", out)]
    if n:
        rows.append(("number", n))
    rows += [("weight", "2"), ("leaf", "true")]
    return ("<!-- ts:meta -->\n"
            + "\n".join('<meta name="ts:%s" content="%s">' % (k, v)
                         for k, v in rows)
            + "\n<!-- /ts:meta -->\n")


def slug(name):
    """<full institution name>-mft.html

    The first version stripped "university", "college" and "institute" to keep
    slugs short, then wrapped the result in mft-...-california. It produced
    `mft-california-of-integral-studies-california.html` for the California
    Institute of Integral Studies - the removed word was the one carrying the
    meaning - and `-california-california` for anything already named after the
    state. Both read as machine output, which is the wrong signal on a page
    asking a reader to trust its research.

    Keeping the whole name and suffixing once is longer and unambiguous.
    """
    s = unicodedata.normalize("NFKD", name).encode("ascii", "ignore").decode()
    s = re.sub(r"\(.*?\)", " ", s.lower())          # drop parenthetical asides
    # Strip a LEADING "the" only. Stripping it everywhere turned "University of
    # the Pacific" into `university-of-pacific` and "University of the West"
    # into `university-of-west` - names nobody would type and which do not
    # match the school. The leading article is the only one that adds nothing
    # ("The Wright Institute" -> `wright-institute`), and confining the rule to
    # it leaves every already-published slug unchanged.
    s = re.sub(r"^the\b", " ", s)
    s = re.sub(r"[^a-z0-9]+", "-", s).strip("-")
    s = re.sub(r"-+", "-", s)
    return s[:64].strip("-") + "-mft.html"


def score(r):
    s = 0
    if F.THREADS.get(r["institution"]):
        s += 3
    if r.get("coamfte"):
        s += 2
    if r.get("per_unit") or r.get("total"):
        s += 2
    for k in ("degree", "units", "length", "format", "notable"):
        if r.get(k):
            s += 1
    return s


# A school earns a page if it was actually researched, or if what the directory
# already knows about it clears the threshold. The scored threshold came first
# and was the right rule when the only inputs were directory rows; now that a
# depth record exists for every institution, the presence of that record IS the
# qualification, and the score survives as the fallback for any school added
# later that has not been researched yet.
SELECTED = [r for r in PROGRAMS
            if slug(r["institution"]).replace(".html", "") in DEPTH
            or score(r) >= MIN_SCORE]
SLUGS = {}
for r in sorted(SELECTED, key=lambda x: x["institution"]):
    sl = slug(r["institution"])
    n = 2
    while sl in SLUGS.values():
        sl = sl.replace(".html", "-%d.html" % n)
        n += 1
    SLUGS[r["institution"]] = sl

CSS = """<style>/* school */
.sc{--pine:#2C6350;--amber:#F6C560;--ink:#17271F;--line:#E2DACA;--mut:#7C8878;
  --green:#3F9577;--red:#B5483F}
.scband{background:linear-gradient(135deg,#14261E 0%,#1B4536 48%,#2C6350 100%);
  color:#EFF5F2;padding:30px 0 36px}
.scband .in{max-width:1180px;margin:0 auto;padding:0 26px;display:grid;
  grid-template-columns:minmax(0,1.3fr) minmax(250px,.7fr);gap:34px;align-items:center}
.scband .bcr{display:flex;flex-wrap:wrap;align-items:center;gap:4px 8px;margin:0 0 14px;
  padding:0;list-style:none;font-family:'IBM Plex Mono',ui-monospace,monospace;
  font-size:10.4px;letter-spacing:.1em;text-transform:uppercase}
.scband .bcr li{display:flex;align-items:center;gap:8px}
.scband .bcr a{color:#EFF5F2;opacity:.66;text-decoration:none;padding:5px 0;min-height:26px;
  display:inline-flex;align-items:center;border-bottom:1px solid transparent}
.scband .bcr a:hover{opacity:1;border-bottom-color:currentColor}
.scband .bcr .sep{opacity:.36}
.scband .bcr [aria-current]{opacity:.95;font-weight:600;color:var(--amber)}
.scband h1{font-family:Fraunces,Georgia,serif;font-size:clamp(25px,3.3vw,38px);
  line-height:1.08;font-weight:600;letter-spacing:-.02em;color:#fff;margin:0 0 12px;max-width:20ch}
.scband .sub{font-family:'IBM Plex Mono',monospace;font-size:11px;letter-spacing:.11em;
  text-transform:uppercase;color:var(--amber);margin:0 0 12px}
.scband .dek{font-size:15.2px;line-height:1.72;color:rgba(255,255,255,.87);margin:0;max-width:56ch}
.scmeta{display:flex;gap:14px;flex-wrap:wrap;margin-top:17px;
  font-family:'IBM Plex Mono',monospace;font-size:10.4px;letter-spacing:.06em;
  text-transform:uppercase;color:rgba(255,255,255,.62)}
.scfig{background:rgba(0,0,0,.26);border:1px solid rgba(255,255,255,.18);border-radius:16px;
  padding:20px 22px;min-width:0}
.scfig b{display:block;font-family:Fraunces,Georgia,serif;font-size:clamp(26px,3.4vw,38px);
  line-height:1.05;color:var(--amber);overflow-wrap:anywhere}
.scfig span{display:block;font-size:12.4px;line-height:1.55;color:rgba(255,255,255,.74);margin-top:9px}
.scfig .row{display:flex;justify-content:space-between;gap:10px;padding:8px 0;
  border-top:1px solid rgba(255,255,255,.14);font-size:12.1px;color:rgba(255,255,255,.8)}
.scfig .row:first-of-type{margin-top:16px}
.scfig .row b{display:inline;font-size:12.3px;font-family:inherit;color:#fff;text-align:right}

.scwrap{max-width:1180px;margin:0 auto;padding:32px 26px 20px;display:grid;
  grid-template-columns:206px minmax(0,1fr);gap:38px;align-items:start}
.scnav{position:sticky;top:16px;min-width:0}
.scnav b{display:block;font-family:'IBM Plex Mono',monospace;font-size:10px;
  letter-spacing:.13em;text-transform:uppercase;color:var(--mut);margin-bottom:11px}
.scnav a{display:block;font-size:13px;line-height:1.42;color:#4A5A46;text-decoration:none;
  padding:6px 0 6px 12px;border-left:2px solid var(--line)}
.scnav a:hover{color:var(--ink);border-left-color:#B9AE93}
.scnav a.on{color:var(--pine);border-left-color:var(--pine);font-weight:600}
.scbody{min-width:0}
.scbody h2{font-family:Fraunces,Georgia,serif;font-size:clamp(20px,2.4vw,26px);
  line-height:1.2;font-weight:600;color:var(--ink);margin:42px 0 13px;scroll-margin-top:20px}
.scbody h2:first-child{margin-top:0}
.scbody p{font-size:15.2px;line-height:1.78;color:#3B4A38;margin:0 0 15px;max-width:68ch}
.scbody p b{color:var(--ink)}
.scbody a{color:var(--pine)}

.verd{border-radius:12px;padding:19px 21px;margin:6px 0 16px;border:1px solid}
.verd.ok{background:#F2F8F1;border-color:#CFE3CB;border-left:4px solid var(--green)}
.verd.warn{background:#FBF0E2;border-color:#EBD9BC;border-left:4px solid #C98B4B}
/* A Board-issued Notice to Students, which is a different kind of thing from
   every other block on the page: not something found out about the school, but
   the regulator speaking about it. Red, and above the fold. */
.verd.board{background:#FBF0EF;border-color:#E4B7B2;border-left:4px solid #B5483F}
.verd.board h3{color:#8E3A32}
.verd.board a{color:#8E3A32}
.verd h3{font-family:Fraunces,Georgia,serif;font-size:18.5px;margin:0 0 8px;color:var(--ink)}
.verd p{margin:0 0 10px;font-size:14.5px;max-width:none;color:#3B4A38}
.verd p:last-child{margin-bottom:0}

.tbl{display:grid;gap:0;background:#fff;border:1px solid var(--line);border-radius:11px;
  overflow:hidden;margin:6px 0 8px}
.tbl .r{display:grid;grid-template-columns:150px minmax(0,1fr);gap:14px;padding:13px 16px;
  border-bottom:1px solid #F0EBDE;font-size:14px}
.tbl .r:last-child{border-bottom:0}
.tbl .r span{font-family:'IBM Plex Mono',monospace;font-size:10.2px;letter-spacing:.07em;
  text-transform:uppercase;color:var(--mut);padding-top:3px}
.tbl .r b{font-weight:500;color:#3B4A38;min-width:0;overflow-wrap:anywhere}
.tbl .r b a{color:var(--pine)}
.np{color:#B0A896;font-style:italic}
.yr{font-family:'IBM Plex Mono',monospace;font-size:10px;color:var(--mut)}

.thl{display:grid;gap:9px;margin:8px 0}
.th{display:block;background:#fff;border:1px solid var(--line);border-radius:10px;
  padding:13px 15px;text-decoration:none;min-width:0;border-left:3px solid #CFC7B4}
.th:hover{background:#FBFAF6}
.th.pos{border-left-color:var(--green)}
.th.neg{border-left-color:var(--red)}
.th.mix{border-left-color:#C98B4B}
.th.inf{border-left-color:#8FA3C4}
.tm{display:block;font-family:'IBM Plex Mono',monospace;font-size:9.8px;letter-spacing:.06em;
  text-transform:uppercase;color:var(--mut);margin-bottom:4px}
.th b{display:block;font-size:14px;line-height:1.35;color:var(--ink);font-weight:600;margin-bottom:4px}
.th i{display:block;font-style:normal;font-size:12.6px;line-height:1.5;color:#4A5A46}
.sn{display:inline-block;margin-top:7px;font-family:'IBM Plex Mono',monospace;font-size:9.2px;
  letter-spacing:.08em;text-transform:uppercase;color:var(--mut)}

.ask{display:grid;gap:9px;margin:8px 0}
.q{background:#fff;border:1px solid var(--line);border-radius:10px;padding:14px 16px;min-width:0}
.q b{display:block;font-size:14.4px;color:var(--ink);margin-bottom:5px}
.q p{font-size:13.3px;line-height:1.6;color:#4A5A46;margin:0;max-width:none}

.nxt{display:grid;grid-template-columns:repeat(auto-fit,minmax(240px,1fr));gap:11px;margin:14px 0 6px}
.nx{display:block;background:#fff;border:1px solid var(--line);border-left:3px solid var(--pine);
  border-radius:10px;padding:14px 16px;text-decoration:none;min-width:0}
.nx:hover{background:#FBFAF6}
.nx b{display:block;font-family:Fraunces,Georgia,serif;font-size:15.5px;color:var(--ink);margin-bottom:4px}
.nx span{display:block;font-size:12.8px;line-height:1.5;color:#4A5A46}

@media (max-width:900px){
  .scwrap{grid-template-columns:minmax(0,1fr);gap:20px;padding-top:22px}
  .scnav{position:static;display:flex;gap:7px;overflow-x:auto;padding-bottom:5px}
  .scnav b{display:none}
  .scnav a{border-left:0;border:1px solid var(--line);border-radius:20px;padding:6px 12px;
    white-space:nowrap;font-size:12.3px}
  .scnav a.on{border-color:var(--pine);background:#EAF3DE}
  .scband .in{grid-template-columns:minmax(0,1fr);gap:22px}
}
@media (max-width:560px){
  .tbl .r{grid-template-columns:minmax(0,1fr);gap:5px}
  .scbody p{font-size:14.7px}
}
</style>"""

JS = """<script>
(function(){
  var links=[].slice.call(document.querySelectorAll('.scnav a'));
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

# The same four paragraphs open the practicum section on every page, because
# almost nobody arrives knowing this and the school-specific detail underneath
# is meaningless without it. Two vocabulary notes are deliberate: California
# retired the word "intern" in 2018 - anyone still saying "MFT intern" is
# working from pre-2018 material - and "trainee" and "associate" are two
# different legal statuses with different rules, which is the distinction people
# most often get wrong when they compare programmes.
PRIMER = (
    "<p>Californian clinical training runs in two legally distinct stages, and "
    "the difference decides what a programme can and cannot do for you.</p>"
    "<p><b>A trainee</b> is a student. You see clients while still enrolled, "
    "at a site your programme approves, supervised by someone the site "
    "provides. This is practicum, and it is the stage a programme controls. "
    "<b>An associate</b> &mdash; registered with the Board after you graduate "
    "&mdash; is no longer a student, is usually paid, and is working toward the "
    "3,000 hours the licence requires. The Board renamed this stage from "
    "&ldquo;intern&rdquo; to &ldquo;associate&rdquo; in 2018, so any page still "
    "saying &ldquo;MFT intern&rdquo; is quoting something out of date.</p>"
    "<p>Hours you bank as a trainee count toward the 3,000, up to a limit, "
    "which is why the size and quality of a programme&rsquo;s placement matters "
    "long after graduation: a student who leaves with 1,000 hours starts the "
    "associate years a third of the way through them, and one who leaves with "
    "the 225-hour minimum starts at the beginning.</p>"
    "<p>Practicum is also where a degree most often stops being on schedule. "
    "Coursework runs on a calendar the school controls; placement does not. The "
    "questions that matter are therefore all about <em>who owns the problem of "
    "finding you a site</em> &mdash; and the answer differs enormously between "
    "programmes on this list.</p>"
    '<p><a href="amft-3000-hours-california.html">What happens after the degree '
    "&rarr;</a></p>")

ASK = [
    ("Where do students actually get placed, and who finds the placement?",
     "The single question that separates programmes. Ask for a list of current "
     "sites, and ask plainly whether the programme places you or expects you to "
     "find your own. A rural or online student unable to find a site cannot "
     "graduate."),
    ("How many of your graduates passed the clinical exam last year?",
     "The Board publishes this by school, so the programme cannot be the only "
     "source. Ask anyway, and see whether the answer matches."),
    ("What is the total cost, including fees, in the year I would start?",
     "Per-unit rates move. Multiply by the actual unit count and add campus fees "
     "before comparing anything."),
    ("How many relational hours does a typical student leave with?",
     "The 500 couples-and-families hours are carved out of the 1,750 clinical "
     "ones, and they are the category associates most often finish short on. A "
     "programme placing students in adult individual settings will not generate "
     "them."),
    ("Does this degree also make me eligible for the LPCC?",
     "Sometimes yes, sometimes with extra units, sometimes only in one delivery "
     "format. Get it in writing rather than from a brochure."),
]


def threads(name):
    t = F.THREADS.get(name)
    if not t:
        return None
    return "".join(
        '<a class="th %s" href="%s" target="_blank" rel="noopener noreferrer">'
        '<span class="tm">%s &middot; %s</span><b>%s</b><i>%s</i>'
        '<span class="sn">%s</span></a>'
        % (SENT[s][0], u, f, y, esc(title), esc(note), SENT[s][1])
        for u, f, title, y, s, note in t)


def tuition(p):
    if p.get("total"):
        return "$%s total" % "{:,}".format(int(p["total"]))
    if p.get("per_unit"):
        return "$%s a unit" % "{:,}".format(int(p["per_unit"]))
    return None


def page(p):
    name = p["institution"]
    tu = tuition(p)
    tyear = (' <span class="yr">%s</span>' % esc(str(p["tyear"]))) if p.get("tyear") else ""
    turl = p.get("turl") or p["url"]
    coam = bool(p.get("coamfte"))
    th = threads(name)

    # headline figure: the most decision-relevant thing that is actually known
    if tu:
        fig_b, fig_s = tu, "published tuition%s" % (
            ", %s" % esc(str(p["tyear"])) if p.get("tyear") else "")
    elif p.get("units"):
        fig_b, fig_s = esc(p["units"]), "to complete the degree"
    else:
        fig_b, fig_s = ("COAMFTE" if coam else "BBS-listed"), "accreditation status"

    rows = [("Degree", esc(p.get("degree")) or NP),
            ("Units", esc(p.get("units")) or NP),
            ("Length", esc(p.get("length")) or NP),
            ("Format", esc(p.get("format")) or NP),
            # Three answers, not two-and-a-blank. "No" is the Board's row
            # saying this school is listed for LMFT and not for LPCC, which is
            # a fact about what the degree opens; NP means nobody checked. They
            # used to render identically.
            ("Also LPCC",
             ("Yes" + (" &mdash; " + esc(p["lpcc_note"]) if p.get("lpcc_note") else "")
              if p.get("lpcc") is True else
              "No &mdash; the Board lists this school for LMFT, not LPCC"
              if p.get("lpcc") is False else NP)),
            ("Published tuition",
             ('<a href="%s" target="_blank" rel="noopener noreferrer">%s</a>%s'
              % (turl, tu, tyear)) if tu else NP)]
    table = '<div class="tbl">%s</div>' % "".join(
        '<div class="r"><span>%s</span><b>%s</b></div>' % (k, v) for k, v in rows)

    if coam:
        cnote = p.get("coamfte_note")
        verdict = ('<div class="verd %s"><h3>COAMFTE accredited%s</h3>'
                   % ("warn" if cnote else "ok",
                      (", " + cnote) if cnote else "") +
                   "<p>This is the accreditation that decides whether the degree "
                   "travels. %d of the %d institutions on the Board&rsquo;s list "
                   "hold it, and this is one of them.</p>" % (N_COAM, N_ALL) +
                   "<p>It matters most if there is any chance you will practise "
                   "outside California. It matters less inside California, where a "
                   "regionally-accredited, Board-listed degree is sufficient.</p></div>")
    else:
        verdict = ('<div class="verd warn"><h3>Not COAMFTE accredited</h3>'
                   "<p>That is not a defect &mdash; %d of the %d "
                   "institutions on the Board&rsquo;s list are in the same position, " % (N_ALL - N_COAM, N_ALL) +
                   "including most of the Cal States, and their graduates license in "
                   "California every year.</p>"
                   "<p><b>It becomes a problem if you leave.</b> Several states will "
                   "not accept a non-COAMFTE degree without remedial coursework, and a "
                   "few will not accept it at all. If there is any chance you move, "
                   "check the destination board&rsquo;s rules before you enrol, not "
                   "after.</p></div>")

    cost_body = (
        "<p>The figure below is the institution&rsquo;s own, from its own page, "
        "with the year it applies to. Multiply the per-unit rate by the actual "
        "unit count and add campus fees before comparing it with anything.</p>"
        if tu else
        "<p><b>This programme does not publish a tuition figure</b> anywhere I "
        "could find it. %d of the %d on the Board&rsquo;s list "
        "are the same." % (N_ALL - N_TU, N_ALL) + " That is a fair thing to ask admissions directly, and the "
        "speed and specificity of the answer tells you something on its own.</p>")

    ask = '<div class="ask">%s</div>' % "".join(
        '<div class="q"><b>%s</b><p>%s</p></div>' % (q, a) for q, a in ASK)

    dep = DEPTH.get(SLUGS[name].replace(".html", ""), {})
    vid = VIDEOS.get(name)
    pho = dep.get("photo") or PHOTOS_EXTRA.get(name)

    secs = []

    # A Notice to Students goes above everything, including what the programme
    # is. Nothing else on the page can mean "this degree may not lead to a
    # licence at all", and a reader who stops after the first section must not
    # be one of the readers who misses it.
    if p.get("notice"):
        n = p["notice"]
        secs.append(("board-notice", "Read this first",
                     '<div class="verd board"><h3>%s</h3><p>%s</p>'
                     '<p><a href="%s" target="_blank" rel="noopener noreferrer">'
                     "The Board&rsquo;s notice, in full (PDF, %s) &rarr;</a></p>"
                     "</div>" % (esc(n["title"]), esc(n["body"]), n["url"],
                                 esc(n.get("as_of") or ""))))

    char = D.character(dep.get("character"), dep.get("orientation"))
    if char:
        secs.append(("overview", "What this programme actually is", char +
                     '<p><a href="%s" target="_blank" rel="noopener noreferrer">'
                     "The programme&rsquo;s own page &rarr;</a></p>" % p["url"]))

    med = D.media(vid, pho, name)
    if med:
        secs.append(("media", "See it and hear it", med))

    crs = D.courses(dep.get("signature"))
    if crs:
        secs.append(("courses", "The courses that define it",
                     "<p>Every California programme teaches law and ethics, "
                     "assessment and a survey of theories. These are the courses "
                     "that are <em>not</em> on every list &mdash; the ones that "
                     "tell you what this particular faculty believes therapy is. "
                     "The quoted text is the catalog&rsquo;s own; the note "
                     "underneath each one is mine.</p>" + crs))

    cur = D.curriculum(dep.get("curriculum"))
    if cur:
        secs.append(("curriculum", "The whole degree, term by term",
                     "<p>What you would actually take, in the order you would "
                     "take it. Sequences change; check the current catalog before "
                     "you count on any single term.</p>" + cur))

    secs.append(("practicum", "How practicum actually works", PRIMER +
                 (D.practicum(dep.get("practicum")) or
                  "<p><b>This programme&rsquo;s placement model could not be "
                  "established from public sources.</b> That is the first "
                  "question to ask admissions, and the specificity of the answer "
                  "tells you a great deal.</p>")))

    secs += [("accreditation", "Will this degree travel", verdict +
             '<p><a href="become-an-mft-california.html">What the Board requires of '
             "any qualifying degree &rarr;</a></p>"),
            ("the-programme", "What it is, on paper", table +
             ('<p>%s</p>' % esc(p["notable"]) if p.get("notable") else
              ('<p>%s</p>' % esc(p["note"]) if p.get("note") else "")) +
             '<p><a href="%s" target="_blank" rel="noopener noreferrer">'
             "The programme&rsquo;s own page &rarr;</a></p>" % p["url"]),
            ("cost", "What it costs", cost_body +
             (table if False else "") +
             ('<p style="font-size:15.2px"><b>%s</b>%s &mdash; '
              '<a href="%s" target="_blank" rel="noopener noreferrer">source</a></p>'
              % (tu, tyear, turl) if tu else "") +
             '<p><a href="therapist-cost-of-living-california.html">What a month '
             "costs to live on while you study &rarr;</a></p>")]

    adm = D.admissions(dep.get("admissions"))
    if adm:
        secs.append(("getting-in", "Getting in", adm))

    # After admissions and before what people say. It is about what happened to
    # people who already went here, so it belongs after "how you get in" and
    # before opinion - and putting it any higher would give it a prominence the
    # caveat spends three paragraphs arguing against.
    ex = D.exam(dep.get("exam"))
    if ex:
        secs.append(("exam-results", "How its graduates did on the Board&rsquo;s exam", ex))

    oc = D.outcomes(dep.get("outcomes"))
    if oc:
        secs.append(("outcomes",
                     "What the accreditor makes it publish", oc))

    vox = D.voices(dep.get("voices"))
    if vox or th:
        secs.append(("what-people-say", "What people say about it",
                     "<p>Quoted where the wording carries the meaning, linked in "
                     "every case, opening in a new window. The tags are my reading "
                     "of each source, not a measurement, and the unflattering ones "
                     "are here too.</p>" + vox +
                     ('<div class="thl">%s</div>' % th if th else "")))
    else:
        secs.append(("what-people-say", "What people say about it",
                     "<p><b>Nothing credible was found.</b> Searched by every name "
                     "variant across Reddit, Student Doctor Network and The GradCafe. "
                     "Silence is not a verdict &mdash; small programmes generate "
                     "little discussion &mdash; but a missing section should not read "
                     "as an endorsement, so it says so.</p>"
                     '<p><a href="mft-programs-california.html#general">Threads about '
                     "the decision itself, rather than about one school &rarr;</a></p>"))
    secs.append(("before-you-apply", "What to ask before you apply",
                 "<p>None of these are answered on a programme page, and all five "
                 "change what the degree is actually worth to you.</p>" + ask +
                 '<div class="nxt">'
                 '<a class="nx" href="mft-programs-california.html"><b>All {{NALL}} programmes'
                 "</b><span>Filter by accreditation, region and whether tuition is "
                 "published</span></a>"
                 '<a class="nx" href="become-an-mft-california.html"><b>The licensure route'
                 "</b><span>Every requirement, with the code section it comes from</span></a>"
                 '<a class="nx" href="amft-3000-hours-california.html"><b>The 3,000 hours'
                 "</b><span>What happens after the degree, and how long it takes</span></a>"
                 "</div>"))

    gp = D.gaps(dep.get("gaps"), dep.get("sources"))
    if gp:
        secs.append(("what-i-could-not-find", "What I could not establish", gp))

    nav = '<nav class="scnav"><b>On this page</b>%s</nav>' % "".join(
        '<a href="#%s">%s</a>' % (i, t) for i, t, _b in secs)
    body = "".join('<h2 id="%s">%s</h2>%s' % (i, t, b) for i, t, b in secs)

    fig = ('<div class="scfig"><b>%s</b><span>%s</span>'
           '<div class="row"><span>COAMFTE</span><b>%s</b></div>'
           '<div class="row"><span>Format</span><b>%s</b></div>'
           '<div class="row"><span>Discussion found</span><b>%s</b></div></div>'
           % (fig_b, fig_s, "yes" if coam else "no",
              esc((p.get("format") or "not published"))[:34],
              ("%d threads" % len(F.THREADS[name])) if th else "none"))

    dek = ("%s, in %s. What the programme publishes about itself, what its "
           "accreditation means for where you can practise, and what students and "
           "graduates say in public." % (esc(p.get("degree")) or "An MFT-qualifying degree",
                                         esc(p.get("city")) or "California"))

    return """<!doctype html>
<html lang="en"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>%s — MFT programme in California: accreditation, cost and what people say</title>
<meta name="description" content="%s — degree, units, length, format, COAMFTE status and published tuition, plus real discussion from students and graduates. Part of a directory of {{NALL}} California MFT programmes.">
<link rel="canonical" href="https://therapistsupport.org/%s">
%s
%s
%s
%s
</head><body class="sc">
%s
<main>
<section class="scband"><div class="in"><div>
<ol class="bcr" aria-label="Breadcrumb">
<li><a href="index.html">Therapist Support</a><span class="sep">&rsaquo;</span></li>
<li><a href="mft-programs-california.html">MFT programmes</a><span class="sep">&rsaquo;</span></li>
<li><span aria-current="page">%s</span></li></ol>
<p class="sub">%s</p>
<h1>%s</h1>
<p class="dek">%s</p>
<div class="scmeta"><span>California</span><span>Updated %s</span><span>%s</span></div>
</div>%s</div></section>
<div class="scwrap">%s<article class="scbody">%s</article></div>
</main>
%s
%s
%s
</body></html>""" % (esc(name), esc(name), SLUGS[name],
                     # The ts:meta block, immediately after the canonical link -
                     # the same anchor registry_meta.py uses, so the two cannot
                     # end up writing to different places in the head.
                     library_meta(p),
                     "\n".join(links), "\n".join(styles), CSS + DEPTH_CSS, header,
                     esc(name), esc(p.get("city")) or "California", esc(name), dek,
                     UPDATED, "COAMFTE accredited" if coam else "BBS-listed",
                     fig, nav, body, footer, navscript, JS + DEPTH_JS)


def main():
    os.makedirs(OUTDIR, exist_ok=True)
    written = []
    for p in sorted(SELECTED, key=lambda x: x["institution"]):
        # {{NALL}} rather than a %d in the template: the template is one
        # `%`-formatted string with nineteen positional arguments, and adding a
        # twentieth in the right slot to print a number that never varies
        # within a run is exactly the off-by-one edit that has broken this
        # project's pages before. A token and a replace cannot miscount.
        doc = page(p).replace("{{NALL}}", str(N_ALL))
        path = os.path.join(OUTDIR, SLUGS[p["institution"]])
        open(path, "w", encoding="utf-8").write(doc)
        written.append((SLUGS[p["institution"]], p["institution"], len(doc)))

    # ---- sweep the output directory
    # A builder that only ever writes leaves its own mistakes lying around. The
    # slug rule was corrected once - it had been stripping "the" everywhere, so
    # the University of the Pacific came out as `university-of-pacific` - and
    # the three files from before the fix sat in this directory for days,
    # invisible because nothing linked to them and every guard here iterates
    # over what was WRITTEN rather than over what is PRESENT. They were one
    # `cp schools/*.html` from being published as duplicates of three real
    # pages. Sweep what this run did not write.
    keep = set(SLUGS.values())
    swept = []
    for f in sorted(os.listdir(OUTDIR)):
        if f.endswith(".html") and f not in keep:
            os.remove(os.path.join(OUTDIR, f))
            swept.append(f)
    if swept:
        print("   swept %d stale page(s): %s" % (len(swept), ", ".join(swept)))

    # ---- guards
    bad = []
    if len(set(SLUGS.values())) != len(SLUGS):
        bad.append("duplicate slugs")
    for sl, name, _n in written:
        doc = open(os.path.join(OUTDIR, sl), encoding="utf-8").read()
        if doc.count("<h1") != 1:
            bad.append("%s: %d h1" % (sl, doc.count("<h1")))
        if 'rel="canonical" href="https://therapistsupport.org/%s"' % sl not in doc:
            bad.append("%s: canonical does not match its own filename" % sl)
        if not re.search(r"<script>[\s\S]*?navpanel[\s\S]*?</script>", doc):
            bad.append("%s: dead header" % sl)
        # no page may invent a cost
        p = next(x for x in PROGRAMS if x["institution"] == name)
        if not tuition(p) and "does not publish a tuition figure" not in doc:
            bad.append("%s: no tuition and no statement saying so" % sl)
        # A Board notice in the data that is not on the page is the worst
        # single failure this builder can have: the page looks complete and
        # omits the one thing that decides whether the degree leads anywhere.
        # Every page must carry its own library metadata. Without it the page
        # is built, deployed, indexed by nobody and reachable from no list on
        # the site - which is precisely what happened to the first new school
        # page after the ts:meta handover, because this builder never emitted a
        # block and the existing pages had theirs backfilled from a registry
        # seeded by hand.
        if "<!-- ts:meta -->" not in doc or 'name="ts:topic"' not in doc:
            bad.append("%s: no library metadata - it would be an orphan" % sl)
        if p.get("coamfte_note") and "show cause" not in doc:
            bad.append("%s: the coamfte_note did not render" % sl)
        if p.get("notice") and p["notice"]["url"] not in doc:
            bad.append("%s: the Board notice did not render" % sl)
        if tuition(p) and tuition(p) not in doc:
            bad.append("%s: published tuition missing from the page" % sl)
        # every forum link must open safely
        for m in re.finditer(r'<a class="th [^"]*" href="[^"]+"([^>]*)>', doc):
            if 'target="_blank"' not in m.group(1) or "noopener" not in m.group(1):
                bad.append("%s: forum link not opening safely" % sl)
                break
        # the school must link back into the directory and the guide
        for must in ("mft-programs-california.html", "become-an-mft-california.html"):
            if must not in doc:
                bad.append("%s: no link back to %s" % (sl, must))
        # ---- depth-section guards
        dep = DEPTH.get(sl.replace(".html", ""), {})
        # practicum is the section people come for and it is unconditional
        if 'id="practicum"' not in doc:
            bad.append("%s: no practicum section" % sl)
        # the nav has to name every section and no others, or the scroll-spy
        # silently highlights nothing
        ids = re.findall(r'<h2 id="([^"]+)"', doc)
        navs = re.findall(r'<nav class="scnav">.*?</nav>', doc, re.S)
        if not navs or [m for m in re.findall(r'href="#([^"]+)"', navs[0])] != ids:
            bad.append("%s: nav does not match its sections" % sl)
        # no third-party player may load on page view - only the facade
        if re.search(r"<iframe[^>]*youtube", doc):
            bad.append("%s: a YouTube iframe ships in the HTML" % sl)
        for vid in re.findall(r'data-yt="([^"]*)"', doc):
            if not D.YT_RE.match(vid):
                bad.append("%s: malformed video id %r" % (sl, vid))
        # an image we did not verify the licence of must never be published
        if dep.get("photo") or PHOTOS_EXTRA.get(name):
            ph = dep.get("photo") or PHOTOS_EXTRA.get(name)
            if not (ph.get("license") and ph.get("credit") and ph.get("page")):
                bad.append("%s: photo without licence, credit or source page" % sl)
            elif esc(ph["license"]) not in doc or esc(ph["credit"]) not in doc:
                bad.append("%s: photo credit not rendered" % sl)
        # a quotation presented as the catalog's own words needs the catalog
        for c in (dep.get("signature") or []):
            if c.get("verbatim") and not c.get("src"):
                bad.append("%s: verbatim quote with no source (%s)"
                           % (sl, c.get("code") or c.get("title")))
        # research that came back but did not reach the page is a wiring bug,
        # and it is silent - the page still looks finished
        for key, marker in (("character", 'id="overview"'),
                            ("signature", 'id="courses"'),
                            ("voices", 'id="what-people-say"'),
                            ("gaps", 'id="what-i-could-not-find"')):
            if dep.get(key) and marker not in doc:
                bad.append("%s: %s researched but not rendered" % (sl, key))
        if ((dep.get("curriculum") or {}).get("terms")
                and 'id="curriculum"' not in doc):
            bad.append("%s: curriculum researched but not rendered" % sl)
    if bad:
        sys.exit("build_schools: " + "; ".join(bad[:6]))

    json.dump(SLUGS, open(os.path.join(HERE, "school_slugs.json"), "w"), indent=1)
    tot = sum(n for _s, _i, n in written)
    print("%d school pages · %d skipped as too thin · %.1f MB total"
          % (len(written), len(PROGRAMS) - len(written), tot / 1e6))
    print("   with threads: %d   COAMFTE: %d   with tuition: %d"
          % (sum(1 for _s, i, _n in written if F.THREADS.get(i)),
             sum(1 for p in SELECTED if p.get("coamfte")),
             sum(1 for p in SELECTED if tuition(p))))
    dv = [DEPTH.get(s.replace(".html", ""), {}) for s, _i, _n in written]
    print("   depth: %d/%d  courses: %d  terms: %d  voices: %d  video: %d  photo: %d"
          % (sum(1 for d in dv if d), len(written),
             sum(len(d.get("signature") or []) for d in dv),
             sum(len((d.get("curriculum") or {}).get("terms") or []) for d in dv),
             sum(len(d.get("voices") or []) for d in dv),
             sum(1 for _s, i, _n in written if VIDEOS.get(i)),
             sum(1 for k, (_s, i, _n) in enumerate(written)
                 if dv[k].get("photo") or PHOTOS_EXTRA.get(i))))


if __name__ == "__main__":
    main()
