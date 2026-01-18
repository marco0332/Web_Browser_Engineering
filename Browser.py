import tkinter as tk

from URL import URL
from Util import lex, layout, WIDTH, HEIGHT, HSTEP, VSTEP
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
        text = lex(body)
        self.display_list = layout(text)
        self.draw()
    
    def draw(self):
        self.canvas.delete("all")
        for x, y, c in self.display_list:
            if y > self.scroll + HEIGHT: continue
            if y + VSTEP < self.scroll: continue
            self.canvas.create_text(x, y - self.scroll, text=c)

if __name__ == "__main__":
    import sys
    Browser().load(URL(sys.argv[1]))
    tk.mainloop()
