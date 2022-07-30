from __future__ import annotations

from typing import TYPE_CHECKING, Optional, Sequence

from common import util
from common.event import EventType, GameEvent
from common.types import EntityType
from config import GameConfig, NpcConfig
from game_entities.base import BaseEntity

if TYPE_CHECKING:
    from worlds.world import World

logger = util.get_logger(__name__)


class FriendlyNpc(BaseEntity):
    """
    Non-playable character, will talk and interact with Player.
    """

    def __init__(self, npc_config, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Shift position up to above the ground tile, since Npc is taller than standard tile size.
        self.rect.bottom = self.rect.y + GameConfig.TILE_SIZE

        self.npc_config: NpcConfig = npc_config
        self.is_near_player: bool = False
        self.question_mark_id: Optional[int] = None
        self.dialogue_box_id: Optional[int] = None

    def update(self, events: Sequence[GameEvent], world: World) -> None:
        super().update(events, world)
        self._handle_events()
        if self.is_near_player:
            self._highlight()
        else:
            self._unhightlight()

    def _handle_events(self):
        self.is_near_player = False
        for event in self.events:
            # Handle events specifically sent to this NPC
            if not event.get_listener_id() == self.id:
                continue
            if event.is_type(EventType.PLAYER_NEAR_NPC):
                self.is_near_player = True
            elif event.is_type(EventType.PLAYER_ACTIVATE_NPC):
                self._activate()

    def _highlight(self):
        if not self.question_mark_id:
            self.question_mark_id = self.world.add_entity(EntityType.QUESTION_MARK)
            new_entity = self.world.get_entity(self.question_mark_id)
            new_entity.rect.centerx = self.rect.centerx
            new_entity.rect.y = self.rect.y - 80

    def _unhightlight(self):
        if self.question_mark_id:
            self.world.remove_entity(self.question_mark_id)
            self.question_mark_id = None

    def _activate(self):
        """
        Manipulates the dialogue box entity.
        """
        logger.info("NPC Activated")
        if not self.dialogue_box_id:
            self.dialogue_box_id = self.world.add_entity(EntityType.DIALOGUE_BOX)
        dialogue_box = self.world.get_entity(self.dialogue_box_id)
        dialogue_box.sprite.set_text("Xin chào!")
