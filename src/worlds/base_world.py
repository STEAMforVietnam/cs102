from typing import Sequence

from common.event import GameEvent


class BaseWorld:
    """Base class to manage all game entities."""

    def __init__(self, screen):
        self.screen = screen

    def tick(self, events: Sequence[GameEvent]):
        """Subclasses should implement"""
