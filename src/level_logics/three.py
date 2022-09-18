from __future__ import annotations

import random
from typing import TYPE_CHECKING, Optional

from common.event import EventType, GameEvent
from common.types import EntityType
from common.util import now
from config import GameConfig
from entities.shadow import Shadow

if TYPE_CHECKING:
    from worlds.world import World

boss_died_at_ms: Optional[int] = None


def event_handler(world: World) -> None:
    """
    Logics for level 3 ending.
    """
    global boss_died_at_ms
    for event in world.events:
        if event.get_sender_type() == EntityType.SHADOW_BOSS and event.is_type(EventType.DIE):
            boss_died_at_ms = now()
            world.set_bg_delta_alpha(-0.8)  # fading the background
            shadow: Shadow
            for shadow in world.get_entities(EntityType.SHADOW):
                shadow.die()

    if boss_died_at_ms is not None:
        for _ in range(2):
            world.add_entity(EntityType.ENDING_BURGER, x=random.randint(0, GameConfig.WIDTH), y=0)

        if now() > boss_died_at_ms + 4300:
            boss_died_at_ms = None
            GameEvent(EventType.VICTORY).post()  # it's time to roll the credits
