from typing import List

from common.types import COLLECTABLE_TILE_TYPES, OBSTACLES_TILE_TYPES, TileType
from config import GameConfig, SceneData, ShadowConfig
from game_entities.base_entity import BaseEntity
from game_entities.movable_entity import MovableEntity


class World:
    """
    Manage and draw the world around Player.
    """

    def __init__(self, tile_images):
        self.tile_images = tile_images
        self.tiles: {int: BaseEntity} = {}
        self.abs_screen_offset = 0
        self.delta_screen_offset = 0

    def add_tile(self, tile: BaseEntity):
        self.tiles[tile.id] = tile

    def remove_tile(self, tile_id: int):
        del self.tiles[tile_id]

    def load_scene(self, scene_id):
        data = SceneData(id=scene_id).data

        for i, row in enumerate(data):
            for j, tile_type in enumerate(row):
                if tile_type == TileType.EMPTY:
                    continue
                x = j * GameConfig.TILE_SIZE
                y = i * GameConfig.TILE_SIZE
                if tile_type == TileType.SHADOW:
                    self.add_tile(
                        MovableEntity(
                            object_type=tile_type,
                            x=x,
                            y=y,
                            sprites_dir=ShadowConfig.sprite_dir,
                            scale=ShadowConfig.scale,
                            animation_interval_ms=ShadowConfig.animation_interval_ms,
                        )
                    )
                else:
                    self.add_tile(
                        BaseEntity(
                            object_type=tile_type,
                            x=x,
                            y=y,
                            image=self.tile_images[tile_type],
                        )
                    )

    def update_screen_offset(self, delta):
        # do not let abs_screen_offset becomes > 0, to prevent overscroll to the left
        new_abs_screen_offset = min(0, self.abs_screen_offset + delta)
        self.delta_screen_offset = new_abs_screen_offset - self.abs_screen_offset
        self.abs_screen_offset = new_abs_screen_offset

    def update(self):
        for tile in self.tiles.values():
            tile.update(self)

    def draw(self, screen):
        for tile in self.tiles.values():
            tile.rect.x += self.delta_screen_offset
            tile.draw(screen)

    def at_left_most(self):
        return self.abs_screen_offset >= 0

    def get_obstacles(self) -> List[BaseEntity]:
        return [tile for tile in self.tiles.values() if tile.object_type in OBSTACLES_TILE_TYPES]

    def get_collectable_tiles(self) -> List[BaseEntity]:
        return [tile for tile in self.tiles.values() if tile.object_type in COLLECTABLE_TILE_TYPES]
