import pygame, sys
import config
from pygame.locals import *
from states import state
from lib.graphics.colors import *

class Title(state.State):
	def handle_event(self, event):
		if event.type == QUIT:
			pygame.quit()
			sys.exit()

	def update(self):
		pass

	def init(self):
		pygame.display.set_caption("Tech Comm Strategy Game")
		config.DISPLAY.fill(WHITE)