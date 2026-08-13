#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Build psyd-programs-california.html — the California PsyD directory.

WHY THIS IS ITS OWN PAGE AND NOT A TAB ON THE MFT DIRECTORY

They are different licences, different boards, different statutes and a
different accreditation regime. An MFT applicant is reading the BBS's list; a
psychologist applicant is reading the Board of Psychology's rule and APA's. The
one thing the two audiences share is the word "programme", and organising a page
around a shared word rather than a shared decision is how directories become
useless.

THE SPINE OF THIS PAGE IS ACCREDITATION, NOT COST

Because the single most consequential fact about a California PsyD is one that
almost nobody states plainly:

  The California Board of Psychology does NOT require APA accreditation.
  B&P § 2914(b)(2)(A) requires only that the degree come from an institution
  accredited by a REGIONAL accrediting agency — WSCUC, here. That is
  INSTITUTIONAL accreditation.

  But 16 CCR § 1387 requires the supervised professional experience to be at an
  internship that is APA-accredited, or an APPIC or CAPIC member. And
  APA-accredited internships overwhelmingly take applicants from APA-accredited
  doctoral programmes.

So a non-APA PsyD can license you in California — the Board's own 2025 figures
show it happening every year — and can still make the internship year hard, and
can make moving states or working for the VA very hard indeed. That is the
distinction the aggregator sites blur, and it is why this page is grouped by
accreditation status and says what each status actually costs you.

