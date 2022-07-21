from pathlib import Path
from typing import Optional, Tuple, Union

import pygame
from pygame.rect import Rect
from pygame.surface import Surface

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
        self.visible = True  # whether to render the image
        self.flip_x = False  # whether to flip the image horizontally

        self.image = util.scale_image(pygame.image.load(sprite_path), scale)
        self.rect: Rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

    def set_visible(self, visible: bool) -> None:
        self.visible = visible

    def is_visible(self) -> bool:
        return self.visible

    def set_flip_x(self, flip_x: bool) -> None:
        self.flip_x = flip_x

    def render(
        self,
        screen: Surface,
        x_y: Tuple[float, float] = None,
        scale: float = None,
    ) -> None:
        """
        Renders the stored image onto the screen at (self.rect.x, self.rect.y).

        If arg x_y is set, use that pair of coordinates instead of self.rect.
        If arg scale is set, resize the image before rendering.
        """
        if not self.visible:
            return

        if x_y is None:
            x_y = (self.rect.x, self.rect.y)

        image = util.scale_image(self.image, scale)

        if self.flip_x:
            image = pygame.transform.flip(image, True, False)

        screen.blit(image, x_y)
