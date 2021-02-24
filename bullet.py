from pygame.sprite import Sprite
import settings as sett


class Bullet(Sprite):
    def __init__(self, xpos, ypos, direction, speed, filename, side):
        Sprite.__init__(self)
        self.image = sett.IMAGES[filename]
        self.rect = self.image.get_rect(topleft=(xpos, ypos))
        self.speed = speed
        self.direction = direction
        self.side = side
        self.filename = filename

    def update(self, keys, *args):
        sett.SCREEN.blit(self.image, self.rect)
        self.rect.y += self.speed * self.direction
        if self.rect.y < 15 or self.rect.y > 600:
            self.kill()
