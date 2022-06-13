import enum
from typing import List, Tuple

import pygame
from pygame import Surface
from pygame.color import Color

WIDTH: int = 1280
HEIGHT: int = 768

WHITE: Color = Color(255, 255, 255)
YELLOW: Color = Color(255, 255, 0)  # Màu Vàng
RED: Color = Color(255, 0, 0)  # Màu Đỏ
GREEN: Color = Color(0, 255, 0)  # Màu Xanh

FPS: int = 30  # Số cảnh mỗi giây (frame per second)

pygame.init()

# Fonts
FREESANSBOLD_24 = pygame.font.Font("freesansbold.ttf", 24)
FREESANSBOLD_48 = pygame.font.Font("freesansbold.ttf", 48)

screen: Surface = pygame.display.set_mode([WIDTH, HEIGHT])
clock = pygame.time.Clock()


def scale_image(image: Surface, scale: float) -> Surface:
    # Calculate new Width & Height
    new_dimension: Tuple[int, int] = (
        image.get_width() * scale,
        image.get_height() * scale,
    )
    image = pygame.transform.scale(image, new_dimension)
    return image


# Hình nền:
BACKGROUND_SPRITE: Surface = pygame.image.load("assets/background.png").convert_alpha()
BACKGROUND_SPRITE.set_alpha(128)
BACKGROUND_SPRITE = pygame.transform.scale(BACKGROUND_SPRITE, [WIDTH, HEIGHT])

# Game objects Sprites
PLAYER_SPRITE: Surface = scale_image(pygame.image.load("assets/player.png"), 0.2)
SHADOW_SPRITE: Surface = scale_image(pygame.image.load("assets/shadow.png"), 0.3)
DIAMOND_BLUE_SPRITE: Surface = scale_image(pygame.image.load("assets/diamond_blue.png"), 0.03)
DIAMOND_RED_SPRITE: Surface = scale_image(pygame.image.load("assets/diamond_red.png"), 0.03)
TO_MO_SPRITE: Surface = scale_image(pygame.image.load("assets/to_mo.png"), 0.2)


class Player:
    def __init__(self, x: float, y: float) -> None:
        self.x: float = x
        self.y: float = y
        self.image: Surface = PLAYER_SPRITE

    def move(self, change_x: int, change_y: int):
        new_x = self.x + change_x
        new_y = self.y + change_y

        if new_x > 0 and new_x < WIDTH - self.image.get_width():
            self.x = new_x
        if new_y > 0 and new_y < HEIGHT - self.image.get_height():
            self.y = new_y


class Shadow:
    def __init__(self, x: float, y: float, x_heading: float, y_heading: float) -> None:
        self.x: float = x
        self.y: float = y
        self.image: Surface = SHADOW_SPRITE
        self.x_heading: float = x_heading
        self.y_heading: float = y_heading

    def move(self):
        self.x = self.x + self.x_heading
        self.y = self.y + self.y_heading

        if self.x > WIDTH - self.image.get_width():
            self.x_heading = -self.x_heading
        if self.x < 0:
            self.x_heading = -self.x_heading
        if self.y > HEIGHT - self.image.get_height():
            self.y_heading = -self.y_heading
        if self.y < 0:
            self.y_heading = -self.y_heading


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
        self.type = type
        self.name: str

        if type == ItemType.DIAMOND_BLUE:
            self.name = "Kim Cuong Xanh"
            self.image = DIAMOND_BLUE_SPRITE
        elif type == ItemType.DIAMOND_RED:
            self.name = "Kim Cuong Do"
            self.image = DIAMOND_RED_SPRITE


# Utils:
def overlap(x1: float, y1: float, image1: Surface, x2: float, y2: float, image2: Surface) -> bool:
    mask1 = pygame.mask.from_surface(image1)
    mask2 = pygame.mask.from_surface(image2)
    offset_x = x2 - x1
    offset_y = y2 - y1
    if mask1.overlap(mask2, (offset_x, offset_y)):
        return True
    else:
        return False


# Game States:
player: Player = Player(350, 200)

list_shadow: List[Shadow] = [
    Shadow(500, 500, 1, 1),
    Shadow(50, 50, -2, 2),
    Shadow(500, 50, 3, 5),
]

list_item: List[GameItem] = [
    GameItem(600, 500, ItemType.DIAMOND_BLUE),
    GameItem(800, 500, ItemType.DIAMOND_RED),
    GameItem(1000, 400, ItemType.DIAMOND_RED),
]
score: int = 0

to_mo: Princess = Princess(1000, 50)

# Bắt đầu game
running: bool = True
end_game: bool = False
is_win: bool = False
while running:
    # Tạo hình nền
    screen.fill(WHITE)

    screen.blit(BACKGROUND_SPRITE, (0, 0))

    # Người chơi có tắt màn hình game chưa
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # ----------------------------------------
    if not end_game:
        pressed = pygame.key.get_pressed()
        if pressed[pygame.K_UP] or pressed[pygame.K_w]:
            player.move(0, -10)
        if pressed[pygame.K_DOWN] or pressed[pygame.K_s]:
            player.move(0, 10)
        if pressed[pygame.K_LEFT] or pressed[pygame.K_a]:
            player.move(-10, 0)
        if pressed[pygame.K_RIGHT] or pressed[pygame.K_d]:
            player.move(10, 0)

        for shadow in list_shadow:
            shadow.move()

        # Check Game State
        new_list_item: GameItem = []
        for item in list_item:
            if overlap(player.x, player.y, player.image, item.x, item.y, item.image):
                print("COLLECTED %s" % item.name)
                score += 1
            else:
                new_list_item.append(item)
        list_item = new_list_item

        for shadow in list_shadow:
            if overlap(player.x, player.y, player.image, shadow.x, shadow.y, shadow.image):
                print("YOU LOST!!")
                is_win = False
                end_game = True

        if overlap(player.x, player.y, player.image, to_mo.x, to_mo.y, to_mo.image):
            print("YOU WIN!!")
            is_win = True
            end_game = True

    # ----------------------------------------
    # Vẽ các vật phẩm game
    screen.blit(player.image, (player.x, player.y))

    for shadow in list_shadow:
        screen.blit(shadow.image, (shadow.x, shadow.y))

    for item in list_item:
        screen.blit(item.image, (item.x, item.y))

    screen.blit(to_mo.image, (to_mo.x, to_mo.y))

    # Ve Text:
    score_text: Surface = FREESANSBOLD_24.render("Score: %d" % score, True, YELLOW)
    screen.blit(score_text, (10, 10))

    if end_game:
        status_text: Surface
        if is_win:
            status_text = FREESANSBOLD_48.render("YOU WON!!", True, RED)
        else:
            status_text = FREESANSBOLD_48.render("YOU LOST!!", True, RED)

        position = (
            WIDTH / 2 - status_text.get_width() / 2,
            HEIGHT / 2 - status_text.get_height() / 2,
        )
        screen.blit(status_text, position)

    pygame.display.flip()
    clock.tick(FPS)

# Ket thuc game
pygame.quit()
