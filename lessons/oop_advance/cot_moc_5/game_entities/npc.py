from common import TO_MO_SPRITE

from .base_entity import BaseEntity


class NPC(BaseEntity):
    def __init__(self, x: float, y: float) -> None:
        super().__init__(x, y, TO_MO_SPRITE)
