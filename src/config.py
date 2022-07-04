from pathlib import Path

import pygame

pygame.init()


ASSET_DIR = Path("assets")
DATA_DIR = Path("data")


class Font:
    FREESANSBOLD_14 = pygame.font.Font("freesansbold.ttf", 14)
    FREESANSBOLD_18 = pygame.font.Font("freesansbold.ttf", 18)
    FREESANSBOLD_24 = pygame.font.Font("freesansbold.ttf", 24)


class GameConfig:
    DEBUG: bool = False
    NAME: str = "STEAM Valley"
    FPS: int = 60
    WIDTH: int = 1280
    HEIGHT: int = 768
    GRAVITY: int = 2

    BG_OFFICE_PATH: Path = ASSET_DIR / "bg_office_1.png"

    GROUND_LEVEL: int = 730


class PlayerConfig:
    SPRITE_PATH: Path = ASSET_DIR / "player/idle/tm_1.png"
    SCALE: float = 0.18
    SPEED: int = 8
    JUMP_VERTICAL_SPEED: int = 30
    # minimal time until switching to the next sprite in sequence
    ANIMATION_INTERVAL_MS: int = 80
