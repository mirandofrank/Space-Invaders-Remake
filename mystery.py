from pygame.sprite import Sprite
import settings as sett
import pygame

class Mystery(Sprite):
    def __init__(self):
        Sprite.__init__(self)
        self.image = sett.IMAGES['mystery']
        self.image = pygame.transform.scale(self.image, (75, 35))
        self.rect = self.image.get_rect(topleft=(-80, 45))
        self.row = 5
        self.moveTime = 25000
        self.direction = 1
        self.timer = pygame.time.get_ticks()
        self.mysteryEntered = pygame.mixer.Sound(sett.SOUND_PATH + 'mysteryentered.wav')
        self.mysteryEntered.set_volume(0.3)
        self.playSound = True
        self.screen = sett.SCREEN

    def update(self, keys, current_time, *args):
        reset_timer = False
        passed = current_time - self.timer
        if passed > self.moveTime:
            if (self.rect.x < 0 or self.rect.x > 800) and self.playSound:
                self.mysteryEntered.play()
                self.playSound = False
            if self.rect.x < 840 and self.direction == 1:
                self.mysteryEntered.fadeout(4000)
                self.rect.x += 2
                self.screen.blit(self.image, self.rect)
            if self.rect.x > -100 and self.direction == -1:
                self.mysteryEntered.fadeout(4000)
                self.rect.x -= 2
                self.screen.blit(self.image, self.rect)

        if self.rect.x > 830:
            self.playSound = True
            self.direction = -1
            reset_timer = True
        if self.rect.x < -90:
            self.playSound = True
            self.direction = 1
            reset_timer = True
        if passed > self.moveTime and reset_timer:
            self.timer = current_time
