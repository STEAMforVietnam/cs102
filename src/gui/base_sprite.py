from pathlib import Path
from typing import Optional, Tuple, Union

import pygame
from pygame.rect import Rect

from common import util


class BaseSprite(pygame.sprite.Sprite):
    """
    Base class for all sprites. This simply supports drawing a still image.
    """

    def __init__(
        self,
        x: int,
        y: int,
        sprite_path: Path,
        scale: Optional[Union[float, Tuple[int, int]]] = None,
    ) -> None:
        """Load and init image at position (x, y)"""
        super().__init__()
        self.image = util.scale_image(pygame.image.load(sprite_path), scale)
        self.rect: Rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

    def render(
        self,
        screen: pygame.Surface,
        x_y: Tuple[float, float] = None,
        scale: float = None,
        flip_x: bool = False,
    ) -> None:
        """
        Renders the stored image onto the screen at (self.rect.x, self.rect.y).

        If arg x_y is set, use that pair of coordinates instead of self.rect.
        If arg scale is set, resize the image before rendering.
        If arg flip_x is set, flip the image horizontally before rendering.
        """
        if x_y is None:
            x_y = (self.rect.x, self.rect.y)

        image = util.scale_image(self.image, scale)

        if flip_x:
            image = pygame.transform.flip(image, True, False)

        screen.blit(image, x_y)

    def set_action(self, new_action):
        raise NotImplementedError
