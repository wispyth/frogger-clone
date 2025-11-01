import cv2
import numpy as np
import time
import random

# =========================
# КОНФИГУРАЦИИ
# =========================

# Параметры сетки
CELL_SIZE = 40  # 1 клетка = 40x40 пикселей
GRID_COLS = 17
GRID_ROWS = 12

# Параметры окна
WINDOW_WIDTH    = GRID_COLS * CELL_SIZE # 17 * 40 = 680
WINDOW_HEIGHT   = GRID_ROWS * CELL_SIZE # 12 * 40 = 480
WINDOW_TITLE    = "Frogger"

# Скорость обновления кадров
TARGET_FPS      = 60
FRAME_DELAY_MS  = int(1000 / TARGET_FPS)

# Цвета фона
GRID_COLOR      = (50, 50, 50)
FINISH_COLOR    = (190, 15, 150)
WATER_COLOR     = (255, 0, 0)
ROAD_COLOR      = (60, 60, 60)
START_COLOR     = (0, 120, 0)

# Параметры для машин
ROAD_LANES = [
    {"row": 5, "dir": -1, "speed": 140},
    {"row": 6, "dir": +1, "speed": 190},
    {"row": 7, "dir": -1, "speed": 220},
    {"row": 8, "dir": +1, "speed": 160},
]
CAR_SIZES = [
    {"size": 1, "prob": 0.40},
    {"size": 2, "prob": 0.40},
    {"size": 3, "prob": 0.20}
]
CAR_COLORS = [
    (70, 50, 200),  # красный
    (50, 210, 240), # жёлтый
    (230, 120, 60), # синий
    (120, 200, 80), # зелёный
    (40, 140, 255), # оранжевый
    (200, 80, 170), # фиолетовый
]

# =========================
# ВСПОМОГАТЕЛЬНЫЕ ФУНКЦИИ
# =========================

def clamp(num, min, max):
    if num < min:
        num = min
    if num > max:
        num = max

    return num

def spawn_car(lanes):
    lane = random.choice(lanes)

    a = random.random()
    b = 0.0
    size = 0
    for item in CAR_SIZES:
        b += item["prob"]
        if a <= b:
            size = item["size"]
            break

    color = random.choice(CAR_COLORS)

    if lane["dir"] == +1:
        x = -size * CELL_SIZE
    else:
        x = WINDOW_WIDTH

    return {
        "x": x,
        "row": lane["row"],
        "dir": lane["dir"],
        "speed": lane["speed"],
        "size": size,
        "color": color,
    }

# =========================
# ФУНКЦИИ РИСОВАНИЯ
# =========================

# Сетка поверх кадра
def draw_grid(frame, cell_size, color):
    h, w, _ = frame.shape

    for x in range(0, w, cell_size):
        cv2.line(frame, (x, 0), (x, h), color, 1)

    for y in range(0, h, cell_size):
        cv2.line(frame, (0, y), (w, y), color, 1)

# Раскраска фона:
# - 0-й ряд: зона финиша
# - 1-4 ряды: вода
# - 5-8 ряды: дорога
# - 9-11 ряды: стартовая зона
def draw_background(frame):
    frame[:] = (10, 10, 10)

    def row_to_y(row):
        return row * CELL_SIZE

    y_finish_start = row_to_y(0)
    y_finish_end = row_to_y(1)
    cv2.rectangle(frame, (0, y_finish_start), (WINDOW_WIDTH, y_finish_end), FINISH_COLOR, -1)

    y_water_start = row_to_y(1)
    y_water_end = row_to_y(5)
    cv2.rectangle(frame, (0, y_water_start), (WINDOW_WIDTH, y_water_end), WATER_COLOR, -1)

    y_road_start = row_to_y(5)
    y_road_end = row_to_y(9)
    cv2.rectangle(frame, (0, y_road_start), (WINDOW_WIDTH, y_road_end), ROAD_COLOR, -1)

    y_start_start = row_to_y(9)
    y_start_end = row_to_y(12)
    cv2.rectangle(frame, (0, y_start_start), (WINDOW_WIDTH, y_start_end), START_COLOR, -1)

