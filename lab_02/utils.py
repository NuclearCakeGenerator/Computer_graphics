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
        self.dots: set[Dot] = set()
        self.update_dots()

    def update_dots(self):
        self.dots.clear()
        for segment in self.segments:
            self.dots.add(segment.first_dot)
            self.dots.add(segment.second_dot)


_RAW_INITIAL_CONTENT = Content([
    Segment(Dot(611.2476439651997, 491.92429638485453), Dot(746.0613920740224, 475.0064927006101)),
    Segment(Dot(746.0613920740224, 475.0064927006101), Dot(833.8224986860403, 498.26847276644617)),
    Segment(Dot(833.8224986860403, 498.26847276644617), Dot(843.8674446235603, 550.0792465494446)),
    Segment(Dot(843.8674446235603, 550.0792465494446), Dot(808.9744745248063, 634.6682649706667)),
    Segment(Dot(808.9744745248063, 634.6682649706667), Dot(820.6054645577243, 675.9054114510125)),
    Segment(Dot(820.6054645577243, 675.9054114510125), Dot(772.4954603306543, 718.1999206616234)),
    Segment(Dot(772.4954603306543, 718.1999206616234), Dot(737.6024902319001, 718.1999206616234)),
    Segment(Dot(737.6024902319001, 718.1999206616234), Dot(741.3032597878287, 703.3968424379096)),
    Segment(Dot(741.3032597878287, 703.3968424379096), Dot(757.1637007418077, 699.1673915168485)),
    Segment(Dot(757.1637007418077, 699.1673915168485), Dot(779.3683180773785, 674.3193673556145)),
    Segment(Dot(779.3683180773785, 674.3193673556145), Dot(726.5001815641148, 596.0745253159841)),
    Segment(Dot(726.5001815641148, 596.0745253159841), Dot(746.0613920740224, 475.0064927006101)),
    Segment(Dot(611.2476439651997, 491.92429638485453), Dot(592.2151148204248, 591.3163930297904)),
    Segment(Dot(592.2151148204248, 591.3163930297904), Dot(452.11455306027574, 716.6138765662256)),
    Segment(Dot(452.11455306027574, 716.6138765662256), Dot(414.0494947707258, 716.6138765662256)),
    Segment(Dot(414.0494947707258, 716.6138765662256), Dot(418.27894569178693, 701.282116977379)),
    Segment(Dot(418.27894569178693, 701.282116977379), Dot(436.7827934714293, 694.9379405957874)),
    Segment(Dot(436.7827934714293, 694.9379405957874), Dot(495.99510636628463, 625.1520003982793)),
    Segment(Dot(495.99510636628463, 625.1520003982793), Dot(494.9377436360194, 587.6156234738619)),
    Segment(Dot(494.9377436360194, 587.6156234738619), Dot(547.2771987841505, 492.45297774998716)),
    Segment(Dot(547.2771987841505, 492.45297774998716), Dot(611.2476439651997, 491.92429638485453)),
    Segment(Dot(574.8724135110327, 606.8266579744164), Dot(736.7609482795776, 611.2604600548693)),
    Segment(Dot(630.7909799768897, 608.358155289447), Dot(648.784020889617, 716.6138765662256)),
    Segment(Dot(648.784020889617, 716.6138765662256), Dot(606.489511679006, 716.0851952010929)),
    Segment(Dot(606.489511679006, 716.0851952010929), Dot(611.7763253303324, 700.7534356122464)),
    Segment(Dot(611.7763253303324, 700.7534356122464), Dot(622.8786339981177, 699.1673915168485)),
    Segment(Dot(622.8786339981177, 699.1673915168485), Dot(586.9143795607911, 607.1564632580364)),
    Segment(Dot(778.9435373358831, 483.7222420471274), Dot(857.0844787518763, 432.1833021248665)),
    Segment(Dot(857.0844787518763, 432.1833021248665), Dot(878.2317333571818, 356.58186691089924)),
    Segment(Dot(878.2317333571818, 356.58186691089924), Dot(921.0549239329255, 315.3447204305535)),
    Segment(Dot(921.0549239329255, 315.3447204305535), Dot(951.1897617454858, 306.35713722329865)),
    Segment(Dot(951.1897617454858, 306.35713722329865), Dot(915.6765773615278, 358.4223478812243)),
    Segment(Dot(915.6765773615278, 358.4223478812243), Dot(896.7355811368242, 447.51506171371295)),
    Segment(Dot(896.7355811368242, 447.51506171371295), Dot(833.8224986860403, 498.26847276644617)),
    Segment(Dot(833.8224986860403, 498.26847276644617), Dot(867.1294246893965, 582.3288098225355)),
    Segment(Dot(867.1294246893965, 582.3288098225355), Dot(902.5510761532831, 601.8598586169296)),
    Segment(Dot(902.5510761532831, 601.8598586169296), Dot(932.1572326007108, 667.9751909740229)),
    Segment(Dot(932.1572326007108, 667.9751909740229), Dot(921.0549239329255, 704.9828865333075)),
    Segment(Dot(921.0549239329255, 704.9828865333075), Dot(907.3092084394768, 695.4666219609201)),
    Segment(Dot(907.3092084394768, 695.4666219609201), Dot(908.3665711697422, 682.2495878326041)),
    Segment(Dot(908.3665711697422, 682.2495878326041), Dot(882.4611842782429, 641.0124413522583)),
    Segment(Dot(882.4611842782429, 641.0124413522583), Dot(812.1870132994211, 626.8802921837215)),
    Segment(Dot(543.1880563332516, 499.887782206167), Dot(465.86026855372427, 494.56770321051766)),
    Segment(Dot(465.86026855372427, 494.56770321051766), Dot(418.8076270569195, 466.01890949335524)),
    Segment(Dot(418.8076270569195, 466.01890949335524), Dot(435.19674937603133, 506.72737460856837)),
    Segment(Dot(435.19674937603133, 506.72737460856837), Dot(465.86026855372427, 494.56770321051766)),
    Segment(Dot(429.69485678907836, 493.0613833442015), Dot(407.17663702400154, 518.887046006619)),
    Segment(Dot(407.17663702400154, 518.887046006619), Dot(412.46345067532786, 551.1366092797099)),
    Segment(Dot(412.46345067532786, 551.1366092797099), Dot(405.5905929286036, 568.583094329087)),
    Segment(Dot(405.5905929286036, 568.583094329087), Dot(425.6804848036438, 580.7427657271377)),
    Segment(Dot(425.6804848036438, 580.7427657271377), Dot(482.2493908728361, 569.6404570593522)),
    Segment(Dot(482.2493908728361, 569.6404570593522), Dot(500.75323865247844, 574.398589345546)),
])


