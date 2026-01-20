import tkinter as tk

from Util import paint_tree
from DocumentLayout import DocumentLayout, WIDTH, HEIGHT, HSTEP, VSTEP
from HTMLParser import HTMLParser
from ViewSourceHTMLParser import ViewSourceHTMLParser
from URL import URL
from BrowerEvent import BrowerEvent

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
