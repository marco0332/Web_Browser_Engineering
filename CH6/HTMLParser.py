from Element import Element
from Text import Text


SELF_CLOSING_TAGS = [
    "area", "base", "br", "col", "embed", "hr", "img", "input",
    "link", "meta", "param", "source", "track", "wbr",
]


class HTMLParser:
    HEAD_TAGS = [
        "base", "basefont", "bgsound", "noscript",
        "link", "meta", "title", "style", "script"
    ]
    def __init__(self, body):
        self.body = body
        self.unfinished = []
        self.in_script = False
    
    def get_attributes(self, text):
        parts = text.split()
        tag = parts[0].casefold()
        attributes = {}
        for attrpair in parts[1:]:
            if "=" in attrpair:
                key, value = attrpair.split("=", 1)
                if len(value) > 2 and value[0] in ["'", "\""]:
                    value = value[1:-1]
                attributes[key.casefold()] = value
            else:
                attributes[attrpair.casefold()] = ""
        return tag, attributes
    
    def add_text(self, text):
        if text.isspace(): return
        self.implicit_tags(None)
        parent = self.unfinished[-1]
        node = Text(text, parent)
        parent.children.append(node)
    
    def add_tag(self, tag):
        tag, attributes = self.get_attributes(tag)
        if tag.startswith("!"): return
        self.implicit_tags(tag)
        
        if tag.startswith("/"):
            if tag == "/script":
                self.in_script = False
            if len(self.unfinished) == 1: return
            node = self.unfinished.pop()
            parent = self.unfinished[-1]
            parent.children.append(node)
        elif tag in SELF_CLOSING_TAGS:
            parent = self.unfinished[-1]
            node = Element(tag, attributes, parent)
            parent.children.append(node)
        else:
            # Practice 4-3
            if tag == "script":
                self.in_script = True
            # Practice 4-2
            if tag in ["p", "li"] and self.unfinished:
                if self.unfinished[-1].tag == tag:
                    node = self.unfinished.pop()
                    parent = self.unfinished[-1] if self.unfinished else None
                    if parent:
                        parent.children.append(node)

            parent = self.unfinished[-1] if self.unfinished else None
            node = Element(tag, attributes, parent)
            self.unfinished.append(node)
    
    def finish(self):
        if not self.unfinished:
            self.implicit_tags(None)
        while len(self.unfinished) > 1:
            node = self.unfinished.pop()
            parent = self.unfinished[-1]
            parent.children.append(node)
        return self.unfinished.pop()
    
    def parse(self):
        text = ""
        in_tag = False
        for i, c in enumerate(self.body):
            # <script> 내부에서는 </script> 태그 특별 처리
            if self.in_script and not in_tag:
                if c == "<":
                    remaining = self.body[i:]
                    if remaining.lower().startswith("</script"):
                        # 다음 문자가 허용된 문자인지 확인
                        if len(remaining) > len("</script"):
                            next_char = remaining[len("</script")]
                            if next_char in [' ', '\t', '\v', '\r', '/', '>']:
                                # </script> 태그로 처리
                                if text:
                                    self.add_text(text)
                                    text = ""
                                # > 까지 찾기
                                tag_end = remaining.find('>', len("</script"))
                                if tag_end != -1:
                                    tag_content = remaining[1:tag_end]
                                    self.add_tag(tag_content)
                                    continue
                    text += c
                else:
                    text += c
                continue

            if c == "<":
                in_tag = True
                if text: self.add_text(text)
                text = ""
            elif c == ">":
                in_tag = False
                self.add_tag(text)
                text = ""
            else:
                text += c
        if not in_tag and text:
            self.add_text(text)
        return self.finish()
    
    def implicit_tags(self, tag):
        while True:
            open_tags = [node.tag for node in self.unfinished]
            if open_tags == [] and tag != "html":
                self.add_tag("html")
            elif open_tags == ["html"] \
                and tag not in ["head", "body", "/html"]:
                if tag in self.HEAD_TAGS:
                    self.add_tag("head")
                else:
                    self.add_tag("body")
            elif open_tags == ["html", "head"] and \
                tag not in ["/head"] + self.HEAD_TAGS:
                self.add_tag("/head")
            else:
                break