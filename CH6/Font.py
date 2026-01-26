import tkinter as tk
import tkinter.font as tk_font

FONTS = {}

def get_font(size, weight, style):
    key = (size, weight, style)
    if key not in FONTS:
        font = tk_font.Font(
            size=size,
            weight=weight,
            slant=style
        )
        label = tk.Label(font=font)
        FONTS[key] = (font, label)
    return FONTS[key][0]