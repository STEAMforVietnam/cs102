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

        self.dialogues = self.npc_config.dialogues
        self.dialogue_index: int = 0
        self.line_index: int = -1

    def update(self, events: Sequence[GameEvent], world: World) -> None:
        super().update(events, world)
        self._handle_events()
        if self.has_dialogue() and self.is_near_player:
            self._highlight()
        else:
            self._unhightlight()

    def has_dialogue(self) -> bool:
        return self.dialogues and self.dialogues[-1] and self.dialogue_index < len(self.dialogues)

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
        next_line = self._get_next_line()
        if not next_line:
            GameEvent(EventType.NPC_DIALOGUE_END, sender_id=self.id).post()
            if self.dialogue_box_id:
                self.world.remove_entity(self.dialogue_box_id)
                self.dialogue_box_id = None
            return

        if not self.dialogue_box_id:
            self.dialogue_box_id = self.world.add_entity(EntityType.DIALOGUE_BOX)
        dialogue_box = self.world.get_entity(self.dialogue_box_id)
        dialogue_box.sprite.set_text(next_line)

    def _get_next_line(self) -> Optional[str]:
        """
        Returns the next line in the current dialogue or None.
        """
        self.line_index += 1
        if self.line_index >= len(self.dialogues[self.dialogue_index]):
            # Prepare to move on to the next dialogue,
            # return None to indicate current dialogue has ended.
            self.line_index = -1
            self.dialogue_index += 1
            return None
        if not self.has_dialogue():
            return None
        line = self.dialogues[self.dialogue_index][self.line_index]
        return "\n".join((line["Subject"], line["Line"]))
