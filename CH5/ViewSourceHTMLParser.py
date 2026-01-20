from HTMLParser import HTMLParser
from Element import Element
from Text import Text

# Practice 4-5
class ViewSourceHTMLParser(HTMLParser):
    def __init__(self, body):
        super().__init__(body)
        self.root = Element("pre", {}, None)
        self.unfinished = [self.root]
        self.in_script = False
    
    def implicit_tags(self, tag):
        return
    
    def finish(self):
        return self.root
    
    def add_tag(self, tag_text):
        folded = tag_text.split()[0].casefold() if tag_text.strip() else ""

        if folded == "script":
            self.in_script = True
        if folded == "/script":
            self.in_script = False

        parent = self.unfinished[-1]
        parent.children.append(Text("<" + tag_text + ">", parent))
    
    def add_text(self, text):
        parent = self.unfinished[-1]

        lines = text.split("\n")
        for i, line in enumerate(lines):
            if i > 0:
                parent.children.append(Element("br", {}, parent))  # 줄바꿈 유지(레이아웃이 br 처리함)

            if line != "":
                b = Element("b", {}, parent)
                b.children.append(Text(line, b))
                parent.children.append(b)