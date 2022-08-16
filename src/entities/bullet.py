from entities.movable_entity import MovableEntity


class Bullet(MovableEntity):
    def __init__(self, damage, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.damage = damage
