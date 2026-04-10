import tkinter as tk
from dataclasses import dataclass
from tkinter import colorchooser, messagebox

WINDOW_WIDTH = 1300
WINDOW_HEIGHT = 900
LEFT_PANEL_WIDTH = 320
CANVAS_WIDTH = 920
CANVAS_HEIGHT = 860


@dataclass(frozen=True)
class Point:
    x: int
    y: int


class Lab05App:
    def __init__(self, root: tk.Tk):
        self.root = root
        self.root.title("Lab 05 - Заполнение со списком ребер и флагом")
        self.root.geometry(f"{WINDOW_WIDTH}x{WINDOW_HEIGHT}")

        self.fill_color = "#FF0000"

        self.contours: list[list[Point]] = []
        self.current_contour: list[Point] = []
        self.segment_ids: list[int] = []
        self.vertex_ids: list[int] = []

        self.in_step_mode = False
        self.step_index = 0
        self.step_plan: list[str] = []

        self._build_layout()
        self._bind_events()
        self._update_status("Кликайте по холсту для ввода вершин.")

    def _build_layout(self):
        self.container = tk.Frame(self.root)
        self.container.pack(fill="both", expand=True)

        self.left_frame = tk.Frame(
            self.container,
            width=LEFT_PANEL_WIDTH,
            padx=10,
            pady=10,
            relief="ridge",
            borderwidth=1,
        )
        self.left_frame.pack(side="left", fill="y")
        self.left_frame.pack_propagate(False)

        self.right_frame = tk.Frame(self.container, padx=10, pady=10)
        self.right_frame.pack(side="left", fill="both", expand=True)

        tk.Label(self.left_frame, text="Цвет заливки:").pack(anchor="w")

        self.color_row = tk.Frame(self.left_frame)
        self.color_row.pack(fill="x", pady=(4, 10))

        self.color_preview = tk.Label(
            self.color_row,
            text="      ",
            bg=self.fill_color,
            relief="sunken",
            borderwidth=1,
        )
        self.color_preview.pack(side="left")

        self.color_label = tk.Label(self.color_row, text=self.fill_color)
        self.color_label.pack(side="left", padx=8)

        self.btn_choose_color = tk.Button(
            self.left_frame,
            text="Выбрать цвет",
            command=self._choose_fill_color,
            cursor="hand2",
        )
        self.btn_choose_color.pack(fill="x", pady=(0, 12))

        self.hint_frame = tk.LabelFrame(
            self.left_frame,
            text="Подсказки",
            padx=8,
            pady=8,
        )
        self.hint_frame.pack(fill="x", pady=(0, 10))

        hints = [
            "ЛКМ: добавить вершину",
            "Shift + клик: горизонталь",
            "Ctrl + клик: вертикаль",
            "Shift + Ctrl: авто H/V",
            "Кнопка 'Замкнуть': закрыть контур",
        ]
        for line in hints:
            tk.Label(self.hint_frame, text=line, anchor="w").pack(fill="x")

        self.btn_close = tk.Button(
            self.left_frame,
            text="Замкнуть",
            command=self._close_current_contour,
            bg="#CBF2C6",
            cursor="hand2",
        )
        self.btn_close.pack(fill="x", pady=(0, 8))

        self.btn_fill = tk.Button(
            self.left_frame,
            text="Закрасить",
            command=self._fill_immediately,
            bg="#FFD8A8",
            cursor="hand2",
        )
        self.btn_fill.pack(fill="x", pady=(0, 8))

        self.btn_fill_step = tk.Button(
            self.left_frame,
            text="Закрасить по шагам",
            command=self._start_step_mode,
            bg="#FFD8A8",
            cursor="hand2",
        )
        self.btn_fill_step.pack(fill="x", pady=(0, 8))

        self.btn_clear = tk.Button(
            self.left_frame,
            text="Очистить",
            command=self._clear_canvas,
            bg="#FFCCCC",
            cursor="hand2",
        )
        self.btn_clear.pack(fill="x")

        self.step_frame = tk.LabelFrame(
            self.left_frame,
            text="Пошаговая заливка",
            padx=8,
            pady=8,
        )
        self.btn_next_step = tk.Button(
            self.step_frame,
            text="Дальше",
            command=self._next_step,
            cursor="hand2",
        )
        self.btn_exit_step = tk.Button(
            self.step_frame,
            text="Выход",
            command=self._exit_step_mode,
            cursor="hand2",
        )
        self.btn_next_step.pack(fill="x", pady=(0, 6))
        self.btn_exit_step.pack(fill="x")

        tk.Label(self.right_frame, text="Статус:").pack(anchor="w")
        self.status_var = tk.StringVar(value="")
        self.status_entry = tk.Entry(
            self.right_frame,
            textvariable=self.status_var,
            state="readonly",
            readonlybackground="#FFFFFF",
        )
        self.status_entry.pack(fill="x", pady=(0, 8))

        self.canvas = tk.Canvas(
            self.right_frame,
            width=CANVAS_WIDTH,
            height=CANVAS_HEIGHT,
            bg="#111111",
            highlightthickness=1,
            highlightbackground="#555555",
            cursor="crosshair",
        )
        self.canvas.pack(fill="both", expand=True)

    def _bind_events(self):
        self.canvas.bind("<Button-1>", self._on_canvas_click)

    def _update_status(self, text: str):
        self.status_var.set(text)

    def _choose_fill_color(self):
        color = colorchooser.askcolor(
            title="Выберите цвет заливки",
            color=self.fill_color,
        )[1]
        if not color:
            return
        self.fill_color = color.upper()
        self.color_preview.config(bg=self.fill_color)
        self.color_label.config(text=self.fill_color)
        self._update_status(f"Цвет заливки: {self.fill_color}")

    def _draw_vertex(self, p: Point):
        r = 3
        vertex_id = self.canvas.create_oval(
            p.x - r,
            p.y - r,
            p.x + r,
            p.y + r,
            fill="#F5F5F5",
            outline="#F5F5F5",
        )
        self.vertex_ids.append(vertex_id)

    def _draw_segment(self, p1: Point, p2: Point):
        seg_id = self.canvas.create_line(
            p1.x,
            p1.y,
            p2.x,
            p2.y,
            fill="#FFFFFF",
            width=2,
        )
        self.segment_ids.append(seg_id)

    def _on_canvas_click(self, event: tk.Event):
        if self.in_step_mode:
            self._update_status(
                "Пошаговый режим активен. Нажмите 'Выход', "
                "чтобы редактировать контуры."
            )
            return

        if not (0 <= event.x < CANVAS_WIDTH and 0 <= event.y < CANVAS_HEIGHT):
            return

        new_point = Point(event.x, event.y)
        if self.current_contour:
            new_point = self._apply_snap(
                self.current_contour[-1],
                new_point,
                event.state,
            )
            self._draw_segment(self.current_contour[-1], new_point)

        self.current_contour.append(new_point)
        self._draw_vertex(new_point)
        self._update_status(
            f"Текущий контур: {len(self.current_contour)} вершин. "
            f"Замкнутых контуров: {len(self.contours)}."
        )

    def _apply_snap(self, previous: Point, current: Point, state: int) -> Point:
        shift_pressed = bool(state & 0x0001)
        ctrl_pressed = bool(state & 0x0004)

        if shift_pressed and ctrl_pressed:
            if abs(current.x - previous.x) >= abs(current.y - previous.y):
                return Point(current.x, previous.y)
            return Point(previous.x, current.y)

        if shift_pressed:
            return Point(current.x, previous.y)

        if ctrl_pressed:
            return Point(previous.x, current.y)

        return current

    def _close_current_contour(self):
        if self.in_step_mode:
            self._update_status("Нельзя замкнуть контур в пошаговом режиме.")
            return

        if len(self.current_contour) < 3:
            messagebox.showwarning(
                "Недостаточно вершин",
                "Нужно минимум 3 вершины для замыкания контура.",
            )
            return

        first_point = self.current_contour[0]
        last_point = self.current_contour[-1]
        self._draw_segment(last_point, first_point)

        self.contours.append(self.current_contour.copy())
        self.current_contour.clear()

        self._update_status(
            f"Контур замкнут. Всего замкнутых контуров: {len(self.contours)}."
        )

    def _all_closed_contours(self) -> list[list[Point]]:
        return self.contours.copy()

    def _fill_immediately(self):
        if self.current_contour:
            messagebox.showwarning(
                "Контур не замкнут",
                "Сначала замкните текущий контур кнопкой 'Замкнуть'.",
            )
            return

        contours = self._all_closed_contours()
        if not contours:
            messagebox.showwarning(
                "Нет данных",
                "Сначала задайте хотя бы один замкнутый контур.",
            )
            return

        # Здесь будет вызов алгоритма заполнения со списком ребер и флагом.
        self._update_status(
            "UI готов: нажата 'Закрасить'. Алгоритм еще не подключен (заглушка)."
        )

    def _build_step_plan(self):
        self.step_plan = [
            "Шаг 1: сформировать список ребер по всем замкнутым контурам.",
            "Шаг 2: найти диапазон строк сканирования (min_y..max_y).",
            "Шаг 3: для текущей строки найти пересечения с активными ребрами.",
            "Шаг 4: отсортировать X пересечений и переключать флаг inside/outside.",
            "Шаг 5: закрасить интервалы, где флаг inside = True.",
            "Шаг 6: перейти к следующей строке и повторить.",
        ]
        self.step_index = 0

    def _start_step_mode(self):
        if self.current_contour:
            messagebox.showwarning(
                "Контур не замкнут",
                "Сначала замкните текущий контур кнопкой 'Замкнуть'.",
            )
            return

        if not self.contours:
            messagebox.showwarning(
                "Нет данных",
                "Сначала задайте хотя бы один замкнутый контур.",
            )
            return

        self.in_step_mode = True
        self._set_edit_controls_state("disabled")
        self.step_frame.pack(fill="x", pady=(10, 0))
        self._build_step_plan()
        self._update_status("Пошаговый режим включен. Нажмите 'Дальше'.")

    def _next_step(self):
        if not self.in_step_mode:
            return

        if self.step_index >= len(self.step_plan):
            self._update_status("Пошаговая демонстрация завершена.")
            return

        self._update_status(self.step_plan[self.step_index])
        self.step_index += 1

    def _exit_step_mode(self):
        if not self.in_step_mode:
            return

        self.in_step_mode = False
        self.step_frame.pack_forget()
        self._set_edit_controls_state("normal")
        self._update_status(
            "Выход из пошагового режима. "
            "Можно продолжать ввод контуров."
        )

    def _set_edit_controls_state(self, state: str):
        self.btn_close.config(state=state)
        self.btn_fill.config(state=state)
        self.btn_fill_step.config(state=state)
        self.btn_clear.config(state=state)
        self.btn_choose_color.config(state=state)

    def _clear_canvas(self):
        if self.in_step_mode:
            self._exit_step_mode()

        self.canvas.delete("all")
        self.contours.clear()
        self.current_contour.clear()
        self.segment_ids.clear()
        self.vertex_ids.clear()
        self._update_status("Холст очищен. Начните ввод вершин заново.")


if __name__ == "__main__":
    root = tk.Tk()
    app = Lab05App(root)
    root.mainloop()
