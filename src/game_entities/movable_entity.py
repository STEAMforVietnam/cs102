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
        jump_vertical_speed: int,
        *args,
        **kwargs,
    ) -> None:
        super().__init__(*args, **kwargs)

        # How fast this subject moves.
        self.speed: int = speed
        self.jump_vertical_speed: int = jump_vertical_speed

        # Amount of delta (change) in position, along the 2 axis.
        self.dx: int = 0
        self.dy: int = 0

        # Tracking the states of this subject
        self.moving_left: bool = False
        self.moving_right: bool = False
        self.is_landed: bool = False  # Let object fall to stable position

    def update(self, ground_tiles=[]):
        # Calculate Ideal dx dy
        dx = 0
        dy = 0

        if self.moving_left:
            dx = -self.speed

        if self.moving_right:
            dx = self.speed

        dy = self.dy + GameConfig.GRAVITY

        # dx, dy in obstacle condition
        for obstacle in ground_tiles:
            if obstacle.rect.colliderect(
                self.rect.x + dx, self.rect.y, self.rect.width, self.rect.height
            ):
                dx = 0
            if obstacle.rect.colliderect(
                self.rect.x, self.rect.y + dy, self.rect.width, self.rect.height
            ):
                if self.dy < 0:
                    self.dy = 0
                    dy = (
                        obstacle.rect.bottom - self.rect.top
                    )  # the gap between player's head and obstacle above
                else:
                    self.dy = 0
                    self.is_landed = True
                    dy = (
                        obstacle.rect.top - self.rect.bottom
                    )  # the gap between player's feet and ground

        # Update position & speed state
        self.rect.x += dx
        self.rect.y += dy
        self.dx = dx
        self.dy = dy

        # Restrict absolute world x, y coordinate
        if self.rect.y > GameConfig.HEIGHT - self.rect.height:
            self.rect.y = GameConfig.HEIGHT - self.rect.height
            self.dy = 0
            self.is_landed = True

        if self.rect.x < 0:
            self.rect.x = 0
            self.dx = 0
        if self.rect.x > GameConfig.WIDTH - self.rect.width:
            self.rect.x = GameConfig.WIDTH - self.rect.width
            self.dx = 0

        super().update()

    def move_left(self, enabled=True):
        self.moving_left = enabled

    def move_right(self, enabled=True):
        self.moving_right = enabled

    def jump(self):
        if self.is_landed:
            self.is_landed = False
            self.dy = -self.jump_vertical_speed
