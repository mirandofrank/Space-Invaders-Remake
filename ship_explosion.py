import pygame
from pygame.sprite import Sprite
import settings as sett


class ShipExplosion(Sprite):
    def __init__(self, ship, *groups):
        super(ShipExplosion, self).__init__(*groups)
        self.image = sett.explosion_anim['ship_exp'][0]
        self.rect = self.image.get_rect(topleft=(ship.rect.x, ship.rect.y))
        self.last_update = pygame.time.get_ticks()
        self.frame = 0                          #at frame 0
        self.frame_rate = 50                    #how long to wait between frames
        self.screen = sett.SCREEN

    def update(self, current_time, *args):
        now = pygame.time.get_ticks()
        if now - self.last_update > self.frame_rate:
            self.screen.blit(sett.explosion_anim['ship_exp'][self.frame], self.rect)
            self.last_update = now
            self.frame += 1
            if self.frame == len(sett.explosion_anim['ship_exp']):
                self.kill()
            else:
                center = self.rect.center
                self.image = sett.explosion_anim['ship_exp'][self.frame]
                self.rect = self.image.get_rect()
                self.rect.center = center


