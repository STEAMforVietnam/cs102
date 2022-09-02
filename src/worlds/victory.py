import json
from typing import Sequence

import pygame

from common import util
from common.event import EventType, GameEvent
from common.util import now
from config import DATA_DIR, Color, GameConfig
from worlds.base_scene import BaseScene


class Victory(BaseScene):
    """Show when player won game."""

    BG_MAX_ALPHA = 160
    ROLLING_TEXT_INTERVAL_MS = 19  # how fast the text rolls

    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.created_at_ms: int = now()

        with open(DATA_DIR / "ending_scene.json", encoding="utf-8") as fin:
            data = json.load(fin)
            self.internship_report_text = data["internship_report"]
            self.credit_text = data["credit"]

        self.rolling_i = 0
        self.rolling_j = 0
        self.last_rolling_at = self.created_at_ms

        self.credit_text_alpha = 0

        self.background = util.scale_image(
            pygame.image.load(GameConfig.VICTORY_BACKGROUND).convert(),
            (GameConfig.WIDTH, GameConfig.HEIGHT),
        )
        self.bg_alpha = 0

    def tick(self, events: Sequence[GameEvent]) -> bool:
        super().tick(events)
        self.draw_background()
        if self.draw_internship_report():
            self.draw_credit()
        self.handle_return_to_menu(events)
        return True

    def handle_return_to_menu(self, events: Sequence[GameEvent]):
        now_ms = now()
        if now_ms - self.created_at_ms > 4100:
            for e in events:
                if e.is_key_up(pygame.K_ESCAPE):
                    GameEvent(EventType.SHOW_MENU_AND_RESET_LEVEL_ID).post()

    def draw_background(self):
        self.bg_alpha = min(self.bg_alpha + 0.5, self.BG_MAX_ALPHA)
        self.background.set_alpha(self.bg_alpha)
        self.screen.blit(self.background, (0, 0))

    def draw_internship_report(self) -> bool:
        """
        Gradually roll out the text and return whether the whole text is visible.
        """
        rolling_text = self.internship_report_text
        x, y = 274, 196
        line_height = 45
        for i in range(len(rolling_text)):
            if i < self.rolling_i:
                text = rolling_text[i]  # previous lines
            elif i == self.rolling_i:
                text = rolling_text[i][: self.rolling_j]  # current line
            else:
                break

            util.display_text(
                self.screen,
                text=text,
                x=x,
                y=y + i * line_height,
                font_size=27 if i == 0 else 26,
                color=Color.TEXT_INTERNSHIP_REPORT,
            )

        now_ms = now()
        if now_ms >= self.last_rolling_at + self.ROLLING_TEXT_INTERVAL_MS:
            self.last_rolling_at = now_ms
            self.rolling_j += 1
            if self.rolling_i < len(rolling_text) and self.rolling_j >= len(
                rolling_text[self.rolling_i]
            ):
                self.rolling_i += 1
                self.rolling_j = 0

        return self.rolling_i >= len(rolling_text) and self.rolling_j >= len(rolling_text[-1])

    def draw_credit(self):
        line_height = 38
        self.credit_text_alpha += 1
        for i, line in enumerate(self.credit_text):
            util.display_text(
                self.screen,
                text=line,
                x=345,
                y=510 + i * line_height,
                font_size=22,
                color=Color.TEXT_CREDIT,
                alpha=self.credit_text_alpha,
            )
