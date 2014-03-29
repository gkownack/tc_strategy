import pygame

class Macro_Terrain():
    pass

class Macro_Grass(Macro_Terrain):
    pic = pygame.image.load('lib/graphics/grass.png')

class Macro_SmallSword(Macro_Terrain):
    pic = pygame.image.load('lib/graphics/SmallSword.png')

class Macro_SmallSwordAnim(Macro_Terrain):
    pic = pygame.image.load('lib/graphics/SmallSwordAnim.png')

class Macro_Square():
    rect = x = y = terrain = None

    def __init__(self, rect, x, y, terrain):
        self.rect = rect
        self.x = x
        self.y = y
        self.terrain = terrain
