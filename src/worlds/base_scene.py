from typing import Sequence

from common import util
from common.event import GameEvent

logger = util.get_logger(__name__)


class BaseScene:
    """Base class to extend when you want a new scene, such as player dies, credit, etc."""

    def __init__(self, screen):
        self.screen = screen

    def tick(self, events: Sequence[GameEvent]) -> bool:
        """Subclasses should override"""
