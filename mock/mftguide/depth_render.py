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
