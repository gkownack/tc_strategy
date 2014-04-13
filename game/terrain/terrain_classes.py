import pygame

class Terrain():
    pass

class Grass(Terrain):
    pic = pygame.image.load('lib/graphics/grass.png')
    weight = 1
    impass = False

class Mountain(Terrain):
    pic = pygame.image.load('lib/graphics/mountain.png')
    weight = 3
    impass = False

class Tree(Terrain):
    pic = pygame.image.load('lib/graphics/tree.png')
    weight = 2
    impass = False

class Water(Terrain):
    pic = pygame.image.load('lib/graphics/water.png')
    weight = 1
    impass = True


