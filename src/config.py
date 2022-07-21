import csv
from dataclasses import dataclass
from pathlib import Path
from typing import List, Optional

import pygame

from common.types import EntityType

pygame.init()


ASSET_DIR = Path("assets")
DATA_DIR = Path("data")


class Color:
    DEFAULT = (0, 0, 255)


class GameConfig:
    DEBUG: bool = True
    NAME: str = "STEAM Valley"
    FPS: int = 60
    WIDTH: int = 1248
    HEIGHT: int = 768
    GRAVITY: int = 2
    TILE_SIZE: int = 48
    PLAYER_SOFT_EDGE_WIDTH: int = 300

    BG_OFFICE_PATH: Path = ASSET_DIR / "bg_office_1.png"


class PlayerConfig:
    SPRITE_PATH: Path = ASSET_DIR / "player"
    SCALE: float = 0.18
    SPEED: int = 8
    JUMP_VERTICAL_SPEED: int = 30
    JUMP_WITH_TRAMPOLINE_SPEED: int = 40
    # minimal time until switching to the next sprite in sequence
    ANIMATION_INTERVAL_MS: int = 80


@dataclass
class WorldData:
    level_id: int
    data: Optional[List] = None

    def __post_init__(self):
        with open(DATA_DIR / "levels" / f"{self.level_id}.csv", newline="") as csvfile:
            reader = csv.reader(csvfile, delimiter=",")
            self.data = [
                [EntityType(int(tile or EntityType.EMPTY.value)) for tile in row] for row in reader
            ]
