import model
import vue

import numpy
import matplotlib.path as mpltPath

# function to transform the coordinates of a shape to be displayed at a certain
# locolisation
# input : shape[[x,y]...],
# top left hand corner coordinates where it's displayed [x,y]
# output : new shape with offset
def offsetShape (shape, offset) :
    localShape = numpy.copy(shape)
    for i in range(0, len(localShape)) :
        localShape[i][0] += offset[0]
        localShape[i][1] += offset[1]
    return localShape

# function to fin all the place where the shape can fit in the patron
# input : shape you want to test + patron
# output : list of valid coordinates
def shapeFits (shape, patron) :
    listResult = []
    for i in range(0, len(patron)) :
        validated = True
        shapeOffset = offsetShape( shape, patron[i] )
        path = mpltPath.Path( patron )
        result = path.contains_points( shapeOffset, radius = 1.0 )
        #print(result)
        for y in range(0, len(result)) :
            if not result[y] :
                validated = False
                break
        if validated:
            listResult.append(patron[i])
    #print(listResult)
    return listResult

#_________________________________________________TEST_________________________________________________


#_________________________________________________DISPLAY_________________________________________________

shapeFits(model.SHAPE_1, model.PATRON)
vue.affiche()


#_________________________________________________RULES_________________________________________________

