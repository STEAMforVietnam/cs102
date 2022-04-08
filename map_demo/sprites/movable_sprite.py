from config import ActionType, GameConfig
from sprites.base_sprite import BaseSprite


class MovableSprite(BaseSprite):
  def __init__(self, speed, y_speed=0, **kwargs):
    super().__init__(**kwargs)
    self.speed = speed
    self.y_speed = y_speed
    self.moving_left = False
    self.moving_right = False
    self.jumping = False

  def _set_action(self, new_action):
    if self.action != new_action:
      self.action = new_action
      self.sprite_index = 0

  def start_action(self, action):
    if action == ActionType.MOVE_LEFT:
      self.moving_left = True
    elif action == ActionType.MOVE_RIGHT:
      self.moving_right = True
    elif action == ActionType.JUMP:
      self.jumping = True

  def stop_action(self, action):
    if action == ActionType.MOVE_LEFT:
      self.moving_left = False
    elif action == ActionType.MOVE_RIGHT:
      self.moving_right = False

  def move(self):
    dx = 0
    dy = 0
    if self.moving_left:
      dx = -self.speed
      self._set_action(ActionType.MOVE_LEFT)
      self.flip = True

    if self.moving_right:
      dx = self.speed
      self._set_action(ActionType.MOVE_RIGHT)
      self.flip = False

    if self.is_landing:
      self._set_action(ActionType.JUMP)

    if self.jumping and not self.is_landing:
      self.jump_velocity += self.y_speed
      self.jumping = False
      self.is_landing = True

    self.jump_velocity += GameConfig.gravity
    dy += self.jump_velocity

    if self.rect.bottom + dy > GameConfig.height - 10:
      dy = GameConfig.height - 10 - self.rect.bottom
      self.jump_velocity = 0
      self.is_landing = False

    elif self.rect.bottom + dy > GameConfig.height - 200 and self.rect.left < 800 and self.rect.right > 600:
      dy = GameConfig.height - 200 - self.rect.bottom
      self.jump_velocity = 0
      self.is_landing = False

    if self._is_standing():
      self._set_action(ActionType.IDLE)
    self._previous_coordinate(self.rect.x, self.rect.y)
    self.rect.x += dx
    self.rect.y += dy

