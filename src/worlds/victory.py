from typing import Sequence

from common import util
from common.event import EventType, GameEvent
from common.util import now
from worlds.base_scene import BaseScene


class Victory(BaseScene):
    """Show when player won game."""

    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.created_at_ms: int = now()

    def tick(self, events: Sequence[GameEvent]) -> bool:
        super().tick(events)
        # TODO: clean up, move hardcoded values to configs
        util.display_text(
            self.screen,
            text="Victory!",
            x=200,
            y=200,
            font_size=32,
        )
        now_ms = now()
        if now_ms - self.created_at_ms > 4100:
            GameEvent(EventType.SHOW_MENU_AND_RESET_LEVEL_ID).post()

        return True
