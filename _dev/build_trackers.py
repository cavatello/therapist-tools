#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Who is holding your licensure record? - the hours trackers, compared.

THE QUESTION THIS ANSWERS

Somebody a few weeks into an associateship asks which app to log hours in, and
gets five product names and no basis for choosing between them. The products
are cheap enough that the price is not the decision. What is at stake is that
one of them will be holding the only continuous record of three thousand hours
of supervised work for the next two to four years.

THE CORRECTION THAT CHANGED THIS PAGE

The research this page was scoped from assumed the Board publishes no position
on whether it accepts an electronic supervisor signature, and that the whole
category therefore rested on an unanswered question. That was wrong, and it
was wrong in the reader's favour.

The Board does publish a position, in three places: its FAQs for Supervisors
(marked New 02/2026) answers the question directly - "Signed documents may be
original, scanned, or have an electronic signature" - and the Verification of
Experience forms themselves print "ORIGINAL OR ELECTRONIC SIGNATURE REQUIRED"
above the supervisor's line. The weekly log forms carry no signature
instruction at all, so for those the FAQ is the governing published answer.

So the e-signature feature is real and the Board will take it. The page's
ending moved to the question that is actually open: who these companies are.

THE FINDING THAT REPLACED IT

Of the five products, one publishes a legal entity, a street address and a
telephone number. Four publish an email address and nothing else, and three of
those four have a /about page that returns 404. And the domains, from the
registries' own RDAP records on the date below: one from 2006, one from 2024,
and three registered during 2026.

That is not an accusation of anything. New companies are new, and a 2026
domain is a fact about a domain. It is printed because it is the single
hardest-to-fake signal available about who is going to be holding the record,
and because nobody selling one of these publishes it.

