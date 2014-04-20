import pygame
from images import images

class Terrain():
    pass

class Grass(Terrain):
    terrain_type = 'Grass'
    pic = images.terrain['Grass']
    weight = 1
    impass = False

class Mountain(Terrain):
    terrain_type = 'Mountain'
    pic = images.terrain['Mountain']
    weight = 3
    impass = False

class Tree(Terrain):
    terrain_type = 'Tree'
    pic = images.terrain['Tree']
    weight = 2
    impass = False

class Water(Terrain):
    terrain_type = 'Water'
    pic = images.terrain['Water']
    weight = 1
    impass = True

def toString(t):
    line1 = t.terrain_type + "\n"
    if t.impass:
        line2 = "Impassable\n"
    else:
        line2 = "Passable\tCost: %d\n" % t.weight
    return line1 + line2 + "\n"
