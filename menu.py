
import os

import pygame
from constants import RESOURCE_DIR, RED, WHITE

from cursor import Cursor
from text_sprite import TextSprite
from dialog import Dialog
from pygame import JOYAXISMOTION, KEYUP, JOYBUTTONDOWN, JOYBUTTONUP, KEYDOWN, KEYUP
from pygame.locals import K_UP, K_DOWN, K_LEFT, K_RIGHT, K_MINUS, K_PLUS, K_ESCAPE, K_BACKSPACE, K_RETURN
from pygame.locals import QUIT


class Menu:
    def __init__(self, options):

        self.options = options
        self.index = None
        self.cursor = Cursor(600, 525, 3, 50)

        self.sprite_group = pygame.sprite.Group()

        base_dir = os.path.dirname(os.path.abspath(__file__))
        self.image_path = os.path.join(base_dir, RESOURCE_DIR, "menu", "background.png")
        self.background = pygame.image.load(self.image_path)

        self.dialog = Dialog(440, 500, 220, 180)

        self.sprite_group.add(self.dialog)

        for name, menu in self.options.items():
            for key, option in menu.items():
                text = TextSprite(option)
                self.sprite_group.add(text)

        self.sprite_group.add(self.cursor)

    def draw(self, screen):
        screen.blit(self.background, (0, 0))
        self.sprite_group.draw(screen)
        # print("MENU DRAW")

    def update(self, dt):

        self.sprite_group.update(dt)

        # print("MENU DT")
    def handle_input(self, event):

        if event.type == JOYAXISMOTION:
            if event.axis == 1:  # Y Axis = 1
                if round(event.value) == -1.0:
                    self.cursor.move_up()
                elif round(event.value) == 1.0:
                    self.cursor.move_down()

        elif event.type == JOYBUTTONDOWN:

            if event.button == 1:
                self.index = self.cursor.get_position()
            elif event.button == 0:
                self.index = self.cursor.get_position()

        elif event.type == JOYBUTTONUP:
            if event.button == 2:
                pass

        elif event.type == KEYDOWN:
            if event.key == K_UP:
                self.cursor.move_up()

            elif event.key == K_DOWN:
                self.cursor.move_down()

            elif event.key == K_RETURN:
                self.index = self.cursor.get_position()

    def get_mode(self):
        return self.index
