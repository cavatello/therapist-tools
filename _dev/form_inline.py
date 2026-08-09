#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Answer the form on the page, instead of handing the reader to Formspree.

THE REPORT

  "can the footer email just reply with confirmation and results within the
   page? I don't like it going to formspring, looks bad"

Right now both forms on this site - the signup band that sits above the footer
on all 158 pages, and the contact form - are plain `method="post"` forms
pointed at formspree.io. Submitting one navigates the browser away from this
site to a Formspree-branded confirmation page carrying somebody else's logo,
and the reader has to press Back to return. For a site whose whole argument is
that it is a careful, self-contained reference, that hand-off is the least
careful thing on it.

WHAT CHANGES

The form posts by `fetch` with `Accept: application/json`, which is Formspree's
documented AJAX mode, and the answer is rendered in place. Nothing navigates.

WHAT DOES NOT CHANGE, AND WHY THAT MATTERS

  - **The form still works with JavaScript off.** The only thing the script
    does is call `preventDefault` inside a submit handler. No handler, no
    preventDefault, and the browser posts the form the old way and lands on
    Formspree - which is worse, and still works. Progressive enhancement is
    the right shape here because the alternative is a contact form that
    silently does nothing.
  - **No value goes anywhere except Formspree.** This site's printed promise
    is that nothing you type is sent anywhere, and `_dev/tool_analytics.py`
    carries a guard that fails the build if the tracking script can read a
    field. That promise is about the calculators, and a contact form the
    reader deliberately submits is the one exception - but the exception stops
    at Formspree. The script fires no analytics event carrying any field, and
    the guard below checks for it.
  - **The address stays visible.** If the request fails - offline, blocked,
    Formspree down - the error state shows the real mailto address rather than
    swallowing the message. A form that eats what somebody wrote is worse than
    no form.

FAILURE STATES, WHICH ARE MOST OF THE WORK

  sending    the button is disabled and says so, because a form with no
             feedback gets double-submitted
  sent       the form is replaced by a confirmation naming what happens next
  failed     an error, the original text still in the box, and the address

Idempotent, guarded.
"""
import os, re, sys

HERE = os.path.dirname(os.path.abspath(__file__))
SITE = os.path.dirname(HERE)
MARK = "/* _dev/form_inline.py */"
JSMARK = "// _dev/form_inline.py"
EMAIL = "shawn@shawnwalters.com"

CSS = """<style>%(mark)s
/* The answer, rendered where the form was. Same box language as everything
   else on the site: 2px ink, a solid offset shadow, never a blur. */
