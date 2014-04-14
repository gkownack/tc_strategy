import pygame
from images import images

class Terrain():
    pass

class Grass(Terrain):
    pic = images.terrain['Grass']
    weight = 1
    impass = False

class Mountain(Terrain):
    pic = images.terrain['Mountain']
    weight = 3
    impass = False

class Tree(Terrain):
    pic = images.terrain['Tree']
    weight = 2
    impass = False

class Water(Terrain):
    pic = images.terrain['Water']
    weight = 1
    impass = True


