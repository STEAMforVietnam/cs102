from sprites.movable_sprite import MovableSprite


class Player(MovableSprite):
  def __init__(self, **kwargs):
    super().__init__(**kwargs)