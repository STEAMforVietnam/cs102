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
        *args,
        **kwargs,
    ) -> None:
        super().__init__(*args, **kwargs)

        # How fast this subject moves.
        self.speed: int = speed

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

       

    def move_left(self, enabled=True):
        self.moving_left = enabled

    def move_right(self, enabled=True):
        self.moving_right = enabled
