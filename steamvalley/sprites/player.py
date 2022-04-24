import pygame

from config import INVENTORY_TEXT
from sprites.movable_sprite import MovableSprite


class Player(MovableSprite):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.inventory = []

    def collect_item(self, item):
        # TODO: check duplicates?
        self.inventory.append(item)

    def draw(self, window):
        super().draw(window)

        # Draw Inventory on top left corner
        window.blit(*INVENTORY_TEXT)
        item_x, item_y = INVENTORY_TEXT[1]
        item_x += 120
        for item in self.inventory:
            window.blit(pygame.transform.scale(item.image, (30, 30)), (item_x, item_y))
            item_x += 40
