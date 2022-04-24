import pygame

from config import ItemType, ITEM_IMAGES
from sprites.base_sprite import BaseSprite


class CollectableItem(BaseSprite):
    def __init__(self, x, y, item_type: ItemType):
        super().__init__(x, y)
        self.item_type = item_type
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)
        self.mask = pygame.mask.from_surface(self.image)
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)

    def __repr__(self):
        return f"Item(type={self.item_type}, topleft={self.rect.topleft})"

    @property
    def image(self):
        return ITEM_IMAGES[self.item_type]

    def to_blit_args(self):
        return ITEM_IMAGES[self.item_type], self.rect
