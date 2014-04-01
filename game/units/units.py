import pygame
import config
import time

class Attributes:
    Melee, Ranged, Arcane, Divine = range(4)

class Unit():
    skills = [0 for i in xrange(4)]
    primary_attribute = team = pics = pic = pic_index = None
    last_update = time.clock()*1000

    def __init__(self, primary_attribute):
        self.primary_attribute = primary_attribute
        if primary_attribute == Attributes.Melee:
            self.pics = [pygame.image.load('lib/graphics/SmallSword.png'),
                         pygame.image.load('lib/graphics/SmallSwordAnim.png')]
        elif primary_attribute == Attributes.Ranged:
            # This should be updated when we make a ranged sprite
            self.pics = [pygame.image.load('lib/graphics/SmallSword.png'),
                         pygame.image.load('lib/graphics/SmallSwordAnim.png')]
        elif primary_attribute == Attributes.Arcane:
            self.pics = [pygame.image.load('lib/graphics/ArcaneMage.png'),
                         pygame.image.load('lib/graphics/ArcaneMageAnim.png')]
        elif primary_attribute == Attributes.Divine:
            self.pics = [pygame.image.load('lib/graphics/DivineMage.png'),
                         pygame.image.load('lib/graphics/DivineMageAnim.png')]
        self.pic = self.pics[0]
        self.pic_index = 0

    def update(self):
        now = time.clock()*1000
        if now - self.last_update > config.ANIMATION_INTERVAL:
            self.last_update = now
            if self.pic_index == 0:
                self.pic_index = 1
            elif self.pic_index == 1:
                self.pic_index = 0
            self.pic = self.pics[self.pic_index]
        

    
