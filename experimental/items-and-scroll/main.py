from cmath import rect
from re import L
import pygame as pg
import os
import time
import random
from const import *
from player import Player
from item import *
from tick import *

# initialize pygame
pg.init()

# create screen
WIN = pg.display.set_mode((WIDTH, HEIGHT))
pg.display.set_caption("S4V Demo")


def main():
    global player_sprite
    RED = (255, 0, 0)
    run = True
    clock = pg.time.Clock()
    # create player
    player = Player(250, HEIGHT - PLAYER_HEIGHT, PLAYER_SPRITE_DIR, 0.2)
    player_sprite = player
    moving_left, moving_right = False, False
    # create items
    item = Items("Blue", 300, 650)
    item_boxes_group.add(item)
    item = Items("Red", 700, 400)
    item_boxes_group.add(item)
    # Create rect
    rect = pg.Rect(600, HEIGHT - 200, 200, 50)
    # main function to redraw all objects
    def redraw_window():
        WIN.blit(BG, (0, 0))
        # pg.draw.line(WIN, RED, (0,HEIGHT-10), (WIDTH, HEIGHT-10))
        pg.draw.rect(WIN, RED, rect)
        player.move(moving_left, moving_right)
        player.draw(WIN)
        # Draw Items
        item_boxes_group.update()
        item_boxes_group.draw(WIN)
        # Draw collected items
        item_x = 150
        item_y = 100
        draw_text(WIN)
        for item in COLLECTED_ITEMS:
            WIN.blit(pg.transform.scale(item.image, (30, 30)), (item_x, item_y))
            item_x += 40
        # cleanObjects
        pg.display.update()

    while run:
        clock.tick(FPS)

        redraw_window()

        # userInput = pg.key.get_pressed()

        for event in pg.event.get():
            if event.type == pg.QUIT:
                run = False

            if event.type == pg.KEYDOWN:
                if event.key == pg.K_LEFT:
                    moving_left = True
                if event.key == pg.K_RIGHT:
                    moving_right = True
                if event.key == pg.K_SPACE and player.is_landing == False:
                    player.jump = True

            if event.type == pg.KEYUP:
                if event.key == pg.K_LEFT:
                    moving_left = False
                if event.key == pg.K_RIGHT:
                    moving_right = False

        tick(player, item_boxes_group)
        scroll(player, item_boxes_group, rect)

        # if userInput[pg.K_LEFT]:
        #     moving_left = True
        # if userInput[pg.K_RIGHT]:
        #     moving_right = True
        # if userInput[pg.K_SPACE]:
        #     player.jump = True


main()
