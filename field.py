import os

import pygame

import pyscroll
import pyscroll.data
from pyscroll.group import PyscrollGroup

from pygame import Rect, JOYAXISMOTION, JOYBUTTONDOWN, JOYBUTTONUP, KEYUP, KEYDOWN
from pygame.locals import K_UP, K_DOWN, K_LEFT, K_RIGHT, K_MINUS, K_PLUS, K_ESCAPE, K_BACKSPACE

from pytmx import load_pygame

from constants import RESOURCE_DIR, RED
from warp_point import WarpPoint
from player import Player
from npc import Npc


class Field(object):
    def __init__(self, name, screen_size):

        self.map_name = name
        self.screen_size = screen_size

        self.fading = None
        self.fade_end = False

        self.alpha = 0
        sr = Rect(0, 0, screen_size[0], screen_size[1])

        self.fade_rect = pygame.Surface(sr.size)
        self.fade_rect.fill((0, 0, 0))

        self.base_dir = os.path.dirname(os.path.abspath(__file__))

        self.initialize()

    def initialize(self):

        self.file_path = os.path.join(self.base_dir, RESOURCE_DIR, "maps", self.map_name)
        # load data from pytmx
        self.tmx_data = load_pygame(self.file_path)

        # create new data source for pyscroll
        self.map_data = pyscroll.data.TiledMapData(self.tmx_data)

        # create new renderer (camera)
        self.map_layer = pyscroll.BufferedRenderer(self.map_data,
                                                   self.screen_size,
                                                   clamp_camera=False,
                                                   tall_sprites=1
                                                   )
        self.map_layer.zoom = 2

        # pyscroll supports layered rendering.  our map has 3 'under' layers
        # layers begin with 0, so the layers are 0, 1, and 2.
        # since we want the sprite to be on top of layer 1, we set the default
        # layer for sprites as 2
        self.group = PyscrollGroup(map_layer=self.map_layer, default_layer=2)

        self.hero_move_speed = 250  # pixels per second

        self.player = Player(self, image="pocky.png")

        self.npcs = []

        self.npc_1 = Npc(self, self.player, "rocky.png", 0, 0, 34, 34, follower=True, wanderer=False)
        self.charly = Npc(self, self.player, "rocky.png", 0, 0, 34, 34, follower=False, wanderer=True)

        self.npcs.append(self.npc_1)
        self.npcs.append(self.charly)

        # put the hero in the center of the map
        self.player.position = [400, 300]
        self.npc_1.position = [300, 300]

        # add our hero to the group
        self.group.add(self.player)
        self.group.add(self.npc_1)
        self.group.add(self.charly)

        # setup level geometry with simple pygame rects, loaded from pytmx
        self.walls = []
        self.warps = dict()
        self.spawns = dict()

        for obj in self.tmx_data.objects:
            if obj.type == "warp":
                warp = WarpPoint(obj, "warp.png", 30)
                self.warps[obj.name] = warp
                self.group.add(warp)
            elif obj.type == "spawn":
                print("SPAWN FOUND")
                self.spawns[obj.name] = (obj.x, obj.y)
            else:
                self.walls.append(Rect(obj.x, obj.y, obj.width, obj.height))

        for name, spawn in self.spawns.items():
            self.charly.position = self.spawns[name]

    def handle_input(self, event):

        dead_zone = 0.25

        if event.type == JOYAXISMOTION:
            if event.axis == 0 or event.axis == 1:
                if abs(event.value) > dead_zone:

                    self.player.velocity[event.axis] = event.value * self.hero_move_speed
                else:
                    self.player.velocity[event.axis] = 0

            elif event.axis == 3:
                if event.value > dead_zone or event.value < dead_zone:
                    self.map_layer.zoom += event.value / 10

        elif event.type == JOYBUTTONDOWN:
            if event.button == 1:
                self.npc_1.shoot()
                self.player.shoot()

            elif event.button == 0:
                for name, warp in self.warps.items():
                    if warp.get_player():
                        map_name = warp.get_warp_map()
                        print(f"Change Field {map_name} from warp name {name}")
                        self.change_field(map_name)

        elif event.type == JOYBUTTONUP:
            if event.button == 2:
                pass

        elif event.type == KEYDOWN:
            if event.key == K_LEFT:
                self.player.velocity[0] = -self.hero_move_speed

            elif event.key == K_RIGHT:
                self.player.velocity[0] = self.hero_move_speed

            elif event.key == K_UP:
                self.player.velocity[1] = -self.hero_move_speed

            elif event.key == K_DOWN:
                self.player.velocity[1] = self.hero_move_speed

        elif event.type == KEYUP:
            if event.key == K_LEFT or event.key == K_RIGHT:
                self.player.velocity[0] = 0
            elif event.key == K_UP or event.key == K_DOWN:
                self.player.velocity[1] = 0

    def update(self, dt):
        self.group.update(dt)

        # check if the sprite's feet are colliding with wall
        # sprite must have a rect called feet, and move_back method,
        # otherwise this will fail
        for sprite in self.group.sprites():
            if isinstance(sprite, Player):

                if sprite.feet.collidelist(self.walls) > -1:
                    sprite.move_back(dt)
                # elif sprite.rect.collidelist(self.npcs) > -1:
                #     sprite.move_back(dt)

                for name, warp in self.warps.items():
                    if sprite.feet.colliderect(warp.get_rect()):
                        self.warps[name].go_inside(self.player)
                    else:
                        self.warps[name].go_outisde()

            elif isinstance(sprite, Npc):
                if sprite.feet.collidelist(self.walls) > -1:
                    sprite.move_back(dt)

                elif sprite.feet.colliderect(self.player.get_rect()):
                    sprite.velocity[0] = 0
                    sprite.velocity[1] = 0

        if self.fading == "IN":
            fade_speed = 0.25
            self.alpha += fade_speed
            if self.alpha >= 255:
                self.fading = None
                self.fade_end = True

        elif self.fading == "OUT":
            fade_speed = 0.25
            self.alpha -= fade_speed
            if self.alpha <= 0:
                self.fading = None

        if self.fade_end is True:
            self.initialize()
            self.fade_end = False
            self.fading = "OUT"

    def draw(self, screen):

        # center the map/screen on our Hero
        self.group.center(self.player.rect.center)

        # draw the map and all sprites
        self.group.draw(screen)

        if self.fading is not None:
            self.fade_rect.set_alpha(self.alpha)
            screen.blit(self.fade_rect, (0, 0))

    def add_bullet(self, bullet):
        self.group.add(bullet)

    def change_field(self, name):
        self.fading = "IN"
        self.map_name = name
