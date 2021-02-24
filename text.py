from pygame import font

class Text(object):
    def __init__(self, text_font, size, message, color, xpos, ypos):
        self.font = font.Font(text_font, size)
        self.surface = self.font.render(message, True, color)
        self.rect = self.surface.get_rect(topleft=(xpos, ypos))

    def draw(self, surface):
        surface.blit(self.surface, self.rect)
