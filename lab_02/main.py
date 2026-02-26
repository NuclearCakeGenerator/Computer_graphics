import tkinter as tk
from tkinter import ttk, messagebox
from itertools import combinations
import copy

from utils import show_content
from utils import CANVAS_WIDTH, CANVAS_HEIGHT, Content, INITIAL_CONTENT

LEFT_PANEL_WIDTH = 300

current_content: Content | None = copy.deepcopy(INITIAL_CONTENT)
last_content: Content | None = None

root = tk.Tk()
root.title("Computer Graphics Lab 1")

main_container = tk.Frame(root)
main_container.pack(fill="both", expand=True)

# Multiline Entry
left_frame = tk.Frame(main_container, width=LEFT_PANEL_WIDTH, padx=10, pady=10)
left_frame.pack(side="left", fill="y")
left_frame.pack_propagate(False)
tk.Label(left_frame, text="Raw Dot Input:").pack(anchor="w")
text_entry = tk.Text(left_frame, wrap="none")
text_entry.pack(fill="both", expand=True, pady=(0, 10))
parse_button = tk.Button(left_frame, text="Parse Dots", cursor="hand2", background="#2bff00")
parse_button.pack(fill="x", side="bottom")

# 3. RIGHT COLUMN: Random Text + Canvas
right_frame = tk.Frame(main_container, padx=10, pady=10)
right_frame.pack(side="left", fill="both", expand=True)
# Single-line field for random text (Result output )
tk.Label(right_frame, text="Status/Result:").pack(anchor="w")
info_field = tk.Entry(right_frame)
info_field.insert(0, "Enter your dots first")
info_field.pack(fill="x", pady=(0, 10))

canvas = tk.Canvas(right_frame, width=CANVAS_WIDTH, height=CANVAS_HEIGHT, background="#000000")
canvas.pack(fill="both", expand=True)
img = tk.PhotoImage(width=CANVAS_WIDTH, height=CANVAS_HEIGHT)
canvas.create_image((0, 0), image=img, anchor="nw")


def put_pixel(x, y, color="#FFFFFF", text: str = ""):
    if 0 <= x < CANVAS_WIDTH and 0 <= y < CANVAS_HEIGHT:
        if not text:
            img.put(color, (x, y))
        else:
            canvas.create_text(
                x,
                y,
                text=text,
                fill=color,
                anchor="sw"
            )


show_content(current_content, put_pixel, img, canvas)

root.mainloop()
