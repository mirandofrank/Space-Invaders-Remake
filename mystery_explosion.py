from pygame.sprite import Sprite
import pygame
import settings as sett
from text import Text


class MysteryExplosion(Sprite):
    def __init__(self, mystery, score, *groups):
        super(MysteryExplosion, self).__init__(*groups)
        self.text = Text(sett.FONT, 20, str(score), sett.WHITE,
                         mystery.rect.x + 20, mystery.rect.y + 6)
        self.timer = pygame.time.get_ticks()
        self.screen = sett.SCREEN

    def update(self, current_time, *args):
        passed = current_time - self.timer
        if passed <= 200 or 400 < passed <= 600:
            self.text.draw(self.screen)
        elif 600 < passed:
            self.kill()
