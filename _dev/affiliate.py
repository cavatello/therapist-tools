#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Make the site's own claims true again, now that it carries affiliate links.

Every page footer said "Free, and not selling anything", and the home page
carried a promise block headed "Nothing saved, nothing sold" whose body ended
"there is no paid tier and nothing here is trying to sell you a service."

Those were true when written. The moment a single affiliate link ships they
stop being true, and on a site whose entire proposition is that every figure is
computed or cited, a false claim in the footer is worse than the money is
worth. So the claims are narrowed to what remains true - free to use, no
account, nothing stored - and the part that is no longer true is replaced by
the disclosure it needs.

Three commitments the new copy makes, and this pass enforces all three:

  1. The disclosure is GLOBAL. It sits in the footer of every page, because a
     reader can land on any page from search and the footer is the only thing
     every page shares.
  2. Affiliate links are MARKED AT THE LINK, not only in the footer. A footer
     disclosure that a reader has to scroll to find is the letter of the rule
     and not the point of it. Each one carries a visible tag.
  3. The disclosure says the thing that actually matters to this audience:
     an affiliate link never changes what a calculator says. That is the real
     worry, and it is the one a generic "contains affiliate links" line does
     not answer.

Idempotent, and guarded: the pass fails if any affiliate URL exists without a
marker beside it, or if any page carries the old claim.
"""
import os, re, sys

HERE = os.path.dirname(os.path.abspath(__file__))
SITE = os.path.dirname(HERE)
MARK = "/* _dev/affiliate.py */"

# THE REGISTRY LIVES IN ONE FILE, NOT IN THIS ONE.
#
# It used to be a dict here, which meant the tracking codes were buried in a
# post-pass nobody opens and there was no way to see, at a glance, which links
# on the site earn anything. mock/affiliates/partners.json is now the single
# place a partner link exists; this pass only applies it.
#
# The fallback matters. If the registry is missing - a partial checkout, a file
# not yet synced - this pass must not silently strip every affiliate link and
# leave the site pointing at bare URLs. It stops instead.
def load_partners():
    for cand in (os.path.join(SITE, "mock", "affiliates", "partners.json"),
                 os.path.join(SITE, "..", "work", "affiliates", "partners.json")):
        if os.path.exists(cand):
            import json
            d = json.load(open(cand, encoding="utf-8"))
            return [p for p in d["partners"] if p.get("active", True)], cand
    sys.exit("affiliate: no partners.json found - refusing to run, because a "
             "missing registry looks exactly like 'this site has no affiliate "
             "links' and would quietly revert every one of them")


PARTNERS, REGISTRY = load_partners()
AFFILIATE = {p["slug"]: (p["url"], p["bare"]) for p in PARTNERS}

FOOT_OLD = ("<b>Built by Cavatello.</b> Free, and not selling anything. Nothing here "
            "is legal, tax, financial or clinical advice, and using this site does not "
            "create a professional relationship &mdash; see the "
            '<a href="terms.html">Terms of Use</a>.')
FOOT_NEW = ("<b>Built by Cavatello.</b> Some links out to third-party services are affiliate links and are "
            "tagged where they appear; they cost you nothing and never change what a "
            "calculator here tells you. Nothing here is legal, tax, financial or "
            "clinical advice, and using this site does not create a professional "
            'relationship &mdash; see the <a href="terms.html">Terms of Use</a>.')

PROMISE_OLD = ('<div class="lpromise"><h3>Nothing saved, nothing sold</h3><p>No account, '
               "no email required, nothing stored on a server. Your numbers live in the "
               "page and in a link you can copy. There is no paid tier and nothing here "
               "is trying to sell you a service.</p></div>")
PROMISE_NEW = ('<div class="lpromise"><h3>How the calculators work</h3><p>The '
               "calculators run in your browser, and your numbers travel in a link you "
               "can copy. A few links out to third-party services "
               "are affiliate links, tagged where they appear &mdash; they never change "
               "what a calculator here tells you.</p></div>")

CSS = """
/* The affiliate tag. Deliberately legible rather than discreet: a disclosure
   sized to be missed is not a disclosure. Small, but at full contrast and
   immediately beside the link it describes. */
.afl{display:inline-block;font-family:'IBM Plex Mono',ui-monospace,monospace;
  font-size:9.4px;letter-spacing:.09em;text-transform:uppercase;
  background:#FBF0E2;color:#8A5B22;border:1px solid #EBD9BC;border-radius:20px;
  padding:2px 7px;margin-left:6px;vertical-align:middle;white-space:nowrap}
