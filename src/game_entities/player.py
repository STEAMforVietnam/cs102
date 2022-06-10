from typing import Optional

import pygame

from common.types import ActionType
from config import GameConfig
from game_entities.movable_entity import MovableEntity
from game_entities.world import World


class Player(MovableEntity):
    """
    Extra logics to MovableEntity specific to Player (the user-controllable character).
    """

    def update(self, world: Optional[World] = None) -> None:
        super().update(world)

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

    def draw(self, screen: pygame.Surface, debug=False) -> None:
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

        if debug:
            pygame.draw.rect(screen, (255, 0, 0), self.rect, 1)
