import pygame

from common.event import EventType, GameEvent
from common.util import get_logger
from scenes.scene_menu import SceneMenu
from scenes.scene_one import SceneOne

logger = get_logger(__name__)


class SceneManager:
    def __init__(self, screen: pygame.Surface):
        self.screen = screen
        self.active_scene = None
        self.scenes = {
            SceneMenu.__name__: SceneMenu(self.screen),
            SceneOne.__name__: SceneOne(self.screen),
        }
        logger.info(f"Initialized scenes: {list(self.scenes.keys())}")

        self.current_game_scene = self.scenes[SceneOne.__name__]
        self.show_menu()

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
                self.resume_game()
            elif e.is_key_up(pygame.K_ESCAPE) and self.in_game():
                self.show_menu()

        # Asking the active scene to process other events
        is_running = self.active_scene.tick(events)
        return is_running

    def in_game(self):
        return type(self.active_scene) in (SceneOne,)

    def show_menu(self):
        self.active_scene = self.scenes[SceneMenu.__name__]

    def resume_game(self):
        self.active_scene = self.current_game_scene
