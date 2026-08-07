# -*- coding: utf-8 -*-
"""Headway, for California therapists. Every claim retrieved 6 August 2026.

Written with an affiliate link on the page, which is exactly why the standard
is higher rather than lower. The rule applied throughout: where Headway
publishes a number, it is quoted and linked; where Headway does NOT publish a
number, the page says "not published" rather than reaching for an estimate that
would happen to be flattering.
"""

AFF = "https://share.findheadway.com/shawn-924"

HC = "https://help.headway.co/hc/en-us/articles/"

# ------------------------------------------------------------------ the gate
GATE_LICENCES = ["LMFT", "LCSW", "LPCC", "Psychologist", "MD / DO",
                 "NP", "CNS"]
GATE_EXCLUDED = ["AMFT", "ASW", "APCC", "Registered psych associate"]

# ------------------------------------------------------------------ payers
PAYERS = [
    ("Aetna", 98), ("Carelon", 79), ("Cigna", 76),
    ("Anthem Blue Cross of California", 75), ("Blue Shield of California", 65),
]
CA_PROVIDERS = 8544

# ------------------------------------------------------------------ money
MONEY = [
    ("Membership or subscription fee", "$0",
     "There is no monthly charge. This part of the pitch is true and it is the "
     "real difference from Alma.", HC + "8465814515348-Rates-and-agreements"),
    ("What Headway keeps", "not published",
     "Headway holds the payer contract, is paid by the insurer, and pays you a "
     "set rate per session &mdash; keeping the difference. Its own words are "
     "&ldquo;a small percentage of session payments&rdquo;. The percentage is "
     "not published.", "https://headway.co/resources/how-does-headway-make-money"),
    ("Your California rate", "not published",
     "Rates are visible only after you are credentialed, inside the portal. "
     "There is no public California rate card, and Headway&rsquo;s own page "
     "titled &ldquo;how much do therapists make in California&rdquo; contains "
     "federal wage-survey data rather than any Headway payout figure.",
     "https://headway.co/resources/how-much-do-therapists-make-in-california"),
    ("When you are paid", "twice a month",
     "The 15th and the last day of the month. That is 24 payments a year, not "
     "26 &mdash; the marketing word is &ldquo;biweekly&rdquo;, which would be "
     "26.", HC + "4416374825748-Getting-paid"),
    ("Late-cancellation fee", "you set it, capped at $200",
     "Paid to you in full.", HC + "4428462506388-Cancellations-and-rescheduling"),
]

# the one hard number in public, and where it came from
OPTUM = {
    "code": "90834",
    "was": 144.27,
    "now": 103.00,
    "when": "1 January 2025",
    "url": ("https://clearhealthcosts.com/blog/2024/11/2-digital-mental-health-"
            "platforms-cut-pay-rates-for-therapists-with-unitedhealths-optum-"
            "stirring-anger/"),
    "note": ("Headway said fewer than 340 of its 40,000-plus providers were "
             "affected. The number matters less than the mechanism: the rate is "
             "set by a contract you are not a party to, and it can move."),
}

# ------------------------------------------------------------------ claims
CLAIMS = [
    ("&ldquo;Get credentialed in 30 days&rdquo;",
     "Headway&rsquo;s own help centre says <b>three weeks to four months</b>.",
     HC + "360022161631-Credentialing-timeline", "amber"),
    ("&ldquo;Earn $27,000 more per year&rdquo;",
     "No methodology, footnote or source appears anywhere on the page carrying "
     "the claim.", "https://provider.headway.co/", "amber"),
    ("&ldquo;We protect you from clawbacks&rdquo;",
     "The help centre article says Headway will <b>aim to</b> protect you, and "
     "reserves the right to adjust payment after an audit.",
     HC + "14930522558868-Chart-reviews-and-audits-on-Headway", "amber"),
    ("&ldquo;No membership fees, no hidden fees&rdquo;",
     "True as stated. There is no subscription. What is not disclosed is the "
     "share of the reimbursement Headway retains.",
     HC + "8465814515348-Rates-and-agreements", "green"),
]

# ------------------------------------------------------------------ give up
TRADEOFFS = [
    ("Your existing credentialing does not transfer",
     "If you are already contracted directly with Aetna, that contract "
     "&ldquo;cannot be applied to or honored&rdquo; on Headway. You end up on "
     "two contracts with the same insurer at two different rates.",
     HC + "8465814515348-Rates-and-agreements"),
    ("Clients who found you through Headway stay on Headway",
     "Headway&rsquo;s own account-management article states that clients who "
     "came to you through its directory will continue to be seen on the "
     "platform. Clients you brought yourself are yours.",
     HC + "4428388155028-Managing-your-account"),
    ("Download your notes before you leave",
     "Records live in Headway&rsquo;s EHR. Offboarding is not instant and "
     "several providers describe friction getting documentation out.",
     "https://www.reddit.com/r/therapists/comments/1tmr4bz/my_headway_nightmare/"),
    ("Identity verification is a biometric facial scan",
     "Rolled out through spring 2026, with no opt-out reported.",
     "https://www.404media.co/headway-therapy-facial-scan-biometric-data-"
     "identity-verification/"),
    ("Support is chat-first",
     "A recurring complaint rather than a published policy &mdash; there is no "
     "phone line for providers.",
     "https://www.reddit.com/r/therapists/comments/1gqfa1m/be_wary_of_headway/"),
]

