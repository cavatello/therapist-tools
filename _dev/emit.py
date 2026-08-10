"""JSON in, Python source out.

`json.dumps` was the first attempt and it produced `null` where the file needed
`None`. The file still parsed - `null` is a valid Python NAME - so `ast.parse`
said yes and the import said NameError. Syntax checking is not type checking
and it is certainly not evaluation.
"""
def emit(v, ind=0, width=76):
    pad = " " * ind
    if v is None:
        return "None"
    if v is True:
        return "True"
    if v is False:
        return "False"
    if isinstance(v, str):
        return pystr(v, ind, width)
    if isinstance(v, (int, float)):
        return repr(v)
    if isinstance(v, list):
        if not v:
            return "[]"
        inner = ",\n".join(pad + "    " + emit(x, ind + 4, width) for x in v)
        return "[\n" + inner + ",\n" + pad + "]"
    if isinstance(v, dict):
        if not v:
            return "{}"
        inner = ",\n".join(pad + "    " + pystr(k, ind + 4, width) + ": "
                           + emit(x, ind + 4, width) for k, x in v.items())
        return "{\n" + inner + ",\n" + pad + "}"
    raise TypeError(type(v))


def pystr(s, ind, width):
    """One implicitly-concatenated string per line, wrapped to the width."""
    room = max(28, width - ind - 2)
    if len(s) + 2 <= room:
        return _q(s)
    out, line = [], ""
    for w in s.split(" "):
        if line and len(line) + 1 + len(w) > room:
            out.append(line + " ")
            line = w
        else:
            line = (line + " " + w) if line else w
    if line:
        out.append(line)
    pad = " " * (ind + 4)
    return ("\n" + pad).join(_q(x) for x in out)


def _q(s):
    return '"' + s.replace("\\", "\\\\").replace('"', '\\"') + '"'
