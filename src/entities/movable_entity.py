from __future__ import annotations

import random
from typing import TYPE_CHECKING, Sequence

from common import util
from common.event import EventType, GameEvent
from entities.base_entity import BaseEntity

if TYPE_CHECKING:
    from worlds.world import World

logger = util.get_logger(__name__)


class MovableEntity(BaseEntity):
    def __init__(
        self,
        animation_interval_ms: int = 80,
        speed: int = 0,
        gravity: int = 0,
        init_dx: int = 0,
        init_dy: int = 0,
        jump_vertical_speed: int = 0,
        jump_with_trampoline_speed: int = 0,
        *args,
        **kwargs,
    ) -> None:
        super().__init__(*args, **kwargs)

        # The gravity value unique to this subject.
        self.gravity = gravity

        # How fast this subject moves.
        self.speed: int = speed
        self.jump_vertical_speed: int = jump_vertical_speed
        self.jump_with_trampoline_speed: int = jump_with_trampoline_speed

        # Amount of delta (change) in position, along the 2 axis.
        self.dx: int = init_dx
        self.dy: int = init_dy

        # Tracking the states of this subject
        self.moving_left: bool = False
        self.moving_right: bool = False
        self.is_landed: bool = False  # Let subject fall to stable position
        self.is_dying: bool = False

        # minimal time until switching to next sprite
        self.animation_interval_ms: int = animation_interval_ms
        self.last_animation_ms: int = 0

    def update(self, events: Sequence[GameEvent], world: World) -> None:
        super().update(events, world)
        # Knowing the current state of the subject, we calculate the amount of changes
        # - dx and dy - that should occur to the player position during this current game tick.

        # Step 1: calculate would-be dx, dy when unobstructed
        self.dx = 0

        if self.is_landed:
            self.dy = 0
        self.dy += self.gravity

        if self.moving_left:
            self.dx = -self.speed
        if self.moving_right:
            self.dx = self.speed

        # Step 2: update dx, dy to prevent player from overlapping with obstacles
        self._update_dx_dy_based_on_obstacles(world.get_obstacles())

        # Step 3: update current position by the deltas
        self.rect.x += self.dx
        self.rect.y += self.dy

    def die(self):
        self.stop()
        self.is_dying = True
        GameEvent(EventType.DIE, sender_type=self.entity_type).post()

    def stop(self):
        self.moving_left = False
        self.moving_right = False

    def move_left(self, enabled=True):
        self.moving_left = enabled
        if self.moving_left:
            self.moving_right = False

    def move_right(self, enabled=True):
        self.moving_right = enabled
        if self.moving_right:
            self.moving_left = False

    def move_opposite(self):
        if self.moving_left:
            self.move_right()
        elif self.moving_right:
            self.move_left()

    def move_random(self):
        if random.randint(0, 1):
            self.move_left()
        else:
            self.move_right()

    def jump(self):
        if self.is_landed:
            self.is_landed = False
            self.dy = -self.jump_vertical_speed
            GameEvent(EventType.JUMP, sender_type=self.entity_type).post()

    def jump_with_trampoline(self):
        if not self.is_landed:
            self.dy = -self.jump_with_trampoline_speed
            GameEvent(EventType.JUMP, sender_type=self.entity_type).post()

    def _update_dx_dy_based_on_obstacles(self, obstacles):
        """
        Knowing the positions of all obstacles and the would-be position of this subject
        (self.rect.x + self.dx, self.rect.y + self.dy), check if the would-be position
        is colliding with any of the obstacles.

        If collision happens, restrict the movement by modifying self.dx and(or) self.dy.
        """
        # The obstacle check in the following for loop will determine
        # whether the subject is_landed, so we first reset it.
        self.is_landed = False
        for obstacle in obstacles:
            x, y, w, h = self.get_x_y_w_h()

            if obstacle.rect.colliderect(x + self.dx, y, w, h):
                # Hitting an obstacle horizontally, prevent horizontal movement altogether:
                self.dx = 0

            if obstacle.rect.colliderect(x, y + self.dy, w, h):
                # Hitting an obstacle vertically, reduce vertical movement:
                if self.dy < 0:
                    # the gap between player's head and obstacle above
                    self.dy = obstacle.rect.bottom - self.rect.top
                else:
                    self.is_landed = True
                    # the gap between player's feet and ground
                    self.dy = obstacle.rect.top - self.rect.bottom
