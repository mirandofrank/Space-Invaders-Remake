from os import path

import pygame
from os.path import abspath, dirname

# Colors (R, G, B)
WHITE = (255, 255, 255)
GREEN = (78, 255, 87)
YELLOW = (241, 255, 0)
BLUE = (80, 255, 239)
PURPLE = (203, 0, 255)
RED = (237, 28, 36)

#Screen dimensions
screen_width = 800
screen_height = 600
pygame.init()
SCREEN = pygame.display.set_mode((screen_width, screen_height))

#Button dimensions
button_width = 200
button_height = 50

#Loading images and sounds
BASE_PATH = abspath(dirname(__file__))
FONT_PATH = BASE_PATH + '/fonts/'
IMAGE_PATH = BASE_PATH + '/images/'
SOUND_PATH = BASE_PATH + '/sounds/'
EXP_PATH = BASE_PATH + '/explosions/'

IMG_NAMES = ['ship', 'mystery',
             'enemy1_1', 'enemy1_2',
             'enemy2_1', 'enemy2_2',
             'enemy3_1', 'enemy3_2',
             'explosionblue', 'explosiongreen', 'explosionpurple',
             'laser', 'enemylaser']
IMAGES = {name: pygame.image.load(IMAGE_PATH + '{}.png'.format(name)).convert_alpha()
          for name in IMG_NAMES}

#Load explosion images
explosion_anim = {'ship_exp': []}
for i in range(1, 12):
    filename = 'exp{}.png'.format(i)
    img = pygame.image.load(path.join(EXP_PATH, filename)).convert()
    img_ship_exp = pygame.transform.scale(img, (50, 48))
    explosion_anim['ship_exp'].append(img_ship_exp)

BLOCKERS_POSITION = 450
ENEMY_DEFAULT_POSITION = 65  # Initial value for a new game
ENEMY_MOVE_DOWN = 35

FONT = FONT_PATH + 'space_invaders.ttf'


