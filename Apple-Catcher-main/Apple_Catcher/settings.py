import pygame as pg

class Settings:
    def __init__(self):
        screen_info = pg.display.Info()
        self.screen_width = screen_info.current_w
        self.screen_height = screen_info.current_h
        self.bg_color = (230, 230, 230)
        self.flag = pg.RESIZABLE

        # Initialize static settings
        self.apples_allowed = 3
        self.apple_limit = 3
        self.game_over = False

        # Scoring
        self.apple_points = 2

        # Levelup Scale
        self.levelup_scale = 1.1

        self.initialize_dynamic_settings()

    def initialize_dynamic_settings(self):
        self.basket_speed = 1
        self.apple_drop_speed = 0.5

    def increase_speed(self):
        self.basket_speed *= self.levelup_scale
        self.apple_drop_speed *= self.levelup_scale
