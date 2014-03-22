import pygame, sys
import config
import macro_classes
from states import state
from pygame.locals import *
from lib.graphics.colors import *

class Macro(state.State):
    WINDOWWIDTH = 1000
    WINDOWHEIGHT = 600
    BOXSIDE = 25
    assert (WINDOWWIDTH%BOXSIDE == 0 and WINDOWHEIGHT%BOXSIDE == 0)
    XBOXES = WINDOWWIDTH/BOXSIDE
    YBOXES = (WINDOWHEIGHT)/BOXSIDE
    squares = []
    cursor = None

    def handle_event(self, event):
        if event.type == QUIT:
            pygame.quit()
            sys.exit()

    def update(self):
        self.draw_board()

    def init(self):
        config.DISPLAY = pygame.display.set_mode((self.WINDOWWIDTH, self.WINDOWHEIGHT))
        pygame.display.set_caption("Macro")
        config.DISPLAY.fill(WHITE)
        self.squares = []
        column = []
        for x in range(self.XBOXES):
            for y in range(self.YBOXES):
                column.append(macro_classes.Macro_Square(None, x, y, macro_classes.Macro_Grass()))
            self.squares.append(column)
            column = []
        self.cursor = (0,0)

    def draw_board(self):
        for x in range(self.XBOXES):
            for y in range(self.YBOXES):
                config.DISPLAY.blit(self.squares[x][y].terrain.pic, (x*self.BOXSIDE, y*self.BOXSIDE))
        self.draw_grid()

    def draw_grid(self):
        for x in range(self.BOXSIDE, self.WINDOWWIDTH, self.BOXSIDE):
            pygame.draw.line(config.DISPLAY, BLACK, (x, 0), (x, self.WINDOWHEIGHT))
        for y in range(self.BOXSIDE, self.WINDOWHEIGHT, self.BOXSIDE):
            pygame.draw.line(config.DISPLAY, BLACK, (0, y), (self.WINDOWWIDTH, y))