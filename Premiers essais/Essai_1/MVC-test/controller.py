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
    path = mpltPath.Path(model.PATRON)
    path.contains_points( shape, radius = 1.0 )
    return 0

#_________________________________________________TEST_________________________________________________


#_________________________________________________DISPLAY_________________________________________________

shapeFits(model.SHAPE_1)
vue.affiche()


#_________________________________________________RULES_________________________________________________

