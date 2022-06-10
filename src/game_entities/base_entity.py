import itertools
from typing import Tuple

import pygame


class BaseEntity(pygame.sprite.Sprite):
    """
    Base class for all game entities. This simply supports drawing a still image.
    Most game entities will be objects of the child classes instead of using this class directly.
    """

    gen_id = itertools.count()

    def __init__(self, x: int, y: int, image: pygame.Surface, object_type=None) -> None:
        super().__init__()
        self.id = next(BaseEntity.gen_id)
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.object_type = object_type

    def draw(
        self,
        screen: pygame.Surface,
        x_y: Tuple[float, float] = None,
        scale: float = None,
    ) -> None:
        if x_y is None:
            x_y = (self.rect.x, self.rect.y)

        image = self.image
        if scale is not None:
            image = pygame.transform.scale(image, scale)

        screen.blit(image, x_y)
