import pygame

from common.types import ActionType
from game_entities.movable_entity import MovableEntity


class Player(MovableEntity):
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
