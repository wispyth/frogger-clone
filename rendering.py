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
)

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

def draw_frog(frame, frog):
    draw_rect_from_hitbox(frame, frog.hitbox, (0, 255, 0))

def draw_movers(frame, movers):
    for m in movers:
        draw_rect_from_hitbox(frame, m.hitbox, m.color)
