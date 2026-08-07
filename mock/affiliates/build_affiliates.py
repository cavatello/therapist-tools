#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Build the affiliate disclosure page and the SimplePractice review.

TWO PAGES, ONE UNCOMFORTABLE PROBLEM.

This site's whole proposition is that every figure is computed or cited and
that nothing here is trying to sell anything. It now carries affiliate links.
Those two things can coexist, but only if the second one is handled with more
care than the money is worth - which is the standard applied here.

So: the disclosure page says exactly what each arrangement is and what it pays,
including where that is unknown. The review page leads with the number that
actually costs the reader most (card processing, which at a full caseload is
five times the subscription), states plainly the cheapest tier that does the job
for a California associate, and ends on a section titled "you may not need this
at all" with three options that would earn nothing. If the honest verdict for a
given reader is "don't buy it", the page has to say so, or none of the rest of
the site is trustworthy either.

The affiliate URL itself does NOT appear in this file. It comes from
mock/affiliates/partners.json via _dev/affiliate.py, which rewrites the bare
simplepractice.com URL after these pages are generated. That is deliberate:
these builders write natural prose linking to a product's real address, and
exactly one file in the repo knows the tracking code.
"""
import os, re, sys, json, html

HERE = os.path.dirname(os.path.abspath(__file__))
WORK = os.path.dirname(HERE)
SITE = os.path.join(WORK, "..", "stage2")
CHROME = os.path.join(SITE, "become-an-mft-california.html")
OUT = os.path.join(HERE, "out")
BASE = "https://cavatello.github.io/therapist-tools/"
UPDATED = "7 August 2026"

REG = json.load(open(os.path.join(HERE, "partners.json"), encoding="utf-8"))
PARTNERS = [p for p in REG["partners"] if p.get("active", True)]
SP = json.load(open(os.path.join(HERE, "simplepractice.json"), encoding="utf-8"))


def esc(x):
    return html.escape(str(x)) if x is not None else ""


def src(url, label="source"):
    return ('<a class="srcl" href="%s" target="_blank" rel="noopener noreferrer">'
            "%s &nearr;</a>" % (esc(url), esc(label))) if url else ""


# ---------------------------------------------------------------- chrome

def balanced(s, tag, start=0):
    i = s.find("<" + tag, start)
    if i < 0:
        return None
    d = 0
    for m in re.finditer(r"<%s\b|</%s>" % (tag, tag), s[i:]):
        d += 1 if m.group(0).startswith("<" + tag) else -1
        if d == 0:
            return (i, i + m.end())
    return None


src_doc = open(CHROME, encoding="utf-8").read()
_he = src_doc.find("</head>")
LINKS = "\n".join(m.group(0) for m in re.finditer(r"<link\b[^>]*>", src_doc[:_he])
                  if 'rel="stylesheet"' in m.group(0) or "fonts." in m.group(0)
                  or 'rel="preconnect"' in m.group(0))
STYLES = "\n".join(re.findall(r"<style>.*?</style>", src_doc, re.S))
assert STYLES or "css/" in LINKS, "no stylesheet lifted - the page would render bare"
_h = balanced(src_doc, "header")
HEADER = re.sub(r'(<a href="[^"]*") class="on"', r"\1", src_doc[_h[0]:_h[1]])
_f = balanced(src_doc, "footer")
FOOTER = re.sub(r'(<a href="[^"]*") class="on"', r"\1", src_doc[_f[0]:_f[1]])
NAVSCRIPT = ""
for m in re.finditer(r"<script>([\s\S]*?)</script>", src_doc):
    if "navpanel" in m.group(1):
        NAVSCRIPT = m.group(0)
assert NAVSCRIPT, "no nav script in the chrome - the header would be dead"


def crumbs_ld(items):
    return json.dumps({
        "@context": "https://schema.org", "@type": "BreadcrumbList",
        "itemListElement": [
            {"@type": "ListItem", "position": i + 1, "name": n,
             **({"item": BASE + u} if u else {})}
            for i, (n, u) in enumerate(items)]}, separators=(",", ":"))


def crumbs_html(items):
    out = []
    for i, (n, u) in enumerate(items):
        sep = '<span class="sep">&rsaquo;</span>' if i < len(items) - 1 else ""
        out.append('<li><a href="%s">%s</a>%s</li>' % (esc(u), esc(n), sep) if u
                   else '<li><span aria-current="page">%s</span></li>' % esc(n))
    return '<ol class="bcr" aria-label="Breadcrumb">%s</ol>' % "".join(out)


def page(title, desc, canon, kicker, h1, dek, meta, nav, body, crumbs):
    return """<!doctype html>
