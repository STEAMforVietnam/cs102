from typing import Sequence

import pygame
import pygame_menu

from common.event import EventType, GameEvent
from config import GameConfig
from scenes.base_scene import BaseScene


class SceneMenu(BaseScene):
    """Draw the menu and listen to user inputs."""

    def __init__(self, screen: pygame.Surface) -> None:
        super().__init__(screen)
        self.menu = pygame_menu.Menu(
            GameConfig.NAME,
            GameConfig.WIDTH,
            GameConfig.HEIGHT,
            theme=pygame_menu.themes.THEME_SOLARIZED,
        )
        self.menu.add.button("PLAY", lambda: GameEvent(EventType.START_GAME).post())
        self.menu.add.button("QUIT", lambda: GameEvent(pygame.QUIT).post())

    def tick(self, events: Sequence[GameEvent]) -> bool:
        if self.menu.is_enabled():
            self.menu.update([e.event for e in events])
            self.menu.draw(self.screen)
        return True
