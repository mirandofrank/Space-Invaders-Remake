import pygame.font
import settings as sett

class ButtonHighScores(object):
    def __init__(self, screen, msg):
        self.screen = screen
        self.screen_rect = screen.get_rect()

        #Dimensions of button
        self.width = sett.button_width + 40
        self.height = sett.button_height
        self.button_color = sett.GREEN
        self.text_color = sett.WHITE
        self.font = pygame.font.SysFont(None, 48)

        #Build the button's rect object and center it
        #High scores button will be placed lower than play button
        self.rect = pygame.Rect(0, 0, self.width, self.height)
        self.rect.centerx = self.screen_rect.centerx + 5
        self.rect.centery = 500

        #Initialized again to get rid of warnings
        self.msg_image = self.font.render(msg, True, self.text_color, self.button_color)
        self.msg_image_rect = self.msg_image.get_rect()

        #Button only needs to be prepped once
        self.prep_msg(msg)

    def prep_msg(self, msg):
        #Turn msg into a rendered image and center the text in the rect
        self.msg_image = self.font.render(msg, True, self.text_color, self.button_color)
        self.msg_image_rect = self.msg_image.get_rect()
        self.msg_image_rect.center = self.rect.center

    def draw_button(self):
        #Draw blank button then draw message
        self.screen.fill(self.button_color, self.rect)
        self.screen.blit(self.msg_image, self.msg_image_rect)
