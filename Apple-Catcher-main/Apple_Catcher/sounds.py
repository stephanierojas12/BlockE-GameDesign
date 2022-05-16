from pygame import mixer

class Music:
    def __init__(self):
        # Msuics: Used in the Game
        self.bg_music = mixer.Sound('Sounds/bg_sound.mp3')
        self.apple_droped = mixer.Sound('Sounds/apple_dropped.mp3')
        self.apple_catched = mixer.Sound('Sounds/apple_catched.mp3')
        self.game_over = mixer.Sound('Sounds/game_over.mp3')