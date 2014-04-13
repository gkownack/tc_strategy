import pygame
import config
import time
import random
from images import images

class Attributes():
    Melee = "Melee"
    Ranged = "Ranged"
    Arcane = "Arcane"
    Divine = "Divine"

class Unit():
    skills = {"Melee":0, "Ranged":0, "Arcane":0, "Divine":0}
    primary_attribute = team = pics = pic = pic_index = None
    last_update = time.clock()*1000
    stats = {"move":7}

    def __init__(self, skills):
        if skills == None:
            self.pics = images.units["Rogue"]
        else:
            best_skills = ["Melee", "Ranged", "Arcane", "Divine"]
            for skill in skills:
                best_skills = list(filter(lambda x: skills[x] >= skills[skill], best_skills))
            if len(best_skills) == 4:
                self.primary_attribute = None
                self.pics = images.units["Rogue"]
            else:
                self.primary_attribute = random.choice(best_skills)
                self.pics = images.units[self.primary_attribute]
            self.skills = skills
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
            return True
        return False
