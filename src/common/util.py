import functools
import logging
from typing import Iterable, Optional, Tuple, Union

import pygame
from pygame.font import Font
from pygame.surface import Surface

from config import DATA_DIR, FONT_PATH, Color, GameConfig, LevelLoadingBarConfig

logging.basicConfig(level=logging.DEBUG if GameConfig.DEBUG else logging.INFO)


def get_logger(name):
    logger = logging.getLogger(name)
    return logger


logger = get_logger(__name__)


@functools.lru_cache(maxsize=None)
def get_font(font_size):
    """
    Font loading is slow, but PyGame doesn't let you load a font without specifying a font size,
    so we cache the loaded ones to improve performance.

    If you get some error around here, that is probably due to using an older Python version.
    -> remove the decorator line `@functools.lru_cache(maxsize=None)` and try again.
    """
    return Font(FONT_PATH, font_size)


def now():
    return pygame.time.get_ticks()


def scale_image(image: Surface, scale: Optional[Union[float, Tuple[int, int]]] = None):
    if scale is None or scale == 1.0:
        return image
    if isinstance(scale, int) or isinstance(scale, float):
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


def draw_loading_bar(screen: Surface, loading_percent: int):
    draw_pct_bar(
        screen,
        fraction=loading_percent / 100,
        x=(GameConfig.WIDTH - LevelLoadingBarConfig.WIDTH) / 2,
        y=(GameConfig.HEIGHT - LevelLoadingBarConfig.HEIGHT) / 2,
        width=LevelLoadingBarConfig.WIDTH,
        height=LevelLoadingBarConfig.HEIGHT,
        margin=10,
        color=Color.LOADING_BAR,
    )


def draw_pct_bar(screen: Surface, fraction: float, x, y, width, height, margin, color: Color):
    """
    Draw a bar at given position, filled up to the given `fraction`.
    """
    fraction = min(fraction, 1)
    pygame.draw.rect(screen, color, (x, y, width, height), 2)
    pygame.draw.rect(
        screen,
        color,
        (x + margin, y + margin, int(fraction * (width - 2 * margin)), height - 2 * margin),
    )


def get_available_level_ids() -> Iterable[int]:
    """
    Look at ALL *.csv files in the level data dir to get the list of available level IDs.
    """
    level_ids = sorted(
        [
            int(level_data_file.stem)
            for level_data_file in (DATA_DIR / "levels").iterdir()
            if level_data_file.suffix == ".csv"
            and not level_data_file.name.startswith(".")
            and not level_data_file.is_dir()
        ]
    )
    logger.info(f"Detected available levels: {level_ids}")
    return level_ids
