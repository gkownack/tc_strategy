import config
import random
import terrain_classes

def get_options(terrain_type):
    if terrain_type == terrain_classes.Grass:
        return [terrain_classes.Grass, terrain_classes.Grass, terrain_classes.Grass,
                terrain_classes.Mountain, terrain_classes.Tree, terrain_classes.Water]
    else:
        return [terrain_type, terrain_type, terrain_type]

def generate_terrain(width, height, primary=terrain_classes.Grass):
    terrain = [[terrain_classes.Grass for i in xrange(width)] for i in xrange(height)]

    for i in xrange(width*height):
        row = random.randint(1,height-2)
        col = random.randint(1,width-2)

        for x in xrange(-1,2):
           for y in xrange(-1,2):
               options = []
               for j in xrange(-1,2):
                   for k in xrange(-1,2):
                       if row+x+j >= 0 and row+x+j < height and col+y+k >= 0 and col+y+k <width:
                           options.extend(get_options(terrain[row+x+j][col+y+k]))
               terrain[row+x][col+y] = random.choice(options)
               if terrain[row+x][col+y] == terrain_classes.Grass:
                   if random.randint(0,1):
                       terrain[row+x][col+y] = primary

    return terrain
