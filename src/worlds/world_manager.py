import pygame
from pygame.surface import Surface

from common.event import EventType, GameEvent
from common.sound import handle_music_events, load_music, play_sounds
from common.types import EntityType
from common.util import get_logger
from config import GameConfig
from worlds.bonus_level_end import BonusLevelEnd
from worlds.defeated import Defeated
from worlds.menu import Menu
from worlds.victory import Victory
from worlds.world import World

logger = get_logger(__name__)


class WorldManager:
    def __init__(self, screen: Surface):
        self.screen = screen
        self.level_id = None
        self.worlds = {
            Menu.__name__: Menu(self.screen, can_resume=False),
            World.__name__: None,
        }
        self.active_world = Menu.__name__
        self.sound_on = True
        load_music(GameConfig.MENU_MUSIC, GameConfig.MENU_MUSIC_VOLUME, play=self.sound_on)

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
                self.start_or_resume_game(e.get_level_id(), force_start=True)

            elif e.is_type(EventType.RESTART_LEVEL):
                GameEvent(EventType.START_GAME, level_id=self.level_id).post()

            elif e.is_type(EventType.RESUME_GAME):
                self.start_or_resume_game(self.level_id, force_start=False)

            elif e.is_type(EventType.SHOW_MENU_AND_RESET_LEVEL_ID):
                self.active_world = Menu.__name__
                self.level_id = None
                self.worlds[Menu.__name__] = Menu(self.screen, can_resume=False)

            elif e.is_type(EventType.LEVEL_END):
                e.event.level_id = self.level_id
                if self.level_id < 10:
                    # Player finishes a main story level, go to next level
                    GameEvent(EventType.START_GAME, level_id=self.level_id + 1).post()
                else:
                    # Player finishes a bonus level, show a congrats screen
                    self.start_scene(BonusLevelEnd)

            elif e.is_type(EventType.DIE) and e.get_sender_type() == EntityType.PLAYER:
                logger.info("Player is dead!")
                self.start_scene(Defeated)

            elif e.is_type(EventType.VICTORY):
                logger.info("Game ENDED!")
                self.start_scene(Victory)

            elif e.is_type(EventType.TOGGLE_SOUND):
                self.toggle_sound()

            elif e.is_key_up(pygame.K_ESCAPE) and self.active_world in (
                Menu.__name__,
                World.__name__,
            ):
                self.toggle_menu()

        # Only play sound effects when we are not in muted mode.
        if self.sound_on:
            play_sounds(events)

        # Unlike sound effects, we do want to load the specific level music
        # when some level start / end event happens, regardless whether we are muted or not.
        #   Unmute: load and play
        #   Mute: load only
        handle_music_events(events, self.sound_on)

        # Asking the active world to process other events
        is_running = self.worlds[self.active_world].tick(events)
        return is_running

    def start_or_resume_game(self, level_id: int, force_start: bool):
        self.active_world = World.__name__
        if force_start or not self.worlds[self.active_world] or level_id != self.level_id:
            logger.info(f"Current level: {self.level_id} -> (Re)starting level: {level_id}")
            self.level_id = level_id
            self.worlds[self.active_world] = World(self.screen, level_id=level_id)

            # TODO: this could be optimized instead of initiating a new Menu instance somehow?
            self.worlds[Menu.__name__] = Menu(self.screen, can_resume=True)

    def start_scene(self, scene_class):
        logger.info(f"Starting scene: {scene_class.__name__}")
        self.worlds.update({scene_class.__name__: scene_class(self.screen)})
        self.active_world = scene_class.__name__

    def toggle_menu(self):
        if self.active_world == World.__name__:
            self.active_world = Menu.__name__
        else:
            if self.level_id:
                self.start_or_resume_game(self.level_id, force_start=False)

    def toggle_sound(self):
        self.sound_on = not self.sound_on
        if self.sound_on:
            logger.info("Unpausing Music")
            pygame.mixer.music.unpause()
        else:
            if pygame.mixer.music.get_busy():
                logger.info("Pausing Music")
                pygame.mixer.music.pause()
