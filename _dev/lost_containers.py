#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""The container rule was lost and its own children's overrides survived.

WHAT WAS REPORTED

"Tyopgrapohy and text still wrong ... forms look awful, not even readable",
with a screenshot of newsletter.html showing:

    $72,000the Solo 401(k) ceiling at real practice profit, against $7,500
    $27,400of that is tax you would have paid anyway, on $253,500 of profit
    And the catchIt is deferred, not forgiven - you pay income tax on the way

WHAT IS ACTUALLY WRONG

Not typography. Layout, in one specific shape worth naming because it will
happen again.

`.issue-row` was authored as two rules:

    .issue-row{display:flex;gap:10px;align-items:baseline;...}
    .issue-row b{font-family:'IBM Plex Mono',monospace;color:var(--gold);flex:none}

Between 8 and 13 August the FIRST stopped being served to the page and the
SECOND survived - it is still in house-rest.css and house-skin.css as a
colour override. So the page ships a `b` styled to be the fixed first cell of
a flex row, inside a container that is no longer a flex row. `flex:none` on a
child of a block box does nothing, and the number runs into the sentence.

Measured on the shipped page, every container in the block had collapsed:

    .issue-h     display:block    should be flex
    .issue-row   display:block    should be flex
    .facts       display:block    should be grid, repeat(3,1fr)
    .fact        padding:0        should be 15px 17px
    .fact em/b/i display:inline   should be block

while the rules that colour and size those same elements were all still
present. That asymmetry is the signature: **a component whose leaves are
styled and whose box is not.**

WHY NO GUARD CAUGHT IT

`family_coverage.py` asks whether a class appears in any selector the page
loads. `.issue-row` does appear - inside `.issue-row b`. So the class counted
as covered while the element it names had no box at all. Coverage of a NAME
is not coverage of a BOX, and this pass is the answer to that hole.

WHERE THE VALUES COME FROM

Recovered from commit 3e24b289 (8 August), the last build in which the block
rendered, then re-expressed in current tokens: `--muted` became `--dim`, the
hard-coded `#4E4940` became `--ink`, `--cream` became `--paper`. Nothing here
is a new design decision - it is the design already agreed, put back.

The sizes ARE raised, and only where a measurement said they had to be. The
consent line - the one sentence California requires a reader to actually
read - shipped at 12px, and the note under it at 10.5px, which is the house
LABEL size, meant for two uppercase words rather than a thirty-word sentence.
The `.fact` label was 9.5px Inter where every other label on the site is
10.5px IBM Plex Mono. The submit button was 40px tall beside a 52px field.

