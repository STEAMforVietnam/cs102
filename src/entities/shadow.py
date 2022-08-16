from __future__ import annotations

import logging
import random
from collections import Sequence
from typing import TYPE_CHECKING

from common.event import GameEvent
from entities.animated_entity import AnimatedEntity

if TYPE_CHECKING:
    from worlds.world import World

logger = logging.getLogger(__name__)


class Shadow(AnimatedEntity):
    """Shadow entity haunting STEAM Valley."""

    def __init__(self, damage, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.damage = damage

        # Shadow may move in a random direction at the start.
        self.move_random()

    def update(self, events: Sequence[GameEvent], world: World) -> None:
        super().update(events, world)

        # Shadow has a probability to change direction.
        rand_move = random.randint(1, 30)
        if rand_move == 1:
            self.move_opposite()
