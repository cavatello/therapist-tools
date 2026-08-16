#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""P3, the curated half: EB CAMFT's practicum-site directory, annotated.

WHY THIS PAGE EXISTS NEXT TO practicum-sites-bay-area.html. The settings
directory (13 Aug) answers what a setting IS - the universes the statute
allows, from federal and IRS files, with availability language banned
because those files cannot know it. This page is the other kind of
directory and says so plainly: a CURATED, NAMED-SITE list, not exhaustive,
whose source is East Bay CAMFT's own public "Practicum Site Directory
2026-2027 Training Year" (https://ebcamft.org/practicum-sites, fetched
15 August 2026). The chapter collected per-site facts no public dataset
holds - who was accepting students, hours, supervision form, populations,
school MOUs, prerequisites, a named contact - and because the chapter
publishes them, this site may republish them WITH THE DATE ON EVERY CLAIM.
The listing is the chapter's work and is credited as the source throughout.

THE FRAME IS THE TRAINEE'S. A practicum student may not work in a private
practice or a professional corporation at all - BPC 4980.43.3(b) - which is
why three entries matter differently: Bonita House and Rose MFT also hire
registered associates, and Calliope Coast is ASSOCIATES-ONLY and not a
practicum site at all. The directory's own framing, published as such.

LINK DISCIPLINE. Every published site URL was fetched from this workspace
on 15 August 2026 (4-variant fallback, browser UA); each entry below
records the verdict. 18 of 19 URLs answered 200; cchealth.org answers 403
to scripted fetches (bot-blocker) but is the link both shipped Bay
directories have carried since 13 Aug 2026, so that verified link form is
reused. Two sites publish no website in the directory - LifePractice and
Rose MFT - and that renders as the finding it is, never as a blank.
"Not stated" is likewise printed wherever the directory has no value.

NOT REPRODUCED: nothing beyond what the chapter's public page states. The
count discrepancy is published too: the directory's own counter said
"Showing all 22 sites" while 21 entries carried published details at the
15 August 2026 read.

