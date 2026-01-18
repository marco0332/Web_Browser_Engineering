WIDTH, HEIGHT = 800, 600
HSTEP, VSTEP = 13, 18

def lex(body):
    text = ""
    in_tag = False
    for c in body:
        if c =="<":
            in_tag = True
        elif c == ">":
            in_tag = False
        elif not in_tag:
            text += c
    return text
    
def load(url):
    body = url.request()
    lex(body)

def layout(text):
        display_list = []
        cursor_x, cursor_y = HSTEP, VSTEP

        for c in text:
            # Practice 2-1
            if c == "\n":
                cursor_y += VSTEP
                cursor_x = HSTEP
                continue

            display_list.append((cursor_x, cursor_y, c))
            cursor_x += HSTEP
            if cursor_x >= WIDTH - HSTEP:
                cursor_y += VSTEP
                cursor_x = HSTEP
        return display_list