.fi-ok{border:2px solid #16211B;border-radius:12px;background:#FBF9F3;
  box-shadow:5px 5px 0 #2C6350;padding:18px 20px;margin:0}
.fi-ok b{display:block;font-family:'Bricolage Grotesque',system-ui,sans-serif;
  font-weight:800;letter-spacing:-.028em;font-size:19px;color:#16211B;
  margin:0 0 6px}
.fi-ok p{font-size:14.6px;line-height:1.65;color:#635E53;margin:0;max-width:62ch}
.fi-ok p a{color:#2C6350}
.fi-err{border:2px solid #B5483F;border-radius:12px;background:#FBF9F3;
  padding:13px 16px;margin:12px 0 0}
.fi-err p{font-size:14px;line-height:1.6;color:#8A3730;margin:0;max-width:62ch}
.fi-err a{color:#8A3730;font-weight:600}
.fi-busy{opacity:.6;cursor:progress}
</style>"""

# form kind -> (heading, what happens next)
SAID = {
    "contact": ("Sent.",
                "It comes straight to a person, not a queue. If you left an "
                "email address you will get a reply; if you did not, that is "
                "fine too and the note still gets read."),
    "signup": ("You&rsquo;re on the list.",
               "About monthly. One click to leave, and the address is never "
               "sold or shared."),
}

JS = """<script>%(jsmark)s
(function(){
  // Progressive enhancement, deliberately. If this script never runs, the
  // form is an ordinary POST and still reaches Formspree - the reader just
  // gets the off-site page they were getting before instead of an in-page
  // answer. Nothing here is load-bearing for the message arriving.
  var forms = document.querySelectorAll('form[action*="formspree.io"]');
  if(!forms.length) return;
  Array.prototype.forEach.call(forms, function(f){
    if(f.getAttribute('data-fi')) return;
    f.setAttribute('data-fi','1');
    var kind = f.className.indexOf('nlform') > -1 ? 'signup' : 'contact';
    f.addEventListener('submit', function(ev){
      ev.preventDefault();
      var btn = f.querySelector('button[type=submit],button');
      var was = btn ? btn.textContent : '';
      if(btn){ btn.disabled = true; btn.textContent = 'Sending\\u2026'; }
      f.classList.add('fi-busy');
      var old = f.querySelector('.fi-err');
      if(old) old.parentNode.removeChild(old);

      fetch(f.action, {
        method: 'POST',
        body: new FormData(f),
        headers: {'Accept': 'application/json'}
      }).then(function(r){
        if(!r.ok) throw new Error(r.status);
        var box = document.createElement('div');
        box.className = 'fi-ok';
        box.setAttribute('role','status');
        box.setAttribute('aria-live','polite');
        box.innerHTML = '<b>' + SAID[kind][0] + '</b><p>' + SAID[kind][1] + '</p>';
        f.parentNode.replaceChild(box, f);
        if(box.scrollIntoView) box.scrollIntoView({block:'nearest'});
      }).catch(function(){
        // Never swallow what somebody wrote. The text stays in the box and
        // the real address is shown, because a form that eats a message is
        // worse than no form.
        f.classList.remove('fi-busy');
        if(btn){ btn.disabled = false; btn.textContent = was; }
        var e = document.createElement('div');
        e.className = 'fi-err';
        e.setAttribute('role','alert');
        e.innerHTML = '<p>That did not send \\u2014 your message is still in ' +
          'the box above. Try again, or email it to <a href="mailto:%(email)s">' +
          '%(email)s</a>.</p>';
        f.appendChild(e);
      });
    });
  });
})();
</script>"""


def js():
    said = "  var SAID = {%s};\n" % ", ".join(
        "%s:['%s','%s']" % (k, v[0].replace("'", "\\'"),
                            v[1].replace("'", "\\'"))
        for k, v in sorted(SAID.items()))
    body = JS % {"jsmark": JSMARK, "email": EMAIL}
    # SAID has to be in scope inside the IIFE, so it goes after the opening
    return body.replace("(function(){\n", "(function(){\n" + said, 1)


def main():
    css = CSS % {"mark": MARK}
    script = js()

    print("forms answered on the page instead of on formspree.io:")
    n = 0
    withforms = 0
    for rel in sorted(os.listdir(SITE)):
        if not rel.endswith(".html"):
            continue
        p = os.path.join(SITE, rel)
        s = open(p, encoding="utf-8").read()
        if "sitenav" not in s:
            continue
        orig = s
        s = re.sub(r"\n?<style>" + re.escape(MARK) + r"[\s\S]*?</style>\n?", "", s)
        s = re.sub(r"\n?<script>" + re.escape(JSMARK) + r"[\s\S]*?</script>\n?",
                   "", s)
        e = s.lower().rfind("</body>")
        if e < 0:
            print("  MISSING  %s has no </body>" % rel)
            continue
        s = s[:e] + css + "\n" + script + "\n" + s[e:]
        if "formspree.io" in s:
            withforms += 1
        if s != orig:
            open(p, "w", encoding="utf-8").write(s)
        n += 1

    print("  %d page(s) carry the handler, %d of them have a form"
          % (n, withforms))

    # --------------------------------------------------------------- guards
    bad = 0
    for rel in sorted(os.listdir(SITE)):
        if not rel.endswith(".html"):
            continue
        s = open(os.path.join(SITE, rel), encoding="utf-8").read()
        if "sitenav" not in s:
            continue
        if s.count(MARK) != 1 or s.count(JSMARK) != 1:
            print("GUARD %s: %d stylesheet(s), %d script(s)"
                  % (rel, s.count(MARK), s.count(JSMARK)))
            bad += 1

        # Every Formspree form must still be a real POST form, so that a
        # reader with JavaScript off still reaches a working endpoint.
        for m in re.finditer(r"<form[^>]*formspree\.io[^>]*>", s):
            tag = m.group(0)
            if 'method="post"' not in tag.lower():
                print("GUARD %s: a formspree form lost its method=post, so it "
                      "does nothing without JavaScript" % rel)
                bad += 1

    # The privacy line. This site's promise is that nothing typed into it is
    # reported anywhere; a contact form the reader submits on purpose is the
    # one exception, and the exception has to stop at Formspree. If this
    # script ever grows an analytics call carrying a field, the build fails.
    body = re.search(r"<script>" + re.escape(JSMARK) + r"([\s\S]*?)</script>",
                     open(os.path.join(SITE, "contact.html"),
                          encoding="utf-8").read())
    if not body:
        print("GUARD: the handler is not on contact.html")
        bad += 1
    else:
        code = body.group(1)
        for pat, why in (
            (r"\bgtag\b", "calls gtag"),
            (r"\bdataLayer\b", "writes to dataLayer"),
            (r"\bclarity\b", "calls Clarity"),
            (r"location\.hash", "reads the URL hash"),
            (r"localStorage|sessionStorage", "writes to browser storage"),
        ):
            if re.search(pat, code):
                print("GUARD: the form handler %s. A form's contents go to "
                      "Formspree and nowhere else." % why)
                bad += 1
        # It must send to the form's own action, not to anything else.
        urls = re.findall(r"fetch\(([^,]+),", code)
        if urls != ["f.action"]:
            print("GUARD: the handler fetches %r, expected the form's own "
                  "action" % urls)
            bad += 1

    if bad:
        sys.exit("\n%d problem(s)" % bad)
    print("guards clean - every form still posts without JavaScript, and the "
          "handler sends to the form's own action and reports nothing to "
          "anyone else")


if __name__ == "__main__":
    main()
