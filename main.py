import os
import time
from collections import deque

import pygame

from pygame import JOYAXISMOTION, KEYUP, JOYBUTTONDOWN, JOYBUTTONUP
from pygame.locals import K_UP, K_DOWN, K_LEFT, K_RIGHT, K_MINUS, K_PLUS, K_ESCAPE, K_BACKSPACE
from pygame.locals import KEYDOWN, VIDEORESIZE, QUIT

from pytmx.util_pygame import load_pygame

import pyscroll
import pyscroll.data
from pyscroll.group import PyscrollGroup

from constants import RESOURCE_DIR, RED, GRAY
from npc import Npc
from player import Player


# simple wrapper to keep the screen resizeable
def init_screen(width: int, height: int) -> pygame.Surface:
    screen = pygame.display.set_mode((width, height))
    return screen


class Game:
    """This class is a basic game.
    This class will load data, create a pyscroll group, a hero object.
    It also reads input and moves the Hero around the map.
    Finally, it uses a pyscroll group to render the map and Hero.
    """

    map_path = "mapa.tmx"

    def __init__(self, screen: pygame.Surface) -> None:
        self.screen = screen

        self.running = False
        self.shooting = False

        base_dir = directory_path = os.getcwd()
        pygame.mixer.music.load(os.path.join(base_dir, RESOURCE_DIR, "music", "02 Main Theme.ogg"))
        pygame.mixer.music.play(-1)

        # load data from pytmx
        tmx_data = load_pygame(self.map_path)

        # setup level geometry with simple pygame rects, loaded from pytmx
        self.walls = []

        for obj in tmx_data.objects:
            self.walls.append(pygame.Rect(obj.x, obj.y, obj.width, obj.height))

        # create new data source for pyscroll
        map_data = pyscroll.data.TiledMapData(tmx_data)

        # create new renderer (camera)
        self.map_layer = pyscroll.BufferedRenderer(
            map_data, screen.get_size(), clamp_camera=False, tall_sprites=1
        )
        self.map_layer.zoom = 2

        # pyscroll supports layered rendering.  our map has 3 'under' layers
        # layers begin with 0, so the layers are 0, 1, and 2.
        # since we want the sprite to be on top of layer 1, we set the default
        # layer for sprites as 2
        self.group = PyscrollGroup(map_layer=self.map_layer, default_layer=2)

        self.hero_move_speed = 250  # pixels per second
        self.player = Player(self, image="pocky.png")

        self.npc_1 = Npc(self, self.player, "pocky.png", True)

        # put the hero in the center of the map
        self.player.position = [400, 300]
        self.npc_1.position = [300, 300]

        # add our hero to the group
        self.group.add(self.player)
        self.group.add(self.npc_1)

        self.init_textedit()


    def init_textedit(self):

        self.text = ""
        self.font = pygame.font.SysFont(None, 64)
        self.text_image = self.font.render(self.text, True, RED)

        self.text_rect = self.text_image.get_rect()
        self.text_rect.topleft = (20, 20)

        self.text_cursor = pygame.locals.Rect(self.text_rect.topright, (3, self.text_rect.height))

    def add_bullet(self, bullet):
        self.group.add(bullet)

    def draw(self) -> None:

        # center the map/screen on our Hero
        self.group.center(self.player.rect.center)

        # draw the map and all sprites
        self.group.draw(self.screen)


        self.screen.blit(self.text_image, self.text_rect)
        if time.time() % 1 > 0.5:
            pygame.draw.rect(self.screen, RED, self.text_cursor)

    def handle_input(self) -> None:
        """Handle pygame input events"""
        poll = pygame.event.poll

        dead_zone = 0.25

        event = poll()

        while event:
            if event.type == QUIT:
                self.running = False
                break

            elif event.type == JOYAXISMOTION:
                if event.axis == 0 or event.axis == 1:
                    if abs(event.value) > dead_zone:

                        self.player.velocity[event.axis] = event.value * self.hero_move_speed
                    else:
                        self.player.velocity[event.axis] = 0
                elif event.axis == 3:
                    if event.value > dead_zone or event.value < dead_zone:
                        self.map_layer.zoom += event.value / 10

            elif event.type == JOYBUTTONDOWN:
                if event.button == 2:
                    self.npc_1.shoot()
                    self.player.shoot()

            elif event.type == JOYBUTTONUP:
                if event.button == 2:
                    pass

            elif event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    break

                elif event.key == K_LEFT:
                    self.player.velocity[0] = -self.hero_move_speed

                elif event.key == K_RIGHT:
                    self.player.velocity[0] = self.hero_move_speed

                elif event.key == K_UP:
                    self.player.velocity[1] = -self.hero_move_speed

                elif event.key == K_DOWN:
                    self.player.velocity[1] = self.hero_move_speed

                elif event.key == K_BACKSPACE:
                    if len(self.text) > 0:
                        self.text = self.text[:-1]
                        self.text_image = self.font.render(self.text, True, RED)
                        self.text_rect.size = self.text_image.get_size()
                        self.text_cursor.topleft = self.text_rect.topright
                else:
                    self.text += event.unicode
                    self.text_image = self.font.render(self.text, True, RED)
                    self.text_rect.size = self.text_image.get_size()
                    self.text_cursor.topleft = self.text_rect.topright

            elif event.type == KEYUP:
                if event.key == K_LEFT or event.key == K_RIGHT:
                    self.player.velocity[0] = 0
                elif event.key == K_UP or event.key == K_DOWN:
                    self.player.velocity[1] = 0

            # this will be handled if the window is resized
            elif event.type == VIDEORESIZE:
                self.screen = init_screen(event.w, event.h)
                self.map_layer.set_size((event.w, event.h))

            event = poll()

    def update(self, dt):
        """Tasks that occur over time should be handled here"""
        self.group.update(dt)

        # check if the sprite's feet are colliding with wall
        # sprite must have a rect called feet, and move_back method,
        # otherwise this will fail
        for sprite in self.group.sprites():
            if sprite.feet.collidelist(self.walls) > -1:
                sprite.move_back(dt)

        self.text = f"X: {self.npc_1.position[0]:.2f} Y: {self.npc_1.position[1]:.2f}"
        self.text_image = self.font.render(self.text, True, RED)

        self.text_rect = self.text_image.get_rect()
        self.text_rect.topleft = (20, 20)

        self.text_cursor = pygame.locals.Rect(self.text_rect.topright, (3, self.text_rect.height))


    def run(self):
        """Run the game loop"""
        clock = pygame.time.Clock()
        self.running = True

        times = deque(maxlen=30)

        try:
            while self.running:
                dt = clock.tick() / 1000
                times.append(clock.get_fps())

                self.handle_input()
                self.update(dt)
                self.draw()

                pygame.display.flip()

        except KeyboardInterrupt:
            self.running = False


def main() -> None:
    pygame.init()
    pygame.font.init()
    pygame.joystick.init()
    joysticks = [pygame.joystick.Joystick(x) for x in range(pygame.joystick.get_count())]

    if joysticks:
        print("Joystick found:")

    for joystick in joysticks:
        print(f"\t1 {joystick.get_name()}")

    screen = init_screen(1024, 768)
    pygame.display.set_caption("Turbo Pocky Rocky - An epic journey.")

    try:
        game = Game(screen)
        game.run()
    except KeyboardInterrupt:
        pass
    finally:
        pygame.quit()


if __name__ == "__main__":
    main()
