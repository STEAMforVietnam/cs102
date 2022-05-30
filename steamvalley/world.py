import logging

from config import ItemType, LevelConfig, TILE_IMGS, GameConfig, TileType
from sprites import CollectableItem

logger = logging.getLogger(__name__)

class World:
    def __init__(self):
        self.tiles = []
        self.obstacles = []
        self.collectable_items = []
        self.abs_screen_offset = 0
        self.level_length = 0

    # def load_level(self, level_id):
    #     # TODO: actually load from game data, this is just a demo
    #     self.collectable_items = [
    #         CollectableItem(300, 650, item_type=ItemType.BLUE),
    #         CollectableItem(700, 400, item_type=ItemType.RED),
    #     ]

    def load_level(self, level_id):
        level = LevelConfig(id=level_id)
        self.level_length = len(level.raw_data[0])

        for y, row in enumerate(level.raw_data):
            for x, tile_type in enumerate(row):
                if tile_type != TileType.VOID:
                    img = TILE_IMGS[tile_type]
                    img_rect = img.get_rect()
                    img_rect.x = x * GameConfig.tile_size
                    img_rect.y = y * GameConfig.tile_size
                    self.tiles.append((img, img_rect))

    def handle_player_item_overlap(self, player):
        remaining_items = []
        for item in self.collectable_items:
            if player.is_overlap(item):
                logger.info(f"Player is overlapping with: {item}")
                player.collect_item(item)
            else:
                remaining_items.append(item)
        self.collectable_items = remaining_items


    def draw(self, screen, screen_offset):
        self.abs_screen_offset += screen_offset
        for tile in self.tiles:
            tile[1][0] += screen_offset
            screen.blit(tile[0], tile[1])
