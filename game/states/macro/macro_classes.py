import pygame

class Macro_Terrain():
    pass

class Macro_Grass(Macro_Terrain):
    pic = pygame.image.load('lib/graphics/grass.png')
    move = 1
    impass = False

class Macro_Mountain(Macro_Terrain):
    pic = pygame.image.load('lib/graphics/mountain.png')
    move = 3
    impass = False

class Macro_Tree(Macro_Terrain):
    pic = pygame.image.load('lib/graphics/tree.png')
    move = 2
    impass = False

class Macro_Water(Macro_Terrain):
    pic = pygame.image.load('lib/graphics/water.png')
    move = 1
    impass = True

class Macro_Square():
    rect = x = y = terrain = unit = mask = None

    def __init__(self, rect, x, y, terrain):
        self.rect = rect
        self.x = x
        self.y = y
        self.terrain = terrain

    def set_unit(self, unit):
        self.unit = unit