The footer form's dimmer #84AC99 on #123C30 was checked before being touched:
4.76:1, which passes. That is the house footer treatment doing its job, not a
defect, so only its sizes change and its colour is left alone.
"""
import os, re, sys

HERE = os.path.dirname(os.path.abspath(__file__))
SITE = os.path.dirname(HERE)
SUBDIRS = ("money", "licensure", "getting-paid", "practice", "training", "for")

MARK = "/* _dev/lost_containers.py */"
END = "/* /_dev/lost_containers.py */"
OPEN = "<style>" + MARK
SHUT = END + "</style>"

# Every declaration restores a box the page had already lost. The !important
# is not a preference - house-rest.css and house-skin.css both carry
# surviving descendant overrides for these components, and this ships after.
BOX_CSS = """
.issue{border:1px solid var(--line) !important;border-radius:14px;padding:19px 21px !important}
.issue h3{font-size:19px !important;margin:0 0 10px}
.issue p{font-size:15px !important;line-height:1.7;color:var(--ink) !important;margin:0 0 13px}
.issue-h{display:flex !important;gap:10px;align-items:center;flex-wrap:wrap;
border-bottom:1px solid var(--line);padding-bottom:12px;margin-bottom:13px}
.issue-h span{margin-left:auto}
.issue-row{display:grid !important;grid-template-columns:minmax(0,max-content) minmax(0,1fr);
gap:4px 14px;align-items:baseline;padding:10px 0;border-top:1px dashed var(--line);
font-size:15px !important;line-height:1.6}
.issue-row b{align-self:start;font-size:15px !important}
.facts{display:grid !important;grid-template-columns:repeat(3,minmax(0,1fr));
gap:14px;margin-top:18px}
.fact{padding:15px 17px !important}
.fact em{display:block !important;font-style:normal;font-family:'IBM Plex Mono',monospace;
font-size:10.5px !important;font-weight:700;letter-spacing:.09em;text-transform:uppercase;
color:var(--dim) !important;margin:0 0 7px}
.fact b{display:block !important;font-size:19px !important}
.fact i{display:block !important;font-style:normal;font-size:13.5px !important;
color:var(--dim) !important;margin-top:6px;line-height:1.55}
@media (max-width:820px){.facts{grid-template-columns:repeat(2,minmax(0,1fr))}}
@media (max-width:560px){.facts{grid-template-columns:1fr}
.issue-row{grid-template-columns:1fr;gap:2px}}
"""

# THE VISIBLE SCREEN-READER LABEL.
#
# `.sr` is the visually-hidden class. The generic rule that hides it lives
# only in an extracted sheet most pages do not load; `house-chrome.css`
# carries just `.askq .sr`, scoped to the ask-a-question form. So on every
# page whose only `.sr` is the newsletter field's label, the word "Email"
# renders on screen beside the input - measured on 107 pages.
#
# It reads as a stray label, which is what "forms look awful" was pointing
# at, and it is also an accessibility defect in its own right: a duplicate
# visible label for a field that already shows a placeholder.
SR_CSS = """
.sr{position:absolute !important;width:1px !important;height:1px !important;
padding:0 !important;margin:-1px !important;overflow:hidden !important;
clip:rect(0 0 0 0);white-space:nowrap;border:0 !important}
"""

FORM_CSS = """
.nlform input[type=email]{font-size:16px !important;min-height:52px !important}
.nlform button{font-size:15px !important;min-height:52px !important}
.nlform .consent{display:flex;align-items:flex-start;gap:9px;margin-top:11px}
.nlform .consent input[type=checkbox]{margin:2px 0 0;flex:none}
.nlform .consent span{font-size:14px !important;line-height:1.5}
.nlform .nlmeta{font-size:12.5px !important;line-height:1.55;margin-top:9px}
"""

# Match the MARKUP, never the rule text. Six other pages carry `.issue-row`
# rules in a page-local <style> of their own and render no such element -
# dead CSS left by an earlier extraction. An earlier draft of this pass
# matched the rule text and silently restyled all six. A trigger that fires
# on a page's own stylesheet is a trigger that rewrites somebody else's
# working design.
# Whole class TOKENS, not \b. `\bfacts\b` matches `dc-facts`, because a
# hyphen is a word boundary - which is how a first draft of this pass nearly
# shipped a three-column grid onto the narrative block of 48 discipline-case
# pages. Same class name, different component: the exact hazard the house
# notes call "one class, two surfaces".
ATTR = re.compile(r'class="([^"]*)"')
BOX_NAMES = {"issue", "issue-h", "issue-row", "facts", "fact"}
FORM_NAMES = {"nlform"}
SR_NAMES = {"sr"}


def _tokens(t):
    seen = set()
    for m in ATTR.findall(t):
        seen.update(m.split())
    return seen


def pages():
    out = [f for f in sorted(os.listdir(SITE)) if f.endswith(".html")]
    for d in SUBDIRS:
        p = os.path.join(SITE, d)
        if os.path.isdir(p):
            out += ["%s/%s" % (d, f) for f in sorted(os.listdir(p))
                    if f.endswith(".html")]
    return out


def strip(t):
    return re.sub(re.escape(OPEN) + r"[\s\S]*?" + re.escape(SHUT), "", t)


def main():
    check = "--check" in sys.argv
    boxes = forms = srs = 0
    bad = []
    for rel in pages():
        p = os.path.join(SITE, rel)
        with open(p, encoding="utf-8") as fh:
            t = fh.read()
        bare = strip(t)
        tok = _tokens(bare)
        nb, nf = bool(tok & BOX_NAMES), bool(tok & FORM_NAMES)
        ns = bool(tok & SR_NAMES)
        block = (OPEN + (BOX_CSS if nb else "") + (FORM_CSS if nf else "")
                 + (SR_CSS if ns else "") + SHUT)
        if nb:
            boxes += 1
        if nf:
            forms += 1
        if ns:
            srs += 1
        if check:
            if (nb or nf or ns) and OPEN not in t:
                bad.append("%s renders the component and carries no CSS for it" % rel)
            if OPEN in t and not (nb or nf or ns):
                bad.append("%s carries the CSS and renders no component" % rel)
            continue
        new = bare
        if nb or nf or ns:
            i = new.rfind("</head>")
            if i < 0:
                bad.append("%s has no </head>" % rel)
                continue
            new = new[:i] + block + new[i:]
        if new != t:
            with open(p, "w", encoding="utf-8") as fh:
                fh.write(new)

    if check:
        if bad:
            print("  lost_containers.py: %d problem(s)" % len(bad))
            for b in bad:
                print("    " + b)
            return 1
        print("  guards clean - the issue block has a box on %d page(s), the "
              "signup form on %d, the hidden label on %d" % (boxes, forms, srs))
        return 0
    print("  container rules restored: issue block on %d page(s), signup form "
          "on %d, visually-hidden label on %d" % (boxes, forms, srs))
    return 0


if __name__ == "__main__":
    sys.exit(main())
