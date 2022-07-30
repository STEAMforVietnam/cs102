import csv
import json
from dataclasses import dataclass
from pathlib import Path
from typing import List, Optional, Tuple

import pygame

from common.types import EntityType

pygame.init()


ASSET_DIR = Path("assets")
DATA_DIR = Path("data")

FONT_PATH = ASSET_DIR / "fonts" / "arial.ttf"


class Color:
    DEFAULT = (0, 0, 255)
    TEXT_DIALOGUE_SUBJECT = (19, 2, 150)
    TEXT_DIALOGUE = (204, 115, 14)


class GameConfig:
    DEBUG: bool = False
    NAME: str = "STEAM Valley"
    FPS: int = 60
    WIDTH: int = 1280
    HEIGHT: int = 768
    GRAVITY: int = 2
    TILE_SIZE: int = 48
    PLAYER_SOFT_EDGE_WIDTH: int = 300

    BG_OFFICE_PATH: Path = ASSET_DIR / "bg_office_1.png"


class DialogueBoxConfig:
    SPRITE_PATH: Path = ASSET_DIR / "items" / "dialogue_box.png"
    WIDTH: int = 800
    HEIGHT: int = 200
    SCALE: Tuple[int, int] = (WIDTH, HEIGHT)
    X: int = (GameConfig.WIDTH - WIDTH) // 2
    Y: int = GameConfig.HEIGHT - HEIGHT + 24
    PADDING_X: int = 108
    PADDING_Y: int = 30
    LINE_HEIGHT: int = 24


class PlayerConfig:
    SPRITE_PATH: Path = ASSET_DIR / "player"
    SCALE: float = 0.18
    SPEED: int = 8
    JUMP_VERTICAL_SPEED: int = 30
    # minimal time until switching to the next sprite in sequence
    ANIMATION_INTERVAL_MS: int = 80


class ShadowConfig:
    SPRITE_PATH: Path = ASSET_DIR / "npcs" / "shadow"
    SCALE: float = 0.2
    ANIMATION_INTERVAL_MS: int = 200


@dataclass
class NpcConfig:
    entity_type: EntityType
    scale: float = 0.6
    animation_interval_ms: int = 900
    default_alpha: int = 180  # 255 is fully opaque

    def __post_init__(self):
        with open(
            DATA_DIR / "dialogues" / f"{self.entity_type.name.lower()}.json", encoding="utf-8"
        ) as fin:
            data = json.load(fin)
            self.name = data["name"]
            self.dialogues = data["dialogues"]

        self.sprite_path = ASSET_DIR / "npcs" / self.entity_type.name.lower()


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
