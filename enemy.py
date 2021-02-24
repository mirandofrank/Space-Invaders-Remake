from pygame.sprite import Sprite
import settings as sett
#import game_object as go
import pygame

class Enemy(Sprite):
    def __init__(self, row, column):
        Sprite.__init__(self)
        self.row = row
        self.column = column
        self.images = []
        self.load_images()
        self.index = 0
        self.image = self.images[self.index]
        self.rect = self.image.get_rect()
        self.screen = sett.SCREEN

    def toggle_image(self):
        self.index += 1
        if self.index >= len(self.images):
            self.index = 0
        self.image = self.images[self.index]

    def update(self, *args):
        self.screen.blit(self.image, self.rect)

    def load_images(self):
        images = {0: ['1_2', '1_1'],
                  1: ['2_2', '2_1'],
                  2: ['2_2', '2_1'],
                  3: ['3_1', '3_2'],
                  4: ['3_1', '3_2'],
                  }
        img1, img2 = (sett.IMAGES['enemy{}'.format(img_num)] for img_num in
                      images[self.row])
        self.images.append(pygame.transform.scale(img1, (40, 35)))
        self.images.append(pygame.transform.scale(img2, (40, 35)))
