import pygame, sys
import config
import macro_classes
import random
from states import state
from units import units
from pygame.locals import *
from lib.graphics.colors import *

class Macro(state.State):
    BOXSIDE = 48
    WINDOWWIDTH = 28*BOXSIDE
    WINDOWHEIGHT = 16*BOXSIDE
    assert (WINDOWWIDTH%BOXSIDE == 0 and WINDOWHEIGHT%BOXSIDE == 0)
    XBOXES = WINDOWWIDTH/BOXSIDE
    YBOXES = (WINDOWHEIGHT)/BOXSIDE
    squares = []
    cursor = None
    cursor_color = RED
    cursor_rect = None
    selected = None
    mask = pygame.Surface((BOXSIDE,BOXSIDE))
    mask.set_alpha(80)
    boxCosts = []
    boxPaths = []

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
                        self.selected = square
                        self.cursor_color = CYAN
                else:
                    square = self.squares[self.cursor[0]][self.cursor[1]]
                    if square.mask == BLUE and (square.unit is None or square.unit == self.selected.unit):
                        square.unit = self.selected.unit
                        if square != self.selected:
                            self.selected.unit = None
                        config.DIRTY_RECTS += [square, self.selected]
                        self.selected = None
                        self.cursor_color = RED
                    elif square.unit is not None and self.selected is not None:
                        self.selected = square
                        self.run_dijkstra()
            elif event.key == K_SPACE:
                config.STATE = config.MICRO
                config.STATE.update()
                pygame.display.update()
            if self.selected is None:
                self.run_dijkstra()
        elif event.type == MOUSEBUTTONDOWN:
            if event.button == 1:
                mousex, mousey = event.pos
                x = mousex / self.BOXSIDE
                y = mousey / self.BOXSIDE                
                self.cursor = (x,y)

    def update(self):
        config.DISPLAY = pygame.display.set_mode((self.WINDOWWIDTH, self.WINDOWHEIGHT))
        pygame.display.set_caption("Macro")
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
	self.squares[3][0].unit = units.Unit(units.Attributes.Ranged)
        self.update()
        self.run_dijkstra()
        pygame.display.update()

    def draw_board(self):
        for x in range(self.XBOXES):
            for y in range(self.YBOXES):
                square = self.squares[x][y]
                config.DISPLAY.blit(square.terrain.pic, (x*self.BOXSIDE, y*self.BOXSIDE))
                if square.unit != None:
                    config.DISPLAY.blit(square.unit.pic, (x*self.BOXSIDE, y*self.BOXSIDE))
                if square.mask != None:
                    self.mask.fill(square.mask)
                    config.DISPLAY.blit(self.mask, square.rect.topleft)
                    config.DIRTY_RECTS.append(square)
        self.draw_grid()
        if self.cursor_rect is not None:
            config.DIRTY_RECTS += [self.cursor_rect]
        self.cursor_rect = pygame.draw.rect(config.DISPLAY, self.cursor_color, self.squares[self.cursor[0]][self.cursor[1]].rect, 3)
        config.DIRTY_RECTS += [self.cursor_rect]

        #Draw the arrows 'n' shit
        if self.selected != None:
            BOXSIDE = self.BOXSIDE
            DISPLAYSURF = config.DISPLAY
            current = self.selected.rect.center
            x, y = self.cursor[0], self.cursor[1]
            path = self.boxPaths[x][y]
            for z in path:
                if z == 'u':
                    nextcoord = (current[0], current[1] - BOXSIDE)
                    pygame.draw.line(DISPLAYSURF, WHITE, current, nextcoord, BOXSIDE/8)
                if z == 'd':
                    nextcoord = (current[0], current[1] + BOXSIDE)
                    pygame.draw.line(DISPLAYSURF, WHITE, current, nextcoord, BOXSIDE/8)
                if z == 'l':
                    nextcoord = (current[0] - BOXSIDE, current[1])
                    pygame.draw.line(DISPLAYSURF, WHITE, current, nextcoord, BOXSIDE/8)
                if z == 'r':
                    nextcoord = (current[0] + BOXSIDE, current[1])
                    pygame.draw.line(DISPLAYSURF, WHITE, current, nextcoord, BOXSIDE/8)
                current = nextcoord
            if current == self.selected.rect.center:
                pass
            elif z == 'l':
                pygame.draw.polygon(DISPLAYSURF, WHITE, [(current[0]-BOXSIDE/6, current[1]), (current[0]+BOXSIDE/6, current[1]+BOXSIDE/6), (current[0]+BOXSIDE/6, current[1]-BOXSIDE/6)])
            elif z == 'd':
                pygame.draw.polygon(DISPLAYSURF, WHITE, [(current[0], current[1]+BOXSIDE/6), (current[0]+BOXSIDE/6, current[1]-BOXSIDE/6), (current[0]-BOXSIDE/6, current[1]-BOXSIDE/6)])
            elif z == 'r':
                pygame.draw.polygon(DISPLAYSURF, WHITE, [(current[0]+BOXSIDE/6, current[1]), (current[0]-BOXSIDE/6, current[1]-BOXSIDE/6), (current[0]-BOXSIDE/6, current[1]+BOXSIDE/6)])
            elif z == 'u':
                pygame.draw.polygon(DISPLAYSURF, WHITE, [(current[0], current[1]-BOXSIDE/6), (current[0]-BOXSIDE/6, current[1]+BOXSIDE/6), (current[0]+BOXSIDE/6, current[1]+BOXSIDE/6)])


    def draw_grid(self):
        for x in range(self.BOXSIDE, self.WINDOWWIDTH, self.BOXSIDE):
            pygame.draw.line(config.DISPLAY, BLACK, (x, 0), (x, self.WINDOWHEIGHT))
        for y in range(self.BOXSIDE, self.WINDOWHEIGHT, self.BOXSIDE):
            pygame.draw.line(config.DISPLAY, BLACK, (0, y), (self.WINDOWWIDTH, y))

    def run_dijkstra(self):
        boxCosts = []
        column = []
        boxPaths = []
        column2 = []
        for x in range(self.XBOXES):
            for y in range(self.YBOXES):
                if self.squares[x][y].mask is not None:
                    config.DIRTY_RECTS.append(self.squares[x][y])
                    self.squares[x][y].mask = None
                column.append(-1)
                column2.append("")
            boxCosts.append(column)
            boxPaths.append(column2)
            column = []
            column2 = []
        square = self.squares[self.cursor[0]][self.cursor[1]]
        if square.unit is not None:
            self.dijkstra(square, square.unit.stats["move"], boxCosts, boxPaths, "")
        self.boxCosts = boxCosts
        self.boxPaths = boxPaths

    def validDijk(self, x, y, newx, newy, grid, weight, boxCosts):
        XBOXES = self.XBOXES
        YBOXES = self.YBOXES
        grid = self.squares
        if newx < 0 or newx >= XBOXES:
            return False
        if newy < 0 or newy >= YBOXES:
            return False
        config.DIRTY_RECTS += [grid[newx][newy]]
        if grid[newx][newy].terrain.impass == True:
            grid[newx][newy].mask = RED
            return False
        if weight - grid[newx][newy].terrain.weight <= boxCosts[newx][newy]:
            if weight - grid[newx][newy].terrain.weight < 0 and grid[newx][newy].mask != BLUE and grid[x][y].unit == None:
                grid[newx][newy].mask = RED
            return False
        return True

    def dijkstra(self, current, weight, boxCosts, boxPaths, path):
        grid = self.squares
        x, y = current.x, current.y
        boxCosts[x][y] = weight
        boxPaths[x][y] = path
        toSearch = []
        if self.validDijk(x, y, x-1, y, grid, weight, boxCosts):
            toSearch.append((grid[x-1][y], grid[x-1][y].terrain.weight, 'l'))
        if self.validDijk(x, y, x+1, y, grid, weight, boxCosts):
            toSearch.append((grid[x+1][y], grid[x+1][y].terrain.weight, 'r'))
        if self.validDijk(x, y, x, y-1, grid, weight, boxCosts):
            toSearch.append((grid[x][y-1], grid[x][y-1].terrain.weight, 'u'))
        if self.validDijk(x, y, x, y+1, grid, weight, boxCosts):
            toSearch.append((grid[x][y+1], grid[x][y+1].terrain.weight, 'd'))
        for z in toSearch:
            self.dijkstra(z[0], weight-z[1], boxCosts, boxPaths, path+z[2])
        current.mask = BLUE
        config.DIRTY_RECTS += [current]
