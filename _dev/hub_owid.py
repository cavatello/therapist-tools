#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Concept 04 - the five topic hubs on the Our World in Data template.

THE SEQUENCE, AND WHY IT IS THIS ONE

  scope line -> most asked -> key insights -> the calculator -> reading -> cite

Our World in Data runs exactly this order on all 126 of its topic pages and
states the rationale: Shneiderman's "overview first, zoom and filter, then
details-on-demand". The hubs already had the reading and the tools. What they
did not have was an OVERVIEW - a reader landing on /money/ from search met two
paragraphs of intro and then a wall of cards, with no way to find out what this
topic actually says without opening six pages.

WHERE EVERY WORD COMES FROM

Nothing here is written by this pass. Every field is read out of
mock/library/registry.json, which the site already maintains:

  scope       the topic's cluster names, joined. "Includes entity choice,
              self-employment tax, retirement accounts and deductions" is
              literally the list of sections further down the page.
  most asked  the three highest-WEIGHT pages in the topic, shown by their
              `question` - the phrasing a reader would actually type.
  insights    the three highest-weight pages that carry a `number`. The claim
              IS the number field ("$18,244 optional on a $217,350 profit"),
              the elaboration is the `outcome` field, and the figure is the
              leading token of the number.
  calculator  the topic's highest-weight page whose format is `calculator`.

"MOST ASKED", NOT "MOST VIEWED"

Our World in Data prints most-viewed because it has years of analytics. This
site's analytics property was installed today and has no history at all, so a
"most viewed" strip would be a fabrication dressed as a measurement. Weight is a
real editorial field that already orders the library, and "most asked" is what
it honestly means. Revisit this once GA has a quarter of data.

THE "WHAT YOU SHOULD KNOW" BOX IS THE POINT

It is what lets the headline stay a clean claim. A figure with its conditions
stapled to the front of it reads as hedging; the same figure with a disclosure
one click below reads as confident and checkable. The conditions here are real:
which page computes it, on what rate year, and that the reader's own number
will differ.

Idempotent, delimited, guarded. Run before restyle.py.
"""
import os, re, sys, json, html

HERE = os.path.dirname(os.path.abspath(__file__))
SITE = os.path.dirname(HERE)
REGISTRY = os.path.join(SITE, "mock", "library", "registry.json")

MARK = "<!-- _dev/hub_owid.py -->"
END = "<!-- /hub_owid -->"
CSSMARK = "/* _dev/hub_owid.py */"
CHECKED = "8 August 2026"
BASE = "therapistsupport.org"

HUBS = ("money", "licensure", "getting-paid", "practice", "training")

# What the figures on each topic are conditioned on. Stated per topic because
# it differs, and a single generic sentence would be wrong for four of them.
BASIS = {
    "money": "2026 federal and California rates, for a California resident, "
             "with no other household income",
    "licensure": "the Board's published fee schedule and the statute sections "
                 "linked on the page",
    "getting-paid": "the 2026 Medicare and Medi-Cal fee schedules and the "
                    "platforms' own published terms",
    "practice": "the vendors' own published pricing and the 2026 California "
                "payroll rates",
    "training": "what each institution publishes about itself",
}

CSS = """<style>%s
/* Concept 04. Pixel language: 2px ink, solid offset shadow, never a blur.
   Fraunces is reserved for figures and appears here only inside .insf. */
