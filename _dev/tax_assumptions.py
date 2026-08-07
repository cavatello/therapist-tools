#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Disclose the one modelling choice the tax page was still making silently.

The page already discloses its bracket year, and discloses it well: California
had not published 2026 rate schedules, the FTB's own 2026 Form 540-ES tells
filers to use the 2025 tables, and the copy says so. That one needed no fix.

What was NOT disclosed is the Unemployment Insurance rate. The engine charges
`CA_UI = .034` on the corporation's side. That is a real, correct number - it
is the rate the EDD assigns to a NEW employer - but it is only true for the
first two to three years. After that the employer is experience-rated
somewhere between 1.5% and 6.2%, and at the top of that range the UI charge on
a $7,000 wage base is $434 instead of $238.

Small in dollars. Not small in kind: this project's standing rule is that
every figure is computed or cited, never illustrative, and a rate chosen from
inside a range without saying so is exactly the sort of thing that makes the
rest of the arithmetic less trustworthy when a reader finds it. Better to name
it and let the reader adjust.

Verified 6 August 2026 against the EDD's own Tax-Rated Employers page:
"New employers are assigned a 3.4 percent UI rate for two to three years";
the 2026 schedule "provides for UI contribution rates from 1.5 percent to
6.2 percent"; the taxable wage limit is $7,000; ETT for 2026 is 0.1 percent.
All three of the engine's constants match.

Two insertions, because the reader may meet the number in either place:
  1. the .disc assumptions paragraph, which is where a careful reader looks
  2. the payroll row's own explanation, which is where everyone else will see it

Idempotent. Run after the other style passes; it touches copy only.
"""
import os, re, sys

HERE = os.path.dirname(os.path.abspath(__file__))
SITE = os.path.dirname(HERE)
PAGE = "therapist-tax-strategy-california.html"

EDD = "https://edd.ca.gov/en/payroll_taxes/tax-rated-employers/"

# 1. assumptions paragraph -------------------------------------------------
DISC_OLD = ("The professional-corporation comparison prices payroll, the 1120-S "
            "and the Statement of Information at typical figures, not quotes you "
            "have been given.")
DISC_NEW = ("The corporation&rsquo;s California payroll line charges Unemployment "
            "Insurance at <b>3.4%</b>, the rate the EDD assigns to a new employer "
            "for its first two to three years; after that an employer is "
            "experience-rated somewhere between 1.5% and 6.2%, so an established "
            "practice&rsquo;s figure will sit above this one.<a href=\"" + EDD +
            "\" target=\"_blank\" rel=\"noopener noreferrer\"> EDD rates</a>. "
            "The professional-corporation comparison prices payroll, the 1120-S "
            "and the Statement of Information at typical figures, not quotes you "
            "have been given.")

# 2. the row the reader actually reads ------------------------------------
ROW_OLD = '+ ", no cap since 2024) plus UI, ETT and FUTA on the first $7,000 ("'
ROW_NEW = ('+ ", no cap since 2024) plus UI at the 3.4% new-employer rate, '
           'ETT and FUTA on the first $7,000 ("')

MARK = "the rate the EDD assigns to a new employer"


def main():
    path = os.path.join(SITE, PAGE)
    if not os.path.exists(path):
        sys.exit("tax_assumptions: %s not found" % PAGE)
    s = open(path, encoding="utf-8").read()

    if MARK in s:
        print("%-44s already disclosed" % PAGE)
    else:
        for old, new, what in ((DISC_OLD, DISC_NEW, "assumptions paragraph"),
                               (ROW_OLD, ROW_NEW, "payroll row")):
            n = s.count(old)
            if n != 1:
                sys.exit("tax_assumptions: %s matched %d times, expected 1" % (what, n))
            s = s.replace(old, new, 1)
        open(path, "w", encoding="utf-8").write(s)
        print("%-44s UI-rate assumption disclosed in 2 places" % PAGE)

    # ---- guards
    s = open(path, encoding="utf-8").read()
    bad = 0
    if s.count(MARK) != 1:
        print("GUARD: %d disclosure sentences" % s.count(MARK)); bad += 1
    if s.count("3.4% new-employer rate") != 1:
        print("GUARD: %d row mentions" % s.count("3.4% new-employer rate")); bad += 1
    # the constant the copy now describes must still be what the engine charges
    m = re.search(r"CA_UI\s*=\s*(\.?\d*\.?\d+)", s)
    if not m or float(m.group(1)) != .034:
        print("GUARD: CA_UI is %s, copy claims 3.4%%" % (m.group(1) if m else "absent")); bad += 1
    # and the two other constants the same sentence relies on
    if not re.search(r"UI_BASE\s*=\s*7000", s):
        print("GUARD: UI_BASE is not 7000"); bad += 1
    if s.count("<h1") != 1:
        print("GUARD: %d h1" % s.count("<h1")); bad += 1
    if bad:
        sys.exit("tax_assumptions: %d guard failure(s)" % bad)
    print("guards clean")


if __name__ == "__main__":
    main()
