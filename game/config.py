# All globals stored here
# Imported by everyone

import pygame
from macro import macro_state

def init():
	global DISPLAY, WINDOW_HEIGHT, WINDOW_WIDTH, STATE
	WINDOW_WIDTH = 300
	WINDOW_HEIGHT = 400
	DISPLAY = pygame.display.set_mode((WINDOW_HEIGHT, WINDOW_WIDTH))
	STATE = macro_state.Macro()