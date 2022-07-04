from typing import Sequence

import pygame
from pygame.surface import Surface

from common.event import GameEvent
from common.types import EntityType
from config import GameConfig, PlayerConfig
from game_entities.player import Player
from gui.animated_sprite import AnimatedSprite
from worlds.base_world import BaseWorld


class World(BaseWorld):
    """The in-game world.

    This class manages all game entities in self.player and self.entities.
    """

    def __init__(self, screen: Surface) -> None:
        super().__init__(screen)
        self.background = pygame.transform.scale(
            pygame.image.load(GameConfig.BG_OFFICE_PATH),
            (GameConfig.WIDTH, GameConfig.HEIGHT),
        )

        self.player = Player(
            entity_type=EntityType.PLAYER,
            speed=PlayerConfig.SPEED,
            jump_vertical_speed=PlayerConfig.JUMP_VERTICAL_SPEED,
            sprite=AnimatedSprite(
                x=350,
                y=200,
                sprite_path=PlayerConfig.SPRITE_PATH,
                scale=PlayerConfig.SCALE,
                animation_interval_ms=PlayerConfig.ANIMATION_INTERVAL_MS,
            ),
        )

    def tick(self, events: Sequence[GameEvent]) -> bool:
        if pygame.event.peek(pygame.QUIT):
            return False

        self.screen.blit(self.background, (0, 0))

        self.update(events)

        self.render(self.screen)

        return True

    def update(self, events):
        self.player.update(events, self)

    def render(self, screen):
        self.player.sprite.render(screen)
