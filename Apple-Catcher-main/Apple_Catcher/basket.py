import pygame

class Basket:
    '''A class to manage the Basket'''
    def __init__(self, ac_game):
        '''Initialize the basket and set its starting position.'''
        self.screen = ac_game.screen
        self.settings = ac_game.settings
        self.screen_rect = ac_game.screen.get_rect()

        # Load the Basket image
        self.image = pygame.image.load('Images/basket.bmp')
        self.rect = self.image.get_rect()
        self.rect.midbottom = self.screen_rect.midbottom
        
        # Store the decimal value for the basket's horizontal position.
        self.x = float(self.rect.x)

        # Movement flag
        self.moving_right = False
        self.moving_left = False

    def update(self):
        """Update the basket position based on the movement flag."""
        # Update the basket's x value, not the rect.
        if self.moving_right and self.rect.right < self.screen_rect.right:
            self.x += self.settings.basket_speed
        if self.moving_left and self.rect.left > 0:
            self.x -= self.settings.basket_speed

        # Update rect object from self.x
        self.rect.x = self.x

    def blitme(self):
        """Draw the basket at its current location"""
        self.screen.blit(self.image, self.rect)