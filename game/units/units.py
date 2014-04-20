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
    skill_names = [Melee, Ranged, Arcane, Divine]

class Squad():
    HALF_BOXSIDE = config.MACRO_BOXSIDE/2
    pic = pygame.Surface((HALF_BOXSIDE, HALF_BOXSIDE))
    units = []
    stats = {"move": 8}

    def __init__(self, units):
        self.units = units

    def update(self):
        for unit in self.units:
            unit.update()
        self.pic.blit(self.units[0].macro_pic, (0, 0))
        self.pic.blit(self.units[1].macro_pic, (self.HALF_BOXSIDE, 0))
        self.pic.blit(self.units[2].macro_pic, (0, self.HALF_BOXSIDE))
        self.pic.blit(self.units[3].macro_pic, (self.HALF_BOXSIDE, self.HALF_BOXSIDE))

class Unit():
    skills = {} # Initialized to have a skill for each map
    uses = {} # Number of times each skill has been used
    level_ups = {} # Number of times each skill increases at next level-up
    team = 0
    level = 0
    upgrades = 0
    primary_attribute = team = pics = macro_pic = micro_pic = pic_index = None
    last_update = time.clock()*1000
    stats = {} # Initialized to include fields: "move", "max_hp", "cur_hp", "luck", "phys_def", "mag_def"
    can_move = False
    can_attack = False

    def __init__(self, skills={"Melee":4,"Ranged":4,"Arcane":4,"Divine":4}, team=0):
        self.skills = skills.copy()
        self.stats = {"move":7} # level_up() will initialize the rest of the stats
        self.level_ups = {skill:0 for skill in Attributes.skill_names}
        self.uses = {skill:0 for skill in Attributes.skill_names}
        self.team = team
        self.skills = skills
        total_skills = 0
        for k in self.skills:
            total_skills += self.skills[k]
        self.level = max([0,(total_skills / 5) - 1])
        self.level_up()
        self.macro_pic = self.pics.macro[0]
        self.micro_pic = self.pics.micro[0]
        self.pic_index = 0
        self.can_move = False
        self.can_attack = False

    def update(self):
        now = time.clock()*1000
        if now - self.last_update > config.ANIMATION_INTERVAL:
            self.last_update = now
            if self.pic_index == 0:
                self.pic_index = 1
            elif self.pic_index == 1:
                self.pic_index = 0
            self.macro_pic = self.pics.macro[self.pic_index]
            self.micro_pic = self.pics.micro[self.pic_index]
            return True
        return False

    def is_dead(self):
        return self.stats["cur_hp"] <= 0

    def level_up(self):
        self.upgrades = 0
        self.level += 1
        best_skill_val = 0
        best_skill = [self.primary_attribute]

        # Update primary stats
        for skill in Attributes.skill_names:
            self.skills[skill] += self.level_ups[skill] + 1
            self.level_ups[skill] = 0

            if self.skills[skill] > best_skill_val:
                best_skill_val = self.skills[skill]
                best_skill = [skill]
            elif self.skills[skill] == best_skill_val:
                best_skill.append(skill)

        # Determine best skill and picture
        best_skills = ["Melee", "Ranged", "Arcane", "Divine"]
        for skill in self.skills:
            best_skills = list(filter(lambda x: self.skills[x] >= self.skills[skill], best_skills))
        if len(best_skills) == 4:
            self.primary_attribute = None
            self.pics = images.units["Rogue"]
        elif self.primary_attribute in best_skills:
            self.pics = images.units[self.primary_attribute]
        else:
            self.primary_attribute = random.choice(best_skills)
            self.pics = images.units[self.primary_attribute]

        # Update secondary stats
        self.stats["phys_def"] = (self.skills["Melee"] + self.skills["Ranged"])/3
        self.stats["mag_def"] = (self.skills["Arcane"] + self.skills["Divine"])/3
        self.stats["luck"] = (self.skills["Ranged"] + self.skills["Arcane"])/3
        self.stats["max_hp"] = 10*(self.level + (self.skills["Melee"] + self.skills["Divine"])/5)

        # max out current hp
        self.stats["cur_hp"] = self.stats["max_hp"]

    def update_health(self, attack_stat, opp_team, attack_type):
        if attack_type == "Melee" or attack_type == "Ranged":
            self.stats["cur_hp"] -= max([1, attack_stat-self.stats["phys_def"]])
        elif attack_type == "Arcane":
            self.stats["cur_hp"] -= max([1, attack_stat-self.stats["mag_def"]])
        else:
            # Divine
            modifier = -1
            if self.team == opp_team:
                 modifier = 1
            self.stats["cur_hp"] += modifier*max([1, attack_stat + modifier*self.stats["mag_def"]])
            self.stats["cur_hp"] = min([self.stats["cur_hp"], self.stats["max_hp"]])

    def attack(self, target, attack_type):
        self.uses[attack_type] += target.level
        if self.uses[attack_type] > self.level*self.level*5:
            self.uses[attack_type] = 0
            self.level_ups[attack_type] += 1
            self.upgrades += 1

        damage = self.skills[attack_type]
        if random.randint(0,100) + self.stats["luck"] > 100:
            damage *= 2

        target.update_health(damage, self.team, attack_type)

        if self.upgrades >= 5:
            self.level_up()

    def __str__(self):
       line_1 = ("Level: %d\tMax HP: %d\tCur HP: %d\n" %
                 (self.level, self.stats["max_hp"], self.stats["cur_hp"]))
       line_2 = ("Melee: %d\tRanged: %d\tArcane: %d\tDivine: %d\n" % 
                 (self.skills["Melee"], self.skills["Ranged"], self.skills["Arcane"], self.skills["Divine"]))
       line_3 = ("Phys D: %d\tMag D: %d\tLuck: %d\n" %
                 (self.stats["phys_def"], self.stats["mag_def"], self.stats["luck"]))
       return line_1 + line_2 + line_3
