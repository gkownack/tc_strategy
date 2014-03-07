import pygame, sys
import config
from lib.classes import state
from pygame.locals import *

class Macro(state.State):
	def handle_event(self, event):
		if event.type == QUIT:
			pygame.quit()
			sys.exit()

	def update(self):
		pass

	def init(self):
		pass