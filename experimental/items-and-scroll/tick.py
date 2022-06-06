import pygame as pg
from const import *


def tick(player, items):
    for item in items:
        offset_x = player.rect.center[0] - item.rect.center[0]
        offset_y = player.rect.center[1] - item.rect.center[1]
        if player.mask.overlap(item.mask, (offset_x, offset_y)):
            if item not in COLLECTED_ITEMS:
                COLLECTED_ITEMS.append(item)
                item.kill()


def draw_text(WIN):
    font = pg.font.Font("freesansbold.ttf", 24)
    text = font.render("Collected", True, (0, 0, 0))
    WIN.blit(text, (20, 110))


def scroll(player, items, rect):
    if player.rect.x + 200 > WIDTH:
        for item in items:
            item.rect.x -= 5
        player.rect.x -= 5
        rect.x -= 5
        player.moving = True
    elif player.rect.x - 200 < 0:
        for item in items:
            item.rect.x += 5
        player.rect.x += 5
        rect.x += 5
        player.moving = True
    else:
        player.moving = False
