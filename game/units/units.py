import pygame

class Attributes:
    Melee, Ranged, Arcane, Divine = range(4)

class Unit():
    skills = [0 for i in xrange(4)]
    primary_attribute = team = pic = None

    def __init__(self, primary_attribute):
        self.primary_attribute = primary_attribute
        if primary_attribute == Attributes.Melee:
            self.pic = pygame.image.load('lib/graphics/SmallSword.png')
        elif primary_attribute == Attributes.Ranged:
            self.pic = None
        elif primary_attribute == Attributes.Arcane:
            self.pic = pygame.image.load('lib/graphics/ArcaneMage.png')
        elif primary_attribute == Attributes.Divine:
            self.pic = pygame.image.load('lib/graphics/DivineMage.png')

    
