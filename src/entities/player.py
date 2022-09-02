from __future__ import annotations

from typing import TYPE_CHECKING, Iterable, List, Optional, Sequence

import pygame

from common import util
from common.event import EventType, GameEvent
from common.types import ActionType, EntityType
from common.util import now
from config import GameConfig, PlayerConfig, TrampolineConfig
from entities.animated_entity import AnimatedEntity
from entities.friendly_npc import FriendlyNpc
from entities.trampoline import Trampoline

if TYPE_CHECKING:
    from worlds.world import World

logger = util.get_logger(__name__)


class Player(AnimatedEntity):
    """
    The main character controlled by user, can talk / fight NPCs, can interact with in-game objects.
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.npc_near_by: Optional[FriendlyNpc] = None
        self.talking: bool = False
        self.inventory: List = []
        self.inventory_entity_id: Optional[int] = None
        self.hp: int = PlayerConfig.INITIAL_HP
        self.max_hp: int = PlayerConfig.INITIAL_HP
        self.hp_entity_id: Optional[int] = None

        self.last_hit_t: int = 0

    def get_x_y_w_h(self) -> tuple:
        """Slightly narrow down the Player rectangle since the head is too big."""
        x, y, w, h = super().get_x_y_w_h()
        x += 12 if self.get_flip_x() else 10
        w -= 26
        return x, y, w, h

    def update(self, events: Sequence[GameEvent], world: World) -> None:
        super().update(events, world)
        self._update_npc_near_by()
        self._pick_item_near_by()
        self._handle_events()
        self._update_screen_offset()
        self._maybe_jump_with_trampoline()

        # Manage the dependent entities.
        self._update_hp_entity()
        self._update_inventory_entity()

        self._handle_get_hit()
        if self.hp <= 0:
            self.die()
        if self.rect.top > GameConfig.HEIGHT:
            GameEvent(EventType.FALL, sender_type=self.entity_type).post()
            self.die()

    def count_inventory(self, entity_types: Iterable[EntityType] = tuple()) -> int:
        """
        Returns the number of collected entities,
        ALL of them or FILTERED by some give EntityType(s).
        """
        if not entity_types:
            return len(self.inventory)
        return len([entity for entity in self.inventory if entity.entity_type in entity_types])

    def discard_inventory(self, entity_types: Iterable[EntityType] = tuple()) -> None:
        """
        Discards certain types of entities from Player inventory.
        """
        # Do nothing if not given a specific list of types to discard.
        if not entity_types:
            return
        self.inventory = [
            entity for entity in self.inventory if entity.entity_type not in entity_types
        ]

    def _update_hp_entity(self):
        """
        This Player entity directly manages a PlayerHp entity.
        """
        # Cap the HP to self.max_hp
        self.hp = min(self.hp, self.max_hp)

        if not self.hp_entity_id:
            self.hp_entity_id = self.world.add_entity(EntityType.PLAYER_HP)
        self.world.get_entity(self.hp_entity_id).set_hp(self.max_hp, self.hp)

    def _update_inventory_entity(self):
        """
        This Player entity directly manages a PlayerInventory entity.
        """
        if not self.inventory_entity_id:
            self.inventory_entity_id = self.world.add_entity(EntityType.PLAYER_INVENTORY)
        self.world.get_entity(self.inventory_entity_id).set_inventory(self.inventory)

    def _handle_events(self):
        """
        This subject is controllable by user, we ask it to move based on keyboard inputs here.
        """
        for event in self.events:

            # Only allow player to move when NOT being hurt / NOT talking to some NPC.
            if not self.talking and not self.is_hurting:
                if event.is_key_down(pygame.K_LEFT, pygame.K_a):
                    self.move_left(True)
                elif event.is_key_down(pygame.K_RIGHT, pygame.K_d):
                    self.move_right(True)
                elif event.is_key_down(pygame.K_UP, pygame.K_SPACE, pygame.K_w):
                    self.jump()

            if event.is_key_up(pygame.K_LEFT, pygame.K_a):
                self.move_left(False)
            elif event.is_key_up(pygame.K_RIGHT, pygame.K_d):
                self.move_right(False)
            elif event.is_key_up(pygame.K_e):
                self._handle_activation()
            elif event.is_key_down(pygame.K_f):
                self._handle_throw()
            elif event.is_type(EventType.NPC_DIALOGUE_END):
                self.talking = False

    def _handle_activation(self):
        if not self.npc_near_by or not self.npc_near_by.has_dialogue():
            return
        # Broadcast an event for the NPC to handle
        # logger.info(f"_handle_activation with: {self.npc_near_by.entity_type}")
        GameEvent(EventType.PLAYER_ACTIVATE_NPC, listener_id=self.npc_near_by.id).post()
        self.talking = True  # this will turn back to False when receiving event NPC_DIALOGUE_END

    def _update_npc_near_by(self):
        self.npc_near_by = None
        for npc in self.world.get_friendly_npcs():
            if self.collide(npc):
                # Get a hold of the NPC, and post an event for that NPC to handle
                self.npc_near_by = npc
                GameEvent(EventType.PLAYER_NEAR_NPC, listener_id=npc.id).post()
                break

    def _pick_item_near_by(self):
        """
        If Player collides with a collectable entity, remove that entity from World,
        while adding that entity to the self.inventory list.
        """
        for entity in self.world.get_collectable_tiles():
            if self.collide(entity):
                self.world.remove_entity(entity.id)
                self.inventory.append(entity)
                GameEvent(EventType.COLLECT_ITEM, sender_type=self.entity_type).post()
                logger.info(f"Player picked up 1 {entity.entity_type}")

                if entity.entity_type == EntityType.LEVEL_END_FLAG:
                    GameEvent(EventType.LEVEL_END).post()

    def _handle_throw(self):
        """
        Spawns a ball at Player position, around the shoulder-level.
        Set it motions to go left or right depending on the facing of Player.
        :return:
        """
        self.set_action(ActionType.THROW, duration_ms=PlayerConfig.THROW_DURATION_MS)
        ball_id = self.world.add_entity(
            EntityType.PLAYER_BULLET,
            self.rect.centerx,
            self.rect.centery - 30,
        )
        ball = self.world.get_entity(ball_id)
        if self.get_flip_x():
            ball.move_left()
        else:
            ball.move_right()

    def _handle_get_hit(self):
        for bullet in self.world.get_entities(EntityType.SHADOW_BULLET):
            if self.collide(bullet):
                self.world.remove_entity(bullet.id)
                self._take_damage(bullet.damage)

        for shadow in self.world.get_entities(EntityType.SHADOW):
            if self.collide(shadow):
                self._take_damage(shadow.damage)

    def _take_damage(self, damage: int):
        now_ms = now()
        if now_ms - self.last_hit_t < PlayerConfig.INVULNERABLE_DURATION_MS:
            return
        else:
            self.stop()
            self.start_hurt(duration_ms=PlayerConfig.HURT_DURATION_MS)
            self.last_hit_t = now_ms
            logger.debug(f"Player HP: {self.hp} -> {self.hp - damage}")
            self.hp -= damage

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
            or (at_right_soft_edge and not self.world.at_right_most())
        ):
            # Undo player position change (player walks in-place)
            self.rect.x -= self.dx
            delta_screen_offset = -self.dx

        self.world.update_screen_offset(delta_screen_offset)

    def _maybe_jump_with_trampoline(self):
        trampoline: Trampoline
        for trampoline in self.world.get_trampolines():
            if self.collide(trampoline) and self.rect.bottom > trampoline.rect.top:
                trampoline.set_action(
                    ActionType.ANIMATE, duration_ms=TrampolineConfig.ANIMATION_DURATION_MS
                )
                self.jump_with_trampoline()
