# -*- coding: utf-8 -*-
"""Copy and constants for therapist-cost-of-living-california.html.

Every number below was fetched and checked, and every one is cited on the page.

  MIT Living Wage Calculator, 1 adult / 0 children, current 15 Feb 2026
  HHS poverty guidelines 2026, via the US Courts 150% table
  Repayment Assistance Plan, live 1 July 2026 (One Big Beautiful Bill)

Design rule this page keeps, same as the rest of the site: the area picker
PRE-FILLS, it does not decide. Every category is an editable field, because a
single number for "cost of living in California" is exactly the illustrative
figure this site refuses to print.
"""

SITE = "https://therapistsupport.org"
SLUG = "therapist-cost-of-living-california.html"
TITLE = ("Cost of Living for California Therapists — what you need to earn, "
         "and what is left")
DESC = ("Work out your real monthly break-even in California: housing, transport, "
        "food and medical by area, your student loan payment on RAP or the standard "
        "plan, and what is left for savings. Built for LMFTs, LCSWs, LPCCs and "
        "registered associates. Free, nothing saved.")

# --- MIT Living Wage, 1 adult / 0 children, ANNUAL -------------------------
# Only the two verified directly are shipped as presets. Adding six more from
# memory would be exactly the kind of plausible-looking figure this site does
# not print; the fields are editable, and the page says which two are measured.
AREAS = [
    ("ca", "California, statewide", dict(housing=23383, transport=9528, food=4580,
                                         civic=3876, medical=3432, phone=1625,
                                         other=4992), 63402),
    ("la", "Los Angeles County", dict(housing=22471, transport=8681, food=4463,
                                      civic=3876, medical=3255, phone=1517,
                                      other=4992), 60161),
]

CATS = [
    ("housing", "Housing"),
    ("transport", "Transport"),
    ("food", "Food"),
    ("medical", "Medical"),
    ("civic", "Civic &amp; taxes on spending"),
    ("phone", "Internet &amp; mobile"),
    ("other", "Everything else"),
]

# --- student loans --------------------------------------------------------
# RAP bands: percentage of AGI. Live 1 July 2026.
RAP_BANDS = [(10000, 0.00), (20000, 0.01), (30000, 0.02), (40000, 0.03),
             (50000, 0.04), (60000, 0.05), (70000, 0.06), (80000, 0.07),
             (90000, 0.08), (100000, 0.09), (10 ** 9, 0.10)]
RAP_MIN = 10          # dollars a month, whatever the AGI
RAP_DEPENDENT = 50    # dollars a month off, per dependent
RAP_MONTHS = 360      # forgiveness
PSLF_MONTHS = 120     # unchanged by the new law

FPL_1 = 15960         # 2026, 48 contiguous states
FPL_EXTRA = 5680      # per additional person
IBR_RATE = 0.10       # of discretionary income, above 150% FPL
IBR_MONTHS = 240      # 20 years, new borrowers

# --- the principles, straight ---------------------------------------------
# Presented as the framework it is, in its own terms. The site's own arithmetic
# is elsewhere on the page and speaks for itself.
RAMSEY_H = "A framework people actually use"
RAMSEY_LEDE = (
    "Most people who get on top of this did not invent a system. They followed one. "
    "The best-known is Dave Ramsey&rsquo;s <em>Baby Steps</em> &mdash; deliberately "
    "simple, ordered, and built around finishing one thing before starting the next.")
RAMSEY_STEPS = [
    ("1", "$1,000 starter emergency fund",
     "Before anything else. It is not enough to live on; it is enough to stop a flat "
     "tyre turning into a credit card balance."),
    ("2", "Pay off all debt except the house, smallest balance first",
     "The debt snowball. Smallest first rather than highest-rate first, on the "
     "argument that finishing a debt is what keeps people going."),
    ("3", "Three to six months of expenses saved",
     "A full emergency fund. For a practice whose income depends on clients showing "
     "up, the upper end of that range is the one worth aiming at."),
    ("4", "15% of income into retirement",
     "Consistently, from here on."),
    ("5", "Save for children&rsquo;s education", "If that applies to you."),
    ("6", "Pay off the house early", "Everything spare goes at the mortgage."),
    ("7", "Build wealth and give",
     "The point of the previous six."),
]
RAMSEY_NOTE = (
    "Two places where the arithmetic on this page will disagree with a strict reading "
    "of step 2, and both are specific to this profession. <b>If you are working toward "
    "Public Service Loan Forgiveness</b>, the balance is written off after 120 "
    "qualifying payments &mdash; so paying extra shortens nothing and forgives nothing "
    "extra. The calculator above shows both paths so you can see the gap. And <b>this "
    "site never assumes a rate of return</b>; every projection here asks you for one, "
    "because the number you choose is the whole answer.")

# --- savings --------------------------------------------------------------
SAVE_H = "What is left, and where it goes"
