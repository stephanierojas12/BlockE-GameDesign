class GameStats:
    '''Track statistics for Apple Catcher.'''
    def __init__(self, ac_game):
        self.settings = ac_game.settings
        self.game_active = False
        self.reset_stats()

    def reset_stats(self):
        self.apples_left = self.settings.apple_limit
        self.score = 0
        self.level = 1