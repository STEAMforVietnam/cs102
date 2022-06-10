import csv
from dataclasses import dataclass
from pathlib import Path
from typing import List, Optional

from common.types import TileType

ASSET_DIR = Path("assets")
DATA_DIR = Path("data")


class GameConfig:
    NAME: str = "Steam Valley"
    FPS: int = 60
    WIDTH: int = 1280
    HEIGHT: int = 768
    SCENE_ONE_BG_IMG_PATH: str = ASSET_DIR / "bg_scene_one.png"
    GROUND_SPRITE_PATH: str = ASSET_DIR / "tiles" / "ground.png"

    GRAVITY: int = 2
    TILE_SIZE: int = 48
    PLAYER_SOFT_EDGE_WIDTH: int = 300


class PlayerConfig:
    SPRITES_DIR: str = ASSET_DIR / "player"
    SCALE: float = 0.18
    SPEED: int = 8
    JUMP_VERTICAL_SPEED: int = 30
    # minimal time until switching to the next sprite in sequence
    ANIMATION_INTERVAL_MS: int = 80


class ShadowConfig:
    sprite_dir: str = ASSET_DIR / "shadow"
    scale: float = 0.2
    animation_interval_ms: int = 200


@dataclass
class SceneData:
    id: int
    data: Optional[List] = None

    def __post_init__(self):
        with open(DATA_DIR / "scenes" / f"{self.id}.csv", newline="") as csvfile:
            reader = csv.reader(csvfile, delimiter=",")
            self.data = [
                [TileType(int(tile or TileType.EMPTY.value)) for tile in row] for row in reader
            ]