Idempotent - rewrites its page from scratch every run. Guarded.
"""
import os, re, sys

HERE = os.path.dirname(os.path.abspath(__file__))
SITE = os.path.dirname(HERE)
sys.path.insert(0, HERE)

import pagekit as pk

PAGE = "associate-hours-trackers-compared.html"
DONOR = "hiring-first-associate-california-therapist.html"

HOURS = "amft-3000-hours-california.html"
SIMPLE = "simplepractice-california-therapists.html"
TNSP = "therapynotes-vs-simplepractice-california.html"
UNPAID = "associate-unpaid-hours-california.html"

RDAP_CHECKED = "10 August 2026"
FAQ_DATED = "February 2026"

TOTAL_HOURS = 3000
WEEKS = 104

# ---------------------------------------------------------------- the products
#
# Everything in this table was read off the vendor's own site on the date in
# RDAP_CHECKED, except `domain`, which is the registration date in the
# registry's RDAP record. Nothing is inferred. Where a vendor does not publish
# something the value is None and the page prints "not published" - which is a
# finding, not a gap.
#
# `esign` is deliberately three-valued rather than a tick. "Sends the form to
# the supervisor" and "captures the supervisor's signature" are different
# products, and one vendor's own copy says its signature fields are left blank.
PRODUCTS = [
    {
        "name": "Track Your Hours",
        "site": "https://www.trackyourhours.com/",
        "price": "$89.95 a year",
        "price_more": "$159.95 for two years, $199.95 for three",
        "free": "30 days, no card",
        "domain": "October 2006",
        "esign": None,
        "esign_note": "Not advertised anywhere on the home page, the features "
                      "page or the FAQ.",
        "forms": "Generic. &ldquo;The forms required by the boards in the "
                 "states we operate in&rdquo;, with no form number named.",
        "entity": "Track Your Hours, LLC",
        "address": "2834 Colorado Ave, Santa Monica, CA",
        "phone": "Published",
        "about404": False,
        "note": "The oldest product in the category by eighteen years. Its "
                "terms route legal notices care of <b>SimplePractice, LLC</b> "
                "in Santa Monica, which is the only relationship between an "
                "hours tracker and a practice-management company disclosed "
                "anywhere in this table.",
    },
    {
        "name": "HourJourney",
        "site": "https://hourjourney.io/",
        "price": "$79 a year",
        "price_more": "$49 a year at trainee level; a &ldquo;Plus&rdquo; "
                      "add-on is $20 more",
        "free": "30 days, no card",
        "domain": "March 2026",
        "esign": "sends",
        "esign_note": "Sends forms to the supervisor and tracks delivery and "
                      "opens &mdash; but its own copy says the "
                      "<b>&ldquo;signature and pay-status fields are always "
                      "left blank&rdquo;</b> for you and your supervisor to "
                      "complete. It transmits a form; it does not capture a "
                      "signature.",
        "forms": "<b>37A-525</b> and <b>37A-301</b>, named.",
        "entity": None,
        "address": "Moreno Valley, California &mdash; city only",
        "phone": None,
        "about404": True,
        "note": "Governing law is California. Contact is a web form.",
    },
    {
        "name": "License Journey",
        "site": "https://licensejourney.com/",
        "price": "$74.99 a year",
        "price_more": "$6.99 a month, or $199.99 once",
        "free": "1 month, no card",
        "domain": "February 2024",
        "esign": "yes",
        "esign_note": "Added 10 May 2026. Covers weekly logs, "
                      "end-of-experience verification, supervision "
                      "agreements and hour corrections.",
        "forms": "Generic. &ldquo;The official BBS forms for your supervisor "
                 "to sign&rdquo;, with no form number named.",
        "entity": None,
        "address": None,
        "phone": None,
        "about404": False,
        "note": "Its published claim is the most specific of the five: every "
                "signature is &ldquo;time-stamped, tied to the "
                "signer&rsquo;s authenticated account, and bound "
                "cryptographically to the version of the log being "
                "signed&rdquo;, exportable as a PDF with an audit trail.",
    },
    {
        "name": "ClearPath Hours",
        "site": "https://www.clearpathhours.com/",
        "price": "$25 a year",
        "price_more": "A free tier at 50 entries a month; twelve months free "
                      "on a school email; supervisors free",
        "free": "Free tier, no expiry",
        "domain": "April 2026",
        "esign": "review",
        "esign_note": "&ldquo;Supervisor review and sign-off&rdquo; through a "
                      "supervisor portal with a review queue. No signature "
                      "standard is named.",
        "forms": "Shows an image of a California BBS Weekly Log of Experience "
                 "Hours; claims auto-filled board PDFs for all fifty states.",
        "entity": None,
        "address": None,
        "phone": None,
        "about404": True,
        "note": "The cheapest paid tier in the category by a factor of three, "
                "at a price the page itself describes as fixed forever.",
    },
    {
        "name": "SparkHours",
        "site": "https://sparkhours.com/",
        "price": "$100 a year",
        "price_more": "$10 a month; supervisors free",
        "free": "14 days, no card",
        "domain": "January 2026",
        "esign": "yes",
        "esign_note": "The supervisor gets a link, reviews the summary and "
                      "signs, without needing an account.",
        "forms": "<b>37A-525</b> for AMFTs and <b>37A-638</b> for ASWs and "
                 "APCCs, named, plus the in-state experience verification.",
        "entity": None,
        "address": None,
        "phone": None,
        "about404": True,
        "note": "The only vendor to name the statutes its signatures are "
                "meant to satisfy: <b>SHA-256 document hashing, a full audit "
                "trail, a signed consent ceremony, and compliance with UETA "
                "and the federal ESIGN Act</b>.",
    },
]

ESIGN_LABEL = {
    None: "Not advertised",
    "sends": "Sends, does not sign",
    "review": "Sign-off, unspecified",
    "yes": "Captures a signature",
}

JUMPS = [
    ("board", "What the Board accepts"),
    ("table", "The five, compared"),
    ("who", "Who is behind them"),
    ("ehr", "Your EHR does not do this"),
    ("choose", "How to choose"),
]


def new_in_2026():
    return [p for p in PRODUCTS if p["domain"].endswith("2026")]


def anonymous():
    return [p for p in PRODUCTS if not p["phone"]]


def body():
    o = ['<article class="pk-wrap">']

    o.append(pk.hero(
        "Hours trackers &middot; five products &middot; checked %s"
        % pk.CHECKED,
        "Who is holding your licensure record?",
        "Five apps will log your %s hours for between $25 and $100 a year. "
        "The price is not the decision. <b>Three of the five had their "
        "domain registered this year</b>, and four publish no address, no "
        "telephone number and no named human being."
        % format(TOTAL_HOURS, ",d"),
        [("5", "products compared"),
         ("$25&ndash;$100", "a year, the whole range"),
         ("%d of 5" % len(new_in_2026()), "domains registered in 2026"),
         ("%d of 5" % len(anonymous()), "publish no phone or address")],
        JUMPS))

    # ------------------------------------------------------------- the Board
    o.append('<section class="pk-sec" id="board">')
    o.append('<p class="pk-k">Settled, and worth knowing before you shop</p>')
    o.append('<h2 class="pk-h">The Board accepts an electronic signature. It '
             "does not accept a typed name.</h2>")
    o.append('<p class="pk-d">Two of these products are sold largely on '
             "supervisor e-signature, so the first question is whether the "
             "Board will take one. It will, and it says so in three separate "
             "places &mdash; which is more than most things about supervision "
             "documentation can claim.</p>")
    o.append(pk.table(
        ["Where it says so", "What it says"],
        [(["FAQs for Supervisors, marked new %s, question 37" % FAQ_DATED,
           "&ldquo;Signed documents may be original, scanned, or have an "
           "<b>electronic signature</b>.&rdquo; The same document adds that "
           "supervisees are not permitted to sign the weekly logs for the "
           "supervisor."], "good"),
         ["In-State Experience Verification forms &mdash; 37A-301 (MFT), "
          "37A-201 (LCSW), 37A-675 (LPCC)",
          "Printed immediately above the supervisor&rsquo;s line: "
          "<b>&ldquo;ORIGINAL OR ELECTRONIC SIGNATURE REQUIRED&rdquo;</b>. "
          "The LCSW form adds &ldquo;scanned&rdquo;."],
         ["The license applications themselves",
          "The LMFT application asks for a wet signature <b>or</b> an "
          "electronic one, and says an electronic signature is accepted if "
          "completed through a platform &ldquo;such as Adobe Sign or "
          "DocuSign which ensures security and authenticity&rdquo;."],
         (["The Weekly Log forms &mdash; 37A-525, 37A-638",
           "<b>No signature instruction at all.</b> A bare "
           "&ldquo;Supervisor Signature&rdquo; line, unchanged since 2022. "
           "For these two forms the general FAQ answer is the only published "
           "guidance there is."], "hi")],
        "The line the Board draws is between a signature and a typed name. "
        "CAMFT reported in 2022 that the Board would keep accepting "
        "electronic signatures on supervision documents but would not accept "
        "a form with the supervisor&rsquo;s name simply typed in &mdash; "
        "which is the distinction every product below is either on the right "
        "side of or silent about."))
    o.append("</section>")

    # -------------------------------------------------------------- the table
    o.append('<section class="pk-sec" id="table">')
    o.append('<p class="pk-k">Read off each vendor&rsquo;s own site, %s</p>'
             % RDAP_CHECKED)
    o.append('<h2 class="pk-h">The five, side by side.</h2>')
    rows = []
    for p in PRODUCTS:
        cls = "good" if p["phone"] else ""
        rows.append(([
            '<b>%s</b>' % p["name"],
            (p["price"], "f"),
            p["free"],
            (ESIGN_LABEL[p["esign"]], "m"),
            (p["domain"], "m"),
        ], cls))
    o.append(pk.table(
        ["Product", "Price", "Free", "Supervisor signature", "Domain since"],
        rows,
        "Domain registration dates are from the registries&rsquo; own RDAP "
        "records, checked %s. A domain age is not a company age and is not a "
        "judgment about a product &mdash; it is the one fact about a vendor "
        "that cannot be written by the vendor." % RDAP_CHECKED, minw=680))

    for p in PRODUCTS:
        o.append('<h3 class="pk-h3">%s</h3>' % p["name"])
        o.append('<p class="pk-d">%s Price: <b>%s</b>%s. Free: %s.</p>'
                 % (p["note"], p["price"],
                    " &mdash; " + p["price_more"] if p["price_more"] else "",
                    p["free"]))
        o.append(pk.table(
            ["", ""],
            [["Supervisor signature", p["esign_note"]],
             ["BBS forms named", p["forms"]],
             ["Legal entity published", p["entity"] or
              "<b>Not published</b>"],
             ["Address", p["address"] or "<b>Not published</b>"],
             ["Telephone", p["phone"] or "<b>Not published</b>"],
             ["An /about page", "Returns 404" if p["about404"]
              else "Present"]], minw=420))
    o.append("</section>")

    # ---------------------------------------------------------------- who
    o.append('<section class="pk-sec" id="who">')
    o.append('<p class="pk-k">The part nobody writes up</p>')
    o.append('<h2 class="pk-h">You are choosing a custodian, not an app.</h2>')
    o.append('<p class="pk-d">A tracker holds the only continuous record of '
             "%s hours accumulated over at least %d weeks. If it stops "
             "existing in year three, the reconstruction falls to you and to "
             "supervisors who may have moved on. That makes &ldquo;will this "
             "company still be here&rdquo; a more important question than any "
             "feature in the table above, and it is the question none of them "
             "answers.</p>" % (format(TOTAL_HOURS, ",d"), WEEKS))
    o.append(pk.callout(
        "What was and was not found, %s" % RDAP_CHECKED,
        ["<b>One</b> of the five publishes a legal entity, a street address "
         "and a telephone number. <b>Four</b> publish an email address and "
         "nothing else, and three of those four return a 404 on their own "
         "/about page.",
         "<b>Three</b> of the five domains were registered in 2026 &mdash; "
         "January, March and April. One dates from 2024 and one from 2006.",
         "What could not be established at all: whether any of the four is a "
         "registered business anywhere, who runs them, or whether the "
         "cryptographic claims two of them make are implemented as described. "
         "Those are printed as unestablished rather than guessed at."],
        big="%d of 5" % len(anonymous())))
    o.append(pk.checklist(
        "What to do about it, whichever you pick",
        ["<b>Export on a schedule.</b> Monthly, to a PDF you keep yourself. "
         "Every one of these can produce a file; the point is that the file "
         "lives somewhere the vendor does not control.",
         "<b>Get the verification signed as you go</b>, not at the end. A "
         "supervisor who has already signed cannot become unreachable.",
         "<b>Keep the weekly logs even after they are totalled.</b> The Board "
         "can ask, and the total is not the evidence &mdash; the logs are.",
         "<b>Check the export actually reproduces the form.</b> A tracker "
         "that fills a board PDF is only useful if the PDF it fills is the "
         "current revision of the right form.",
         "<b>Do not let the tracker be the only place your hours exist.</b> "
         "That is the whole of the advice, and it costs nothing."]))
    o.append("</section>")

    # ----------------------------------------------------------------- EHR
    o.append('<section class="pk-sec" id="ehr">')
    o.append('<p class="pk-k">A common and expensive assumption</p>')
    o.append('<h2 class="pk-h">Your practice software is not doing this.</h2>')
    o.append('<p class="pk-d">Both of the practice-management systems most '
             "California associates work in have a supervision feature, and "
             "neither of them tracks hours toward licensure. They do "
             "<i>countersignature of clinical notes</i>, which is a different "
             "thing that happens to involve the same two people.</p>")
    o.append(pk.table(
        ["What it does", "What it does not do"],
        [["<b>SimplePractice</b> &mdash; designate a supervisor and "
          "supervisee, review and sign documentation, bill under "
          "supervision.",
          "No log of hours by Board category, no running total against the "
          "%s, no %d-week test, no cap on the non-clinical categories, no "
          "board form." % (format(TOTAL_HOURS, ",d"), WEEKS)],
         ["<b>TherapyNotes</b> &mdash; note review and co-signature, and "
          "incident-to billing.",
          "The same absence. Neither product publishes an hours-tracking "
          "feature at all."]],
        "Which is why a separate tracker exists as a category. If you are "
        'choosing between the two systems themselves, <a href="%s">that '
        "comparison is a different page</a>." % TNSP))
    o.append("</section>")

    # -------------------------------------------------------------- choosing
    o.append('<section class="pk-sec" id="choose">')
    o.append('<p class="pk-k">No winner, on purpose</p>')
    o.append('<h2 class="pk-h">What would actually decide it.</h2>')
    o.append(pk.numbered([
        ("1", "If continuity is what worries you",
         "Weight the vendor that publishes an entity, an address and a "
         "telephone number, and whose domain predates the category by "
         "eighteen years. That is <b>Track Your Hours</b>, and it is also the "
         "one that does not advertise supervisor e-signature at all &mdash; "
         "so the trade is explicit."),
        ("2", "If the signature workflow is what worries you",
         "Two products capture a supervisor signature and say so in "
         "detail, and one of those names UETA and the federal ESIGN Act. "
         "Read the distinction in the table carefully: <b>one product sends "
         "a form and leaves the signature field blank</b>, which is a "
         "delivery feature described in signature language."),
        ("3", "If price is what worries you",
         "The spread is $75 a year across the whole category, and one "
         "product has a genuinely free tier. Over a two-year associateship "
         "the most expensive option costs about $150 more than the cheapest. "
         "That is not nothing, and it is much less than one unbilled hour "
         "spent reconstructing a lost month."),
        ("4", "What should not decide it",
         "The number of states a product claims to support. Every one of "
         "these is a California decision made by a California registrant, "
         "and &ldquo;all fifty states&rdquo; on a landing page is a "
         "statement about ambition rather than about the form your "
         "supervisor has to sign."),
    ]))
    o.append('<p class="pk-fine">Nothing on this page is a recommendation and '
             "none of these links is an affiliate link. Prices, features and "
             "the presence or absence of a published address were read off "
             "each vendor&rsquo;s own site on %s and will drift; the domain "
             "dates come from the registries and will not. If you would "
             "rather do the arithmetic than the shopping, "
             '<a href="%s">the hours calculator</a> projects a licensure '
             "date from your own numbers and sends nothing anywhere &mdash; "
             'and if the hours themselves are going unpaid, <a href="%s">that '
             "is a separate problem with a separate remedy</a>.</p>"
             % (RDAP_CHECKED, HOURS, UNPAID))
    o.append("</section>")

    # ---------------------------------------------------------------- sources
    vend = [("%s &mdash; the product&rsquo;s own site" % p["name"], p["site"])
            for p in PRODUCTS]
    src, n = pk.sources([
        ("What the Board publishes about signatures", [
            ("BBS FAQs for Supervisors &mdash; question 37, marked new %s"
             % FAQ_DATED,
             "https://www.bbs.ca.gov/pdf/publications/faqs_for_supervisors.pdf"),
            ("MFT In-State Experience Verification, form 37A-301",
             "https://www.bbs.ca.gov/pdf/forms/mft/"
             "lmft_expver_37a-301_option1.pdf"),
            ("Clinical Social Worker In-State Experience Verification, form "
             "37A-201", "https://www.bbs.ca.gov/pdf/forms/lcs/lcs-exp.pdf"),
            ("PCC In-State Experience Verification, form 37A-675",
             "https://www.bbs.ca.gov/pdf/forms/lpc/"
             "lpcc_expver_37a-675_option1.pdf"),
            ("MFT Weekly Log of Experience Hours, form 37A-525 &mdash; read "
             "for the absence of a signature instruction",
             "https://www.bbs.ca.gov/pdf/forms/mft/"
             "mfwkylog_37a-525_option1.pdf"),
            ("ASW and APCC Weekly Log of Experience Hours, form 37A-638",
             "https://www.bbs.ca.gov/pdf/forms/lpc/"
             "lpcc_wkylog_37a-638_option1.pdf"),
            ("LMFT license application, form 37A-318 &mdash; the Adobe Sign "
             "and DocuSign wording",
             "https://www.bbs.ca.gov/pdf/forms/mft/mftapp.pdf"),
            ("CAMFT, June 2022 &mdash; electronic signatures accepted, typed "
             "names not",
             "https://www.camft.org/Membership/About-Us/E-Newsletters/"
             "E-news-2022/June-2022-E-Newsletter/"
             "BBS-Accepts-Electronic-Signatures-on-BBS-Forms"),
        ]),
        ("The products", vend),
        ("What the practice-management systems do instead", [
            ("SimplePractice &mdash; the supervision help section",
             "https://support.simplepractice.com/hc/en-us/sections/"
             "44118126910093-Supervision"),
            ("TherapyNotes &mdash; setting up supervision",
             "https://support.therapynotes.com/hc/en-us/articles/"
             "32522534750363-Set-Up-Supervision"),
        ]),
        ("Domain registration dates", [
            ("Verisign RDAP, for the .com domains &mdash; queried %s"
             % RDAP_CHECKED, "https://rdap.verisign.com/com/v1/"),
            ("The .io registry&rsquo;s RDAP record, for HourJourney", None),
        ]),
    ], note="Prices and features were read from each vendor&rsquo;s own "
            "public pages, not from a review site and not from a press "
            "release. Where a vendor does not publish something, this page "
            "says <b>not published</b> rather than inferring it: an unlisted "
            "telephone number is a fact about a website, not about a "
            "company. Nothing here is an affiliate link.")
    o.append(src)

    o.append("</article>")
    return "".join(o), n


META = pk.meta_block(
    PAGE,
    "BBS hours trackers compared: five products, and who is behind them",
    "Five apps that log California supervised hours, from $25 to $100 a "
    "year, with what the Board actually accepts as a supervisor signature "
    "and which vendors publish an address, a phone number or an entity.",
    "licensure", "comparison",
    "Which app should I log my supervised hours in?",
    "Prices, signature workflows and domain ages for all five, and the "
    "Board&rsquo;s published position on electronic signatures",
    "%d of 5 registered in 2026" % len(new_in_2026()),
    weight=4)


def main():
    print("hours trackers, compared")

    head, header, footer, links, scripts = pk.chrome_parts(DONOR)
    html_body, nsrc = body()
    html = pk.assemble(head, META, header, html_body, footer, links, scripts)

    p = os.path.join(SITE, PAGE)
    open(p, "w", encoding="utf-8").write(html)
    print("  wrote %s, %s bytes, %d sources, %d products"
          % (PAGE, format(len(html), ",d"), nsrc, len(PRODUCTS)))

    bad = pk.check_page(p, [
        ("the Board's e-signature answer", "original, scanned, or have an"),
        ("the form-level requirement", "ORIGINAL OR ELECTRONIC SIGNATURE"),
        ("the EHR section", "countersignature"),
    ], [j[0] for j in JUMPS] + ["sources"])

    s = open(p, encoding="utf-8").read()
    art = pk.article(s)

    # Every product must appear by name, with its price, in the comparison.
    # A product silently dropped from the table would leave the counts in the
    # hero and the callout describing five things while four are shown.
    for prod in PRODUCTS:
        if prod["name"] not in art:
            print("GUARD: %s is not on the page" % prod["name"])
            bad += 1
        if prod["price"] not in art:
            print("GUARD: %s's price is not on the page" % prod["name"])
            bad += 1

    # The derived counts in the hero must match the data, or the page makes a
    # claim the table below it contradicts.
    for phrase, n in (("%d of 5" % len(new_in_2026()), len(new_in_2026())),
                      ("%d of 5" % len(anonymous()), len(anonymous()))):
        if phrase not in art:
            print("GUARD: the derived count %r is not on the page" % phrase)
            bad += 1
    if len(new_in_2026()) != 3 or len(anonymous()) != 4:
        print("GUARD: the counts moved - %d domains from 2026 and %d without "
              "a phone number. The hero and the callout say three and four in "
              "words as well as figures; check both."
              % (len(new_in_2026()), len(anonymous())))
        bad += 1

    # This page names companies. An unsourced adjective about one of them is
    # the failure mode, so every vendor must be linked to its own site.
    for prod in PRODUCTS:
        if prod["site"] not in art:
            print("GUARD: %s is described but not linked to its own site"
                  % prod["name"])
            bad += 1

    if bad:
        sys.exit("\n%d problem(s)" % bad)
    print("  guards clean - %d products, all linked, counts match the data"
          % len(PRODUCTS))


if __name__ == "__main__":
    main()
