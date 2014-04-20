import pygame
from terrain import terrain_classes

class Micro_Square():
    rect = x = y = terrain = unit = mask = None

    def __init__(self, rect, x, y, terrain):
        self.rect = rect
        self.x = x
        self.y = y
        self.terrain = terrain

    def set_unit(self, unit):
        self.unit = unit

    def __str__(self):
        if self.unit == None:
            return terrain_classes.toString(self.terrain)
        else:
            return self.unit.__str__()

def distance(first, second):
    return abs(first.x - second.x) + abs(first.y - second.y)
