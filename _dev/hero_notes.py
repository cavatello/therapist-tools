#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Get the housekeeping small print out of the hero.

Why. Every tool hero had grown the same tail. Measured on the live site:

  grow-your-therapy-practice   breadcrumb / h1 / tagline / lede / worked-example / privacy note
  therapist-tax-strategy       breadcrumb / h1 / tagline / lede / worked-example / privacy note
  associate-mft-job-advisor    breadcrumb / h1 / tagline / lede /                  privacy note
  amft-3000-hours              breadcrumb / h1 / tagline / lede /                  privacy note

Six blocks before the reader can do anything, on a site whose entire proposition
is "put your numbers in". The user's words, looking at one of these: "the h1,
plus paragraph, the cta, then more text, this is a mess here".

The privacy line is the one to move, and the reason is about WHEN it is useful,
not about length. "Nothing is saved and there is no account - your setup lives
in the address bar" answers a question the reader has not asked yet. Nobody
worries about where their data goes before they know what the page does. Put in
the hero it is noise; put directly above the first input it is reassurance,
arriving in the second the reader is deciding whether to type a real number.

So it moves to immediately above the first field group. That is one block off
every tool hero and the sentence starts doing its job.

What is NOT moved. The worked-example caption ("a $200 hour over 24 sessions")
stays in the hero, because it is a caption: it explains the two figures printed
directly above it, and moving it would leave those figures unsourced. The rule
here is that a hero may explain the numbers it shows and may not carry policy.

Idempotent. Run after breadcrumbs.py and before linkcheck.py.
"""
import os, re, sys
from html.parser import HTMLParser

HERE = os.path.dirname(os.path.abspath(__file__))
SITE = os.path.dirname(HERE)
MARK = "/* _dev/hero_notes.py */"
TAG = "<!-- hero-note moved -->"

PAGES = [
    "grow-your-therapy-practice.html",
    "therapist-tax-strategy-california.html",
]

# practice-simulator.html is deliberately NOT here. Its rate/sessions/weeks-off
# fields live INSIDE the hero, and its note already sits immediately above them
# - which is the arrangement this whole pass exists to produce. It failed the
# block-count audit only because that audit counted blocks above the CTA, and a
# page whose lever IS the hero has no CTA above the fields. The audit was wrong,
# not the page; hero-budget.mjs now counts to the first lever instead.

# associate-mft-job-advisor.html and amft-3000-hours-california.html have the
# same note in the same place, but they BUILD it in JavaScript and inject it
# into an empty #apanel in the hero, so it does not exist in the served HTML for
# this pass to find. Those two are fixed at source in mock/amft/build_advisor.py
# and mock/amft/build_hours.py. If either ever moves to static markup, add it
# here and delete its hand-edit.
JS_RENDERED = [
    "associate-mft-job-advisor.html",
    "amft-3000-hours-california.html",
]

# The signature of a housekeeping line. Deliberately narrow: it must talk about
# persistence, not merely mention the word "saved". A wider pattern once matched
# a lede on about.html, which is a page with no fields to move anything to.
HOUSEKEEPING = re.compile(
    r"(nothing is saved|nothing is sent)", re.I)

VOID = {"input", "img", "br", "hr", "meta", "link", "source", "col", "area",
        "base", "embed", "param", "track", "wbr"}
CHROME = {"header", "nav", "footer"}


class Anchor(HTMLParser):
    """Offset of the block holding the first field a reader can actually see.

    An earlier version of this pass anchored on a class name - the first
    `<div class="fgrid|grid4|...">` after the hero - and on practice-simulator
    that matched a .grid4 nested inside `<div id="assoc-fields" hidden>`, a
    collapsed drawer most readers never open. The note was inserted, the file
    parsed, the guards passed, and the paragraph rendered at y=0 with a width of
    0: present in the DOM, invisible on the page. Exactly the failure this
    project has shipped before.

    So: no class names. Walk the document, find the first input/select/textarea
    that is not inside site chrome and has no hidden ancestor, then climb to
    whichever of its ancestors is a direct child of the enclosing <section>.
    That is the block the fields live in, whatever it is called.
    """

    def __init__(self):
        HTMLParser.__init__(self)
        self.stack = []       # [(tag, attrs_dict, start_offset)]
        self.hit = None

    def _off(self):
        line, col = self.getpos()
        return self.offsets[line - 1] + col

    def handle_starttag(self, tag, attrs):
        a = dict(attrs)
        off = self._off()
        if tag in VOID:
            self._consider(tag, a)
            return
        self.stack.append((tag, a, off))
        self._consider(tag, a)

    def handle_startendtag(self, tag, attrs):
        self._consider(tag, dict(attrs))

    def handle_endtag(self, tag):
        for i in range(len(self.stack) - 1, -1, -1):
            if self.stack[i][0] == tag:
                del self.stack[i:]
                return

    def _consider(self, tag, a):
        if self.hit is not None:
            return
        if tag not in ("input", "select", "textarea"):
            return
        chain = self.stack + [(tag, a, None)]
        for t, at, _ in chain:
            if t in CHROME:
                return
            if "hidden" in at:
                return
            st = (at.get("style") or "").replace(" ", "").lower()
            if "display:none" in st or "visibility:hidden" in st:
                return
            if at.get("type") == "hidden":
                return
        # climb to the direct child of the nearest enclosing <section>
        sec = None
        for i in range(len(self.stack) - 1, -1, -1):
            if self.stack[i][0] == "section":
                sec = i
                break
        idx = sec + 1 if sec is not None else 0
        if idx < len(self.stack):
            self.hit = self.stack[idx][2]
        elif self.stack:
            self.hit = self.stack[-1][2]


def field_block_offset(s, after):
    p = Anchor()
    p.offsets = [0]
    for line in s.splitlines(True):
        p.offsets.append(p.offsets[-1] + len(line))
    # feed the whole document so the tag stack is honest, but ignore any hit
    # before the hero ends
    p.feed(s[:after])
    p.close()
    p2 = Anchor()
    p2.offsets = p.offsets
    p2.feed(s)
    p2.close()
    if p2.hit is None or p2.hit < after:
        # first visible field is inside the hero itself; nothing to anchor to
        return None
    return p2.hit

CSS = """
/* The relocated housekeeping note. Small print by weight, but sitting where it
   is actually read - directly above the first field - so it reads as an aside
   to the person about to type, not as another paragraph of preamble. */
