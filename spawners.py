import random
from typing import List, Dict, Type

from enums import Direction
from settings import (
    CELL_SIZE, WINDOW_WIDTH,
    CAR_SIZES, CAR_COLORS, CAR_MIN_GAP_CELLS,
    LOG_SIZES, LOG_COLORS,
    CROC_SIZES, CROC_COLORS,
    WATER_LANES, WATER_MIN_GAP_CELLS,
    WATER_SPAWN_WEIGHTS, WATER_MAX_CONSEC_CROCS,
    ROAD_TARGET_GAP_CELLS, WATER_TARGET_GAP_CELLS,
)
from utils import weighted_choice
from entities import Car, Crocodile, WoodLog, MovingRect


class LaneSpawner:
    def __init__(self, lanes: List[Dict],
                 cls: Type[MovingRect],
                 size_table: List[Dict],
                 colors: List[tuple],
                 min_gap_cells: int):
        self.cls = cls
        self.lanes = []
        for lane in lanes:
            self.lanes.append(
                {
                "row": lane["row"],
                "dir": Direction(lane["dir"]),
                "speed": lane["speed"],
                "items": [],
                "next_spawn_time": 0.0,
                "interval": 1.0,
                }
            )
        self.size_table = size_table
        self.colors = colors
        self.min_gap_px = min_gap_cells * CELL_SIZE

    def _can_spawn_in_lane(self, lane_state, width: int) -> bool:
        dir_ = lane_state["dir"]
        items: List[MovingRect] = lane_state["items"]
        if dir_ == Direction.RIGHT:
            spawn_x = -width
            for it in items:
                if it.row != lane_state["row"]:
                    continue
                if (it.x + it.width) > spawn_x and it.x < (spawn_x + width + self.min_gap_px):
                    return False
            return True
        else:
            spawn_x = WINDOW_WIDTH
            for it in items:
                if it.row != lane_state["row"]:
                    continue
                if (it.x) < (spawn_x + width) and (it.x + it.width) > (spawn_x - self.min_gap_px):
                    return False
            return True

    def _spawn_in_lane(self, lane_state) -> MovingRect:
        size_info = weighted_choice(self.size_table)
        size = size_info["size"]
        color = random.choice(self.colors)
        width = size * CELL_SIZE

        x = -width if lane_state["dir"] == Direction.RIGHT else WINDOW_WIDTH
        obj = self.cls(
            x=x,
            row=lane_state["row"],
            direction=lane_state["dir"],
            speed=lane_state["speed"],
            size=size,
            color=color,
        )
        return obj

    def update(self, now: float, dt: float):
        for lane_state in self.lanes:
            if now >= lane_state["next_spawn_time"]:
                size_info = weighted_choice(self.size_table)
                size = size_info["size"]
                width = size * CELL_SIZE

                if self._can_spawn_in_lane(lane_state, width):
                    obj = self._spawn_in_lane(lane_state)
                    lane_state["items"].append(obj)

                v = lane_state["speed"]
                mean_interval = (ROAD_TARGET_GAP_CELLS * CELL_SIZE + width) / max(v, 1e-6)
                lane_state["interval"] = random.uniform(0.8, 1.2) * mean_interval
                lane_state["next_spawn_time"] = now + lane_state["interval"]

            alive = []
            for it in lane_state["items"]:
                it.update(dt)
                if it.is_visible():
                    alive.append(it)
            lane_state["items"] = alive

    @property
    def all_items(self) -> List[MovingRect]:
        out: List[MovingRect] = []
        for lane_state in self.lanes:
            out.extend(lane_state["items"])
        return out


# ==============================
# Спавнер для машин
# ==============================
class CarSpawner(LaneSpawner):
    def __init__(self, lanes: List[Dict]):
        super().__init__(lanes,
                         Car,
                         CAR_SIZES,
                         CAR_COLORS,
                         min_gap_cells=CAR_MIN_GAP_CELLS)


