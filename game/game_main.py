import pygame, sys
import config
from pygame.locals import *

# Initialization routines
pygame.init()
config.init()
print "fak u billy"
while 1:
    "I'm a boss!"
    for event in pygame.event.get():
        config.STATE.handle_event(event);
    config.STATE.update()
    pygame.display.update()

