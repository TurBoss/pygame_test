import os
from constants import ROOT_PATH, RESOURCE_DIR

import pygame

class MusicList:
    def __init__(self):
        self.current_song = 0
        self.mylist = ["02 Main Theme.ogg", "31 Demon Island.ogg", "32 Dragon In The Sky.ogg"]

    def change_music(self, song):
        self.current_song = song

    def play_music(self):
        music_path = os.path.join(ROOT_PATH,
                                  RESOURCE_DIR,
                                  "music",
                                  self.mylist[self.current_song])

        pygame.mixer.music.load(music_path)
        pygame.mixer.music.play(-1)
