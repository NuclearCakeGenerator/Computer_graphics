import tkinter as tk
from tkinter import ttk
from utils import CANVAS_WIDTH, CANVAS_HEIGHT, draw_triangle, draw_line, Dot

LEFT_PANEL_WIDTH = 300
MIDDLE_PANEL_WIDTH = 400

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
text_entry.pack(fill="both", expand=True)

# Table (Number, X, Y)
middle_frame = tk.Frame(main_container, width=MIDDLE_PANEL_WIDTH, padx=10, pady=10)
middle_frame.pack(side="left", fill="y")
middle_frame.pack_propagate(False)
tk.Label(middle_frame, text="Parsed Dots:").pack(anchor="w")
columns = ("number", "x", "y")
tree = ttk.Treeview(middle_frame, columns=columns, show="headings")

tree.heading("number", text="№")
tree.heading("x", text="Coordinate X")
tree.heading("y", text="Coordinate Y")

# Adjust column widths
tree.column("number", width=50, anchor="center")
tree.column("x", width=100, anchor="center")
tree.column("y", width=100, anchor="center")

tree.pack(fill="both", expand=True)

# 3. RIGHT COLUMN: Random Text + Canvas
right_frame = tk.Frame(main_container, padx=10, pady=10)
right_frame.pack(side="left", fill="both", expand=True)

# Single-line field for random text (Result output )
tk.Label(right_frame, text="Status/Result:").pack(anchor="w")
info_field = tk.Entry(right_frame)
info_field.insert(0, "Random text or result output here...")
info_field.pack(fill="x", pady=(0, 10))

# Your existing Canvas setup
canvas = tk.Canvas(right_frame, width=CANVAS_WIDTH, height=CANVAS_HEIGHT, background="#000000")
canvas.pack(fill="both", expand=True)

img = tk.PhotoImage(width=CANVAS_WIDTH, height=CANVAS_HEIGHT)
canvas.create_image((0, 0), image=img, anchor="nw")

def put_pixel(x, y, color="#FFFFFF"):
    if 0 <= x < CANVAS_WIDTH and 0 <= y < CANVAS_HEIGHT:
        img.put(color, (x, y))

draw_line(Dot(50, 50), Dot(100, 150), put_pixel)

root.mainloop()
