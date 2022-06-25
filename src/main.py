import enum
from typing import List, Optional, Tuple

import pygame
from pygame import Color
from pygame.surface import Surface

pygame.init()

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


# Hàm tiện ích (utility)
def scale_image(image: Surface, scale: float) -> Surface:
    """Resizes image by a factor of input arg `scale`."""
    new_dimension: Tuple[int, int] = (
        int(image.get_width() * scale),
        int(image.get_height() * scale),
    )
    return pygame.transform.scale(image, new_dimension)


# Game Entities Sprites
PLAYER_SPRITE: Surface = scale_image(pygame.image.load("assets/player.png"), 0.2)
ROBOT_SPRITE: Surface = scale_image(pygame.image.load("assets/robot.png"), 0.08)
DIAMOND_BLUE_SPRITE: Surface = scale_image(pygame.image.load("assets/diamond_blue.png"), 0.02)
DIAMOND_RED_SPRITE: Surface = scale_image(pygame.image.load("assets/diamond_red.png"), 0.02)
TO_MO_SPRITE: Surface = scale_image(pygame.image.load("assets/to_mo.png"), 0.2)


# Hàm tiện ích (utility)
def overlap(x1: int, y1: int, image1: Surface, x2: int, y2: int, image2: Surface) -> bool:
    """Returns True if 2 items overlap."""
    mask1 = pygame.mask.from_surface(image1)
    mask2 = pygame.mask.from_surface(image2)
    offset_x = x2 - x1
    offset_y = y2 - y1
    return bool(mask1.overlap(mask2, (offset_x, offset_y)))


class EntityType(enum.Enum):
    PLAYER = enum.auto()
    ROBOT = enum.auto()
    DIAMOND_BLUE = enum.auto()
    DIAMOND_RED = enum.auto()


class GameState(enum.Enum):
    RUNNING = enum.auto()
    WON = enum.auto()
    LOST = enum.auto()


class Player:
    def __init__(self, x: int, y: int, image: Surface) -> None:
        self.x = x
        self.y = y
        self.image = image

    def _move(self, dx: int, dy: int):
        new_x = self.x + dx
        new_y = self.y + dy

        if 0 < new_x < SCREEN_WIDTH - self.image.get_width():
            self.x = new_x
        if 0 < new_y < SCREEN_HEIGHT - self.image.get_height():
            self.y = new_y

    def update(self) -> None:
        pressed = pygame.key.get_pressed()
        if pressed[pygame.K_UP] or pressed[pygame.K_w]:
            self._move(0, -10)
        if pressed[pygame.K_DOWN] or pressed[pygame.K_s]:
            self._move(0, 10)
        if pressed[pygame.K_LEFT] or pressed[pygame.K_a]:
            self._move(-10, 0)
        if pressed[pygame.K_RIGHT] or pressed[pygame.K_d]:
            self._move(10, 0)

    def render(self, screen: Surface) -> None:
        screen.blit(self.image, (self.x, self.y))


class Robot:
    def __init__(self, x: int, y: int, image: Surface, x_heading: int, y_heading: int) -> None:
        self.x = x
        self.y = y
        self.image = image
        self.x_heading = x_heading
        self.y_heading = y_heading

    def update(self):
        self.x = self.x + self.x_heading
        self.y = self.y + self.y_heading

        if self.x > SCREEN_WIDTH - self.image.get_width():
            self.x_heading = -self.x_heading
        if self.x < 0:
            self.x_heading = -self.x_heading
        if self.y > SCREEN_HEIGHT - self.image.get_height():
            self.y_heading = -self.y_heading
        if self.y < 0:
            self.y_heading = -self.y_heading

    def render(self, screen: Surface) -> None:
        screen.blit(self.image, (self.x, self.y))


class NPC:
    def __init__(self, x: int, y: int, image: Surface) -> None:
        self.x = x
        self.y = y
        self.image = image

    def render(self, screen: Surface) -> None:
        screen.blit(self.image, (self.x, self.y))


class GameItem:
    def __init__(self, x: int, y: int, image: Surface) -> None:
        self.x = x
        self.y = y
        self.image = image
        self.hidden = False

    def set_hidden(self):
        self.hidden = True

    def render(self, screen: Surface) -> None:
        if not self.hidden:
            screen.blit(self.image, (self.x, self.y))


class GameStatus:
    def __init__(self) -> None:
        self.score: int = 0
        self.state: GameState = GameState.RUNNING

    def update_state(self, state: GameState) -> None:
        self.state = state

    def update_score(self, delta: int) -> None:
        self.score += delta

    def render(self, screen: Surface) -> None:
        # Score Text Render on Top Left Corner
        score_text = FREESANSBOLD_24.render("Score: %d" % self.score, True, BLUE)
        screen.blit(score_text, (10, 10))

        # Status Text Render in Middle of Screen
        status_text = None
        if self.state == GameState.WON:
            status_text = FREESANSBOLD_48.render("YOU WON!!", True, RED)
        elif self.state == GameState.LOST:
            status_text = FREESANSBOLD_48.render("YOU LOST!!", True, RED)

        if status_text:
            position = (
                SCREEN_WIDTH // 2 - status_text.get_width() // 2,
                SCREEN_HEIGHT // 2 - status_text.get_height() // 2,
            )

            screen.blit(status_text, position)

    def is_running(self):
        return self.state == GameState.RUNNING


screen: Surface = pygame.display.set_mode([SCREEN_WIDTH, SCREEN_HEIGHT])
clock = pygame.time.Clock()

# Khởi tạo (initialize) game entities
player: Player = Player(350, 200, PLAYER_SPRITE)

list_robot: List[Robot] = [
    Robot(500, 500, ROBOT_SPRITE, 1, 1),
    Robot(50, 50, ROBOT_SPRITE, -2, 2),
    Robot(500, 50, ROBOT_SPRITE, 3, 5),
]

list_item: List[GameItem] = [
    GameItem(600, 500, DIAMOND_BLUE_SPRITE),
    GameItem(800, 500, DIAMOND_RED_SPRITE),
    GameItem(1000, 400, DIAMOND_RED_SPRITE),
]

to_mo: NPC = NPC(1000, 50, TO_MO_SPRITE)

# Bắt đầu game
status: GameStatus = GameStatus()

running: bool = True
while running:
    # Người chơi có tắt màn hình game chưa
    if pygame.event.peek(pygame.QUIT):
        running = False
        break

    # ----------------------------------------
    if status.is_running():
        player.update()

        for robot in list_robot:
            robot.update()

        for item in list_item:
            if not item.hidden:
                if overlap(player.x, player.y, player.image, item.x, item.y, item.image):
                    item.set_hidden()
                    status.update_score(delta=1)  # increase score

        for robot in list_robot:
            if overlap(player.x, player.y, player.image, robot.x, robot.y, robot.image):
                print("YOU LOST!!")
                status.update_state(GameState.LOST)

        if overlap(player.x, player.y, player.image, to_mo.x, to_mo.y, to_mo.image):
            print("YOU WON!!")
            status.update_state(GameState.WON)

    # ----------------------------------------
    # Vẽ các vật phẩm game
    screen.fill(WHITE)
    screen.blit(BACKGROUND_SPRITE, (0, 0))

    player.render(screen)

    for robot in list_robot:
        robot.render(screen)

    for item in list_item:
        item.render(screen)

    to_mo.render(screen)

    status.render(screen)

    pygame.display.flip()
    clock.tick(FPS)

# Kết thúc game
pygame.quit()
