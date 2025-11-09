import cv2
import numpy as np

from settings import (
    CELL_SIZE,
    WINDOW_WIDTH,
    WINDOW_HEIGHT,
    BG_COLOR,
    GRID_COLOR,
    FINISH_COLOR,
    WATER_COLOR,
    ROAD_COLOR,
    START_COLOR,
    FINISH_ROWS, WATER_ROWS, ROAD_ROWS, START_ROWS,
    CAR_COLORS, CAR_SIZES,
    LOG_COLORS, LOG_SIZES,
    CROC_COLORS, CROC_SIZES,
    LILYPAD_LOCATIONS,
    GRASS_LOCATIONS,
)
from enums import Facing, Direction
from entities import Frog, MovingRect, Car, WoodLog, Crocodile

# Cловарь для хранения сгенерированных спрайтов
ASSETS = {}

# ===============================================
# Функция для рисования спрайтов с прозрачностью
# ================================================
def overlay_sprite(background_frame, sprite_bgra, x, y):
    x, y = int(x), int(y)
    h, w = sprite_bgra.shape[:2]

    sprite_x_start, sprite_y_start = 0, 0
    frame_x_start, frame_y_start = x, y

    if frame_x_start < 0:
        sprite_x_start = -frame_x_start
        frame_x_start = 0
    if frame_y_start < 0:
        sprite_y_start = -frame_y_start
        frame_y_start = 0
    
    sprite_w = w - sprite_x_start
    sprite_h = h - sprite_y_start
    
    frame_x_end = frame_x_start + sprite_w
    frame_y_end = frame_y_start + sprite_h
    
    if frame_x_end >= WINDOW_WIDTH:
        sprite_w = max(0, sprite_w - (frame_x_end - WINDOW_WIDTH))
        frame_x_end = WINDOW_WIDTH
    if frame_y_end >= WINDOW_HEIGHT:
        sprite_h = max(0, sprite_h - (frame_y_end - WINDOW_HEIGHT))
        frame_y_end = WINDOW_HEIGHT
        
    # Если спрайт полностью за экраном, выходим
    if sprite_w <= 0 or sprite_h <= 0:
        return

    sprite_cut = sprite_bgra[sprite_y_start : sprite_y_start + sprite_h, sprite_x_start : sprite_x_start + sprite_w]
    
    roi = background_frame[frame_y_start : frame_y_end, frame_x_start : frame_x_end]

    sprite_bgr = sprite_cut[..., :3]
    alpha = sprite_cut[..., 3] / 255.0
    alpha = alpha[..., np.newaxis]

    blended_roi = (roi * (1.0 - alpha) + sprite_bgr * alpha).astype(np.uint8)

    background_frame[frame_y_start : frame_y_end, frame_x_start : frame_x_end] = blended_roi

# =================================
# Генераторы спрайтов
# =================================
def _create_frog_sprite(facing: Facing) -> np.ndarray:
    sprite = np.zeros((CELL_SIZE, CELL_SIZE, 4), dtype=np.uint8)
    color = (21, 109, 19, 255)
    cx, cy = CELL_SIZE // 2, CELL_SIZE // 2
    
    # Тело
    cv2.rectangle(sprite, (cx - 10, cy - 10), (cx + 10, cy + 10), color, -1)
    
    # Глаза
    eye_color = (255, 255, 255, 255)
    if facing == Facing.UP:
        cv2.rectangle(sprite, (cx - 7, cy - 12), (cx - 3, cy - 8), eye_color, -1)
        cv2.rectangle(sprite, (cx + 3, cy - 12), (cx + 7, cy - 8), eye_color, -1)
    elif facing == Facing.DOWN:
        cv2.rectangle(sprite, (cx - 7, cy + 12), (cx - 3, cy + 8), eye_color, -1)
        cv2.rectangle(sprite, (cx + 3, cy + 12), (cx + 7, cy + 8), eye_color, -1)
    elif facing == Facing.LEFT:
        cv2.rectangle(sprite, (cx - 12, cy - 7), (cx - 8, cy - 3), eye_color, -1)
        cv2.rectangle(sprite, (cx - 12, cy + 7), (cx - 8, cy + 3), eye_color, -1)
    elif facing == Facing.RIGHT:
        cv2.rectangle(sprite, (cx + 12, cy - 7), (cx + 8, cy - 3), eye_color, -1)
        cv2.rectangle(sprite, (cx + 12, cy + 7), (cx + 8, cy + 3), eye_color, -1)

    return sprite

