import functools
import logging
from typing import Optional, Tuple, Union

import pygame
from pygame.font import Font
from pygame.surface import Surface

from config import FONT_PATH, Color, GameConfig

logging.basicConfig(level=logging.DEBUG if GameConfig.DEBUG else logging.INFO)


def get_logger(name):
    logger = logging.getLogger(name)
    return logger


@functools.lru_cache(maxsize=None)
def get_font(font_size):
    """
    Font loading is slow, but PyGame doesn't let you load a font without specifying a font size,
    so we cache the loaded ones to improve performance.

    If you get some error around here, that is probably due to using an older Python version.
    In that case, remove the decorator line `@functools.lru_cache(maxsize=None)` and try again.
    """
    return Font(FONT_PATH, font_size)


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


def display_text(
    screen: Surface,
    text: str,
    x: int,
    y: int,
    font_size: int = 14,
    color: tuple = Color.DEFAULT,
):
    """
    Given a screen object, display text at (x, y) position, with set font, font size, and color.
    """
    screen.blit(
        get_font(font_size).render(text, True, color),
        (x, y),
    )
