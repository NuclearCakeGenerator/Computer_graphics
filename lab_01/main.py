import tkinter as tk
from tkinter import ttk, messagebox
from itertools import combinations

from lab_01.utils import show_content
from utils import CANVAS_WIDTH, CANVAS_HEIGHT, draw_triangle, Dot, Triangle, update_limits

parsed_dots = []
triangles = []


def handle_parse():
    # Clear the table for new input
    for item in tree.get_children():
        tree.delete(item)

    raw_text = text_entry.get("1.0", "end-1c")
    lines = raw_text.strip().split('\n')

    try:
        for i, line in enumerate(lines):
            if not line.strip():
                continue  # Skip empty lines

            # Split by comma and strip whitespace to handle "double spaces"
            parts = [p.strip() for p in line.split(',')]

            if len(parts) != 2:
                raise ValueError(f"Line {i + 1} must have exactly two coordinates: 'x, y'")

            # Convert to float (to allow decimal input) then to Dot objects
            x = float(parts[0])
            y = float(parts[1])

            dot = Dot(x, y, len(parsed_dots))
            parsed_dots.append(dot)

            # Display in table: (Number, X, Y)
            # Since duplicated dots are valid, we just append them all.
            tree.insert("", "end", values=(i + 1, dot.x, dot.y))

        info_field.delete(0, tk.END)
        info_field.insert(0, f"Successfully parsed {len(parsed_dots)} dots.")

        global triangles
        triangles = []
        show_content(parsed_dots, triangles, put_pixel, img, canvas)

        return

    except ValueError as e:
        # Requirement: Display message for incorrect data
        messagebox.showerror("Input Error", f"Invalid format on line {i + 1}.\nUse: x, y\nError: {e}")
        return


def solve_task():
    if len(parsed_dots) < 6:  # Need at least 4 dots for one triangle inside another
        messagebox.showinfo("Result", "Need at least 6 dots to find a solution.")
        return

    best_outer = None
    best_inner = None
    min_outer_area = float('inf')
    min_inner_area = float('inf')

    # 1. Generate all possible triangles (Full search)
    all_possible_triangles = []
    for combo in combinations(parsed_dots, 3):
        t = Triangle(*combo)
        if t.area > 1e-9:  # Ignore degenerate triangles
            all_possible_triangles.append(t)

    # 2. Compare pairs of triangles
    for t_outer in all_possible_triangles:
        if t_outer.area > min_outer_area:
            continue

        for t_inner in all_possible_triangles:
            if t_outer == t_inner:
                continue

            # Check if t_inner is strictly inside t_outer
            # All vertices of inner must be inside outer
            if (t_outer.is_dot_inside(t_inner.a) and
                    t_outer.is_dot_inside(t_inner.b) and
                    t_outer.is_dot_inside(t_inner.c)):

                # Check priority criteria
                if (t_outer.area < min_outer_area) or (
                        abs(t_outer.area - min_outer_area) < 1e-9 and t_inner.area < min_inner_area):
                    min_outer_area = t_outer.area
                    min_inner_area = t_inner.area
                    best_outer = t_outer
                    best_inner = t_inner

    if not best_outer or not best_inner:
        messagebox.showinfo("Result", "No solution found where one triangle is strictly inside another.")
        return

    global triangles
    triangles = [best_outer, best_inner]
    result_text = f"Outer Area: {min_outer_area:.2f}, Inner Area: {min_inner_area:.2f}"
    info_field.delete(0, tk.END)
    info_field.insert(0, result_text)

    show_content(parsed_dots, triangles, put_pixel, img, canvas)


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
text_entry.pack(fill="both", expand=True, pady=(0, 10))
parse_button = tk.Button(left_frame, text="Parse Dots", cursor="hand2", background="#2bff00", command=handle_parse)
parse_button.pack(fill="x", side="bottom")

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
tree.column("number", width=50, anchor="center")
tree.column("x", width=100, anchor="center")
tree.column("y", width=100, anchor="center")
tree.pack(fill="both", expand=True)
solve_button = tk.Button(middle_frame, text="Solve", cursor="hand2", background="#2bff00", command=solve_task)
solve_button.pack(fill="x", side="bottom")

# 3. RIGHT COLUMN: Random Text + Canvas
right_frame = tk.Frame(main_container, padx=10, pady=10)
right_frame.pack(side="left", fill="both", expand=True)
# Single-line field for random text (Result output )
tk.Label(right_frame, text="Status/Result:").pack(anchor="w")
info_field = tk.Entry(right_frame)
info_field.insert(0, "Random text or result output here...")
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


root.mainloop()