.hkn{margin:0 0 14px;font-size:12.6px;line-height:1.55;opacity:.72;max-width:62ch}
.hkn b{font-weight:600}
"""


def find_hero(s):
    """Byte span of the <section> that contains the first <h1>.

    Regex cannot do this: these heroes nest <section>-less divs but the page
    itself has many sections, and taking the first </section> after the h1
    closes the wrong one on pages whose hero contains a nested block. Scan and
    balance instead.
    """
    h1 = s.find("<h1")
    if h1 < 0:
        return None
    start = s.rfind("<section", 0, h1)
    if start < 0:
        return None
    depth = 0
    for m in re.finditer(r"<section\b|</section>", s[start:]):
        depth += 1 if m.group(0).startswith("<section") else -1
        if depth == 0:
            return (start, start + m.end())
    return None


def paragraphs(block):
    """(span, class, inner) for every <p> in the block, non-nested."""
    for m in re.finditer(r'<p\b([^>]*)>((?:(?!</p>).)*)</p>', block, re.S):
        cls = re.search(r'class="([^"]*)"', m.group(1))
        yield (m.start(), m.end()), (cls.group(1) if cls else ""), m.group(2)


def main():
    moved = skipped = 0
    for slug in PAGES:
        path = os.path.join(SITE, slug)
        if not os.path.exists(path):
            print("%-44s MISSING" % slug)
            continue
        s = open(path, encoding="utf-8").read()

        # idempotent: put any previously-moved note back into nothing, i.e. drop
        # it, then re-derive from the hero. Re-deriving is only possible if the
        # hero still has one, so a second run with an already-moved note must
        # not delete it. Instead: if our marker is present, this page is done.
        if TAG in s:
            # still strip and re-add the stylesheet so CSS edits take effect
            s = re.sub(r"\n?<style>" + re.escape(MARK) + r".*?/\* end hkn \*/</style>\n?",
                       "", s, flags=re.S)
            s = s.replace("</body>", "\n<style>" + MARK + CSS + "/* end hkn */</style>\n</body>", 1)
            open(path, "w", encoding="utf-8").write(s)
            print("%-44s already moved" % slug)
            skipped += 1
            continue

        span = find_hero(s)
        if not span:
            print("%-44s no hero found, skipped" % slug)
            continue
        hs, he = span
        hero = s[hs:he]

        hits = [(sp, cls, inner) for sp, cls, inner in paragraphs(hero)
                if HOUSEKEEPING.search(re.sub(r"<[^>]+>", "", inner))]
        if not hits:
            print("%-44s no housekeeping note in hero" % slug)
            continue
        if len(hits) > 1:
            print("%-44s %d notes in hero - merging" % (slug, len(hits)))

        # remove them from the hero, last first so earlier spans stay valid
        note_inner = " ".join(h[2].strip() for h in hits)
        new_hero = hero
        for h in sorted(hits, key=lambda x: -x[0][0]):
            (a, b) = h[0]
            new_hero = new_hero[:a] + new_hero[b:]

        s = s[:hs] + new_hero + s[he:]

        # re-home above the block holding the first field the reader can see
        tail_from = hs + len(new_hero)
        at = field_block_offset(s, tail_from)
        if at is None:
            print("%-44s NO VISIBLE FIELD - note not moved" % slug)
            continue
        s = s[:at] + TAG + '<p class="hkn">' + note_inner + "</p>" + s[at:]

        s = s.replace("</body>", "\n<style>" + MARK + CSS + "/* end hkn */</style>\n</body>", 1)
        open(path, "w", encoding="utf-8").write(s)
        print("%-44s moved (%d chars), anchored at offset %d" % (slug, len(note_inner), at))
        moved += 1

    # ---- guards
    bad = 0
    for slug in PAGES:
        path = os.path.join(SITE, slug)
        if not os.path.exists(path):
            continue
        s = open(path, encoding="utf-8").read()
        if s.count(TAG) != 1:
            print("GUARD %s: %d re-homed notes" % (slug, s.count(TAG))); bad += 1
        if s.count(MARK) != 1:
            print("GUARD %s: %d stylesheets" % (slug, s.count(MARK))); bad += 1
        span = find_hero(s)
        if span:
            hero = s[span[0]:span[1]]
            if HOUSEKEEPING.search(re.sub(r"<[^>]+>", "", hero)):
                print("GUARD %s: housekeeping still in hero" % slug); bad += 1
        if s.count("<h1") != 1:
            print("GUARD %s: %d h1" % (slug, s.count("<h1"))); bad += 1
    if bad:
        sys.exit("hero_notes: %d guard failure(s)" % bad)
    print("%d moved, %d already done" % (moved, skipped))


if __name__ == "__main__":
    main()
