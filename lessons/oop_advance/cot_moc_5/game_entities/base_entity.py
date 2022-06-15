from pygame import Surface
from utils import overlap


class BaseEntity:
    def __init__(self, x: float, y: float, image: Surface) -> None:
        self.x: float = x
        self.y: float = y
        self.image: Surface = image

    # Note: 'BaseEntity' is forward reference of BaseEntity
    def touch(self, obj: "BaseEntity"):
        return overlap(self.x, self.y, self.image, obj.x, obj.y, obj.image)

    def render(self, screen: Surface) -> None:
        screen.blit(self.image, (self.x, self.y))
