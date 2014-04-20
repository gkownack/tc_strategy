# All globals stored here
# Imported by everyone

import pygame

global DISPLAY, WINDOW_HEIGHT, WINDOW_WIDTH, STATE, ANIMATION_INTERVAL, DIRTY_RECTS, MICRO, MACRO, MACRO_BOXSIDE
MACRO_BOXSIDE = 48
assert(MACRO_BOXSIDE % 2 == 0)
ANIMATION_INTERVAL = 500 # milliseconds per frame
WINDOW_WIDTH = 300
WINDOW_HEIGHT = 400
DIRTY_RECTS = []
DISPLAY = pygame.display.set_mode((WINDOW_HEIGHT, WINDOW_WIDTH))