.hscope{font-size:15px;line-height:1.6;color:#3A3529;margin:14px 0 0;max-width:66ch}
.hscope b{font-weight:600}
.hmost{display:flex;flex-wrap:wrap;align-items:center;gap:8px 10px;margin:16px 0 0}
.hmost .mvk{font-family:'IBM Plex Mono',ui-monospace,monospace;font-size:9.4px;
  letter-spacing:.13em;text-transform:uppercase;color:#6C6555}
.hmost a{font-size:13px;color:#16211B;text-decoration:none;background:#fff;
  border:2px solid #16211B;border-radius:999px;padding:5px 12px 4px;
  box-shadow:2px 2px 0 #16211B}
.hmost a:hover{background:#F6C560}
.hmost a:active{transform:translate(2px,2px);box-shadow:0 0 0 #16211B}
.hsec{font-family:'Bricolage Grotesque','Archivo',Inter,system-ui,sans-serif;
  font-weight:800;letter-spacing:-.032em;font-size:23px;color:#16211B;
  margin:34px 0 14px}
.ins{border:2px solid #16211B;border-radius:12px;box-shadow:3px 3px 0 #16211B;
  background:#FBF9F3;padding:15px 17px;margin:0 0 12px}
.ins>h3{font-family:'Bricolage Grotesque','Archivo',Inter,system-ui,sans-serif;
  font-weight:800;letter-spacing:-.028em;font-size:18px;line-height:1.2;
  color:#16211B;margin:0 0 9px}
.insg{display:grid;grid-template-columns:minmax(0,1fr) auto;gap:16px;
  align-items:start}
.insg>p{margin:0;font-size:14px;line-height:1.6;color:#3A3529;max-width:60ch}
.insf{border:2px solid #16211B;border-radius:10px;background:#fff;
  box-shadow:2px 2px 0 #16211B;padding:9px 13px;text-align:right;min-width:132px}
.insf b{display:block;font-family:Fraunces,Georgia,serif;font-weight:600;
  font-size:21px;line-height:1.1;color:#2C6350;letter-spacing:-.01em}
.insf span{display:block;font-size:11.4px;line-height:1.4;color:#5A5647;
  margin:4px 0 0}
.ysk{margin:11px 0 0;border-top:2px dashed #D9D0BA;padding:9px 0 0}
.ysk>summary{cursor:pointer;list-style:none;font-family:'IBM Plex Mono',
  ui-monospace,monospace;font-size:10px;letter-spacing:.09em;
  text-transform:uppercase;color:#2C6350;font-weight:700}
.ysk>summary::-webkit-details-marker{display:none}
.ysk>summary::after{content:" +"}
.ysk[open]>summary::after{content:" \\2212"}
.ysk p{margin:8px 0 0;font-size:13px;line-height:1.6;color:#4A463A;max-width:64ch}
.hcalc{display:grid;grid-template-columns:auto minmax(0,1fr) auto;gap:14px;
  align-items:center;border:2px solid #16211B;border-radius:12px;
  box-shadow:4px 4px 0 #F6C560;background:#fff;padding:14px 16px;
  text-decoration:none;color:#16211B}
.hcalc:active{transform:translate(3px,3px);box-shadow:1px 1px 0 #F6C560}
.hcalc b{display:block;font-family:'Bricolage Grotesque','Archivo',Inter,
  system-ui,sans-serif;font-weight:800;letter-spacing:-.028em;font-size:17px}
.hcalc i{display:block;font-style:normal;font-size:13px;color:#4A463A;margin:2px 0 0}
.hcalc .ci{font-family:'IBM Plex Mono',ui-monospace,monospace;font-size:9.4px;
  letter-spacing:.12em;text-transform:uppercase;color:#6C6555;
  writing-mode:vertical-rl;transform:rotate(180deg)}
.hgo{font-family:'IBM Plex Mono',ui-monospace,monospace;font-size:10.4px;
  font-weight:700;letter-spacing:.08em;text-transform:uppercase;color:#16211B;
  background:#F6C560;border:2px solid #16211B;border-radius:999px;
  padding:6px 13px 5px;box-shadow:2px 2px 0 #16211B;white-space:nowrap}
.citeb{border:2px solid #16211B;border-radius:12px;background:#F4F0E6;
  box-shadow:2px 2px 0 #16211B;padding:14px 16px;margin:34px 0 0}
.citeb .mvk{display:block;font-family:'IBM Plex Mono',ui-monospace,monospace;
  font-size:9.4px;letter-spacing:.13em;text-transform:uppercase;color:#6C6555;
  margin:0 0 7px}
.citeb code{display:block;font-family:'IBM Plex Mono',ui-monospace,monospace;
  font-size:12.2px;line-height:1.6;color:#16211B;background:#fff;
  border:2px solid #D9D0BA;border-radius:8px;padding:9px 11px;white-space:normal;
  word-break:break-word}
.citeb p{margin:9px 0 0;font-size:12.6px;line-height:1.6;color:#4A463A;max-width:66ch}
@media (max-width:620px){
  .insg{grid-template-columns:minmax(0,1fr)}
  .insf{text-align:left;min-width:0}
  .hcalc{grid-template-columns:minmax(0,1fr)}
  .hcalc .ci{display:none}
  .hsec{font-size:20px}
}
</style>""" % CSSMARK


def esc(x):
    return html.escape(str(x), quote=False)


def raw(x):
    return str(x).replace("<", "&lt;").replace(">", "&gt;")


def lead(number):
    """The figure itself, split off from the sentence around it.

    "$18,244 optional on a $217,350 profit" -> ("$18,244", "optional on a
    $217,350 profit"). A money token if there is one, else the first word,
    because "12 expense categories" and "§17701.04(e)" are both legitimate
    headline figures and neither starts with a dollar sign.
    """
    m = re.match(r"(\$[\d,]+(?:\.\d+)?|\d[\d,]*(?:\.\d+)?%?|§[\w.()]+)\s*(.*)",
                 number.strip())
    if m:
        return m.group(1), m.group(2)
    parts = number.split(None, 1)
    return parts[0], (parts[1] if len(parts) > 1 else "")


def main():
    reg = json.load(open(REGISTRY, encoding="utf-8"))
    topics, pages = reg["topics"], reg["pages"]

    done = 0
    for key in HUBS:
        path = os.path.join(SITE, key, "index.html")
        if not os.path.exists(path):
            print("  missing: %s" % path)
            continue
        t = topics[key]
        mine = [p for p in pages
                if p.get("topic") == key and not p.get("skip")]
        mine.sort(key=lambda p: (-(p.get("weight") or 0), p["file"]))

        s = open(path, encoding="utf-8").read()
        orig = s
        s = re.sub(re.escape(MARK) + r"[\s\S]*?" + re.escape(END), "", s)
        s = re.sub(r"\n?<style>" + re.escape(CSSMARK) + r"[\s\S]*?</style>\n?",
                   "", s)

        # ---- scope line, from the section names further down the page
        names = [c["name"] for c in t.get("clusters", []) if c.get("name")]
        scope = ""
        if names:
            scope = ('<p class="hscope">%d pages, in %d sections: %s. Every '
                     "figure below is computed or cited, and links to the page "
                     "that carries it.</p>"
                     % (len(mine), len(names),
                        " &middot; ".join("<b>%s</b>" % raw(n) for n in names)))

        # ---- most asked
        asked = [p for p in mine if p.get("question")][:3]
        most = ""
        if asked:
            most = ('<div class="hmost"><span class="mvk">Most asked</span>%s'
                    "</div>"
                    % "".join('<a href="../%s">%s</a>'
                              % (esc(p["file"]), raw(p["question"]))
                              for p in asked))

        # ---- key insights
        def figrank(p):
            """A dollar amount is a finding. A bare count usually is not.

            "$18,244 optional on a $217,350 profit" and "39 cents on the
            dollar" are claims about the world; "12 expense categories" is a
            description of a form. Both are legitimate headline numbers on
            their own pages - only one belongs at the top of a topic hub.
            """
            n = (p.get("number") or "").strip()
            if n.startswith("$"):
                order = 0
            elif "%" in n[:6] or "cents" in n.lower():
                order = 1
            elif n.startswith("\u00a7"):
                order = 2
            elif re.match(r"^\d", n):
                order = 3
            else:
                order = 4
            return (order, -(p.get("weight") or 0), p["file"])

        figs = sorted([p for p in mine if p.get("number")], key=figrank)[:3]
        ins = ""
        if figs:
            cards = []
            for p in figs:
                big, rest = lead(p["number"])
                cards.append(
                    '<div class="ins"><h3>%s</h3><div class="insg"><p>%s</p>'
                    '<div class="insf"><b>%s</b><span>%s</span></div></div>'
                    '<details class="ysk"><summary>What you should know about '
                    "this figure</summary><p>This figure comes from "
                    '<a href="../%s">%s</a>, on %s. Your own number will '
                    "differ &mdash; the page shows the working and, where "
                    "there is a calculator, runs it on your figures.</p>"
                    "</details></div>"
                    % (raw(p["number"]), raw(p.get("outcome") or ""),
                       esc(big), esc(rest or "on this page's own example"),
                       esc(p["file"]), raw(p.get("question") or p["file"]),
                       esc(BASIS.get(key, "the sources linked on the page"))))
            ins = '<h2 class="hsec">Key insights</h2>' + "".join(cards)

        # ---- the calculator
        calc = ""
        tool = next((p for p in mine if p.get("format") == "calculator"), None)
        if tool:
            calc = ('<h2 class="hsec">Run it on your own numbers</h2>'
                    '<a class="hcalc" href="../%s"><span class="ci">Tool</span>'
                    "<div><b>%s</b><i>%s</i></div>"
                    '<span class="hgo">Open the calculator &rarr;</span></a>'
                    % (esc(tool["file"]),
                       raw(tool.get("question") or tool["file"]),
                       raw(tool.get("outcome") or "")))

        block = MARK + scope + most + ins + calc + END

        # goes between the intro prose and the first block of cards, which is
        # where "overview first" puts it
        m = re.search(r'<section class="intro">[\s\S]*?</section>', s)
        if m:
            s = s[:m.end()] + block + s[m.end():]
        else:
            m = re.search(r'<div class="libwrap">', s)
            if not m:
                print("  no anchor: %s" % path)
                continue
            s = s[:m.end()] + block + s[m.end():]

        # ---- cite, at the foot of the hub
        cite = (MARK
                + '<div class="citeb"><span class="mvk">Cite this page</span>'
                "<code>Therapist Support, &ldquo;%s&rdquo;, checked %s, "
                "%s/%s/</code><p>Free to reuse with attribution. If you are a "
                "program or a professional association linking to a figure, "
                "link to the page that carries it rather than copying the "
                "number &mdash; it will change.</p></div>"
                % (esc(t["name"]), CHECKED, BASE, key)
                + END)
        k = s.find("<footer")
        if k > 0:
            s = s[:k] + cite + s[k:]

        i = s.lower().rfind("</body>")
        s = s[:i] + CSS + "\n" + s[i:]

        if s != orig:
            open(path, "w", encoding="utf-8").write(s)
            done += 1
            print("  %s/  scope=%s most=%d insights=%d calc=%s"
                  % (key, bool(scope), len(asked), len(figs), bool(calc)))

    print("%d hub(s) rebuilt" % done)

    bad = 0
    for key in HUBS:
        p = os.path.join(SITE, key, "index.html")
        if not os.path.exists(p):
            continue
        s = open(p, encoding="utf-8").read()
        if s.count(MARK) != 2 or s.count(END) != 2:
            print("GUARD %s: %d marks / %d ends" % (key, s.count(MARK), s.count(END)))
            bad += 1
        if 'class="ins"' not in s:
            print("GUARD %s: no key insights" % key)
            bad += 1
        if 'class="citeb"' not in s:
            print("GUARD %s: no citation block" % key)
            bad += 1
        # Every link this pass emits must resolve. The hub sits one level down,
        # so a bare relative href would point at a sibling inside money/ rather
        # than at the site root - the exact bug that shipped 39 dead links out
        # of build_library.py. Checked here rather than trusted.
        for href in set(re.findall(r'href="\.\./([a-z0-9-]+\.html)"', s)):
            if not os.path.exists(os.path.join(SITE, href)):
                print("GUARD %s: links ../%s which does not exist" % (key, href))
                bad += 1
    if bad:
        sys.exit("\n%d problem(s)" % bad)
    print("guards clean")


if __name__ == "__main__":
    main()
