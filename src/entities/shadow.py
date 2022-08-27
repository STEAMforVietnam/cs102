from __future__ import annotations

import logging
import random
from typing import TYPE_CHECKING, Sequence

from common.event import GameEvent
from common.types import EntityType
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
        if self.is_dying:
            return

        # Shadow has a probability to change direction.
        rand_move = random.randint(1, 30)
        if rand_move == 1:
            self.move_opposite()

        self._handle_get_hit()

    def die(self):
        super().die()
        self.set_remaining_ttl_ms(self.animation_interval_ms * 6)

    def _handle_get_hit(self):
        for bullet in self.world.get_entities(EntityType.PLAYER_BULLET):
            if self.collide(bullet):
                self.start_hurt(0)  # For Sound effects - skip hurt state
                self.die()

        if self.collide(self.world.player):
            self.die()
