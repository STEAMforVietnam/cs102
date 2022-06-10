from typing import Dict, Optional, Sequence

import pygame

from common.event import GameEvent
from common.types import TileType
from common.util import load_tile_img
from config import GameConfig, PlayerConfig
from game_entities.player import Player
from game_entities.world import World
from scenes.base_scene import BaseScene


class SceneOne(BaseScene):
    """First playing scene in the game."""

    def __init__(self, screen: pygame.Surface) -> None:
        super().__init__(screen)
        self.background = pygame.transform.scale(
            pygame.image.load(GameConfig.SCENE_ONE_BG_IMG_PATH),
            (GameConfig.WIDTH, GameConfig.HEIGHT),
        )

        # These tile images will be used to create Entities (using BaseEntity or its subclass)
        # in World, that later get drawn on the game screen.
        tile_images: Dict[TileType, Optional[pygame.Surface]] = {
            tile_type: load_tile_img(tile_type) for tile_type in TileType
        }
        self.world = World(tile_images)
        self.world.load_scene(1)

        # TODO: load player position from level data
        self.player = Player(
            x=350,
            y=200,
            sprites_dir=PlayerConfig.SPRITES_DIR,
            scale=PlayerConfig.SCALE,
            speed=PlayerConfig.SPEED,
            jump_vertical_speed=PlayerConfig.JUMP_VERTICAL_SPEED,
            animation_interval_ms=PlayerConfig.ANIMATION_INTERVAL_MS,
        )

    def tick(self, events: Sequence[GameEvent]) -> bool:
        self.screen.blit(self.background, (0, 0))

        # Game logic
        self.world.update(events)
        self.player.update(events, self.world)

        # Draw
        self.world.draw(self.screen)
        self.player.draw(self.screen)

        return True