Run:  python3 _dev/build_psyd.py
Then the usual pipeline: restyle -> extract_css -> css_cdo_fix -> the rest.
"""
import os, re, sys, html

HERE = os.path.dirname(os.path.abspath(__file__))
SITE = os.path.dirname(HERE)
sys.path.insert(0, HERE)

from psyd_data import PROGRAMS, GONE, DEAD_END          # noqa: E402

OUT = os.path.join(SITE, "psyd-programs-california.html")
# The chrome is lifted from an ARTICLE page, not from the MFT directory.
# extract_css.py links each page only to the blocks that page actually had, so
# borrowing the directory's stylesheet set gave a page whose markup is
# .art/.artband/.artwrap but whose CSS knows nothing about any of them: the
# hero lost its dark band, .artmeta printed as running text and the breadcrumb
# rendered as a numbered list. Copy the chrome from something built the same
# way as what you are building.
CHROME_FROM = os.path.join(SITE, "hiring-first-associate-california-therapist.html")
CHECKED = "8 August 2026"


def esc(x):
    return html.escape(str(x), quote=False) if x is not None else ""


def money(n):
    return "$" + "{:,}".format(int(n))


TIERS = [
    ("full", "APA-accredited",
     "The default expectation. An APA-accredited doctorate is what "
     "APA-accredited internships, the VA, most hospital posts and most other "
     "states' boards are looking for."),
    ("contingency", "APA-accredited, on contingency",
     "Real accreditation, not a provisional half-measure — a degree finished "
     "while a program holds this status counts as completed at an accredited "
     "program. It is the status APA grants a program too new to have graduated "
     "anyone, because there are no outcomes yet to judge. The program must "
     "apply for full accreditation within three years. The risk to weigh is "
     "small but not zero: ask the program how conversion is tracking."),
    ("inactive", "APA-accredited, inactive",
     "A teach-out. Accreditation is held open so students already enrolled "
     "graduate from an accredited program, but the program is not admitting "
     "anyone. Not an option if you are applying."),
    ("none", "Not APA-accredited",
     "These are regionally accredited institutions, so the degree can satisfy "
     "the California Board of Psychology. What it does not do is clear the "
     "internship, portability and employment hurdles above. Read the section "
     "on what accreditation decides before you rule one in or out."),
]

CSS = """<style>/* _dev/build_psyd.py */
.pdintro{font-size:15.4px;line-height:1.65;color:#3A3529;max-width:66ch}
.pdkey{border:2px solid #16211B;border-radius:12px;box-shadow:4px 4px 0 #F6C560;
  background:#fff;padding:16px 18px;margin:22px 0 0}
.pdkey h2{font-family:'Bricolage Grotesque','Archivo',Inter,system-ui,sans-serif;
  font-weight:800;letter-spacing:-.03em;font-size:20px;color:#16211B;margin:0 0 10px}
.pdkey p{margin:0 0 10px;font-size:14.4px;line-height:1.62;color:#3A3529;max-width:66ch}
.pdkey p:last-child{margin-bottom:0}
.pdkey b{font-weight:600}
.pdcite{font-family:'IBM Plex Mono',ui-monospace,monospace;font-size:11.6px;
  letter-spacing:.02em;color:#2C6350}
.pdtier{margin:38px 0 0}
.pdth{display:flex;flex-wrap:wrap;align-items:baseline;gap:10px 14px;margin:0 0 6px}
.pdth h2{font-family:'Bricolage Grotesque','Archivo',Inter,system-ui,sans-serif;
  font-weight:800;letter-spacing:-.032em;font-size:23px;color:#16211B;margin:0}
.pdn{font-family:'IBM Plex Mono',ui-monospace,monospace;font-size:10.4px;
  font-weight:700;letter-spacing:.09em;text-transform:uppercase;color:#16211B;
  border:2px solid #16211B;border-radius:999px;padding:4px 11px 3px;
  box-shadow:2px 2px 0 #16211B}
.pdn.full{background:#CFE3D6}.pdn.contingency{background:#F6C560}
.pdn.inactive{background:#F0EADA}.pdn.none{background:#fff;color:#B5483F}
.pdwhat{font-size:13.6px;line-height:1.6;color:#5A5647;margin:0 0 16px;max-width:70ch}
.pdgrid{display:grid;grid-template-columns:repeat(auto-fit,minmax(320px,1fr));gap:13px}
.pdc{border:2px solid #16211B;border-radius:12px;box-shadow:3px 3px 0 #16211B;
  background:#FBF9F3;padding:15px 17px}
.pdc h3{font-family:'Bricolage Grotesque','Archivo',Inter,system-ui,sans-serif;
  font-weight:800;letter-spacing:-.028em;font-size:16.5px;line-height:1.25;
  color:#16211B;margin:0 0 3px}
.pdc .pdcity{font-family:'IBM Plex Mono',ui-monospace,monospace;font-size:10px;
  letter-spacing:.1em;text-transform:uppercase;color:#6C6555;display:block;margin:0 0 10px}
.pdr{display:grid;grid-template-columns:104px minmax(0,1fr);gap:4px 12px;
  padding:7px 0;border-top:1px dashed #E4DCC8;font-size:13.2px;line-height:1.5}
.pdr:first-of-type{border-top:none}
.pdr span{font-family:'IBM Plex Mono',ui-monospace,monospace;font-size:9.6px;
  letter-spacing:.09em;text-transform:uppercase;color:#6C6555;padding-top:2px}
.pdr b{font-weight:500;color:#16211B}
/* 3.04:1 at #9A8F76. "Not published" is a real answer on this site, so it has
   to be readable, not just present. */
.pdr b .np{color:#6C6555;font-style:italic;font-weight:400}
/* Pine on cream measured 3.63:1 at this size - under the 4.5:1 floor. Darkened
   until it passed rather than left because it looked fine. */
.pdfig{font-family:Fraunces,Georgia,serif;font-weight:600;font-size:17px;
  color:#1F4A3B;letter-spacing:-.01em}
.pdyr{font-family:'IBM Plex Mono',ui-monospace,monospace;font-size:9.6px;
  letter-spacing:.08em;color:#6C6555;margin-left:5px}
.pdnote{margin:11px 0 0;padding:10px 0 0;border-top:2px dashed #D9D0BA;
  font-size:13.2px;line-height:1.6;color:#4A463A}
.pdgo{display:inline-block;margin:10px 0 0;font-family:'IBM Plex Mono',
  ui-monospace,monospace;font-size:10px;font-weight:700;letter-spacing:.07em;
  text-transform:uppercase;color:#2C6350;text-decoration:none}
.pdgo:hover{text-decoration:underline}
.pdgone{border:2px solid #16211B;border-radius:12px;background:#F4F0E6;
  box-shadow:2px 2px 0 #16211B;padding:14px 16px;margin:0 0 11px}
.pdgone b{display:block;font-family:'Bricolage Grotesque','Archivo',Inter,
  system-ui,sans-serif;font-weight:800;letter-spacing:-.026em;font-size:15.5px;
  color:#16211B}
.pdgone i{display:block;font-style:normal;font-family:'IBM Plex Mono',
  ui-monospace,monospace;font-size:9.6px;letter-spacing:.1em;
  text-transform:uppercase;color:#6C6555;margin:2px 0 7px}
.pdgone p{margin:0;font-size:13.4px;line-height:1.6;color:#4A463A;max-width:74ch}
.pdwarn{border:2px solid #B5483F;border-radius:12px;background:#FDF4F2;
  box-shadow:3px 3px 0 #B5483F;padding:16px 18px;margin:16px 0 0}
.pdwarn h3{font-family:'Bricolage Grotesque','Archivo',Inter,system-ui,sans-serif;
  font-weight:800;letter-spacing:-.028em;font-size:17px;color:#8E3A33;margin:0 0 8px}
.pdwarn p,.pdwarn li{font-size:13.6px;line-height:1.62;color:#5A3B37;max-width:70ch}
.pdwarn ul{margin:9px 0 0;padding-left:20px}
.pdwarn li{margin:0 0 5px}
@media (max-width:600px){
  .pdr{grid-template-columns:minmax(0,1fr);gap:2px}
  .pdth h2{font-size:20px}
}
</style>"""


def card(p):
    rows = []

    def row(k, v):
        rows.append('<div class="pdr"><span>%s</span><b>%s</b></div>' % (k, v))

    row("Degree", esc(p["degree"]))
    row("Units", esc(p["units"]) or '<span class="np">not published</span>')
    row("Length", esc(p["length"]))
    row("Format", esc(p["fmt"]))

    if p.get("total"):
        fig = ('<span class="pdfig">%s</span> total' % money(p["total"]))
    elif p.get("per_unit"):
        fig = ('<span class="pdfig">%s</span> a unit' % money(p["per_unit"]))
    else:
        fig = '<span class="np">not published as a single figure</span>'
    if p.get("tyear") and (p.get("total") or p.get("per_unit")):
        fig += '<span class="pdyr">%s</span>' % esc(p["tyear"])
    if p.get("turl"):
        fig = ('<a href="%s" target="_blank" rel="noopener noreferrer">%s</a>'
               % (esc(p["turl"]), fig))
    row("Tuition", fig)

    if p["apa"] in ("full", "contingency", "inactive"):
        a = "APA-accredited since %s" % esc(p["apa_since"])
        if p.get("apa_next"):
            a += ", next review %s" % esc(p["apa_next"])
        row("Accreditation", a)
    else:
        row("Accreditation", "Not APA-accredited. The institution is "
                             "regionally accredited (WSCUC).")

    note = ('<p class="pdnote">%s</p>' % esc(p["note"])) if p.get("note") else ""
    go = ('<a class="pdgo" href="%s" target="_blank" rel="noopener noreferrer">'
          "The program&rsquo;s own page &nearr;</a>" % esc(p["url"]))
    # The site's OWN page for this school first (user, 13 Aug 2026):
    # readers stay inside the site; the external program page is secondary.
    ours = _school_page(p["inst"])
    if ours:
        go = ('<a class="pdgo" href="%s">Our page on this school &rarr;</a> '
              % ours) + go
    return ('<article class="pdc"><h3>%s</h3><span class="pdcity">%s</span>'
            "%s%s%s</article>"
            % (esc(p["inst"]), esc(p["city"]), "".join(rows), note, go))


def _school_page(inst, _cache={}):
    """Map an institution name to its existing on-site school page, if any."""
    if not _cache:
        import re as _re
        for f in os.listdir(SITE):
            if f.endswith("-mft.html"):
                _cache[_re.sub(r"[^a-z]", "", f[:-9].lower())] = f
        _cache["_"] = True
    import re as _re
    base = _re.sub(r"[^a-z]", "",
                   _re.sub(r"^The\s+|\(.*?\)|,.*$", "", inst).lower())
    for key, f in _cache.items():
        if key == "_":
            continue
        if key.startswith(base[:16]) or base.startswith(key[:16]):
            return f
    return None


def body():
    n_apa = sum(1 for p in PROGRAMS if p["apa"] in ("full", "contingency"))
    n_all = len(PROGRAMS)
    n_open = sum(1 for p in PROGRAMS if p["apa"] != "inactive")
    pub = [p for p in PROGRAMS if p.get("total") or p.get("per_unit")]

    out = ['<article class="art"><section class="artband"><div class="in"><div>']
    out.append('<ol class="bcr" aria-label="Breadcrumb">'
               '<li><a href="index.html">Therapist Support</a>'
               '<span class="sep">&rsaquo;</span></li>'
               '<li><a href="training/">Training</a>'
               '<span class="sep">&rsaquo;</span></li>'
               '<li><span aria-current="page">PsyD programs</span></li></ol>')
    out.append("<h1>California PsyD programs, and the one thing that decides "
               "<em>what the degree is worth</em>.</h1>")
    out.append('<p class="dek">%d doctorates in psychology based in California, '
               "grouped by accreditation &mdash; because California will license "
               "you without APA accreditation, and the internship year very "
               "largely will not.</p>" % n_all)
    out.append('<div class="artmeta"><span>Training</span>'
               "<span>%d APA-accredited</span></div>" % n_apa)
    out.append("</div></div></section>")

    out.append('<div class="artwrap"><div class="artbody">')

    # ---- the thing that actually decides it
    out.append(
        '<div class="pdkey"><h2>California does not require APA accreditation. '
        "Your internship does.</h2>"
        "<p>Every list of PsyD programs sorts on accreditation and none of them "
        "explains what it decides, so here it is in full.</p>"
        "<p><b>For the licence itself, the Board of Psychology asks about the "
        "institution, not the program.</b> Business and Professions Code "
        "&sect;&nbsp;2914(b)(2)(A) requires a doctorate from &ldquo;a college or "
        "institution of higher education that is accredited by a regional "
        "accrediting agency recognized by the United States Department of "
        "Education.&rdquo; In California that means WSCUC. The word "
        "&ldquo;APA&rdquo; does not appear in the statute, and it does not "
        "appear in the implementing regulation, 16&nbsp;CCR &sect;&nbsp;1386, "
        "either. This is not theoretical: the Board&rsquo;s own 2025 figures "
        "show new California psychologists licensed from non-APA programs every "
        "year.</p>"
        "<p><b>For the supervised experience, the rule is programmatic.</b> "
        "16&nbsp;CCR &sect;&nbsp;1387 requires the internship or postdoc to be "
        "APA-accredited, or a member of APPIC or CAPIC. APA-accredited "
        "internship sites overwhelmingly take applicants from APA-accredited "
        "doctoral programs, so a non-APA doctorate narrows that funnel sharply "
        "and pushes candidates toward CAPIC placements.</p>"
        "<p><b>And for everything after,</b> the constraint is geographic and "
        "occupational rather than legal. Many other state boards, the ASPPB "
        "Certificate of Professional Qualification, the VA and most federal "
        "psychologist posts, and a lot of hospital and academic medical centre "
        "jobs presume an APA-accredited doctorate <em>and</em> internship. A "
        "degree that works in California and nowhere else is a career "
        "geography decision, taken years early.</p>"
        '<p class="pdcite">B&amp;P &sect; 2914(b) &middot; 16 CCR &sect; 1386 '
        "&middot; 16 CCR &sect; 1387 &middot; verified against the Board&rsquo;s "
        "published law and regulations, %s</p></div>" % CHECKED)

    out.append('<p class="pdintro" style="margin-top:26px">Every figure below is '
               "the institution&rsquo;s own, with the year it applies to and a "
               "link to the page it came from. %d of the %d publish a tuition "
               "figure; the rest say nothing and this page says so rather than "
               "estimating. Accreditation status is APA&rsquo;s own, read from "
               "its quarterly Notices of Actions rather than from a school&rsquo;s "
               "description of itself &mdash; which matters, because at least one "
               "school&rsquo;s site is a year out of date about its own "
               "status.</p>" % (len(pub), n_all))

    # ---- tiers
    for key, title, what in TIERS:
        rows = [p for p in PROGRAMS if p["apa"] == key]
        if not rows:
            continue
        rows.sort(key=lambda p: p["inst"])
        out.append('<section class="pdtier"><div class="pdth"><h2>%s</h2>'
                   '<span class="pdn %s">%d</span></div>'
                   '<p class="pdwhat">%s</p><div class="pdgrid">%s</div>'
                   "</section>"
                   % (esc(title), key, len(rows), esc(what),
                      "".join(card(p) for p in rows)))

    # ---- gone
    out.append('<section class="pdtier"><div class="pdth">'
               "<h2>Closed, moved, or no longer offered</h2>"
               '<span class="pdn inactive">%d</span></div>'
               '<p class="pdwhat">These still turn up on directory sites, which '
               "is the reason to list them. A program you cannot apply to is not "
               "an option, and one that was never accredited does not become "
               "accredited by being listed next to ones that are.</p>%s</section>"
               % (len(GONE), "".join(
                   '<div class="pdgone"><b>%s</b><i>%s</i><p>%s</p></div>'
                   % (esc(a), esc(b), esc(c)) for a, b, c in GONE)))

    # ---- dead end
    items = "".join("<li><b>%s</b>%s%s</li>"
                    % (esc(a), " &mdash; " + esc(b) if b else "",
                       " " + esc(c) if c else "")
                    for a, b, c in DEAD_END)
    out.append(
        '<div class="pdwarn"><h3>Four schools whose PsyD no longer qualifies '
        "anyone for a California licence</h3>"
        "<p>These are approved by the Bureau for Private Postsecondary "
        "Education but are <b>not regionally accredited</b>, and "
        "&sect;&nbsp;2914(b)(2)(A) requires regional accreditation. The pathway "
        "that used to accept them, &sect;&nbsp;2914(b)(4), expired on "
        "1&nbsp;January&nbsp;2020, and the Board&rsquo;s own list of them is now "
        "headed <em>&ldquo;Previous Approved Schools Accepted Prior to "
        "2020.&rdquo;</em> There is a narrow grandfather clause at "
        "&sect;&nbsp;2914(b)(2)(B) for students who were already enrolled on "
        "31&nbsp;December&nbsp;2016.</p><ul>%s</ul>"
        "<p>If you are looking at one of these, ask the Board directly before "
        "you pay anything. &sect;&nbsp;2914(b)(3): &ldquo;The board shall make "
        "the final determination as to whether a degree meets the requirements "
        "of this subdivision.&rdquo;</p></div>" % items)

    # ---- what this page is not
    out.append(
        '<section class="pdtier"><div class="pdth"><h2>How this page was '
        "built</h2></div>"
        '<p class="pdwhat"><b>Nothing is ranked.</b> There is no score and no '
        "best-of. Accreditation is a fact and it is used as a grouping, not as a "
        "verdict.<br><b>No tuition figure is estimated.</b> Where a school "
        "publishes a per-unit rate but no total, this page shows the per-unit "
        "rate &mdash; multiplying it out and presenting the answer as the "
        "school&rsquo;s would be inventing a number.<br><b>Accreditation status "
        "comes from APA, not from the schools.</b> Read from APA&rsquo;s "
        "quarterly Notices of Actions. California Baptist&rsquo;s own site still "
        "described its program as on contingency after APA had moved it to full "
        "accreditation, which is exactly why.<br><b>MFT and LPCC are a different "
        "route entirely</b> &mdash; different board, different statute, "
        "master&rsquo;s level. Those are on the "
        '<a href="mft-programs-california.html">MFT programs page</a>.</p>'
        "</section>")

    out.append("</div></div></article>")
    return "".join(out)


def main():
    chrome = open(CHROME_FROM, encoding="utf-8").read()

    head_end = chrome.index("</head>")
    head = chrome[:head_end]
    # strip the donor page's own title/description/canonical/JSON-LD
    head = re.sub(r"<title>[\s\S]*?</title>", "", head)
    head = re.sub(r'<meta name="description"[^>]*>', "", head)
    head = re.sub(r'<meta property="og:[^>]*>', "", head)
    head = re.sub(r'<link rel="canonical"[^>]*>', "", head)
    head = re.sub(r'<meta name="ts:[^>]*>', "", head)
    head = re.sub(r'<script type="application/ld\+json">[\s\S]*?</script>', "", head)
    head = re.sub(r"<!-- _dev/[\s\S]*?-->", "", head)

    title = ("California PsyD programs, and what accreditation actually decides "
             "&mdash; Therapist Support")
    desc = ("Every PsyD in California grouped by APA accreditation, with each "
            "school's own published tuition, units and length. California "
            "licenses psychologists without APA accreditation; internship "
            "largely does not. The statute, the regulation and the "
            "consequences, in plain language.")
    meta = (
        "<title>%s</title>\n"
        '<meta name="description" content="%s" />\n'
        '<link rel="canonical" href="https://therapistsupport.org/psyd-programs-california.html">\n'
        '<meta name="ts:topic" content="training">\n'
        '<meta name="ts:format" content="reference">\n'
        '<meta name="ts:question" content="Which PsyD programs are there in California?">\n'
        '<meta name="ts:outcome" content="Every PsyD in the state, grouped by what its accreditation actually gets you">\n'
        '<meta name="ts:number" content="%d of %d are APA-accredited">\n'
        '<meta name="ts:weight" content="5">\n'
        '<meta name="ts:stale" content="false">\n'
        % (title, desc,
           sum(1 for p in PROGRAMS if p["apa"] in ("full", "contingency")),
           len(PROGRAMS)))

    body_start = chrome.index("<body")
    body_open_end = chrome.index(">", body_start) + 1
    header_end = chrome.index("</header>") + len("</header>")
    header = chrome[body_open_end:header_end]

    foot_start = chrome.rindex("<footer")
    foot_end = chrome.index("</footer>", foot_start) + len("</footer>")
    footer = chrome[foot_start:foot_end]

    links = re.findall(r'<link rel="stylesheet" href="css/[0-9a-f]{12}\.css">',
                       chrome)

    doc = ("<!DOCTYPE html>\n<html lang=\"en\">\n" + head + meta + "</head>\n"
           "<body>" + header + "<main>" + body() + "</main>" + footer
           + "\n" + "\n".join(links) + "\n" + CSS + "\n</body>\n</html>\n")

    open(OUT, "w", encoding="utf-8").write(doc)
    print("wrote %s (%.0f KB)" % (os.path.basename(OUT), len(doc) / 1024))

    # ---- guards
    bad = 0
    s = open(OUT, encoding="utf-8").read()
    if s.count("<h1") != 1:
        print("GUARD: %d h1" % s.count("<h1")); bad += 1
    if "<footer" not in s or "sitenav" not in s:
        print("GUARD: chrome missing"); bad += 1
    n = len(re.findall(r'<article class="pdc">', s))
    if n != len(PROGRAMS):
        print("GUARD: %d cards, expected %d" % (n, len(PROGRAMS))); bad += 1
    for href in set(re.findall(r'href="([a-z0-9-]+\.html)"', s)):
        if not os.path.exists(os.path.join(SITE, href)):
            print("GUARD: links %s which does not exist" % href); bad += 1
    for href in set(re.findall(r'href="((?:\.\./)*[a-z-]+/)"', s)):
        if not os.path.exists(os.path.join(SITE, href, "index.html")):
            print("GUARD: links %s which does not exist" % href); bad += 1
    # a figure must never appear without the year it applies to
    for m in re.finditer(r'<span class="pdfig">([^<]*)</span>([^<]*)', s):
        pass
    if bad:
        sys.exit("\n%d problem(s)" % bad)
    print("%d program(s): %d APA-accredited, %d on contingency, %d inactive, "
          "%d not accredited"
          % (len(PROGRAMS),
             sum(1 for p in PROGRAMS if p["apa"] == "full"),
             sum(1 for p in PROGRAMS if p["apa"] == "contingency"),
             sum(1 for p in PROGRAMS if p["apa"] == "inactive"),
             sum(1 for p in PROGRAMS if p["apa"] == "none")))
    print("guards clean")


if __name__ == "__main__":
    main()
