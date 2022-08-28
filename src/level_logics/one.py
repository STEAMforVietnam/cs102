from __future__ import annotations

from typing import TYPE_CHECKING

from common.event import EventType, GameEvent
from common.types import TRAMPOLINE_PART_TYPES, EntityType, QuestName

if TYPE_CHECKING:
    from worlds.world import World


def event_handler(world: World) -> None:
    """
    Logics for some specific events in level 1.
    """
    for event in world.events:
        npc_chu_nhan_id = world.get_entity_id_by_type(EntityType.NPC_CHU_NHAN)
        npc_chu_nam_id = world.get_entity_id_by_type(EntityType.NPC_CHU_NAM)

        # After talking to this NPC (the last NPC in level 1), level 1 should end.
        if event.get_sender_id() == npc_chu_nhan_id and event.is_type(EventType.NPC_DIALOGUE_END):
            GameEvent(EventType.LEVEL_END).post()

        # Player finishes TRAMPOLINE quest.
        elif (
            event.get_sender_id() == npc_chu_nam_id
            and event.is_type(EventType.NPC_DIALOGUE_END)
            and world.player.count_inventory(TRAMPOLINE_PART_TYPES) >= 4
        ):
            GameEvent(
                EventType.QUEST_END,
                listener_id=npc_chu_nam_id,
                quest_name=QuestName.TRAMPOLINE,
            ).post()

            world.player.discard_inventory(TRAMPOLINE_PART_TYPES)

            # NPC makes the trampoline
            npc = world.get_entity(npc_chu_nam_id)
            world.add_entity(
                EntityType.TRAMPOLINE,
                npc.rect.x + 76,
                npc.rect.y + 156,
            )
