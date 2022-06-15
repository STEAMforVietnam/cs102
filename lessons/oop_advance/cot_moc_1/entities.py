import pygame
from pygame import Surface

from common import (
    BLUE,
    DIAMOND_BLUE_SPRITE,
    DIAMOND_RED_SPRITE,
    FREESANSBOLD_24,
    FREESANSBOLD_48,
    PLAYER_SPRITE,
    RED,
    ROBOT_SPRITE,
    SCREEN_HEIGHT,
    SCREEN_WIDTH,
    TO_MO_SPRITE,
    GameStateType,
    ItemType,
)


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
