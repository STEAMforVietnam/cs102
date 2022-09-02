from collections import Counter
from typing import List

import pygame

from common import util
from config import Color, PlayerInventoryConfig
from entities.base_entity import BaseEntity


class PlayerInventory(BaseEntity):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.inventory: List = []
        self.rect.centery = self.rect.y + PlayerInventoryConfig.TILE_SIZE // 2

    def set_inventory(self, inventory: List):
        """Set the backend data, called by Player."""
        self.inventory = inventory

    def render(
        self,
        screen: pygame.Surface,
        *args,
        **kwargs,
    ) -> None:
        super().render(screen, *args, **kwargs)

        # Render the collected items, each with a count.
        # This computation could be optimized more for performance.
        counter = Counter([item.entity_type for item in self.inventory])
        inventory_dict = {item.entity_type: item for item in self.inventory}
        x = PlayerInventoryConfig.X
        y = PlayerInventoryConfig.Y
        for entity_type, cnt in counter.items():
            x += PlayerInventoryConfig.X_STEP
            inventory_dict[entity_type].render(
                screen,
                x_y=(x, y),
                scale=(PlayerInventoryConfig.TILE_SIZE, PlayerInventoryConfig.TILE_SIZE),
            )
            util.display_text(
                screen,
                text=str(cnt),
                x=x + PlayerInventoryConfig.TILE_SIZE - 2,
                y=y + PlayerInventoryConfig.TILE_SIZE - 2,
                color=Color.TEXT_INVENTORY_CNT,
            )
