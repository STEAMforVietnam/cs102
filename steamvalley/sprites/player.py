import pygame
from pygame.sprite import collide_mask

from config import ActionType, GameConfig, INVENTORY_TEXT
from sprites.movable_sprite import MovableSprite
from world import World, Tile


class Player(MovableSprite):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.jump_velocity = 0
        self.in_air = False
        self._inventory = []

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
        for tile in world.get_obstacle_tiles():
            obstacle = tile.sprite
            if obstacle.rect.colliderect(self.rect.x + dx, self.rect.y, self.rect.width, self.rect.height):
                dx = 0
            if obstacle.rect.colliderect(self.rect.x, self.rect.y + dy, self.rect.width, self.rect.height):
                if self.jump_velocity < 0:
                    self.jump_velocity = 0
                    dy = obstacle.rect.bottom - self.rect.top  # the gap between player's head and obstacle above
                else:
                    self.jump_velocity = 0
                    self.in_air = False
                    dy = obstacle.rect.top - self.rect.bottom  # the gap between player's feet and ground
        return dx, dy

    def move(self, world: World):
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

    def collect(self, tile: Tile):
        self._inventory.append(tile)

    def interact_items(self, world: World):
        for tile in world.get_collectable_tiles():
            if collide_mask(self, tile.sprite):
                world.remove_tile(tile.id)
                self.collect(tile)

    def draw(self, screen):
        super().draw(screen)

        # Draw Inventory on top left corner
        screen.blit(*INVENTORY_TEXT)
        item_x, item_y = INVENTORY_TEXT[1]
        item_x += 120
        for item in self._inventory:
            item.sprite.draw(screen, x_y=(item_x, item_y), scale=(30, 30))
            item_x += 40
