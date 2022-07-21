from __future__ import annotations

from typing import TYPE_CHECKING, Sequence

import pygame

from common import util
from common.event import GameEvent
from config import GameConfig
from game_entities.movable import MovableEntity

if TYPE_CHECKING:
    from worlds.world import World


logger = util.get_logger(__name__)


class Player(MovableEntity):
    """
    The main character controlled by user, can talk / fight NPCs, can interact with in-game objects.
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def update(self, events: Sequence[GameEvent], world: World) -> None:
        super().update(events, world)
        self._handle_events()
        self._update_screen_offset()

    def _handle_events(self):
        """
        This subject is controllable by user, we ask it to move based on keyboard inputs here.
        """
        for event in self.events:
            if event.is_key_down(pygame.K_LEFT, pygame.K_a):
                self.move_left(True)
            elif event.is_key_down(pygame.K_RIGHT, pygame.K_d):
                self.move_right(True)
            elif event.is_key_down(pygame.K_UP, pygame.K_SPACE, pygame.K_w):
                self.jump()
            elif event.is_key_up(pygame.K_LEFT, pygame.K_a):
                self.move_left(False)
            elif event.is_key_up(pygame.K_RIGHT, pygame.K_d):
                self.move_right(False)

    def _update_screen_offset(self):
        """Logics for horizontal world scroll based on player movement"""
        delta_screen_offset = 0

        at_right_edge = self.rect.right >= GameConfig.WIDTH
        at_right_soft_edge = self.rect.right > GameConfig.WIDTH - GameConfig.PLAYER_SOFT_EDGE_WIDTH
        at_left_edge = self.rect.left <= 0
        at_left_soft_edge = self.rect.left < GameConfig.PLAYER_SOFT_EDGE_WIDTH

        if (
            at_left_edge
            or at_right_edge
            or (at_left_soft_edge and not self.world.at_left_most())
            or at_right_soft_edge
        ):
            # Undo player position change (player walks in-place)
            self.rect.x -= self.dx
            delta_screen_offset = -self.dx

        self.world.update_screen_offset(delta_screen_offset)
