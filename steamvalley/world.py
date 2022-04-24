import logging

from config import ItemType
from sprites import CollectableItem

logger = logging.getLogger(__name__)

class World:
    def __init__(self):
        self.obstacles = []
        self.collectable_items = []

    def load_level(self, level_id):
        # TODO: actually load from game data, this is just a demo
        self.collectable_items = [
            CollectableItem(300, 650, item_type=ItemType.BLUE),
            CollectableItem(700, 400, item_type=ItemType.RED),
        ]

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
        for tile in self.collectable_items:
            # tile[1][0] -= 1  # todo: scroll
            screen.blit(*tile.to_blit_args())
