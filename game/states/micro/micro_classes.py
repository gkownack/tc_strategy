import pygame

class Micro_Terrain():
    pass

class Micro_Grass(Micro_Terrain):
    pic = pygame.image.load('lib/graphics/grass.png')
    weight = 1
    impass = False

class Micro_Mountain(Micro_Terrain):
    pic = pygame.image.load('lib/graphics/mountain.png')
    weight = 3
    impass = False

class Micro_Tree(Micro_Terrain):
    pic = pygame.image.load('lib/graphics/tree.png')
    weight = 2
    impass = False

class Micro_Water(Micro_Terrain):
    pic = pygame.image.load('lib/graphics/water.png')
    weight = 1
    impass = True

class Micro_Square():
    rect = x = y = terrain = unit = mask = None

    def __init__(self, rect, x, y, terrain):
        self.rect = rect
        self.x = x
        self.y = y
        self.terrain = terrain

    def set_unit(self, unit):
        self.unit = unit

def distance(first, second):
    return abs(first.x - second.x) + abs(first.y - second.y)
