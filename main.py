import tkinter as tk

from utils import WIDTH, HEIGHT, Dot, draw_line, draw_triangle

root = tk.Tk()
canvas = tk.Canvas(root, width=WIDTH, height=HEIGHT, background="#000000")
canvas.pack()

img = tk.PhotoImage(width=WIDTH, height=HEIGHT)
canvas.create_image((0, 0), image=img, anchor="nw")


def put_pixel(x, y, color="#FFFFFF"):
    if 0 <= x < WIDTH and 0 <= y < HEIGHT:
        img.put(color, (x, y))


draw_line(Dot(50, 50), Dot(300, 60), put_pixel)

dot_a = Dot(150, -60)
dot_b = Dot(50, 58)
dot_c = Dot(250, 59)

draw_triangle(dot_a, dot_b, dot_c, put_pixel, color="#00FF00")

root.mainloop()
