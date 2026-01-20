from Text import Text
from Tag import Tag

def lex(body):
    out = []
    buffer = ""
    in_tag = False
    for c in body:
        if c =="<":
            in_tag = True
            if buffer: out.append(Text(buffer))
            buffer = ""
        elif c == ">":
            in_tag = False
            out.append(Tag(buffer))
            buffer = ""
        elif not in_tag:
            buffer += c
    if not in_tag and buffer:
        out.append(Text(buffer))
    return out
    
def load(url):
    body = url.request()
    lex(body)