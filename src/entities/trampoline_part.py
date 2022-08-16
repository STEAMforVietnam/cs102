from __future__ import annotations

from typing import TYPE_CHECKING, Sequence

from common.event import EventType, GameEvent
from common.types import QuestName
from entities.base_entity import BaseEntity

if TYPE_CHECKING:
    from worlds.world import World


class TrampolinePart(BaseEntity):
    """
    Trampoline parts that can be picked up to give to an NPC.
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.set_active(False)

    def update(self, events: Sequence[GameEvent], world: World):
        """
        Turn on sprite visibility when the TRAMPOLINE quest starts.
        """
        super().update(events, world)
        for e in self.events:
            if e.is_type(EventType.QUEST_START) and e.event.quest_name == QuestName.TRAMPOLINE:
                self.set_active(True)
