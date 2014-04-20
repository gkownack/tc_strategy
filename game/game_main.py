import pygame, sys
import config
from pygame.locals import *
from states.title import title_state

# Initialization Routines
pygame.init()

config.STATE = title_state.Title()
config.STATE.init()

while 1:
    for event in pygame.event.get():
        config.STATE.handle_event(event);
    config.STATE.update()
    pygame.display.update(config.DIRTY_RECTS)
    config.DIRTY_RECTS = []

