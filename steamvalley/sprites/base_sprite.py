import itertools
from typing import Optional

import pygame

import util


class BaseSprite(pygame.sprite.Sprite):
    """
    Base class for visible game objects.
    """
    gen_id = itertools.count()

    def __init__(self, x: int, y: int, image: pygame.Surface, object_type=None):
        super().__init__()
        self.id = next(BaseSprite.gen_id)
        self.last_animation_ms = pygame.time.get_ticks()
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.object_type = object_type

    def draw(self, screen, x_y=None, scale: Optional[float] = None):
        if x_y is None:
            x_y = (self.rect.x, self.rect.y)

        image = self.image
        image = util.scale_image(image, scale)

        screen.blit(image, x_y)
