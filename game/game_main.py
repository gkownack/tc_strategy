import pygame, sys
import config
from pygame.locals import *

# Initialization Routines
pygame.init()
config.init()

while 1:
    '''Jafarr stil smells'''
    for event in pygame.event.get():
        config.STATE.handle_event(event);
    config.STATE.update()
    pygame.display.update()
