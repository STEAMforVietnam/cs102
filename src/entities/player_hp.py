import pygame

from common.types import EntityType
from config import PlayerConfig, PlayerHpConfig
from entities.base_entity import BaseEntity


class PlayerHp(BaseEntity):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.max_hp: int = PlayerConfig.INITIAL_HP
        self.hp: int
        self.full_heart = BaseEntity(
            entity_type=EntityType.HP_HEART, x=0, y=0, sprite_path=PlayerHpConfig.FULL_HEART_PATH
        )
        self.empty_heart = BaseEntity(
            entity_type=EntityType.HP_HEART, x=0, y=0, sprite_path=PlayerHpConfig.EMPTY_HEART_PATH
        )

    def set_hp(self, max_hp: int, hp: int):
        """Set the backend data, called by Player."""
        self.max_hp = max_hp
        self.hp = hp

    def render(
        self,
        screen: pygame.Surface,
        *args,
        **kwargs,
    ) -> None:
        x = PlayerHpConfig.X
        y = PlayerHpConfig.Y
        for i in range(self.hp):
            x += PlayerHpConfig.X_STEP
            self.full_heart.render(screen, x_y=(x, y))
        for i in range(self.hp, self.max_hp):
            x += PlayerHpConfig.X_STEP
            self.empty_heart.render(screen, x_y=(x, y))
