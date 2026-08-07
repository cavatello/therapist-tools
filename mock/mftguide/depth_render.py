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


# ---------------------------------------------------------------- tracks

def tracks(tr):
    """Concentrations inside one degree.

    Several California institutions run ONE M.A. with several BBS-approved
    concentrations under it, and the school is then two decisions rather than
    one: the institution, then the track. The unit counts, length and delivery
    format differ per track, and at some schools one track does not reach the
    LMFT at all - which is the single most expensive thing a prospective
    student can fail to notice, because it is usually the most convenient one.

    Rendered as rows rather than prose because the whole value is the
    comparison, and prose hides a column that differs by one number.
    """
    if not tr or not tr.get("rows"):
        return ""
    note = ("<p>%s%s</p>" % (esc(tr.get("note") or ""),
            " " + _src(tr.get("src"), "the department") if tr.get("src") else "")
            ) if tr.get("note") else ""
    rows = []
    for r in tr["rows"]:
        lm = esc(r.get("lmft") or "")
        cell = ('<span class="trkno">not an LMFT route</span>'
                if r.get("lmft_no") else '<b>%s</b>' % lm)
        rows.append(
            '<div class="trkr%s"><div class="trkn"><b>%s</b>%s</div>'
            '<div class="trku"><span>LMFT</span>%s</div>'
            '<div class="trku"><span>LPCC</span><b>%s</b></div>'
            '<div class="trkf"><span>%s</span><span>%s</span></div></div>'
            % (" no" if r.get("lmft_no") else "",
               esc(r.get("name") or ""),
               '<span>%s</span>' % esc(r["note"]) if r.get("note") else "",
               cell, esc(r.get("lpcc") or "&mdash;"),
               esc(r.get("length") or ""), esc(r.get("format") or "")))
    head = ('<div class="trkr hd"><div class="trkn">Concentration</div>'
            '<div class="trku">LMFT units</div><div class="trku">LPCC units</div>'
            '<div class="trkf">Length and format</div></div>')
    return note + '<div class="trk">%s%s</div>' % (head, "".join(rows))


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

PLACE = {
    "program-placed": ("ok", "The programme places you",
                       "The school owns the problem of finding you a site. This "
                       "is the single biggest structural difference between "
                       "programmes and it is worth more than almost anything "
                       "else on this page."),
    "student-finds": ("warn", "You find your own site",
                      "You are responsible for securing a placement. Most "
                      "programmes are like this and most students manage it, "
                      "but a student who cannot find a site cannot graduate - "
                      "and that risk is highest if you are rural, online, or "
                      "need Spanish-language or specialty hours."),
    "mixed": ("mix", "Mixed - some help, your responsibility",
              "The programme maintains a site list or relationships and may "
              "place some students, but securing the placement is ultimately "
              "yours. Ask for last year's numbers, not the policy."),
}


def practicum(pr):
    if not pr:
        return ""
    rows = []
    for label, key in (("Starts", "starts"), ("Hours required", "hours"),
                       ("In-house clinic", "clinic")):
        v = pr.get(key)
        if v:
            rows.append('<div class="pr"><span>%s</span><b>%s</b></div>'
                        % (label, esc(v)))
    grid = '<div class="prg">%s</div>' % "".join(rows) if rows else ""
    who = ""
    w = PLACE.get(pr.get("who_places"))
    if w:
        who = ('<div class="verd %s"><h3>%s</h3><p>%s</p></div>'
               % (w[0], w[1], w[2]))
    detail = "<p>%s%s</p>" % (esc(pr.get("detail") or ""),
                              " " + _src(pr.get("src"))
                              if pr.get("src") else "") if pr.get("detail") else ""
    return who + grid + detail


# ---------------------------------------------------------------- admissions

def admissions(ad):
    if not ad:
        return ""
    rows = []
    for label, key in (("Cohort size", "cohort_size"), ("GRE", "gre"),
                       ("Prerequisites", "prereqs"), ("Deadline", "deadline")):
        v = ad.get(key)
        if v:
            rows.append('<div class="r"><span>%s</span><b>%s</b></div>'
                        % (label, esc(v)))
    if not rows:
        return ""
    return ('<div class="tbl">%s</div>' % "".join(rows)) + (
        "<p>%s</p>" % _src(ad.get("src"), "admissions page") if ad.get("src") else "")


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
