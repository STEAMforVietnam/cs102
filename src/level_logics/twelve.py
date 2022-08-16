from __future__ import annotations

from typing import TYPE_CHECKING

from common import util
from common.event import EventType, GameEvent
from common.types import COLLECTABLE_TYPES

if TYPE_CHECKING:
    from worlds.world import World

logger = util.get_logger(__name__)


def event_handler(world: World) -> None:
    """
    Logics for ending bonus level 12.
    """
    needed_items_cnt = 19
    if world.player.count_inventory(COLLECTABLE_TYPES) >= needed_items_cnt:
        world.player.discard_inventory(COLLECTABLE_TYPES)
        logger.info("Ending Level 12")
        GameEvent(EventType.LEVEL_END).post()
