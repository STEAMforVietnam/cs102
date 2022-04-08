import enum
import os
from dataclasses import dataclass

import pygame


RED = (255, 0, 0)

@dataclass
class GameConfig:
  fps: int = 60
  width: int = 1500
  height: int = 750
  gravity: float = 0.5


BACKGROUND = pygame.transform.scale(pygame.image.load(os.path.join("assets", "background.png")),
                                    (GameConfig.width, GameConfig.height))

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
