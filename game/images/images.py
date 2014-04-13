import pygame

units = {}
units["Rogue"] = [pygame.image.load('lib/graphics/Rogue.png'),
                  pygame.image.load('lib/graphics/RogueAnim.png')]
units["Melee"] = [pygame.image.load('lib/graphics/SmallSword.png'),
                  pygame.image.load('lib/graphics/SmallSwordAnim.png')]
units["Ranged"] = [pygame.image.load('lib/graphics/Ranged.png'),
                   pygame.image.load('lib/graphics/RangedAnim.png')]
units["Arcane"] = [pygame.image.load('lib/graphics/ArcaneMage.png'),
                   pygame.image.load('lib/graphics/ArcaneMageAnim.png')]
units["Divine"] = [pygame.image.load('lib/graphics/DivineMage.png'),
                   pygame.image.load('lib/graphics/DivineMageAnim.png')]

terrain = {}
terrain["Grass"] = pygame.image.load('lib/graphics/grass.png')
terrain["Water"] = pygame.image.load('lib/graphics/water.png')
terrain["Mountain"] = pygame.image.load('lib/graphics/mountain.png')
terrain["Tree"] = pygame.image.load('lib/graphics/tree.png')
