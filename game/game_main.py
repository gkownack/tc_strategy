import pygame, sys
import config
from pygame.locals import *

# Initialization routines
pygame.init()
config.init()

pygame.display.set_caption("Tech Comm Strategy Game")

while 1:
	for event in pygame.event.get():
		if event.type == QUIT:
			pygame.quit()
			sys.exit()
	pygame.display.update

