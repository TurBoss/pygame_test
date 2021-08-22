import pygame


class WarpPoint(pygame.sprite.Sprite):

    def __init__(self, warp):
        super(WarpPoint, self).__init__()

        self.warp = warp
        # for name, property in self.warp.properties.items():
        #     print(name, property)

        self.map_name = self.warp.properties.get("Map")

        self.player_inside = False

    def get_rect(self):
        return pygame.Rect(self.warp.x,
                           self.warp.y,
                           self.warp.width,
                           self.warp.height)

    def go_inside(self, player):
        # print("IN")
        self.player_inside = True

    def go_outisde(self):
        # print("OUT")
        self.player_inside = False

    def get_player(self):
        return self.player_inside

    def get_warp_map(self):
        return self.map_name
