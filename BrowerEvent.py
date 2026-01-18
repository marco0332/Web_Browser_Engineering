SCROLL_STEP = 100

class BrowerEvent:
    def __init__(self, browser):
        self.browser = browser
        self.browser.window.bind("<Down>", self.scrolldown)
    
    def scrolldown(self, e):
        self.browser.scroll += SCROLL_STEP
        self.browser.draw()