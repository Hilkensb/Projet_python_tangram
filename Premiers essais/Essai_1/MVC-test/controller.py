import model
import vue

import numpy
import matplotlib.path as mpltPath

# functio to transform the coordinates of a shape to be displayed at a certain
# locolisation
# input : shape[[x,y]...],
# top left hand corner coordinates where it's displayed [x,y]
# output : new shape with offset
def offsetShape (shape, offset) :
    for i in range(0, len(shape)) :
        shape[i][0] += offset[0]
        shape[i][1] += offset[1]
    return shape

def shapeFits (shape) :
    PATRONBIS = [(0,0),(100,0),(100,100),(200,100),(200,200),(100,200),(0,200),(0,100)]
    SHAPE_1BIS = [(0,0),(100,0),(100,100),(0,100)]
    path = mpltPath.Path(PATRONBIS)
    print( path.contains_points(SHAPE_1BIS) )
    return 0

#_________________________________________________TEST_________________________________________________


#_________________________________________________DISPLAY_________________________________________________

shapeFits(1)
vue.affiche()


#_________________________________________________RULES_________________________________________________

