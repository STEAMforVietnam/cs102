from common import ROBOT_SPRITE, SCREEN_HEIGHT, SCREEN_WIDTH

from .base_entity import BaseEntity


class Robot(BaseEntity):
    def __init__(self, x: float, y: float, x_heading: float, y_heading: float) -> None:
        super().__init__(x, y, ROBOT_SPRITE)
        self.x_heading: float = x_heading
        self.y_heading: float = y_heading

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
