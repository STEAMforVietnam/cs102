import logging

from config import GameConfig

from game_entities.animated_entity import AnimatedEntity

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class MovableEntity(AnimatedEntity):
    """
    For movable entities such as players, enemies, etc.
    Basic movements: move left, move right, jump.
    """

    def __init__(
        self,
        speed: int,
        vertical_speed: int,
        *args,
        **kwargs,
    ) -> None:
        super().__init__(*args, **kwargs)

        # How fast this subject moves.
        self.speed: int = speed
        self.vertical_speed: int = vertical_speed

        # Amount of delta (change) in position, along the 2 axis.
        self.dx: int = 0
        self.dy: int = 0

        # Tracking the states of this subject
        self.moving_left: bool = False
        self.moving_right: bool = False
        self.is_landed: bool = True

    def update(self):
        self.dx = 0
        if self.moving_left:
            self.dx = - self.speed
        elif self.moving_right:
            self.dx = self.speed
        new_x = self.rect.x + self.dx
        new_y = self.rect.y + self.dy

        # Y-axis obstacle check
        if new_y > 200:
            new_y = 200
            self.dy = 0
            self.is_landed = True

        if not self.is_landed:
            self.dy += GameConfig.GRAVITY

        # X-axis obstacle check
        if new_x < 0:
            new_x = 0
            self.dx = 0

        self.rect.x = new_x
        self.rect.y = new_y
        super().update()

    def move_left(self, enabled=True):
        self.moving_left = enabled

    def move_right(self, enabled=True):
        self.moving_right = enabled

    def jump(self):
        if self.is_landed:
            self.is_landed = False
            self.dy = -self.vertical_speed
