import enum
from typing import List, Tuple

import pygame
from pygame import Surface
from pygame.color import Color

SCREEN_WIDTH: int = 1280
SCREEN_HEIGHT: int = 768
WHITE: Color = Color(255, 255, 255)
FPS: int = 30  # Số cảnh mỗi giây (frame per second)

pygame.init()
screen: Surface = pygame.display.set_mode([SCREEN_WIDTH, SCREEN_HEIGHT])
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
BACKGROUND_SPRITE = pygame.transform.scale(BACKGROUND_SPRITE, [SCREEN_WIDTH, SCREEN_HEIGHT])

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

    def render(self, screen: Surface) -> None:
        screen.blit(self.image, (self.x, self.y))


class Robot:
    def __init__(self, x: float, y: float) -> None:
        self.x: float = x
        self.y: float = y
        self.image: Surface = ROBOT_SPRITE

    def render(self, screen: Surface) -> None:
        screen.blit(self.image, (self.x, self.y))


class NPC:
    def __init__(self, x: float, y: float) -> None:
        self.x: float = x
        self.y: float = y
        self.image: Surface = TO_MO_SPRITE

    def render(self, screen: Surface) -> None:
        screen.blit(self.image, (self.x, self.y))


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

    def render(self, screen: Surface) -> None:
        screen.blit(self.image, (self.x, self.y))


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

to_mo: NPC = NPC(1000, 50)

# Bắt đầu game
running: bool = True
while running:
    # Người chơi có tắt màn hình game chưa
    if pygame.event.peek(pygame.QUIT):
        running = False
        break

    # Vẽ các vật phẩm game
    screen.fill(WHITE)
    screen.blit(BACKGROUND_SPRITE, (0, 0))

    player.render(screen)

    for robot in list_robot:
        robot.render(screen)

    for item in list_item:
        item.render(screen)

    to_mo.render(screen)

    pygame.display.flip()
    clock.tick(FPS)

# Ket thuc game
pygame.quit()