# ------------------------------------------------------------------ survey
PSIAN = {
    "n": 667,
    "same_or_less": 50,
    "not_told": 84,
    "url": "https://www.psian.org/practice-management-companies",
    "cover": ("https://clearhealthcosts.com/blog/2025/11/therapists-have-"
              "misgivings-on-the-platforms-alma-headway-etc-and-the-business-"
              "of-therapy/"),
}

# ------------------------------------------------------------------ compare
# name, fee model, pay timing, credentialing, associates?, url
COMPARE = [
    ("Headway", "No fee. Undisclosed share of the reimbursement.",
     "Twice monthly", "3 weeks &ndash; 4 months", False,
     "https://headway.co/for-providers"),
    ("Alma", "<b>$95/mo</b> billed annually ($1,140/yr), or $125/mo monthly.",
     "Not published", "Not published", False,
     "https://helloalma.com/for-providers/"),
    ("Grow Therapy", "Not published.", "Weekly", "5&ndash;7 days", False,
     "https://growtherapy.com/providers"),
    ("Rula", "Not published. <i>Rula is Path, rebranded in 2024 &mdash; not a "
     "separate option.</i>", "Every two weeks", "Not published", False,
     "https://www.rula.com/for-providers/"),
    ("SonderMind", "No fee. 2% to be paid same-day.", "Not published",
     "Not published", False, "https://www.sondermind.com/for-providers/"),
    ("Direct with the payer", "None. You keep the whole contracted rate.",
     "Payer&rsquo;s own cycle", "Blue Shield of CA quotes 45&ndash;60 days; "
     "60&ndash;120 is realistic per payer", "Varies by payer",
     "https://www.blueshieldca.com/en/provider/authorizations/credentialing"),
]

FITS = [
    "You are <b>fully licensed</b> in California &mdash; LMFT, LCSW, LPCC or "
    "psychologist. This is not negotiable.",
    "You want insurance clients and do not want to run credentialing or claims.",
    "You have empty hours now and would rather fill them at a rate you do not "
    "set than leave them empty.",
    "You are testing whether insurance work suits you before committing to "
    "direct contracts, which take months to unwind.",
]
DOESNT = [
    "You are an <b>associate</b>. You are not eligible, full stop.",
    "You already hold direct contracts with the same payers &mdash; you cannot "
    "bring them, and you may end up at a worse rate for the same insurer.",
    "Your practice is full at private-pay rates. The arithmetic does not work; "
    "run it on the simulator rather than taking my word for it.",
    "You need to know your rate before committing. You cannot; it is visible "
    "only after credentialing.",
]

SOURCES = [
    ("Headway &mdash; how Headway makes money",
     "https://headway.co/resources/how-does-headway-make-money",
     "&ldquo;A small percentage of session payments.&rdquo; The percentage is not given."),
    ("Headway help centre &mdash; rates and agreements",
     HC + "8465814515348-Rates-and-agreements",
     "Rates are per payer and CPT code, visible after credentialing. Existing "
     "direct contracts cannot be transferred."),
    ("Headway help centre &mdash; accepted licences by state",
     HC + "30499083574292-Headway-s-accepted-licenses-by-state",
     "The California list. No AMFT, ASW or APCC appears on it."),
    ("Headway help centre &mdash; supervisory billing",
     HC + "45958397590164-Supervisory-billing",
     "The pre-licensed pilot: New York and Texas, group practices only. Not California."),
    ("Headway help centre &mdash; getting paid",
     HC + "4416374825748-Getting-paid",
     "The 15th and the last day of the month."),
    ("Headway help centre &mdash; chart reviews and audits",
     HC + "14930522558868-Chart-reviews-and-audits-on-Headway",
     "The clawback language, and the reserved right to adjust payment."),
    ("Headway &mdash; California providers",
     "https://headway.co/therapists/california",
     "Payer mix and the count of California providers on the platform."),
    ("ClearHealthCosts &mdash; Optum rate cuts, November 2024", OPTUM["url"],
     "The one publicly documented Headway rate change, with figures."),
    ("Psychotherapy Action Network &mdash; practice management companies survey",
     PSIAN["url"],
     "n=667 clinicians across these platforms. Self-selected, so read it as "
     "signal rather than as a population estimate."),
    ("404 Media &mdash; biometric identity verification",
     "https://www.404media.co/headway-therapy-facial-scan-biometric-data-"
     "identity-verification/",
     "The facial-scan rollout, spring 2026."),
]

NOT_VERIFIED = [
    "Any California rate for any payer. Headway does not publish them and no "
    "credible third-party table exists. Anyone quoting you a Headway California "
    "rate is quoting one person&rsquo;s portal.",
    "The percentage Headway keeps. Not published. The only public evidence it "
    "is greater than zero is Headway&rsquo;s own statement, during the Optum "
    "cuts, that in those specific cases it would make $0.",
    "Trustpilot&rsquo;s score. The site blocks automated retrieval, and its "
    "reviewers for Headway are overwhelmingly clients rather than providers, "
    "which makes it the wrong instrument for this question anyway.",
]
