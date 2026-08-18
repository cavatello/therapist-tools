#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""P8's slab, rolled out from a claims file, with the claim checked.

WHAT P8 ASKS FOR

    | HEY | One slab per page. **One.** | Deep pine, scalloped edges, aimed
    | at the one claim that page makes.

`slab_guard.py` enforces the ceiling and has since it was written. It
deliberately does NOT enforce the floor, and says why: 241 pages of 242 carry
no slab, and each slab is "aimed at the one claim that page makes", so adding
them is writing 236 claims. That is a content project. This file is the
machinery that content project ships through.

WHY A PASS AND NOT AN EDIT

Every page here is written whole by a builder on every run. A slab typed into
a page by hand is gone the next time `ship.py` runs, silently, with no guard
failing. So the claims live in `_dev/slab_claims.json` and this pass puts them
back on every build.

THE ANCHOR, WHICH IS THE POINT OF THE WHOLE FILE

Each record carries an `anchor`: the exact string the claim rests on - a
figure, a count, a code section. Before a slab is emitted, the anchor must be
present in the page **as it ships**, after every builder and every family pass
has run. A record whose anchor is absent is a failure, not a warning.

Three things that buys, none of which a style rule can:

  1. It stops a claim being written from metadata instead of from the page.
     `mock/library/registry.json` carries a `number` per page and flags 168 of
     its 232 records stale - several still using the word the plain-words pass
     removed from 199 pages. A claim drafted from that would be plausible,
     well-voiced, and wrong.
  2. It fails when a builder's figure moves. These pages are rebuilt from live
     data. The slab is the one sentence on a page that must not go quietly
     stale, and this is the only thing that would notice.
  3. It bounds what a claim may say. No anchor, no slab - which is why the
     exempt list exists and carries a reason per page rather than a silence.

An anchor that is present does NOT make the sentence around it fair. That part
is read by a person before a wave ships. This checks the half a machine can.

WHERE THE SLAB CAN LIVE, AND WHERE IT CANNOT

The P8 slab's fill, its text colours and its scalloped edge are all scoped to
`body.bc2` in `css/house.css`. 239 of 242 pages carry that class. The three
that do not are `tools.html` and `tycoon.html`, which carry no class on the
body at all - the same fact that forced `mockup_floor.py` to exist - and
`rates.html`, whose body is `ratespage` and whose editorial voice is excluded
from the house passes by decision. A slab on any of those three renders as an
unstyled block: correct markup, no pine, no scallop, and nothing failing. So
this pass refuses to place one there rather than trusting the caller.

That is the same class-scoping trap this repository has now hit nine times.
Here it is checked instead of remembered.

AND THE TENTH, WHICH THIS PASS FOUND BY LOOKING

Carrying `bc2` turns out NOT to be enough. The first slab this pass placed -
on `amft-3000-hours-california.html`, a page that carries `bc2` - rendered
with a WHITE fill and its white heading on top of it: a contrast ratio of
1.00, an invisible claim, and not one static check anywhere in this tree
noticed. `node`-equivalent syntax checks passed, `slab_guard.py` was clean,
the scalloped edge was correctly applied. Only loading the page in a real
browser and reading the computed background found it.

The cause is a THIRD component wearing the name. Alongside the P8 slab and
the coloured section band there is a page-local card rule, `.adv .slab`,
carrying `background:var(--white)`, that ships inside a style block on the
page itself. It has the same specificity as house.css's `.bc2 .slab` and
comes later, so it wins. It had never mattered, because until now no page
carrying it also carried a bare slab - a latent rule that only bites the
moment the rollout starts.

So this pass does not trust the cascade. It wraps its slab in a container of
its own and re-asserts the fill, the four text colours and the scalloped edge
against it with `!important` - the same move `mobile_reassert.py` and
`mockup_floor.py` make, and for the same reason. The colours are written as
literal tokens rather than `var()` so a page that never defined the custom
property still renders a readable slab.

**No wave of these ships without a browser pass that reads the computed
background of every slab it placed.** A slab is the one element on a page
whose entire job is to be read, and this failure mode is silent.

TELLING THE TWO COMPONENTS APART

`.slab` names two things on this site: the P8 slab, which carries the class
and nothing else, and a coloured section band, which always carries a colour
modifier. `slab_guard.py` documents the separation and reads the modifier
rather than renaming a component. This pass emits only the bare form, and
counts only the bare form.

WHERE ON THE PAGE, AND WHY IT IS NOT ALWAYS THE SAME PLACE

By default the slab goes as low as it can - above the ask surface, the footer
band or the footer, whichever comes first. That is right for an article, where
the claim is the last thing read.

