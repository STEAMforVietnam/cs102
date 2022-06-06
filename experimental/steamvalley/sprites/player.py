import logging
from typing import Optional

import util
from pygame.sprite import collide_mask
from sprites.base_sprite import BaseSprite
from sprites.movable_sprite import MovableSprite
from sprites.npc import Npc
from world import World

from config import INVENTORY_TEXT, ActionType, GameConfig


class Player(MovableSprite):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.jump_velocity = 0
        self.in_air = False
        self.npc_near_by: Optional[Npc] = None
        self._inventory = []

        self.reset_dialogue()

        # TODO: move somewhere else
        self.dialogue = [
            ("Co Thao", "Xin chao"),
            ("Tay May", "Xin chao co"),
        ]

    def reset_dialogue(self):
        self._dialogue_text = None
        self._dialogue_index = -1

    def _get_dx_dy_unobstructed(self):
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

        if self.jumping and not self.in_air:
            self.jump_velocity += self.y_speed
            self.jumping = False
            self.in_air = True

        self.jump_velocity += GameConfig.gravity
        dy += self.jump_velocity
        return dx, dy

    def _get_dx_dy_in_world(self, dx, dy, world: World):
        for obstacle in world.get_obstacles():
            if obstacle.rect.colliderect(
                self.rect.x + dx, self.rect.y, self.rect.width, self.rect.height
            ):
                dx = 0
            if obstacle.rect.colliderect(
                self.rect.x, self.rect.y + dy, self.rect.width, self.rect.height
            ):
                if self.jump_velocity < 0:
                    self.jump_velocity = 0
                    # the gap between player's head and obstacle above
                    dy = obstacle.rect.bottom - self.rect.top
                else:
                    self.jump_velocity = 0
                    self.in_air = False
                    # the gap between player's feet and ground
                    dy = obstacle.rect.top - self.rect.bottom
        return dx, dy

    def move(self, world: World):
        if self._dialogue_text is not None:
            return 0
        dx, dy = self._get_dx_dy_unobstructed()
        dx, dy = self._get_dx_dy_in_world(dx, dy, world)

        # Horizontal world scroll based on player movement
        screen_offset = 0
        self.rect.x += dx
        self.rect.y += dy

        at_right_soft_edge = self.rect.right > GameConfig.width - GameConfig.player_soft_edge_width
        at_right_edge = self.rect.right >= GameConfig.width
        at_left_soft_edge = self.rect.left < GameConfig.player_soft_edge_width
        at_left_edge = self.rect.left <= 0

        if (
            at_left_edge
            or at_right_edge
            or (world.abs_screen_offset < 0 and at_left_soft_edge)
            or at_right_soft_edge
        ):
            # Undo player position change (player walks in-place)
            self.rect.x -= dx
            screen_offset = -dx

        # Maintain abs_screen_offset <= 0 to avoid over-scrolling to the left
        if world.abs_screen_offset + screen_offset > 0:
            screen_offset = -world.abs_screen_offset
        return screen_offset

    def collect(self, tile: BaseSprite):
        self._inventory.append(tile)

    def interact(self, world: World):
        for tile in world.get_collectable_tiles():
            if collide_mask(self, tile):
                world.remove_tile(tile.id)
                self.collect(tile)
        self.update_npc_near_by(world)

    def update_npc_near_by(self, world: World):
        # Assume no 2 or more NPCs are next to one another
        self.npc_near_by = None
        for npc_id in world.get_npc_ids():
            npc = world.tiles[npc_id]
            if collide_mask(self, npc):
                self.npc_near_by = npc
                npc.is_near_player = True
            else:
                npc.is_near_player = False

    def handle_special_interaction(self, screen):
        logging.info(f"handle_special_interaction - self.npc_near_by: {self.npc_near_by}")
        if not self.npc_near_by or not self.npc_near_by.has_quest():
            return
        # Continue dialogue with NPC
        self._dialogue_text = self.npc_near_by.get_next_line()

    def draw(self, screen):
        super().draw(screen)
        if self._dialogue_text:
            util.draw_dialogue_box(screen)
            util.draw_dialogue_text(screen, self._dialogue_text)

        # Draw Inventory on top left corner
        screen.blit(*INVENTORY_TEXT)
        item_x, item_y = INVENTORY_TEXT[1]
        item_x += 120
        for item in self._inventory:
            item.draw(screen, x_y=(item_x, item_y), scale=0.5)
            item_x += 40
