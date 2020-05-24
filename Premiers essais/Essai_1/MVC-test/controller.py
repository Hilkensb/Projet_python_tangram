import model
import vue

import numpy
import matplotlib.path as mpltPath
import matplotlib.pyplot as mpltPlt
import networkx as nx
import shapely.wkt
from shapely.geometry import LineString




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

class node:
    def __init__(self, shape, patron, father):
        self.shape = shape
        self.patron = patron
        self.father = father
    def mySonIs(self, son):
        self.son = son
        

#_________________________________________________TEST_________________________________________________

# listResult = shapeFits(model.SHAPE_1, model.PATRON)
# print(listResult)
# print(model.PATRON)
# model.PATRON = reshapePatron(listResult[0], model.SHAPE_1, model.PATRON)
# print(model.PATRON)
# listResult = shapeFits(model.SHAPE_1, model.PATRON)
# print(listResult)

# print("Graph : ")
# buildGraph([model.SHAPE_1,model.SHAPE_2,model.SHAPE_3],model.PATRON,listResult)

#_________________________________________________DISPLAY_________________________________________________


vue.affiche()

DG = nx.DiGraph()
dicoResult = []

graphLevel = 0
nodeID = 0
cpt = 0
str_graphLevel = str(graphLevel) + "_" + str(nodeID)
dicoResult[cpt][0] = str_graphLevel
dicoResult[cpt][1] = model.PATRON
dicoResult[cpt][2] = model.SHAPE_LIST
DG.add_node(str_graphLevel)
listResult = shapeFits(model.SHAPE_1, model.PATRON)

graphLevel+=1
nodeID = 0
cpt = 1
str_graphLevel_father = str_graphLevel

while listResult:
    str_graphLevel = str(graphLevel) + "_" + str(nodeID)
    DG.add_node(str_graphLevel)
    DG.add_edge(str_graphLevel_father,str_graphLevel)
    listResult.pop()
    nodeID+=1
print("Nodes of graph: ")
print(DG.nodes())
print("Edges of graph: ")
print(DG.edges())
nx.draw(DG, with_labels=True)
mpltPlt.savefig("test.png")
#_________________________________________________RULES_________________________________________________

