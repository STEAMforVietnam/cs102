from entities.base_entity import BaseEntity
from pygame.surface import Surface

from common import SCREEN_HEIGHT, SCREEN_WIDTH


class Robot(BaseEntity):
    def __init__(self, x: int, y: int, image: Surface, x_heading: int, y_heading: int) -> None:
        super().__init__(x, y, image)
        self.x_heading = x_heading
        self.y_heading = y_heading

    def update(self):
        self.x = self.x + self.x_heading
        self.y = self.y + self.y_heading

        if self.x > SCREEN_WIDTH - self.image.get_width():
            self.x_heading = -self.x_heading
        if self.x < 0:
            self.x_heading = -self.x_heading
        if self.y > SCREEN_HEIGHT - self.image.get_height():
            self.y_heading = -self.y_heading
        if self.y < 0:
            self.y_heading = -self.y_heading
