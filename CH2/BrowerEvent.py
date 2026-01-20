from Util import HEIGHT, VSTEP

SCROLL_STEP = 100

class BrowerEvent:
    def __init__(self, browser):
        self.browser = browser
        self.browser.window.bind("<Down>", self.scrolldown)
        self.browser.window.bind("<Up>", self.scrollup)
        # Windows, macOS: MouseWheel 이벤트
        self.browser.canvas.bind("<MouseWheel>", self.on_mousewheel)
        # Linux (구버전 Tk): Button-4, Button-5
        self.browser.canvas.bind("<Button-4>", self.on_mousewheel)
        self.browser.canvas.bind("<Button-5>", self.on_mousewheel)
    
    def scrolldown(self, e):
        if hasattr(self.browser, 'display_list') and self.browser.display_list:
            max_y = max(y for _, y, _ in self.browser.display_list)
            scroll_limit = max(max_y + VSTEP - HEIGHT, 0)
            self.browser.scroll = min(self.browser.scroll + SCROLL_STEP, scroll_limit)
        else:
            self.browser.scroll += SCROLL_STEP
        self.browser.draw()
    
    # Practice 2-2
    def scrollup(self, e):
        self.browser.scroll = max(self.browser.scroll - SCROLL_STEP, 0)
        self.browser.draw()
    
    def on_mousewheel(self, e):
        # Windows/macOS: delta 속성 사용
        if hasattr(e, 'delta') and e.delta:
            if e.delta > 0:
                self.scrollup(e)
            else:
                self.scrolldown(e)
        # Linux: num 속성 사용 (4=위로, 5=아래로)
        elif hasattr(e, 'num'):
            if e.num == 4:
                self.scrollup(e)
            elif e.num == 5:
                self.scrolldown(e)