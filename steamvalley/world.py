import logging
from typing import List

from config import (
    GameConfig,
    LevelConfig,
    TileType,
    ShadowConfig,
    COLLECTABLE_TILE_TYPES,
    TILE_IMGS,
    OBSTACLES_TILE_TYPES,
)
from sprites.base_sprite import BaseSprite
from sprites.movable_sprite import MovableSprite

logger = logging.getLogger(__name__)


class Tile:
    def __init__(self, tile_id: int, tile_type: TileType, sprite: BaseSprite):
        self.id = tile_id
        self.type = tile_type
        self.sprite = sprite


class World:
    def __init__(self):
        self.tiles: {int: BaseSprite} = {}
        self.incremental_tile_id = 0
        self.abs_screen_offset = 0
        self.level_length = 0

    def add_tile(self, tile_type: TileType, sprite: BaseSprite):
        self.incremental_tile_id += 1
        self.tiles[self.incremental_tile_id] = Tile(self.incremental_tile_id, tile_type, sprite)

    def remove_tile(self, tile_id: int):
        del self.tiles[tile_id]

    def load_level(self, level_id):
        level = LevelConfig(id=level_id)
        self.level_length = len(level.data[0])

        for y, row in enumerate(level.data):
            for x, tile_type in enumerate(row):
                if tile_type == TileType.EMPTY:
                    continue
                img_x = x * GameConfig.tile_size
                img_y = y * GameConfig.tile_size
                if tile_type == TileType.SHADOW:
                    self.add_tile(
                        tile_type,
                        MovableSprite(
                            x=img_x,
                            y=img_y,
                            sprite_dir=ShadowConfig.sprite_dir,
                            scale=ShadowConfig.scale,
                            animation_interval_ms=ShadowConfig.animation_interval_ms,
                        ),
                    )
                else:
                    self.add_tile(
                        tile_type,
                        BaseSprite(
                            x=img_x,
                            y=img_y,
                            image=TILE_IMGS[tile_type],
                        ),
                    )

    def draw(self, screen, screen_offset):
        self.abs_screen_offset += screen_offset
        for tile in self.tiles.values():
            tile.sprite.rect.x += screen_offset
            tile.sprite.draw(screen)

    def get_obstacle_tiles(self) -> List[Tile]:
        return [tile for tile in self.tiles.values() if tile.type in OBSTACLES_TILE_TYPES]

    def get_collectable_tiles(self) -> List[Tile]:
        return [tile for tile in self.tiles.values() if tile.type in COLLECTABLE_TILE_TYPES]