# ================================
# Спавнер для крокодилов и брёвен
# ================================
class WaterLaneSpawner:
    def __init__(self, lanes: List[Dict]):
        self.lanes = []
        for lane in lanes:
            self.lanes.append(
                {
                "row": lane["row"],
                "dir": Direction(lane["dir"]),
                "speed": lane["speed"],
                "items": [],
                "next_spawn_time": 0.0,
                "interval": 1.0,
                "consec_crocs": 0,
                "last_type": None,
                }
            )
        self.min_interval = 0.0
        self.max_interval = 0.0
        self.min_gap_px  = WATER_MIN_GAP_CELLS * CELL_SIZE

    def _choose_type(self, lane_state) -> str:
        if lane_state["consec_crocs"] >= WATER_MAX_CONSEC_CROCS:
            return "log"
        r = random.random()
        if r < WATER_SPAWN_WEIGHTS["croc"]:
            return "croc"
        return "log"

    def _can_spawn(self, lane_state, width: int) -> bool:
        dir_ = lane_state["dir"]
        items: List[MovingRect] = lane_state["items"]
        if dir_ == Direction.RIGHT:
            spawn_x = -width
            for it in items:
                if it.row != lane_state["row"]:
                    continue
                if (it.x + it.width) > spawn_x and it.x < (spawn_x + width + self.min_gap_px):
                    return False
            return True
        else:
            spawn_x = WINDOW_WIDTH
            for it in items:
                if it.row != lane_state["row"]:
                    continue
                if (it.x) < (spawn_x + width) and (it.x + it.width) > (spawn_x - self.min_gap_px):
                    return False
            return True

    def _spawn(self, lane_state, kind: str) -> MovingRect:
        if kind == "log":
            size = weighted_choice(LOG_SIZES)["size"]
            color = random.choice(LOG_COLORS)
            cls = WoodLog
        else:
            size = weighted_choice(CROC_SIZES)["size"]
            color = random.choice(CROC_COLORS)
            cls = Crocodile

        width = size * CELL_SIZE
        x = -width if lane_state["dir"] == Direction.RIGHT else WINDOW_WIDTH
        return cls(
            x=x,
            row=lane_state["row"],
            direction=lane_state["dir"],
            speed=lane_state["speed"],
            size=size,
            color=color,
        )
    
    def _spawn_with_size(self, lane_state, kind: str, size: int) -> MovingRect:
        if kind == "log":
            color = random.choice(LOG_COLORS)
            cls = WoodLog
        else:
            color = random.choice(CROC_COLORS)
            cls = Crocodile

        width = size * CELL_SIZE
        x = -width if lane_state["dir"] == Direction.RIGHT else WINDOW_WIDTH
        return cls(
            x=x,
            row=lane_state["row"],
            direction=lane_state["dir"],
            speed=lane_state["speed"],
            size=size,
            color=color,
        )

    def update(self, now: float, dt: float):
        for lane_state in self.lanes:
            if now >= lane_state["next_spawn_time"]:
                kind = self._choose_type(lane_state)

                if kind == "log":
                    size = weighted_choice(LOG_SIZES)["size"]
                else:
                    size = weighted_choice(CROC_SIZES)["size"]
                width = size * CELL_SIZE

                if self._can_spawn(lane_state, width):
                    obj = self._spawn_with_size(lane_state, kind, size)
                    lane_state["items"].append(obj)
                    if kind == "croc":
                        lane_state["consec_crocs"] += 1
                    else:
                        lane_state["consec_crocs"] = 0

                v = lane_state["speed"]
                mean_interval = (WATER_TARGET_GAP_CELLS * CELL_SIZE + width) / max(v, 1e-6)
                lane_state["interval"] = random.uniform(0.8, 1.2) * mean_interval
                lane_state["next_spawn_time"] = now + lane_state["interval"]

            alive = []
            for it in lane_state["items"]:
                it.update(dt)
                if it.is_visible():
                    alive.append(it)
            lane_state["items"] = alive

    @property
    def all_items(self) -> List[MovingRect]:
        out: List[MovingRect] = []
        for lane_state in self.lanes:
            out.extend(lane_state["items"])
        return out
