import pygame
from common.types import ActionType
from config import GameConfig

from game_entities.movable_entity import MovableEntity


class Player(MovableEntity):
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
