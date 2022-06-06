import logging
from typing import List

import util
from config import (
    COLLECTABLE_TILE_TYPES,
    TILE_IMGS,
    OBSTACLES_TILE_TYPES,
    NPC_TILE_TYPES,
    GameConfig,
    LevelConfig,
    TileType,
    ShadowConfig,
    npc_co_nga_config,
)
from sprites.base_sprite import BaseSprite
from sprites.movable_sprite import MovableSprite
from sprites.npc import Npc

logger = logging.getLogger(__name__)


class World:
    def __init__(self):
        self.tiles: {int: BaseSprite} = {}
        self.incremental_tile_id = 0
        self.abs_screen_offset = 0
        self.level_length = 0

    def add_tile(self, tile: BaseSprite):
        self.tiles[tile.id] = tile

    def remove_tile(self, tile_id: int):
        del self.tiles[tile_id]

    def load_level(self, level_id):
        level = LevelConfig(id=level_id)
        self.level_length = len(level.data[0])

        for i, row in enumerate(level.data):
            for j, tile_type in enumerate(row):
                if tile_type == TileType.EMPTY:
                    continue
                x = j * GameConfig.tile_size
                y = i * GameConfig.tile_size
                if tile_type == TileType.SHADOW:
                    self.add_tile(
                        MovableSprite(
                            object_type=tile_type,
                            x=x,
                            y=y,
                            sprite_dir=ShadowConfig.sprite_dir,
                            scale=ShadowConfig.scale,
                            animation_interval_ms=ShadowConfig.animation_interval_ms,
                        )
                    )
                elif tile_type == TileType.NPC_CO_NGA:
                    npc = Npc(
                        npc_config=npc_co_nga_config,
                        object_type=tile_type,
                        x=x,
                        y=y,
                        image=util.scale_image(
                            TILE_IMGS[tile_type], npc_co_nga_config.scale
                        ),
                    )
                    # Adjust vertical placement of large size NPCs
                    npc.rect.y -= npc.image.get_height() - GameConfig.tile_size
                    self.add_tile(npc)
                else:
                    self.add_tile(
                        BaseSprite(
                            object_type=tile_type,
                            x=x,
                            y=y,
                            image=TILE_IMGS[tile_type],
                        )
                    )

    def draw(self, screen, screen_offset):
        self.abs_screen_offset += screen_offset
        for tile in self.tiles.values():
            tile.rect.x += screen_offset
            tile.draw(screen)

    def get_obstacles(self) -> List[BaseSprite]:
        return [
            tile
            for tile in self.tiles.values()
            if tile.object_type in OBSTACLES_TILE_TYPES
        ]

    def get_collectable_tiles(self) -> List[BaseSprite]:
        return [
            tile
            for tile in self.tiles.values()
            if tile.object_type in COLLECTABLE_TILE_TYPES
        ]

    def get_npcs(self) -> List[BaseSprite]:
        return [
            tile for tile in self.tiles.values() if tile.object_type in NPC_TILE_TYPES
        ]

    def get_npc_ids(self) -> List[int]:
        return [
            tile.id
            for tile in self.tiles.values()
            if tile.object_type in NPC_TILE_TYPES
        ]
