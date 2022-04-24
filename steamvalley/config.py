import enum
from collections import UserDict
from dataclasses import dataclass
from pathlib import Path

import pygame
import os

pygame.init()


RED = (255, 0, 0)


@dataclass
class GameConfig:
    name: str = "Steam Valley"
    fps: int = 60
    width: int = 1500
    height: int = 750
    gravity: float = 0.5


BACKGROUND = pygame.transform.scale(pygame.image.load(os.path.join("assets", "background.png")),
                                    (GameConfig.width, GameConfig.height))


class Font(enum.Enum):
    FREESANSBOLD_24 = pygame.font.Font("freesansbold.ttf", 24)


INVENTORY_TEXT = (Font.FREESANSBOLD_24.value.render("Inventory", True, RED), (20, 30))


@dataclass
class PlayerConfig:
    starting_health: int = 500
    animation_time: int = 80
    width: int = 100
    height: int = 220
    scale: int = 0.2
    x0: int = 30
    sprite_dir: str = "assets/player"
    speed: int = 5
    y_speed: int = -15  # previously PLAYER_JUMP_VEL


class ActionType(enum.Enum):
    IDLE = "idle"
    JUMP = "jump"
    MOVE_LEFT = "move_left"
    MOVE_RIGHT = "move_right"


class ItemType(enum.Enum):
    RED = "red"
    BLUE = "blue"


class ItemImages(UserDict):
    def __init__(self, asset_dir):
        super().__init__()
        for image_file in Path(asset_dir).iterdir():
            super().__setitem__(
                ItemType(image_file.stem),
                pygame.transform.scale(pygame.image.load(str(image_file)), (50, 50)))


ITEM_IMAGES = ItemImages("assets/items")
