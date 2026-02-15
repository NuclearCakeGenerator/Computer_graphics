CANVAS_WIDTH, CANVAS_HEIGHT, CANVAS_INTERNAL_PADDING = 1100, 1000, 30

camera_config = {
    'max_x': 310,
    'min_x': -5,
    'max_y': 60,
    'min_y': 50,
}


def draw_line(d1: Dot, d2: Dot, plot_func, color="#FFFFFF"):
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


def draw_triangle(d1: Dot, d2: Dot, d3: Dot, plot_func, color="#FFFFFF"):
    def plot_with_color(x, y):
        plot_func(x, y, color=color)

    draw_line(d1, d2, plot_with_color)
    draw_line(d2, d3, plot_with_color)
    draw_line(d3, d1, plot_with_color)


# Internal functions below


def convert_to_canvas_navigation(x0, y0, config):
    x1 = x0 - config['min_x']
    y1 = y0 - config['min_y']

    canvas_drawable_area = (CANVAS_WIDTH - 2 * CANVAS_INTERNAL_PADDING,
                            CANVAS_HEIGHT - 2 * CANVAS_INTERNAL_PADDING)
    area_width = config['max_x'] - config['min_x']
    area_height = config['max_y'] - config['min_y']

    scale = min(canvas_drawable_area[1] / area_height, canvas_drawable_area[0] / area_width)

    canvas_center = (CANVAS_WIDTH / 2, CANVAS_HEIGHT / 2)
    area_center = ((config['max_x'] - config['min_x']) / 2, (config['max_y'] - config['min_y']) / 2)

    x2 = scale * (x1 - area_center[0]) + canvas_center[0]
    y2 = scale * (y1 - area_center[1]) + canvas_center[1]

    x3 = round(x2)
    y3 = round(CANVAS_HEIGHT - y2)

    return x3, y3


class Dot:
    def __init__(self, x, y):
        self.x = x
        self.y = y
