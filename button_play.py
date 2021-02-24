import pygame.font
import settings as sett

class ButtonPlay(object):
    def __init__(self, screen, msg):
        # Initialize the button attributes
        self.screen = screen
        self.screen_rect = screen.get_rect()

        # Set the dimensions and properties of the button
        self.width = sett.button_width
        self.height = sett.button_height
        self.button_color = sett.GREEN
        self.text_color = sett.WHITE
        self.font = pygame.font.SysFont(None, 48)

        # Build the button's rect object and center it
        self.rect = pygame.Rect(0, 0, self.width, self.height)
        #self.rect.center = self.screen_rect.center
        self.rect.centerx = self.screen_rect.centerx
        self.rect.centery = 200

        #Initialized again to get rid of warnings
        self.msg_image = self.font.render(msg, True, self.text_color, self.button_color)
        self.msg_image_rect = self.msg_image.get_rect()

        # The button message needs to be prepped only once
        self.prep_msg(msg)

    def prep_msg(self, msg):
        # Turn msg into a rendered image and center text on the button
        self.msg_image = self.font.render(msg, True, self.text_color, self.button_color)
        self.msg_image_rect = self.msg_image.get_rect()
        self.msg_image_rect.center = self.rect.center

    def draw_button(self):
        # Draw blank button and then draw message
        self.screen.fill(self.button_color, self.rect)
        self.screen.blit(self.msg_image, self.msg_image_rect)
