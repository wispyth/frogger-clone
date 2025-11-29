import cv2
import time

from enums import GameState
from settings import (
    WINDOW_WIDTH, WINDOW_HEIGHT, WINDOW_TITLE,
    FRAME_DELAY_MS,
    FINISH_ROWS,
    ROAD_LANES, WATER_LANES,
    START_LIVES,
)
from entities import Frog, WoodLog, Crocodile
from spawners import CarSpawner, WaterLaneSpawner
from rendering import (
    create_empty_frame,
    draw_background,
    draw_grid,
    draw_ui,
    draw_frog,
    draw_movers,
)
from utils import rects_intersect


class Game:
    def __init__(self):
        cv2.namedWindow(WINDOW_TITLE, cv2.WINDOW_NORMAL)
        cv2.resizeWindow(WINDOW_TITLE, WINDOW_WIDTH, WINDOW_HEIGHT)

        # сущности
        self.frog = Frog(col=8, row=10)
        self.cars = CarSpawner(ROAD_LANES)
        self.water = WaterLaneSpawner(WATER_LANES) # брёвна + крокодилы

        # состояние
        self.state = GameState.START
        self.lives = START_LIVES
        self.running = True
        self.paused = False

        self.last_time = time.time()
        self.max_pos = 0

    @property
    def score(self):
        return self.max_pos * 10

    # ==============================
    # Ввод с клавиатуры
    # ==============================
    def handle_input(self, key):
        if key in (27, ord('q')):
            self.running = False
            return
        if key == 13 and self.state == GameState.START:
            self.state = GameState.PLAYING
            return
        if key != 255 and self.state in (GameState.GAME_OVER, GameState.WIN):
            self.state = GameState.START
            self.lives = START_LIVES
            return
        if key == ord('p'):
            self.paused = not self.paused
            return
        if self.paused or self.state != GameState.PLAYING:
            return

        if key in (ord('w'), 82):
            self.frog.step(0, -1)
        elif key in (ord('a'), 81):
            self.frog.step(-1, 0)
        elif key in (ord('s'), 84):
            self.frog.step(0, +1)
        elif key in (ord('d'), 83):
            self.frog.step(+1, 0)

    # ==============================
    # Коллизии & правила
    # ==============================
    def _attach_or_detach_on_water(self):
        # наступили на бревно -> привязываемся к нему
        if self.frog.attached_log is None and self.frog.on_water():
            for it in self.water.all_items:
                if isinstance(it, WoodLog) and rects_intersect(self.frog.hitbox, it.hitbox):
                    self.frog.attach_to(it)
                    break
        # если уже привязаны к какому-то бревну, то проверяем до сих пор ли мы на нём стоим
        elif self.frog.attached_log is not None:
            cur = self.frog.attached_log
            if rects_intersect(self.frog.hitbox, cur.hitbox):
                return
            # если не стоим, то пытаемся привязаться к другому бревну
            for it in self.water.all_items:
                if isinstance(it, WoodLog) and rects_intersect(self.frog.hitbox, it.hitbox):
                    self.frog.attach_to(it)
                    return
            self.frog.detach()

    def _death(self):
        self.lives -= 1
        print("DEAD")
        if self.lives <= 0:
            self.state = GameState.GAME_OVER
            self.max_pos = 0
        self.frog = Frog(col=8, row=10)

    def _check_death_conditions(self):
        # врезаемся в машину -> смерть
        for car in self.cars.all_items:
            if rects_intersect(self.frog.hitbox, car.hitbox):
                self._death(); return

        # наступаем на крокодила -> смерть
        for it in self.water.all_items:
            if isinstance(it, Crocodile) and rects_intersect(self.frog.hitbox, it.hitbox):
                self._death(); return

        if self.frog.on_water():
            # падаем в воду -> смерть
            if self.frog.attached_log is None:
                self._death(); return
            # уезжаем на бревне за край экрана -> смерть
            x1, _, x2, _ = self.frog.hitbox
            if x1 < 0 or x2 > WINDOW_WIDTH:
                self._death(); return

    def _check_win(self):
        if self.frog.row <= FINISH_ROWS[1]:
            self.state = GameState.WIN
            print("YOU WIN!")
            self.lives += 1; self._death(); self.max_pos = 0; return
        
    def _score_update(self):
        if self.frog.row <= (10 - self.max_pos):
            self.max_pos = 10 - self.frog.row

    # ==============================
    # Обновление & рендеринг
    # ==============================
    def update(self, now, dt):
        if self.paused or self.state not in (GameState.START, GameState.PLAYING):
            return

        self.cars.update(now, dt)
        self.water.update(now, dt)
        self.frog.update(dt)

        self._attach_or_detach_on_water()
        self._check_death_conditions()
        self._check_win()
        self._score_update()

    def draw(self):
        frame = create_empty_frame()
        draw_background(frame)
        # draw_grid(frame)
        # крокодилы и брёвна -> лягушка -> машины
        draw_movers(frame, self.water.all_items)

        if self.state not in (GameState.START, GameState.GAME_OVER, GameState.WIN):
            draw_frog(frame, self.frog)

        draw_movers(frame, self.cars.all_items)

        state_text = ""
        if self.paused == True:
            state_text = "PAUSED"
        elif self.state == GameState.START:
            state_text = "Press ENTER to start play"
        elif self.state == GameState.GAME_OVER:
            state_text = "GAME OVER - press ANY KEY to restart"
        elif self.state == GameState.WIN:
            state_text = "YOU WIN! - press ANY KEY to restart"
        draw_ui(frame, self.lives, self.score, state_text)
        cv2.imshow(WINDOW_TITLE, frame)

    def run(self):
        while self.running:
            now = time.time()
            dt = now - self.last_time
            self.last_time = now

            self.update(now, dt)
            self.draw()

            key = cv2.waitKey(FRAME_DELAY_MS) & 0xFF
            if key != 255:
                self.handle_input(key)
        cv2.destroyAllWindows()
