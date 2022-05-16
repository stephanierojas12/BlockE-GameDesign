import pygame
import random
from pygame.sprite import Sprite

class Apple(Sprite):
    '''A class to manage the Apples'''
    def __init__(self, ac_game):
        '''Initialize the apple and set its starting position.'''
        super().__init__()
        self.screen = ac_game.screen
        self.settings = ac_game.settings
        self.screen_rect = ac_game.screen.get_rect()

        # Load the Apple Image
        self.image = pygame.image.load('Images/apple.bmp')
        self.rect = self.image.get_rect()

        # Define the location from where the apple will enter
        self.rect.x = random.randrange(20, self.screen_rect.right-30)
        self.rect.y = 0
        
        # Store the decimal value for the apple's vertical position.
        self.y = float(self.rect.y)


    def update(self):
        self.y += self.settings.apple_drop_speed
        self.rect.y = self.y


    def blitme(self):
        """Draw the basket at its current location"""
        self.screen.blit(self.image, self.rect)
