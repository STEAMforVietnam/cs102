from __future__ import annotations

import logging
from typing import TYPE_CHECKING, Sequence

from common.event import GameEvent
from common.types import ActionType
from config import GameConfig
from game_entities.base import BaseEntity

if TYPE_CHECKING:
    from worlds.world import World

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class MovableEntity(BaseEntity):
    """
    For movable entities such as players, enemies, etc.
    Basic movements: move left, move right, jump.
    """

    def __init__(
        self,
        speed: int = 0,
        jump_vertical_speed: int = 0,
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

    def update(self, events: Sequence[GameEvent], world: World) -> None:
        super().update(events, world)
        # Knowing the current state of the subject, we calculate the amount of changes
        # - dx and dy - that should occur to the player position during this current game tick.

        # Step 1: calculate would-be dx, dy when unobstructed
        self.dx = 0
        self.dy += GameConfig.GRAVITY

        if self.moving_left:
            self.dx = -self.speed
        if self.moving_right:
            self.dx = self.speed

        # Step 2: update current position by the deltas
        self.rect.x += self.dx
        self.rect.y += self.dy

        self.is_landed = False

        # Step 3: Use a hardcoded ground (before next lesson)
        if self.rect.bottom >= GameConfig.GROUND_LEVEL:
            self.rect.bottom = GameConfig.GROUND_LEVEL
            self.is_landed = True
            self.dy = 0

        # Depends on the subject current action, tweak the sprite rendering.
        self._update_sprite_state()

    def _update_sprite_state(self):
        # Set the current movement state
        if self.is_landed:
            if self.dx == 0:
                self.sprite.set_action(ActionType.IDLE)
            else:
                self.sprite.set_action(ActionType.MOVE)
        else:
            self.sprite.set_action(ActionType.JUMP)

        # If detected subject is moving left, turn on flip_x
        if self.dx > 0:
            self.sprite.flip_x = False
        elif self.dx < 0:
            self.sprite.flip_x = True

    def move_left(self, enabled=True):
        self.moving_left = enabled

    def move_right(self, enabled=True):
        self.moving_right = enabled

    def jump(self):
        if self.is_landed:
            self.is_landed = False
            self.dy = -self.jump_vertical_speed
