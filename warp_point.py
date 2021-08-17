import pygame


class WarpPoint(pygame.sprite.Sprite):

    def __init__(self, warp):
        super(WarpPoint, self).__init__()

        self.warp = warp
        self.player = None
        self.player_inside = False

    def get_rect(self):
        return pygame.Rect(self.warp.x, self.warp.y, self.warp.width, self.warp.height)

    def go_inside(self, player):
        self.player_inside = True

    def go_outisde(self):
        self.player = None
        self.player_inside = False

    def get_player(self):
        return self.player_inside