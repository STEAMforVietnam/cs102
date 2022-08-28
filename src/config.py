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

    MENU_MUSIC: Path = ASSET_DIR / "sounds" / "background" / "menu.wav"
    MENU_MUSIC_VOLUME: float = 0.12

    BONUS_LEVEL_END_MUSIC: Path = ASSET_DIR / "sounds" / "background" / "victory.wav"
    DEFEATED_MUSIC: Path = ASSET_DIR / "sounds" / "background" / "defeated.wav"

    INGAME_MUSIC_VOLUME: float = 0.05
    SOUND_EFFECT_VOLUME: float = 0.18


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
    DEFAULT_X: int = 350
    DEFAULT_Y: int = 400
    SPRITE_PATH: Path = ASSET_DIR / "player"
    SCALE: float = 0.16
    GRAVITY: int = 2
    SPEED: int = 7
    JUMP_VERTICAL_SPEED: int = 26
    JUMP_WITH_TRAMPOLINE_SPEED: int = 40
    # minimal time until switching to the next sprite in sequence
    ANIMATION_INTERVAL_MS: int = 70 * 60 // GameConfig.FPS
    INITIAL_HP: int = 3
    INVULNERABLE_DURATION_MS: int = 1000

    HURT_DURATION_MS: int = 80 * 4

    # TODO: we have 7 sprites for ActionType.THROW but only use 2-3 now
    THROW_DURATION_MS: int = 170 * 60 // GameConfig.FPS


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


class PlayerBulletConfig:
    SPRITE_PATH: Path = ASSET_DIR / "items" / "player_bullet.png"
    SCALE: float = 0.7
    SPEED: int = 35
    GRAVITY: int = 2
    DAMAGE: int = 10

    # initial vertical movement
    INIT_DY: int = -10

    # the time between creation and deletion of entities of this type
    TTL_MS: int = 400 * 60 // GameConfig.FPS


class ShadowConfig:
    SPRITE_PATH: Path = ASSET_DIR / "npcs" / "shadow"
    SCALE: float = 0.2
    ANIMATION_INTERVAL_MS: int = 200
    SPEED: int = 1
    DAMAGE: int = 1


class ShadowBossConfig:
    SPRITE_PATH: Path = ASSET_DIR / "npcs" / "shadow"
    SCALE: float = 0.6
    ANIMATION_INTERVAL_MS: int = 200
    SPEED: int = 1
    DAMAGE: int = 1
    INITIAL_HP: int = 100

    ANGRY_INTERVAL_MS: int = 7000
    ANGRY_DURATION_MS: int = 2000

    HURT_DURATION_MS: int = 500


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
    ANIMATION_INTERVAL_MS: int = 60
    ANIMATION_DURATION_MS: int = 700


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