<html lang="en"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>%s</title>
<meta name="description" content="%s">
<link rel="canonical" href="%s%s">
%s
%s
%s
<script type="application/ld+json">%s</script>
</head><body class="afp">
%s
<main>
<section class="afband"><div class="in">%s<p class="sub">%s</p><h1>%s</h1>
<p class="dek">%s</p><div class="afmeta">%s</div></div></section>
<div class="afwrap">%s<article class="afbody">%s</article></div>
</main>
%s
%s
</body></html>""" % (esc(title), esc(desc), BASE, canon, LINKS, STYLES, CSS,
                     crumbs_ld(crumbs), HEADER, crumbs_html(crumbs), esc(kicker),
                     h1, dek, "".join("<span>%s</span>" % esc(m) for m in meta),
                     nav, body, FOOTER, NAVSCRIPT)


def navof(secs):
    return '<nav class="afnav"><b>On this page</b>%s</nav>' % "".join(
        '<a href="#%s">%s</a>' % (i, t) for i, t, _b in secs)


def bodyof(secs):
    return "".join('<h2 id="%s">%s</h2>%s' % (i, t, b) for i, t, b in secs)


# ---------------------------------------------------------------- disclosure

def build_disclosure():
    rows = []
    for p in PARTNERS:
        rows.append(
            '<article class="pcard" id="%s"><h3>%s</h3>'
            '<p class="what">%s</p>'
            '<div class="tbl">'
            '<div class="r"><span>The arrangement</span><b>%s</b></div>'
            '<div class="r"><span>What it pays</span><b>%s</b></div>'
            '<div class="r"><span>What it costs you</span><b>%s</b></div>'
            "</div>"
            '<p><a href="%s" target="_blank" rel="sponsored nofollow noopener noreferrer">'
            "%s &rarr;</a></p></article>"
            % (esc(p["slug"]), esc(p["name"]), esc(p["what"]), esc(p["program"]),
               esc(p["pays"]) if p.get("pays") else
               "<span class=\"np\">not disclosed to me by the programme</span>",
               esc(p["costs_you"]), esc(p["bare"]), esc(p["name"])))

    secs = [
        ("what-this-is", "What this page is", (
            "<p>Some links on this site earn money if you sign up for something "
            "through them. This page lists <b>every</b> one of them, what the "
            "arrangement actually is, and what it costs you &mdash; which in "
            "every case is nothing.</p>"
            "<p>It exists because the site used to say, in the footer of every "
            "page, that it was &ldquo;not selling anything&rdquo;. That was "
            "true when it was written and it stopped being true the moment the "
            "first affiliate link shipped. Rather than quietly delete the "
            "claim, the honest version is this: here is the list, kept in one "
            "file, and here is what each one is.</p>")),
        ("the-rule", "The rule I hold myself to", (
            '<div class="rule"><b>An affiliate link never changes a number on '
            "this site.</b><span>Every calculator, every rate, every published "
            "tuition figure and every comparison is what it would be if none of "
            "these arrangements existed. Where a product I earn from is worse "
            "than one I do not, the page says so &mdash; the SimplePractice "
            "review below spends more words on what it costs and who should not "
            "buy it than on what it does well.</span></div>"
            "<p>Three practical commitments behind that:</p>"
            "<ul class=\"rules\">"
            "<li><b>Marked at the link, not only here.</b> Every affiliate link "
            "on the site carries a visible <span class=\"afl-demo\">affiliate"
            "</span> tag immediately beside it. A disclosure you have to go "
            "looking for is the letter of the rule and not the point of it.</li>"
            "<li><b>No paid placement, ever.</b> Nothing appears on this site "
            "because someone paid for it to. The two arrangements below are both "
            "products I would have written about anyway, and both pages were "
            "researched before the link existed.</li>"
            "<li><b>Cheaper alternatives get named.</b> Where there is a "
            "genuinely cheaper path that earns me nothing, it is on the page, "
            "with its price.</li></ul>")),
        ("partners", "Every arrangement, in full",
         "<p>Two, at the time of writing. If this list grows, it grows here "
         "first &mdash; it is generated from a single file in the repository, "
         "so a link cannot exist on the site without appearing on this "
         'page.</p><div class="pgrid">%s</div>' % "".join(rows)),
        ("what-i-dont-do", "What I do not do", (
            "<ul class=\"rules\">"
            "<li><b>No advertising.</b> There are no ad slots, no trackers sold "
            "to anyone, and no sponsored posts.</li>"
            "<li><b>No email list rental, no data sales.</b> The calculators "
            "store nothing on a server; there is nothing to sell.</li>"
            "<li><b>No affiliate links inside a calculator&rsquo;s results.</b> "
            "A tool that computes your take-home does not then recommend you "
            "something. The links live in prose, on pages that are about the "
            "thing being linked to.</li>"
            "<li><b>No link to anything I would not use.</b> That is a low bar "
            "and it is the honest one &mdash; it does not mean these are the "
            "best products for you, only that they are not junk.</li></ul>"
            '<p><a href="contact.html">If something here looks like it is '
            "shading toward a sales pitch, tell me</a>. That is the failure "
            "mode worth catching early.</p>")),
    ]
    return page(
        "Affiliate disclosure — every paid link on Therapist Support",
        "Every affiliate arrangement on this site, what each one pays, and what "
        "it costs you (nothing). Plus the rule: an affiliate link never changes "
        "a number on this site.",
        "affiliate-disclosure.html", "Full disclosure",
        "Every link on this site that <em>earns money</em>, and what it pays.",
        "Two arrangements, both listed in full. Neither costs you anything, and "
        "neither changes a single figure anywhere on this site.",
        ["Updated " + UPDATED, "%d arrangements" % len(PARTNERS)],
        navof(secs), bodyof(secs),
        [("Therapist Support", "index.html"),
         ("Everything", "resources.html"), ("Affiliate disclosure", None)])


# ---------------------------------------------------------------- review

def build_simplepractice():
    P = SP["pricing"]
    tiers = "".join(
        '<article class="tier%s"><h3>%s</h3><p class="pr">$%s<span>a month</span></p>'
        "%s%s</article>"
        % (" best" if t["name"] == "Plus" else "", esc(t["name"]),
           esc(t["monthly"]),
           '<ul class="inc">%s</ul>' % "".join("<li>%s</li>" % esc(x)
                                               for x in (t.get("includes") or [])[:6]),
           ('<ul class="exc"><b>Not included</b>%s</ul>'
            % "".join("<li>%s</li>" % esc(x) for x in (t.get("excludes") or [])[:5]))
           if t.get("excludes") else "")
        for t in P["tiers"])

    extras = "".join(
        '<div class="r"><span>%s</span><b>%s %s</b></div>'
        % (esc(e["what"])[:120], esc(e["cost"]), src(e.get("src")))
        for e in (P.get("extras") or []))

    hidden = ('<div class="verd warn"><h3>The subscription is not the cost</h3>'
              "<p><b>Card processing is %s.</b> A therapist billing $8,000 a "
              "month in private pay hands over about $255 of it &mdash; more "
              "than five times the Starter subscription. It is the largest "
              "number on this page and it is the one nobody compares.</p>"
              "<p>%s</p></div>"
              % (esc(P.get("card_processing", "")[:90]),
                 esc(P.get("claim_and_clearinghouse_fees", ""))[:400]))

    cal = "".join(
        '<div class="q"><b>%s</b><p>%s %s</p></div>'
        % (esc(c["topic"]), esc(c["finding"]), src(c.get("src")))
        for c in SP["california"])

    A = SP["associates"]
    assoc = ('<div class="verd %s"><h3>%s</h3><p>%s</p></div>'
             % ("ok" if A.get("cosign") else "warn",
                "Supervisor co-signature works &mdash; on the %s"
                % esc(A.get("tier", "top tier")),
                esc(A.get("detail", ""))[:900] + " " + src(A.get("src"))))

    alts = "".join(
        '<div class="alt m-%s"><b>%s</b><span class="mo">%s</span>'
        "<span class=\"su\">%s</span>%s</div>"
        % (esc(a.get("model", "software")), esc(a["name"]), esc(a.get("monthly", "")),
           esc(a.get("suits", "")),
           ('<a href="%s" target="_blank" rel="noopener noreferrer">its own page '
            "&rarr;</a>" % esc(a["url"])) if a.get("url") else "")
        for a in SP["alternatives"] if a["name"] != "SimplePractice")

    crit = "".join(
        '<div class="cr"><p>%s</p><span class="who">%s%s</span></div>'
        % (esc(c["what"]), esc(c.get("who", "")),
           " " + src(c["url"], "read it") if c.get("url") else "")
        for c in SP["criticism"])

    secs = [
        ("verdict", "The short version", (
            '<div class="lede">%s</div>'
            % "".join("<p>%s</p>" % esc(v) for v in SP["verdict"][:3])
            + '<p><a href="%s" target="_blank" rel="noopener noreferrer">'
              "SimplePractice &rarr;</a></p>" % esc(SP["url"]))),
        ("what-it-is", "What it actually is",
         "".join("<p>%s</p>" % esc(x) for x in SP["summary"])),
        ("price", "What it costs, all in",
         "<p>Three tiers, and the tier you need is decided by two things: "
         "whether you bill insurance, and whether anyone has to co-sign your "
         "notes. Everything below is SimplePractice&rsquo;s own published "
         "figure as of %s.</p>" % esc(P.get("as_of", "August 2026"))
         + '<div class="tiers">%s</div>' % tiers + hidden
         + ("<p>The charges that are not on the pricing page:</p>"
            '<div class="tbl">%s</div>' % extras if extras else "")
         + ("<p><b>Realistically, all in:</b> %s</p>"
            % esc(P["realistic_all_in_solo_private_pay"])
            if P.get("realistic_all_in_solo_private_pay") else "")),
        ("associates", "If you are an associate, or supervise one", assoc),
        ("california", "The California-specific answers",
         "<p>Seven things a California therapist needs from practice software "
         "that a generic review will not tell you.</p>"
         '<div class="ask">%s</div>' % cal),
        ("alternatives", "What else there is, with prices",
         "<p>Including the options that earn me nothing. A therapist seeing "
         "eight private-pay clients a week does not need $99 a month of "
         "software, and the bottom of this list is how you do it for under "
         "$60.</p><div class=\"alts\">%s</div>" % alts),
        ("criticism", "The complaints, unsoftened",
         "<p>Sourced, and left as found.</p>" + crit),
        ("leaving", "What you can take with you if you leave",
         "<p>%s %s</p>" % (esc(SP["portability"].get("detail", "")),
                           src(SP["portability"].get("src")))),
        ("who-should-not", "Who should not buy it", (
            "".join("<p>%s</p>" % esc(v) for v in SP["verdict"][3:])
            + '<div class="rule"><b>Disclosure.</b><span>%s</span></div>'
              '<p><a href="affiliate-disclosure.html">Every paid link on this '
              "site, in full &rarr;</a></p>"
            % esc(SP.get("affiliate_disclosure_note", "")))),
    ]
    if SP.get("gaps"):
        secs.append(("gaps", "What I could not establish",
                     "<p>Take these to their sales team, and notice how quickly "
                     "they answer.</p><ul class=\"gapl\">%s</ul>"
                     % "".join("<li>%s</li>" % esc(g) for g in SP["gaps"])
                     + ('<details class="srcs"><summary>Sources (%d)</summary>'
                        "<ol>%s</ol></details>"
                        % (len(SP["sources"]),
                           "".join('<li><a href="%s" target="_blank" '
                                   'rel="noopener noreferrer">%s</a></li>'
                                   % (esc(s["url"]), esc(s.get("label") or s["url"]))
                                   for s in SP["sources"] if s.get("url"))))))

    return page(
        "SimplePractice for California therapists: real cost, the associate "
        "co-signature problem, and cheaper alternatives",
        "What SimplePractice actually costs a California therapist once card "
        "processing, claim fees and the AMA fee are counted — plus which tier "
        "an AMFT needs for supervisor co-signature, and three cheaper paths.",
        "simplepractice-california-therapists.html",
        "Practice software, reviewed",
        "SimplePractice, and <em>what it really costs</em>.",
        esc(SP["one_line"])[:230],
        ["Updated " + UPDATED, "Checked Aug 2026", "Affiliate link, disclosed"],
        navof(secs), bodyof(secs),
        [("Therapist Support", "index.html"),
         ("Running a practice", "practice/"),
         ("SimplePractice", None)])


CSS = """<style>/* affiliate pages */
.afp{--pine:#2C6350;--amber:#F6C560;--ink:#17271F;--line:#E2DACA;--mut:#7C8878;
  --green:#3F9577;--red:#B5483F}
.afband{background:linear-gradient(135deg,#14261E 0%,#1B4536 48%,#2C6350 100%);
  color:#EFF5F2;padding:30px 0 36px}
.afband .in{max-width:1120px;margin:0 auto;padding:0 26px}
.afband .bcr{display:flex;flex-wrap:wrap;align-items:center;gap:4px 8px;margin:0 0 14px;
  padding:0;list-style:none;font-family:'IBM Plex Mono',ui-monospace,monospace;
  font-size:10.4px;letter-spacing:.1em;text-transform:uppercase}
.afband .bcr li{display:flex;align-items:center;gap:8px}
.afband .bcr a{color:#EFF5F2;opacity:.66;text-decoration:none;padding:5px 0;min-height:26px;
  display:inline-flex;align-items:center;border-bottom:1px solid transparent}
.afband .bcr a:hover{opacity:1;border-bottom-color:currentColor}
.afband .bcr .sep{opacity:.36}
.afband .bcr [aria-current]{opacity:.95;font-weight:600;color:var(--amber)}
.afband .sub{font-family:'IBM Plex Mono',monospace;font-size:11px;letter-spacing:.11em;
  text-transform:uppercase;color:var(--amber);margin:0 0 12px}
.afband h1{font-family:Fraunces,Georgia,serif;font-size:clamp(26px,3.5vw,40px);
  line-height:1.07;font-weight:600;letter-spacing:-.02em;color:#fff;margin:0 0 13px;
  max-width:20ch}
.afband h1 em{font-style:normal;color:var(--amber)}
.afband .dek{font-size:15.4px;line-height:1.72;color:rgba(255,255,255,.87);margin:0;
  max-width:62ch}
.afmeta{display:flex;gap:14px;flex-wrap:wrap;margin-top:17px;
  font-family:'IBM Plex Mono',monospace;font-size:10.4px;letter-spacing:.06em;
  text-transform:uppercase;color:rgba(255,255,255,.62)}

.afwrap{max-width:1120px;margin:0 auto;padding:32px 26px 20px;display:grid;
  grid-template-columns:206px minmax(0,1fr);gap:38px;align-items:start}
.afnav{position:sticky;top:16px;min-width:0}
.afnav b{display:block;font-family:'IBM Plex Mono',monospace;font-size:10px;
  letter-spacing:.13em;text-transform:uppercase;color:var(--mut);margin-bottom:11px}
.afnav a{display:block;font-size:13px;line-height:1.42;color:#4A5A46;text-decoration:none;
  padding:6px 0 6px 12px;border-left:2px solid var(--line)}
.afnav a:hover{color:var(--ink);border-left-color:#B9AE93}
.afnav a.on{color:var(--pine);border-left-color:var(--pine);font-weight:600}
.afbody{min-width:0}
.afbody h2{font-family:Fraunces,Georgia,serif;font-size:clamp(20px,2.4vw,26px);
  line-height:1.2;font-weight:600;color:var(--ink);margin:42px 0 13px;scroll-margin-top:20px}
.afbody h2:first-child{margin-top:0}
.afbody p{font-size:15.2px;line-height:1.78;color:#3B4A38;margin:0 0 15px;max-width:68ch}
.afbody a{color:var(--pine)}
.lede p{font-size:16.6px;line-height:1.72}
.lede p:first-child{font-weight:500;color:var(--ink)}

.rule{background:#F2F8F1;border:1px solid #CFE3CB;border-left:4px solid var(--green);
  border-radius:12px;padding:18px 20px;margin:8px 0 18px}
.rule b{display:block;font-family:Fraunces,Georgia,serif;font-size:18px;color:var(--ink);
  margin-bottom:7px}
.rule span{display:block;font-size:14.5px;line-height:1.72;color:#3B4A38}
.rules{margin:8px 0 16px;padding-left:19px}
.rules li{font-size:14.8px;line-height:1.72;color:#3B4A38;margin-bottom:10px;max-width:68ch}
.afl-demo{display:inline-block;font-family:'IBM Plex Mono',monospace;font-size:9.4px;
  letter-spacing:.09em;text-transform:uppercase;background:#FBF0E2;color:#8A5B22;
  border:1px solid #EBD9BC;border-radius:20px;padding:2px 7px;vertical-align:middle}

.pgrid{display:grid;gap:13px;margin:14px 0}
.pcard{background:#fff;border:1px solid var(--line);border-radius:13px;padding:19px 21px;
  border-left:3px solid var(--amber);min-width:0}
.pcard h3{font-family:Fraunces,Georgia,serif;font-size:19px;color:var(--ink);margin:0 0 6px}
.pcard .what{font-size:14.2px;line-height:1.62;color:#4A5A46;margin:0 0 12px;max-width:none}

.tiers{display:grid;grid-template-columns:repeat(auto-fit,minmax(232px,1fr));gap:12px;
  margin:14px 0}
.tier{background:#fff;border:1px solid var(--line);border-radius:13px;padding:18px 20px;
  min-width:0}
.tier.best{border-color:var(--pine);border-width:2px}
.tier h3{font-family:Fraunces,Georgia,serif;font-size:18px;color:var(--ink);margin:0 0 4px}
.tier .pr{font-family:Fraunces,Georgia,serif;font-size:33px;color:var(--pine);margin:0 0 12px;
  line-height:1}
.tier .pr span{font-family:'IBM Plex Mono',monospace;font-size:10px;letter-spacing:.08em;
  text-transform:uppercase;color:var(--mut);margin-left:7px}
.tier ul{margin:0 0 10px;padding:0;list-style:none}
.tier li{position:relative;padding-left:18px;font-size:13px;line-height:1.55;color:#4A5A46;
  margin-bottom:6px}
.tier .inc li:before{content:"";position:absolute;left:1px;top:6px;width:8px;height:4px;
  border-left:2px solid var(--green);border-bottom:2px solid var(--green);
  transform:rotate(-45deg)}
.tier .exc{border-top:1px solid #F0EBDE;padding-top:10px}
.tier .exc b{display:block;font-family:'IBM Plex Mono',monospace;font-size:9.4px;
  letter-spacing:.09em;text-transform:uppercase;color:#9C3E36;margin-bottom:7px}
.tier .exc li:before{content:"";position:absolute;left:2px;top:9px;width:9px;height:2px;
  background:var(--red)}

.verd{border-radius:12px;padding:19px 21px;margin:8px 0 18px;border:1px solid}
.verd.ok{background:#F2F8F1;border-color:#CFE3CB;border-left:4px solid var(--green)}
.verd.warn{background:#FBF0E2;border-color:#EBD9BC;border-left:4px solid #C98B4B}
.verd h3{font-family:Fraunces,Georgia,serif;font-size:18.5px;margin:0 0 8px;color:var(--ink)}
.verd p{margin:0 0 10px;font-size:14.6px;max-width:none;color:#3B4A38}
.verd p:last-child{margin-bottom:0}

.tbl{display:grid;background:#fff;border:1px solid var(--line);border-radius:11px;
  overflow:hidden;margin:8px 0 14px}
.tbl .r{display:grid;grid-template-columns:190px minmax(0,1fr);gap:14px;padding:13px 16px;
  border-bottom:1px solid #F0EBDE;font-size:14px}
.tbl .r:last-child{border-bottom:0}
.tbl .r span{font-family:'IBM Plex Mono',monospace;font-size:10.2px;letter-spacing:.07em;
  text-transform:uppercase;color:var(--mut);padding-top:3px}
.tbl .r b{font-weight:400;color:#3B4A38;line-height:1.66;min-width:0;overflow-wrap:anywhere}
.np{color:#B0A896;font-style:italic}

.ask{display:grid;gap:9px;margin:10px 0}
.q{background:#fff;border:1px solid var(--line);border-radius:10px;padding:15px 17px;
  min-width:0}
.q b{display:block;font-size:14.6px;color:var(--ink);margin-bottom:6px}
.q p{font-size:13.8px;line-height:1.68;color:#4A5A46;margin:0;max-width:none}

.alts{display:grid;grid-template-columns:repeat(auto-fill,minmax(252px,1fr));gap:11px;
  margin:12px 0}
.alt{background:#fff;border:1px solid var(--line);border-radius:11px;padding:15px 17px;
  min-width:0;border-top:3px solid #CFC7B4}
.alt.m-network{border-top-color:#C98B4B}
.alt.m-DIY,.alt.m-diy{border-top-color:var(--green)}
.alt b{display:block;font-family:Fraunces,Georgia,serif;font-size:16.5px;color:var(--ink);
  margin-bottom:4px}
.alt .mo{display:block;font-family:'IBM Plex Mono',monospace;font-size:11.6px;
  color:var(--pine);margin-bottom:8px;line-height:1.5}
.alt .su{display:block;font-size:13.2px;line-height:1.6;color:#4A5A46;margin-bottom:8px}
.alt a{font-family:'IBM Plex Mono',monospace;font-size:9.6px;letter-spacing:.07em;
  text-transform:uppercase}

.cr{background:#fff;border:1px solid var(--line);border-left:3px solid var(--red);
  border-radius:10px;padding:14px 16px;margin-bottom:9px}
.cr p{margin:0 0 7px;font-size:14.2px;line-height:1.68;max-width:none}
.cr .who{font-family:'IBM Plex Mono',monospace;font-size:9.6px;letter-spacing:.06em;
  text-transform:uppercase;color:var(--mut)}
.srcl{font-family:'IBM Plex Mono',monospace;font-size:9.6px;letter-spacing:.06em;
  text-transform:uppercase;white-space:nowrap;margin-left:6px}
.gapl{margin:8px 0 14px;padding-left:19px}
.gapl li{font-size:14.2px;line-height:1.68;color:#4A5A46;margin-bottom:7px;max-width:66ch}
.srcs{border:1px solid var(--line);border-radius:10px;background:#fff;padding:13px 16px}
.srcs summary{cursor:pointer;font-family:'IBM Plex Mono',monospace;font-size:10.4px;
  letter-spacing:.08em;text-transform:uppercase;color:var(--pine)}
.srcs ol{margin:12px 0 0;padding-left:19px}
.srcs li{font-size:12.8px;line-height:1.55;margin-bottom:6px;overflow-wrap:anywhere}

@media (max-width:900px){
  .afwrap{grid-template-columns:minmax(0,1fr);gap:20px;padding-top:22px}
  .afnav{position:static;display:flex;gap:7px;overflow-x:auto;padding-bottom:5px}
  .afnav b{display:none}
  .afnav a{border-left:0;border:1px solid var(--line);border-radius:20px;padding:6px 12px;
    white-space:nowrap;font-size:12.3px}
  .afnav a.on{border-color:var(--pine);background:#EAF3DE}
}
@media (max-width:560px){
  .tbl .r{grid-template-columns:minmax(0,1fr);gap:5px}
  .tiers,.alts{grid-template-columns:minmax(0,1fr)}
}
</style>
<script>
(function(){
  var links=[].slice.call(document.querySelectorAll('.afnav a'));
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


def main():
    os.makedirs(OUT, exist_ok=True)
    written = [("affiliate-disclosure.html", build_disclosure()),
               ("simplepractice-california-therapists.html", build_simplepractice())]
    for fn, doc in written:
        open(os.path.join(OUT, fn), "w", encoding="utf-8").write(doc)

    bad = []
    for fn, doc in written:
        if doc.count("<h1") != 1:
            bad.append("%s: %d h1" % (fn, doc.count("<h1")))
        if ('rel="canonical" href="%s%s"' % (BASE, fn)) not in doc:
            bad.append("%s: canonical does not match its filename" % fn)
        if not re.search(r"<script>[\s\S]*?navpanel[\s\S]*?</script>", doc):
            bad.append("%s: dead header" % fn)
        if '"@type":"BreadcrumbList"' not in doc:
            bad.append("%s: no breadcrumb data" % fn)
        ids = re.findall(r'<h2 id="([^"]+)"', doc)
        nv = re.findall(r'<nav class="afnav">.*?</nav>', doc, re.S)
        if not nv or re.findall(r'href="#([^"]+)"', nv[0]) != ids:
            bad.append("%s: nav does not match its sections" % fn)
        for m in re.finditer(r'<a [^>]*href="https?://[^"]+"([^>]*)>', doc):
            if "noopener" not in m.group(1) or 'target="_blank"' not in m.group(1):
                bad.append("%s: an external link does not open safely" % fn)
                break

    # The two commitments this page set are checked, not just asserted.
    sp = dict(written)["simplepractice-california-therapists.html"]
    dis = dict(written)["affiliate-disclosure.html"]
    if "affiliate-disclosure.html" not in sp:
        bad.append("the review does not link to the disclosure")
    if "who-should-not" not in sp:
        bad.append("the review has no 'who should not buy it' section")
    # Every alternative that earns nothing must actually be on the page - the
    # cheap paths are the part a reader will check, and the part most likely to
    # be quietly dropped.
    for a in SP["alternatives"]:
        if a["name"] != "SimplePractice" and esc(a["name"]) not in sp:
            bad.append("alternative missing from the page: %s" % a["name"])
    for c in SP["criticism"]:
        if esc(c["what"])[:60] not in sp:
            bad.append("a sourced criticism did not reach the page")
            break
    for p in PARTNERS:
        if ('id="%s"' % p["slug"]) not in dis:
            bad.append("disclosure is missing partner %s" % p["slug"])
        # The tracking code must NOT be hardcoded here - _dev/affiliate.py owns
        # it, and a copy in a builder is exactly how the two drift apart.
        if p["url"] in sp:
            bad.append("the review hardcodes the affiliate URL for %s" % p["slug"])
    if bad:
        sys.exit("build_affiliates: " + "; ".join(sorted(set(bad))[:6]))

    print("2 pages · %d partners · %d tiers · %d alternatives · %d criticisms · "
          "%d sources" % (len(PARTNERS), len(SP["pricing"]["tiers"]),
                          len(SP["alternatives"]) - 1, len(SP["criticism"]),
                          len(SP["sources"])))


if __name__ == "__main__":
    main()
