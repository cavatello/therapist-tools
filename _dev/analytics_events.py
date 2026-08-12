#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Send GA4 events for every email signup and contact message on the site.

WHY A DELEGATED LISTENER RATHER THAN onsubmit= ATTRIBUTES. There are six forms
across the site and they are emitted by four different builders. Anything
written into the markup has to be written four times and will be missed the
fifth time a form is added. One listener on `document`, added by one pass, is
the version that keeps working.

WHAT IS MEASURED, AND WHY IT IS TWO EVENTS AND NOT ONE.

  newsletter_submit / contact_submit   fired when the reader presses the button.
  newsletter_signup / contact_sent     fired only when the POST actually
                                       succeeded.

These are different numbers and the gap between them is the interesting one: it
is the failure rate of the form. A single "signup" event fired on click reports
a healthy conversion rate for a form that is silently 502-ing, which is exactly
the failure you most want the analytics to surface.

Success is detected by watching for the confirmation node the existing handler
inserts (.nlok). That handler already posts in the background rather than
letting the browser navigate to Formspree's dead-end thank-you page, so there is
no unload race here and no need for `transport_type: 'beacon'` gymnastics -
the page is still alive when the event goes out.

`generate_lead` is ALSO fired on a confirmed signup. It is one of GA4's
recommended events, which means it appears in the standard reports and in
Google Ads conversion setup without anyone having to register a custom
definition first. The custom names are for readable reports; the recommended
name is for the tooling.

WHAT IS NOT COLLECTED. Not the email address, and not anything typed into a
calculator. What goes to Google is: which form, where it sat on the page,
whether the optional consent box was ticked, and whether it worked.

Idempotent, and guarded.

Run after analytics.py, which is what puts gtag on the page in the first place.
"""
import os, re, sys

HERE = os.path.dirname(os.path.abspath(__file__))
SITE = os.path.dirname(HERE)
SUBDIRS = ("money", "licensure", "getting-paid", "practice", "training", "for")

MARK = "/* _dev/analytics_events.py */"

JS = """<script>%s
(function(){
  if (typeof window === 'undefined') return;
  // gtag may not have loaded yet, or may be blocked. Queue into dataLayer the
  // way the snippet itself does, so a blocked loader costs the event and not
  // the page.
  function send(name, params){
    try {
      window.dataLayer = window.dataLayer || [];
      if (typeof window.gtag === 'function') { window.gtag('event', name, params); }
      else { window.dataLayer.push(['event', name, params]); }
    } catch (e) {}
  }

  // Where on the page the form sat. Two signup forms on one page are the same
  // event with different placements, and the placement is the thing worth
  // knowing: a footer form and a hero form convert nothing like each other.
  function place(form){
    if (form.classList.contains('hero')) return 'hero';
    var s = form.closest('footer, .sitefoot, .lnews, .nlband, section, main');
    if (!s) return 'unknown';
    if (s.tagName === 'FOOTER' || s.classList.contains('sitefoot')) return 'footer';
    return s.id || (s.className || '').split(/\\s+/)[0] || 'body';
  }

  function kindOf(form){
    return form.dataset.kind === 'contact' ? 'contact' : 'newsletter';
  }

  function base(form){
    var c = form.querySelector('input[type=checkbox][name=consent]');
    return {
      form_location: place(form),
      form_id: form.className || 'form',
      consent_given: c ? !!c.checked : null,
      page_path: location.pathname
    };
  }

  document.addEventListener('submit', function(e){
    var f = e.target;
    if (!f || f.tagName !== 'FORM') return;
    if (!f.querySelector('input[type=email]')) return;
    var kind = kindOf(f);
    f.dataset.tsSent = '1';
    send(kind === 'contact' ? 'contact_submit' : 'newsletter_submit', base(f));
  }, true);

  // The confirmation the page's own handler writes on a successful POST. Only
  // this fires the conversion.
  function confirmed(node){
    var f = node.closest ? node.closest('form') : null;
    if (!f) {
      // The handler replaces the form with the notice on some templates, so
      // fall back to the nearest form-ish ancestor's own dataset.
      f = node.parentElement && node.parentElement.querySelector
          ? node.parentElement.querySelector('form') : null;
    }
    var kind = f ? kindOf(f) : 'newsletter';
    var p = f ? base(f) : {form_location: 'unknown', page_path: location.pathname};
    if (kind === 'contact') { send('contact_sent', p); return; }
    send('newsletter_signup', p);
    send('generate_lead', p);   // GA4's own recommended name, for the standard reports
  }

  new MutationObserver(function(muts){
    muts.forEach(function(m){
      Array.prototype.forEach.call(m.addedNodes || [], function(n){
        if (n.nodeType !== 1) return;
        if (n.classList && n.classList.contains('nlok')) confirmed(n);
        else if (n.querySelector) {
          var hit = n.querySelector('.nlok');
          if (hit) confirmed(hit);
        }
      });
    });
  }).observe(document.documentElement, {childList: true, subtree: true});
})();
</script>""" % MARK


def pages():
    out = [f for f in sorted(os.listdir(SITE)) if f.endswith(".html")]
    for d in SUBDIRS:
        p = os.path.join(SITE, d)
        if os.path.isdir(p):
            out += ["%s/%s" % (d, f) for f in sorted(os.listdir(p))
                    if f.endswith(".html")]
    return [f for f in out if os.path.basename(f) not in
            ("tycoon.html", "concepts.html")]


def main():
    n = 0
    for rel in pages():
        p = os.path.join(SITE, rel)
        s = open(p, encoding="utf-8").read()
        orig = s
        s = re.sub(r"\n?<script>" + re.escape(MARK) + r"[\s\S]*?</script>\n?", "", s)
        i = s.lower().rfind("</body>")
        if i < 0:
            print("no </body>: %s" % rel)
            continue
        s = s[:i] + JS + "\n" + s[i:]
        if s != orig:
            open(p, "w", encoding="utf-8").write(s)
            n += 1
    print("%d page(s) carry the event listener" % n)

    bad = 0
    for rel in pages():
        s = open(os.path.join(SITE, rel), encoding="utf-8").read()
        if s.count(MARK) != 1:
            print("GUARD %s: %d copies" % (rel, s.count(MARK)))
            bad += 1
        if "gtag/js?id=" not in s:
            print("GUARD %s: events but no gtag - run analytics.py first" % rel)
            bad += 1
    if bad:
        sys.exit("\n%d problem(s)" % bad)
    print("guards clean")


if __name__ == "__main__":
    main()
