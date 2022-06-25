from __future__ import annotations

from typing import Optional

import pygame
import utils
from pygame.surface import Surface

from common import (
    BLUE,
    FREESANSBOLD_24,
    FREESANSBOLD_48,
    RED,
    SCREEN_HEIGHT,
    SCREEN_WIDTH,
    GameState,
)


class BaseEntity:
    def __init__(self, x: int, y: int, image: Surface) -> None:
        self.x = x
        self.y = y
        self.image = image

    def render(self, screen: Surface) -> None:
        screen.blit(self.image, (self.x, self.y))

    def touch(self, other: BaseEntity):
        return utils.overlap(self.x, self.y, self.image, other.x, other.y, other.image)


class Player(BaseEntity):
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


class Robot(BaseEntity):
    def __init__(self, x: int, y: int, image: Surface, x_heading: int, y_heading: int) -> None:
        super().__init__(x, y, image)
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


class GameItem(BaseEntity):
    def __init__(self, x: int, y: int, image: Surface) -> None:
        super().__init__(x, y, image)
        self.hidden = False

    def set_hidden(self):
        self.hidden = True

    def render(self, screen: Surface) -> None:
        if not self.hidden:
            super().render(screen)


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
