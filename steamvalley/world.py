import logging

from config import LevelConfig, TILE_IMGS, GameConfig, TileType, ShadowConfig
from sprites import MovableSprite

logger = logging.getLogger(__name__)


class World:
    def __init__(self):
        self.tiles = []
        self.abs_screen_offset = 0
        self.level_length = 0
        self.monsters = []

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
                    self.monsters.append(MovableSprite(
                        x=img_x,
                        y=img_y,
                        sprite_dir=ShadowConfig.sprite_dir,
                        scale=ShadowConfig.scale,
                        animation_interval_ms=ShadowConfig.animation_interval_ms,
                    ))
                else:
                    img = TILE_IMGS[tile_type]
                    img_rect = img.get_rect()
                    img_rect.x = img_x
                    img_rect.y = img_y
                    self.tiles.append((img, img_rect))

    def draw(self, screen, screen_offset):
        self.abs_screen_offset += screen_offset
        for tile in self.tiles:
            tile[1][0] += screen_offset
            screen.blit(tile[0], tile[1])
        for monster in self.monsters:
            monster.rect.x += screen_offset
            monster.draw(screen)
