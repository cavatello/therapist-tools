#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Two defects in the Touro show-cause notice, found on the live page.

1. **Double-escaped entities.** The notice body was written with HTML entities
   (`&rsquo;`, `&ldquo;`, `&mdash;`) and `<b>` tags. `build_schools.py` escapes
   the body, so a reader saw literal `&amp;rsquo;` and `<b>`. The Sentio notice
   that set the precedent uses raw Unicode characters and no markup, which is
   why it renders correctly - the body is TEXT, not HTML. Rewritten to match.

2. **The In-short card still said "COAMFTE accredited" flat.** The verdict block
   was qualified but the summary above it - the first thing a reader sees, and
   the one that becomes `ts:outcome` and the hub card - was not. The unqualified
   claim survived in the one place it does the most work.

Both are the same underlying mistake: qualifying the claim in one place and
assuming the page only says it once. It said it in three.
"""
import json, os, sys

HERE = os.path.dirname(os.path.abspath(__file__))
SITE = os.path.dirname(HERE)
DATA = os.path.join(SITE, "mock", "mftguide", "programs.json")
BUILDER = os.path.join(SITE, "mock", "mftguide", "build_schools.py")

# Raw characters, no entities, no tags - the builder escapes this.
BODY = (
    "Touro’s own student-and-consumer-information page states that the "
    "Marriage and Family Therapy track “is the only track accredited with show "
    "cause” by COAMFTE. Show cause is the most serious status short of "
    "withdrawal: the program keeps its accreditation while it is required to "
    "demonstrate why it should not lose it. "
    "Two things this does not mean. The institution is not in trouble — WSCUC "
    "lists Touro University Worldwide as accredited with no sanction, most "
    "recent Commission action 27 June 2025. And it does not stop you licensing "
    "in California: the Board lists this institution, and California licensure "
    "does not require COAMFTE accreditation at all. "
    "What it does affect is portability to states and employers that require a "
    "COAMFTE degree, and the risk that the program’s status changes while you "
    "are enrolled. If you are considering this program, or are in it, ask the "
    "program directly what the show-cause findings were and when the "
    "Commission next reviews them.")

TITLE = "This program’s COAMFTE accreditation is on show cause"
COAM_NOTE = "on show cause — read the notice at the top of this page"


def main():
    progs = json.load(open(DATA, encoding="utf-8"))
    hit = [p for p in progs if p.get("institution") == "Touro University Worldwide"]
    if len(hit) != 1:
        sys.exit("fix_touro_notice: %d Touro records" % len(hit))
    p = hit[0]
    if not p.get("notice"):
        sys.exit("fix_touro_notice: no notice to fix - run patch_touro.py first")
    p["notice"]["title"] = TITLE
    p["notice"]["body"] = BODY
    p["coamfte_note"] = COAM_NOTE
    for bad in ("&rsquo;", "&ldquo;", "&mdash;", "<b>"):
        if bad in p["notice"]["body"] or bad in p["coamfte_note"]:
            sys.exit("fix_touro_notice: %r is still in the body. The builder "
                     "escapes this field, so markup and entities render "
                     "literally." % bad)
    json.dump(progs, open(DATA, "w", encoding="utf-8"), indent=1,
              ensure_ascii=False)
    print("  ok  notice body rewritten as plain text")

    # ---- the summary line, which is where the unqualified claim survived
    s = open(BUILDER, encoding="utf-8").read()
    OLD = '        bits.append("COAMFTE accredited")\n'
    NEW = ('        # Qualified where a qualifier exists. This line feeds the\n'
           '        # In-short card, ts:outcome and the hub card - the three\n'
           '        # places a reader meets the claim before the verdict block\n'
           '        # that was already fixed.\n'
           '        bits.append("COAMFTE accredited"\n'
           '                    + (" (%s)" % p["coamfte_note"]\n'
           '                       if p.get("coamfte_note") else ""))\n')
    if s.count(OLD) != 1:
        sys.exit("fix_touro_notice: the summary line matched %d times"
                 % s.count(OLD))
    if "Qualified where a qualifier exists" not in s:
        s = s.replace(OLD, NEW, 1)
        open(BUILDER, "w", encoding="utf-8").write(s)
    print("  ok  the In-short summary is qualified too")


if __name__ == "__main__":
    main()
