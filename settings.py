# === Параметры сетки ===
CELL_SIZE = 40
GRID_COLS = 17
GRID_ROWS = 12

# === Параметры окна ===
WINDOW_WIDTH = GRID_COLS * CELL_SIZE
WINDOW_HEIGHT = GRID_ROWS * CELL_SIZE
WINDOW_TITLE = "Frogger"

# === Скорость обновления кадров ===
TARGET_FPS = 30
FRAME_DELAY_MS = int(1000 / TARGET_FPS)

# === Цвета (в BGR) ===
BG_COLOR = (10, 10, 10)
GRID_COLOR = (50, 50, 50)
FINISH_COLOR = (190, 15, 150)
WATER_COLOR = (255, 0, 0)
ROAD_COLOR = (60, 60, 60)
START_COLOR = (0, 120, 0)

# === Зоны (включительно) ===
FINISH_ROWS = (0, 0)
WATER_ROWS = (1, 4)
ROAD_ROWS = (5, 8)
START_ROWS = (9, 11)

# === Параметры полос ===
# Дорога
ROAD_LANES = [
    {"row": 5, "dir": -1, "speed": 65},
    {"row": 6, "dir": +1, "speed": 90},
    {"row": 7, "dir": -1, "speed": 105},
    {"row": 8, "dir": +1, "speed": 80},
]
ROAD_TARGET_GAP_CELLS = 6.5

# Вода
WATER_LANES = [
    {"row": 1, "dir": -1, "speed": 45},
    {"row": 2, "dir": +1, "speed": 55},
    {"row": 3, "dir": -1, "speed": 60},
    {"row": 4, "dir": +1, "speed": 50},
]
WATER_TARGET_GAP_CELLS = 3.0

# === Параметры машин ===
CAR_SIZES = [
    {"size": 1, "prob": 0.35},
    {"size": 2, "prob": 0.45},
    {"size": 3, "prob": 0.20},
]
CAR_COLORS = [
    (100, 50, 200),
    (50, 210, 240),
    (230, 120, 60),
    (120, 200, 80),
    (40, 140, 255),
    (200, 80, 170),
]
CAR_MIN_GAP_CELLS = 1

# === Параметры брёвен ===
LOG_SIZES = [
    {"size": 2, "prob": 0.50},
    {"size": 3, "prob": 0.30},
    {"size": 4, "prob": 0.20},
]
LOG_COLORS = [
    (131, 86, 62),
]

# === Параметры крокодилов ===
CROC_SIZES = [
    {"size": 2, "prob": 0.70},
    {"size": 3, "prob": 0.30},
]
CROC_COLORS = [
    (20, 120, 20),
]

# Параметры спавна объектов на воде
WATER_MIN_GAP_CELLS = 1
WATER_SPAWN_WEIGHTS = {"log": 0.75, "croc": 0.25}
WATER_MAX_CONSEC_CROCS = 2 # максимальное кол-во подряд идущих крокодилов

# === Геймплей ===
START_LIVES = 3
