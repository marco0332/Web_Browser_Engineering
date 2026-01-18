import tkinter as tk

from URL import URL
from Util import lex

WIDTH, HEIGHT = 800, 600

class Browser:
    def __init__(self):
        self.window = tk.Tk()
        self.canvas = tk.Canvas(
            self.window,
            width=WIDTH,
            height=HEIGHT,
        )
        self.canvas.pack()

    def load(self, url):
        body = url.request()
        text = lex(body)

        HSTEP, VSTEP = 13, 18
        cursor_x, cursor_y = HSTEP, VSTEP
        
        for c in text:
            self.canvas.create_text(cursor_x, cursor_y, text=c)
            cursor_x += HSTEP
            if cursor_x >= WIDTH - HSTEP:
                cursor_y += VSTEP
                cursor_x = HSTEP

if __name__ == "__main__":
    import sys
    Browser().load(URL(sys.argv[1]))
    tk.mainloop()
