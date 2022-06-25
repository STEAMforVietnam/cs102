from entities.base_entity import BaseEntity
from pygame.surface import Surface


class GameItem(BaseEntity):
    def __init__(self, x: int, y: int, image: Surface) -> None:
        super().__init__(x, y, image)
        self.hidden = False

    def set_hidden(self):
        self.hidden = True

    def render(self, screen: Surface) -> None:
        if not self.hidden:
            super().render(screen)
