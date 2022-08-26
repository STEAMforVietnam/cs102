import logging

from common import util
from config import Color, ShadowBossConfig
from entities.shadow import Shadow

logger = logging.getLogger(__name__)


class ShadowBoss(Shadow):
    """Boss (a large shadow)."""

    HP_BAR_HEIGHT: int = 20
    HP_TEXT_HEIGHT_OFFSET: int = -40

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.hp = ShadowBossConfig.INITIAL_HP

    def render(self, screen, *args, **kwargs) -> None:
        super().render(screen, *args, **kwargs)

        # Render boss HP
        if self.hp > 0:
            util.display_text(
                screen,
                f"{self.hp} / 100",
                x=self.rect.x,
                y=self.rect.top + self.HP_TEXT_HEIGHT_OFFSET,
                color=Color.BOSS_HP_BAR,
            )

            util.draw_pct_bar(
                screen,
                fraction=self.hp / ShadowBossConfig.INITIAL_HP,
                x=self.rect.x,
                y=self.rect.y - self.HP_BAR_HEIGHT,
                width=self.rect.width,
                height=self.HP_BAR_HEIGHT,
                color=Color.BOSS_HP_BAR,
                margin=4,
            )
