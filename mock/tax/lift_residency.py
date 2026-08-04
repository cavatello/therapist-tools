#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Lift the residency engine out of app.js into a self-contained module.

app.js and _engine_core.js name the same quantities differently (SS_WAGE_BASE
vs SS_BASE, FED_BRACKETS_BY_STATUS vs FED, ...) and in a few places carry
slightly different bracket tables. Declaring both sets in one scope is either a
`const` redeclaration error or, worse, a silent disagreement about which table
won. So the lift goes inside its own IIFE: the residency functions keep the
exact constants app.js gives them, and expose nothing but themselves.

Nothing here is retyped. Every block is sliced out of app.js by name and copied
byte for byte, and /tmp/resid-parity.mjs then asserts the two engines return the
same dollars for the same inputs.
"""
import os, re, sys

HERE = os.path.dirname(os.path.abspath(__file__))
APP = open(os.path.join(HERE, "..", "..", "site", "app.js"), encoding="utf-8").read()

# The public surface. Everything else is pulled in because one of these needs it.
EXPORTS = ["computeNYC", "computePittsburgh", "computeFrance", "computeUAE",
           "computeBrisbane", "computeResidency"]

# Discovered by running the module and reading the ReferenceError, one at a
# time, until it ran. Order matters only for readability - these are all
# hoisted or declared before first call inside the IIFE.
NEEDED = [
    # constants
    "FED_STD", "FED_BRACKETS", "CA_BRACKETS",
    "FED_STD_BY_STATUS", "CA_STD_BY_STATUS", "FED_BRACKETS_BY_STATUS",
    "CA_BRACKETS_BY_STATUS", "QBI_PHASE_BY_STATUS", "ADDL_MED_THRESH_BY_STATUS",
    "QBI_RATE", "ADDL_MED_THRESH", "CA_MHS_THRESH", "OASDI_RATE",
    "MEDICARE_RATE", "SE_FACTOR",
    "SS_WAGE_BASE", "NY_STD", "NY_BRACKETS", "NYC_BRACKETS",
    "EUR_TO_USD", "USD_TO_EUR", "MCTMT_THRESHOLD", "UBT_RATE", "UBT_PIT_LOW",
    "PA_FLAT_RATE", "PITTSBURGH_EIT_RATE", "PITTSBURGH_LST",
    "FR_BRACKETS", "FR_COTISATION_RATE", "FR_CSG_RATE",
    "USD_TO_AED", "FEIE_2026", "AU_BRACKETS", "USD_TO_AUD", "PT_BRACKETS",
    # functions
    "bracketTax", "fedLayer", "addlMedFor", "computeUBT", "usFedAbroad",
    "germanIncomeTax", "portugalSolidarity",
] + EXPORTS


def slice_decl(name):
    """Pull one top-level declaration out of app.js, comments above it included.

    Retyping a block is how you get a version that looks the same and is not, so
    this only ever copies a substring; it never reconstructs one.
    """
    m = re.search(r"^(?:function %s\s*\(|const %s\s*[,=])" % (name, name),
                  APP, re.M)
    if not m:
        sys.exit("not found in app.js: " + name)
    start = m.start()

    # walk back over the comment block immediately above, if there is one
    lines = APP[:start].split("\n")
    take = 0
    for ln in reversed(lines[:-1]):
        if ln.startswith("//"):
            take += 1
        else:
            break
    if take:
        start -= sum(len(x) + 1 for x in lines[-take - 1:-1])

    is_fn = APP[m.start():].startswith("function")
    # A function ends at the brace that closes its BODY. Counting every bracket
    # from the declaration keyword ends the slice at the close of the parameter
    # list instead, which produces a file that parses as far as the first
    # function and then falls apart - so for a function, start counting at the
    # first `{`, and count only braces.
    i = APP.index("{", m.start()) if is_fn else m.start()
    depth, in_s, in_c, in_lc, started = 0, None, False, False, False
    while i < len(APP):
        ch, nxt = APP[i], APP[i + 1:i + 2]
        if in_lc:
            if ch == "\n":
                in_lc = False
        elif in_c:
            if ch == "*" and nxt == "/":
                in_c = False; i += 1
        elif in_s:
            if ch == "\\":
                i += 1
            elif ch == in_s:
                in_s = None
        elif ch in "\"'`":
            in_s = ch
        elif ch == "/" and nxt == "*":
            in_c = True; i += 1
        elif ch == "/" and nxt == "/":
            in_lc = True; i += 1
        elif ch in ("{" if is_fn else "{[("):
            depth += 1; started = True
        elif ch in ("}" if is_fn else "}])"):
            depth -= 1
            if is_fn and started and depth == 0:
                return APP[start:i + 1] + "\n"
        elif ch == ";" and depth == 0 and not is_fn:
            return APP[start:i + 1] + "\n"
        i += 1
    sys.exit("ran off the end of app.js looking for the end of " + name)


HEAD = """/* ==========================================================================
   RESIDENCY ENGINE.  Lifted out of app.js by lift_residency.py - every block
   below is a byte-for-byte substring of that file, comments included. Do not
   edit it here; edit app.js (or, once app.js is gone, promote this file to the
   source of truth and say so at the top).

   It lives inside an IIFE because app.js and _engine_core.js use DIFFERENT
   NAMES for the same quantities, and in two places slightly different bracket
   tables. Sharing a scope would be a redeclaration error at best and a silent
   disagreement about which table applied at worst. In here, the residency
   functions see exactly the constants app.js gives them and nothing else.
   ========================================================================== */
var RESID = (function(){
"use strict";
"""

TAIL = """
return {%s};
})();
""" % ", ".join("%s: %s" % (n, n) for n in EXPORTS)


def main():
    seen, parts = set(), []
    for name in NEEDED:
        if name in seen:
            continue
        seen.add(name)
        parts.append(slice_decl(name))
    out = HEAD + "\n".join(parts) + TAIL
    # A name can be the second declarator of a multi-declarator `const`
    # (ADDL_MED_RATE lives inside `const ADDL_MED_THRESH = ..., ADDL_MED_RATE = ...`).
    # Slicing by such a name silently misses it, so check the assembled module
    # binds every identifier its own bodies reach for.
    code = re.sub(r"/\*.*?\*/", " ", out, flags=re.S)
    code = re.sub(r"//[^\n]*", " ", code)
    bound = set(re.findall(r"(?:function|const|var|let)\s+([A-Za-z_$][\w$]*)", code))
    bound |= set(re.findall(r",\s*\n?\s*([A-Z][A-Z0-9_]*)\s*=", code))
    used = set(re.findall(r"\b([A-Z][A-Z0-9_]{3,})\b", code))
    missing = sorted(used - bound - {"RESID", "Math", "NaN"})
    assert not missing, "unbound identifiers in the lifted module: %s" % missing
    path = os.path.join(HERE, "_residency_core.js")
    open(path, "w", encoding="utf-8").write(out)
    print("wrote _residency_core.js  %d lines, %d declarations"
          % (len(out.splitlines()), len(seen)))


if __name__ == "__main__":
    main()
