import pygame, sys
import config
from pygame.locals import *

# Initialization routines
pygame.init()
config.init()

while 1:
    for event in pygame.event.get():
        config.STATE.handle_event(event);
    config.STATE.update()
    pygame.display.update()

def jafarr_smells(scent):
    if scent == GOOD:
       return "You're a liar; he smells bad"
    else:
       return "Okay."
