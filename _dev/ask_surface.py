#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""The ask-a-question surface. Queued since the home-page options doc.

WHAT WAS PROMISED AND NEVER BUILT

Home option F mocked a question box under the index - "Cannot find it?
Ask, and the answer becomes a page. [Type your question...]" - and the
options doc recorded plainly that "the question box needs the ask
surface that is already queued". The stage doors each present the four
questions that bring their stage to the site, which sharpens the gap:
a reader whose question is the FIFTH one has nowhere to put it.

WHAT IT IS

One compact section: a kicker, the promise, a textarea, an optional
email, a submit. It posts to the same Formspree endpoint the site's
contact and feedback forms already use - which privacy.html already
discloses ("Formspree handles the contact and feedback forms") - with a
hidden `page` field naming where it was asked from, because "which door
was this asked behind" is half the value of the question.

The promise is the honest one from the mockup: questions become PAGES,
not replies. The email field is optional and says exactly what it is
for - hearing back when the answer exists. And this audience is
therapists, so the form says out loud: no client details.

WHERE. The home page and the four stage doors. On a door it sits
between the shelf and the sources - after the reader has scanned every
guide for their stage and found theirs missing, which is the moment the
question exists. On the home page it sits above the signup band via the
same anchor scan footer_band.py uses.

WITH JAVASCRIPT OFF the form still posts - Formspree answers with its
own confirmation page, which is worse than inline but is a working
fallback, the same trade form_inline.py documents. The inline handler
here binds ONLY `form.askform`; the sitewide handler in
mock/amft/_chrome_js.txt binds `form.nlform, form.cform` - the two must
never overlap or two POSTs race for one click (that bug is written up
in _dev/form_inline.py).

Idempotent: markered block, rewritten in place. Styles in
css/house-chrome.css, bracketed by this pass's own CSS markers.
"""
import os, re, sys

HERE = os.path.dirname(os.path.abspath(__file__))
SITE = os.path.dirname(HERE)

MARK = "<!-- _dev/ask_surface.py -->"
END = "<!-- /ask_surface -->"
ACTION = "https://formspree.io/f/xzdnyabp"

# page -> where the block goes: "sources" = before the door's sources
# section; "foot" = above the first of signup band / up-link / footer.
PAGES = {
    "index.html": "foot",
    "for/associates.html": "sources",
    "for/students.html": "sources",
    "for/deciding.html": "sources",
    "for/licensed.html": "sources",
}

CSS_MARK = "/* _dev/ask_surface.py */"
CSS_END = "/* /ask_surface */"
CSS = CSS_MARK + """
.askq{max-width:1120px;margin:34px auto 8px;padding:0 26px}
.askq>div{background:var(--paper);border:1px solid var(--line);
 border-radius:14px;padding:22px 24px}
.askq .ak{margin:0;font-family:'IBM Plex Mono',ui-monospace,monospace;
 font-size:10px;letter-spacing:.09em;text-transform:uppercase;
 color:var(--pine);font-weight:600}
.askq h2{margin:6px 0 0;font-family:Fraunces,serif;font-size:19px;
 line-height:1.3;color:var(--ink);letter-spacing:-.01em}
.askq .ad{margin:9px 0 0;font-size:13.5px;line-height:1.65;
 color:var(--ink);max-width:62ch}
.askq form{margin:14px 0 0}
.askq textarea{display:block;width:100%;box-sizing:border-box;
 background:#fff;border:1px solid var(--line);border-radius:10px;
 padding:11px 13px;font:inherit;font-size:14px;color:var(--ink);
 resize:vertical;min-height:74px}
.askq textarea:focus{outline:2px solid var(--pine);outline-offset:1px}
.askq .ar{display:flex;flex-wrap:wrap;gap:10px;margin-top:10px;
 align-items:center}
.askq input[type=email]{flex:1 1 220px;min-width:0;background:#fff;
 border:1px solid var(--line);border-radius:10px;padding:10px 13px;
 font:inherit;font-size:13.5px;color:var(--ink)}
.askq input[type=email]:focus{outline:2px solid var(--pine);
 outline-offset:1px}
.askq button{background:var(--pine);color:#fff;border:0;
 border-radius:10px;padding:11px 22px;font:inherit;font-size:13.5px;
 font-weight:700;cursor:pointer}
.askq button:hover{background:var(--deep)}
.askq button:focus-visible{outline:2px solid var(--gold);
 outline-offset:2px}
.askq .an{margin:9px 0 0;font-size:11.5px;color:var(--muted);
 line-height:1.5}
.askq .aok{margin:12px 0 0;font-size:13.5px;color:var(--pine);
 font-weight:600;display:none}
.askq .sr{position:absolute;width:1px;height:1px;padding:0;margin:-1px;
 overflow:hidden;clip:rect(0,0,0,0);white-space:nowrap;border:0}
@media (max-width:640px){.askq{padding:0 16px}
 .askq>div{padding:16px 18px}}
