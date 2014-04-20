import pygame

file_prefix = 'lib/graphics/'
file_postfix = '.png'

class UnitImage():
    macro = micro = None

    def __init__(self, unit_file_name):
        self.macro = [pygame.image.load(file_prefix + 'Squad_' + unit_file_name + file_postfix),
                      pygame.image.load(file_prefix + 'Squad_' + unit_file_name + 'Anim' + file_postfix)]
        self.micro = [pygame.image.load(file_prefix + unit_file_name + file_postfix),
                      pygame.image.load(file_prefix + unit_file_name + 'Anim' + file_postfix)]

units = {}
units["Rogue"] = UnitImage('Rogue')
units["Melee"] = UnitImage('SmallSword')
units["Ranged"] = UnitImage('Ranged')
units["Arcane"] = UnitImage('ArcaneMage')
units["Divine"] = UnitImage('DivineMage')

terrain = {}
terrain["Grass"] = pygame.image.load('lib/graphics/grass.png')
terrain["Water"] = pygame.image.load('lib/graphics/water.png')
terrain["Mountain"] = pygame.image.load('lib/graphics/mountain.png')
terrain["Tree"] = pygame.image.load('lib/graphics/tree.png')
