import cv2
import numpy as np

# =========================
# КОНФИГУРАЦИИ
# =========================

CELL_SIZE       = 40                        # 1 клетка = 40 пикселей
GRID_COLS       = 16
GRID_ROWS       = 12
WINDOW_WIDTH    = GRID_COLS * CELL_SIZE     # 16 * 40 = 640
WINDOW_HEIGHT   = GRID_ROWS * CELL_SIZE     # 12 * 40 = 480

WINDOW_TITLE    = "Frogger"

TARGET_FPS      = 60
FRAME_DELAY_MS  = int(1000 / TARGET_FPS)

GRID_COLOR      = (50, 50, 50)
FINISH_COLOR    = (190, 15, 150)
WATER_COLOR     = (255, 0, 0)
ROAD_COLOR      = (60, 60, 60)
START_COLOR     = (0, 120, 0)

# =========================
# ВСПОМОГАТЕЛЬНЫЕ ФУНКЦИИ РИСОВАНИЯ
# =========================

# Сетка поверх кадра
def draw_grid(frame, cell_size=40, color=(50, 50, 50)):
    h, w, _ = frame.shape

    for x in range(0, w, cell_size):    # вертикальные линии
        cv2.line(frame, (x, 0), (x, h), color, 1)

    for y in range(0, h, cell_size):    # горизонтальные линии
        cv2.line(frame, (0, y), (w, y), color, 1)

# Грубая раскраска фона:
# - 0-й ряд: зона финиша
# - 1-4 ряды: вода
# - 5-8 ряды: дорога
# - 9-11 ряды: стартовая зона
def draw_background(frame):
    frame[:] = (10, 10, 10)

    # вычислим границы по рядам
    def row_to_y(row):
        return row * CELL_SIZE

    # зона финиша
    y_finish_start = row_to_y(0)
    y_finish_end = row_to_y(1)
    cv2.rectangle(frame, (0, y_finish_start), (WINDOW_WIDTH, y_finish_end), FINISH_COLOR, -1)

    # вода
    y_water_start = row_to_y(1)
    y_water_end = row_to_y(5)
    cv2.rectangle(frame, (0, y_water_start), (WINDOW_WIDTH, y_water_end), WATER_COLOR, -1)

    # дорога
    y_road_start = row_to_y(5)
    y_road_end = row_to_y(9)
    cv2.rectangle(frame, (0, y_road_start), (WINDOW_WIDTH, y_road_end), ROAD_COLOR, -1)

    # стартовая зона
    y_start_start = row_to_y(9)
    y_start_end = row_to_y(12)
    cv2.rectangle(frame, (0, y_start_start), (WINDOW_WIDTH, y_start_end), START_COLOR, -1)

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

def main():
    # создаём окно
    cv2.namedWindow(WINDOW_TITLE, cv2.WINDOW_NORMAL)
    cv2.resizeWindow(WINDOW_TITLE, WINDOW_WIDTH, WINDOW_HEIGHT)

    while True:
        # создаём пустой кадр
        frame = np.zeros((WINDOW_HEIGHT, WINDOW_WIDTH, 3), dtype=np.uint8)

        # рисуем фон
        draw_background(frame)

        # рисуем сетку
        draw_grid(frame)

        # рисуем UI
        draw_ui(frame)

        # показываем
        cv2.imshow(WINDOW_TITLE, frame)

        # обработка клавиатуры
        key = cv2.waitKey(FRAME_DELAY_MS) & 0xFF
        if key == 27 or key == ord('q'):    # ESC или q
            break

    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()
