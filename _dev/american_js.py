#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""The British spellings that `american.py` could not see: the ones inside JavaScript.

WHAT WAS MISSED AND WHY

`american.py` converted 2,776 `programme`s and 489 `licence`s across the HTML.
It works on markup - it protects `<blockquote>`, `<q>` and URLs, and it walks
JSON-LD string values - and that is exactly why it missed these: the remaining
British text is not in the markup at all. It is in string literals inside
`<script>` blocks, assembled into the DOM at runtime.

The two that matter are on the two busiest pages on the site:

    mft-programs-california.html   "78 of 78 programmes"   the directory's own count
                                   "Programme places you"  a filter chip label
    amft-3000-hours-california     "off your licence date" the headline sentence
    associate-mft-job-advisor      (the same five, shared)

A reader filtering the school directory sees the word in the result count. No
amount of re-running the HTML pass would have caught it.

WHAT THIS DOES NOT TOUCH

Code comments. `// the ONE drawer behaviour`, `/* Directory behaviour */`,
`// which quietly favoured them` - a dozen of these exist and every one of them
is invisible to a reader. Converting them would be churn dressed as
thoroughness, and it would make the next diff of these files noisier for no
reader benefit. The scope here is text a reader can see.

Distinguishing the two requires actually tokenising, not pattern-matching: a
regex for `'...'` finds a "string" in `// don't do this`, and an apostrophe in a
comment would swallow everything to the next quote. So this walks each script
character by character, tracking line comments, block comments, and the three
string forms (single, double, template), and rewrites only inside a literal.

Idempotent - the replacements are American, so a second pass finds nothing.
"""
import os, re, sys

HERE = os.path.dirname(os.path.abspath(__file__))
SITE = os.path.dirname(HERE)
SUBDIRS = ("money", "licensure", "getting-paid", "practice", "training")

# Suffix-grouped, for the reason written up in _dev/american.py: a bare
# `criticis -> criticiz` produced "criticizm", and `centre -> center` produced
# "centerd". Each rule here names the endings it accepts.
RULES = [
    (r"\blicence(s?)\b", lambda m: "license" + m.group(1)),
    (r"\bLicence(s?)\b", lambda m: "License" + m.group(1)),
    (r"\bprogramme(s?)\b", lambda m: "program" + m.group(1)),
    (r"\bProgramme(s?)\b", lambda m: "Program" + m.group(1)),
    (r"\bcancelled\b", lambda m: "canceled"),
    (r"\bCancelled\b", lambda m: "Canceled"),
    (r"\bcancelling\b", lambda m: "canceling"),
    (r"\bfavour(s|ed|ing|able)?\b", lambda m: "favor" + (m.group(1) or "")),
    (r"\bbehaviour(s|al)?\b", lambda m: "behavior" + (m.group(1) or "")),
    (r"\bdefence(s?)\b", lambda m: "defense" + m.group(1)),
    (r"\bcentre(s|d)?\b", lambda m: "center" + (m.group(1) or "")),
    (r"\bcolour(s|ed|ing)?\b", lambda m: "color" + (m.group(1) or "")),
    (r"\benrolment(s?)\b", lambda m: "enrollment" + m.group(1)),
    (r"\bwhilst\b", lambda m: "while"),
]

# Nothing here may ever be produced. The last conversion shipped "criticizm"
# and "centerd" to 26 pages before it was caught.
NEVER = ["licensece", "licensess", "programe", "programss", "favoror",
         "behaviorr", "defensee", "centerd", "colord", "canceleded",
         "centerss", "colorr"]


def convert(text):
    out = text
    for pat, rep in RULES:
        out = re.sub(pat, rep, out)
    return out


def rewrite_script(js):
    """Convert inside string literals only. Comments and identifiers untouched."""
    out = []
    i, n = 0, len(js)
    changed = 0
    while i < n:
        c = js[i]
        if c == "/" and i + 1 < n and js[i + 1] == "/":
            j = js.find("\n", i)
            j = n if j < 0 else j
            out.append(js[i:j]); i = j; continue
        if c == "/" and i + 1 < n and js[i + 1] == "*":
            j = js.find("*/", i + 2)
            j = n if j < 0 else j + 2
            out.append(js[i:j]); i = j; continue
        if c in "'\"`":
            q = c
            j = i + 1
            while j < n:
                if js[j] == "\\":
                    j += 2; continue
                if js[j] == q:
                    break
                if q != "`" and js[j] == "\n":
                    break          # unterminated: bail rather than guess
                j += 1
            lit = js[i:j + 1]
            new = convert(lit)
            if new != lit:
                changed += 1
            out.append(new)
            i = j + 1
            continue
        out.append(c)
        i += 1
    return "".join(out), changed


SCRIPT = re.compile(r"(<script\b[^>]*>)([\s\S]*?)(</script>)", re.I)


def pages():
    out = [f for f in sorted(os.listdir(SITE)) if f.endswith(".html")]
    for d in SUBDIRS:
        p = os.path.join(SITE, d)
        if os.path.isdir(p):
            out += ["%s/%s" % (d, f) for f in sorted(os.listdir(p))
                    if f.endswith(".html")]
    return out


def main():
    total, files = 0, 0
    touched = []
    for rel in pages():
        p = os.path.join(SITE, rel)
        s = open(p, encoding="utf-8").read()
        changed_here = 0

        def one(m):
            nonlocal changed_here
            body, c = rewrite_script(m.group(2))
            changed_here += c
            return m.group(1) + body + m.group(3)

        out = SCRIPT.sub(one, s)
        if changed_here and out != s:
            open(p, "w", encoding="utf-8").write(out)
            files += 1
            total += changed_here
            touched.append((rel, changed_here))
    for rel, c in touched:
        print("  %-46s %d literal(s)" % (rel, c))
    print("\n%d string literal(s) converted across %d file(s)" % (total, files))

    # ------------------------------------------------------------- guards
    bad = 0
    left = []
    for rel in pages():
        s = open(os.path.join(SITE, rel), encoding="utf-8").read()
        for w in NEVER:
            if w in s:
                print("GUARD %s: produced %r" % (rel, w))
                bad += 1
        for m in SCRIPT.finditer(s):
            js = m.group(2)
            # re-tokenise and look only inside literals
            probe, _c = rewrite_script(js)
            if probe != js:
                left.append(rel)
                break
    if left:
        print("GUARD: still convertible: %s" % ", ".join(sorted(set(left))))
        bad += 1
    if bad:
        sys.exit("\n%d problem(s)" % bad)
    print("guards clean - no British spelling left in any script string literal")


if __name__ == "__main__":
    main()
