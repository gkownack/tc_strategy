import pygame, sys
import config
import macro_classes
from states import state
from pygame.locals import *
from lib.graphics.colors import *

class Macro(state.State):
    WINDOWWIDTH = 1512
    WINDOWHEIGHT = 864
    BOXSIDE = 72
    assert (WINDOWWIDTH%BOXSIDE == 0 and WINDOWHEIGHT%BOXSIDE == 0)
    XBOXES = WINDOWWIDTH/BOXSIDE
    YBOXES = (WINDOWHEIGHT)/BOXSIDE
    squares = []
    cursor = None
    cursor_color = RED

    def handle_event(self, event):
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == KEYDOWN:
            if event.key == K_w or event.key == K_UP:
                self.cursor = (self.cursor[0], max(0, self.cursor[1] - 1))
            if event.key == K_a or event.key == K_LEFT:
                self.cursor = (max(0, self.cursor[0] - 1), self.cursor[1])
            if event.key == K_s or event.key == K_DOWN:
                self.cursor = (self.cursor[0], min(self.YBOXES - 1, self.cursor[1] + 1))
            if event.key == K_d or event.key == K_RIGHT:
                self.cursor = (min(self.XBOXES - 1, self.cursor[0] + 1), self.cursor[1])
        elif event.type == MOUSEBUTTONDOWN:
            if event.button == 1:
                mousex, mousey = event.pos
                x = mousex / self.BOXSIDE
                y = mousey / self.BOXSIDE
                self.cursor = (x,y)

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
                if(y%2 == 0):
                    column.append(macro_classes.Macro_Square(pygame.Rect(x*self.BOXSIDE, y*self.BOXSIDE, self.BOXSIDE, self.BOXSIDE),
                                                             x, y, macro_classes.Macro_SmallSword()))
                else:
                    column.append(macro_classes.Macro_Square(pygame.Rect(x*self.BOXSIDE, y*self.BOXSIDE, self.BOXSIDE, self.BOXSIDE),
                                                             x, y, macro_classes.Macro_SmallSwordAnim()))
            self.squares.append(column)
            column = []
        self.cursor = (0,0)

    def draw_board(self):
        for x in range(self.XBOXES):
            for y in range(self.YBOXES):
                config.DISPLAY.blit(self.squares[x][y].terrain.pic, (x*self.BOXSIDE, y*self.BOXSIDE))
        self.draw_grid()
        pygame.draw.rect(config.DISPLAY, self.cursor_color, self.squares[self.cursor[0]][self.cursor[1]].rect, 2)

    def draw_grid(self):
        for x in range(self.BOXSIDE, self.WINDOWWIDTH, self.BOXSIDE):
            pygame.draw.line(config.DISPLAY, BLACK, (x, 0), (x, self.WINDOWHEIGHT))
        for y in range(self.BOXSIDE, self.WINDOWHEIGHT, self.BOXSIDE):
            pygame.draw.line(config.DISPLAY, BLACK, (0, y), (self.WINDOWWIDTH, y))
