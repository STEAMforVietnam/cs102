import pygame as pg
from const import *
import os

class Character(pg.sprite.Sprite):
    def __init__(self,x,y,sprites_dir,scale):
        self.animation_list = self.__load_sprites(sprites_dir,scale)
        self.speed = PLAYER_SPEED
        self.jump_velocity = 0
        self.jump = False
        self.pre_x = x
        self.pre_y = y
        self.action = 0
        self.sprite_index = 0
        self.image = self.animation_list[self.action][self.sprite_index]
        self.rect = self.image.get_rect()
        self.rect.center = (x,y)
        self.animation_time = pg.time.get_ticks()
        self.flip = False
        self.is_landing = True
        self.fly = False

    # load all sprites for all action types
    def __load_sprites(self,sprites_dir,scale):
        sprite_list = []
        for action_type in ACTION_TYPES:
            action_sprites = []
            for img_name in os.listdir(f'{sprites_dir}/{action_type}'):
                img = pg.image.load(os.path.join(sprites_dir,action_type,img_name))
                action_sprites.append(pg.transform.scale(img,(int(img.get_width() * scale), int(img.get_height() * scale))))
            sprite_list.append(action_sprites)
        return sprite_list

    # store previous coordinate
    def __previous_coordinate(self,x,y):
        self.pre_x, self.pre_y = x, y

    def __is_standing(self):
        return self.pre_x == self.rect.x and self.pre_y == self.rect.y

    def __set_action(self, new_action):
        
        if self.action != new_action:
            self.action = new_action
            self.sprite_index = 0

    def __update_animation(self):
        self.image = self.animation_list[self.action][self.sprite_index]
        if pg.time.get_ticks() - self.animation_time > ANIMATION_TIME:
            self.animation_time = pg.time.get_ticks()
            self.sprite_index = (self.sprite_index+1)%len(self.animation_list[self.action])

    def is_on_trampoline(self,trampoline):
        return (self.rect.right < trampoline.rect.right and self.rect.right > trampoline.rect.left or self.rect.left >= trampoline.rect.left and self.rect.left <= trampoline.rect.right) and self.rect.bottom > 600

    def move(self,moving_left,moving_right):
        dx = 0
        dy = 0
        if moving_left:
            dx = -self.speed 
            self.__set_action(MOVE)
            self.flip = True

        if moving_right:
            dx = self.speed
            self.__set_action(MOVE)
            self.flip = False
        
        if self.is_landing:
            self.__set_action(JUMP)

        if self.jump and not self.is_landing:
            self.jump_velocity += PLAYER_JUMP_VEL
            self.jump = False
            self.is_landing = True

        if self.fly:
            self.jump_velocity = TRAMPOLINE_VEL
            self.fly = False
            self.is_landing = True

        self.jump_velocity += GRAVITY
        dy += self.jump_velocity 

        if self.rect.bottom + dy > HEIGHT-10:
            dy =  HEIGHT-10 - self.rect.bottom
            self.jump_velocity = 0
            self.is_landing = False
        
        elif self.rect.bottom + dy > HEIGHT-200 and self.rect.left < 800 and self.rect.right > 600:
            dy =  HEIGHT-200 - self.rect.bottom
            self.jump_velocity = 0
            self.is_landing = False

        if self.__is_standing():
            self.__set_action(IDLE)
        self.__previous_coordinate(self.rect.x,self.rect.y)
        self.rect.x += dx
        self.rect.y += dy

    def draw(self, window):
        self.__update_animation()
        window.blit(pg.transform.flip(self.image,self.flip,False),self.rect)

class Trampoline:
    def __init__(self,x,y,sprites_dir,scale):
        self.animation_list = self.__load_sprites(sprites_dir,scale)
        self.action = 0
        self.sprite_index = 0
        self.image = self.animation_list[self.action][self.sprite_index]
        self.rect = self.image.get_rect()
        self.rect.center = (x,y)
        self.animation_time = 0
    
    # load all sprites for all action types
    def __load_sprites(self,sprites_dir,scale):
        sprite_list = []
        for action_type in TRAMPOLINE_ACTION:
            action_sprites = []
            for img_name in os.listdir(f'{sprites_dir}/{action_type}'):
                img = pg.image.load(os.path.join(sprites_dir,action_type,img_name))
                action_sprites.append(pg.transform.scale(img,(int(img.get_width() * scale), int(img.get_height() * scale))))
            sprite_list.append(action_sprites)
        return sprite_list

    def __update_animation(self):
        self.image = self.animation_list[self.action][self.sprite_index]
        if pg.time.get_ticks() - self.animation_time > ANIMATION_TIME:
            self.animation_time = pg.time.get_ticks()
            self.sprite_index = (self.sprite_index+1)%len(self.animation_list[self.action])

    def move(self):
        self.__update_animation()

    def draw(self, window):
        self.__update_animation()
        window.blit(self.image,self.rect)