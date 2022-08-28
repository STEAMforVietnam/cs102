import logging
import random

from common import util
from common.event import EventType, GameEvent
from common.types import ActionType, EntityType
from common.util import now
from config import Color, ShadowBossConfig
from entities.bullet import Bullet
from entities.shadow import Shadow

logger = logging.getLogger(__name__)


class ShadowBoss(Shadow):
    """Boss (a large shadow)."""

    HP_BAR_HEIGHT: int = 20
    HP_TEXT_HEIGHT_OFFSET: int = -40

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.initial_hp = ShadowBossConfig.INITIAL_HP
        self.hp = self.initial_hp
        self.recent_action_started_at[ActionType.ANGRY] = now()

    def _update_action(self):
        if self.set_action(
            ActionType.ANGRY,
            duration_ms=ShadowBossConfig.ANGRY_DURATION_MS,
            interval_ms=ShadowBossConfig.ANGRY_INTERVAL_MS,
        ):
            self._get_angry()
        super()._update_action()

    def _get_angry(self):
        for _ in range(10):
            bullet_id = self.world.add_entity(
                EntityType.SHADOW_BULLET,
                self.rect.centerx + random.random() * self.rect.width / 2,
                self.rect.centery + random.random() * self.rect.height / 2,
            )

            bullet: Bullet = self.world.get_entity(bullet_id)
            bullet.move_random()

    def _take_damage(self, damage: int):
        self.hp -= damage
        self.start_hurt(duration_ms=ShadowBossConfig.HURT_DURATION_MS)

    def _handle_get_hit(self):
        bullet: Bullet
        for bullet in self.world.get_entities(EntityType.PLAYER_BULLET):
            if self.collide(bullet):

                # Unlike normal shadow vs. bullet interaction, the boss would absorb the bullet,
                # so we remove the bullet right here.
                self.world.remove_entity(bullet.id)

                self._take_damage(bullet.damage)

                if self.hp <= 0:
                    self.die()

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
                fraction=self.hp / self.initial_hp,
                x=self.rect.x,
                y=self.rect.y - self.HP_BAR_HEIGHT,
                width=self.rect.width,
                height=self.HP_BAR_HEIGHT,
                color=Color.BOSS_HP_BAR,
                margin=4,
            )

    def __del__(self):
        if self.hp <= 0:
            GameEvent(EventType.VICTORY).post()
