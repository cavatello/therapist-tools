#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Concept 05 - the 78 programs as two objects, not one.

THE PROBLEM THE TWO VIEWS SOLVE

The directory answers one question well: "does this specific program qualify?"
Type a name, filter on COAMFTE, read the row. It answers the other question -
"what are my options?" - badly, because a filterable list of 78 rows shows you
the field only after you have already decided how to narrow it. A reader who
does not yet know that Loma Linda and La Sierra are twenty minutes apart cannot
filter their way to that.

Kitces hit this exactly with the AdvisorTech Map and says so outright: the map
grew until it defeated its own purpose. His fix was to add a filterable
directory WITHOUT DELETING THE MAP - because the two views answer different
questions and neither is a better version of the other. Same here, in reverse:
this site already has the lookup, so what it needs is the orientation.

  Compare - what are my options?   grouped by where the campuses actually are
  Find - does this one qualify?    the existing filters, search, table and print

WHY THE PANES ARE SWITCHED IN CSS AND NOT BY MOVING MARKUP

The lookup view is `.flt`, `.az`, `.grid` and `.tblwrap`, and it carries a
search box, eight filter buttons, a keep-list, a print handler, a card/table
toggle and an A-Z jump nav - all wired to script that finds them by id. Wrapping
that in a new container to hide it is a restructuring edit on the most
script-heavy page on the site, for a purely visual outcome.

So nothing existing is wrapped or moved. A `data-tv` attribute on <html> drives
`display:none`, the new markup is inserted between existing siblings, and every
handler on the page keeps the DOM it was written against.

A SCHOOL APPEARS IN EVERY METRO IT HAS A CAMPUS IN

Several run three or four campuses. Filing each under one "primary" metro would
be a guess, and would hide a San Diego campus from a San Diego reader - the
exact failure the orientation view exists to prevent. So the group counts are
labelled "programs with a campus here" and deliberately sum to more than 78.

