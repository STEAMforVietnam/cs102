import enum

import pygame
from pygame import Surface
from pygame.color import Color
from utils import scale_image

SCREEN_WIDTH: int = 1280
SCREEN_HEIGHT: int = 768

WHITE: Color = Color(255, 255, 255)
RED: Color = Color(255, 0, 0)  # Màu Đỏ
BLUE: Color = Color(0, 0, 255)  # Màu Xanh

FPS: int = 30  # Số cảnh mỗi giây (frame per second)

# Fonts
pygame.font.init()
FREESANSBOLD_24 = pygame.font.Font("freesansbold.ttf", 24)
FREESANSBOLD_48 = pygame.font.Font("freesansbold.ttf", 48)

# Hình nền:
BACKGROUND_SPRITE: Surface = pygame.image.load("assets/background.png")
BACKGROUND_SPRITE.set_alpha(128)
BACKGROUND_SPRITE = pygame.transform.scale(BACKGROUND_SPRITE, [SCREEN_WIDTH, SCREEN_HEIGHT])

# Game Entities Sprites
PLAYER_SPRITE: Surface = scale_image(pygame.image.load("assets/player.png"), 0.2)
ROBOT_SPRITE: Surface = scale_image(pygame.image.load("assets/robot.png"), 0.08)
DIAMOND_BLUE_SPRITE: Surface = scale_image(pygame.image.load("assets/diamond_blue.png"), 0.02)
DIAMOND_RED_SPRITE: Surface = scale_image(pygame.image.load("assets/diamond_red.png"), 0.02)
TO_MO_SPRITE: Surface = scale_image(pygame.image.load("assets/to_mo.png"), 0.2)


# Các thể loại vật phẩm
class ItemType(enum.Enum):
    DIAMOND_BLUE = 0
    DIAMOND_RED = 1


class GameStateType(enum.Enum):
    RUNNING = 0
    WON = 1
    LOST = 2
