# Developed by Subhankar Rakshit

import pygame as pg
import sys
from apple import Apple
from settings import Settings
from basket import Basket
from game_stats import GameStats
from button import Button
from scoreboard import Scoreboard
from sounds import Music

class AppleCatcher:
    def __init__(self):
        pg.init()

        self.settings = Settings()
        self.screen = pg.display.set_mode((self.settings.screen_width, \
        self.settings.screen_height), self.settings.flag)
        pg.display.set_caption('Egg Catcher')

        # Background Window Image
        self.background = pg.image.load('Apple-Catcher-main\og background.jpg')

        self.music = Music()

        self.stats = GameStats(self)
        self.sb = Scoreboard(self)
        self.basket = Basket(self)
        self.apples = pg.sprite.Group()
        # Make the Play button
        self.play_button = Button(self, "Play")

        # Getting the Screen's Rectangular
        self.screen_rect = self.screen.get_rect()

       
    def run_game(self):
        while True:
            self._check_events()
            if self.stats.game_active:
                self.basket.update()
                self._drop_apples()
                self.apples.update()
                self._check_apples_bottom()
                self._update_apples()
            self._update_screen()


    def check_for_level_up(self):
        # The game level up when the scores reach multiple of 20.
        if self.stats.score!=0 and self.stats.score%20 == 0:
            self.settings.increase_speed()
            # Increase Level
            self.stats.level += 1
            self.sb.prep_level()


    def _update_apples(self):
        '''If a apple crosses the window, it disappears'''
        for apple in self.apples.copy():
            if apple.rect.bottom >= self.screen_rect.bottom:
                self.apples.remove(apple)
        self._check_basket_apple_collisions()


    def _check_basket_apple_collisions(self):
        '''If the basket and a apple collide, add a point.'''
        collisions = pg.sprite.spritecollide(self.basket, self.apples, True)
        if collisions:
            # If collision detected add a point
            self.stats.score += self.settings.apple_points
            self.check_for_level_up()
            self.music.apple_catched.play()
            self.sb.prep_score()


    def _check_apples_bottom(self):
        '''It checks if the apple crosses the screen bottom'''
        screen_rect = self.screen.get_rect()
        for apple in self.apples.sprites():
            if apple.rect.bottom >= screen_rect.bottom:
                self._apple_hit()
                break


    def _apple_hit(self):
        '''It checks the remaining chances to miss the apple 
        from being catched and play the drop sound. If chances over, it
        plays a 'game over' sound.'''
        if self.stats.apples_left > 0:
            self.stats.apples_left -= 1
            self.music.apple_droped.play()
            self.sb.prep_apples()
        else:
            self.music.game_over.play()
            self.stats.game_active = False
            pg.mouse.set_visible(True)
            self.music.bg_music.stop()

        
    def _drop_apples(self):
        '''Drop apples from the top, randomly'''
        if len(self.apples) == 0:
                new_apple = Apple(self)
                self.apples.add(new_apple)
        if len(self.apples) == 1:
            for apple in self.apples.sprites():
                if apple.rect.bottom > 300:
                    new_apple = Apple(self)
                    self.apples.add(new_apple)
        if len(self.apples) == 2:
            for apple in self.apples.sprites():
                if apple.rect.bottom > 600:
                    new_apple = Apple(self)
                    self.apples.add(new_apple)
        if len(self.apples) == 3:
            for apple in self.apples.sprites():
                if apple.rect.bottom > 900:
                    new_apple = Apple(self)
                    self.apples.add(new_apple)
                    

    def _check_play_button(self, mouse_pos):
        """Start a new game when the player clicks Play."""
        button_clicked = self.play_button.rect.collidepoint(mouse_pos)
        if button_clicked and not self.stats.game_active:
            self.settings.initialize_dynamic_settings()
            # Reset the game statistics.
            self.stats.reset_stats()
            self.stats.game_active = True
            # Play the Background Music
            self.music.bg_music.play()

            self.sb.prep_score()
            self.sb.prep_apples()
            self.sb.prep_level()
            # Get rid of any remaining apples
            self.apples.empty()
            # Hide the mouse cursor
            pg.mouse.set_visible(False)
        
        
    def _check_events(self):
        """Respond to keypresses and mouse events."""
        for event in pg.event.get():
            if event.type == pg.QUIT:
                sys.exit()
            elif event.type == pg.MOUSEBUTTONDOWN:
                mouse_pos = pg.mouse.get_pos()
                self._check_play_button(mouse_pos)
            elif event.type == pg.KEYDOWN:
                self._check_keydown_events(event)
            elif event.type == pg.KEYUP:
                self._check_keyup_events(event)
            
                
    def _check_keydown_events(self, event):
        """Respond to keypresses."""
        if event.key == pg.K_RIGHT:
            self.basket.moving_right = True
        elif event.key == pg.K_LEFT:
            self.basket.moving_left = True
        elif event.key == pg.K_SPACE:
            self._drop_apples()

    
    def _check_keyup_events(self, event):
        """Respond to key releases."""
        if event.key == pg.K_RIGHT:
            self.basket.moving_right = False
        elif event.key == pg.K_LEFT:
            self.basket.moving_left = False


    def _update_screen(self):
        """Update images on the screen, and flip to the new screen."""
        self.screen.blit(self.background, (0,0))
        self.basket.blitme()

        for apple in self.apples.sprites():
            apple.blitme()

        # Draw the score information.
        self.sb.show_score()
        # Draw the play button if the game is inactive.
        if not self.stats.game_active:
            self.play_button.draw_button()

        pg.display.flip()


if __name__ == '__main__':
    ec = AppleCatcher()
    ec.run_game()
