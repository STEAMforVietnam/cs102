from __future__ import annotations

import utils
from pygame.surface import Surface


class BaseEntity:
    def __init__(self, x: int, y: int, image: Surface) -> None:
        self.x = x
        self.y = y
        self.image = image

    def render(self, screen: Surface) -> None:
        screen.blit(self.image, (self.x, self.y))

    def touch(self, other: BaseEntity):
        return utils.overlap(self.x, self.y, self.image, other.x, other.y, other.image)
