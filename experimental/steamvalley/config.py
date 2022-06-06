import csv
import enum
import json
from dataclasses import dataclass
from pathlib import Path
from typing import Optional, List, Dict

import pygame
import os

pygame.init()


class GameConfig:
    name: str = "Steam Valley"
    fps: int = 60
    width: int = 1500
    height: int = 768
    dialogue_box_width: int = 780
    dialogue_box_height: int = 80
    dialogue_line_height: int = 24
    gravity: float = 0.5
    tile_size: int = 48
    player_soft_edge_width: int = 300


ASSET_DIR = Path("assets")
BACKGROUND = pygame.transform.scale(
    pygame.image.load(ASSET_DIR / "bg_office.png"),
    (GameConfig.width, GameConfig.height),
)
IMG_BG_DIALOGUE_BOX = pygame.transform.scale(
    pygame.image.load(ASSET_DIR / "bg_dialogue_box.png"),
    (GameConfig.dialogue_box_width + 210, GameConfig.dialogue_box_height + 50),
)
IMG_QUESTION_MARK = pygame.transform.scale(
    pygame.image.load(ASSET_DIR / "items" / "question_mark.png"),
    (30, 35),
)


class Font(enum.Enum):
    FREESANSBOLD_14 = pygame.font.Font("freesansbold.ttf", 14)
    FREESANSBOLD_18 = pygame.font.Font("freesansbold.ttf", 18)
    FREESANSBOLD_24 = pygame.font.Font("freesansbold.ttf", 24)


class Color:
    RED = (255, 0, 0)
    BG_DIALOGUE_BOX = (240, 206, 237)
    TEXT_DIALOGUE_SUBJECT = (19, 2, 150)
    TEXT_DIALOGUE = (204, 115, 14)


INVENTORY_TEXT = (
    Font.FREESANSBOLD_24.value.render("Inventory", True, Color.RED),
    (20, 30),
)


class PlayerConfig:
    sprite_dir: str = "assets/player"
    scale: float = 0.18
    animation_interval_ms: int = 80
    width: int = 100
    height: int = 220
    x0: int = 360
    speed: int = 7  # previously set to 5
    y_speed: int = -15  # previously PLAYER_JUMP_VEL
    starting_health: int = 500


@dataclass
class NpcConfig:
    dialogues: list
    scale: float = 0.07
    default_alpha: int = 180  # 255 is fully opaque


with open("data/npc_quests.json", "r") as fin:
    npc_quests = json.load(fin)
npc_co_nga_config = NpcConfig(dialogues=npc_quests["Cô Nga"])


class ShadowConfig:
    sprite_dir: str = "assets/shadow"
    scale: float = 0.2
    animation_interval_ms: int = 200


class ActionType(enum.Enum):
    IDLE = "idle"
    JUMP = "jump"
    MOVE_LEFT = "move_left"
    MOVE_RIGHT = "move_right"


class TileType(enum.Enum):
    EMPTY = 0
    GROUND = 1
    HEART = 2
    CANDY = 3
    SHADOW = 9
    # Any special tiles with id >= 20 will NOT be scaled to GameConfig.tile_size.
    NPC_CO_NGA = 21
    NPC_B = 22


OBSTACLES_TILE_TYPES = (TileType.GROUND,)
COLLECTABLE_TILE_TYPES = (TileType.HEART, TileType.CANDY)
NPC_TILE_TYPES = (TileType.NPC_CO_NGA, TileType.NPC_B)


def load_tile_img(tile_type: TileType) -> Optional[pygame.Surface]:
    if tile_type == TileType.EMPTY:
        return None
    path = f"assets/tiles/{tile_type.name.lower()}.png"
    image = pygame.image.load(path)
    if tile_type.value < 20:
        image = pygame.transform.scale(
            image, (GameConfig.tile_size, GameConfig.tile_size)
        )
    return image


TILE_IMGS: Dict[TileType, Optional[pygame.Surface]] = {
    tile_type: load_tile_img(tile_type) for tile_type in TileType
}


@dataclass
class LevelConfig:
    id: int = 0
    data_dir: str = "data/levels/"
    data: Optional[List] = None

    def __post_init__(self):
        with open(
            os.path.join(self.data_dir, str(self.id) + ".csv"), newline=""
        ) as csvfile:
            reader = csv.reader(csvfile, delimiter=",")
            self.data = [
                [TileType(int(tile or TileType.EMPTY.value)) for tile in row]
                for row in reader
            ]
