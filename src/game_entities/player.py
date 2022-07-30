from __future__ import annotations

from typing import TYPE_CHECKING, Optional, Sequence

import pygame

from common import util
from common.event import EventType, GameEvent
from config import GameConfig
from game_entities.friendly_npc import FriendlyNpc
from game_entities.movable import MovableEntity

if TYPE_CHECKING:
    from worlds.world import World


logger = util.get_logger(__name__)


class Player(MovableEntity):
    """
    The main character controlled by user, can talk / fight NPCs, can interact with in-game objects.
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.npc_near_by: Optional[FriendlyNpc] = None

    def update(self, events: Sequence[GameEvent], world: World) -> None:
        super().update(events, world)
        self._update_npc_near_by()
        self._handle_events()
        self._update_screen_offset()

    def _handle_events(self):
        """
        This subject is controllable by user, we ask it to move based on keyboard inputs here.
        """
        for event in self.events:
            if event.is_key_down(pygame.K_LEFT, pygame.K_a):
                self.move_left(True)
            elif event.is_key_down(pygame.K_RIGHT, pygame.K_d):
                self.move_right(True)
            elif event.is_key_down(pygame.K_UP, pygame.K_SPACE, pygame.K_w):
                self.jump()
            elif event.is_key_up(pygame.K_LEFT, pygame.K_a):
                self.move_left(False)
            elif event.is_key_up(pygame.K_RIGHT, pygame.K_d):
                self.move_right(False)
            elif event.is_key_up(pygame.K_e):
                self._handle_activation()

    def _handle_activation(self):

        if not self.npc_near_by or not self.npc_near_by.has_dialogue():
            return
        # Broadcast an event for the NPC to handle
        logger.info(f"_handle_activation with: {self.npc_near_by.entity_type}")
        GameEvent(EventType.PLAYER_ACTIVATE_NPC, listener_id=self.npc_near_by.id).post()

    def _update_npc_near_by(self):
        for npc in self.world.get_friendly_npcs():
            if self.collide(npc):
                # Get a hold of the NPC, and broadcast an event for that NPC to handle
                self.npc_near_by = npc
                GameEvent(EventType.PLAYER_NEAR_NPC, listener_id=npc.id).post()
                break

    def _update_screen_offset(self):
        """Logics for horizontal world scroll based on player movement"""
        delta_screen_offset = 0

        at_right_edge = self.rect.right >= GameConfig.WIDTH
        at_right_soft_edge = self.rect.right > GameConfig.WIDTH - GameConfig.PLAYER_SOFT_EDGE_WIDTH
        at_left_edge = self.rect.left <= 0
        at_left_soft_edge = self.rect.left < GameConfig.PLAYER_SOFT_EDGE_WIDTH

        if (
            at_left_edge
            or at_right_edge
            or (at_left_soft_edge and not self.world.at_left_most())
            or at_right_soft_edge
        ):
            # Undo player position change (player walks in-place)
            self.rect.x -= self.dx
            delta_screen_offset = -self.dx

        self.world.update_screen_offset(delta_screen_offset)
