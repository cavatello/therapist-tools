#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Remove HTML comment markers from stylesheets, and rehash the files.

THE BUG THIS EXISTS TO CLOSE. `_dev/uplinks.py` opened its <style> block with
the string "<!-- _dev/uplinks.py -->" as a marker. Inside CSS that is a CDO
token: legal between rules, so nothing errors and nothing appears in the
console - but the text following it is then read as the beginning of a SELECTOR,
and the parser consumes until the next "{". The next "{" belonged to the rule
below it, so the rule that actually shipped was

    _dev/uplinks.py --> .uplink { max-width:1120px;margin:34px auto 8px }

an invalid selector, and the entire declaration block was dropped. The up-link
("More on this") therefore had no max-width and no auto margins: it ran the full
width of the viewport while the footer directly under it sat in a 1180px centred
column. At 1280px that is a small misalignment; at 2560px the two adjacent
blocks are ~700px out of line, which is what "the footer is broken" meant.

extract_css.py then lifted the block, comment and all, into css/, so the same
dead rule was being served from a cached file to 120 pages.

WHY IT REHASHES. A file in css/ is named for the sha1 of its contents - that is
the cache key and the thing extract_css.py checks. Editing the bytes in place
would leave a file whose name no longer describes it, and the next person to
compare the two would be right to distrust both. So the repaired block is
written under its new hash, every link is repointed, and the stale file is
removed only once nothing references it.

Idempotent, and guarded: it exits non-zero if any stylesheet still contains a
CDO or CDC token, or if any page points at a file that is not there.

Run after extract_css.py.
"""
import os, re, sys, hashlib

HERE = os.path.dirname(os.path.abspath(__file__))
SITE = os.path.dirname(HERE)
CSSDIR = os.path.join(SITE, "css")
SUBDIRS = ("money", "licensure", "getting-paid", "practice", "training")

LINKED = re.compile(r'<link rel="stylesheet" href="((?:\.\./)*)css/([0-9a-f]{12})\.css">')
CDO = re.compile(r"<!--(.*?)-->", re.S)


def pages():
    out = [f for f in sorted(os.listdir(SITE)) if f.endswith(".html")]
    for d in SUBDIRS:
        p = os.path.join(SITE, d)
        if os.path.isdir(p):
            out += ["%s/%s" % (d, f) for f in sorted(os.listdir(p))
                    if f.endswith(".html")]
    return out


def main():
    remap = {}
    for fn in sorted(os.listdir(CSSDIR)):
        if not fn.endswith(".css"):
            continue
        path = os.path.join(CSSDIR, fn)
        body = open(path, encoding="utf-8").read()
        if "<!--" not in body and "-->" not in body:
            continue
        fixed = CDO.sub(lambda m: "/*%s*/" % m.group(1), body)
        # A stray opener or closer with no partner: comment out the token
        # rather than leaving half of one behind.
        fixed = fixed.replace("<!--", "/*").replace("-->", "*/")
        new = hashlib.sha1(fixed.encode("utf-8")).hexdigest()[:12]
        old = fn[:-4]
        open(os.path.join(CSSDIR, "%s.css" % new), "w", encoding="utf-8").write(fixed)
        remap[old] = new
        print("  %s -> %s  (%d marker(s) removed)"
              % (old, new, body.count("<!--")))

    if not remap:
        print("no HTML comments in css/ - nothing to do")
    else:
        n = 0
        for rel in pages():
            p = os.path.join(SITE, rel)
            s = open(p, encoding="utf-8").read()
            out = LINKED.sub(
                lambda m: '<link rel="stylesheet" href="%scss/%s.css">'
                          % (m.group(1), remap.get(m.group(2), m.group(2))), s)
            if out != s:
                open(p, "w", encoding="utf-8").write(out)
                n += 1
        print("%d page(s) repointed" % n)

        # Only now, and only if nothing still names it.
        live = set()
        for rel in pages():
            live |= set(h for _u, h in
                        LINKED.findall(open(os.path.join(SITE, rel),
                                            encoding="utf-8").read()))
        for old in remap:
            if old not in live:
                # MOVED, not deleted. This repository is edited through a bridge
                # that cannot unlink, and a half-completed clean-up that raises
                # PermissionError after repointing 120 pages leaves the site in
                # a worse state than one that never tried. _to_delete/ is where
                # this project already parks things it is finished with.
                bin_ = os.path.join(SITE, "_to_delete")
                os.makedirs(bin_, exist_ok=True)
                try:
                    os.replace(os.path.join(CSSDIR, "%s.css" % old),
                               os.path.join(bin_, "stale-%s.css" % old))
                    print("  css/%s.css -> _to_delete/" % old)
                except OSError as e:
                    print("  could not move css/%s.css (%s) - it is unreferenced,"
                          " so it is dead weight rather than a fault" % (old, e))

    bad = 0
    for fn in sorted(os.listdir(CSSDIR)):
        if not fn.endswith(".css"):
            continue
        b = open(os.path.join(CSSDIR, fn), encoding="utf-8").read()
        if "<!--" in b or "-->" in b:
            print("GUARD css/%s: still carries an HTML comment" % fn)
            bad += 1
        h = hashlib.sha1(b.encode("utf-8")).hexdigest()[:12]
        if h != fn[:-4]:
            print("GUARD css/%s: name does not match its contents (%s)" % (fn, h))
            bad += 1
    for rel in pages():
        s = open(os.path.join(SITE, rel), encoding="utf-8").read()
        for _u, h in LINKED.findall(s):
            if not os.path.exists(os.path.join(CSSDIR, "%s.css" % h)):
                print("GUARD %s: links css/%s.css which does not exist" % (rel, h))
                bad += 1
    if bad:
        sys.exit("\n%d problem(s)" % bad)
    print("guards clean")


if __name__ == "__main__":
    main()
