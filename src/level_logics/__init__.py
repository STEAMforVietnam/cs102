"""
Each level may have some custom logics, depending on the game story.

For example, in level 1 we handle when the quest TRAMPOLINE is complete,
or when the Player gets to the end of the level.

Refer to one.py to write your own levels and stories.
"""
from typing import Callable, Optional

from level_logics import one


def get_event_handler(level_id: int) -> Optional[Callable]:
    return {
        1: one.event_handler,
    }.get(level_id)
