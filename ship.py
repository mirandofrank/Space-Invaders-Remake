import pygame
import settings as sett
from pygame.sprite import Sprite


class Ship(Sprite):
    def __init__(self):
        Sprite.__init__(self)
        self.image = sett.IMAGES['ship']
        self.rect = self.image.get_rect(topleft=(375, 540))
        self.speed = 5
        self.screen = sett.SCREEN

    def update(self, keys, *args):
        if keys[pygame.K_LEFT] and self.rect.x > 10:
            self.rect.x -= self.speed
        if keys[pygame.K_RIGHT] and self.rect.x < 740:
            self.rect.x += self.speed
        self.screen.blit(self.image, self.rect)
