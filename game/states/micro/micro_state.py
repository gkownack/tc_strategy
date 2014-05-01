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
            elif event.key == K_t:
                self.deselect()
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
                    current_unit = self.selected.unit
                    square = self.squares[self.cursor[0]][self.cursor[1]]
                    if current_unit.moves_left:
                        # Moves the unit
                        if square.mask == BLUE and (square.unit is None or square.unit == current_unit):
                            current_unit.moves_left = self.boxCosts[self.cursor[0]][self.cursor[1]]
                            square.unit = self.selected.unit
                            if square != self.selected:
                                self.selected.unit = None
                            if not current_unit.can_attack:
                                self.deselect()
                            else:
                                self.selected = square
                                self.run_dijkstra()
                        else:
                            self.deselect()
                    elif square.unit is not None and self.selected is not None and square.unit.team == self.current_team:
                        self.selected = square
                        self.run_dijkstra()
            elif event.key == K_1:
                # Melee attack
                self.manageAttack(units.Attributes.Melee)
            elif event.key == K_2:
                # Ranged attack
                self.manageAttack(units.Attributes.Ranged)
            elif event.key == K_3:
                # Arcane attack
                self.manageAttack(units.Attributes.Arcane)
            elif event.key == K_4:
                # Divine intervention
                self.manageAttack(units.Attributes.Divine)
            elif event.key == K_SPACE:
                config.STATE = config.MACRO
                config.STATE.update()
                pygame.display.update()
            elif event.key == K_r:
                self.nextTurn()

            if self.selected is None:
                self.run_dijkstra()
            self.printCurrent()
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

    def init(self, squad1, squad2, primary_terrain=terrain_classes.Grass):
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
        """
        self.squares[0][0].unit = units.Unit({"Melee": 1000, "Ranged":0, "Arcane":0, "Divine":0}, 0)
        self.squares[1][0].unit = units.Unit({"Melee": 1000, "Ranged":0, "Arcane":0, "Divine":0}, 0)
        self.squares[2][0].unit = units.Unit({"Melee": 1000, "Ranged":1, "Arcane":0, "Divine":0}, 0)
        self.squares[3][0].unit = units.Unit({"Melee": 1000, "Ranged":2, "Arcane":0, "Divine":0}, 0)
        self.squares[4][0].unit = units.Unit({"Melee": 1000, "Ranged":1, "Arcane":1, "Divine":0}, 0)
        self.squares[5][0].unit = units.Unit({"Melee": 0, "Ranged":0, "Arcane":1, "Divine":0}, 1)
        self.squares[6][0].unit = units.Unit({"Melee": 0, "Ranged":0, "Arcane":2, "Divine":2}, 1)
        self.squares[7][0].unit = units.Unit({"Melee": 0, "Ranged":0, "Arcane":0, "Divine":100}, 1)
        self.squares[8][0].unit = units.Unit({"Melee": 2, "Ranged":0, "Arcane":2, "Divine":2}, 1)
        self.squares[9][0].unit = units.Unit({"Melee": 1, "Ranged":1, "Arcane":1, "Divine":1}, 1)
        """
        self.units = {0:[],1:[]}
        for i in xrange(len(squad1.units)):
            self.squares[i][0].unit = squad1.units[i]
            self.units[0].append(squad1.units[i])
        for j in xrange(len(squad2.units)):
            self.squares[j][2].unit = squad2.units[j]
            self.units[1].append(squad2.units[i])
        #self.units[0] = [self.squares[0][0].unit, self.squares[1][0].unit, self.squares[2][0].unit, self.squares[3][0].unit, self.squares[4][0].unit]
        #self.units[1] = [self.squares[5][0].unit, self.squares[6][0].unit, self.squares[7][0].unit, self.squares[8][0].unit, self.squares[9][0].unit]
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
            self.dijkstra(square, square.unit.moves_left, boxCosts, boxPaths, "")
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
        if self.current_team in self.units:
            for u in self.units[self.current_team]:
                u.moves_left = u.stats["move"]
        self.current_team += 1
        while self.current_team not in self.units:
            self.current_team += 1
            if self.current_team > max(self.units.keys()):
                self.current_team = 0
        for u in self.units[self.current_team]:
            u.moves_left = u.stats["move"]
            u.can_attack = True
        self.deselect()
        print "Current Turn: ", self.current_team

    def manageAttack(self, attack_type):
        if attack_type == units.Attributes.Melee:
            minDist = 1
            maxDist = 1
        elif attack_type == units.Attributes.Ranged:
            minDist = 2
            maxDist = 3
        elif attack_type == units.Attributes.Arcane:
            minDist = 1
            maxDist = 2
        else: # Divine
            minDist = 0
            maxdist = 1

        if self.selected is not None and self.selected.unit.can_attack:
            current_unit = self.selected.unit
            targ_square = self.squares[self.cursor[0]][self.cursor[1]]
            target = targ_square.unit
            if target is not None and micro_classes.distance(self.selected, targ_square) >= minDist and micro_classes.distance(self.selected, targ_square) <= maxDist:
                current_unit.can_attack = False
                current_unit.attack(target, attack_type)
                if target.is_dead():
                    targ_square.unit = None
                    config.DIRTY_RECTS += [targ_square]
                    self.units[target.team].remove(target)
                    if len(self.units[target.team]) == 0:
                        print "Team Destroyed"
                        self.units.pop(target.team)
                current_unit.moves_left = 0
                self.deselect()
            print "Attacker"
            print current_unit
            print "Defender"
            print target

    def deselect(self):
        config.DIRTY_RECTS += [self.squares[self.cursor[0]][self.cursor[1]], self.selected]
        self.selected = None
        self.cursor_color = RED

    def printCurrent(self):
        print self.squares[self.cursor[0]][self.cursor[1]]
