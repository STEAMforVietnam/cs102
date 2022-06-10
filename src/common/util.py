from typing import Optional

import pygame

from common.types import TileType
from config import GameConfig


def scale_image(image: pygame.Surface, scale: Optional[float] = None):
    if scale is None:
        return image
    return pygame.transform.scale(
        image, (int(image.get_width() * scale), int(image.get_height() * scale))
    )


def load_tile_img(tile_type: TileType) -> Optional[pygame.Surface]:
    if tile_type == TileType.EMPTY:
        return None
    path = f"assets/tiles/{tile_type.name.lower()}.png"
    image = pygame.image.load(path)
    if TileType.should_scale_when_load(tile_type):
        image = pygame.transform.scale(image, (GameConfig.TILE_SIZE, GameConfig.TILE_SIZE))
    return image
