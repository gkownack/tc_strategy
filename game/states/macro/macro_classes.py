import pygame

class Macro_Terrain():
    pass

class Macro_Grass(Macro_Terrain):
    pic = pygame.image.load('lib/graphics/grass.png')
    weight = 1
    impass = False

class Macro_Mountain(Macro_Terrain):
    pic = pygame.image.load('lib/graphics/mountain.png')
    weight = 3
    impass = False

class Macro_Tree(Macro_Terrain):
    pic = pygame.image.load('lib/graphics/tree.png')
    weight = 2
    impass = False

class Macro_Water(Macro_Terrain):
    pic = pygame.image.load('lib/graphics/water.png')
    weight = 1
    impass = True

class Macro_Square():
    rect = x = y = terrain = squad = mask = None

    def __init__(self, rect, x, y, terrain):
        self.rect = rect
        self.x = x
        self.y = y
        self.terrain = terrain

    def set_squad(self, squad):
        self.squad = squad
