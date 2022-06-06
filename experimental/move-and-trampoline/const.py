import pygame as pg 
import os

FPS = 60
WIDTH, HEIGHT = 1500, 750
PLAYER_WIDTH, PLAYER_HEIGHT = 100, 220

BG = pg.transform.scale(pg.image.load(os.path.join("assets","background.png")),(WIDTH,HEIGHT))
PLAYER_IMG = ['tm_0.png','tm_1.png','tm_2.png','tm_3.png','tm_4.png','tm_5.png','tm_6.png','tm_7.png','tm_8.png','tm_9.png','tm_10.png']

PLAYER_HEALTH = 500
PLAYER_SPEED = 5
ANIMATION_TIME = 80
PLAYER_SPRITE_DIR = 'assets/player'
PLAYER_JUMP_VEL = -15

GRAVITY = 0.5
JUMP_LIMIT = 200

# define action type
ACTION_TYPES = ['idle','jump','move']
IDLE = 0
JUMP = 1
MOVE = 2

TRAMPOLINE_DIR = 'assets/trampoline'
TRAMPOLINE_ACTION = ['blow']
TRAMPOLINE_VEL = -20
MAX_TRAMPOLINE_VEL = -20

