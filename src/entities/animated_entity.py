from __future__ import annotations

from pathlib import Path
from typing import TYPE_CHECKING, Dict, List, Optional, Sequence, Tuple, Union

import pygame
from pygame.rect import Rect
from pygame.surface import Surface

from common import util
from common.event import GameEvent
from common.types import ActionType
from entities.movable_entity import MovableEntity

if TYPE_CHECKING:
    from worlds.world import World

logger = util.get_logger(__name__)


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
        self.action: ActionType = ActionType.IDLE
        self.image = self.sprites[self.action][self.sprite_index]
        self.rect: Rect = self.image.get_rect()
        self.rect.x, self.rect.y = kwargs["x"], kwargs["y"]

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

        # Deduct the current action based on movement.
        if self.is_landed:
            if self.dx == 0:
                self.set_action(ActionType.IDLE)
            else:
                self.set_action(ActionType.MOVE)
        else:
            self.set_action(ActionType.JUMP)

        # If subject is moving left, turn on flip_x.
        if self.dx > 0:
            self.set_flip_x(False)
        elif self.dx < 0:
            self.set_flip_x(True)

    def set_action(self, new_action: ActionType) -> None:
        if self.action != new_action:
            self.action = new_action
            self.sprite_index = 0

    def _change_sprite(self):
        """
        Change to the next sprite in the sequence corresponding to the current action
        (note that there are multiple sequences to choose from)
        """
        current_ms = pygame.time.get_ticks()
        if current_ms - self.last_animation_ms > self.animation_interval_ms:
            self.last_animation_ms = current_ms
            self.sprite_index = (self.sprite_index + 1) % len(self.sprites[self.action])
        self.image = self.sprites[self.action][self.sprite_index]

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
            for image_file in sprite_subdir.iterdir():
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
    Various items in the game that does not move / jump, but still needs animation.
    """

    def _update_action(self):
        """
        This special entity does not have actions such as jump,
        so we override this method with an empty body.
        """

    def _update_dx_dy_based_on_obstacles(self, obstacles):
        """
        This special entity does not need to worry about overlapping with obstacles,
        so we override this method with an empty body.
        """