Idempotent, delimited, guarded. Run before restyle.py.
"""
import os, re, sys, json, html, unicodedata

HERE = os.path.dirname(os.path.abspath(__file__))
SITE = os.path.dirname(HERE)
DATA = os.path.join(SITE, "mock", "mftguide", "programs.json")
PAGE = os.path.join(SITE, "mft-programs-california.html")

MARK = "<!-- _dev/dir_two_views.py -->"
END = "<!-- /dir_two_views -->"
CSSMARK = "/* _dev/dir_two_views.py */"

# Which view opens. The concept's own answer was "compare" - orientation before
# filtering, the Kitces AdvisorTech Map pattern - and it shipped that way for a
# day. The owner looked at it and did not want it: someone arriving at a school
# directory usually arrives with a school in mind, and making them dismiss an
# overview to reach the filters is a step for the reader who needs it least.
# The comparison view is still there behind its tab; it just no longer opens.
DEFAULT_VIEW = "find"

SHOWN_PER_GROUP = 6

# City strings in programs.json are free text written for a human ("San Diego,
# Irvine, Los Angeles/Alhambra, Sacramento, Online"), so the metro is matched on
# substrings rather than parsed. Order is only for readability; a school is
# tested against every bucket, not the first that hits.
METROS = [
    ("Greater Los Angeles", [
        "los angeles", "northridge", "pasadena", "culver city", "long beach",
        "carson", "la mirada", "rosemead", "san dimas", "pomona", "azusa",
        "calabasas", "thousand oaks", "la verne", "alhambra", "west los angeles",
        "malibu"]),
    ("Orange County & the Inland Empire", [
        "anaheim", "irvine", "orange", "fullerton", "brea", "costa mesa",
        "tustin", "los alamitos", "riverside", "san bernardino", "redlands",
        "loma linda", "inland empire"]),
    ("San Diego", ["san diego", "el cajon", "la mesa"]),
    ("San Francisco Bay", [
        "san francisco", "berkeley", "palo alto", "san jose", "santa clara",
        "belmont", "hayward", "moraga", "richmond", "san rafael", "petaluma",
        "rohnert park", "san mateo", "oakland"]),
    ("Central Valley & Sacramento", [
        "fresno", "bakersfield", "stockton", "turlock", "sacramento",
        "rocklin", "lathrop", "merced", "modesto"]),
    ("Central Coast & the North", [
        "santa barbara", "carpinteria", "san luis obispo", "arcata", "chico",
        "redding", "weimar", "monterey", "humboldt"]),
]
ONLINE = "Online, hybrid or out of state"


def esc(x):
    return html.escape(str(x), quote=False)


def hrefs_from(doc):
    """{normalised institution name: href or None}, read off the directory.

    Twelve institutions have no page yet - they came in with the Board's list
    and nothing has been written about them - so the value is None and the
    orientation view prints the name without a link. A name that goes nowhere
    is honest; a link that 404s is not.
    """
    out = {}
    for art in re.findall(r'<article class="pg"[\s\S]*?</article>', doc):
        h3 = re.search(r"<h3>(.*?)</h3>", art)
        if not h3:
            continue
        link = re.search(r'href="([a-z0-9-]+-mft\.html)"', art)
        out[norm(h3.group(1))] = link.group(1) if link else None
    return out


def norm(name):
    """Match the directory's display name to programs.json's institution field.

    They differ in punctuation and parenthetical suffixes - "California State
    University, Fresno (Fresno State)" against "California State University,
    Fresno" - so both sides are reduced to letters and digits and the
    parenthetical is dropped.
    """
    n = unicodedata.normalize("NFKD", str(name)).encode("ascii", "ignore").decode()
    # Numeric entities too. The directory writes an apostrophe as &#x27;
    # and an alpha-only pattern left the "x27" behind, so "Saint Mary's
    # College" and "Saint Marys College" did not match.
    n = re.sub(r"&(?:[a-z]+|#\d+|#x[0-9a-fA-F]+);", " ", n)
    n = re.sub(r"\([^)]*\)", " ", n)
    return re.sub(r"[^a-z0-9]+", "", n.lower())


def metros_of(p):
    city = (p.get("city") or "").lower()
    hits = [name for name, keys in METROS if any(k in city for k in keys)]
    if not hits:
        hits = [ONLINE]
    elif "online" in city or "hybrid" in city:
        hits = hits + [ONLINE]
    return hits


CSS = """<style>%s
/* Concept 05. The two views are switched by an attribute on <html>, so no
   existing element is wrapped or moved and every handler on the page keeps the
   DOM it was written against. */
html[data-tv="compare"] .flt,
html[data-tv="compare"] .az,
html[data-tv="compare"] .grid,
html[data-tv="compare"] .tblwrap{display:none !important}
html[data-tv="find"] .tvcompare{display:none !important}

