import csv
import enum
from dataclasses import dataclass
from typing import Optional, List

import pygame
import os

pygame.init()


RED = (255, 0, 0)


class GameConfig:
    name: str = "Steam Valley"
    fps: int = 60
    width: int = 1500
    height: int = 768
    gravity: float = 0.5
    tile_size: int = 48
    player_soft_edge_width: int = 300


BACKGROUND = pygame.transform.scale(pygame.image.load(os.path.join("assets", "bg_office.png")),
                                    (GameConfig.width, GameConfig.height))


class Font(enum.Enum):
    FREESANSBOLD_24 = pygame.font.Font("freesansbold.ttf", 24)


INVENTORY_TEXT = (Font.FREESANSBOLD_24.value.render("Inventory", True, RED), (20, 30))


class PlayerConfig:
    sprite_dir: str = "assets/player"
    scale: float = 0.2
    animation_interval_ms: int = 80
    width: int = 100
    height: int = 220
    x0: int = 360
    speed: int = 7  # previously set to 5
    y_speed: int = -15  # previously PLAYER_JUMP_VEL
    starting_health: int = 500


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
    SHADOW = 3


OBSTACLES_TILE_TYPES = (TileType.GROUND,)


def load_tile_img(path):
  img = pygame.image.load(path)
  img = pygame.transform.scale(img, (GameConfig.tile_size, GameConfig.tile_size))
  return img


TILE_IMGS = {
    tile_type: load_tile_img(f"assets/tiles/{tile_type.name.lower()}.png")
    for tile_type in TileType if tile_type != TileType.EMPTY
}


@dataclass
class LevelConfig:
  id: int = 0
  data_dir: str = "data/levels/"
  data: Optional[List] = None

  def __post_init__(self):
    with open(os.path.join(self.data_dir, str(self.id) + ".csv"), newline="") as csvfile:
      reader = csv.reader(csvfile, delimiter=",")
      self.data = [[TileType(int(tile or TileType.EMPTY.value)) for tile in row]
                   for row in reader]