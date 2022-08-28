from __future__ import annotations

import random
from typing import TYPE_CHECKING, Sequence

from common.event import GameEvent
from config import GameConfig
from entities.animated_entity import AnimatedEntity

if TYPE_CHECKING:
    from worlds.world import World


class ShadowAlpha(AnimatedEntity):
    """ShadowAlpha entity haunting STEAM Valley.

    ShadowAlpha does not cause harm and has the alpha (opacity) level varies, become more and more
    visible as the game progresses.
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.set_alpha(int(self.rect.x * 1.2 // GameConfig.TILE_SIZE))
        self.sprite_index = random.randint(0, 7)

    def update(self, events: Sequence[GameEvent], world: World) -> None:
        super().update(events, world)
        self.set_flip_x(world.player.rect.x >= self.rect.x)
