#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Wire the liability-insurance page into the site, and record what we found
about affiliate programs on the disclosure page.

TWO EDITS, BOTH SMALL, BOTH IN FILES OTHER PASSES OWN.

**1. The nav.** `_dev/restyle.py` builds the seven-group topic panel from data
lists at the top of the file. The insurance page belongs under **Practice** —
it is about running the business, not about being paid, and putting it under
"Getting paid" would file it next to the payer comparisons it is not.

**2. The disclosure page.** This is the more interesting edit, and it is the
reason this pass exists rather than being a line in the builder.

The research question was "which of these insurers pay referral commissions."
The answer, verified across every carrier and every major affiliate network, is
**none of them**. CPH, HPSO, The Trust, Berxi, Proliability, CM&F, American
Professional Agency and Lockton Affinity all work through association
endorsements negotiated one-off with professional bodies; not one runs a public
publisher program. Impact, CJ, ShareASale, PartnerStack, Awin, FlexOffers and
Refersion between them list no healthcare-professional malpractice carrier at
all.

A disclosure page that only lists what you ARE paid says less than one that also
says where you looked and found nothing. `affiliate-disclosure.html` already
promises that the list is generated from a single file "so a link cannot exist
on the site without appearing on this page" — the natural completion of that
promise is to say what was checked and came back empty.

There is a second reason to write it down rather than quietly move on. Even if
one of them HAD offered, California insurance licensing law is an unresolved
problem for it: Ins. Code §1631 bars an unlicensed person from soliciting or
negotiating insurance, §1633 makes it a misdemeanour, and no California statute
expressly authorises a referral fee to an unlicensed person for referring a
BUYER. The permission, if it exists, is inferred from the negative scope of
§1631. Editorial comparison content of the kind this site publishes sits closer
to "describing coverage and encouraging a purchase" than a passive listing does.
That is a real tension and the honest place to record it is here.

Idempotent, guarded.
"""
import os, re, sys

HERE = os.path.dirname(os.path.abspath(__file__))
SITE = os.path.dirname(HERE)
RESTYLE = os.path.join(HERE, "restyle.py")
DISCLOSURE = os.path.join(SITE, "affiliate-disclosure.html")
PAGE = "therapy-liability-insurance-california.html"
MARK = "<!-- _dev/insurance_wire.py -->"
END = "<!-- /insurance_wire -->"

NAV_ENTRY = (
    '    ("therapy-liability-insurance-california.html", "Liability insurance",\n'
    '     "eight programs, what they publish and what people pay",\n'
    '     "therapist-cost-of-living-california.html"),\n'
)
NAV_ANCHOR = '    ("simplepractice-california-therapists.html", "SimplePractice",\n'

BLOCK = """%s<h2 id="what-we-are-not-paid">What we looked for and did not find</h2>
<p>Before publishing the <a href="%s">liability insurance comparison</a> we
checked every carrier and agency on it for an affiliate, referral or partner
program &mdash; <b>CPH &amp; Associates, HPSO, The Trust, Berxi, Proliability,
CM&amp;F Group, American Professional Agency and Lockton Affinity</b>. Not one of
them runs a public affiliate program. They work through association endorsements
negotiated one&nbsp;off with professional bodies, not through publisher
commissions.</p>
<p>We also searched the affiliate networks directly &mdash; Impact, CJ,
ShareASale, PartnerStack, Awin, FlexOffers and Refersion. Between them they list
no healthcare&#8209;professional malpractice carrier at all. There is no
affiliate path to any insurer a California therapist would actually buy from,
and so nothing on that page is paid for.</p>
<p>The programs that <em>do</em> pay publishers &mdash; Hiscox, Thimble, Simply
Business, Insureon &mdash; are general small&#8209;business insurers, and we could
not verify that any of them writes licensed mental&#8209;health professional
liability. Recommending one to a therapist for malpractice cover would be wrong
on the merits whatever it paid.</p>
<p>And if that changes, there is a second problem to solve first. California
Insurance Code &sect;&thinsp;1631 bars an unlicensed person from soliciting or
negotiating insurance, &sect;&thinsp;1633 makes doing so a misdemeanour, and we
could find no California statute that expressly permits paying a referral fee to
an unlicensed person for sending an insurance <em>buyer</em>. Comparison writing
of the kind on that page sits closer to the line than a bare listing does. We
would want a written answer from a California insurance lawyer before accepting
any of it.</p>
%s""" % (MARK, PAGE, END)


def main():
    bad = 0

    # ------------------------------------------------------------- the nav
    if not os.path.exists(RESTYLE):
        sys.exit("insurance_wire: _dev/restyle.py is not there")
    s = open(RESTYLE, encoding="utf-8").read()
    if PAGE in s:
        print("nav: already carries the insurance page")
    else:
        if NAV_ANCHOR not in s:
            sys.exit("insurance_wire: the PRACTICE list has changed shape - "
                     "re-read restyle.py rather than letting this half-apply")
        s = s.replace(NAV_ANCHOR, NAV_ENTRY + NAV_ANCHOR, 1)
        open(RESTYLE, "w", encoding="utf-8").write(s)
        print("nav: added to the Practice column")

    # ------------------------------------------------------ the disclosure
    if not os.path.exists(DISCLOSURE):
        sys.exit("insurance_wire: affiliate-disclosure.html is not there")
    d = open(DISCLOSURE, encoding="utf-8").read()
    orig = d
    d = re.sub(re.escape(MARK) + r"[\s\S]*?" + re.escape(END), "", d)

    # It goes immediately before "What I do not do", because that section is
    # the page's list of things it will not accept, and this is the evidence
    # for one of them.
    m = re.search(r'<h2 id="what-i-dont-do">', d)
    if not m:
        m = re.search(r"<h2[^>]*>What I do not do</h2>", d)
    if not m:
        print("GUARD: cannot find the 'What I do not do' heading")
        bad += 1
    else:
        d = d[:m.start()] + BLOCK + d[m.start():]
        if d != orig:
            open(DISCLOSURE, "w", encoding="utf-8").write(d)
            print("disclosure: recorded the carriers we checked")
        else:
            print("disclosure: already up to date")

    # ------------------------------------------------------------- guards
    d = open(DISCLOSURE, encoding="utf-8").read()
    if d.count(MARK) != 1 or d.count(END) != 1:
        print("GUARD disclosure: %d marks / %d ends" % (d.count(MARK), d.count(END)))
        bad += 1
    if not os.path.exists(os.path.join(SITE, PAGE)):
        print("GUARD: the disclosure links %s, which does not exist yet - "
              "run build_insurance.py first" % PAGE)
        bad += 1
    s = open(RESTYLE, encoding="utf-8").read()
    if s.count(PAGE) != 1:
        print("GUARD restyle: %d nav entries for the page" % s.count(PAGE))
        bad += 1
    # The claim on the disclosure page must name every carrier the comparison
    # page lists, or it is a narrower claim than it looks.
    sys.path.insert(0, HERE)
    from insurance_data import CARRIERS  # noqa: E402
    import html as _h
    plain = _h.unescape(d)
    for c in CARRIERS:
        stem = _h.unescape(c["name"]).split(" ")[0]
        if stem not in plain:
            print("GUARD disclosure: does not name %s" % c["name"])
            bad += 1
    if bad:
        sys.exit("\n%d problem(s)" % bad)
    print("guards clean - the disclosure names all %d carriers" % len(CARRIERS))


if __name__ == "__main__":
    main()
