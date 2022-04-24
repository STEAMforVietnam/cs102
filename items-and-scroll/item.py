import pygame as pg
from const import *
import os

#Load Item
Blue_item = pg.transform.scale(pg.image.load('assets/Items/1.png'),(50,50))
Red_item = pg.transform.scale(pg.image.load('assets/Items/2.png'), (50,50))
item_boxes = {
    'Blue' : Blue_item,
    'Red' : Red_item
}
item_boxes_group = pg.sprite.Group()

class Items(pg.sprite.Sprite):
    def __init__(self, type, x, y):
        pg.sprite.Sprite.__init__(self)
        self.type = type
        self.image = item_boxes[self.type]
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)
        self.mask = pg.mask.from_surface(self.image)

    



