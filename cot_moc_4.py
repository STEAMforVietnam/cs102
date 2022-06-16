import enum
from typing import List, Tuple

import pygame
from pygame import Surface
from pygame.color import Color

SCREEN_WIDTH: int = 1280
SCREEN_HEIGHT: int = 768

WHITE: Color = Color(255, 255, 255)
RED: Color = Color(255, 0, 0)  # Màu Đỏ
BLUE: Color = Color(0, 0, 255)  # Màu Xanh

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

# Fonts
FREESANSBOLD_24 = pygame.font.Font("freesansbold.ttf", 24)
FREESANSBOLD_48 = pygame.font.Font("freesansbold.ttf", 48)


class Player:
    def __init__(self, x: float, y: float) -> None:
        self.x: float = x
        self.y: float = y
        self.image: Surface = PLAYER_SPRITE

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
    def __init__(self, x: float, y: float, x_heading: float, y_heading: float) -> None:
        self.x: float = x
        self.y: float = y
        self.image: Surface = ROBOT_SPRITE
        self.x_heading: float = x_heading
        self.y_heading: float = y_heading

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
        self.type = type
        self.name: str
        self.hidden = False

        if type == ItemType.DIAMOND_BLUE:
            self.name = "Kim Cuong Xanh"
            self.image = DIAMOND_BLUE_SPRITE
        elif type == ItemType.DIAMOND_RED:
            self.name = "Kim Cuong Do"
            self.image = DIAMOND_RED_SPRITE

    def set_hidden(self):
        self.hidden = True

    def render(self, screen: Surface) -> None:
        if not self.hidden:
            screen.blit(self.image, (self.x, self.y))


class GameStateType(enum.Enum):
    RUNNING = 0
    WON = 1
    LOST = 2


class GameState:
    def __init__(self, score: int) -> None:
        # State
        self.state: GameStateType = None
        self.score: int = None
        self.status_text: Surface = None
        self.score_text: Surface = None

        # Init
        self.update_score(score)
        self.update_state(GameStateType.RUNNING)

    def update_state(self, state: GameStateType) -> None:
        self.state = state

        if self.state == GameStateType.WON:
            self.status_text = FREESANSBOLD_48.render("YOU WON!!", True, RED)
        elif self.state == GameStateType.LOST:
            self.status_text = FREESANSBOLD_48.render("YOU LOST!!", True, RED)
        elif self.state == GameStateType.RUNNING:
            self.status_text = None

    def update_score(self, score: int) -> None:
        self.score = score
        self.score_text: Surface = FREESANSBOLD_24.render("Score: %d" % score, True, BLUE)

    def render(self, screen: Surface) -> None:
        # Score Text Render on Top Left Corner
        if self.score_text:
            screen.blit(self.score_text, (10, 10))

        # Status Text Render in Middle of Screen
        if self.status_text:
            position = (
                SCREEN_WIDTH // 2 - self.status_text.get_width() // 2,
                SCREEN_HEIGHT // 2 - self.status_text.get_height() // 2,
            )

            screen.blit(self.status_text, position)


# Hàm hỗ trợ
def overlap(x1: float, y1: float, image1: Surface, x2: float, y2: float, image2: Surface) -> bool:
    """Returns True if 2 items overlap."""
    mask1 = pygame.mask.from_surface(image1)
    mask2 = pygame.mask.from_surface(image2)
    offset_x = x2 - x1
    offset_y = y2 - y1
    return bool(mask1.overlap(mask2, (offset_x, offset_y)))


# Game States:
player: Player = Player(350, 200)

list_robot: List[Robot] = [
    Robot(500, 500, 1, 1),
    Robot(50, 50, -2, 2),
    Robot(500, 50, 3, 5),
]

list_item: List[GameItem] = [
    GameItem(600, 500, ItemType.DIAMOND_BLUE),
    GameItem(800, 500, ItemType.DIAMOND_RED),
    GameItem(1000, 400, ItemType.DIAMOND_RED),
]

to_mo: NPC = NPC(1000, 50)

# Bắt đầu game
game_state: GameState = GameState(score=0)

running: bool = True
while running:
    # Người chơi có tắt màn hình game chưa
    if pygame.event.peek(pygame.QUIT):
        running = False
        break

    # ----------------------------------------
    if game_state.state == GameStateType.RUNNING:
        player.update()

        for robot in list_robot:
            robot.update()

        for item in list_item:
            if not item.hidden:
                if overlap(player.x, player.y, player.image, item.x, item.y, item.image):
                    item.set_hidden()
                    # Increase Score
                    new_score: int = game_state.score + 1
                    game_state.update_score(new_score)

        for robot in list_robot:
            if overlap(player.x, player.y, player.image, robot.x, robot.y, robot.image):
                print("YOU LOST!!")
                game_state.update_state(GameStateType.LOST)

        if overlap(player.x, player.y, player.image, to_mo.x, to_mo.y, to_mo.image):
            print("YOU WON!!")
            game_state.update_state(GameStateType.WON)

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

    game_state.render(screen)

    pygame.display.flip()
    clock.tick(FPS)

# Ket thuc game
pygame.quit()
