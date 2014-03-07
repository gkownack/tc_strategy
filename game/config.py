# All globals stored here
# Imported by everyone

import pygame

def init():
	global DISPLAY, WINDOW_HEIGHT, WINDOW_WIDTH
	WINDOW_WIDTH = 300
	WINDOW_HEIGHT = 400
	DISPLAY = pygame.display.set_mode((WINDOW_HEIGHT, WINDOW_WIDTH))