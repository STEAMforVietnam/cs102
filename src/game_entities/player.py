from typing import Optional, Sequence

import pygame

from common.event import GameEvent
from common.types import ActionType
from config import GameConfig
from game_entities.movable_entity import MovableEntity
from game_entities.world import World


class Player(MovableEntity):
    """
    Extra logics to MovableEntity specific to Player (the user-controllable character).
    """

    def _handle_events(self, events: Sequence[GameEvent]):
        """
        This subject is controllable by user, we ask it to move based on keyboard inputs here.
        """
        for event in events:
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

    def update(self, events: Sequence[GameEvent] = tuple(), world: Optional[World] = None) -> None:
        super().update(events, world)
        self._handle_events(events)

        # Horizontal world scroll based on player movement
        delta_screen_offset = 0

        at_right_edge = self.rect.right >= GameConfig.WIDTH
        at_right_soft_edge = self.rect.right > GameConfig.WIDTH - GameConfig.PLAYER_SOFT_EDGE_WIDTH
        at_left_edge = self.rect.left <= 0
        at_left_soft_edge = self.rect.left < GameConfig.PLAYER_SOFT_EDGE_WIDTH

        if (
            at_left_edge
            or at_right_edge
            or (at_left_soft_edge and not world.at_left_most())
            or at_right_soft_edge
        ):
            # Undo player position change (player walks in-place)
            self.rect.x -= self.dx
            delta_screen_offset = -self.dx

        world.update_screen_offset(delta_screen_offset)

    def draw(self, screen: pygame.Surface) -> None:
        if self.is_landed:
            if self.dx == 0:
                self.set_action(ActionType.IDLE)
            else:
                self.set_action(ActionType.MOVE)
        else:
            self.set_action(ActionType.JUMP)

        if self.dx > 0:
            self.flip_x = False
        elif self.dx < 0:
            self.flip_x = True

        super().draw(screen)

        if GameConfig.DEBUG:
            pygame.draw.rect(screen, (255, 0, 0), self.rect, 1)
