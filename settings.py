# Параметры сетки
CELL_SIZE = 40
GRID_COLS = 17
GRID_ROWS = 12

# Параметры окна
WINDOW_WIDTH  = GRID_COLS * CELL_SIZE
WINDOW_HEIGHT = GRID_ROWS * CELL_SIZE
WINDOW_TITLE  = "Frogger"

# FPS
TARGET_FPS     = 30
FRAME_DELAY_MS = int(1000 / TARGET_FPS)

# Цвета
BG_COLOR     = (10, 10, 10)
GRID_COLOR   = (50, 50, 50)
FINISH_COLOR = (190, 15, 150)
WATER_COLOR  = (255, 0, 0)
ROAD_COLOR   = (60, 60, 60)
START_COLOR  = (0, 120, 0)

# Параметры воды и дороги
WATER_LANES = [
    {"row": 1, "dir": -1, "speed": 70},
    {"row": 2, "dir": -1, "speed": 70},
    {"row": 3, "dir": -1, "speed": 70},
    {"row": 4, "dir": -1, "speed": 70},
]
ROAD_LANES = [
    {"row": 5, "dir": -1, "speed": 140},
    {"row": 6, "dir": +1, "speed": 190},
    {"row": 7, "dir": -1, "speed": 220},
    {"row": 8, "dir": +1, "speed": 160},
]

# Параметры машин
CAR_SIZES = [
    {"size": 1, "prob": 0.30},
    {"size": 2, "prob": 0.50},
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
CAR_MIN_SPAWN_INTERVAL = 0.7
CAR_MAX_SPAWN_INTERVAL = 1.5

# Параметры брёвен
LOG_SIZES = [
    {"size": 2, "prob": 0.50},
    {"size": 3, "prob": 0.25},
    {"size": 4, "prob": 0.25},
]
LOG_COLORS = [
    (131, 86, 62),
]
LOG_MIN_SPAWN_INTERVAL = 0.6
LOG_MAX_SPAWN_INTERVAL = 0.9
