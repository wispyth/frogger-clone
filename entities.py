from __future__ import annotations
from dataclasses import dataclass
from typing import Optional

from settings import (
    CELL_SIZE, GRID_COLS, GRID_ROWS,
    WINDOW_WIDTH,
    WATER_ROWS, ROAD_ROWS,
)
from enums import Direction
from utils import clamp


class HasHitbox:
    @property
    def hitbox(self):
        raise NotImplementedError


# ==============================
# Лягушка
# ==============================
@dataclass
class Frog(HasHitbox):
    col: int
    row: int

    attached_log: Optional[WoodLog] = None
    rel_cell: int = 0 # позиция относительно бревна

    def on_water(self) -> bool:
        return WATER_ROWS[0] <= self.row <= WATER_ROWS[1]

    def on_road(self) -> bool:
        return ROAD_ROWS[0] <= self.row <= ROAD_ROWS[1]

    @property
    def pixel_x(self) -> int:
        if self.attached_log is not None:
            return int(self.attached_log.x) + self.rel_cell * CELL_SIZE
        return self.col * CELL_SIZE

    @property
    def pixel_y(self) -> int:
        if self.attached_log is not None:
            return int(self.attached_log.y)
        return self.row * CELL_SIZE

    @property
    def hitbox(self):
        pad = 1
        x1, y1 = self.pixel_x + pad, self.pixel_y + pad
        x2, y2 = x1 + CELL_SIZE - 2*pad, y1 + CELL_SIZE - 2*pad
        return (x1, y1, x2, y2)

    # ==============================
    # Действия
    # ==============================
    def step(self, col: int, row: int):
        if row != 0 and self.attached_log is not None:
            # при сходе с бревна нужно снова встать в сетку
            self.col = int(round(self.pixel_x / CELL_SIZE))
            self.detach() # чтобы нас не откатывало на то же бревно

        self.row += row

        # движение влево/вправо зависит от того, находимся ли мы на бревне
        if self.attached_log is None:
            self.col += col
        else:
            self.rel_cell = self.rel_cell + col

        self._clamp_to_bounds()

    def attach_to(self, log: WoodLog):
        self.attached_log = log
        log_start_cell = log.start_cell
        self.rel_cell = clamp(self.col - log_start_cell, 0, log.size - 1)
        self.row = log.row
        self.col = log_start_cell + self.rel_cell

    def detach(self):
        self.attached_log = None
        self.rel_cell = 0

    def update(self, dt: float):
        if self.attached_log is not None:
            self.row = self.attached_log.row
        self._clamp_to_bounds()

    def _clamp_to_bounds(self):
        self.col = clamp(self.col, 0, GRID_COLS - 1)
        self.row = clamp(self.row, 0, GRID_ROWS - 1)


# ===============================================
# Движущиеся объекты (машины, крокодилы, брёвна)
# ===============================================
@dataclass
class MovingRect(HasHitbox):
    x: float
    row: int
    direction: Direction
    speed: float # пиксели в секунду
    size: int # кол-во ячеек
    color: tuple

    @property
    def y(self) -> float:
        return self.row * CELL_SIZE

    @property
    def width(self) -> int:
        return self.size * CELL_SIZE

    def update(self, dt: float):
        self.x += self.direction * self.speed * dt

    def is_visible(self) -> bool:
        if self.direction > 0:
            return self.x < WINDOW_WIDTH
        else:
            return (self.x + self.width) > 0

    @property
    def hitbox(self):
        pad = 1
        x1, y1 = int(self.x) + pad, int(self.y) + pad
        x2, y2 = x1 + self.width - 2*pad, y1 + CELL_SIZE - 2*pad
        return (x1, y1, x2, y2)


class Car(MovingRect):
    pass


class Crocodile(MovingRect):
    pass


class WoodLog(MovingRect):
    @property
    def start_cell(self) -> int:
        return int(self.x // CELL_SIZE)
