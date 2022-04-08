import pygame as pg 
import os
import time
import random
from const import *
from player import Player

#initialize pygame
pg.init()

#create screen
WIN = pg.display.set_mode((WIDTH,HEIGHT))
pg.display.set_caption("S4V Demo")
def main():
    RED = (255,0,0)
    run = True
    clock = pg.time.Clock()
    #create player
    player = Player(30,HEIGHT-PLAYER_HEIGHT,PLAYER_SPRITE_DIR,0.2)
    moving_left, moving_right = False, False
    # main function to redraw all objects
    def redraw_window():
        WIN.blit(BG,(0,0))
        pg.draw.line(WIN, RED, (0,HEIGHT-10), (WIDTH, HEIGHT-10))
        pg.draw.rect(WIN, RED, (600, HEIGHT-200,200,50))
        player.move(moving_left,moving_right)
        player.draw(WIN)

        #cleanObjects
        pg.display.update()

    while run:
        clock.tick(FPS)

        redraw_window()

       
        
        for event in pg.event.get():
            if event.type == pg.QUIT:
                run = False

            if event.type == pg.KEYDOWN:
                if event.key == pg.K_LEFT:
                    moving_left = True
                if event.key == pg.K_RIGHT:
                    moving_right = True
                if event.key == pg.K_SPACE:
                    player.jump = True

            if event.type == pg.KEYUP:
                if event.key == pg.K_LEFT:
                    moving_left = False
                if event.key == pg.K_RIGHT:
                    moving_right = False
        

main()