import csv
import json
from dataclasses import dataclass
from pathlib import Path
from typing import List, Optional, Tuple

import pygame

from common.types import EntityType

pygame.init()
pygame.mixer.init()

ASSET_DIR = Path("assets")
DATA_DIR = Path("data")

FONT_PATH = ASSET_DIR / "fonts" / "arial.ttf"


class Color:
    DEFAULT = (0, 0, 255)
    BLACK = (0, 0, 0)
    WHITE = (255, 255, 255)
    LOADING_BAR = (255, 51, 153)
    BOSS_HP_BAR = (255, 51, 153)
    TEXT_DIALOGUE_SUBJECT = (19, 2, 150)
    TEXT_DIALOGUE = (204, 115, 14)
    TEXT_INVENTORY_CNT = (255, 255, 0)


class GameConfig:
    DEBUG: bool = True
    NAME: str = "STEAM Valley"
    FPS: int = 60
    WIDTH: int = 1248
    HEIGHT: int = 768
    TILE_SIZE: int = 48
    PLAYER_SOFT_EDGE_WIDTH: int = 300

    BG_LOADING: Path = ASSET_DIR / "black.png"


class LevelLoadingBarConfig:
    WIDTH: int = 600
    HEIGHT: int = 100
    STEP = 3 if not GameConfig.DEBUG else 10  # how fast the loading bar goes


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
    STEP_SOUND_PATH: Path = ASSET_DIR / "sound" / "step_sound.wav"
    JUMP_SOUND_PATH: Path = ASSET_DIR / "sound" / "jump_sound.wav"
    STEP_SOUND = pygame.mixer.Sound(STEP_SOUND_PATH)
    JUMP_SOUND = pygame.mixer.Sound(JUMP_SOUND_PATH)
    SCALE: float = 0.18
    GRAVITY: int = 2
    SPEED: int = 8
    JUMP_VERTICAL_SPEED: int = 30
    JUMP_WITH_TRAMPOLINE_SPEED: int = 40
    # minimal time until switching to the next sprite in sequence
    ANIMATION_INTERVAL_MS: int = 80
    INITIAL_HP: int = 3


class PlayerHpConfig:
    X: int = 10
    Y: int = 30
    X_STEP: int = 60  # distance between 2 consecutive hearts
    FULL_HEART_PATH: Path = ASSET_DIR / "items" / "full_heart.png"
    EMPTY_HEART_PATH: Path = ASSET_DIR / "items" / "empty_heart.png"


class PlayerInventoryConfig:
    X: int = 290
    Y: int = 30
    X_STEP: int = 60  # distance between 2 consecutive items

    # the simple vertical divider
    SPRITE_PATH: Path = ASSET_DIR / "items" / "player_inventory.png"
    SCALE: int = 1

    TILE_SIZE: int = 34


class ShadowConfig:
    SPRITE_PATH: Path = ASSET_DIR / "npcs" / "shadow"
    SCALE: float = 0.2
    ANIMATION_INTERVAL_MS: int = 200
    SPEED: int = 1
    DAMAGE: int = 1


class ShadowBulletConfig:
    SPRITE_PATH: Path = ASSET_DIR / "items" / "shadow_bullet.png"
    SCALE: float = 0.05
    SPEED: int = 5
    GRAVITY: int = 0.3
    DAMAGE: int = 1

    # initial vertical movement
    INIT_DY: int = -15

    # the time between creation and deletion of entities of this type
    TTL_MS: int = 3000


class TrampolineConfig:
    SPRITE_PATH: Path = ASSET_DIR / "items" / "trampoline"
    SCALE: float = 0.3
    ANIMATION_INTERVAL_MS: int = 200


@dataclass
class NpcConfig:
    entity_type: EntityType
    scale: float = 0.6
    animation_interval_ms: int = 2500
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
    bg_path: Optional[Path] = None

    def __post_init__(self):
        self.bg_path = ASSET_DIR / "backgrounds" / f"level_{self.level_id}.png"
        with open(DATA_DIR / "levels" / f"{self.level_id}.csv", newline="") as csvfile:
            reader = csv.reader(csvfile, delimiter=",")
            self.data = [
                [EntityType(int(tile or EntityType.EMPTY.value)) for tile in row] for row in reader
            ]
