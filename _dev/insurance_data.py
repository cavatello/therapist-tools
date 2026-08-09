#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Data for therapy-liability-insurance-california.html.

Every figure here is either published by the carrier or reported by a named
person in a linkable post. Nothing is estimated. Where a carrier does not
publish a price, the field says so rather than carrying a guess.

TWO THINGS THIS FILE DELIBERATELY KEEPS SEPARATE

1. `published` — the carrier's own number, with the URL it appears on.
2. `reported` — what a practitioner said they actually paid, with who, when,
   and where they said it.

They disagree, often, and the disagreement is the useful part: CPH publishes
$320 for a full-time California MFT and Californians report $110, $284 and
$591, because discounts, general liability and cyber all move the number.
Presenting only one of the two would be presenting a number nobody pays.

A FRESHNESS PROBLEM WORTH KNOWING ABOUT

CPH is the only carrier that publishes a California MFT rate table at all, and
the PDF it lives in returns `last-modified: Thu, 01 Jun 2023`. It is the best
published figure available anywhere and it is two years old. Every use of it on
the page is stamped accordingly.
"""

CHECKED = "9 August 2026"

# ---------------------------------------------------------------- carriers

CARRIERS = [
    {
        "key": "cph",
        "name": "CPH &amp; Associates",
        "url": "https://cphins.com/licensed-marriage-and-family-therapist-lmft/",
        "agency": "CPH &amp; Associates (an agency, not an insurer)",
        "underwriter": "Philadelphia Indemnity Insurance Company and Tokio "
                       "Marine Specialty Insurance Company",
        "ambest": "A++ (Superior)",
        "ambest_url": "https://ratings.ambest.com/DisclosurePDF.aspx?AMBNum=3616",
        "form": "Occurrence",
        "limits": "$1M / $3M and $1M / $5M",
        "endorsed_by": "CAMFT and AAMFT",
        "tags": ["amft", "solo", "student", "telehealth", "office"],
        "headline": "$320",
        "headline_note": "full-time California MFT, $1M/$3M, before discounts",
        "published": [
            ("Student in an accredited program", "$15", "$1M/$5M only"),
            ("AMFT / post-master&rsquo;s under supervision", "$90", "$1M/$3M"),
            ("Employed, or up to 10 hrs/wk self-employed", "$115", "$1M/$3M"),
            ("Employed, or 11&ndash;20 hrs/wk self-employed", "$180", "$1M/$3M"),
            ("Employed, or over 20 hrs/wk self-employed", "$320", "$1M/$3M"),
        ],
        "published_url": "https://cphins.com/wp-content/uploads/2023/02/CAMFT.pdf",
        "published_note": "CPH&rsquo;s CAMFT application, section 2. The PDF was "
                          "last modified June 2023 and CPH publishes no newer "
                          "rate card &mdash; treat it as last-published, not "
                          "guaranteed-current. A $10 administrative fee is "
                          "added to every policy.",
        "board_defense": "$35,000",
        "board_defense_max": "$100,000 for +$100/yr",
        "extras": [
            ("Defense costs", "Unlimited, and outside the liability limit"),
            ("Deposition representation", "$10,000 per deposition"),
            ("Attorney helpline", "2 hours per policy period"),
            ("General liability", "+$182/yr, or +$332 with $15,000 business property"),
            ("Cyber / HIPAA", "+$87/yr for $15,000; +$141 for $25,000. Excludes ransomware"),
            ("Prior acts (&ldquo;nose&rdquo;)", "$175, one time"),
            ("Sexual misconduct", "Defense only"),
        ],
        "discounts": "50% newly licensed year one, 25% year two, 10% for "
                     "law-and-ethics CEUs, 5% for applying online. Students and "
                     "associates get no discounts at all.",
        "entity": "Does not cover your corporation. CPH states an individual "
                  "policy &ldquo;will only cover you as an individual provider "
                  "and does not cover your business entity, even if you are the "
                  "sole owner,&rdquo; and you cannot add a company you own as an "
                  "additional insured. Hiring W-2 employees forces you to a "
                  "separate entity policy, priced on headcount and not published.",
        "entity_url": "https://cphins.com/business-entities/",
        "ca_note": "CPH rates California as its own class. Its AAMFT rate sheet "
                   "prints the two side by side: a full-time California MFT is "
                   "<b>$320</b> where the same therapist in any other state is "
                   "<b>$246</b>, and part-time is <b>$180</b> against <b>$123</b>. "
                   "That is a 30&ndash;46% California loading, published by the "
                   "carrier.",
        "ca_note_url": "https://cphins.com/wp-content/uploads/2023/02/AAMFT.pdf",
        "verdict": "The default for a California MFT, and the reason is the "
                   "attorney helpline rather than the price.",
        "verdict_why": "Seven separate therapists describe actually using CPH&rsquo;s "
                       "legal line &mdash; for a subpoena, a criminal-trial witness "
                       "summons, a supervision question &mdash; and all seven were "
                       "positive. That is the strongest single pattern in the "
                       "public record, and it is exactly what HPSO&rsquo;s critics "
                       "say HPSO lacks.",
        "against": [
            "Does not cover discrimination claims, which a therapist found out "
            "the hard way.",
            "The cyber sublimit is $15,000&ndash;$25,000 and excludes ransomware "
            "&mdash; below what some 1099 contracts now require.",
            "Policies do not auto-renew. You reapply every year, and two lapsed "
            "or cancelled policies makes you ineligible.",
            "Three BBB reviews average 1.33 out of 5, including one therapist "
            "declined on reapplication after a non-renewal.",
        ],
    },
    {
        "key": "hpso",
        "name": "HPSO",
        "url": "https://www.hpso.com/Insurance-for-you/Individual-Practitioners/Counselors",
        "agency": "Affinity Insurance Services, an Aon company",
        "underwriter": "American Casualty Company of Reading, Pennsylvania, a "
                       "CNA company",
        "ambest": "A+ (Superior)",
        "ambest_url": "https://ratings.ambest.com/disclosurepdf.aspx?ambnum=2127",
        "form": "Occurrence",
        "limits": "$1M / $3M",
        "endorsed_by": "Many national associations; not CAMFT",
        "tags": ["solo", "telehealth"],
        "headline": "from $153",
        "headline_note": "the only price HPSO publishes anywhere",
        "published": [
            ("Counselors, floor rate", "from $153", "not California-specific"),
        ],
        "published_url": "https://landing.hpso.com/counselors/",
        "published_note": "HPSO publishes no rate table by state, hours or "
                          "limit. Everything else is quote-only.",
        "board_defense": "$25,000",
        "board_defense_max": "not published",
        "extras": [
            ("Defense costs", "Outside the liability limit"),
            ("Subpoena assistance", "$10,000 aggregate, insurer-appointed attorney"),
            ("Defendant expense", "$1,000/day up to $25,000"),
            ("HIPAA proceedings", "Patient notification to $25,000 plus fines where permitted"),
            ("Abuse and molestation", "$25,000 sublimit"),
        ],
        "discounts": "New graduate up to 60% in year one, 40% year two, 20% "
                     "year three; 10% three-year risk-management discount.",
        "entity": "A separate &ldquo;Businesses or Practices&rdquo; line with its own "
                  "phone number. No premiums published.",
        "entity_url": "https://www.hpso.com/Insurance-for-you/Individual-Practitioners/Counselors",
        "ca_note": "",
        "ca_note_url": "",
        "verdict": "Widely held, and the migration runs one way.",
        "verdict_why": "Four therapists describe leaving HPSO for CPH &mdash; over "
                       "the missing legal consultation, over service, over a "
                       "four-month fight to add general liability. Nobody in the "
                       "public record describes moving the other way. HPSO&rsquo;s "
                       "genuine strength is its published claim research, which "
                       "therapists cite approvingly.",
        "against": [
            "The most-upvoted structural criticism of any carrier: a therapist "
            "of ten years discovered HPSO had no legal consultation service. "
            "&ldquo;Honestly I&rsquo;m a little taken aback by how vulnerable I feel and "
            "how unknowingly unprotected I have been for so long.&rdquo;",
            "A January 2026 BBB complaint alleges the license-protection benefit "
            "is a reimbursement, not a defense: &ldquo;At no point did Affinity "
            "explain that the so-called &lsquo;license protection benefit&rsquo; was merely "
            "an ancillary reimbursement benefit.&rdquo;",
            "23 BBB complaints in three years against the parent agency, "
            "including a bounced refund cheque and billing continuing eleven "
            "months after cancellation.",
            "Certificate-of-insurance delays have cost people credentialing "
            "deadlines: &ldquo;BCBS gave me TWO BUSINESS DAYS to respond.&rdquo;",
        ],
    },
    {
        "key": "trust",
        "name": "The Trust",
        "url": "https://www.trustinsurance.com/insurance-programs/allied-healthcare/marriage-and-family-counselor-or-therapist/",
        "agency": "Trust Risk Management Services",
        "underwriter": "Not named on the allied-health pages. ACE American "
                       "(Chubb) underwrites the psychologist program",
        "ambest": "A++ (Superior) for the psychologist program&rsquo;s carrier",
        "ambest_url": "https://ratings.ambest.com/DisclosurePDF.aspx?AMBNum=2257",
        "form": "Occurrence",
        "limits": "$1M / $3M standard, others on request",
        "endorsed_by": "State psychological associations",
        "tags": ["solo", "office", "group"],
        "headline": "not published",
        "headline_note": "MFT premiums are quote-only",
        "published": [],
        "published_url": "https://www.trustinsurance.com/insurance-programs/allied-healthcare/marriage-and-family-counselor-or-therapist/",
        "published_note": "The Trust publishes rate tables for psychologists and "
                          "none for the allied-health program MFTs buy under.",
        "board_defense": "included, amount not published",
        "board_defense_max": "not published",
        "extras": [
            ("General liability", "Included in the policy, not an add-on"),
            ("Deductible", "None. First-dollar defense and indemnity"),
            ("Defense costs", "Outside the limit"),
            ("HIPAA", "Fines, penalties and consumer notification included"),
            ("Territory", "24-hour worldwide, if the claim is brought in the US or Canada"),
        ],
        "discounts": "50% newly licensed, 50% part-time at 24 hours or less, "
                     "10% CE, 10% for switching carriers, 5% online &mdash; "
                     "capped at 50% combined.",
        "entity": "Group practices and entities may buy separate general "
                  "liability limits. Not published.",
        "entity_url": "https://www.trustinsurance.com/about/frequently-asked-questions/professional-liability/group-coverage-vicarious-liability/",
        "ca_note": "The one California data point in the public record is a "
                   "psychologist, not an MFT: quoted <b>$1,126/yr</b> for eight "
                   "hours a week of part-time practice. They went with CPH "
                   "instead. Psychologist rates are not MFT rates &mdash; but The "
                   "Trust does not publish MFT rates for anyone to compare.",
        "ca_note_url": "https://www.reddit.com/r/Psychologists/comments/1l2obm3/liability_insurance_premiums_help/",
        "verdict": "The one that includes general liability without an add-on.",
        "verdict_why": "If you rent an office, general liability is not optional "
                       "&mdash; your landlord requires it. The Trust folds it in; "
                       "CPH charges $182 for it. One therapist moved to The "
                       "Trust for exactly that reason and landed around $375 all "
                       "in.",
        "against": [
            "No published price of any kind for MFTs.",
            "The underwriter is not named on the allied-health pages.",
            "The rate pages carry an effective date of 1999, which is almost "
            "certainly a stale field rather than a real date &mdash; but it means "
            "you cannot tell how current anything is.",
        ],
    },
    {
        "key": "apa",
        "name": "American Professional Agency",
        "url": "https://www.americanprofessional.com/covered-professions/marriage-family-therapist/",
        "agency": "American Professional Agency",
        "underwriter": "Allied World Insurance Company (Fairfax)",
        "ambest": "A+ (Superior)",
        "ambest_url": "https://awac.com/ratings/",
        "form": "Claims-made",
        "limits": "up to $2M / $4M",
        "endorsed_by": "No association membership required",
        "tags": ["incorporated", "solo"],
        "headline": "not published",
        "headline_note": "the MFT rate schedule is not on their site",
        "published": [],
        "published_url": "https://www.americanprofessional.com/wp-content/uploads/MHC_Rates.pdf",
        "published_note": "MFTs are rated in &ldquo;Group 0&rdquo;, which appears in no "
                          "public PDF. Their <i>mental health counselor</i> "
                          "schedule is reachable but undated and rates a "
                          "different group &mdash; do not read it as MFT pricing.",
        "board_defense": "$5,000 per proceeding, no annual aggregate",
        "board_defense_max": "$150,000",
        "extras": [
            ("Board defense structure", "The only program with no annual cap on the base benefit"),
            ("Subpoena", "$5,000 per proceeding, no annual aggregate"),
            ("Loss of earnings", "$1,000 per day while assisting the defense"),
            ("Premises liability", "Included at no extra cost"),
            ("Telehealth and forensic work", "Both included"),
            ("Free tail", "On death, disability, or retirement at 55+ with five years held"),
        ],
        "discounts": "35% part-time at 20 hours or less across all positions; "
                     "5% for three hours of risk-management CE; separate rates "
                     "for W-2 employed practitioners.",
        "entity": "<b>The best answer of any carrier for an incorporated solo.</b> "
                  "Their rate schedule states a P.C. or P.A. &ldquo;with no employees "
                  "other than the owner qualifies for the Individual rate&rdquo; "
                  "&mdash; the corporation is named at no extra premium. Every "
                  "other carrier surveyed either refuses the entity or sells you "
                  "a second policy.",
        "entity_url": "https://www.americanprofessional.com/wp-content/uploads/MHC_Rates.pdf",
        "ca_note": "",
        "ca_note_url": "",
        "verdict": "Cheap at the front, and the cheapness is structural.",
        "verdict_why": "This is the only claims-made policy in the set. A "
                       "claims-made premium starts low and steps up for six or "
                       "seven years, and you need tail coverage to leave. The "
                       "Trust&rsquo;s own published table shows the shape exactly: a "
                       "California non-psychologist pays $103 in year one and "
                       "$529 at maturity &mdash; year one is 19% of the real price.",
        "against": [
            "&ldquo;They only do claims-based policies with an option to add on tail "
            "coverage at 175% of your premium, which is why they are so much "
            "cheaper than everyone else up front.&rdquo;",
            "&ldquo;Be sure that the APA rate is not a promotional rate and the cost "
            "doubles the next year.&rdquo;",
            "A psychologist reports their consultation line assigns "
            "non-psychologists: &ldquo;they can&rsquo;t really help you with any ethics "
            "consultation needs.&rdquo;",
        ],
    },
    {
        "key": "berxi",
        "name": "Berxi",
        "url": "https://www.berxi.com/insurance/counselor/",
        "agency": "Berkshire Hathaway Global Insurance Services, CA license #0K09397",
        "underwriter": "Berkshire Hathaway Specialty Insurance Company",
        "ambest": "A++ (Superior)",
        "ambest_url": "https://ratings.ambest.com/DisclosurePDF.aspx?AMBNum=864",
        "form": "Occurrence and claims-made",
        "limits": "$500K/$1M up to $2M/$6M",
        "endorsed_by": "None &mdash; sells direct",
        "tags": ["solo", "telehealth"],
        "headline": "$169",
        "headline_note": "Berxi&rsquo;s own California sample, at $500K/$1M",
        "published": [
            ("California counselor/therapist, full-time", "$169", "$500K/$1M occurrence"),
            ("Self-employed family/marriage counselor", "$224", "$1M/$3M occurrence, Massachusetts"),
            ("General liability, added", "$150", "$1M/$1M"),
        ],
        "published_url": "https://www.berxi.com/resources/articles/best-malpractice-insurance-for-mental-health-counselors/",
        "published_note": "The $169 is Berxi&rsquo;s published California sample and "
                          "it is at a <b>$500,000</b> per-claim limit &mdash; half "
                          "what Headway, Alma and most payers require. It is not "
                          "comparable to the $1M/$3M prices elsewhere on this "
                          "page.",
        "board_defense": "$25,000",
        "board_defense_max": "not published",
        "extras": [
            ("Consent to settle", "&ldquo;We won&rsquo;t settle a claim without your consent&rdquo;"),
            ("Reputation coverage", "$50,000 per claim"),
            ("HIPAA defense", "$25,000 per policy period"),
            ("Wage loss / deposition", "up to $1,000 per day"),
            ("Deductible", "None. Defense outside the limits"),
        ],
        "discounts": "Student discounts available. No published schedule.",
        "entity": "Not published.",
        "entity_url": "https://www.berxi.com/faq/",
        "ca_note": "",
        "ca_note_url": "",
        "verdict": "The cheapest quotes, and two warnings attached.",
        "verdict_why": "A therapist quoted $97 against $225&ndash;375 elsewhere "
                       "asked publicly whether Berxi was legitimate. Nobody "
                       "answered. The underwriter is Berkshire Hathaway, which "
                       "is about as solid as insurers get &mdash; the questions "
                       "are about the product, not the balance sheet.",
        "against": [
            "&ldquo;Berxi was around $130, but they told me it slowly creeps up to "
            "the &lsquo;regular&rsquo; rate after 5 years. It was simply an intro rate.&rdquo; "
            "(reported by a psychiatric NP, not a therapist &mdash; but it is a "
            "carrier-level mechanism)",
            "A practitioner was told Berxi &ldquo;don&rsquo;t support virtual practices&rdquo; "
            "and could not get that confirmed in writing. If you are "
            "telehealth-only, get the answer by email before you buy.",
            "The headline California figure is at a $500K limit that will fail "
            "Headway, Alma and Blue Shield credentialing.",
        ],
    },
    {
        "key": "proliability",
        "name": "Proliability",
        "url": "https://www.proliability.com/professional-liability-insurance/mental-health-professionals.html",
        "agency": "AMBA (formerly Mercer Consumer), CA license #0I96562",
        "underwriter": "Liberty Insurance Underwriters Inc. (Liberty Mutual)",
        "ambest": "A (Excellent)",
        "ambest_url": "https://ratings.ambest.com/DisclosurePDF.aspx?AMBNum=3794",
        "form": "Occurrence",
        "limits": "up to $1M / $3M",
        "endorsed_by": "Various associations",
        "tags": ["solo", "group"],
        "headline": "not published",
        "headline_note": "quote-only",
        "published": [],
        "published_url": "https://www.proliability.com/professional-liability-insurance/mental-health-professionals.html",
        "published_note": "No premiums published; the site blocks automated "
                          "retrieval on its quote pages.",
        "board_defense": "$25,000 per incident / $100,000 per year",
        "board_defense_max": "not published",
        "extras": [
            ("Deposition expense", "$15,000 per policy period"),
            ("Wage loss", "$2,500 per day, $35,000 per period &mdash; the highest found"),
            ("HIPAA", "$50,000 &mdash; the highest sublimit of any program here"),
            ("Risk management", "30-minute Advice-on-Demand consultations"),
        ],
        "discounts": "Not published.",
        "entity": "Group quote path available; media sublimits are larger for a "
                  "group practice.",
        "entity_url": "https://www.proliability.com/professional-liability-insurance/mental-health-professionals.html",
        "ca_note": "",
        "ca_note_url": "",
        "verdict": "The strongest sublimits on paper, and almost no therapist "
                   "evidence behind them.",
        "verdict_why": "$100,000 a year of board defense and $50,000 of HIPAA "
                       "coverage are the best numbers in this table. But not one "
                       "therapist in the public record reports a Proliability "
                       "price or a Proliability claim. Every report found was "
                       "from a nurse, a dietitian or a music therapist.",
        "against": [
            "No published prices at all.",
            "Same parent agency as HPSO and NSO &mdash; Affinity/Aon &mdash; so the "
            "BBB complaint file above applies to it too.",
        ],
    },
    {
        "key": "cmf",
        "name": "CM&amp;F Group",
        "url": "https://www.cmfgroup.com/professional-liability-insurance/counseling-professional-insurance/marriage-family-counselor-insurance/",
        "agency": "CM&amp;F Group (Specialty Program Group)",
        "underwriter": "Not named on the public page",
        "ambest": "&ldquo;A++&rdquo; claimed, carrier unnamed",
        "ambest_url": "",
        "form": "Occurrence",
        "limits": "$1M / $6M",
        "endorsed_by": "Runs the Headway provider program",
        "tags": ["solo", "telehealth", "headway"],
        "headline": "not published",
        "headline_note": "quote-only",
        "published": [],
        "published_url": "https://www.cmfgroup.com/professional-liability-insurance/counseling-professional-insurance/marriage-family-counselor-insurance/",
        "published_note": "&ldquo;The rate you see is the rate you will pay based on "
                          "the questions you answered.&rdquo;",
        "board_defense": "$35,000 per claim / $100,000 aggregate",
        "board_defense_max": "not published",
        "extras": [
            ("Aggregate limit", "$6,000,000 &mdash; the highest standard aggregate found"),
            ("HIPAA defense", "$35,000 including relevant fines"),
            ("Deposition", "$25,000"),
            ("Telemedicine", "Included for services within scope"),
        ],
        "discounts": "Not published.",
        "entity": "Not published.",
        "entity_url": "",
        "ca_note": "",
        "ca_note_url": "",
        "verdict": "The Headway route, and the highest aggregate.",
        "verdict_why": "CM&amp;F runs the partner program Headway points its "
                       "providers at. If you are credentialing through Headway "
                       "this is the path of least friction. No therapist price "
                       "reports exist for it.",
        "against": [
            "Will not name its underwriter, while advertising that "
            "underwriter&rsquo;s A++ rating.",
            "No therapist has publicly reported what they pay.",
        ],
    },
    {
        "key": "lockton",
        "name": "Lockton Affinity Health",
        "url": "https://locktonaffinityhealth.com/counselors/",
        "agency": "Lockton Affinity",
        "underwriter": "Not named on the public page",
        "ambest": "not published",
        "ambest_url": "",
        "form": "not published",
        "limits": "$500K/$500K up to $2M/$4M",
        "endorsed_by": "Association programs",
        "tags": ["student", "solo"],
        "headline": "$117",
        "headline_note": "at $500K/$500K &mdash; a quarter of the standard limit",
        "published": [
            ("Student", "$20", "$500K/$500K"),
            ("Professional", "$117", "$500K/$500K"),
        ],
        "published_url": "https://locktonaffinityhealth.com/counselors/",
        "published_note": "Both figures are at a $500,000 aggregate. Headway, "
                          "Alma, Blue Shield and Optum all require more.",
        "board_defense": "included, amount not published",
        "board_defense_max": "not published",
        "extras": [
            ("General liability", "Included automatically"),
            ("Loss of earnings", "up to $500 per day"),
        ],
        "discounts": "Not published.",
        "entity": "Not published.",
        "entity_url": "",
        "ca_note": "",
        "ca_note_url": "",
        "verdict": "The cheapest number on the page, at the smallest limit.",
        "verdict_why": "$117 looks like the bargain of the table until you "
                       "notice the aggregate is $500,000 where everyone else "
                       "quotes $3,000,000. It does not publish its policy form, "
                       "its carrier, or its board-defense sublimit.",
        "against": [
            "Occurrence or claims-made is not stated anywhere. That is the "
            "single most consequential fact about a policy and it is missing.",
            "The underwriter is not named.",
        ],
    },
]

# ------------------------------------------------- what people actually pay

REPORTED = [
    # (carrier key, amount, who, when, url, is_california)
    ("cph", "$110/yr", "an LMFT, in a California-specific thread", "Jan 2026",
     "https://www.reddit.com/r/therapists/comments/1qff1jh/cheapest_malpractice_insurance_for_ca/", True),
    ("cph", "$280/yr", "a Californian, at $1M/$3M &mdash; and $180 at $100K/$300K",
     "Jan 2026",
     "https://www.reddit.com/r/therapists/comments/1qff1jh/cheapest_malpractice_insurance_for_ca/", True),
    ("cph", "$76/yr", "a newly licensed therapist at $1M/$5M &mdash; &ldquo;I was "
     "expecting a lot more than that&rdquo;", "Mar 2026",
     "https://www.reddit.com/r/therapists/comments/1s8wn2l/obtaining_liability_insurance_as_a_newly_licensed/", False),
    ("cph", "$311/yr", "a therapist comparing against a $1,000 HPSO quote", "Dec 2025",
     "https://www.reddit.com/r/therapists/comments/1piluu2/whats_an_average_quote_for_malpractice_insurance/", False),
    ("cph", "$327/yr", "at $1M/$5M with cyber added", "Nov 2025",
     "https://www.reddit.com/r/therapists/comments/1onjn0c/malpractice_insurance/", False),
    ("cph", "$451/yr", "hourly-rented office plus 1099 work, no cyber, no property",
     "Dec 2025",
     "https://www.reddit.com/r/therapists/comments/1ppeas3/is_general_liability_insurance_needed/", False),
    ("cph", "$591/yr", "including renter&rsquo;s and general liability, &ldquo;because my "
     "landlord requires it&rdquo;", "Dec 2025",
     "https://www.reddit.com/r/therapists/comments/1pznbji/private_practice_insurance_policy_recommendations/", False),
    ("cph", "$600/yr", "&ldquo;for my virtual and in person practice&rdquo;", "Dec 2025",
     "https://www.reddit.com/r/therapists/comments/1piluu2/whats_an_average_quote_for_malpractice_insurance/", False),
    ("cph", "$70 &rarr; $300/yr", "an LCSW, before and after forming an LLC", "Jun 2025",
     "https://www.reddit.com/r/socialwork/comments/1kzva84/being_a_private_supervisor_and_liability_insurance/", False),

    ("hpso", "$113/yr", "a hospital-system employee carrying their own policy", "Dec 2025",
     "https://www.reddit.com/r/therapists/comments/1piluu2/whats_an_average_quote_for_malpractice_insurance/", False),
    ("hpso", "$130 &rarr; $147/yr", "one renewal, a 13% increase", "Mar 2025",
     "https://www.reddit.com/r/socialwork/comments/1j81mmt/liability_insurance/", False),
    ("hpso", "$147/yr", "a social worker", "Jun 2024",
     "https://www.reddit.com/r/socialwork/comments/1ddjjf5/all_things_liability_insurance/", False),
    ("hpso", "$250/yr", "a therapist", "Dec 2025",
     "https://www.reddit.com/r/therapists/comments/1piluu2/whats_an_average_quote_for_malpractice_insurance/", False),
    ("hpso", "$1,000/yr", "quoted for $1M/$3M, fully virtual, one employee, Texas",
     "Dec 2025",
     "https://www.reddit.com/r/therapists/comments/1piluu2/whats_an_average_quote_for_malpractice_insurance/", False),
    ("hpso", "$6,400/yr", "quoted to an LCSW in New Jersey at $1M/$3M &mdash; "
     "&ldquo;I&rsquo;m assuming this is some kind of mistake&rdquo;", "Apr 2025",
     "https://www.reddit.com/r/therapists/comments/1jyaq9v/liability_insurance/", False),

    ("trust", "$1,126/yr", "a California <b>psychologist</b> quoted for eight "
     "hours a week part-time. They bought CPH instead", "Jun 2025",
     "https://www.reddit.com/r/Psychologists/comments/1l2obm3/liability_insurance_premiums_help/", True),
    ("trust", "~$375/yr", "a therapist who left CPH, general liability included",
     "Dec 2025",
     "https://www.reddit.com/r/therapists/comments/1ppeas3/is_general_liability_insurance_needed/", False),

    ("apa", "$76/yr", "&ldquo;for my situation&rdquo;", "Mar 2025",
     "https://www.reddit.com/r/socialwork/comments/1j81mmt/liability_insurance/", False),
    ("apa", "$67/yr", "a first-year base rate, against a $144 Preferra renewal",
     "Jun 2026",
     "https://www.reddit.com/r/socialwork/comments/1u3vpvl/professional_insurance/", False),

    ("berxi", "$97/yr", "claims-made, quoted against $225&ndash;375 elsewhere &mdash; "
     "&ldquo;Are they legit?&rdquo; No one answered", "Dec 2024",
     "https://www.reddit.com/r/therapists/comments/1h9l46j/berxi_for_liability_insurance/", False),
    ("berxi", "&ldquo;rates have gone up a bit&rdquo;", "a social worker, several years in",
     "Dec 2025",
     "https://www.reddit.com/r/socialwork/comments/1pp6ytg/malpractice_insurance_recommendations/", False),

    ("cmf", "$650/yr", "quoted to a California S-corp nurse practitioner &mdash; "
     "against $2,500 from HPSO for the same coverage. <b>Not a therapist</b>",
     "Jun 2025",
     "https://www.reddit.com/r/nursepractitioner/comments/1l9t76g/malpractice_insurance/", True),
]

# --------------------------------------------------------------- the law

LEGAL = [
    {
        "q": "Does the BBS require malpractice insurance?",
        "a": "<b>No.</b> Nothing in Business and Professions Code &sect;&thinsp;4980 "
             "et seq. or in 16 CCR Division 18 conditions licensure, "
             "registration or renewal on carrying professional liability "
             "insurance. The word &ldquo;insurance&rdquo; appears in the BBS statutes "
             "mainly as a <i>coursework topic</i> in law-and-ethics training.",
        "cite": "BBS Statutes and Regulations, January 2026",
        "url": "https://www.bbs.ca.gov/pdf/publications/lawsregs.pdf",
    },
    {
        "q": "Does a California MFT corporation have to carry it?",
        "a": "<b>No &mdash; and the reason is worth knowing.</b> B&amp;P "
             "&sect;&thinsp;4988.2(b) gives the Board the power to require that "
             "an MFT corporation &ldquo;provide adequate security by insurance or "
             "otherwise for claims against it by its patients.&rdquo; The Board has "
             "never used it. 16 CCR Article 4.5 contains two live sections &mdash; "
             "corporate naming and share transfer &mdash; and nothing about "
             "insurance.<br><br>The contrast is sharp. The Board of Accountancy "
             "was given the same power and <i>did</i> use it: 16 CCR "
             "&sect;&thinsp;75.8 requires an accountancy corporation to carry at "
             "least $100,000 per claim per licensee, and if it does not, "
             "&ldquo;each and every shareholder&hellip; shall be deemed to have agreed to "
             "be jointly and severally liable.&rdquo; The liability shield goes away. "
             "No such rule exists for MFT corporations.",
        "cite": "B&amp;P &sect;&thinsp;4988.2; 16 CCR &sect;&thinsp;75.8",
        "url": "https://california.public.law/codes/business_and_professions_code_section_4988.2",
    },
    {
        "q": "So who does require it?",
        "a": "Everyone you want to be paid by. <b>Medi&#8209;Cal is a real "
             "regulation</b> &mdash; 22 CCR &sect;&thinsp;51000.30 requires "
             "enrolling providers to carry liability insurance, and DHCS sets "
             "the amount at not less than <b>$100,000 per claim / $300,000 "
             "aggregate</b>. Every commercial payer and platform sets its own "
             "figure by contract. And your landlord will require <i>general</i> "
             "liability, which is a different policy entirely.",
        "cite": "22 CCR &sect;&thinsp;51000.30; DHCS insurance clarification",
        "url": "https://www.dhcs.ca.gov/wp-content/uploads/2025/10/INSURANCEREQUIREMENTCLARIFICATIONWFORM.pdf",
    },
    {
        "q": "Can an associate have private clients on the side?",
        "a": "<b>No.</b> B&amp;P &sect;&thinsp;4980.43.3 says an associate "
             "&ldquo;shall only perform mental health and related services as an "
             "employee or volunteer, and not as an independent contractor,&rdquo; "
             "shall &ldquo;not receive any remuneration from patients or clients,&rdquo; "
             "and shall work only where the employer permits business to be "
             "conducted. So the whole &ldquo;does my employer&rsquo;s policy cover my own "
             "clients&rdquo; question does not arise for an AMFT &mdash; there are no "
             "own clients to cover.",
        "cite": "B&amp;P &sect;&thinsp;4980.43.3",
        "url": "https://leginfo.legislature.ca.gov/faces/codes_displaySection.xhtml?lawCode=BPC&sectionNum=4980.43.3.",
    },
]

# ------------------------------------------------- what payers actually ask

PAYERS = [
    ("Headway", "$1M / $1M", "In California. The certificate must name "
     "<b>you individually</b>, not just your LLC, and must be professional "
     "liability &mdash; not student, general or cyber cover.",
     "https://help.headway.co/hc/en-us/articles/4406639198484-Certificates-of-insurance-COI"),
    ("Alma", "$1M / $3M", "Stated in their credentialing checklist.",
     "https://helloalma.com/for-providers/resources/insurance-credentialing-checklist-therapists/"),
    ("Grow Therapy", "$1M / $3M", "The $100K/$300K California carve-out applies "
     "only to nurse practitioners.",
     "https://help.growtherapy.com/en/articles/6616999-malpractice-insurance-requirements"),
    ("Blue Shield of California", "$1M / $3M", "Plus a malpractice questionnaire "
     "explaining every claim, settlement and open case.",
     "https://www.blueshieldca.com/en/provider/guidelines-resources/prospective-providers/credentialing-requirements"),
    ("Cigna / Evernorth", "$1M / $1M", "Prescribers are held to $1M/$3M; "
     "&ldquo;all other health care professionals&rdquo; to $1M/$1M.",
     "https://static.cigna.com/assets/chcp/html/cbhJoinourNetwork.html"),
    ("Optum / United", "$1M / $3M", "For both general and professional "
     "liability, for agency and group providers.",
     "https://public.providerexpress.com/content/ope-provexpr/us/en/our-network/jon.html"),
    ("Kaiser Permanente", "$1M / $3M", "Organizational and community provider "
     "credentialing.",
     "https://healthy.kaiserpermanente.org/content/dam/kporg/final/documents/community-providers/mas/2022/credentialing-form-en-may2022.pdf"),
    ("Medi&#8209;Cal", "$100K / $300K", "The only one that is a regulation "
     "rather than a contract term. Also requires general liability.",
     "https://www.law.cornell.edu/regulations/california/22-CCR-51000.30"),
    ("Anthem Blue Cross", "not published", "The number lives in your individual "
     "Participating Provider Agreement, not in any public document.",
     "https://providers.anthem.com/docs/gpp/california-provider/CA_CAID_ProviderCredentialingProgram.pdf?v=202010122210"),
    ("A commercial office lease", "$1M / $2M", "This is <b>general</b> "
     "liability, and your malpractice policy will not satisfy it. The standard "
     "California AIR CRE office lease requires it on an occurrence basis with "
     "the landlord as an additional insured.",
     "https://www.aircre.com/site/wp-content/uploads/2017/10/OFG.pdf"),
]

# ------------------------------------------------------------ the glossary

GLOSSARY = [
    ("Occurrence", "Covers anything that happened while the policy was in "
     "force &mdash; forever, whoever you are insured with later. You never buy "
     "tail. Most therapist policies are written this way, including CPH, The "
     "Trust, Proliability and CM&amp;F."),
    ("Claims-made", "Only responds if the policy is <b>still active when the "
     "claim is reported</b>. Therapy claims often surface years later, so "
     "leaving, retiring or switching carriers means buying tail from the old "
     "carrier or prior-acts cover from the new one. American Professional "
     "Agency writes claims-made; Berxi offers both."),
    ("The step-up", "A claims-made premium starts low and climbs for six or "
     "seven years until it matures. The Trust publishes the curve for a "
     "California non-psychologist: <b>$103 in year one, $529 at maturity</b>. "
     "Year one is 19% of the real price, which is why a claims-made quote "
     "looks like a bargain next to an occurrence one."),
    ("Tail", "Extended reporting period &mdash; what you buy to keep a "
     "claims-made policy answering after it ends. A working rule of thumb from "
     "a risk manager is <b>200&ndash;250% of your last annual premium</b>; one "
     "therapist reported paying $443 for a single year of it. Several carriers "
     "waive it on death, disability or retirement."),
    ("Prior acts", "The mirror image &mdash; buying back the retroactive date "
     "from your old carrier when you switch. CPH sells it for <b>$175, once</b>."),
    ("$1M / $3M", "The most payable for any one claim, then the most payable "
     "for every claim in the policy year combined. $1M per occurrence is the "
     "near-universal floor; the aggregate is $1M or $3M depending who is asking, "
     "and $3M is what satisfies all of them with one policy."),
    ("Defense outside the limits", "Whether your legal fees come out of the "
     "$1,000,000 or sit on top of it. On the better therapist policies they sit "
     "on top &mdash; CPH says defense &ldquo;will not reduce the limit of "
     "liability.&rdquo; It is worth checking, because on a policy where defense "
     "erodes the limit, a long case can spend your coverage before anyone is "
     "paid."),
    ("Board defense sublimit", "A completely separate, much smaller pot for "
     "defending a complaint to the BBS &mdash; $5,000 to $35,000, against a $1M "
     "malpractice limit. This is the coverage you are statistically far more "
     "likely to use. See below."),
    ("Professional vs general liability", "Professional liability covers the "
     "therapy. General liability covers the client who slips in your waiting "
     "room. Your landlord wants the second one and will not accept the first."),
]

# ---------------------------------------------------------- example cases

CASES = [
    {
        "t": "A complaint arrives at the Board",
        "odds": "2,127 complaints in FY 2023&ndash;24",
        "body": "This is the likely one. The BBS received 2,127 consumer "
                "complaints in FY 2023&ndash;24 and has averaged about 1,910 a "
                "year. Against roughly 148,000 licensees across all categories, "
                "<b>being complained about is not rare; being disciplined is</b> "
                "&mdash; 7 revocations, 9 surrenders and 24 probations that year.",
        "num": "$5,524",
        "numlab": "average license-protection claim, per CNA",
        "cover": "Your board-defense sublimit, not your $1M limit. A risk "
                 "manager who has handled around 800 of these says most resolve "
                 "with an explanatory letter for $3,000&ndash;5,000, and that "
                 "he has &ldquo;not yet seen a case in which someone with their own "
                 "individual liability policy has exhausted their license "
                 "defense limits.&rdquo; The tail risk is the contested hearing: "
                 "investigations average <b>580 days</b> from opening to "
                 "referral, and defense counsel runs $250&ndash;500 an hour.",
    },
    {
        "t": "A subpoena for your records",
        "odds": "the most commonly reported use of a policy",
        "body": "Not a claim against you at all &mdash; someone else&rsquo;s "
                "litigation reaching into your file. Every reported real-world "
                "use of a therapist policy in the public record is one of these, "
                "or a request for a consultation about one.",
        "num": "$10,000",
        "numlab": "CPH deposition representation, per deposition",
        "cover": "Subpoena assistance and deposition sublimits, and the attorney "
                 "helpline. One therapist: &ldquo;my insurance found me a lawyer who "
                 "guided me through the process and I did not end up needing to "
                 "send my records.&rdquo; Another was subpoenaed as a fact witness in "
                 "a criminal trial and had counsel prepare them. <b>This is "
                 "what people actually use the policy for.</b>",
    },
    {
        "t": "A malpractice suit",
        "odds": "7 reports in four years, across all BBS licensees",
        "body": "Rare, and large. Insurers must report any settlement over "
                "$10,000 to the BBS within 30 days under B&amp;P "
                "&sect;&thinsp;801(b). The Board received <b>seven</b> such "
                "reports across four fiscal years.",
        "num": "$360,000",
        "numlab": "average award paid on behalf of a licensee",
        "cover": "Your $1M/$3M limit, with defense on top on the better "
                 "policies. Two things follow from that $360,000 figure: a "
                 "$500,000 limit is not obviously enough, and <b>a civil "
                 "settlement over $10,000 automatically becomes a board matter "
                 "with your name on it</b>.",
    },
    {
        "t": "A client takes a session from another state",
        "odds": "the fastest-growing claim category",
        "body": "16 CCR &sect;&thinsp;1815.5(e) lets you treat someone in "
                "another jurisdiction <i>only if</i> you meet that "
                "jurisdiction&rsquo;s requirements to practise there. There is no "
                "MFT compact &mdash; PSYPACT is doctoral psychologists only, and "
                "California belongs to no health licensing compact at all. "
                "&sect;&thinsp;1815.5(d)(1) makes you <b>verbally obtain and "
                "document the client&rsquo;s present location at the start of every "
                "single session</b>, which is precisely how you find out.",
        "num": "$317,516",
        "numlab": "average telebehavioral-health claim, CNA 2024",
        "cover": "<b>Probably nothing.</b> Coverage is granted where your "
                 "license permits practice &mdash; CPH&rsquo;s grant is telehealth "
                 "&ldquo;provided such practice is authorized or allowable under the "
                 "scope of your license in the state where you practice.&rdquo; A "
                 "client in a hotel room in Nevada is three problems at once: "
                 "unlicensed practice there, a &sect;&thinsp;1815.5(e) violation "
                 "here, and very likely no cover for either.",
    },
    {
        "t": "Your supervisee makes a mistake",
        "odds": "group-practice claims went 15.9% &rarr; 28.9% in five years",
        "body": "B&amp;P &sect;&thinsp;4980.43.1(b) defines supervision as "
                "&ldquo;<b>responsibility for, and control of, the quality of mental "
                "health and related services provided by the supervisee</b>.&rdquo; "
                "That is a broad standard, and the associate must legally be an "
                "employee &mdash; so the practice carries respondeat superior "
                "exposure and the supervisor carries a statutory one.",
        "num": "$0",
        "numlab": "what an individual policy covers your employees for",
        "cover": "CPH covers supervising an associate on your individual policy "
                 "&mdash; but &ldquo;customers with Individual policies cannot add "
                 "employees or interns to their policies. The employees or "
                 "interns must take out their own policies.&rdquo; The moment you "
                 "have a W-2 employee you need an entity policy. Do not assume "
                 "your policy covers supervision by default; it is usually a "
                 "rated exposure you have to declare.",
    },
    {
        "t": "You incorporate, and get sued",
        "odds": "the gap almost nobody checks",
        "body": "A plaintiff suing an incorporated solo therapist names "
                "<b>both</b> you and the professional corporation. CPH is "
                "explicit that an individual policy &ldquo;does not cover your "
                "business entity, even if you are the sole owner,&rdquo; and that you "
                "cannot add a company you own as an additional insured.",
        "num": "$800",
        "numlab": "the minimum franchise tax you paid for that shield",
        "cover": "The corporation defends itself out of the corporation&rsquo;s "
                 "assets &mdash; which defeats a fair part of the point of "
                 "incorporating. American Professional Agency is the exception "
                 "worth knowing about: their schedule states a P.C. with no "
                 "employees other than the owner <b>qualifies for the individual "
                 "rate</b>, so the entity is named at no extra premium.",
    },
]

# --------------------------------------------------------- needs profiles

NEEDS = [
    {
        "key": "student",
        "who": "A trainee still in a master&rsquo;s program",
        "need": "Free, if you are a CAMFT student member. CAMFT gives student "
                "members professional liability cover at $1M/$3M on an "
                "occurrence form at no cost. If you are not a member, CPH "
                "charges <b>$15 a year</b>.",
        "watch": "CAMFT pre-licensed dues are $95, so &ldquo;free insurance&rdquo; costs "
                 "$95 &mdash; still the cheapest route if you want the other "
                 "member benefits.",
    },
    {
        "key": "amft",
        "who": "An AMFT accruing hours",
        "need": "<b>$90 a year</b> at CPH for $1M/$3M. You are legally an "
                "employee &mdash; associates cannot be independent contractors "
                "or take payment from clients &mdash; so your employer&rsquo;s policy "
                "is doing most of the work.",
        "watch": "Associates get <i>no</i> discounts at CPH until they are fully "
                 "licensed. And the employer&rsquo;s policy insures the employer: it "
                 "has no reason to carry board-defense cover for your "
                 "registration, because a corporation has no license for the BBS "
                 "to discipline.",
    },
    {
        "key": "newly",
        "who": "Newly licensed, first year on your own",
        "need": "About <b>$160</b> at CPH &mdash; the full-time $320 with the "
                "50% newly-licensed discount &mdash; then $240 in year two and "
                "$320 from year three. HPSO discounts new graduates harder "
                "(60/40/20% over three years) but has no legal helpline.",
        "watch": "The discount arrives at <b>first licensure</b>, not at "
                 "graduation, and applies at your next renewal.",
    },
    {
        "key": "solo",
        "who": "Full-time solo private practice",
        "need": "<b>$1M / $3M</b>, occurrence, with defense outside the limits. "
                "Published: $320 at CPH before discounts. Californians actually "
                "report $110 to $600 depending on discounts and add-ons.",
        "watch": "$1M per occurrence is the floor every payer wants; $3M "
                 "aggregate is what satisfies all of them at once. Anything at "
                 "$500,000 will fail Headway, Alma, Blue Shield and Optum "
                 "credentialing.",
    },
    {
        "key": "office",
        "who": "You rent a physical office",
        "need": "Professional liability <b>and</b> general liability &mdash; two "
                "different policies covering two different things. The standard "
                "California office lease requires CGL at $1M/$2M on an "
                "occurrence basis with the landlord as an additional insured.",
        "watch": "CPH charges $182 for GL alone, $332 with business property. "
                 "The Trust and Lockton include it. Adding your landlord as an "
                 "additional insured is free at CPH; every other additional "
                 "insured costs 10% of your premium.",
    },
    {
        "key": "incorporated",
        "who": "You have a Marriage and Family Therapy Corporation",
        "need": "Cover for the <b>entity</b>, not just for you. American "
                "Professional Agency names a solo-owner P.C. at the individual "
                "rate. CPH requires a separate corporate policy and does not "
                "publish its price.",
        "watch": "Headway rejects a certificate that names only your LLC. If you "
                 "move to entity-only cover you can fail credentialing &mdash; "
                 "your individual name has to appear as a named insured.",
    },
    {
        "key": "group",
        "who": "You employ associates or clinicians",
        "need": "An entity policy. Every carrier surveyed requires one. CPH&rsquo;s "
                "covers &ldquo;the business, its owners, w-2 employees, and "
                "volunteers&rdquo; &mdash; <b>independent contractors are not "
                "covered</b>, only the business&rsquo;s vicarious exposure from their "
                "work.",
        "watch": "Group-practice claims rose from 15.9% to 28.9% of the CNA "
                 "counselor dataset in five years &mdash; the fastest-growing "
                 "setting in the study.",
    },
    {
        "key": "telehealth",
        "who": "Telehealth, and clients who travel",
        "need": "Nothing you can buy fixes this. Every carrier includes "
                "telehealth in the professional liability limit at no extra "
                "charge, and every one of them conditions it on lawful practice "
                "in the state where the client is sitting.",
        "watch": "Document the client&rsquo;s location at the start of every session "
                 "&mdash; 16 CCR &sect;&thinsp;1815.5(d)(1) requires it, and it is "
                 "the record the Board will read.",
    },
]

# ------------------------------------------------------------- affiliates

AFFILIATE = {
    "headline": "None of these companies pays us anything.",
    "body": "We checked every carrier and agency on this page for an affiliate, "
            "referral or partner program &mdash; CPH, HPSO, The Trust, Berxi, "
            "Proliability, CM&amp;F, American Professional Agency and Lockton "
            "Affinity. <b>Not one of them runs a public affiliate program.</b> "
            "They all work through association endorsements negotiated one-off "
            "with professional bodies, not through publisher commissions. There "
            "is no affiliate network path to any carrier a California MFT would "
            "actually buy from: searches of Impact, CJ, ShareASale, PartnerStack, "
            "Awin, FlexOffers and Refersion return no healthcare-professional "
            "malpractice carrier at all.",
    "why": "Which means there is nothing to disclose here, and no reason to "
           "doubt the ordering above. The programs that <i>do</i> pay publishers "
           "&mdash; Hiscox at $25 a quote, Thimble, Simply Business, Insureon "
           "&mdash; are general small-business insurers, and we could not verify "
           "that any of them writes licensed mental-health professional "
           "liability at all. Recommending them to a therapist for malpractice "
           "cover would be wrong on the merits whatever it paid.",
}
