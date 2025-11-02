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
)

def create_empty_frame():
    return np.zeros((WINDOW_HEIGHT, WINDOW_WIDTH, 3), dtype=np.uint8)

def draw_background(frame):
    frame[:] = BG_COLOR

    def row_y(row):
        return row * CELL_SIZE

    cv2.rectangle(frame, (0, row_y(0)), (WINDOW_WIDTH, row_y(1)), FINISH_COLOR, -1)
    cv2.rectangle(frame, (0, row_y(1)), (WINDOW_WIDTH, row_y(5)), WATER_COLOR, -1)
    cv2.rectangle(frame, (0, row_y(5)), (WINDOW_WIDTH, row_y(9)), ROAD_COLOR, -1)
    cv2.rectangle(frame, (0, row_y(9)), (WINDOW_WIDTH, row_y(12)), START_COLOR, -1)

def draw_grid(frame):
    h, w, _ = frame.shape
    for x in range(0, w, CELL_SIZE):
        cv2.line(frame, (x, 0), (x, h), GRID_COLOR, 1)
    for y in range(0, h, CELL_SIZE):
        cv2.line(frame, (0, y), (w, y), GRID_COLOR, 1)

def draw_ui(frame):
    cv2.putText(frame, "Frogger", (10, WINDOW_HEIGHT - 15), cv2.FONT_HERSHEY_COMPLEX, 0.6, (255, 255, 255), 1, cv2.LINE_AA)
    cv2.putText(frame, "Press ESC or Q to quit", (10, 25), cv2.FONT_HERSHEY_COMPLEX, 0.6, (255, 255, 255), 1, cv2.LINE_AA)

def draw_frog(frame, frog):
    x_start = frog.col * CELL_SIZE + 4
    y_start = frog.row * CELL_SIZE + 4
    x_end = (frog.col + 1) * CELL_SIZE - 4
    y_end = (frog.row + 1) * CELL_SIZE - 4
    cv2.rectangle(frame, (x_start, y_start), (x_end, y_end), (0, 255, 0), -1)

def draw_cars(frame, cars):
    for car in cars:
        x_start = int(car.x + 4)
        y_start = int(car.row * CELL_SIZE + 4)
        x_end = int(car.x + car.size * CELL_SIZE - 4)
        y_end = int((car.row + 1) * CELL_SIZE - 4)
        cv2.rectangle(frame, (x_start, y_start), (x_end, y_end), car.color, -1)

def draw_logs(frame, logs):
    for log in logs:
        x_start = int(log.x + 4)
        y_start = int(log.row * CELL_SIZE + 4)
        x_end = int(log.x + log.size * CELL_SIZE - 4)
        y_end = int((log.row + 1) * CELL_SIZE - 4)
        cv2.rectangle(frame, (x_start, y_start), (x_end, y_end), log.color, -1)