Chrome borrows from the loan-forgiveness donor (pagekit), so the page
joins the pagekit family and family_pk.py converts it to bc2 (house.css +
house-chrome.css + house-pk.css, content-hash-versioned, no legacy hash
sheets) in the same pipeline run - the shipped state is bc2-native.
"""
import os, sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import pagekit as pk

SITE = pk.SITE
PAGE = "east-bay-practicum-site-directory.html"
DONOR = "loan-forgiveness-employers-california.html"

SETTINGS = "practicum-sites-bay-area.html"
METHOD = "how-to-find-a-practicum-site-california.html"
PRACTICUM = "practicum-california-mft-trainee.html"
EMPLOYERS = "associate-employers-bay-area.html"
NINETY = "bbs-90-day-rule-california.html"

LEG = ("https://leginfo.legislature.ca.gov/faces/codes_displaySection.xhtml"
       "?sectionNum=%s.&lawCode=BPC")

SRC_URL = "https://ebcamft.org/practicum-sites"
SRC_NAME = "East Bay CAMFT"
READ = "15 August 2026"          # the date on every entry claim below
READ_SHORT = "15 Aug 2026"

# Every field below is transcribed from the chapter's public directory at
# the 15 August 2026 fetch; `checked` is this workspace's own URL verdict,
# same date unless noted. src on every entry, per the build rule.
SRC = "ebcamft.org/practicum-sites, read 15 Aug 2026"

SITES = [
 dict(name="Seneca Family of Agencies", accepting="yes", mode="In person",
      hrs="15&ndash;20", also="MSW",
      where="Alameda, Contra Costa, Solano, Sonoma, Marin, SF, San Mateo, "
            "Santa Clara, Monterey, San Benito, San Luis Obispo and Orange "
            "counties; and Seattle, WA",
      days="Monday &ndash; Friday",
      clin="Individual therapy, family, groups, crisis intervention",
      sup="Individual, group",
      pop="Children, youth, and families",
      mou="UC Berkeley; CSU East Bay, San Jose, SF, Sacramento, Sonoma; "
          "Wright Institute; USF; Santa Clara; USC; Columbia; and others",
      bbs="Yes",
      prereq="LiveScan clearance; two-week new-employee orientation "
             "(M&ndash;F, 9am&ndash;5:30pm, live synchronous) before "
             "starting",
      contact="Graduate Internship Program",
      email="internship@senecacenter.org",
      url="https://senecafoa.org/careers/graduate-internship-program/",
      checked="200, 15 Aug 2026", src=SRC),
 dict(name="Diablo Valley Drug and Alcohol Services", accepting="yes",
      mode="In person", hrs="10", also="PsyD &amp; MSW",
      where="Walnut Creek (residential/withdrawal management) and "
            "San Ramon (IOP and PHP)",
      days="Monday &ndash; Friday",
      clin="Individual therapy, family, groups, crisis intervention; all "
           "realms of addiction treatment",
      sup="Individual, group",
      pop="Adults &mdash; addiction and co-occurring disorders",
      mou="DVC", bbs="Yes", prereq="Liability insurance",
      contact="Dr. Dan Smeester", email="dansmeester@yahoo.com",
      url="https://www.diablovalleytreatment.com",
      checked="200, 15 Aug 2026", src=SRC),
 dict(name="Asian Health Services", accepting="yes", mode="Hybrid",
      hrs="15", also="PsyD &amp; MSW", where="Oakland",
      days="Monday &ndash; Friday",
      clin="Individual therapy, couples, family, groups, crisis "
           "intervention, outreach",
      sup="Individual, group, triadic",
      pop="Asian American immigrants and refugees, ages 5&ndash;90",
      mou="Wright Institute, Palo Alto University, Loma Linda, Tulane, "
          "USF, CSUEB, St. Mary&rsquo;s",
      bbs="Yes", prereq="2nd-year master&rsquo;s level or above",
      contact="Jennifer Yu, PhD, LMFT &mdash; BH Training Academy Program "
              "Manager",
      email="jeyu@ahschc.org", url="https://asianhealthservices.org",
      checked="200, 15 Aug 2026", src=SRC),
 dict(name="Healing Pastures @ C Horse Ranch", accepting="yes",
      mode="In person", hrs="Varies", also=None, where="Auburn",
      days="Monday, Friday, Saturday",
      clin="Individual therapy, couples, family, outreach, art therapy, "
           "animal-assisted/equine therapy",
      sup="Individual", pop="Individuals, couples, special needs",
      mou="None currently", bbs="No",
      prereq="Not allergic to animals/equines",
      contact="Honey Cowan, CEO",
      email="honeycowan.chorseranch@yahoo.com",
      url="https://www.healingpastures-chorseranch.org",
      checked="200, 15 Aug 2026", src=SRC),
 dict(name="Compass Family Services", accepting="yes", mode="In person",
      hrs="15&ndash;20", also=None,
      where="San Francisco &mdash; Civic Center",
      days="Monday &ndash; Friday",
      clin="Individual therapy, couples, family, crisis intervention, "
           "play therapy",
      sup="Individual, group, triadic",
      pop="Unhoused, low-income, single parents, trauma, SUD, IPV, child "
          "abuse, immigrant families",
      mou="Wright Institute, Golden Gate University, CIIS, USC, SF State "
          "University",
      bbs="Yes", prereq="Fingerprinting",
      contact="Shonece Barney &mdash; Program Director",
      email="sbarney@compass-sf.org", url="https://www.compass-sf.org",
      checked="200, 15 Aug 2026", src=SRC),
 dict(name="Contra Costa Behavioral Health", accepting="yes",
      mode="In person", hrs="15&ndash;20", also="PsyD",
      where="Contra Costa County &mdash; address varies by program",
      days="Monday &ndash; Friday",
      clin="Individual therapy, family", sup="Individual, group",
      pop="Children, adolescents and adults with severe and persistent "
          "mental illness (age group varies by program)",
      mou="Palo Alto University, UC Berkeley, The Wright Institute, Saint "
          "Mary&rsquo;s College, Alliant International, University of the "
          "Pacific, Cal State East Bay",
      bbs="Yes",
      prereq="Live Scan, practicum agreement, proof of eligibility to "
             "work in the U.S., TB test; HR and Provider Services "
             "onboarding",
      contact="Erika Arevalo &mdash; Countywide Intern Training "
              "Coordinator",
      email="erika.sanchez@cchealth.org",
      url="http://cchealth.org/mentalhealth/",
      checked="the county's own site; carried as a verified link on both "
              "Bay directories since 13 Aug 2026; answers 403 to scripted "
              "fetches (bot-blocker), re-tried 15 Aug 2026", src=SRC),
 dict(name="Heart in Balance Therapy", accepting="yes", mode="Hybrid",
      hrs="15&ndash;20", also=None, where="Oakland",
      days="Monday &ndash; Sunday (flexible)",
      clin="Individual therapy, couples, family, groups, children",
      sup="Individual, group",
      pop="A broad and diverse range of clients", mou="CIIS", bbs="Yes",
      prereq="Enrollment in a graduate-level counseling/therapy degree "
             "program requiring supervised practicum",
      contact="Jen Shelby &mdash; Executive Director",
      email="administration@heartinbalancetherapy.com",
      url="https://www.heartinbalancetherapy.com",
      checked="200, 15 Aug 2026", src=SRC),
 dict(name="Surf Circle", accepting="no", mode="In person", hrs="10",
      also="PsyD",
      where="Pacifica (at the beach), supervision over Zoom; Oakland",
      days="Friday, Sunday", clin="Adolescent psychotherapy",
      sup="Individual, group", pop="Adolescents",
      mou="Wright Institute, CIIS, Stanford", bbs="Yes",
      prereq="Surf experience; CPR/First Aid and water-safety training "
             "provided by the site",
      contact="Adam Moss, PsyD &mdash; Co-Founder and Training Director",
      email="info@surfcircle.org", url="https://www.surfcircle.org",
      checked="200, 15 Aug 2026", src=SRC),
 dict(name="Between Therapy", accepting="yes", mode="Telehealth only",
      hrs="10", also="PsyD &amp; MSW", where="Virtual",
      days="Flexible (Mon&ndash;Sun)", clin="Individual therapy, couples",
      sup="Individual, group, triadic",
      pop="Teens, adults and older adults",
      mou="In progress, per the directory", bbs="Yes",
      prereq="Training modules", contact="Yajun Zeng",
      email="yajun@between-therapy.com", url="https://between-therapy.com/",
      checked="200, 15 Aug 2026 (final URL after redirect)", src=SRC),
 dict(name="LifePractice", accepting="yes", mode="In person", hrs="10",
      also=None, where="Sacramento", days="Tuesday, Thursday",
      clin="Individual therapy, couples, family, groups",
      sup="Individual, group, triadic", pop="Low-to-mid socioeconomic",
      mou="Alliant, CIIS, Palo Alto, National, Northwestern, Touro, "
          "Pepperdine, Saybrook, Meridian, Walden, Capella",
      bbs="Yes", prereq="Fingerprinting",
      contact="Carisa Sherwood &mdash; Executive Director",
      email="LifePractice@comcast.net", url=None,
      checked="no website published in the directory", src=SRC),
 dict(name="The Liberation Institute", accepting="yes",
      mode="Telehealth only", hrs="10", also="MSW",
      where="All telehealth &mdash; California-wide",
      days="Monday (primarily)",
      clin="Individual therapy, couples, family, groups, outreach",
      sup="Group",
      pop="Individual adults, couples, families; some children and "
          "adolescents",
      mou="Touro University Worldwide, National University, CIIS, "
          "Pacifica, GGU, Cal State East Bay, Wright Institute, "
          "Pepperdine, Columbia, Alliant, UMass Global, Sophia, Capella, "
          "Meridian",
      bbs="Yes", prereq="Liability insurance; onboarding process",
      contact="Oriane Rosenthal &mdash; Clinical Training Program Manager",
      email="oriane@liberationinstitute.org",
      url="https://liberationinstitute.org",
      checked="200, 15 Aug 2026", src=SRC),
 dict(name="Magnolia Women&rsquo;s Recovery Programs", accepting="yes",
      mode="Hybrid", hrs="15", also="MSW", where="Oakland and Hayward",
      days="Monday, Saturday, Sunday",
      clin="Individual therapy, family, groups, crisis intervention",
      sup="Individual, group, triadic",
      pop="Pre- and perinatal mothers in SUD treatment", mou="Pepperdine",
      bbs="Yes",
      prereq="ASAM training modules; registration as a SUD counselor for "
             "the year",
      contact="Caitlin Billings &mdash; Clinical Supervisor",
      email="caitlin.billings@gmail.com",
      url="https://www.magnoliarecovery.org",
      checked="200, 15 Aug 2026", src=SRC),
 dict(name="Hayward Unified School District", accepting="yes",
      mode="In person", hrs="10&ndash;20", also="MSW",
      where="Hayward USD (various school sites)",
      days="Monday &ndash; Friday",
      clin="Individual therapy, groups, crisis intervention, outreach, "
           "classroom presentations",
      sup="Individual",
      pop="Title IX and English Learner (EL) students",
      mou="Cal State East Bay, SF State", bbs="Yes",
      prereq="Contact HR for current requirements",
      contact="HR Department", email="jcaruso@husd.k12.ca.us",
      url="https://www.husd.us/",
      checked="200, 15 Aug 2026; the directory lists husd.k12.ca.us, "
              "which resolved here", src=SRC),
 dict(name="The Psychotherapy Institute (TPI)", accepting="yes",
      mode="Hybrid", hrs="10", also="MSW", where="Berkeley",
      days="Tuesday, Thursday, Friday",
      clin="Individual therapy, couples", sup="Individual, group",
      pop="Low-to-mild needs; 18+; sliding scale only",
      mou="The Wright Institute, Palo Alto University, Notre Dame de "
          "Namur",
      bbs="Yes", prereq="At least one year of coursework",
      contact="Sandra Gaspar", email="sgaspar@tpi-berkeley.org",
      url="https://tpi-berkeley.org",
      checked="200, 15 Aug 2026", src=SRC),
 dict(name="Hively", accepting="yes", mode="Hybrid", hrs="15&ndash;20",
      also=None, where="Oakland and San Leandro",
      days="Monday &ndash; Saturday",
      clin="Individual therapy, couples, family, groups",
      sup="Individual, group",
      pop="All ages; mostly adults with moderate-to-severe symptoms",
      mou="Palo Alto, The Wright, Santa Clara, Pacific Oaks, "
          "St. Mary&rsquo;s, Alliant",
      bbs="Yes",
      prereq="Yes, per the directory &mdash; contact the site for details",
      contact="Susheel Bola &mdash; HR", email="sbola@behively.org",
      url="https://behively.org", checked="200, 15 Aug 2026", src=SRC),
 dict(name="Tri-Valley Haven", accepting="yes", mode="Hybrid", hrs="15",
      also=None, where="Livermore and Pleasanton",
      days="Tuesday, Wednesday, Thursday",
      clin="Individual therapy, family, groups, crisis intervention",
      sup="Individual, group, triadic",
      pop="Domestic violence and sexual assault survivors",
      mou="St. Mary&rsquo;s College, Palo Alto University, Pepperdine "
          "University",
      bbs="Yes", prereq="72 hours of online training",
      contact="Olga Hosny &mdash; Clinical Supervisor",
      email="olga@trivalleyhaven.org", url="https://trivalleyhaven.org/",
      checked="200, 15 Aug 2026 (final URL after redirect)", src=SRC),
 dict(name="La Familia Counseling Service", accepting="yes",
      mode="In person", hrs="10", also="PsyD &amp; MSW", where="Hayward",
      days="Thursday (primarily)",
      clin="Individual therapy, family, crisis intervention, outreach",
      sup="Individual, group",
      pop="Primarily Spanish-speaking / Latine community members; "
          "individual adults, children in schools or clinic, and families",
      mou="BAPIC and individual schools: CSUEB, Wright Institute, GGU, "
          "Dominican, San Jose State, Palo Alto, Samuel Merritt, Santa "
          "Clara",
      bbs="Yes",
      prereq="Some program tracks require Spanish fluency; "
             "Spanish-speaking candidates are strongly encouraged",
      contact="Carolynn Gray, PsyD &mdash; Executive Advisor / Clinical "
              "Training Manager",
      email="cgray@livelafamilia.org", url="https://livelafamilia.org",
      checked="200, 15 Aug 2026", src=SRC),
 dict(name="Discovery Counseling Center of the San Ramon Valley",
      accepting="no", mode="In person", hrs="10&ndash;15", also="PsyD",
      where="San Ramon, Danville and Alamo school sites",
      days="Monday &ndash; Friday",
      clin="Individual therapy, couples, family, groups, collateral "
           "sessions with parents/teachers/school staff",
      sup="Individual, group",
      pop="School-age youth (SCIP school-based program); minors through "
          "seniors in the community mental health clinic",
      mou="Pacifica, CSUEB, Alliant, National, SFSU, USF, "
          "St. Mary&rsquo;s, Wright, CIIS, Santa Clara, Notre Dame de "
          "Namur, Palo Alto, San Jose State, GGU, Grand Canyon, Jessup, "
          "Pepperdine, Saybrook, USC",
      bbs="Yes", prereq="Background check and TB test",
      contact="Christopher Duerrmeier, LMFT &mdash; Clinical Director",
      email="christopherd@discoveryctr.net",
      url="https://www.discoveryctr.net",
      checked="200, 15 Aug 2026", src=SRC),
 dict(name="Bonita House", accepting="yes", mode="In person",
      hrs="15&ndash;20", also="MSW", where="1410 Bonita Ave, Berkeley",
      days="Wednesday (primarily)",
      clin="Individual therapy, groups, crisis intervention",
      sup="Individual, group",
      pop="Dual diagnosis, serious mental illness (SMI), adults",
      mou="Cal State East Bay",
      bbs="Yes", prereq="Background check; contract with school",
      hires_assoc=True,
      contact="Monika Poxon, PsyD &mdash; Clinical Manager",
      email="monikap@bonitahouse.org", url="https://bonitahouse.org/",
      checked="200, 15 Aug 2026 (final URL after redirect)", src=SRC),
 dict(name="Rose Marriage and Family Therapy", accepting="no",
      mode="Hybrid", hrs="15", also=None,
      where="Oakland, Berkeley, San Francisco, Mill Valley",
      days="Monday &ndash; Friday",
      clin="Individual therapy, couples, family, groups",
      sup="Group, triadic",
      pop="Adults, older adults, teens, BIPOC, LGBTQIA+, neurodivergent",
      mou="None currently", bbs="Yes", prereq="Liability insurance",
      hires_assoc=True,
      contact="Jeffrey Gianelli &mdash; Supervisor",
      email="jgia1228@gmail.com", url=None,
      checked="no website published in the directory", src=SRC),
 dict(name="Calliope Coast Therapy Group", accepting="assoc",
      mode="Telehealth only", hrs="15", also=None,
      where="Virtual &mdash; California", days="Monday (primarily)",
      clin="Individual therapy, couples, family, groups",
      sup="Individual, group, triadic",
      pop="Associates supported to work with the population of their "
          "interest",
      mou="None currently", bbs="No",
      prereq="Background check; associate registration (associates only "
             "&mdash; not open to practicum students)",
      hires_assoc=True,
      contact="Karyn Noel &mdash; CEO and Clinical Director",
      email="karyn@calliopetherapy.com",
      url="https://www.calliopetherapy.com",
      checked="200, 15 Aug 2026", src=SRC),
]

STATUS = {"yes": "Accepting students",
          "no": "Not accepting students",
          "assoc": "Associates only &mdash; not practicum"}

JUMPS = [("first", "Read this first"),
         ("sites", "The table"),
         ("details", "Site by site"),
         ("associates", "The three that hire associates"),
         ("use", "How to use this list"),
         ("sources", "Sources")]


def ext(url, text):
    return ('<a href="%s" target="_blank" rel="noopener noreferrer">%s</a>'
            % (url, text))


def site_link(s):
    if s["url"]:
        return ext(s["url"], s["name"])
    return s["name"]


def body():
    n_acc = sum(1 for s in SITES if s["accepting"] == "yes")
    n_hire = sum(1 for s in SITES if s.get("hires_assoc"))
    n_nobbs = sum(1 for s in SITES if s["bbs"] == "No")
    hire_names = [s for s in SITES if s.get("hires_assoc")]

    o = ['<article class="pk-wrap">']
    o.append(pk.hero(
        "East Bay &middot; practicum sites &middot; directory read %s"
        % READ,
        "The East Bay practicum directory, annotated.",
        "%s publishes a real practicum-site directory for the "
        "2026&ndash;27 training year &mdash; the per-site facts no state "
        "or federal file holds: who was accepting students, hours, "
        "supervision form, populations, school MOUs, prerequisites, and "
        "a named contact for every site. This page carries all %d "
        "published entries, <b>with the %s read date on every claim</b>, "
        "each site link fetched before publication. The listing is the "
        "chapter&rsquo;s work; the annotation, dating and statute frame "
        "are this site&rsquo;s."
        % (ext(SRC_URL, SRC_NAME), len(SITES), READ),
        [(str(len(SITES)), "sites with published entries"),
         (str(n_acc), "accepting students at the %s read" % READ_SHORT),
         (str(n_hire), "also hire registered associates"),
         (str(n_nobbs), "listed as not BBS-compliant")],
        JUMPS))

    # ------------------------------------------------------- read this first
    o.append('<section class="pk-sec" id="first">')
    o.append(pk.callout(
        "What this list is, and is not",
        ["This is a <b>curated, named-site directory, and it is not "
         "exhaustive</b>. It reprints one source: %s&rsquo;s public "
         "Practicum Site Directory for the 2026&ndash;27 training year, "
         "read %s. A chapter directory lists the sites that chose to file "
         "an entry with the chapter &mdash; nothing about the sites that "
         "did not. The full universe of settings a trainee may lawfully "
         'work in is the companion page, <a href="%s">the Bay Area '
         "practicum settings directory</a>."
         % (ext(SRC_URL, SRC_NAME), READ, SETTINGS),
         "The frame is the trainee&rsquo;s, and the law draws it: a "
         "practicum student <b>may not work in a private practice or a "
         "professional corporation at all</b> &mdash; %s. Three entries "
         "below say they also hire registered associates; that fact "
         "matters for a different reader at a different stage, and it is "
         "broken out separately so nobody mistakes an associate job for "
         "a practicum seat."
         % ext(LEG % "4980.43.3", "BPC &sect;4980.43.3(b)"),
         "Every acceptance status below is <b>the directory&rsquo;s own "
         "statement at the %s read</b>. The chapter&rsquo;s page is live "
         "and filterable and will drift; re-check it before contacting "
         "anyone. One count to have straight: the directory&rsquo;s own "
         "counter said &ldquo;Showing all 22 sites&rdquo; while %d "
         "entries carried published details at that read &mdash; this "
         "page prints the %d." % (READ, len(SITES), len(SITES))],
        big="One chapter&rsquo;s list, annotated. Not the whole market."))
    o.append("</section>")

    # ------------------------------------------------------------- the table
    o.append('<section class="pk-sec" id="sites">')
    o.append('<p class="pk-k">All %d entries &middot; read %s</p>'
             % (len(SITES), READ))
    o.append('<h2 class="pk-h">The directory in one table.</h2>')
    o.append('<p class="pk-d">Status, mode and hours are the '
             "directory&rsquo;s published values at the %s read. "
             "&ldquo;Not stated&rdquo; means the directory carries no "
             "value &mdash; it is a finding about the entry, not a blank. "
             "A site name links to the website the entry publishes; two "
             "entries publish none, and say so below. BBS-compliant is "
             "<b>the directory&rsquo;s own flag</b>, printed as stated."
             % READ)
    rows = []
    for s in SITES:
        rows.append([
            site_link(s),
            STATUS[s["accepting"]],
            s["mode"],
            (s["hrs"], "n"),
            s["where"],
            (s["bbs"], "m"),
            ("Yes", "m") if s.get("hires_assoc") else "Not stated",
        ])
    o.append(pk.table(
        ["Site", "Status at the %s read" % READ_SHORT, "Mode", "Hrs/wk",
         "Where", "BBS, per directory", "Hires associates"],
        rows,
        caption="Source for every cell: %s, %s&rsquo;s Practicum Site "
                "Directory 2026&ndash;2027 Training Year, read %s. The "
                "listing is the chapter&rsquo;s; credit for assembling "
                "it belongs there."
                % (ext(SRC_URL, "ebcamft.org/practicum-sites"), SRC_NAME,
                   READ),
        minw=880))
    o.append("</section>")

    # ------------------------------------------------------------ the detail
    o.append('<section class="pk-sec" id="details">')
    o.append('<p class="pk-k">The rest of each entry</p>')
    o.append('<h2 class="pk-h">Site by site: supervision, populations, '
             "MOUs, prerequisites, contact.</h2>")
    o.append('<p class="pk-d">Everything below is transcribed from the '
             "same %s entry, same %s read date. The school-MOU line is "
             "worth reading first: if your program is named, the written "
             "site agreement %s requires may already exist, and that is "
             "weeks of lead time you do not have to spend.</p>"
             % (SRC_NAME, READ,
                ext(LEG % "4980.42", "BPC &sect;4980.42(e)")))
    o.append('<div class="pk-v">')
    for i, s in enumerate(SITES, 1):
        line1 = ("<b>Status at the %s read:</b> %s &middot; %s, %s "
                 "hrs/week &middot; <b>Days on-site:</b> %s"
                 % (READ_SHORT, STATUS[s["accepting"]], s["mode"],
                    s["hrs"], s["days"]))
        if s["also"]:
            line1 += " &middot; <b>Also takes:</b> %s" % s["also"]
        line2 = ("<b>Where:</b> %s &middot; <b>Clinical experience:</b> "
                 "%s &middot; <b>Supervision:</b> %s &middot; "
                 "<b>Populations:</b> %s"
                 % (s["where"], s["clin"], s["sup"], s["pop"]))
        line3 = ("<b>School MOUs:</b> %s &middot; <b>BBS-compliant, per "
                 "the directory:</b> %s &middot; <b>Prerequisites:</b> %s"
                 % (s["mou"], s["bbs"], s["prereq"]))
        if s.get("hires_assoc"):
            line3 += (" &middot; <b>Hires registered associates:</b> Yes, "
                      "per the directory")
        contact = ('<b>Contact:</b> %s &mdash; <a href="mailto:%s">%s</a>'
                   % (s["contact"], s["email"], s["email"]))
        if s["url"]:
            contact += " &middot; <b>Site:</b> %s" % ext(
                s["url"], s["url"].split("//")[1].rstrip("/"))
        else:
            contact += (" &middot; <b>Site:</b> no website published in "
                        "the directory entry &mdash; the email is the "
                        "route in")
        o.append('<div><span class="vn">%02d</span>'
                 '<span class="vt">%s</span><p>%s</p><p>%s</p><p>%s</p>'
                 "<p>%s</p></div>"
                 % (i, s["name"], line1, line2, line3, contact))
    o.append("</div>")
    o.append("</section>")

    # ----------------------------------------------------- the three, broken out
    o.append('<section class="pk-sec" id="associates">')
    o.append('<p class="pk-k">A different reader, a different stage</p>')
    o.append('<h2 class="pk-h">The three entries that hire registered '
             "associates.</h2>")
    o.append('<p class="pk-d">A practicum seat and an associate job are '
             "different legal objects: the trainee bar on private "
             "practice &mdash; %s &mdash; lifts only once the associate "
             "registration is issued. Three of the %d entries state, in "
             "the directory itself at the %s read, that they hire "
             "registered associates. The wider associate market is "
             '<a href="%s">its own directory</a>, and the clock rules '
             'are on <a href="%s">the 90-day rule page</a>.</p>'
             % (ext(LEG % "4980.43.3", "BPC &sect;4980.43.3(b)"),
                len(SITES), READ_SHORT, EMPLOYERS, NINETY))
    o.append(pk.table(
        ["Site", "Practicum students", "Associates"],
        [[site_link(hire_names[0]),
          "Yes &mdash; accepting at the %s read" % READ_SHORT,
          "Also hires associates, per the directory"],
         [site_link(hire_names[1]),
          "A practicum site, but not accepting at the %s read"
          % READ_SHORT,
          "Also hires associates, per the directory"],
         [site_link(hire_names[2]),
          "No &mdash; <b>associates only, not open to practicum "
          "students</b>, and the directory flags it as not "
          "BBS-compliant as a practicum entry",
          "Hires associates only &mdash; that is the whole entry"]],
        caption="Calliope Coast&rsquo;s distinction is the "
                "directory&rsquo;s own framing and worth repeating: it "
                "is <b>not a practicum site</b>. A trainee cannot use "
                "it; a registered associate can ask.",
        minw=640))
    o.append("</section>")

    # ------------------------------------------------------------- how to use
    o.append('<section class="pk-sec" id="use">')
    o.append('<p class="pk-k">The order that saves you cycles</p>')
    o.append('<h2 class="pk-h">How to use a curated list.</h2>')
    o.append(pk.numbered([
        ("1", "Read the MOU line before the status line.",
         "A site whose MOU list names your school is weeks closer than "
         "an identical site that would need a new agreement &mdash; "
         "%s puts the written site agreement on the school, and an "
         "existing MOU means that work may be done."
         % ext(LEG % "4980.42", "BPC &sect;4980.42(e)")),
        ("2", "Treat every status as dated, because it is.",
         "Every acceptance value on this page carries the %s read date. "
         "The chapter&rsquo;s page is live and filterable; re-read %s "
         "before writing to a contact, and expect drift &mdash; a "
         "directory that was honest in August is not a promise about "
         "January." % (READ, ext(SRC_URL, "the directory itself"))),
        ("3", "Widen the search past the chapter&rsquo;s list.",
         'This page is curated, not complete. The lawful universe is on '
         '<a href="%s">the settings directory</a>, and <a href="%s">the '
         "method page</a> walks the search itself &mdash; whose job the "
         "placement is at your kind of program, and the questions that "
         "sort sites quickly." % (SETTINGS, METHOD)),
        ("4", "Check the statute frame before anything else convinces "
              "you.",
         'Employee or volunteer, never a 1099; no private practice for '
         "trainees at all; enrollment and the school&rsquo;s agreement "
         'before hours count. The full trainee rules are on <a '
         'href="%s">the practicum page</a>.' % PRACTICUM),
    ]))
    o.append("</section>")

    # ---------------------------------------------------------------- sources
    src, n = pk.sources([
        ("The listing", [
            ("%s, Practicum Site Directory 2026&ndash;2027 Training Year "
             "&mdash; the source of every entry, read %s; the listing is "
             "the chapter&rsquo;s work" % (SRC_NAME, READ), SRC_URL),
        ]),
        ("The statutes", [
            ("BPC &sect;4980.43.3 &mdash; employee or volunteer only; no "
             "private practice or professional corporation for trainees",
             LEG % "4980.43.3"),
            ("BPC &sect;4980.42 &mdash; practicum enrollment, and the "
             "school&rsquo;s written agreement with each site",
             LEG % "4980.42"),
        ]),
    ], note="<b>Every claim on this page is dated %s and will drift.</b> "
            "The directory is the chapter&rsquo;s living document; this "
            "page is a read of it, not a replacement for it. Acceptance "
            "status, hours and contacts change without notice, "
            "&ldquo;Not stated&rdquo; means the entry carries no value, "
            "and nothing here is legal or career advice. Site links were "
            "each fetched on %s; one (the county site) blocks scripted "
            "fetches and is carried on its long-verified link."
            % (READ, READ_SHORT))
    o.append(src)

    o.append("</article>")
    return "".join(o), n


TITLE = "East Bay practicum sites: EB CAMFT directory, annotated"
DESC = ("All 21 published entries in East Bay CAMFT's 2026-27 practicum "
        "site directory: acceptance status at the 15 Aug 2026 read, "
        "hours, supervision, MOUs, named contacts.")

META = pk.meta_block(
    PAGE, TITLE, DESC,
    "licensure", "reference",
    "Which East Bay sites were taking practicum students for 2026-27?",
    "Every published entry in the chapter's directory annotated with the "
    "statutes, every site link fetched, every claim dated",
    "21 sites, 3 hire associates",
    weight=4)

# Job-availability language stays banned; the ACCEPTANCE column is allowed
# because it is the source's own published, dated statement - the whole
# point of a curated directory - and the guard below enforces the dating.
BANNED = ["is hiring", "now hiring", "has openings", "open positions",
          "vacanc", "apply now", "spots available", "positions available",
          "job opening"]


def main():
    assert 15 <= len(TITLE) <= 68, "title length %d" % len(TITLE)
    assert 70 <= len(DESC) <= 168, "description length %d" % len(DESC)
    for s in SITES:
        for k in ("name", "accepting", "mode", "hrs", "where", "days",
                  "clin", "sup", "pop", "mou", "bbs", "prereq", "contact",
                  "email", "checked", "src"):
            if not s.get(k):
                sys.exit("build_bayarea_practicum: %s has no %r - write "
                         "the value or the 'Not stated' finding"
                         % (s["name"], k))

    html_body, n_sources = body()
    head, header, footer, links, scripts = pk.chrome_parts(DONOR)
    html = pk.assemble(head, META, header, html_body, footer, links,
                       scripts)
    path = os.path.join(SITE, PAGE)
    open(path, "w", encoding="utf-8").write(html)

    s = open(path, encoding="utf-8").read()
    problems = pk.check_page(path, [
        ("the 4980.43.3(b) trainee bar", "4980.43.3"),
        ("the 4980.42(e) site-agreement rule", "4980.42"),
        ("the source credit", "East Bay CAMFT"),
        ("the source link", "ebcamft.org/practicum-sites"),
        ("the curated-not-exhaustive sentence", "it is not exhaustive"),
        ("the not-the-whole-market verdict", "Not the whole market."),
        ("the Not stated finding", "Not stated"),
        ("the Calliope distinction", "not open to practicum students"),
        ("the count discrepancy", "Showing all 22 sites"),
        ("the drift warning", "will drift"),
    ], [j for j, _ in JUMPS])

    bad = []
    art = pk.article(s)
    low = art.lower()
    for phrase in BANNED:
        if phrase in low:
            bad.append("availability language: %r" % phrase)
    if low.count("read".lower()) < 3 or READ not in art:
        bad.append("the %s read date is not carried through" % READ)
    for site in SITES:
        if site["name"] not in art:
            bad.append("site missing: %s" % site["name"])
        if site["url"] and ('href="%s"' % site["url"]) not in art:
            bad.append("verified link missing: %s" % site["url"])
    if art.count("no website published in the directory") < 2:
        bad.append("the two email-only entries must carry the no-site "
                   "finding")
    detail = art[art.find('id="details"'):art.find('id="associates"')]
    n_details = detail.count('<span class="vn">')
    if n_details != len(SITES):
        bad.append("detail entries: %d against %d sites"
                   % (n_details, len(SITES)))
    for a in ("target=\"_blank\"",):
        if a not in art:
            bad.append("external links must open in a new window")
    # every external link opens in a new window with rel noopener
    import re as _re
    for m in _re.finditer(r'<a href="https?://[^"]*"[^>]*>', art):
        tag = m.group(0)
        if "leginfo" in tag or "therapistsupport" in tag:
            pass
        if "target=" not in tag or "noopener" not in tag:
            bad.append("external link without new-window/noopener: %s"
                       % tag[:80])
            break

    if bad or problems:
        for b in bad:
            print("GUARD %s: %s" % (PAGE, b))
        sys.exit(1)
    print("build_bayarea_practicum: %s written - %d entries, %d also "
          "hire associates, %d sources, every claim dated %s"
          % (PAGE, len(SITES),
             sum(1 for x in SITES if x.get("hires_assoc")), n_sources,
             READ))


if __name__ == "__main__":
    main()
