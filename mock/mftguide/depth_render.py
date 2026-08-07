#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Renderers for the deep-research sections of a school page.

WHY THIS IS A SEPARATE MODULE. build_schools.py was already 500 lines of page
assembly and guards. The depth sections roughly triple the content of a page
and they are the part most likely to be edited again, so they live on their own
where they can be changed without touching the page skeleton or the guards.

EVERY RENDERER RETURNS "" WHEN ITS DATA IS ABSENT. Thirty-seven schools were
researched to the same spec and none of them came back complete - catalogs go
behind bot-walls, small schools publish nothing, some programmes genuinely have
no public discussion. A missing section is normal here, so every renderer is
written to degrade to nothing rather than to a heading with an empty body.

WHERE A SECTION IS MISSING BECAUSE THE INFORMATION DOES NOT EXIST, SAY SO.
That is what `gaps` is for and why it gets rendered rather than hidden. A page
that silently omits what it could not find reads as complete; a page that names
its own holes tells the reader which questions to take to admissions.
"""
import html
import re

YT_RE = re.compile(r"^[A-Za-z0-9_-]{11}$")


def esc(x):
    return html.escape(str(x)) if x else ""


def _src(url, label="source"):
    if not url:
        return ""
    return ('<a class="srcl" href="%s" target="_blank" rel="noopener noreferrer">'
            "%s &nearr;</a>" % (esc(url), esc(label)))


# ---------------------------------------------------------------- media

def media(video, photo, name):
    """Video facade + campus photo.

    The video is NOT an iframe on load. A YouTube iframe is ~700 KB of
    third-party JavaScript that sets cookies before the reader has decided to
    watch anything, on a page whose whole proposition is that it is not selling
    them something. So the markup ships a static thumbnail from i.ytimg.com and
    a button; the iframe is created only on click, and then against
    youtube-nocookie.com.

    The thumbnail is loaded with <img>, not a CSS background, so it still shows
    if the page is printed and still has alt text if it fails.
    """
    if not video and not photo:
        return ""
    out = []
    if video and YT_RE.match(video.get("id", "")):
        vid = video["id"]
        kind = {"program-overview": "Programme overview",
                "student-voices": "Students and alumni",
                "faculty-talk": "Faculty",
                "info-session": "Information session"}.get(video.get("kind"), "Video")
        out.append(
            '<figure class="vfig">'
            '<button class="vplay" type="button" data-yt="%s" '
            'aria-label="Play video: %s">'
            '<img src="https://i.ytimg.com/vi/%s/hqdefault.jpg" alt="" '
            'loading="lazy" width="480" height="360">'
            '<span class="vbtn" aria-hidden="true"></span>'
            '<span class="vkind">%s</span></button>'
            '<figcaption><b>%s</b><span>%s</span>'
            '<span class="vmeta">%s &middot; on YouTube &middot; '
            'nothing loads from YouTube until you press play</span>'
            "</figcaption></figure>"
            % (vid, esc(video.get("title", "")), vid, kind,
               esc(video.get("title", "")), esc(video.get("why", "")),
               esc(video.get("channel", ""))))
    if photo and photo.get("file"):
        out.append(
            '<figure class="pfig"><img src="%s" alt="%s" loading="lazy">'
            '<figcaption>%s <span class="cred">%s &middot; %s &middot; '
            '<a href="%s" target="_blank" rel="noopener noreferrer">Commons</a>'
            "</span></figcaption></figure>"
            % (esc(photo["file"]), esc(photo.get("caption") or name),
               esc(photo.get("caption") or ""), esc(photo.get("credit") or ""),
               esc(photo.get("license") or ""), esc(photo.get("page") or "")))
    return '<div class="media">%s</div>' % "".join(out)


# ---------------------------------------------------------------- character

def character(paras, orientation):
    if not paras:
        return ""
    chip = ('<p class="orient"><span>Orientation</span><b>%s</b></p>'
            % esc(orientation)) if orientation else ""
    return chip + "".join("<p>%s</p>" % esc(p) for p in paras)


# ---------------------------------------------------------------- courses

def courses(sig):
    """Signature courses.

    `desc` is the catalog's own text. When the researcher marked it verbatim it
    is rendered as a quotation with the catalog link attached, because the exact
    wording is frequently the entire point - "an unstructured small group in
    which members study their own interaction as it happens" is information
    that survives no paraphrase.

    `why` is this site's analysis and is styled differently so a reader can tell
    the two apart at a glance. Blurring that line would be the single most
    dishonest thing this page could do.
    """
    if not sig:
        return ""
    cards = []
    for c in sig:
        head = []
        if c.get("code"):
            head.append('<span class="ccode">%s</span>' % esc(c["code"]))
        if c.get("units"):
            head.append('<span class="cun">%s units</span>' % esc(c["units"]))
        desc = esc(c.get("desc") or "")
        if desc:
            if c.get("verbatim"):
                desc = ('<blockquote class="cq">%s%s</blockquote>'
                        % (desc, _src(c.get("src"), "catalog")))
            else:
                desc = "<p>%s%s</p>" % (desc, " " + _src(c.get("src"), "catalog")
                                        if c.get("src") else "")
        why = ('<p class="cwhy"><span>Why it is worth noticing</span>%s</p>'
               % esc(c["why"])) if c.get("why") else ""
        cards.append('<article class="crs"><div class="chd">%s</div>'
                     "<h3>%s</h3>%s%s</article>"
                     % ("".join(head), esc(c.get("title") or ""), desc, why))
    return '<div class="crsl">%s</div>' % "".join(cards)


# ---------------------------------------------------------------- curriculum

def curriculum(cur):
    if not cur or not cur.get("terms"):
        return ""
    note = "<p>%s%s</p>" % (esc(cur.get("note") or ""),
                            " " + _src(cur.get("src"), "course sequence")
                            if cur.get("src") else "") if cur.get("note") else ""
    tot = ('<p class="cutot"><b>%s</b><span>units in total</span></p>'
           % esc(cur["total_units"])) if cur.get("total_units") else ""
    terms = []
    for t in cur["terms"]:
        cs = t.get("courses") or []
        terms.append('<div class="trm"><b>%s</b><ol>%s</ol>'
                     '<span class="tn">%d course%s</span></div>'
                     % (esc(t.get("label") or ""),
                        "".join("<li>%s</li>" % esc(c) for c in cs),
                        len(cs), "" if len(cs) == 1 else "s"))
    return note + tot + '<div class="trml">%s</div>' % "".join(terms)


# ---------------------------------------------------------------- practicum

# The five placement models, in the order a reader should feel better about
# them. The wording is deliberately about consequence rather than quality: a
# school does not become a worse school for expecting you to find your own site,
# it becomes a school where a particular thing can go wrong.
#
# This replaces an earlier three-value `who_places` field that was set by hand
# and unevidenced. Every value here came from a quote on the school's own page,
# and the quote is printed underneath.
PLACE = {
    "guaranteed": ("ok", "A seat is guaranteed",
                   "The school states that every student in good standing gets a "
                   "clinical placement. Three of the seventy-eight say this. It "
                   "removes the single most common reason a two-year degree turns "
                   "into a three-year one."),
    "placed": ("ok", "The programme places you",
               "The school finds or assigns the site. You are not competing for "
               "one, which is worth more than almost anything else on this page "
               "- though it is not the same as a guarantee, and it is worth "
               "asking what happens if a placement falls through mid-year."),
    "assisted": ("mix", "You apply, with the school&rsquo;s help",
                 "There is an approved-site list and real support, and the seat "
                 "is still yours to win. Most programmes are here and most "
                 "students manage it. Ask for last year&rsquo;s numbers rather "
                 "than the policy: how many students placed on the first round, "
                 "and how many had to extend."),
    "student-sourced": ("warn", "You find your own site",
                        "Securing a placement is your responsibility. A student "
                        "who cannot find a site cannot graduate, and that risk is "
                        "highest if you are rural, studying online, or need "
                        "Spanish-language or specialty hours."),
    "not published": ("warn", "The school does not say",
                      "Nothing on this school&rsquo;s published pages states who "
                      "secures your placement. That is not the same as a bad "
                      "answer - but it is the first question to ask admissions, "
                      "and the specificity of the reply tells you a great deal. "
                      "Thirty of the seventy-eight are in this position."),
}


def practicum(pr):
    """The practicum section, led by the one fact that can cost a year.

    Order matters here. The verdict goes first, then the quote it rests on,
    then the mechanics. A reader who stops after the first block should have
    got the thing they came for.
    """
    if not pr:
        return ""
    out = ""
    w = PLACE.get(pr.get("model"))
    if w:
        ev = ""
        if pr.get("model_evidence"):
            ev = ('<blockquote class="pq">%s%s</blockquote>'
                  % (esc(pr["model_evidence"]),
                     ' <a href="%s" target="_blank" rel="noopener noreferrer">'
                     "the school&rsquo;s own page &rarr;</a>" % pr["model_url"]
                     if pr.get("model_url") else ""))
        out += ('<div class="verd %s"><h3>%s</h3><p>%s</p>%s</div>'
                % (w[0], w[1], w[2], ev))
    if pr.get("branches"):
        out += '<p class="pnote"><b>Read this twice.</b> %s</p>' % esc(pr["branches"])
    if pr.get("own_clinic"):
        names = pr.get("clinic_names") or []
        out += ('<p class="pnote"><b>The school runs its own training clinic%s.</b> %s '
                "Owning a clinic and holding a seat in it are different things, "
                "so this sits beside the model above rather than replacing it.</p>"
                % ("s" if len(names) > 1 else "",
                   ("&nbsp;" + esc(" &middot; ".join(names))) if names else ""))
    rows = []
    for label, key in (("Who secures the seat", None),
                       ("Starts", "starts"), ("Hours required", "hours"),
                       ("How long it runs", "how_long"),
                       ("In-house clinic", "clinic")):
        if key is None:
            continue
        v = pr.get(key)
        if v:
            rows.append('<div class="pr"><span>%s</span><b>%s</b></div>'
                        % (label, esc(v)))
    if rows:
        out += '<div class="prg">%s</div>' % "".join(rows)
    if pr.get("detail"):
        out += "<p>%s%s</p>" % (esc(pr["detail"]),
                                " " + _src(pr.get("src")) if pr.get("src") else "")
    return out


# ---------------------------------------------------------------- admissions

# What the school says about an admissions test, in its own terms. "Not
# published" is its own answer and must not read as "not required": most
# schools simply list the application items and never mention a test, and a
# reader who turns up without a score because a directory inferred one has been
# failed by the directory.
GRE_LABEL = {
    "required": "Required",
    "not required": "Not required",
    "waivable": "Required, but waivable",
    "not published": '<span class="np">the school does not say</span>',
}


def admissions(ad):
    if not ad:
        return ""
    rows = []
    if ad.get("gre"):
        rows.append('<div class="r"><span>%s</span><b>%s</b></div>'
                    % ("Admissions test", GRE_LABEL.get(ad["gre"], esc(ad["gre"]))))
    if ad.get("min_gpa"):
        rows.append('<div class="r"><span>Minimum GPA</span><b>%s</b></div>'
                    % esc(str(ad["min_gpa"])))
    for label, key in (("Cohort size", "cohort_size"),
                       ("Prerequisites", "prereqs"), ("Deadline", "deadline")):
        v = ad.get(key)
        if v:
            rows.append('<div class="r"><span>%s</span><b>%s</b></div>'
                        % (label, esc(v)))
    if not rows:
        return ""
    out = '<div class="tbl">%s</div>' % "".join(rows)
    if ad.get("gre_evidence"):
        out += ('<blockquote class="pq">%s%s</blockquote>'
                % (esc(ad["gre_evidence"]),
                   ' <a href="%s" target="_blank" rel="noopener noreferrer">'
                   "source &rarr;</a>" % ad["gre_url"] if ad.get("gre_url") else ""))
    if ad.get("conflict"):
        out += ('<div class="verd warn"><h3>The school contradicts itself here</h3>'
                "<p>%s</p></div>" % esc(ad["conflict"]))
    if ad.get("src"):
        out += "<p>%s</p>" % _src(ad.get("src"), "admissions page")
    return out


# ---------------------------------------------------------------- outcomes

def outcomes(oc):
    """COAMFTE Student Achievement Data, for this school and only this school.

    Every figure carries its cohort size in the same cell, and the school's own
    verbatim definition sits above the table. That is not decoration: nine of
    the twelve define "licensure rate" as graduates who reached ANY level of MFT
    licensure, which in California means filing an Associate registration - so
    a 98% licensure rate is largely a statement about paperwork, and printing it
    under a bare heading that says "licensure" would be the misleading part.

    There is no cross-school version of this table anywhere on the site. See
    coamfte_apply.py for the five separate reasons these numbers cannot be
    lined up against each other even though they look as though they can.
    """
    if not oc:
        return ""
    out = ""
    if oc.get("access_note"):
        out += ('<div class="verd mix"><h3>About this disclosure</h3><p>%s</p></div>'
                % oc["access_note"])
    if oc.get("as_published"):
        out += ('<p class="pnote ocdef"><b>In the school&rsquo;s own words, this counts:</b> '
                "&ldquo;%s&rdquo; &mdash; which is worth reading before the "
                "numbers, because it is rarely what the column heading suggests."
                "</p>" % esc(oc["as_published"]))
    for g in oc.get("groups") or []:
        lab = ('<p class="ocl">%s</p>' % esc(g["label"])) if g.get("label") else ""
        rows = "".join(
            "<tr><th scope=\"row\">%s<span>%s in the cohort</span></th>"
            "<td>%s</td><td>%s</td><td>%s</td></tr>"
            % (esc(r["year"]), esc(r["n"]),
               esc(r["graduation"]) or "&mdash;",
               esc(r["licensure"]) or "&mdash;",
               esc(r["placement"]) or "&mdash;")
            for r in g["rows"])
        out += (lab + '<div class="octw"><table class="octbl"><thead><tr>'
                '<th scope="col">Cohort</th><th scope="col">Graduated</th>'
                '<th scope="col">Reached licensure</th>'
                '<th scope="col">In the field</th></tr></thead>'
                "<tbody>%s</tbody></table></div>" % rows)
    if not (oc.get("groups") or []):
        out += ("<p>The school publishes the required table, and it currently "
                "carries no completed cohorts.</p>")
    out += ('<p class="pnote">Graduation is measured against each school&rsquo;s '
            "own <b>advertised</b> length, which across the twelve accredited "
            "programmes runs from two years to four and a half &mdash; so a low "
            "figure often means students chose a longer track rather than that "
            "they did not finish. Licensure and placement are usually shares of "
            "the graduates who <b>answered a survey</b>, not of the cohort. Both "
            "are reasons these numbers describe one programme over time and "
            "cannot be set against another school&rsquo;s.</p>")
    if oc.get("url"):
        out += ('<p><a href="%s" target="_blank" rel="noopener noreferrer">'
                "The school&rsquo;s own disclosure &rarr;</a> &middot; most "
                "recent %d cohorts shown</p>" % (esc(oc["url"]), oc.get("shown", 5)))
    return out


# ---------------------------------------------------------------- exam

def exam(ex):
    """The Board's own by-school exam results for this school.

    THE DESIGN IS THE ARGUMENT. Everything here is arranged so the figure
    cannot be read as a ranking:

      - The candidate count is set at the same size as the percentage. A rate
        without its N is the specific way this kind of number misleads, and
        making N small is how sites pretend otherwise.
      - The statewide figure sits immediately beside it, so the reader has a
        baseline before they have an opinion.
      - The caveat is not a `<details>`. Collapsing it would be choosing to
        have most readers not see the one thing that determines whether the
        number means what it appears to mean.
      - Nothing links to another school's figure, and no such figure exists on
        the directory page. There is deliberately no way to line them up.
    """
    if not ex:
        return ""
    src = ('<a href="%s" target="_blank" rel="noopener noreferrer">'
           "the Board&rsquo;s published exam results by school &rarr;</a>"
           % esc(ex["source"]))
    st = ex.get("statewide") or {}
    if ex.get("enough"):
        head = (
            '<div class="exg">'
            '<div class="exb"><b>%d%%</b><em>passed first time</em>'
            '<span>%s of %s candidates</span></div>'
            '<div class="exb sw"><b>%d%%</b><em>statewide, same window</em>'
            '<span>%s of %s candidates</span></div>'
            "</div>"
            % (ex["first_time_pct"],
               "{:,}".format(ex["first_time_passed"]),
               "{:,}".format(ex["first_time_taking"]),
               st.get("first_time", 0),
               "{:,}".format(st.get("first_time_passed", 0)),
               "{:,}".format(st.get("first_time_n", 0))))
        extra = ("<p>Counting every attempt rather than only first attempts, "
                 "the figure is <b>%d%%</b> across %s sittings here, against "
                 "<b>%d%%</b> statewide. First attempts are the fairer "
                 "comparison &mdash; counting resits measures how many tries "
                 "people needed rather than how many passed, and it penalises "
                 "a school whose graduates keep going.</p>"
                 % (ex["all_pct"], "{:,}".format(ex["all_taking"]),
                    st.get("all", 0)))
    else:
        head = ('<div class="verd mix"><h3>Too few candidates to publish a rate</h3>'
                "<p>The Board recorded <b>%d</b> first-time candidates from this "
                "school across the whole window, and this page does not print a "
                "percentage below %d. On a handful of candidates a single result "
                "moves the figure by tens of points, and a small programme would "
                "be described by noise. It usually means the programme is small, "
                "new, or both.</p></div>"
                % (ex["first_time_taking"], ex["floor"]))
        extra = ""

    as_rec = ex.get("as_recorded") or []
    rec = ""
    if as_rec:
        rec = ("<p class=\"pnote\">Recorded by the Board as <b>%s</b>. Its list is "
               "kept by institution and its names lag: a school that has since "
               "renamed appears under the name it had when the candidates "
               "sat.</p>" % esc(" &middot; ".join(as_rec)))

    # `exwarn` exists so the build check can assert this block by itself. The
    # section id is on the <h2> and the body is its SIBLING, so "#exam-results
    # .verd.warn" matches nothing - which is how a check that looked correct
    # passed on a page that had lost the caveat entirely.
    caveat = (
        '<div class="verd warn exwarn"><h3>What this number is, and what it is not</h3>'
        "<p><b>It describes candidates, not teaching.</b> In 2022 the Council on "
        "Social Work Education removed licensing-exam pass rates from its "
        "accreditation standards, saying the data &ldquo;may not be an equitable "
        "measure of program outcomes&rdquo; &mdash; after the social-work exam "
        "board&rsquo;s own analysis found first-time pass rates of 84% for white "
        "candidates and 45% for Black candidates. A programme that enrols more "
        "career-changers and more students of colour will post a lower rate while "
        "teaching at least as well. The accrediting body with the most reason to "
        "want this metric examined it and stopped using it.</p>"
        "<p><b>The denominator is not this year&rsquo;s students.</b> These are "
        "people who sat the exam during the window, often several years after "
        "graduating and sometimes after the programme changed shape or owner.</p>"
        "<p>It is published here because it is a real, official figure that is "
        "otherwise almost impossible to find &mdash; and it is published on this "
        "page only. There is no pass-rate column in the directory, nothing is "
        "sorted by it, and no school on this site is ranked against another.</p>"
        "</div>")

    le = ""
    if ex.get("law_ethics_pct"):
        le = ("<p>On the separate California Law and Ethics exam, <b>%d%%</b> of "
              "this school&rsquo;s %s first-time candidates passed, against "
              "<b>%d%%</b> statewide.</p>"
              % (ex["law_ethics_pct"], "{:,}".format(ex["law_ethics_taking"]),
                 st.get("law_ethics_first_time") or 0)
              if st.get("law_ethics_first_time") else
              "<p>On the separate California Law and Ethics exam, <b>%d%%</b> of "
              "this school&rsquo;s %s first-time candidates passed.</p>"
              % (ex["law_ethics_pct"], "{:,}".format(ex["law_ethics_taking"])))

    return (head + extra + le + rec + caveat +
            "<p>%s &middot; %s</p>" % (esc(ex["period"]), src))


# ---------------------------------------------------------------- voices

SENT = {"positive": ("pos", "positive"), "negative": ("neg", "critical"),
        "mixed": ("mix", "mixed"), "info": ("inf", "informational")}


def voices(vx):
    if not vx:
        return ""
    cards = []
    for v in vx:
        cls, lab = SENT.get(v.get("sentiment"), ("inf", "informational"))
        url = v.get("url")
        body = ('<i>%s</i><span class="vwho">%s</span>'
                '<span class="sn">%s</span>'
                % (esc(v.get("text") or ""), esc(v.get("who") or ""), lab))
        if url:
            cards.append('<a class="vox %s" href="%s" target="_blank" '
                         'rel="noopener noreferrer">%s</a>' % (cls, esc(url), body))
        else:
            cards.append('<div class="vox %s">%s</div>' % (cls, body))
    return '<div class="voxl">%s</div>' % "".join(cards)


# ---------------------------------------------------------------- gaps

def gaps(gs, sources):
    """What the research could not establish, named.

    This section exists because the alternative is worse. Every one of these
    pages is assembled from catalogs, handbooks, accreditor disclosures and
    regulator filings, and every one of them has holes - a bot-walled catalog, a
    programme that publishes no cost, an accreditation table marked "in
    process". Listing the holes turns each into a question the reader can put to
    admissions, and it stops the rest of the page from being read as more
    complete than it is.
    """
    out = ""
    if gs:
        out += ('<p>Everything above is sourced. These are the things I looked '
                "for and could not establish - take them to admissions, and "
                "note how quickly and precisely they answer.</p>"
                '<ul class="gapl">%s</ul>'
                % "".join("<li>%s</li>" % esc(g) for g in gs))
    if sources:
        out += ('<details class="srcs"><summary>Sources for this page '
                "(%d)</summary><ol>%s</ol></details>"
                % (len(sources),
                   "".join('<li><a href="%s" target="_blank" '
                           'rel="noopener noreferrer">%s</a></li>'
                           % (esc(s.get("url") or ""), esc(s.get("label") or s.get("url")))
                           for s in sources if s.get("url"))))
    return out