def _create_car_sprite(size: int, color: tuple, direction: Direction) -> np.ndarray:
    width = size * CELL_SIZE
    height = CELL_SIZE
    sprite = np.zeros((height, width, 4), dtype=np.uint8)
    
    # Кузов
    cv2.rectangle(sprite, (0, 0), (width, height), (*color, 255), -1)

    # Стекло
    cv2.rectangle(sprite, (int(width * 0.2), 5), (int(width * 0.8), height - 5), (150, 150, 150, 255), -1)
    
    # Фары
    if direction == Direction.RIGHT:
        cv2.rectangle(sprite, (width - 8, 5), (width - 2, 15), (0, 255, 255, 255), -1)
        cv2.rectangle(sprite, (width - 8, height - 15), (width - 2, height - 5), (0, 255, 255, 255), -1)
    else:
        cv2.rectangle(sprite, (2, 5), (8, 15), (0, 255, 255, 255), -1)
        cv2.rectangle(sprite, (2, height - 15), (8, height - 5), (0, 255, 255, 255), -1)

    return sprite

def _create_log_sprite(size: int) -> np.ndarray:
    width = size * CELL_SIZE
    height = CELL_SIZE
    sprite = np.zeros((height, width, 4), dtype=np.uint8)
    color = LOG_COLORS[0]

    # Бревно
    cv2.rectangle(sprite, (0, 5), (width, height - 5), (*color, 255), -1)

    # Линии коры
    cv2.line(sprite, (5, 10), (width - 5, 10), (color[0]-20, color[1]-20, color[2]-20, 255), 2)
    cv2.line(sprite, (5, height - 10), (width - 5, height - 10), (color[0]-20, color[1]-20, color[2]-20, 255), 2)

    return sprite

def _create_croc_sprite(size: int, direction: Direction) -> np.ndarray:
    width = size * CELL_SIZE
    height = CELL_SIZE
    sprite = np.zeros((height, width, 4), dtype=np.uint8)
    color = CROC_COLORS[0]
    
    # Тело
    cv2.rectangle(sprite, (0, 8), (width, height - 8), (*color, 255), -1)
    
    # Глаза
    eye_color = (0, 200, 200, 255)
    if direction == Direction.RIGHT:
        cv2.rectangle(sprite, (width - 20, 2), (width - 10, 12), eye_color, -1)
        cv2.rectangle(sprite, (width - 40, 2), (width - 30, 12), eye_color, -1)
    else:
        cv2.rectangle(sprite, (10, 2), (20, 12), eye_color, -1)
        cv2.rectangle(sprite, (30, 2), (40, 12), eye_color, -1)

    return sprite

def load_assets():
    global ASSETS
    ASSETS = {}
    
    # Лягушка
    for facing in Facing:
        ASSETS[f"frog_{facing.name.lower()}"] = _create_frog_sprite(facing)
        
    # Машины
    for i, color in enumerate(CAR_COLORS):
        for size_info in CAR_SIZES:
            size = size_info["size"]
            for direction in Direction:
                key = f"car_{size}_{i}_{direction.name.lower()}"
                ASSETS[key] = _create_car_sprite(size, color, direction)
                
    # Бревна
    for size_info in LOG_SIZES:
        size = size_info["size"]
        key = f"log_{size}"
        ASSETS[key] = _create_log_sprite(size)
        
    # Крокодилы
    for size_info in CROC_SIZES:
        size = size_info["size"]
        for direction in Direction:
            key = f"croc_{size}_{direction.name.lower()}"
            ASSETS[key] = _create_croc_sprite(size, direction)

# =================================
# Отрисовка
# =================================
def create_empty_frame():
    return np.zeros((WINDOW_HEIGHT, WINDOW_WIDTH, 3), dtype=np.uint8)

