CANVAS_WIDTH = 900
CANVAS_HEIGHT = 900
CANVAS_INTERNAL_PADDING = 60

camera_config = {
    'max_x': 450,
    'min_x': -450,
    'max_y': 450,
    'min_y': -450,
}


def show_content(dots, triangles, plot_func, photo_image, canvas):
    photo_image.put("#000000", to=(0, 0, CANVAS_WIDTH, CANVAS_HEIGHT))
    canvas.delete("all")
    canvas.create_image(0, 0, image=photo_image, anchor="nw")

    if not dots:
        return

    colors = ["#FF0000", "#00FF00"]  # Red for Outer, Green for Inner
    for i, tri in enumerate(triangles):
        color = colors[i] if i < len(colors) else "#FFFFFF"
        draw_triangle(tri, plot_func, color=color)

    for i, dot in enumerate(dots):
        draw_dot(dot, plot_func, color="#FFFFFF")


# Internal functions below

def draw_dot(dot, plot_func, color="#FFFFFF"):
    cx, cy = convert_to_canvas_navigation(dot.x, dot.y, camera_config)
    padding_x = 5
    padding_y = -5
    for dx in range(-1, 2):
        for dy in range(-1, 2):
            plot_func(cx + dx, cy + dy, color=color)

    label_text = f"{dot.index + 1}: ({dot.x}, {dot.y})"
    plot_func(cx + padding_x, cy + padding_y, color=color, text=label_text)


def draw_segment(d1: Dot, d2: Dot, plot_func, color="#FFFFFF"):
    x0, y0 = convert_to_canvas_navigation(d1.x, d1.y, camera_config)
    x1, y1 = convert_to_canvas_navigation(d2.x, d2.y, camera_config)

    dx = abs(x1 - x0)
    dy = abs(y1 - y0)
    sx = 1 if x0 < x1 else -1
    sy = 1 if y0 < y1 else -1
    err = dx - dy

    while True:
        plot_func(x0, y0, color=color)
        if x0 == x1 and y0 == y1:
            break

        e2 = 2 * err
        if e2 > -dy:
            err -= dy
            x0 += sx
        if e2 < dx:
            err += dx
            y0 += sy


def draw_triangle(tri: Triangle, plot_func, color="#FFFFFF"):
    draw_segment(tri.a, tri.b, plot_func, color=color)
    draw_segment(tri.b, tri.c, plot_func, color=color)
    draw_segment(tri.c, tri.a, plot_func, color=color)


def convert_to_canvas_navigation(x0, y0, config):
    x1 = x0 - config['min_x']
    y1 = y0 - config['min_y']

    canvas_drawable_area = (CANVAS_WIDTH - 2 * CANVAS_INTERNAL_PADDING,
                            CANVAS_HEIGHT - 2 * CANVAS_INTERNAL_PADDING)
    area_width = config['max_x'] - config['min_x']
    area_height = config['max_y'] - config['min_y']

    if area_width == 0:
        scale = canvas_drawable_area[1] / area_height
    elif area_height == 0:
        scale = canvas_drawable_area[0] / area_width
    else:
        scale = min(canvas_drawable_area[1] / area_height, canvas_drawable_area[0] / area_width)

    canvas_center = (CANVAS_WIDTH / 2, CANVAS_HEIGHT / 2)
    area_center = ((config['max_x'] - config['min_x']) / 2, (config['max_y'] - config['min_y']) / 2)

    x2 = scale * (x1 - area_center[0]) + canvas_center[0]
    y2 = scale * (y1 - area_center[1]) + canvas_center[1]

    x3 = round(x2)
    y3 = round(CANVAS_HEIGHT - y2)

    return x3, y3


class Dot:
    def __init__(self, x: float, y: float, index: int):
        self.x = x
        self.y = y
        self.index = index


class Triangle:
    def __init__(self, a: Dot, b: Dot, c: Dot):
        self.a = a
        self.b = b
        self.c = c
        self.area = self.calculate_area()

    def calculate_area(self):
        return 0.5 * abs(self.a.x * (self.b.y - self.c.y) +
                         self.b.x * (self.c.y - self.a.y) +
                         self.c.x * (self.a.y - self.b.y))

    def is_dot_inside(self, p: Dot):
        # A point is strictly inside if it's not a vertex and satisfies area logic
        if p in (self.a, self.b, self.c):
            return False

        area1 = Triangle(p, self.a, self.b).area
        area2 = Triangle(p, self.b, self.c).area
        area3 = Triangle(p, self.c, self.a).area

        # Using a small epsilon for float comparison
        return abs(self.area - (area1 + area2 + area3)) < 1e-9
