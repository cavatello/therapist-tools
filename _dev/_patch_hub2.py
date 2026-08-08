import io, sys

p = sys.argv[1]
s = io.open(p, encoding="utf-8").read()

a = '''        calc = ""
        tool = next((p for p in mine if p.get("format") == "calculator"), None)
        if tool:'''
b = '''        # THE CALCULATOR CTA, AND WHEN IT IS SUPPRESSED
        #
        # Our World in Data puts a chart-and-explore step after the insights so
        # a reader who has just met a claim can immediately test it. That is
        # the right instinct here too - except that four of these five hubs
        # already open their reading with a grid of tool cards, and the first
        # card in that grid is the same calculator. Rendered as written, the
        # page showed the identical destination twice, twenty pixels apart, in
        # two different card styles.
        #
        # So the CTA renders only where it adds a step rather than repeating
        # one: when the hub's own tools grid does not already link to it. A
        # concept implemented literally into a page that already solved half of
        # it is not fidelity, it is duplication.
        calc = ""
        tool = next((p for p in mine if p.get("format") == "calculator"), None)
        if tool and ('href="../%s"' % tool["file"]) in s:
            tool = None
        if tool:'''
assert a in s, "calc"
s = s.replace(a, b, 1)

io.open(p, "w", encoding="utf-8").write(s)
print("patched")