.tvtabs{display:flex;flex-wrap:wrap;gap:9px;margin:26px 0 4px}
.tvtabs button{font-family:'IBM Plex Mono',ui-monospace,monospace;font-size:11px;
  font-weight:700;letter-spacing:.05em;text-transform:uppercase;color:#16211B;
  background:#fff;border:2px solid #16211B;border-radius:999px;
  padding:9px 16px 8px;box-shadow:2px 2px 0 #16211B;cursor:pointer}
.tvtabs button[aria-pressed="true"]{background:#F6C560;box-shadow:3px 3px 0 #16211B}
.tvtabs button:active{transform:translate(2px,2px);box-shadow:0 0 0 #16211B}
.tvnote{font-size:13.4px;line-height:1.6;color:#5A5647;margin:0 0 16px;max-width:70ch}
.pdxlink{font-size:14px;line-height:1.62;color:#3A3529;margin:22px 0 0;max-width:74ch;
  border-left:3px solid #16211B;padding-left:14px}
.pdxlink a{color:#2C6350}

.rgroups{display:grid;grid-template-columns:repeat(auto-fit,minmax(272px,1fr));
  gap:13px;margin:0 0 22px}
.rgroup{border:2px solid #16211B;border-radius:12px;box-shadow:3px 3px 0 #16211B;
  background:#FBF9F3;overflow:hidden}
.rghd{display:flex;align-items:baseline;justify-content:space-between;gap:10px;
  padding:11px 14px 10px;background:#F0EADA;border-bottom:2px solid #16211B}
.rghd b{font-family:'Bricolage Grotesque','Archivo',Inter,system-ui,sans-serif;
  font-weight:800;letter-spacing:-.028em;font-size:15.5px;color:#16211B}
.rghd i{font-family:'IBM Plex Mono',ui-monospace,monospace;font-style:normal;
  font-size:10px;letter-spacing:.06em;color:#6C6555;white-space:nowrap}
.rgbody{padding:9px 14px 12px}
.rgbody a{display:block;font-size:13.6px;line-height:1.4;color:#16211B;
  text-decoration:none;padding:6px 0;border-bottom:1px dashed #E4DCC8}
.rgbody .rgna{display:block;font-size:13.6px;line-height:1.4;color:#6C6555;
  padding:6px 0;border-bottom:1px dashed #E4DCC8}
.rgbody a:last-of-type,.rgbody .rgna:last-of-type{border-bottom:none}
.rgbody .rgna em{margin-left:6px}
.rgbody a:hover{color:#2C6350}
.rgbody a em,.rgbody .rgna em{font-style:normal;font-family:'IBM Plex Mono',ui-monospace,monospace;
  font-size:9px;font-weight:700;letter-spacing:.08em;color:#16211B;
  background:#CFE3D6;border:1.5px solid #16211B;border-radius:999px;
  padding:2px 6px 1px;margin-left:6px;white-space:nowrap}
.rgmore{display:inline-block;margin:9px 0 0;font-family:'IBM Plex Mono',
  ui-monospace,monospace;font-size:10.4px;font-weight:700;letter-spacing:.06em;
  text-transform:uppercase;color:#2C6350;background:none;border:none;
  cursor:pointer;padding:0}
.rgmore:hover{text-decoration:underline}

/* Centred on the page's own measure. Inserted as a bare sibling of the
   directory, so it has no container to inherit a gutter from - exactly the
   mistake that made the "More on this" block run full-bleed while the footer
   under it sat in a centred column. Same width as the up-link, so the two
   blocks that sit next to each other line up. */
.fixrow{display:grid;grid-template-columns:minmax(0,1fr) auto;gap:14px;
  align-items:center;border:2px solid #16211B;border-radius:12px;
  background:#F4F0E6;box-shadow:3px 3px 0 #16211B;padding:14px 16px;
  max-width:1120px;margin:28px auto 8px;box-sizing:border-box}
@media (min-width:1500px){.fixrow{max-width:1320px}}
@media (min-width:1900px){.fixrow{max-width:1560px}}
.fixrow b{display:block;font-family:'Bricolage Grotesque','Archivo',Inter,
  system-ui,sans-serif;font-weight:800;letter-spacing:-.028em;font-size:16px;
  color:#16211B}
.fixrow i{display:block;font-style:normal;font-size:13px;line-height:1.55;
  color:#4A463A;margin:4px 0 0;max-width:70ch}
.fixbtn{font-family:'IBM Plex Mono',ui-monospace,monospace;font-size:10.6px;
  font-weight:700;letter-spacing:.07em;text-transform:uppercase;color:#16211B;
  background:#F6C560;border:2px solid #16211B;border-radius:999px;
  padding:9px 15px 8px;box-shadow:2px 2px 0 #16211B;text-decoration:none;
  white-space:nowrap}
.fixbtn:active{transform:translate(2px,2px);box-shadow:0 0 0 #16211B}
@media (max-width:600px){
  .fixrow{grid-template-columns:minmax(0,1fr)}
  .tvtabs button{font-size:10px;padding:8px 12px 7px}
}
</style>""" % CSSMARK

JS = """<script>%s
(function(){
  var root = document.documentElement;
  var tabs = document.querySelectorAll('.tvtabs button');
  if(!tabs.length) return;
  function set(v){
    root.setAttribute('data-tv', v);
    for(var i=0;i<tabs.length;i++){
      tabs[i].setAttribute('aria-pressed',
        tabs[i].getAttribute('data-v') === v ? 'true' : 'false');
    }
  }
  for(var i=0;i<tabs.length;i++){
    tabs[i].addEventListener('click', function(e){
      set(e.currentTarget.getAttribute('data-v'));
    });
  }
  // A link can open the lookup directly. Anyone sending someone "the filter for
  // COAMFTE programmes" needs a URL that lands on the filters, not on the
  // orientation view with the filters hidden.
  if(location.hash === '#find' || location.hash === '#compare'){
    set(location.hash.slice(1));
  }
  // Reveal the rest of a metro in place. Expanding beats navigating: the reader
  // is comparing, and a page change loses the comparison.
  var more = document.querySelectorAll('.rgmore');
  for(var j=0;j<more.length;j++){
    more[j].addEventListener('click', function(e){
      var b = e.currentTarget;
      var box = b.parentNode;
      var hidden = box.querySelectorAll('a[hidden],span[hidden]');
      for(var k=0;k<hidden.length;k++){ hidden[k].hidden = false; }
      b.parentNode.removeChild(b);
    });
  }
})();
</script>""" % CSSMARK.replace("/*", "//").replace("*/", "")


def main():
    if not os.path.exists(PAGE):
        sys.exit("dir_two_views: %s missing" % PAGE)
    progs = json.load(open(DATA, encoding="utf-8"))
    page0 = open(PAGE, encoding="utf-8").read()
    LINKS = hrefs_from(page0)
    unmatched = [p["institution"] for p in progs
                 if norm(p["institution"]) not in LINKS]
    if unmatched:
        print("  %d name(s) not matched to a directory row: %s"
              % (len(unmatched), ", ".join(unmatched[:4])))

    buckets = {}
    for p in progs:
        for m in metros_of(p):
            buckets.setdefault(m, []).append(p)

    order = [n for n, _k in METROS] + [ONLINE]
    groups = []
    for name in order:
        rows = sorted(buckets.get(name, []), key=lambda p: p["institution"])
        if not rows:
            continue
        # COAMFTE first, then alphabetical - accreditation is the one thing a
        # reader scanning for orientation is most likely to be sorting on, and
        # it is a fact rather than a ranking.
        rows.sort(key=lambda p: (not p.get("coamfte"), p["institution"]))
        items = []
        for i, p in enumerate(rows):
            tag = "<em>COAMFTE</em>" if p.get("coamfte") else ""
            hide = "" if i < SHOWN_PER_GROUP else " hidden"
            href = LINKS.get(norm(p["institution"]))
            if href:
                items.append('<a href="%s"%s>%s%s</a>'
                             % (esc(href), hide, esc(p["institution"]), tag))
            else:
                # On the Board's list, nothing written about it here yet. Named
                # anyway - a reader comparing options needs to know it exists.
                items.append('<span class="rgna"%s>%s%s</span>'
                             % (hide, esc(p["institution"]), tag))
        more = ""
        if len(rows) > SHOWN_PER_GROUP:
            more = ('<button type="button" class="rgmore">+%d more</button>'
                    % (len(rows) - SHOWN_PER_GROUP))
        groups.append(
            '<div class="rgroup"><div class="rghd"><b>%s</b><i>%d program%s</i>'
            '</div><div class="rgbody">%s%s</div></div>'
            % (esc(name), len(rows), "" if len(rows) == 1 else "s",
               "".join(items), more))

    tabs = ('<div class="tvtabs" role="group" aria-label="How to browse the '
            'programs"><button type="button" data-v="compare" '
            'aria-pressed="%s">Compare &mdash; what are my options?</button>'
            '<button type="button" data-v="find" aria-pressed="%s">'
            "Find &mdash; does this one qualify?</button></div>"
            % ("true" if DEFAULT_VIEW == "compare" else "false",
               "true" if DEFAULT_VIEW == "find" else "false"))

    compare = ('<div class="tvcompare"><p class="tvnote">Orientation view: every '
               "program with a campus in each part of the state, accredited ones "
               "first. A school running several campuses appears under each of "
               "them, so these counts add up to more than 78. Switch to "
               "<b>Find</b> for the search, the filters and the printable "
               'shortlist.</p><div class="rgroups">%s</div></div>'
               % "".join(groups))

    fix = ('<div class="fixrow"><div><b>Something wrong on a row?</b>'
           "<i>Fees move, programs close, accreditation lapses and a unit count "
           "changes with a catalog. This page is maintained by one person and "
           "stays accurate because readers report what has drifted &mdash; tell "
           "me which school and what changed, and the correction goes on the "
           'page with the date it landed.</i></div>'
           '<a class="fixbtn" href="contact.html">Report a change</a></div>')

    s = open(PAGE, encoding="utf-8").read()
    orig = s
    s = re.sub(re.escape(MARK) + r"[\s\S]*?" + re.escape(END), "", s)
    s = re.sub(r"\n?<style>" + re.escape(CSSMARK) + r"[\s\S]*?</style>\n?", "", s)
    s = re.sub(r"\n?<script>// _dev/dir_two_views\.py[\s\S]*?</script>\n?", "", s)

    # The doctorate cross-link. It lives INSIDE the marked region on purpose:
    # the first attempt inserted it just before the tabs as a separate edit,
    # which put it between MARK and the tabs - so the next run of this pass
    # stripped MARK..END and took the cross-link with it. Anything that has to
    # survive this pass has to be emitted BY this pass.
    xlink = ('<p class="pdxlink">Looking for a doctorate instead? The MFT and '
             "LPCC routes are master&rsquo;s level and run through the Board of "
             "Behavioral Sciences. Doctorates in psychology are a different "
             "licence, a different board and a different accreditation regime "
             "&mdash; <a href=\"psyd-programs-california.html\">every PsyD in "
             "California is here</a>.</p>")

    i = s.find('<div class="flt">')
    if i < 0:
        sys.exit("dir_two_views: could not find the filter bar")
    s = s[:i] + MARK + xlink + tabs + compare + END + s[i:]

    # the correction row goes after the whole lookup, before the next section
    j = s.find('<div class="grid">')
    k = s.find("<section", j)
    if k < 0:
        k = s.find("<footer", j)
    s = s[:k] + MARK + fix + END + s[k:]

    # the view attribute, so the first paint is already correct and nothing
    # flashes the wrong pane before the script runs.
    #
    # This used to leave an existing data-tv alone, which made it write-once:
    # changing DEFAULT_VIEW and re-running printed "guards clean" and changed
    # nothing, because the attribute the guard checks was already there. It now
    # REPLACES the value, so the constant at the top of this file is the single
    # source of truth for which pane opens.
    s = re.sub(r'\sdata-tv="[a-z]+"', "", s, count=1)
    s = re.sub(r"<html\b[^>]*>",
               lambda m: m.group(0)[:-1] + ' data-tv="%s">' % DEFAULT_VIEW,
               s, count=1)

    n = s.lower().rfind("</body>")
    s = s[:n] + CSS + "\n" + JS + "\n" + s[n:]

    if s != orig:
        open(PAGE, "w", encoding="utf-8").write(s)

    print("%d metro group(s), %d program row(s) across them"
          % (len(groups), sum(len(v) for v in buckets.values())))
    for name in order:
        if buckets.get(name):
            print("  %-36s %3d" % (name, len(buckets[name])))

    # ---- guards
    bad = 0
    s = open(PAGE, encoding="utf-8").read()
    if s.count(MARK) != 2 or s.count(END) != 2:
        print("GUARD: %d marks / %d ends" % (s.count(MARK), s.count(END)))
        bad += 1
    if 'data-tv="' not in s.split(">", 1)[0] and "data-tv" not in s[:2000]:
        print("GUARD: <html> has no data-tv, the first paint will show both views")
        bad += 1
    # every school named in the orientation view must have a page
    for href in set(re.findall(r'<a href="([a-z0-9-]+-mft\.html)"', s)):
        if not os.path.exists(os.path.join(SITE, href)):
            print("GUARD: links %s which does not exist" % href)
            bad += 1
    # nobody may fall out of the grouping
    placed = set()
    for v in buckets.values():
        placed |= {p["institution"] for p in v}
    missing = {p["institution"] for p in progs} - placed
    if missing:
        print("GUARD: %d school(s) in no group: %s"
              % (len(missing), ", ".join(sorted(missing))))
        bad += 1
    if bad:
        sys.exit("\n%d problem(s)" % bad)
    print("guards clean")


if __name__ == "__main__":
    main()
