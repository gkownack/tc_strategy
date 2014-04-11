import pygame, sys
import config
import macro_classes
import random
from states import state
from units import units
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
    cursor_rect = None
    selected = None

    def handle_event(self, event):
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == KEYDOWN:
            config.DIRTY_RECTS.append(self.squares[self.cursor[0]][self.cursor[1]].rect)
            if event.key == K_w or event.key == K_UP:
                self.cursor = (self.cursor[0], max(0, self.cursor[1] - 1))
            elif event.key == K_a or event.key == K_LEFT:
                self.cursor = (max(0, self.cursor[0] - 1), self.cursor[1])
            elif event.key == K_s or event.key == K_DOWN:
                self.cursor = (self.cursor[0], min(self.YBOXES - 1, self.cursor[1] + 1))
            elif event.key == K_d or event.key == K_RIGHT:
                self.cursor = (min(self.XBOXES - 1, self.cursor[0] + 1), self.cursor[1])
            elif event.key == K_ESCAPE:
                pygame.quit()
                sys.exit()
            elif event.key == K_RETURN:
                if self.selected is None:
                    square = self.squares[self.cursor[0]][self.cursor[1]]
                    if square.unit is not None:
                        self.selected = square.unit
                        self.cursor_color = CYAN
                else:
                    self.selected = None
                    self.cursor_color = RED
        elif event.type == MOUSEBUTTONDOWN:
            if event.button == 1:
                mousex, mousey = event.pos
                x = mousex / self.BOXSIDE
                y = mousey / self.BOXSIDE                
                self.cursor = (x,y)

    def update(self):
        for x in range(self.XBOXES):
            for y in range(self.YBOXES):
                square = self.squares[x][y]
                if square.unit != None:
                    if square.unit.update():
                        config.DIRTY_RECTS += [square.rect]
        self.draw_board()

    def getTerrain(self, x, y):
        random.seed((x,y))
        t = random.randint(0,6)
        if t == 0 or t == 1 or t == 2:
            return macro_classes.Macro_Grass
        elif t == 3 or t == 4:
            return macro_classes.Macro_Tree
        elif t == 5:
            return macro_classes.Macro_Water
        else:
            return macro_classes.Macro_Mountain

    def init(self):
        config.DISPLAY = pygame.display.set_mode((self.WINDOWWIDTH, self.WINDOWHEIGHT))
        pygame.display.set_caption("Macro")
        config.DISPLAY.fill(WHITE)
        self.squares = []
        column = []
        for x in range(self.XBOXES):
            for y in range(self.YBOXES):
                column.append(macro_classes.Macro_Square(pygame.Rect(x*self.BOXSIDE, y*self.BOXSIDE, self.BOXSIDE, self.BOXSIDE),
                                                         x, y, self.getTerrain(x,y)))
            self.squares.append(column)
            column = []
        self.cursor = (0,0)

        # for testing sprites:
        self.squares[0][0].unit = units.Unit(units.Attributes.Melee)
        self.squares[1][0].unit = units.Unit(units.Attributes.Arcane)
        self.squares[2][0].unit = units.Unit(units.Attributes.Divine)
        self.update()
        pygame.display.update()

    def draw_board(self):
        for x in range(self.XBOXES):
            for y in range(self.YBOXES):
                square = self.squares[x][y]
                config.DISPLAY.blit(square.terrain.pic, (x*self.BOXSIDE, y*self.BOXSIDE))
                if square.unit != None:
                    config.DISPLAY.blit(square.unit.pic, (x*self.BOXSIDE, y*self.BOXSIDE))
        self.draw_grid()
        if self.cursor_rect is not None:
            config.DIRTY_RECTS += [self.cursor_rect]
        self.cursor_rect = pygame.draw.rect(config.DISPLAY, self.cursor_color, self.squares[self.cursor[0]][self.cursor[1]].rect, 3)
        config.DIRTY_RECTS += [self.cursor_rect]

    def draw_grid(self):
        for x in range(self.BOXSIDE, self.WINDOWWIDTH, self.BOXSIDE):
            pygame.draw.line(config.DISPLAY, BLACK, (x, 0), (x, self.WINDOWHEIGHT))
        for y in range(self.BOXSIDE, self.WINDOWHEIGHT, self.BOXSIDE):
            pygame.draw.line(config.DISPLAY, BLACK, (0, y), (self.WINDOWWIDTH, y))

    def validDijk(self, x, y, newx, newy, grid, weight, boxCosts, charType):
        XBOXES = self.XBOXES
        YBOXES = self.YBOXES
        if newx < 0 or newx >= XBOXES:
            return False
        if newy < 0 or newy >= YBOXES:
            return False
        if grid[newx][newy].impass == True:
            grid[newx][newy].mask = RED
            return False
        if weight - grid[newx][newy].weight <= boxCosts[newx][newy]:
            if weight - grid[newx][newy].weight < 0 and grid[newx][newy].mask != BLUE and grid[x][y].contains == None:
                grid[newx][newy].mask = RED
            return False
        if not (grid[newx][newy].contains == None or grid[newx][newy].contains.charType == charType):
            grid[newx][newy].mask = RED
            return False
        return True

    def dijkstra(self, current, grid, weight, boxCosts, boxPaths, path, charType):
        x, y = getBoxCoords(current.rect)
        boxCosts[x][y] = weight
        boxPaths[x][y] = path
        toSearch = []
        if validDijk(x, y, x-1, y, grid, weight, boxCosts, charType):
            toSearch.append((grid[x-1][y], grid[x-1][y].weight, 'l'))
        if validDijk(x, y, x+1, y, grid, weight, boxCosts, charType):
            toSearch.append((grid[x+1][y], grid[x+1][y].weight, 'r'))
        if validDijk(x, y, x, y-1, grid, weight, boxCosts, charType):
            toSearch.append((grid[x][y-1], grid[x][y-1].weight, 'u'))
        if validDijk(x, y, x, y+1, grid, weight, boxCosts, charType):
            toSearch.append((grid[x][y+1], grid[x][y+1].weight, 'd'))
        for z in toSearch:
            dijkstra(z[0], grid, weight-z[1], boxCosts, boxPaths, path+z[2], charType)
        current.mask = BLUE
