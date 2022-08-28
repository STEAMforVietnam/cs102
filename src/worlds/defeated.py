from typing import Sequence

from common import util
from common.event import EventType, GameEvent
from common.util import now
from worlds.base_scene import BaseScene


class Defeated(BaseScene):
    """Show when player dies."""

    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.created_at_ms: int = now()

    def tick(self, events: Sequence[GameEvent]) -> bool:
        super().tick(events)
        # TODO: clean up, move hardcoded values to configs
        util.display_text(
            self.screen,
            text="You died!",
            x=200,
            y=200,
            font_size=32,
        )
        now_ms = now()
        if now_ms - self.created_at_ms > 1800:
            util.display_text(self.screen, text="Restarting level ...", x=200, y=300, font_size=32)
        if now_ms - self.created_at_ms > 4100:
            GameEvent(EventType.RESTART_LEVEL).post()
        return True
