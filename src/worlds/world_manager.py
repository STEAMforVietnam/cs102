import pygame

from common.event import GameEvent
from common.util import get_logger
from worlds.world import World

logger = get_logger(__name__)


class WorldManager:
    def __init__(self, screen: pygame.Surface):
        self.screen = screen
        self.active_world = World(self.screen)
        logger.info("Initialized WorldManager")

    def tick(self) -> bool:
        if pygame.event.peek(pygame.QUIT):
            return False

        # Get all events from the Event queue
        pg_events = pygame.event.get()

        # We want a nicer interface that works with both pygame native event types and
        # our custom types defined in common/event.py, so from the pygame events we create
        # our own GameEvent objects.
        events = list(map(GameEvent, pg_events))

        # Asking the active world to process events
        is_running = self.active_world.tick(events)
        return is_running
