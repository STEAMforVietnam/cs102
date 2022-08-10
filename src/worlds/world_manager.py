import pygame
from pygame.surface import Surface

from common.event import EventType, GameEvent
from common.util import get_logger
from worlds.menu import Menu
from worlds.world import World

logger = get_logger(__name__)


class WorldManager:
    WORLD_MENU = "menu"
    WORLD_GAME = "game"

    def __init__(self, screen: Surface):
        self.screen = screen
        self.level_id = None
        self.worlds = {
            self.WORLD_MENU: Menu(self.screen, can_resume=False),
            self.WORLD_GAME: None,
        }
        self.active_world = self.WORLD_MENU

    def tick(self) -> bool:
        if pygame.event.peek(pygame.QUIT):
            return False

        # Get all events from the Event queue
        pg_events = pygame.event.get()

        # We want a nicer interface that works with both pygame native event types and
        # our custom types defined in common/event.py, so from the pygame events we create
        # our own GameEvent objects.
        events = list(map(GameEvent, pg_events))

        # Process generic game events first
        for e in events:
            if e.is_type(EventType.START_GAME):
                self.start_or_resume_game(level_id=e.event.level_id, force_start=True)
            elif e.is_type(EventType.RESTART_LEVEL):
                self.start_or_resume_game(level_id=self.level_id, force_start=True)
            elif e.is_type(EventType.RESUME_GAME):
                self.start_or_resume_game(level_id=self.level_id, force_start=False)
            elif e.is_type(EventType.LEVEL_END):
                self.start_or_resume_game(level_id=self.level_id + 1)
            elif e.is_key_up(pygame.K_ESCAPE) and self.active_world == self.WORLD_GAME:
                self.active_world = self.WORLD_MENU

        # Asking the active world to process other events
        is_running = self.worlds[self.active_world].tick(events)
        return is_running

    def start_or_resume_game(self, level_id: int, force_start: bool):
        self.active_world = self.WORLD_GAME
        if force_start or not self.worlds[self.active_world] or level_id != self.level_id:
            logger.info(f"Current level: {self.level_id} -> (Re)starting level: {level_id}")
            self.level_id = level_id
            self.worlds[self.active_world] = World(self.screen, level_id=level_id)

            # TODO: this could be optimized instead of initiating a new Menu instance somehow?
            self.worlds[self.WORLD_MENU] = Menu(self.screen, can_resume=True)
