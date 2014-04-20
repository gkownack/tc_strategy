import pygame, sys
import config
import micro_classes
import random
from states import state
from terrain import terrain_classes
from terrain import terrain
from units import units
from pygame.locals import *
from lib.graphics.colors import *

class Micro(state.State):
    BOXSIDE = 72
    WINDOWWIDTH = 18*BOXSIDE
    WINDOWHEIGHT = 10*BOXSIDE
    assert (WINDOWWIDTH%BOXSIDE == 0 and WINDOWHEIGHT%BOXSIDE == 0)
    XBOXES = WINDOWWIDTH/BOXSIDE
    YBOXES = (WINDOWHEIGHT)/BOXSIDE
    squares = []
    cursor = None
    cursor_color = RED
    cursor_rect = None
    selected = None # Tells you which tile is selected, None otherwise
    mask = pygame.Surface((BOXSIDE,BOXSIDE))
    mask.set_alpha(80)
    boxCosts = []
    boxPaths = []
    world = []
    units = {}
    current_team = -1

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
                    if square.unit is not None and square.unit.team == self.current_team:
                        self.selected = square
                        self.cursor_color = CYAN
                else:
                    square = self.squares[self.cursor[0]][self.cursor[1]]
                    if self.selected.unit.can_move:
                        # Moves the unit
                        if square.mask == BLUE and (square.unit is None or square.unit == self.selected.unit):
                            self.selected.unit.can_move = False
                            square.unit = self.selected.unit
                            if square != self.selected:
                                self.selected.unit = None
                            config.DIRTY_RECTS += [square, self.selected]
                            self.selected = None
                            self.cursor_color = RED
                    elif square.unit is not None and self.selected is not None:
                        self.selected = square
                        self.run_dijkstra()
            elif event.key == K_1:
                # Melee attack
                if self.selected is not None and self.selected.unit.can_attack:
                    targ_square = self.squares[self.cursor[0]][self.cursor[1]]
                    target = targ_square.unit
                    # Melee can only attack adjacent squares
                    if target is not None and micro_classes.distance(self.selected, targ_square) == 1:
                        self.selected.unit.can_attack = False
                        self.selected.unit.attack(target, units.Attributes.Melee)
                        if target.is_dead():
                            targ_square.unit = None
                            config.DIRTY_RECTS += [targ_square]
                        print "Attacker"
                        print self.selected.unit
                        print "Defender"
                        print target
            elif event.key == K_2:
                # Ranged attack
                if self.selected is not None and self.selected.unit.can_attack:
                    targ_square = self.squares[self.cursor[0]][self.cursor[1]]
                    target = targ_square.unit
                    # Ranged can attack 2 or 3 squares away
                    if target is not None and micro_classes.distance(self.selected, targ_square) > 1 and micro_classes.distance(self.selected, targ_square) < 4:
                        self.selected.unit.can_attack = False
                        self.selected.unit.attack(target, units.Attributes.Ranged)
                        if target.is_dead():
                            targ_square.unit = None
                            config.DIRTY_RECTS += [targ_square]
                        print "Attacker"
                        print self.selected.unit
                        print "Defender"
                        print target
            elif event.key == K_3:
                # Arcane attack
                if self.selected is not None and self.selected.unit.can_attack:
                    targ_square = self.squares[self.cursor[0]][self.cursor[1]]
                    target = targ_square.unit
                    # Arcane can attack 1 or 2 squares away
                    if target is not None and micro_classes.distance(self.selected, targ_square) > 0 and micro_classes.distance(self.selected, targ_square) < 3:
                        self.selected.unit.can_attack = False
                        self.selected.unit.attack(target, units.Attributes.Arcane)
                        if target.is_dead():
                            targ_square.unit = None
                            config.DIRTY_RECTS += [targ_square]
                        print "Attacker"
                        print self.selected.unit
                        print "Defender"
                        print target
            elif event.key == K_4:
                # Divine intervention
                if self.selected is not None and self.selected.unit.can_attack:
                    targ_square = self.squares[self.cursor[0]][self.cursor[1]]
                    target = targ_square.unit
                    # Divine can be used 0 or 1 spaces away
                    if target is not None and micro_classes.distance(self.selected, targ_square) <= 1:
                        self.selected.unit.can_attack = False
                        self.selected.unit.attack(target, units.Attributes.Divine)
                        if target.is_dead():
                            targ_square.unit = None
                            config.DIRTY_RECTS += [targ_square]
                        print "Attacker"
                        print self.selected.unit
                        print "Defender"
                        print target
            elif event.key == K_SPACE:
                config.STATE = config.MACRO
                config.STATE.update()
                pygame.display.update()
            elif event.key == K_r:
                self.nextTurn()
            if self.selected is None:
                self.run_dijkstra()
        elif event.type == MOUSEBUTTONDOWN:
            if event.button == 1:
                mousex, mousey = event.pos
                x = mousex / self.BOXSIDE
                y = mousey / self.BOXSIDE                
                self.cursor = (x,y)

    def update(self):
        pygame.display.set_caption("Micro")
        for x in range(self.XBOXES):
            for y in range(self.YBOXES):
                square = self.squares[x][y]
                if square.unit != None:
                    if square.unit.update():
                        config.DIRTY_RECTS += [square.rect]
        self.draw_board()

    def getTerrain(self, x, y):
	return self.world[y][x]

    def init(self, primary_terrain=terrain_classes.Grass):
        config.DISPLAY = pygame.display.set_mode((self.WINDOWWIDTH, self.WINDOWHEIGHT))
        pygame.display.set_caption("Micro")
        config.DISPLAY.fill(WHITE)
        self.squares = []
        column = []
	self.world = terrain.terrain().generate_terrain(self.XBOXES,self.YBOXES, primary_terrain)
        for x in range(self.XBOXES):
            for y in range(self.YBOXES):
                column.append(micro_classes.Micro_Square(pygame.Rect(x*self.BOXSIDE, y*self.BOXSIDE, self.BOXSIDE, self.BOXSIDE),
                                                         x, y, self.getTerrain(x,y)))
            self.squares.append(column)
            column = []
        self.cursor = (0,0)

        # for testing sprites:
        self.squares[0][0].unit = units.Unit({"Melee": 0, "Ranged":0, "Arcane":0, "Divine":0}, 0)
        self.squares[1][0].unit = units.Unit({"Melee": 1, "Ranged":0, "Arcane":0, "Divine":0}, 0)
        self.squares[2][0].unit = units.Unit({"Melee": 1, "Ranged":1, "Arcane":0, "Divine":0}, 0)
        self.squares[3][0].unit = units.Unit({"Melee": 1, "Ranged":2, "Arcane":0, "Divine":0}, 0)
        self.squares[4][0].unit = units.Unit({"Melee": 0, "Ranged":1, "Arcane":1, "Divine":0}, 0)
        self.squares[5][0].unit = units.Unit({"Melee": 0, "Ranged":0, "Arcane":1, "Divine":0}, 1)
        self.squares[6][0].unit = units.Unit({"Melee": 0, "Ranged":0, "Arcane":2, "Divine":2}, 1)
        self.squares[7][0].unit = units.Unit({"Melee": 0, "Ranged":0, "Arcane":0, "Divine":100}, 1)
        self.squares[8][0].unit = units.Unit({"Melee": 2, "Ranged":0, "Arcane":2, "Divine":2}, 1)
        self.squares[9][0].unit = units.Unit({"Melee": 1, "Ranged":1, "Arcane":1, "Divine":1}, 1)
        self.units[0] = [self.squares[0][0].unit, self.squares[1][0].unit, self.squares[2][0].unit, self.squares[3][0].unit, self.squares[4][0].unit]
        self.units[1] = [self.squares[5][0].unit, self.squares[6][0].unit, self.squares[7][0].unit, self.squares[8][0].unit, self.squares[9][0].unit]
        self.nextTurn()
        self.update()
        self.run_dijkstra()
        pygame.display.update()

    def draw_board(self):
        for x in range(self.XBOXES):
            for y in range(self.YBOXES):
                square = self.squares[x][y]
                config.DISPLAY.blit(square.terrain.pic, (x*self.BOXSIDE, y*self.BOXSIDE))
                if square.unit != None:
                    config.DISPLAY.blit(square.unit.micro_pic, (x*self.BOXSIDE, y*self.BOXSIDE))
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

    def nextTurn(self):
        self.current_team += 1
        while self.current_team not in self.units:
            self.current_team += 1
            if self.current_team > max(self.units.keys()):
                self.current_team = 0
        for u in self.units[self.current_team]:
            u.can_move = True
            u.can_attack = True
        self.selected = None