"""

TAG = '<span class="afl" title="Affiliate link">affiliate</span>'


SUBDIRS = ("money", "licensure", "getting-paid", "practice", "training")


def pages():
    """Root and one level down - the topic hubs carry the footer too, so a
    disclosure that skipped them would be missing from five pages."""
    out = [f for f in sorted(os.listdir(SITE)) if f.endswith(".html")]
    for d in SUBDIRS:
        p = os.path.join(SITE, d)
        if os.path.isdir(p):
            out += ["%s/%s" % (d, f) for f in sorted(os.listdir(p))
                    if f.endswith(".html")]
    return out


def main():
    foot = promise = url = tagged = relled = 0
    styled = []

    for f in pages():
        path = os.path.join(SITE, f)
        s = open(path, encoding="utf-8").read()
        before = s

        # 1. the global footer claim
        n = s.count(FOOT_OLD)
        if n:
            s = s.replace(FOOT_OLD, FOOT_NEW)
            foot += n

        # 2. the home page promise block
        if PROMISE_OLD in s:
            s = s.replace(PROMISE_OLD, PROMISE_NEW, 1)
            promise += 1

        # 3. affiliate URLs, and a tag immediately after each link that uses one
        for pr in PARTNERS:
            new = pr["url"]
            # Rewrite the canonical bare URL and any deep links alongside it.
            # A page written naturally links to simplepractice.com; the author
            # should never have to remember a tracking code.
            for old in [pr["bare"]] + list(pr.get("extra") or []):
                # Longest first, so rewriting the short form does not corrupt a
                # longer one that contains it as a prefix.
                if old and old in s and new not in (old,):
                    s = re.sub(re.escape(old) + r'(?![A-Za-z0-9/_-])', new, s)
            url += s.count(new)
            # Google asks for rel="sponsored" on any link that exists because
            # of a commercial arrangement, and nofollow alongside it. Setting it
            # here rather than in the page builders means it cannot be forgotten
            # on a page written later - the marking travels with the URL, not
            # with whoever remembered to type it.
            def fix_rel(m):
                nonlocal relled
                attrs = m.group(1)
                cur = re.search(r'rel="([^"]*)"', attrs)
                want = ["sponsored", "nofollow", "noopener", "noreferrer"]
                have = cur.group(1).split() if cur else []
                merged = " ".join(want + [h for h in have if h not in want])
                if cur and cur.group(1) == merged:
                    return m.group(0)
                relled += 1
                attrs = (re.sub(r'rel="[^"]*"', 'rel="%s"' % merged, attrs) if cur
                         else attrs + ' rel="%s"' % merged)
                if 'target=' not in attrs:
                    attrs += ' target="_blank"'
                return '<a href="' + new + '"' + attrs + ">"
            s = re.sub(r'<a href="' + re.escape(new) + r'"([^>]*)>', fix_rel, s)

            # tag every anchor pointing at the affiliate URL that is not already tagged
            def add_tag(m):
                nonlocal tagged
                if m.group(0).endswith(TAG):
                    return m.group(0)
                tagged += 1
                return m.group(0) + TAG
            s = re.sub(r'<a href="' + re.escape(new) + r'"[^>]*>(?:(?!</a>).)*</a>'
                       + r'(?:' + re.escape(TAG) + r')?', add_tag, s)

        # 4. the stylesheet, only where a tag actually landed
        s = re.sub(r"\n?<style>" + re.escape(MARK) + r"[\s\S]*?/\* end afl \*/</style>\n?",
                   "", s)
        if TAG in s:
            s = s.replace("</body>", "\n<style>" + MARK + CSS + "/* end afl */</style>\n</body>", 1)
            styled.append(f)

        if s != before:
            open(path, "w", encoding="utf-8").write(s)

    print("registry               %s" % REGISTRY)
    print("active partners        %d  (%s)"
          % (len(PARTNERS), ", ".join(p["slug"] for p in PARTNERS)))
    print("footers rewritten      %d" % foot)
    print("promise blocks         %d" % promise)
    print("affiliate URLs         %d" % url)
    print("links tagged           %d  (%s)" % (tagged, ", ".join(styled) or "none"))
    print("rel= corrected         %d" % relled)

    # ---- guards
    bad = 0
    STALE = ["not selling anything", "nothing sold", "no paid tier",
             "trying to sell you a service"]
    # The disclosure page quotes the retired claim in order to explain why it
    # was retired. That is the opposite of the failure this guard exists to
    # catch, and it is the one page where the phrase belongs.
    QUOTES_THE_OLD_CLAIM = "affiliate-disclosure.html"
    for f in pages():
        s = open(os.path.join(SITE, f), encoding="utf-8").read()
        if os.path.basename(f) != QUOTES_THE_OLD_CLAIM:
            for claim in STALE:
                if claim.lower() in s.lower():
                    print("GUARD %s: still claims %r" % (f, claim)); bad += 1
        # every page with a footer must carry the disclosure
        if "<footer" in s and "affiliate links" not in s:
            print("GUARD %s: footer without the disclosure" % f); bad += 1
        # no affiliate URL may appear untagged
        for pr in PARTNERS:
            new = pr["url"]
            # A bare URL only "survives" if it is a LINK TARGET. The same string
            # is a legitimate prefix of every citation on the review page -
            # simplepractice.com/pricing, /help, and so on - and those are
            # sources, not promotions, and must stay unaffiliated. Testing the
            # substring flagged all of them.
            for old in [pr["bare"]] + list(pr.get("extra") or []):
                if re.search(r'href="' + re.escape(old) + r'"', s):
                    print("GUARD %s: bare %s survives as a link target"
                          % (f, old)); bad += 1
            for m in re.finditer(r'<a href="' + re.escape(new) + r'"([^>]*)>(?:(?!</a>).)*</a>', s):
                after = s[m.end():m.end() + len(TAG)]
                if after != TAG:
                    print("GUARD %s: affiliate link without a tag" % f); bad += 1
                rel = re.search(r'rel="([^"]*)"', m.group(1))
                missing = [r for r in ("sponsored", "nofollow", "noopener")
                           if not rel or r not in rel.group(1).split()]
                if missing:
                    print("GUARD %s: affiliate link missing rel=%s"
                          % (f, ",".join(missing))); bad += 1
            if new in s and TAG not in s:
                print("GUARD %s: affiliate url present, no tag anywhere" % f); bad += 1
            if TAG in s and s.count(MARK) != 1:
                print("GUARD %s: tag present, %d stylesheets" % (f, s.count(MARK))); bad += 1
        if s.count("<h1") != 1 and f not in ("privacy.html", "terms.html", "tools.html"):
            print("GUARD %s: %d h1" % (f, s.count("<h1"))); bad += 1
    if bad:
        sys.exit("affiliate: %d guard failure(s)" % bad)
    print("guards clean")


if __name__ == "__main__":
    main()