It is wrong on `practice-simulator.html`, and looking at it is the only way
that was found. The default slot there is directly above the newsletter band,
which is also deep pine: the slab's bottom scallop bites into an identical
green, so it stops reading as a separate object and becomes a notch between
two blocks. Moved above the "where you are on the path" block it has paper on
both sides and both scalloped edges read.

So a record may carry `before`: a literal string to insert in front of,
overriding the default chain. If that string is not on the page the pass
FAILS rather than quietly falling back to the default - a placement that
silently reverts to the thing it was written to avoid is worse than no
placement control at all.

WHY THERE IS A --strip, AND WHY IT RUNS EARLY

The slab is placed in LAST, after the hoisting chain. But an article page is
not rewritten by any builder, so once a slab has shipped it is still sitting
in the tree at the START of the next build - and the family passes carry
hardcoded allow-lists of the classes their pages may wear. `family_art.py`
duly failed 7 pages with `uncovered classes: eb mark p8slab slab`.

That is not an artefact of one messy working copy. It is what every build
after the first deploy would do. So the pass takes the slab out again at the
top of STRUCTURE and puts it back in LAST, which means every pass in between
sees exactly the site it would see on a virgin build. No other pass has to
learn that this component exists.

    python3 _dev/slab_rollout.py            place the slabs
    python3 _dev/slab_rollout.py --check    verify only; writes nothing
    python3 _dev/slab_rollout.py --strip    take them out again, for the
                                            passes that run in between

Idempotent: markered block, rewritten in place.
"""
import os, re, sys, json

HERE = os.path.dirname(os.path.abspath(__file__))
SITE = os.path.dirname(HERE)
SUBDIRS = ("money", "licensure", "getting-paid", "practice", "training", "for")

MARK = "<!-- _dev/slab_rollout.py -->"
END = "<!-- /_dev/slab_rollout.py -->"
DATA = os.path.join(HERE, "slab_claims.json")

CSS_MARK = "/* _dev/slab_rollout.py */"
CSS_END = "/* /_dev/slab_rollout.py */"

# Re-asserted rather than inherited. See the note on the tenth collision
# above: `.bc2 .slab` loses to a page-local card rule of equal specificity,
# so every value the slab needs in order to be legible is set here and won
# on importance rather than on order. Literal tokens, not var(), so a page
# that never defined the custom properties still renders.
#
# The scalloped edge is spelled as a mask built from radial gradients. That
# is P8's signature and `slab_guard.py` is the tripwire that keeps a future
# gradient-removing pass from squaring it off - the spelling here has to stay
# matchable by that guard.
CSSBODY = """
/* ON THE PAGE GRID, like everything else.
   The slab shipped full-bleed: 1904px at a 1920 viewport, against a masthead
   of 1560 and content wraps of 948-1180. It was the widest thing on every page
   it landed on, by up to 970px, and it read - correctly - as broken. The home
   page's hand-written slab had always done this; the rollout put it on forty
   more pages, which is what made it obvious.
   1180 / 1320 / 1560 with 26px of padding are one_grid.py's CANON and STEPS,
   which are the same numbers widen.py gives the masthead. The guard in
   one_grid.py checks those two agree; this follows them. */
.p8slab{max-width:1180px;margin-left:auto;margin-right:auto;
padding-left:26px;padding-right:26px;box-sizing:border-box}
@media (min-width:1500px){.p8slab{max-width:1320px}}
@media (min-width:1900px){.p8slab{max-width:1560px}}
/* index.html's slab is hand-written and has no wrapper of its own, so it takes
   the same measure directly - the grid width less the 26px of padding either
   side, so its edge lands where the wordmark starts rather than where the
   masthead's box does. Both slabs then begin at the same x. */
