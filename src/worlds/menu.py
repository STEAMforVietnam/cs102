from functools import partial
from typing import Sequence

import pygame
import pygame_menu
from pygame.surface import Surface

from common.event import EventType, GameEvent
from config import GameConfig
from worlds.base_world import BaseWorld


def start_game(level_id: int):
    GameEvent(EventType.START_GAME, level_id=level_id).post()


class Menu(BaseWorld):
    """The menu page."""

    def __init__(self, screen: Surface, can_resume: bool) -> None:
        super().__init__(screen)
        self.can_resume = can_resume
        self.menu = pygame_menu.Menu(
            GameConfig.NAME,
            GameConfig.WIDTH,
            GameConfig.HEIGHT,
            theme=pygame_menu.themes.THEME_SOLARIZED,
        )

        frame = self.menu.add.frame_v(GameConfig.WIDTH - 700, GameConfig.HEIGHT - 400)
        if not self.can_resume:
            frame.pack(self.menu.add.button("Play", partial(start_game, level_id=1)))
        else:
            frame.pack(self.menu.add.button("Resume", GameEvent(EventType.RESUME_GAME).post))
            frame.pack(
                self.menu.add.button("Restart Level", GameEvent(EventType.RESTART_LEVEL).post)
            )

        frame.pack(self.menu.add.button("Quit", lambda: GameEvent(pygame.QUIT).post()))

    def tick(self, events: Sequence[GameEvent]) -> bool:
        if self.menu.is_enabled():
            self.menu.update([e.event for e in events])
            self.menu.draw(self.screen)
        return True
