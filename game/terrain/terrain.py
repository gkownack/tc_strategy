import random
from terrain_classes import Grass, Mountain, Tree, Water
import terrain_classes

class terrain():
    def get_options(self, terrain_type):
        if terrain_type == Grass:
            return [Grass, Grass, Grass, Grass, Grass, Grass, Grass, Grass, Mountain, Mountain, Tree, Tree, Water]
	elif terrain_type == Water:
	    return [Water, Water]
        else:
            return [terrain_type, terrain_type, terrain_type, terrain_type]

    def generate_terrain(self, width, height, primary=Grass):
	random.seed()
        terrain = [[Grass for i in xrange(width)] for i in xrange(height)]

        for i in xrange(width*height / 2):
            row = random.randint(1,height-2)
            col = random.randint(1,width-2)

            for x in xrange(-1,2):
                for y in xrange(-1,2):
                    options = []
                    for j in xrange(-1,2):
                        for k in xrange(-1,2):
                            if row+x+j >= 0 and row+x+j < height and col+y+k >= 0 and col+y+k <width:
                                options.extend(self.get_options(terrain[row+x+j][col+y+k]))
                    terrain[row+x][col+y] = random.choice(options)
                    if terrain[row+x][col+y] == Grass:
                        if random.randint(0,1):
                            terrain[row+x][col+y] = primary

        return terrain
