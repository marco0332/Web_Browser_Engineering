import tkinter as tk

from Util import paint_tree, style, tree_to_list, cascade_priority
from DocumentLayout import DocumentLayout, WIDTH, HEIGHT, HSTEP, VSTEP
from HTMLParser import HTMLParser
from ViewSourceHTMLParser import ViewSourceHTMLParser
from URL import URL
from BrowerEvent import BrowerEvent
from CSSParser import DEFAULT_STYLE_SHEET, CSSParser
from Element import Element

class Browser:
    def __init__(self):
        self.window = tk.Tk()
        self.canvas = tk.Canvas(
            self.window,
            width=WIDTH,
            height=HEIGHT,
        )
        self.canvas.pack()
        self.scroll = 0
        self.event_handler = BrowerEvent(self)

    def load(self, url):
        body = url.request()
        parser = HTMLParser if not url.view_source else ViewSourceHTMLParser
        self.nodes = parser(body).parse()

        rules = DEFAULT_STYLE_SHEET
        links = [node.attributes["href"]
                for node in tree_to_list(self.nodes, [])
                if isinstance(node, Element)
                and node.tag == "link"
                and node.attributes.get("rel") == "stylesheet"
                and "href" in node.attributes]
        for link in links:
            style_url = url.resolve(link)
            try:
                body = style_url.request()
            except:
                continue
            rules.extend(CSSParser(body).parse())
        style(self.nodes, sorted(rules, key=cascade_priority))
        self.document = DocumentLayout(self.nodes)
        self.document.layout()
        self.event_handler.add_document(self.document)
        self.display_list = []
        paint_tree(self.document, self.display_list)
        self.draw()
    
    def draw(self):
        self.canvas.delete("all")
        for cmd in self.display_list:
            if cmd.top > self.scroll + HEIGHT: continue
            if cmd.bottom < self.scroll: continue
            cmd.execute(self.scroll, self.canvas)

if __name__ == "__main__":
    import sys
    Browser().load(URL(sys.argv[1]))
    tk.mainloop()
