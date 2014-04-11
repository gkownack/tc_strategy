# All globals stored here
# Imported by everyone

import pygame
from states.title import title_state

def init():
    global DISPLAY, WINDOW_HEIGHT, WINDOW_WIDTH, STATE, ANIMATION_INTERVAL, DIRTY_RECTS
    ANIMATION_INTERVAL = 500 # milliseconds per frame
    WINDOW_WIDTH = 300
    WINDOW_HEIGHT = 400
    DISPLAY = pygame.display.set_mode((WINDOW_HEIGHT, WINDOW_WIDTH))
    STATE = title_state.Title()
    DIRTY_RECTS = []
    STATE.init()
