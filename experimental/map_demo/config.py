import csv
import enum
import os
from dataclasses import dataclass
from typing import Optional, List

import pygame


RED = (255, 0, 0)


@dataclass
class GameConfig:
    fps: int = 60
    width: int = 1500
    height: int = 750
    gravity: float = 0.5


BACKGROUND = pygame.transform.scale(
    pygame.image.load(os.path.join("assets", "background.png")),
    (GameConfig.width, GameConfig.height),
)


@dataclass
class PlayerConfig:
    animation_time: int = 80
    width: int = 100
    height: int = 220
    scale: int = 0.2
    x0: int = 30
    sprite_dir: str = "assets/player"
    speed: int = 5
    y_speed: int = -15


class ActionType(enum.Enum):
    IDLE = "idle"
    JUMP = "jump"
    MOVE_LEFT = "move_left"
    MOVE_RIGHT = "move_right"


@dataclass
class LevelConfig:
    id: int = 0
    rows: int = 16
    cols: int = 150
    tile_size: int = GameConfig.height // rows
    data_dir: str = "data/level/"
    raw_data: Optional[List] = None

    def __post_init__(self):
        with open(
            os.path.join(self.data_dir, str(self.id) + ".csv"), newline=""
        ) as csvfile:
            reader = csv.reader(csvfile, delimiter=",")
            self.raw_data = [[int(tile) for tile in row] for row in reader]


def load_tile_img(path):
    img = pygame.image.load(path)
    img = pygame.transform.scale(img, (LevelConfig.tile_size, LevelConfig.tile_size))
    return img


TILE_IMGS = [load_tile_img(f"assets/tile/{tile_id}.png") for tile_id in range(21)]
