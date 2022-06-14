import enum
from typing import List, Tuple

import pygame
from pygame import Surface
from pygame.color import Color

WIDTH: int = 1280
HEIGHT: int = 768
WHITE: Color = Color(255, 255, 255)
FPS: int = 30  # Số cảnh mỗi giây (frame per second)

pygame.init()
screen: Surface = pygame.display.set_mode([WIDTH, HEIGHT])
clock = pygame.time.Clock()


# Hàm hỗ trợ
def scale_image(image: Surface, scale: float) -> Surface:
    """Resize image by a factor of input arg `scale`."""
    new_dimension: Tuple[int, int] = (
        int(image.get_width() * scale),
        int(image.get_height() * scale),
    )
    return pygame.transform.scale(image, new_dimension)


# Hình nền:
BACKGROUND_SPRITE: Surface = pygame.image.load("assets/background.png").convert_alpha()
BACKGROUND_SPRITE.set_alpha(128)
BACKGROUND_SPRITE = pygame.transform.scale(BACKGROUND_SPRITE, [WIDTH, HEIGHT])

# Game Entities Sprites
PLAYER_SPRITE: Surface = scale_image(pygame.image.load("assets/player.png"), 0.2)
ROBOT_SPRITE: Surface = scale_image(pygame.image.load("assets/robot.png"), 0.08)
DIAMOND_BLUE_SPRITE: Surface = scale_image(pygame.image.load("assets/diamond_blue.png"), 0.02)
DIAMOND_RED_SPRITE: Surface = scale_image(pygame.image.load("assets/diamond_red.png"), 0.02)
TO_MO_SPRITE: Surface = scale_image(pygame.image.load("assets/to_mo.png"), 0.2)


class Player:
    def __init__(self, x: float, y: float) -> None:
        self.x: float = x
        self.y: float = y
        self.image: Surface = PLAYER_SPRITE


class Robot:
    def __init__(self, x: float, y: float) -> None:
        self.x: float = x
        self.y: float = y
        self.image: Surface = ROBOT_SPRITE


class Princess:
    def __init__(self, x: float, y: float) -> None:
        self.x: float = x
        self.y: float = y
        self.image: Surface = TO_MO_SPRITE


class ItemType(enum.Enum):
    DIAMOND_BLUE = 0
    DIAMOND_RED = 1


class GameItem:
    def __init__(self, x: float, y: float, type: ItemType) -> None:
        self.x: float = x
        self.y: float = y
        self.image: Surface

        if type == ItemType.DIAMOND_BLUE:
            self.image = DIAMOND_BLUE_SPRITE
        elif type == ItemType.DIAMOND_RED:
            self.image = DIAMOND_RED_SPRITE


# Game States:
player: Player = Player(350, 200)

list_robot: List[Robot] = [
    Robot(500, 500),
    Robot(50, 50),
    Robot(500, 50),
]

list_item: List[GameItem] = [
    GameItem(600, 500, ItemType.DIAMOND_BLUE),
    GameItem(800, 500, ItemType.DIAMOND_RED),
    GameItem(1000, 400, ItemType.DIAMOND_RED),
]

to_mo: Princess = Princess(1000, 50)

# Bắt đầu game
running: bool = True
while running:
    # Tạo hình nền
    screen.fill(WHITE)

    screen.blit(BACKGROUND_SPRITE, (0, 0))

    # Người chơi có tắt màn hình game chưa
    if pygame.event.peek(pygame.QUIT):
        running = False

    # Vẽ các vật phẩm game
    screen.blit(player.image, (player.x, player.y))

    for robot in list_robot:
        screen.blit(robot.image, (robot.x, robot.y))

    for item in list_item:
        screen.blit(item.image, (item.x, item.y))

    screen.blit(to_mo.image, (to_mo.x, to_mo.y))

    pygame.display.flip()
    clock.tick(FPS)

# Ket thuc game
pygame.quit()
