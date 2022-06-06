from typing import Optional

import pygame


def scale_image(image: pygame.Surface, scale: Optional[float] = None):
    if scale is None:
        return image
    return pygame.transform.scale(image, (int(image.get_width() * scale), int(image.get_height() * scale)))