main.home>.slab{max-width:1128px;margin-left:auto;margin-right:auto}
@media (min-width:1500px){main.home>.slab{max-width:1268px}}
@media (min-width:1900px){main.home>.slab{max-width:1508px}}
.p8slab .slab{background:#123C30 !important;color:#FFFFFF !important;
-webkit-mask:radial-gradient(9px at 50% 0,transparent 98%,#000) repeat-x 0 0/30px 10px,
radial-gradient(9px at 50% 100%,transparent 98%,#000) repeat-x 0 100%/30px 10px,
linear-gradient(#000,#000) no-repeat 0 10px/100% calc(100% - 20px);
mask:radial-gradient(9px at 50% 0,transparent 98%,#000) repeat-x 0 0/30px 10px,
radial-gradient(9px at 50% 100%,transparent 98%,#000) repeat-x 0 100%/30px 10px,
linear-gradient(#000,#000) no-repeat 0 10px/100% calc(100% - 20px)}
.p8slab .slab h2{color:#FFFFFF !important}
.p8slab .slab p{color:#C6DBD1 !important;max-width:56ch}
.p8slab .slab .eb{color:#FFE7A3 !important}
.p8slab .slab .mark{background:#FFE7A3 !important;color:#123C30 !important}
.p8slab .slab p b,.p8slab .slab p strong{color:#FFFFFF !important}
"""



# The class the P8 slab's fill, colours and scallop are all scoped to.
SCOPE = "bc2"

# Budgets from claude/slab-claim-voice-and-rules.md. A claim that needs more
# room than this is making more than one claim.
MAX_CLAIM_WORDS = 22
MAX_SUPPORT_WORDS = 45
MAX_EYEBROW_WORDS = 5


def pages():
    out = [f for f in sorted(os.listdir(SITE)) if f.endswith(".html")]
    for d in SUBDIRS:
        p = os.path.join(SITE, d)
        if os.path.isdir(p):
            out += ["%s/%s" % (d, f)
                    for f in sorted(os.listdir(p)) if f.endswith(".html")]
    return out


def load():
    if not os.path.exists(DATA):
        return {"claims": {}, "exempt": {}}
    return json.load(open(DATA, encoding="utf-8"))


STYLE_OPEN = "<style>" + CSS_MARK
STYLE_SHUT = CSS_END + "</style>"


def strip(s):
    """Take away both things this pass writes: the block, and the one style
    element it ships alongside it. Idempotency depends on removing the style
    element too - otherwise a second run stacks a second copy and
    `extract_css.py` hoists two byte-identical sheets instead of one."""
    s = re.sub(re.escape(MARK) + r"[\s\S]*?" + re.escape(END), "", s)
    s = re.sub(re.escape(STYLE_OPEN) + r"[\s\S]*?" + re.escape(STYLE_SHUT),
               "", s)
    return s


def esc(t):
    return t.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")


def block(rec):
    """The P8 slab. Bare class - a colour modifier here would switch the
    one-per-page rule off, which slab_guard.py checks separately."""
    o = ['<div class="p8slab"><div class="slab">']
    o.append('<span class="eb">%s</span>' % esc(rec["eyebrow"]))
    o.append("<h2>%s</h2>" % esc(rec["claim"]))
    sup = esc(rec["support"])
    mark = rec.get("mark")
    if mark:
        # one highlighted span, on the phrase the claim turns on
        sup = sup.replace(esc(mark),
                          '<span class="mark">%s</span>' % esc(mark), 1)
    o.append("<p>%s</p>" % sup)
    o.append("</div></div>")
    return MARK + "".join(o) + END


def words(t):
    return len(t.split())


def shape_problems(page, rec):
    """Everything about a record that can be judged without the page."""
    bad = []
    for k in ("eyebrow", "claim", "support", "anchor"):
        if not rec.get(k, "").strip():
            bad.append("%s: %s is empty" % (page, k))
    if not bad:
        if words(rec["eyebrow"]) > MAX_EYEBROW_WORDS:
            bad.append("%s: eyebrow is %d words, budget %d"
                       % (page, words(rec["eyebrow"]), MAX_EYEBROW_WORDS))
        if ":" in rec["eyebrow"]:
            bad.append("%s: eyebrow carries a colon" % page)
        if words(rec["claim"]) > MAX_CLAIM_WORDS:
            bad.append("%s: claim is %d words, budget %d"
                       % (page, words(rec["claim"]), MAX_CLAIM_WORDS))
        if not rec["claim"].rstrip().endswith((".", "?", "!")):
            bad.append("%s: claim does not end in a full stop" % page)
        if words(rec["support"]) > MAX_SUPPORT_WORDS:
            bad.append("%s: support is %d words, budget %d"
                       % (page, words(rec["support"]), MAX_SUPPORT_WORDS))
        if rec.get("mark") and rec["mark"] not in rec["support"]:
            bad.append("%s: mark phrase is not in the support line" % page)
        if "before" in rec and not rec["before"].strip():
            bad.append("%s: before is present but empty" % page)
        # the standing legal constraint, in the one place it would be worst
        if re.search(r"\bLLC\b", rec["claim"] + rec["support"]):
            bad.append("%s: claim or support says LLC - Cal. Corp. Code "
                       "17701.04(e) blocks it for this audience" % page)
    return bad


def strip_all():
    """Every slab this pass has ever placed, taken out. Idempotent, and safe
    to run on a tree that has none."""
    n = 0
    for page in pages():
        p = os.path.join(SITE, page)
        s = open(p, encoding="utf-8").read()
        out = strip(s)
        if out != s:
            open(p, "w", encoding="utf-8").write(out)
            n += 1
    print("%d page(s) cleared of a slab, so the passes between here and LAST "
          "see the site they would see on a virgin build." % n)


def main(check_only=False):
    data = load()
    claims = data.get("claims", {})
    exempt = data.get("exempt", {})
    allp = pages()
    bad = []

    for page in sorted(claims):
        if page not in allp:
            bad.append("%s: has a claim but is not a published page" % page)

    placed = 0
    for page in allp:
        p = os.path.join(SITE, page)
        s = open(p, encoding="utf-8").read()
        rec = claims.get(page)
        stripped = strip(s)

        if rec is None:
            # No claim. But a page can carry a bare slab this pass did not
            # place - index.html's is hand-written and exempt by name - and it
            # needs the grid rules just as much, so it gets the stylesheet
            # without the markup.
            out = stripped
            if re.search(r'class="slab"', out):
                h = out.rfind("</head>")
                if h >= 0:
                    out = out[:h] + STYLE_OPEN + CSSBODY + STYLE_SHUT + out[h:]
            if out != s and not check_only:
                open(p, "w", encoding="utf-8").write(out)
            continue

        bad += shape_problems(page, rec)

        # the anchor, against the page WITHOUT our own block, so a claim
        # cannot satisfy its own anchor by quoting it
        if rec["anchor"] not in stripped:
            bad.append("%s: anchor %r is not on the page as it ships"
                       % (page, rec["anchor"]))
            continue

        m = re.search(r"<body([^>]*)>", stripped)
        bodyclass = ""
        if m:
            c = re.search(r'class="([^"]*)"', m.group(1))
            bodyclass = c.group(1) if c else ""
        if SCOPE not in bodyclass.split():
            bad.append("%s: body is %r, so the slab would render with no "
                       "pine and no scallop" % (page, bodyclass or "(unclassed)"))
            continue

        # a bare slab already present, that is not ours, is the ceiling
        others = len(re.findall(r'class="slab"', stripped))
        if others:
            bad.append("%s: already carries %d bare slab(s) this pass does "
                       "not own" % (page, others))
            continue

        # Resolved BEFORE the --check early return, deliberately. A `before`
        # target that a builder has renamed is exactly the kind of drift
        # VERIFY exists to catch, and it would be invisible if this only ran
        # on the writing path.
        anchor = None
        want = rec.get("before")
        if want:
            i = stripped.find(want)
            if i < 0:
                bad.append("%s: before %r is not on the page, and this pass "
                           "will not fall back to the default slot behind "
                           "your back" % (page, want))
                continue
            anchor = i

        if check_only:
            placed += 1
            continue

        if not want:
            for pat in (r"</main>",
                        r"<!-- _dev/ask_surface\.py -->",
                        r"<!-- _dev/footer_band\.py -->",
                        r'<section class="ftnl"',
                        r"<!-- _dev/uplinks\.py -->",
                        r'<section class="uplink"',
                        r"<footer"):
                mm = re.search(pat, stripped)
                if mm:
                    anchor = mm.start()
                    break
        if anchor is None:
            bad.append("%s: nothing to anchor the slab above" % page)
            continue
        out = stripped[:anchor] + block(rec) + stripped[anchor:]

        # The style element, byte-identical on every page that gets a slab,
        # so extract_css.py hoists it once and css_dedupe.py collapses the
        # copies. Placed last in the head so it wins on order as well as on
        # importance.
        h = out.rfind("</head>")
        if h < 0:
            bad.append("%s: has no head to put the slab style in" % page)
            continue
        out = out[:h] + STYLE_OPEN + CSSBODY + STYLE_SHUT + out[h:]

        if out != s:
            open(p, "w", encoding="utf-8").write(out)
        placed += 1

    # exempt pages must stay bare, and must say why
    for page, reason in sorted(exempt.items()):
        if not reason.strip():
            bad.append("%s: exempt with no reason recorded" % page)
        if page in claims:
            bad.append("%s: is both exempt and claimed" % page)

    if bad:
        for b in bad:
            print("GUARD: %s" % b)
        sys.exit("%d problem(s)" % len(bad))

    gap = len(allp) - placed - len(exempt) - 1  # index.html carries its own
    print("%d slab(s) placed from %d claim(s), %d page(s) exempt by name."
          % (placed, len(claims), len(exempt)))
    print("P8's rollout gap: %d published page(s) still have no claim written."
          % max(gap, 0))


if __name__ == "__main__":
    if "--strip" in sys.argv:
        strip_all()
    else:
        main("--check" in sys.argv)
