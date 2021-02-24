from pygame.sprite import Sprite
import settings as sett
import pygame


class EnemyExplosion(Sprite):
    def __init__(self, enemy, *groups):
        super(EnemyExplosion, self).__init__(*groups)
        self.image = pygame.transform.scale(self.get_image(enemy.row), (40, 35))
        self.image2 = pygame.transform.scale(self.get_image(enemy.row), (50, 45))
        self.rect = self.image.get_rect(topleft=(enemy.rect.x, enemy.rect.y))
        self.timer = pygame.time.get_ticks()
        self.screen = sett.SCREEN

    @staticmethod
    def get_image(row):
        img_colors = ['purple', 'blue', 'blue', 'green', 'green']
        return sett.IMAGES['explosion{}'.format(img_colors[row])]

    def update(self, current_time, *args):
        passed = current_time - self.timer
        if passed <= 100:
            self.screen.blit(self.image, self.rect)
        elif passed <= 200:
            self.screen.blit(self.image2, (self.rect.x - 6, self.rect.y - 6))
        elif 400 < passed:
            self.kill()
