from __future__ import annotations

from typing import TYPE_CHECKING, Sequence

import pygame

from common import util
from common.event import GameEvent
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
