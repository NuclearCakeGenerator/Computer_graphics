import tkinter as tk
from tkinter import messagebox
import copy
import math

from utils import show_content
from utils import CANVAS_WIDTH, CANVAS_HEIGHT, Content, INITIAL_CONTENT, Dot

LEFT_PANEL_WIDTH = 300

current_content: Content | None = copy.deepcopy(INITIAL_CONTENT)
last_content: Content | None = None
transformation_center: Dot | None = None


def show_content_wrapper():
    if last_content is not None:
        btn_undo.config(state="normal", bg="#00ff00")
    else:
        btn_undo.config(state="disabled", bg="#f0f0f0")

    show_content(current_content, transformation_center, put_pixel, img, canvas)


transform_job = None


def handle_center_update(*args):
    global transform_job
    if transform_job:
        main_container.after_cancel(transform_job)

    transform_job = main_container.after(300, update_center)


def move_picture():
    try:
        dx = float(entry_dx.get())
        dy = float(entry_dy.get())

        global last_content
        last_content = copy.deepcopy(current_content)
        for segment in current_content.segments:
            segment.first_dot.x += dx
            segment.second_dot.x += dx
            segment.first_dot.y += dy
            segment.second_dot.y += dy

        show_content_wrapper()


    except ValueError:
        messagebox.showerror(
            "Input Error",
            "Please enter valid numeric values for ΔX and ΔY."
        )


def scale_picture():
    global last_content
    global current_content
    try:
        cx = float(entry_cx.get())
        cy = float(entry_cy.get())
    except ValueError:
        messagebox.showerror(
            "Input Error",
            "Please enter valid numeric values for X and Y for center of transformation."
        )
        return
    current_content.transformation_center = Dot(cx, cy)
    # show_content(current_content, put_pixel, img, canvas)

    try:
        scale_factor = float(entry_scale.get())
    except ValueError:
        messagebox.showerror(
            "Input Error",
            "Please enter valid float value for scale."
        )
        return

    last_content = copy.deepcopy(current_content)
    for segment in current_content.segments:
        segment.first_dot.x = (
                                      segment.first_dot.x - current_content.transformation_center.x) * scale_factor + transformation_center.x
        segment.second_dot.x = (
                                       segment.second_dot.x - current_content.transformation_center.x) * scale_factor + transformation_center.x
        segment.first_dot.y = (
                                      segment.first_dot.y - current_content.transformation_center.y) * scale_factor + transformation_center.y
        segment.second_dot.y = (
                                       segment.second_dot.y - current_content.transformation_center.y) * scale_factor + transformation_center.y

        show_content_wrapper()


def update_center():
    try:
        cx = float(entry_cx.get())
        cy = float(entry_cy.get())
        global transformation_center
        transformation_center = Dot(cx, cy)

        show_content_wrapper()
    except ValueError:
        pass


def handle_rotate():
    def rotate_dot(p: Dot) -> Dot:
        pivot = transformation_center
        theta = math.radians(degrees)

        cos_theta = math.cos(theta)
        sin_theta = math.sin(theta)

        temp_x = p.x - pivot.x
        temp_y = p.y - pivot.y

        new_x = temp_x * cos_theta - temp_y * sin_theta
        new_y = temp_x * sin_theta + temp_y * cos_theta

        return Dot(new_x + pivot.x, new_y + pivot.y)

    try:
        cx = float(entry_cx.get())
        cy = float(entry_cy.get())
    except ValueError:
        messagebox.showerror(
            "Input Error",
            "Please enter valid numeric values for X and Y for center of transformation."
        )
        return
    global transformation_center
    transformation_center = Dot(cx, cy)

    try:
        degrees = float(entry_rotate.get())
    except ValueError:
        messagebox.showerror("Input Error", "Invalid rotation value")

    global last_content
    last_content = copy.deepcopy(current_content)
    for segment in current_content.segments:
        segment.first_dot = rotate_dot(segment.first_dot)
        segment.second_dot = rotate_dot(segment.second_dot)

        show_content_wrapper()


