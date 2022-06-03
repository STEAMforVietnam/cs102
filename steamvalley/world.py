import logging

from config import LevelConfig, TILE_IMGS, GameConfig, TileType, ShadowConfig
from sprites import MovableSprite, BaseSprite

logger = logging.getLogger(__name__)


class World:
    def __init__(self):
        self.tiles = []
        self.abs_screen_offset = 0
        self.level_length = 0

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
                    self.tiles.append(MovableSprite(
                        x=img_x,
                        y=img_y,
                        sprite_dir=ShadowConfig.sprite_dir,
                        scale=ShadowConfig.scale,
                        animation_interval_ms=ShadowConfig.animation_interval_ms,
                    ))
                else:
                    self.tiles.append(BaseSprite(
                        x=img_x,
                        y=img_y,
                        image=TILE_IMGS[tile_type],
                    ))

    def draw(self, screen, screen_offset):
        self.abs_screen_offset += screen_offset
        for tile in self.tiles:
            tile.rect.x += screen_offset
            tile.draw(screen)