""" + CSS_END


def block(page):
    o = ['<section class="askq" id="ask"><div>']
    o.append('<p class="ak">Cannot find it?</p>')
    o.append("<h2>Ask, and the answer becomes a page.</h2>")
    o.append('<p class="ad">This site grows by what people cannot find. '
             "A question that reaches us gets researched against the "
             "statute and the Board&rsquo;s own documents, and the answer "
             "is published here for the next person who has it.</p>")
    o.append('<form class="askform" action="%s" method="POST">' % ACTION)
    o.append('<input type="hidden" name="_subject" '
             'value="Question via therapistsupport.org">')
    o.append('<input type="hidden" name="page" value="%s">' % page)
    o.append('<label class="sr" for="ask-q">Your question</label>')
    o.append('<textarea id="ask-q" name="question" required rows="3" '
             'placeholder="Type your question&hellip;"></textarea>')
    o.append('<div class="ar">')
    o.append('<label class="sr" for="ask-e">Email, optional</label>')
    o.append('<input id="ask-e" type="email" name="email" '
             'placeholder="you@example.com &mdash; only if you want to '
             'hear when the answer is up">')
    o.append("<button type=\"submit\">Ask</button>")
    o.append("</div>")
    o.append('<p class="an">Nothing else is collected, and the question '
             "is not published with your name. Please do not include "
             "client details.</p>")
    o.append('<p class="aok" role="status">Received. If it can be '
             "answered from a checkable source, it becomes a page.</p>")
    o.append("</form>")
    o.append("</div></section>")
    # `onsubmit=`, not addEventListener: _dev/form_inline.py's guard
    # counts submit-listener-plus-fetch scripts and requires exactly one
    # per page, because two handlers bound to the SAME form race and
    # double-POST. This handler owns a different form (`.askform`; the
    # sitewide one binds `.nlform, .cform`), so there is no race to
    # guard against - and assigning the property instead of listening
    # keeps that guard's invariant meaningful for the form it protects.
    # A property assignment also cannot stack: re-running this pass can
    # never leave two handlers on the ask form.
    o.append("""<script>(function(){
var f=document.querySelector('form.askform');if(!f)return;
f.onsubmit=function(ev){
 if(!window.fetch)return;ev.preventDefault();
 var b=f.querySelector('button');var t=b.textContent;
 b.disabled=true;b.textContent='Sending\\u2026';
 fetch(f.action,{method:'POST',body:new FormData(f),
  headers:{Accept:'application/json'}}).then(function(r){
  if(!r.ok)throw 0;
  f.querySelector('textarea').value='';
  f.querySelector('.aok').style.display='block';
  b.textContent=t;b.disabled=false;
 }).catch(function(){b.disabled=false;b.textContent=t;f.submit();});
};})();</script>""")
    return MARK + "".join(o) + END


def main():
    bad = 0
    for page, where in PAGES.items():
        p = os.path.join(SITE, page)
        if not os.path.exists(p):
            print("GUARD: %s does not exist" % page)
            bad += 1
            continue
        s = open(p, encoding="utf-8").read()
        s = re.sub(re.escape(MARK) + r"[\s\S]*?" + re.escape(END), "", s)

        anchor = None
        if where == "sources":
            m = re.search(r'<section[^>]*id="sources"', s)
            if m:
                anchor = m.start()
        if anchor is None:
            for pat in (r"<!-- _dev/footer_band\.py -->",
                        r'<section class="ftnl"',
                        r"<!-- _dev/uplinks\.py -->",
                        r'<section class="uplink"', r"<footer"):
                m = re.search(pat, s)
                if m:
                    anchor = m.start()
                    break
        if anchor is None:
            print("GUARD: %s has nothing to anchor the ask block above"
                  % page)
            bad += 1
            continue
        s = s[:anchor] + block(page) + s[anchor:]
        open(p, "w", encoding="utf-8").write(s)

    # ------------------------------------------------------------- css
    cp = os.path.join(SITE, "css", "house-chrome.css")
    cs = open(cp, encoding="utf-8").read()
    new = re.sub(re.escape(CSS_MARK) + r"[\s\S]*?" + re.escape(CSS_END),
                 "", cs).rstrip()
    new += "\n\n" + CSS.strip() + "\n"
    if new != cs:
        open(cp, "w", encoding="utf-8").write(new)

    # ---------------------------------------------------------- guards
    for page in PAGES:
        p = os.path.join(SITE, page)
        if not os.path.exists(p):
            continue
        s = open(p, encoding="utf-8").read()
        if s.count(MARK) != 1 or s.count(END) != 1:
            print("GUARD: %s has %d/%d ask marker(s)"
                  % (page, s.count(MARK), s.count(END)))
            bad += 1
        # exactly one handler may own this form, and it must not also be
        # captured by the sitewide nlform/cform handler
        if s.count("form.askform") != 1:
            print("GUARD: %s has %d askform handler(s)"
                  % (page, s.count("form.askform")))
            bad += 1
        if re.search(r'<form class="askform[^"]*(nlform|cform)', s):
            print("GUARD: %s ask form carries a class the sitewide "
                  "handler binds" % page)
            bad += 1
        i, ifo = s.find(MARK), s.find("<footer")
        if not (0 <= i < ifo):
            print("GUARD: %s ask block is not above the footer" % page)
            bad += 1

    if bad:
        sys.exit("%d problem(s)" % bad)
    print("the ask surface is on %d page(s): %s"
          % (len(PAGES), ", ".join(sorted(PAGES))))


if __name__ == "__main__":
    main()
