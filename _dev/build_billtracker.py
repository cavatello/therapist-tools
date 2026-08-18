#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""RETIRED. The second build of the bill tracker, merged into build_bills.py.

WHAT HAPPENED

On 18 August 2026 two sessions built a tracker for AB 1598 and SB 903 at
the same time, neither aware of the other. `_dev/build_bills.py` landed
first, was wired into `ship.py` and shipped
`california-therapy-bills-2026.html`. This file was the second build, of
`california-therapist-bills-2026.html`, and was never wired in - so
nothing double-shipped, but a builder for a duplicate page sat in the
repository as a loaded gun.

The two were merged rather than one being thrown away, because each had
found things the other had not:

  taken from here into build_bills.py
    - the imam addition to the religious-counseling exemption, and the
      limit that matters more than the addition: it does not reach the
      diagnosis or treatment of mental illness
    - the employer-name disclosure for unlicensed registrants
    - SB 903's companion-chatbot advertising sentence, and its clause on
      sharing, selling, storing and training models on data obtained
      from psychotherapy, with the Confidentiality of Medical
      Information Act sitting over it
    - the correction that the introduced version of SB 903 is three
      amendments out of date and does not contain what the page says
    - the removal of both authors' names, which broke the site's
      standing no-personal-names rule
  already taken, before this merge
    - the freshness lock: a STATE constant that makes the builder refuse
      to run once its status blocks have expired. `build_bills.py`
      records the credit at its own STATE.
  kept from build_bills.py, which had them and this did not
    - the annual Law and Ethics exam retest being removed, the 750
      pre-degree hours, the thirty amended code sections, the $10,000
      per-violation penalty, the proposed chapter numbering, and the
      Board's own analyses as the source for all of it

The full text of what stood here is in the history, at the commit that
added it. It is left as a stub rather than deleted so that the merge is
visible from the tree and not only from a log nobody reads.

DO NOT WIRE THIS INTO ship.py. Two pages about the same two bills is the
one outcome the collision guard in build_bills.py exists to prevent.
"""
import sys

sys.exit("_dev/build_billtracker.py is retired - its research was merged "
         "into _dev/build_bills.py on 18 August 2026 and the page it "
         "built was never published. Edit build_bills.py instead.")
