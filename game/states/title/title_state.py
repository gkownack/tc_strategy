import pygame, sys
import config
from pygame.locals import *
from states import state
from lib.graphics.colors import *
from states.macro import macro_state

class Title(state.State):
    FONT_SIZE = 40
    BUTTON_SIZE = 1.5
    start = None

    def handle_event(self, event):
        mousex, mousey = 0,0
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
        if event.type == MOUSEBUTTONDOWN:
            if event.button == 1:
                mousex, mousey = event.pos
                if self.start.collidepoint((mousex, mousey)) == True:
                    config.STATE = macro_state.Macro()
                    config.STATE.init()

    def update(self):
        pass

    def init(self):
        pygame.display.set_caption("Iron Legacy")
        config.DISPLAY.fill(WHITE)
        start = pygame.Rect(config.DISPLAY.get_rect())
        start.width /= self.BUTTON_SIZE
        start.height /= self.BUTTON_SIZE * 2
        start.centerx = config.DISPLAY.get_rect().centerx
        start.centery = config.DISPLAY.get_rect().centery
        pygame.draw.rect(config.DISPLAY, GRAY, start)
        font = pygame.font.SysFont("", self.FONT_SIZE)
        font_surf = font.render("START", False, BLACK)
        font_rect = font_surf.get_rect()
        font_rect.centerx = start.centerx
        font_rect.centery = start.centery
        config.DISPLAY.blit(font_surf, font_rect)
        self.start = start