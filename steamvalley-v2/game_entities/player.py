import pygame
from common.types import ActionType

from game_entities.movable_sprite import MovableSprite


class Player(MovableSprite):
    def __init__(
        self,
        x: int,
        y: int,
        default_action: ActionType = ActionType.IDLE,
        flip_x: bool = False
    ):
        super().__init__(
            x= x,
            y= y,
            sprites_dir= "assets/player",
            default_action= default_action,
            flip_x= flip_x
        )
        self.speed_x = 0
        self.speed_y = 0

        self.is_landed = True

    def update(self):
        new_x = self.rect.x + self.speed_x
        new_y = self.rect.y + self.speed_y

        # Y-axis obstacle check
        if new_y > 200:
            new_y = 200
            self.speed_y = 0
            self.is_landed = True
        
        if not self.is_landed:
            self.speed_y += 2 # gravity pulling down
        
        # X-axis obstacle check
        if new_x < 0:
            new_x = 0
            self.speed_x = 0

        self.rect.x = new_x
        self.rect.y = new_y
        super().update()

    def draw(self, screen: pygame.Surface) -> None:
        if self.is_landed:
            if self.speed_x == 0:
                self.set_action(ActionType.IDLE)
            else:
                self.set_action(ActionType.MOVE)
        else:
            self.set_action(ActionType.JUMP)

        if self.speed_x > 0:
            self.flip_x = False
        elif self.speed_x < 0:
            self.flip_x = True

        super().draw(screen)

    def move_left(self, enabled=True):
        if enabled:
            self.speed_x = -10
        else:
            self.speed_x = 0

    def move_right(self, enabled=True):
        if enabled:
            self.speed_x = 10
        else:
            self.speed_x = 0

    def jump(self):
        if self.is_landed:
            self.is_landed = False
            self.speed_y = -20
