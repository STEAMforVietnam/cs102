import logging
from typing import Optional, Tuple, Union

import pygame
from pygame.surface import Surface

from config import GameConfig

logging.basicConfig(level=logging.DEBUG if GameConfig.DEBUG else logging.INFO)


def get_logger(name):
    logger = logging.getLogger(name)
    return logger


def scale_image(image: Surface, scale: Optional[Union[float, Tuple[int, int]]] = None):
    if scale is None or scale == 1.0:
        return image
    if isinstance(scale, float):
        return pygame.transform.scale(
            image,
            (int(image.get_width() * scale), int(image.get_height() * scale)),
        )
    else:
        return pygame.transform.scale(
            image,
            scale,
        )
