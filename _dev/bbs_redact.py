#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Strip the licensee out of a BBS decision before anything else reads it.

The site's rule is that no disciplined licensee is named. The cheapest way to
keep that rule is to make a name impossible to copy: redact at the door, so the
text an author ever sees does not contain one.

A BBS decision names the person in six predictable places:

  1. the caption block, in capitals, under "In the Matter of the Accusation
     Against:"
  2. the running footer, "(NAME) ACCUSATION" / "NAME -STIPULATED SETTLEMENT"
  3. "Respondent Firstname Lastname (Respondent) is ..."
  4. the criminal case title, "The People of the State of California v. NAME"
  5. the home address printed under the caption
  6. the license number, which is a lookup key on the Board's own site and is
     therefore an identifier even though it is not a name

Everything is replaced with a neutral token. The residual check at the end
looks for any remaining capitalised run that is not a known institution, and
reports it rather than silently passing - a redactor that cannot fail is a
redactor nobody checks.
"""
import re, sys, os, json

TOKEN = "the respondent"

# Words that legitimately appear in capitals in these documents and are not
# the licensee.
SAFE = {
 "BEFORE","THE","BOARD","OF","BEHAVIORAL","SCIENCES","DEPARTMENT","CONSUMER",
 "AFFAIRS","STATE","CALIFORNIA","DECISION","AND","ORDER","STIPULATED",
 "SETTLEMENT","DISCIPLINARY","ACCUSATION","PETITION","FOR","IT","IS","HEREBY",
 "AGREED","BY","BETWEEN","PARTIES","JURISDICTION","PRAYER","WHEREFORE",
 "DATED","EXECUTIVE","OFFICER","ATTORNEY","GENERAL","SUPERVISING","DEPUTY",
 "CAUSE","DISCIPLINE","FIRST","SECOND","THIRD","FOURTH","FIFTH","SIXTH",
 "SEVENTH","EIGHTH","NINTH","TENTH","ELEVENTH","TWELFTH","ORDERED","SO",
 "IN","MATTER","AGAINST","RESPONDENT","LICENSE","NO","NUMBER","MARRIAGE",
 "FAMILY","THERAPIST","LICENSED","CLINICAL","SOCIAL","WORKER","PROFESSIONAL",
 "COUNSELOR","ASSOCIATE","REGISTRATION","OAH","ADMINISTRATIVE","HEARINGS",
 "OFFICE","PROPOSED","DISMISSAL","REVOCATION","SURRENDER","PROBATION",
 "TERMS","CONDITIONS","COSTS","FACTUAL","FINDINGS","LEGAL","CONCLUSIONS",
 "DETERMINATION","ISSUES","EVIDENCE","DISCUSSION","CREDIBILITY","ORDER",
 "PUBLIC","REPROVAL","CITATION","EFFECTIVE","AMENDED","CORRECTED","NUNC",
 "PRO","TUNC","EXHIBIT","A","B","C","D","E","F","G","H","I","J","K","L","M",
 "N","O","P","Q","R","S","T","U","V","W","X","Y","Z","LA","SF","SD",
 # "ANGELES" is deliberately NOT here. It was, for "LOS ANGELES", and it
 # made the caption "MAYRA NIDIA ANGELES HERNANDEZ" unreadable to the name
 # finder - one document out of a hundred and five, with the name intact.
 # City names are handled by the address rule instead.
 "COUNTY","SUPERIOR","COURT","PEOPLE",
 "COMPLAINANT","ALL","NOT","ANY","THAT","THIS","SHALL","MAY","WILL","ARE",
 "HAS","HAVE","BEEN","WAS","WERE","ON","OR","ABOUT","AT","TO","AS","BE",
 "PURSUANT","SECTION","SECTIONS","CODE","BUSINESS","PROFESSIONS","TITLE",
 "REGULATIONS","VEHICLE","PENAL","HEALTH","SAFETY","WELFARE","INSTITUTIONS",
 "GOVERNMENT","EVIDENCE","CIVIL","PROCEDURE","UNITED","STATES","AMERICA",
 "ROBBONTA","ROB","BONTA","STEVE","SODERGREN","SODERN","CHRISTY","BERGER",
}

INSTITUTION_RE = re.compile(
    r"\b(?:UNIVERSITY|COLLEGE|INSTITUTE|CENTER|CENTRE|HOSPITAL|CLINIC|"
    r"ASSOCIATION|SERVICES|FOUNDATION|INC|LLC|LLP|GROUP)\b")


# Internal capitals are normal in surnames - DeLeon, McKay, O'Brien - and the
# first version of this pattern rejected them, which is how a decision reached
# the "failed" pile with the name still in it.
NAME_TOKEN = re.compile(r"^(?:[A-Z][A-Za-z'\u2019\-]{1,}|[A-Z]\.)$")


def looks_like_name(s):
    s = s.strip(" :,.")
    s = re.sub(r",?\s*Respondents?\.?$", "", s, flags=re.I).strip(" :,.")
    ws = s.split()
    if not (2 <= len(ws) <= 5):
        return None
    if INSTITUTION_RE.search(s.upper()):
        return None
    if any(w.upper() in SAFE for w in ws):
        return None
    if not all(NAME_TOKEN.match(w) for w in ws):
        return None
    return s


def caption_name(t):
    """The licensee, from the caption block.

    Handles the four shapes these decisions actually use: an ALL-CAPS name on
    its own line, a Title Case name on its own line, a name followed by
    ", Respondent" on the same line, and a caption whose "Against:" sits on the
    line above. The first version handled only the first of those and failed on
    five of a hundred and five - which, for a redactor, is five documents that
    would have gone to an author with the name still in them.
    """
    m = re.search(r"Matter\s+of\s*the[\s\S]{0,120}?Against:?\s*\n", t[:4000], re.I)
    if m:
        for line in t[m.end():m.end() + 400].split("\n")[:4]:
            got = looks_like_name(line)
            if got:
                return got
    for line in t[:1800].split("\n"):
        got = looks_like_name(line)
        if got:
            return got
    return None


def parts(name):
    """Every way a document refers to the person, longest first."""
    ws = [w for w in re.split(r"[\s,]+", name) if len(w) > 1]
    out = [" ".join(ws)]
    if len(ws) >= 3:
        out.append(ws[0] + " " + ws[-1])
        out.append(" ".join(ws[1:]))
    if len(ws) >= 2:
        out.append(ws[-1] + ", " + ws[0])
    out += ws                      # bare surname / forename
    seen, res = set(), []
    for p in sorted(out, key=len, reverse=True):
        k = p.lower()
        if k not in seen:
            seen.add(k)
            res.append(p)
    return res


def redact(t):
    name = caption_name(t)
    if not name:
        return None, "no caption name found"

    for p in parts(name):
        t = re.sub(r"\b" + r"\s+".join(re.escape(w) for w in p.split())
                   + r"\b", TOKEN, t, flags=re.I)

    # Board staff, deputy attorneys general and administrative law judges are
    # not the licensee, but they are people, and this site does not need their
    # names to make its point either.
    # The signature blocks set these in capitals, which the Title Case
    # patterns below do not reach. Anchored on the title that follows, so it
    # does not need a list of who currently holds the post.
    t = re.sub(r"\b[A-Z][A-Z'\-]+(?:\s+[A-Z][A-Z'\-]+){0,2}\s*\n\s*"
               r"(?=(?:Supervising\s+)?(?:Deputy\s+)?Attorney\s+General)",
               "[a deputy attorney general]\n", t)
    t = re.sub(r"\b[A-Z][A-Z'\-]+(?:\s+[A-Z][A-Z'\-]+){0,2}\s*\n\s*"
               r"(?=Executive\s+Officer)", "[the executive officer]\n", t)

    for role, pat in (("[the Board's executive officer]",
                       r"Steve\s+Soderg\w*|Steve\s+Sodern|Christy\s+Berger"),
                      ("[the Attorney General]", r"Rob\s*Bonta|Robbonta"),
                      ("[a deputy attorney general]",
                       r"(?:Supervising\s+)?Deputy\s+Attorney\s+General\s+"
                       r"[A-Z][\w'\-]+(?:\s+[A-Z]\.?)?(?:\s+[A-Z][\w'\-]+)?"),
                      ("[an administrative law judge]",
                       r"(?:Administrative\s+Law\s+Judge\s+)"
                       r"[A-Z][\w'\-]+(?:\s+[A-Z]\.?)?(?:\s+[A-Z][\w'\-]+)?"
                       r"|[A-Z][\w'\-]+(?:\s+[A-Z]\.?)?(?:\s+[A-Z][\w'\-]+)?"
                       r"(?=,\s*Administrative\s+Law\s+Judge)")):
        t = re.sub(pat, role, t)

    # license and registration numbers are lookup keys on the Board's site
    t = re.sub(r"\b(?:LMFT|LCSW|LPCC|MFC|ASW|AMFT|APCC|PSY|IMF|ISW|PCE|"
               r"ACSW)\s*#?\s*\d{3,7}\b", "[license number]", t, flags=re.I)
    t = re.sub(r"\bLicense\s+No\.?\s*[A-Z]{0,5}\s*\d{3,7}\b",
               "License No. [redacted]", t, flags=re.I)
    # street address under the caption
    t = re.sub(r"\n\s*\d{1,6}\s+[A-Z][\w'\-\.]*(?:\s+[A-Z][\w'\-\.]*){0,4}\s*\n"
               r"\s*[A-Z][\w\s\.'\-]{2,28},\s*CA\s*\d{5}", "\n[address]\n", t)
    # e-mail addresses and phone numbers
    t = re.sub(r"[\w\.\-]+@[\w\.\-]+", "[email]", t)
    t = re.sub(r"\(\s*\d[\d\s I]{1,4}\)\s*[\d\s\-I]{7,12}", "[phone]", t)
    # criminal case titles, which name the defendant
    t = re.sub(r"(People\s+of\s+the\s+State\s+of\s*California\s+v\.?)\s*[^,\(\)]{0,60}",
               r"\1 " + TOKEN, t, flags=re.I)
    return t, None


def residual(t):
    """Capitalised runs that survived. Reported, never trusted away."""
    out = set()
    for m in re.finditer(r"\b[A-Z][A-Z'\-]{2,}(?:\s+[A-Z][A-Z'\-]{1,}){1,3}\b", t):
        s = m.group(0)
        if INSTITUTION_RE.search(s):
            continue
        if all(w in SAFE for w in s.split()):
            continue
        out.add(s)
    return sorted(out)


if __name__ == "__main__":
    os.makedirs("red", exist_ok=True)
    report = {}
    for f in sorted(os.listdir("txt")):
        if not f.endswith(".txt"):
            continue
        t = open("txt/" + f, encoding="utf-8").read()
        r, err = redact(t)
        if err:
            report[f] = {"error": err}
            continue
        # The only test that matters: the name found in the original must
        # not survive anywhere in the output, in any order, in any case.
        nm = caption_name(t)
        leak = [p for p in parts(nm)
                if len(p) > 3 and re.search(r"\b" + re.escape(p) + r"\b", r, re.I)]
        if leak:
            report[f] = {"error": "NAME SURVIVED: %s" % leak[:3]}
            continue
        open("red/" + f, "w", encoding="utf-8").write(r)
        report[f] = {"name_len": len(nm or ""), "residual": residual(r)[:12]}
    json.dump(report, open("redact_report.json", "w"), indent=1)
    bad = [f for f, v in report.items() if v.get("error")]
    withres = [f for f, v in report.items() if v.get("residual")]
    print("redacted %d, failed %d, with residual capitalised runs %d"
          % (len(report) - len(bad), len(bad), len(withres)))
    if bad:
        print("FAILED:", bad[:10])
    from collections import Counter
    c = Counter()
    for v in report.values():
        for s in v.get("residual", []):
            c[s] += 1
    print("\nmost common residuals:")
    for s, n in c.most_common(30):
        print("  %3d  %s" % (n, s))
