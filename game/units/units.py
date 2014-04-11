import pygame
import config
import time

class Attributes:
    Melee = "Melee"
    Ranged = "Ranged"
    Arcane = "Arcane"
    Divine = "Divine"

class Unit():
    skills = {"Melee":0, "Ranged":0, "Arcane":0, "Divine":0}
    primary_attribute = team = pics = pic = pic_index = None
    last_update = time.clock()*1000
    stats = {"move":7}

    def __init__(self, primary_attribute):
        self.skills[primary_attribute] = 1
        self.primary_attribute = primary_attribute
        self.pics = {}
        self.pics["Melee"] = [pygame.image.load('lib/graphics/SmallSword.png'),
                              pygame.image.load('lib/graphics/SmallSwordAnim.png')]

        self.pics["Ranged"] = [pygame.image.load('lib/graphics/SmallSword.png'),      # change when we make ranged sprite
                               pygame.image.load('lib/graphics/SmallSwordAnim.png')] # change when we make ranged sprite

        self.pics["Arcane"] = [pygame.image.load('lib/graphics/ArcaneMage.png'),
                               pygame.image.load('lib/graphics/ArcaneMageAnim.png')]

        self.pics["Divine"] = [pygame.image.load('lib/graphics/DivineMage.png'),
                               pygame.image.load('lib/graphics/DivineMageAnim.png')]
	'''
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
	'''
        self.pic = self.pics[self.primary_attribute][0]
        self.pic_index = 0

    def update(self):
        now = time.clock()*1000
        if now - self.last_update > config.ANIMATION_INTERVAL:
            self.last_update = now
            if self.pic_index == 0:
                self.pic_index = 1
            elif self.pic_index == 1:
                self.pic_index = 0
            self.pic = self.pics[self.primary_attribute][self.pic_index]
            return True
        return False
