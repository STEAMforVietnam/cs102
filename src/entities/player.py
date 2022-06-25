import pygame
from entities.base_entity import BaseEntity

from common import SCREEN_HEIGHT, SCREEN_WIDTH


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
