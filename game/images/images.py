import pygame

file_prefix = 'lib/graphics/'
file_postfix = '.png'

class UnitImage():
    macro = micro = enemy = None

    def __init__(self, unit_file_name, enemy=""):
        self.macro = [pygame.image.load(file_prefix + 'Squad_' + enemy + unit_file_name + file_postfix),
                      pygame.image.load(file_prefix + 'Squad_' + enemy + unit_file_name + 'Anim' + file_postfix)]
        self.micro = [pygame.image.load(file_prefix + enemy + unit_file_name + file_postfix),
                      pygame.image.load(file_prefix + enemy + unit_file_name + 'Anim' + file_postfix)]
        self.enemy = enemy

units = {}
enemy = ""
for i in xrange(2):
    if i == 1:
        enemy = "Enemy"
    units[("Rogue",i)] = UnitImage('Rogue', enemy)
    units[("Melee",i)] = UnitImage('SmallSword', enemy)
    units[("Ranged",i)] = UnitImage('Ranged', enemy)
    units[("Arcane",i)] = UnitImage('ArcaneMage', enemy)
    units[("Divine",i)] = UnitImage('DivineMage', enemy)

terrain = {}
terrain["Grass"] = pygame.image.load('lib/graphics/grass.png')
terrain["Water"] = pygame.image.load('lib/graphics/water.png')
terrain["Mountain"] = pygame.image.load('lib/graphics/mountain.png')
terrain["Tree"] = pygame.image.load('lib/graphics/tree.png')