# Элементы интерфейса
def draw_ui(frame):
    cv2.putText(frame,
                "Frogger",
                (10, WINDOW_HEIGHT - 15),
                cv2.FONT_HERSHEY_COMPLEX,
                0.6,
                (255, 255, 255),
                1,
                cv2.LINE_AA)

    cv2.putText(frame,
                "Press ESC or Q to quit",
                (10, 0 * CELL_SIZE + 25),
                cv2.FONT_HERSHEY_COMPLEX,
                0.6,
                (255, 255, 255),
                1,
                cv2.LINE_AA)

# Лягушка
def draw_frog(frame, frog_col, frog_row):
    x_start = frog_col * CELL_SIZE + 4
    y_start = frog_row * CELL_SIZE + 4
    x_end = (frog_col + 1) * CELL_SIZE - 4
    y_end = (frog_row + 1) * CELL_SIZE - 4
    
    cv2.rectangle(frame, (x_start, y_start), (x_end, y_end), (0, 255, 0), -1)

# Машины
def draw_cars(frame, cars, dt):
    alive = []

    for car in cars:
        car["x"] += car["dir"] * car["speed"] * dt

        x_start = int(car["x"] + 4)
        y_start = int(car["row"] * CELL_SIZE + 4)
        x_end = int(car["x"] + car["size"] * CELL_SIZE - 4)
        y_end = int((car["row"] + 1) * CELL_SIZE - 4)

        cv2.rectangle(frame, (x_start, y_start), (x_end, y_end), car["color"], -1)

        if car["dir"] == +1:
            if x_start < WINDOW_WIDTH:
                alive.append(car)
        else:
            if x_end > 0:
                alive.append(car)

    cars[:] = alive

def main():
    # создаём окно
    cv2.namedWindow(WINDOW_TITLE, cv2.WINDOW_NORMAL)
    cv2.resizeWindow(WINDOW_TITLE, WINDOW_WIDTH, WINDOW_HEIGHT)

    # координаты лягушки в сетке
    frog_col = GRID_COLS // 2
    frog_row = GRID_ROWS - 2

    last_time = time.time()

    # создание машин
    lanes = ROAD_LANES
    cars = []
    spawn_interval = 1.2
    next_spawn_time = last_time + spawn_interval

    while True:
        current_time = time.time()
        dt = current_time - last_time
        last_time = current_time

        # периодический спавн машин
        if current_time >= next_spawn_time:
            cars.append(spawn_car(lanes))
            spawn_interval = random.uniform(0.7, 1.5)
            next_spawn_time = current_time + spawn_interval

        # создаём пустой кадр
        frame = np.zeros((WINDOW_HEIGHT, WINDOW_WIDTH, 3), dtype=np.uint8)

        # рисуем фон
        draw_background(frame)

        # рисуем сетку
        draw_grid(frame, cell_size=CELL_SIZE, color=GRID_COLOR)

        # рисуем лягушку
        draw_frog(frame, frog_col, frog_row)

        # рисуем машины
        draw_cars(frame, cars, dt)

        # рисуем UI
        draw_ui(frame)

        # показываем
        cv2.imshow(WINDOW_TITLE, frame)

        # обработка клавиатуры
        key = cv2.waitKey(FRAME_DELAY_MS) & 0xFF
        if key == 27 or key == ord('q'):    # ESC или q
            break
        elif key in (ord('w'), 82): # W или стрелка вверх
            frog_row -= 1
        elif key in (ord('a'), 81): # A или стрелка влево
            frog_col -= 1
        elif key in (ord('s'), 84): # S или стрелка вниз
            frog_row += 1
        elif key in (ord('d'), 83): # D или стрелка вправо
            frog_col += 1
        elif key == ord('r'):
            # вернуться в начальную точку
            frog_col = GRID_COLS // 2
            frog_row = GRID_ROWS - 2

        # проверка на выход за границы для лягушки
        frog_col = clamp(frog_col, 0, GRID_COLS - 1)
        frog_row = clamp(frog_row, 0, GRID_ROWS - 1)

    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()
