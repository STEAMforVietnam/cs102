from pygame import Surface

from common import DIAMOND_BLUE_SPRITE, DIAMOND_RED_SPRITE, ItemType

from .base_entity import BaseEntity


class GameItem(BaseEntity):
    def __init__(self, x: float, y: float, type: ItemType) -> None:
        self.type = type
        self.name: str
        self.hidden = False

        if type == ItemType.DIAMOND_BLUE:
            self.name = "Kim Cuong Xanh"
            super().__init__(x, y, DIAMOND_BLUE_SPRITE)
        elif type == ItemType.DIAMOND_RED:
            self.name = "Kim Cuong Do"
            super().__init__(x, y, DIAMOND_RED_SPRITE)

    def set_hidden(self):
        self.hidden = True

    def render(self, screen: Surface) -> None:
        if not self.hidden:
            super().render(screen)
