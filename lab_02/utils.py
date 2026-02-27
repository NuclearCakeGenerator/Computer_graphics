CANVAS_WIDTH = 900
CANVAS_HEIGHT = 900

camera_config = {
    'max_x': 450,
    'min_x': -450,
    'max_y': 450,
    'min_y': -450,
}


class Dot:
    def __init__(self, x: float, y: float):
        self.x = x
        self.y = y


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


class Segment:
    def __init__(self, first_dot: Dot, second_dot: Dot):
        self.first_dot = first_dot
        self.second_dot = second_dot


class Content:
    def __init__(self, segments: list[Segment], target: Dot | None = Dot(0, 0)):
        self.segments: list[Segment] = segments
        self.common_dots: set[Dot] = set()
        self.update_dots()
        self.transformation_center: Dot | None = target

    def update_dots(self):
        for segment in self.segments:
            self.common_dots.add(segment.first_dot)
            self.common_dots.add(segment.second_dot)


INITIAL_CONTENT = Content([
    Segment(Dot(50, -100), Dot(100, 0)),
    Segment(Dot(100, 0), Dot(0, 100)),
    Segment(Dot(0, 100), Dot(-100, 0)),
    Segment(Dot(-100, 0), Dot(-50, -100)),
    Segment(Dot(-50, -100), Dot(50, -100)),

    Segment(Dot(20, 50), Dot(130, 50)),
    Segment(Dot(130, 50), Dot(130, 150)),
    Segment(Dot(130, 150), Dot(20, 150)),
    Segment(Dot(20, 150), Dot(20, 50)),

    Segment(Dot(-50, 50), Dot(-150, 50)),
    Segment(Dot(-150, 50), Dot(-100, -150)),
    Segment(Dot(-100, -150), Dot(-50, 50)),
])


def show_content(content: Content, plot_func, photo_image, canvas):
    photo_image.put("#000000", to=(0, 0, CANVAS_WIDTH, CANVAS_HEIGHT))
    canvas.delete("all")
    canvas.create_image(0, 0, image=photo_image, anchor="nw")

    for segment in content.segments:
        draw_segment(segment, plot_func, color="#FFFFFF")

    for dot in content.common_dots:
        draw_dot(dot, plot_func, color="#FFFFFF")

    if content.transformation_center is not None:
        draw_dot(content.transformation_center, plot_func, color="#FF0000")


# Internal functions below

def draw_dot(dot, plot_func, color="#FFFFFF"):
    cx, cy = convert_to_canvas_navigation(dot.x, dot.y, camera_config)
    padding_x = 5
    padding_y = -5
    for dx in range(-1, 2):
        for dy in range(-1, 2):
            plot_func(cx + dx, cy + dy, color=color)

    label_text = f"({dot.x}, {dot.y})"
    plot_func(cx + padding_x, cy + padding_y, color=color, text=label_text)


def draw_segment(segment: Segment, plot_func, color="#FFFFFF"):
    x0, y0 = convert_to_canvas_navigation(segment.first_dot.x, segment.first_dot.y, camera_config)
    x1, y1 = convert_to_canvas_navigation(segment.second_dot.x, segment.second_dot.y, camera_config)

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
    draw_segment(Segment(tri.a, tri.b), plot_func, color=color)
    draw_segment(Segment(tri.b, tri.c), plot_func, color=color)
    draw_segment(Segment(tri.c, tri.a), plot_func, color=color)


def convert_to_canvas_navigation(x0, y0, config):
    x1 = x0 - config['min_x']
    y1 = y0 - config['min_y']

    x2 = round(x1)
    y2 = round(CANVAS_HEIGHT - y1)

    return x2, y2
