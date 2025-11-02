import cv2
import time

from settings import (
    GRID_COLS,
    GRID_ROWS,
    WINDOW_WIDTH,
    WINDOW_HEIGHT,
    WINDOW_TITLE,
    FRAME_DELAY_MS,
    WATER_LANES,
    ROAD_LANES,
)
from entities import Frog, CarSpawner, WoodLogSpawner
from rendering import (
    create_empty_frame,
    draw_background,
    draw_grid,
    draw_ui,
    draw_frog,
    draw_cars,
    draw_logs,
)


class Game:
    def __init__(self):
        # окно
        cv2.namedWindow(WINDOW_TITLE, cv2.WINDOW_NORMAL)
        cv2.resizeWindow(WINDOW_TITLE, WINDOW_WIDTH, WINDOW_HEIGHT)

        # сущности
        self.frog = Frog(col=GRID_COLS // 2, row=GRID_ROWS - 2)
        self.car_spawner = CarSpawner(ROAD_LANES)
        self.log_spawner = WoodLogSpawner(WATER_LANES)

        # время
        self.last_time = time.time()
        self.running = True
        self.paused = False

    def handle_input(self, key):
        # выход
        if key == 27 or key == ord('q'):
            self.running = False
            return
        
        # пауза
        if key == ord('p'):
            self.paused = not self.paused
            return

        # когда игра на паузе, движения не должны обрабатываться
        if self.paused:
            return
        
        # движение
        if key in (ord('w'), 82):   # W или стрелка вверх
            self.frog.move(0, -1)
        elif key in (ord('a'), 81): # A или стрелка влево
            self.frog.move(-1, 0)
        elif key in (ord('s'), 84): # S или стрелка вниз
            self.frog.move(0, +1)
        elif key in (ord('d'), 83): # D или стрелка вправо
            self.frog.move(+1, 0)

    def update(self, current_time, dt):
        if self.paused:
            return

        self.car_spawner.update(current_time, dt)
        self.log_spawner.update(current_time, dt)

    def draw(self):
        frame = create_empty_frame()
        draw_background(frame)
        draw_grid(frame)
        draw_logs(frame, self.log_spawner.logs)
        draw_frog(frame, self.frog)
        draw_cars(frame, self.car_spawner.cars)
        draw_ui(frame)
        cv2.imshow(WINDOW_TITLE, frame)

    def run(self):
        while self.running:
            current_time = time.time()
            dt = current_time - self.last_time
            self.last_time = current_time

            # логика
            self.update(current_time, dt)

            # отрисовка
            self.draw()

            # ввод
            key = cv2.waitKey(FRAME_DELAY_MS) & 0xFF
            if key != 255:
                self.handle_input(key)

        cv2.destroyAllWindows()
