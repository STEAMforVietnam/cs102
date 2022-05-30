import pygame

from config import INVENTORY_TEXT, ActionType, GameConfig
from sprites.movable_sprite import MovableSprite


class Player(MovableSprite):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.inventory = []

    def collect_item(self, item):
        # TODO: check duplicates?
        self.inventory.append(item)

    def draw(self, window):
        super().draw(window)

        # Draw Inventory on top left corner
        window.blit(*INVENTORY_TEXT)
        item_x, item_y = INVENTORY_TEXT[1]
        item_x += 120
        for item in self.inventory:
            window.blit(pygame.transform.scale(item.image, (30, 30)), (item_x, item_y))
            item_x += 40

    def move(self, abs_screen_offset):
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

        if self.jumping and not self.is_landing:
            self.jump_velocity += self.y_speed
            self.jumping = False
            self.is_landing = True

        self.jump_velocity += GameConfig.gravity
        dy += self.jump_velocity

        # TODO: check against actual world tiles
        if self.rect.bottom + dy > GameConfig.height - GameConfig.tile_size:
            dy = GameConfig.height - GameConfig.tile_size - self.rect.bottom
            self.jump_velocity = 0
            self.is_landing = False

        # Horizontal scroll by player movement
        screen_offset = 0
        self.rect.x += dx
        self.rect.y += dy

        at_right_soft_edge = self.rect.right > GameConfig.width - GameConfig.player_soft_edge_width
        at_right_edge = self.rect.right >= GameConfig.width
        at_left_soft_edge = self.rect.left < GameConfig.player_soft_edge_width
        at_left_edge = self.rect.left <= 0

        print(abs_screen_offset)
        if (
            at_left_edge
            or at_right_edge
            or (abs_screen_offset < 0 and at_left_soft_edge)
            or at_right_soft_edge
        ):
            # undo player position change (player walks in-place)
            self.rect.x -= dx
            screen_offset = -dx

        # Maintain abs_screen_offset <= 0 to avoid over-scrolling to the left
        if abs_screen_offset + screen_offset > 0:
            screen_offset = -abs_screen_offset
        return screen_offset
