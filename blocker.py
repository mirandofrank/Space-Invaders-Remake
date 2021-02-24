from pygame.sprite import Sprite
import settings as sett
import pygame
#import game_object

#go = game_object.game_obj

class Blocker(Sprite):
    def __init__(self, size, color, row, column):
        Sprite.__init__(self)
        self.height = size
        self.width = size
        self.color = color
        self.image = pygame.Surface((self.width, self.height))
        self.image.fill(self.color)
        self.rect = self.image.get_rect()
        self.row = row
        self.column = column
        self.screen = sett.SCREEN

    def update(self, keys, *args):
        self.screen.blit(self.image, self.rect)