def draw_background(frame):
    frame[:] = BG_COLOR

    def row_y(row):
        return row * CELL_SIZE

    cv2.rectangle(frame, (0, row_y(FINISH_ROWS[0])), (WINDOW_WIDTH, row_y(FINISH_ROWS[1] + 1)), FINISH_COLOR, -1)
    cv2.rectangle(frame, (0, row_y(WATER_ROWS[0])), (WINDOW_WIDTH, row_y(WATER_ROWS[1] + 1)), WATER_COLOR, -1)
    cv2.rectangle(frame, (0, row_y(ROAD_ROWS[0])), (WINDOW_WIDTH, row_y(ROAD_ROWS[1] + 1)), ROAD_COLOR, -1)
    cv2.rectangle(frame, (0, row_y(START_ROWS[0])), (WINDOW_WIDTH, row_y(START_ROWS[1] + 1)), START_COLOR, -1)

    row = FINISH_ROWS[0]
    y_center = row * CELL_SIZE + CELL_SIZE // 2
    radius = CELL_SIZE // 2 - 8
    color_dark = (0, 100, 0)
    color_light = (0, 150, 0)
    
    for col in LILYPAD_LOCATIONS:
        x_center = col * CELL_SIZE + CELL_SIZE // 2
        cv2.circle(frame, (x_center, y_center), radius, color_dark, -1)
        cv2.circle(frame, (x_center, y_center), radius - 3, color_light, -1)

    color_grass = (50, 180, 50)
    for col, row in GRASS_LOCATIONS:
        x_base = col * CELL_SIZE + CELL_SIZE // 2
        y_base = row * CELL_SIZE + CELL_SIZE - 5
        
        cv2.line(frame, (x_base - 5, y_base), (x_base - 3, y_base - 10), color_grass, 2)
        cv2.line(frame, (x_base, y_base), (x_base, y_base - 12), color_grass, 2)
        cv2.line(frame, (x_base + 5, y_base), (x_base + 4, y_base - 9), color_grass, 2)

def draw_grid(frame):
    h, w, _ = frame.shape
    for x in range(0, w, CELL_SIZE):
        cv2.line(frame, (x, 0), (x, h), GRID_COLOR, 1)
    for y in range(0, h, CELL_SIZE):
        cv2.line(frame, (0, y), (w, y), GRID_COLOR, 1)

def draw_ui(frame, lives: int, state_text: str = ""):
    cv2.putText(frame, f"Lives: {lives}", (10, WINDOW_HEIGHT - 15), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 1, cv2.LINE_AA)
    if state_text:
        cv2.putText(frame, state_text, (10, 25), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (255, 255, 255), 2, cv2.LINE_AA)

def draw_rect_from_hitbox(frame, hb, color):
    x1, y1, x2, y2 = hb
    cv2.rectangle(frame, (int(x1 + 4), int(y1 + 4)), (int(x2 - 4), int(y2 - 4)), color, -1)

def draw_frog(frame, frog: Frog):
    sprite_key = f"frog_{frog.facing.name.lower()}"
    
    sprite = ASSETS.get(sprite_key)
    
    if sprite is not None:
        overlay_sprite(frame, sprite, frog.pixel_x, frog.pixel_y)
    else:
        draw_rect_from_hitbox(frame, frog.hitbox, (0, 255, 0))

def draw_movers(frame, movers: list[MovingRect]):
    for m in movers:
        sprite_key = ""
        
        if isinstance(m, Car):
            try:
                color_index = CAR_COLORS.index(m.color)
                sprite_key = f"car_{m.size}_{color_index}_{m.direction.name.lower()}"
            except ValueError:
                pass
                
        elif isinstance(m, WoodLog):
            sprite_key = f"log_{m.size}"
            
        elif isinstance(m, Crocodile):
            sprite_key = f"croc_{m.size}_{m.direction.name.lower()}"
        
        sprite = ASSETS.get(sprite_key)
        
        if sprite is not None:
            overlay_sprite(frame, sprite, m.x, m.y)
        else:
            draw_rect_from_hitbox(frame, m.hitbox, m.color)