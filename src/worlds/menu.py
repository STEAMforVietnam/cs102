from functools import partial
from typing import Sequence

import pygame
import pygame_menu
from pygame.surface import Surface

from common import util
from common.event import EventType, GameEvent
from config import GameConfig
from worlds.base_scene import BaseScene


def start_game(level_id: int):
    GameEvent(EventType.START_GAME, level_id=level_id).post()


class Menu(BaseScene):
    """The menu page."""

    def __init__(self, screen: Surface, can_resume: bool, *args, **kwargs) -> None:
        super().__init__(screen, *args, **kwargs)

        self.can_resume = can_resume
        self.menu = pygame_menu.Menu(
            GameConfig.NAME,
            GameConfig.WIDTH,
            GameConfig.HEIGHT,
            theme=pygame_menu.themes.THEME_SOLARIZED,
        )

        frame = self.menu.add.frame_v(1000, 580)
        if not self.can_resume:
            frame.pack(self.menu.add.button("Play", partial(start_game, level_id=1)))
        else:
            frame.pack(self.menu.add.button("Resume", GameEvent(EventType.RESUME_GAME).post))
            frame.pack(
                self.menu.add.button("Restart Level", GameEvent(EventType.RESTART_LEVEL).post)
            )

        available_level_ids = util.get_available_level_ids()
        if GameConfig.DEBUG:
            for level_id in available_level_ids:
                if 1 < level_id < 10:
                    frame.pack(
                        self.menu.add.button(
                            f"[dev-mode] Play Level {level_id}",
                            partial(start_game, level_id),
                        )
                    )

        extra_level_ids = [level_id for level_id in available_level_ids if level_id >= 10]
        frame.pack(
            self.menu.add.dropselect(
                title="Play Extra Levels",
                items=[(str(level_id), level_id) for level_id in extra_level_ids],
                selection_option_font_size=20,
                onreturn=lambda a, _b: GameEvent(EventType.START_GAME, level_id=a[0][1]).post(),
            )
        )

        frame.pack(self.menu.add.button("Mute / Unmute", GameEvent(EventType.TOGGLE_SOUND).post))
        frame.pack(self.menu.add.button("Quit", lambda: GameEvent(pygame.QUIT).post()))

    def tick(self, events: Sequence[GameEvent]) -> bool:
        super().tick(events)
        if self.menu.is_enabled():
            self.menu.update([e.event for e in events])
            self.menu.draw(self.screen)
        return True
