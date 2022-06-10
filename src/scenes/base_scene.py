from typing import Sequence

from common.event import GameEvent


class BaseScene:
    """Base class for all scenes."""

    def __init__(self, screen):
        self.screen = screen

    def tick(self, events: Sequence[GameEvent]):
        """Subclasses should implement"""
