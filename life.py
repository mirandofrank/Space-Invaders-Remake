from pygame.sprite import Sprite
import settings as sett
import pygame


class Life(Sprite):
    def __init__(self, xpos, ypos):
        Sprite.__init__(self)
        self.image = sett.IMAGES['ship']
        self.image = pygame.transform.scale(self.image, (23, 23))
        self.rect = self.image.get_rect(topleft=(xpos, ypos))
        self.screen = sett.SCREEN

    def update(self, *args):
        self.screen.blit(self.image, self.rect)
