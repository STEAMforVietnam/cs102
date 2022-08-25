from __future__ import annotations

from pathlib import Path
from typing import TYPE_CHECKING, Dict, List, Optional, Sequence, Tuple, Union

import pygame
from pygame.rect import Rect
from pygame.surface import Surface

from common import util
from common.event import EventType, GameEvent
from common.types import ActionType
from common.util import now
from entities.movable_entity import MovableEntity

if TYPE_CHECKING:
    from worlds.world import World

logger = util.get_logger(__name__)


class EntityAction:
    """
    This is a helper class for AnimatedEntity below. To see how to call AnimatedEntity.set_action(),
    see that function's docs string.

    A subject can sometimes being in a special states such as being hurt, being angry,
    dying, etc.

    From the animation (GUI) viewpoint, we don't differentiate between action and state.

    The "movement-based" actions are (IDLE, MOVE, JUMP, CRAWL).
    The "state" actions are (DYING, HURT, ANGRY, THROW, ...). These "state" actions can override
    "movement-based" actions for a few hundred milliseconds at a time.
    """

    def __init__(self, action_type: ActionType, duration_ms: Optional[int] = None):
        self.started_at = now()
        self.action_type = action_type
        self.duration_ms = duration_ms

    def is_type(self, action_type: ActionType) -> bool:
        return self.action_type == action_type

    def is_expired(self) -> bool:
        if self.duration_ms is None:
            return False
        return now() - self.started_at >= self.duration_ms

    def is_prioritize(self) -> bool:
        return self.action_type not in (
            ActionType.IDLE,
            ActionType.MOVE,
            ActionType.JUMP,
            ActionType.CRAWL,
            ActionType.HURT,
        )


class AnimatedEntity(MovableEntity):
    def __init__(
        self,
        sprite_path: Path,
        scale: Optional[Union[float, Tuple[int, int]]] = None,
        *args,
        **kwargs,
    ) -> None:
        super().__init__(*args, **kwargs)

        # Load all images and set initial position (x, y).
        self.sprites: Dict[ActionType, List[Surface]] = self._load_sprites(sprite_path, scale)
        self.sprite_index: int = 0
        self.action = EntityAction(ActionType.IDLE)
        self.recent_action_started_at: dict = {}
        self.image = self.sprites[self.action.action_type][self.sprite_index]
        self.rect: Rect = self.image.get_rect()
        self.rect.x, self.rect.y = kwargs["x"], kwargs["y"]

        self.hurt_end_t: int = 0

    def update(self, events: Sequence[GameEvent], world: World) -> None:
        super().update(events, world)

        # Depends on the subject current movement status, deduct the current action
        # and the proper sprite for that action.
        self._update_action()
        self._change_sprite()

    def _update_action(self):
        if self.is_dying:
            self.set_action(ActionType.DYING)
            return

        if self.action.is_prioritize() and not self.action.is_expired():
            return

        if self.is_hurting:
            self.set_action(ActionType.HURT)
            return

        # Deduct the current action based on movement.
        if not self.is_landed:
            self.set_action(ActionType.JUMP)
        elif self.dx != 0:
            self.set_action(ActionType.MOVE)
        else:
            self.set_action(ActionType.IDLE)

        # If subject is moving left, turn on flip_x.
        if self.dx > 0:
            self.set_flip_x(False)
        elif self.dx < 0:
            self.set_flip_x(True)

    def start_hurt(self, duration_ms: int):
        self.hurt_end_t = now() + duration_ms
        GameEvent(EventType.HURT, sender_type=self.entity_type).post()

    @property
    def is_hurting(self):
        return now() < self.hurt_end_t

    def set_action(
        self,
        new_action_type: ActionType,
        duration_ms: Optional[int] = None,
        interval_ms: Optional[int] = None,
    ) -> bool:
        """
        Args:
          new_action_type: the action that should start now.
          duration_ms: how long should the action last. For indefinite action, don't set this arg.
          interval_ms: if set, only start the action if the last same-type action was
                              long enough ago (ie. enough time passed).

        Returns whether the action was registered to start.
        """
        if interval_ms is not None:
            if (
                self.recent_action_started_at.get(new_action_type)
                and now() < self.recent_action_started_at[new_action_type] + interval_ms
            ):
                return False  # do NOT set action if the last same-type action is too recent
        if self.action.action_type != new_action_type:
            self.action = EntityAction(action_type=new_action_type, duration_ms=duration_ms)
            self.recent_action_started_at[new_action_type] = self.action.started_at
            self.sprite_index = 0
            return True
        return False

    def is_action(self, action_type: ActionType) -> bool:
        return self.action.is_type(action_type) and not self.action.is_expired()

    def set_alpha(self, alpha: int) -> None:
        for sprites in self.sprites.values():
            for sprite in sprites:
                sprite.set_alpha(alpha)

    def _change_sprite(self):
        """
        Change to the next sprite in the sequence corresponding to the current action
        (note that there are multiple sequences to choose from)
        """
        current_ms = now()
        if current_ms - self.last_animation_ms > self.animation_interval_ms:
            self.last_animation_ms = current_ms
            self.sprite_index = (self.sprite_index + 1) % len(self.sprites[self.action.action_type])
        self.image = self.sprites[self.action.action_type][self.sprite_index]

    @staticmethod
    def _load_sprites(sprites_dir: Path, scale: float = 0.1) -> Dict[ActionType, List[Surface]]:
        """
        Load all images from directory and convert into a Dictionary
        which maps ActionType to list of Surface
        """
        sprites: Dict[ActionType, List[Surface]] = {}
        cnt = 0

        for sprite_subdir in sprites_dir.iterdir():
            # ignore OS managed files and folders such as .DS_Store
            if sprite_subdir.name.startswith(".") or not sprite_subdir.is_dir():
                continue

            action_sprites: List[Surface] = []
            try:
                action_type: ActionType = ActionType(sprite_subdir.name)
            except ValueError as e:
                logger.warning(
                    f"Unrecognized ActionType when loading from sprites_dir '{sprites_dir}': {e}"
                )
                continue

            # Read list of images & create list of sprites
            for image_file in sorted(sprite_subdir.iterdir()):
                if image_file.name.startswith(".") or not image_file.is_file():
                    continue
                image = pygame.image.load(str(image_file))
                action_sprites.append(util.scale_image(image, scale))
                cnt += 1

            sprites[action_type] = action_sprites
        # logger.debug(f"Loaded a total of {cnt} sprites for {len(sprites)} actions")
        return sprites


class PropEntity(AnimatedEntity):
    """
    Various items in the game that does not move, but still needs animation.
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.is_landed = True

    def _update_dx_dy_based_on_obstacles(self, obstacles):
        """
        This special entity does not need to worry about overlapping with obstacles,
        so we override this method with an empty body.
        """