def fit_to_square(content: Content, size=450.0):
    xs = [p.x for seg in content.segments for p in (seg.first_dot, seg.second_dot)]
    ys = [p.y for seg in content.segments for p in (seg.first_dot, seg.second_dot)]

    min_x, max_x = min(xs), max(xs)
    min_y, max_y = min(ys), max(ys)

    cx = (min_x + max_x) / 2.0
    cy = (min_y + max_y) / 2.0

    scale = size / max(max_x - min_x, max_y - min_y)

    return Content([
        Segment(
            Dot((seg.first_dot.x - cx) * scale, (seg.first_dot.y - cy) * scale),
            Dot((seg.second_dot.x - cx) * scale, (seg.second_dot.y - cy) * scale),
        )
        for seg in content.segments
    ])


INITIAL_CONTENT = fit_to_square(_RAW_INITIAL_CONTENT)


def show_content(content: Content, center: Dot, plot_func, photo_image, canvas):
    content.update_dots()
    photo_image.put("#000000", to=(0, 0, CANVAS_WIDTH, CANVAS_HEIGHT))
    canvas.delete("all")
    canvas.create_image(0, 0, image=photo_image, anchor="nw")

    for segment in content.segments:
        draw_segment(segment, plot_func, color="#FFFFFF")

    for dot in content.dots:
        draw_dot(dot, plot_func, color="#FFFFFF")

    if center is not None:
        draw_dot(center, plot_func, color="#FF0000")


# Internal functions below

def draw_dot(dot, plot_func, color="#FFFFFF"):
    cx, cy = convert_to_canvas_navigation(dot.x, dot.y, camera_config)
    padding_x = 5
    padding_y = -5
    for dx in range(-1, 2):
        for dy in range(-1, 2):
            plot_func(cx + dx, cy + dy, color=color)

    # label_text = f"({round(dot.x, 2)}, {round(dot.y, 2)})"
    # plot_func(cx + padding_x, cy + padding_y, color=color, text=label_text)


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

    x2 = int(round(x1))
    y2 = int(round(CANVAS_HEIGHT - y1))

    return x2, y2
