import random

from dataclasses import dataclass
from typing import List, Dict
from settings import (
    CELL_SIZE,
    GRID_COLS,
    GRID_ROWS,
    WINDOW_WIDTH,
    CAR_SIZES,
    CAR_COLORS,
    CAR_MIN_SPAWN_INTERVAL,
    CAR_MAX_SPAWN_INTERVAL,
    LOG_SIZES,
    LOG_COLORS,
    LOG_MIN_SPAWN_INTERVAL,
    LOG_MAX_SPAWN_INTERVAL,
)
from utils import clamp, weighted_choice

@dataclass
class Frog:
    col: int
    row: int
        
    def move(self, col: int, row: int):
        self.col += col
        self.row += row
        self.col = clamp(self.col, 0, GRID_COLS - 1)
        self.row = clamp(self.row, 0, GRID_ROWS - 1)

    def reset(self):
        self.col = GRID_COLS // 2
        self.row = GRID_ROWS - 2


@dataclass
class Car:
    x: float
    row: int
    direction: int
    speed: float
    size: int
    color: tuple

    def update(self, dt: float):
        self.x += self.direction * self.speed * dt

    def is_visible(self) -> bool:
        if self.direction == +1:
            return (self.x + self.size * CELL_SIZE) > 0
        else:
            return self.x < WINDOW_WIDTH


class CarSpawner:
    def __init__(self, lanes: List[Dict]):
        self.lanes = lanes
        self.cars: List[Car] = []
        self.spawn_interval = 1.0
        self.next_spawn_time = 0.0

    def spawn_car(self) -> Car:
        lane = random.choice(self.lanes)

        size_info = weighted_choice(CAR_SIZES)
        size = size_info["size"]

        color = random.choice(CAR_COLORS)

        if lane["dir"] == +1:
            x = -size * CELL_SIZE
        else:
            x = WINDOW_WIDTH

        return Car(
            x=x,
            row=lane["row"],
            direction=lane["dir"],
            speed=lane["speed"],
            size=size,
            color=color,
        )

    def update(self, current_time: float, dt: float):
        if current_time >= self.next_spawn_time:
            self.cars.append(self.spawn_car())

            self.spawn_interval = random.uniform(CAR_MIN_SPAWN_INTERVAL, CAR_MAX_SPAWN_INTERVAL)
            self.next_spawn_time = current_time + self.spawn_interval

        alive = []
        for car in self.cars:
            car.update(dt)
            if car.is_visible():
                alive.append(car)
        self.cars = alive


@dataclass
class WoodLog:
    x: float
    row: int
    direction: int
    speed: float
    size: int
    color: tuple
    
    def update(self, dt: float):
        self.x += self.direction * self.speed * dt

    def is_visible(self) -> bool:
        if self.direction == +1:
            return (self.x + self.size * CELL_SIZE) > 0
        else:
            return self.x < WINDOW_WIDTH
        

class WoodLogSpawner:
    def __init__(self, lanes: List[Dict]):
        self.lanes = lanes
        self.logs: List[WoodLog] = []
        self.spawn_interval = 1.0
        self.next_spawn_time = 0.0

    def spawn_log(self) -> WoodLog:
        lane = random.choice(self.lanes)

        size_info = weighted_choice(LOG_SIZES)
        size = size_info["size"]

        color = random.choice(LOG_COLORS)

        if lane["dir"] == +1:
            x = -size * CELL_SIZE
        else:
            x = WINDOW_WIDTH

        return WoodLog(
            x=x,
            row=lane["row"],
            direction=lane["dir"],
            speed=lane["speed"],
            size=size,
            color=color,
        )

    def update(self, current_time: float, dt: float):
        if current_time >= self.next_spawn_time:
            self.logs.append(self.spawn_log())

            self.spawn_interval = random.uniform(LOG_MIN_SPAWN_INTERVAL, LOG_MAX_SPAWN_INTERVAL)
            self.next_spawn_time = current_time + self.spawn_interval

        alive = []
        for log in self.logs:
            log.update(dt)
            if log.is_visible():
                alive.append(log)
        self.logs = alive