root = tk.Tk()
root.title("Computer Graphics Lab 2")
center_x = tk.StringVar()
center_y = tk.StringVar()
center_x.trace_add("write", handle_center_update)
center_y.trace_add("write", handle_center_update)

main_container = tk.Frame(root)
main_container.pack(fill="both", expand=True)

# --- Control Panel Setup ---
left_frame = tk.Frame(main_container, width=LEFT_PANEL_WIDTH, padx=10, pady=10, relief="ridge", borderwidth=1)
left_frame.pack(side="left", fill="y")
left_frame.pack_propagate(False)

# 1. Linear Transformation Frame (Move)
linear_transformation_frame = tk.Frame(left_frame, padx=10, pady=10)
linear_transformation_frame.pack(side="top", fill="x")

# Delta X and Delta Y Row
move_inputs = tk.Frame(linear_transformation_frame)
move_inputs.pack(pady=5)

tk.Label(move_inputs, text="Δ X").grid(row=0, column=0, padx=5)
tk.Label(move_inputs, text="Δ Y").grid(row=0, column=1, padx=5)

entry_dx = tk.Entry(move_inputs, width=8)
entry_dx.grid(row=1, column=0, padx=5)
entry_dy = tk.Entry(move_inputs, width=8)
entry_dy.grid(row=1, column=1, padx=5)

# Move Button
btn_move = tk.Button(linear_transformation_frame, text="move", width=20, command=move_picture)
btn_move.pack(pady=10)

# Separator line
tk.Frame(left_frame, height=2, bd=1, relief="sunken").pack(fill="x", pady=10)

# 2. Relative Transformation Frame (Rotate/Scale)
relative_transformation_frame = tk.Frame(left_frame, padx=10, pady=10)
relative_transformation_frame.pack(side="top", fill="x")

tk.Label(relative_transformation_frame, text="centers:", font=("Arial", 10, "bold")).pack()

# Center X and Center Y Row
center_inputs = tk.Frame(relative_transformation_frame)
center_inputs.pack(pady=5)

tk.Label(center_inputs, text="X").grid(row=0, column=0)
tk.Label(center_inputs, text="Y").grid(row=0, column=1)

entry_cx = tk.Entry(center_inputs, width=8, textvariable=center_x)
entry_cx.grid(row=1, column=0, padx=5)
entry_cy = tk.Entry(center_inputs, width=8, textvariable=center_y)
entry_cy.grid(row=1, column=1, padx=5)

# Rotate and Scale Inputs Row
transform_inputs = tk.Frame(relative_transformation_frame)
transform_inputs.pack(pady=10)

tk.Label(transform_inputs, text="rotate°").grid(row=0, column=0)
tk.Label(transform_inputs, text="scale:").grid(row=0, column=1)

entry_rotate = tk.Entry(transform_inputs, width=8)
entry_rotate.grid(row=1, column=0, padx=5)
entry_scale = tk.Entry(transform_inputs, width=8)
entry_scale.grid(row=1, column=1, padx=5)

# Rotate and Scale Buttons Row
button_row = tk.Frame(relative_transformation_frame)
button_row.pack(fill="x")

btn_rotate = tk.Button(button_row, text="rotate", width=10, command=handle_rotate)
btn_rotate.pack(side="left", expand=True, padx=2)

btn_scale = tk.Button(button_row, text="scale", width=10, command=scale_picture)
btn_scale.pack(side="left", expand=True, padx=2)

tk.Frame(left_frame, height=2, bd=1, relief="sunken").pack(fill="x", pady=10)

btn_undo = tk.Button(
    left_frame,
    text="Undo",
    width=20,
    height=2,
    bg="#00ff00"
)
btn_undo.pack(side="bottom", pady=10)

# Canvas
right_frame = tk.Frame(main_container, padx=10, pady=10)
right_frame.pack(side="left", fill="both", expand=True)
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


show_content_wrapper()

root.mainloop()
