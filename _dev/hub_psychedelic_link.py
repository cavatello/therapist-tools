#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""RETIRED. Superseded by the content registry.

This pass hand-inserted a question row for the psychedelic training hub into
resources.html, back when resources.html was a hand-maintained question index.
It is now generated from registry.json by library/build_library.py, along with
every other listing on the site, so a page appears in the index because it has a
registry record rather than because someone remembered to run a script for it.

Kept as a stub rather than deleted so that anyone following the sibling
hub_*_link.py pattern for a new page finds this note instead of copying a
technique that no longer applies. To add a page to the hub now: add a record to
registry.json and rebuild.
"""
import sys

print("hub_psychedelic_link: retired - the hub is generated from registry.json")
sys.exit(0)
