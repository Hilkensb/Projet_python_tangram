import model
import vue

import shapely.wkt # firestarter?
import math  as mth
from shapely.geometry import LineString


import numpy
import matplotlib.path as mpltPath
from shapely.geometry import Polygon

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

# function to substract a certain shape to a patron
# input : emplacement of the shape, the shape and the patron
# output : the new patron
def reshapePatron(offset, shape, patron) :
    localShape = Polygon(offsetShape(shape, offset)) # object polygon needed to use the function difference
    localPatron = Polygon(patron)
    localPatron = localPatron.difference(localShape) # to create the new patron
    localPatronTabFloat = localPatron.exterior.coords[:] # to convert the object polygon into a tab of float
    localPatronTabInt = []
    for i in reversed(range(len(localPatronTabFloat))): # a certain order is needed to detect fits
        localPatronTabInt.append([int(localPatronTabFloat[i][0]),int(localPatronTabFloat[i][1])])
    localPatronTabInt.pop() # to delete the last value which is also the first (avoiding double detection)
    print(localPatronTabInt)
    return localPatronTabInt

#_________________________________________________TEST_________________________________________________

listResult = shapeFits(model.SHAPE_1, model.PATRON)
print(listResult)
print(model.PATRON)
model.PATRON = reshapePatron(listResult[0], model.SHAPE_1, model.PATRON)
print(model.PATRON)
listResult = shapeFits(model.SHAPE_1, model.PATRON)
print(listResult)

#_________________________________________________DISPLAY_________________________________________________


vue.affiche()

#_________________________________________________RULES_________________________________________________

