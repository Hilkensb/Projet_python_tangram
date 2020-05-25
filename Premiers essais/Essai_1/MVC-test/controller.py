import model
import vue
import networkx as nx

import shapely.wkt # firestarter?
import math  as mth
from shapely.geometry import LineString

import matplotlib.pyplot as mpltPlt

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
    localPatron = localPatron.difference(localShape) # to create the new patro
    localPatronTab = localPatron.exterior.coords[:] # to convert the object polygon into a tab of float

    print(type(localPatronTab))
    print(localPatronTab[1])

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
G = nx.Graph()
G.add_nodes_from(["a", "b", "c", "d", "e", "f", "g"], type = "machine")
G.add_nodes_from(["h", "i", "j"], type = "human")
G.add_edges_from([("a", "c"), ("a", "b"), ("a", "d"), ("a", "f"), ("b", "d"), ("b", "e"), ("b", "g"), ("c", "f"), ("c", "d"), ("d", "f"), ("d", "e"), ("d", "g"), ("e", "g"), ("f", "g"), ("f", "h"), ("g", "h"), ("h", "i"), ("i", "j")])

mpltPlt.figure()
pos_nodes = nx.spring_layout(G)
nx.draw(G, pos_nodes, with_labels=True)

pos_attrs = {}
for node, coords in pos_nodes.items():
    pos_attrs[node] = (coords[0], coords[1] + 0.08)

node_attrs = nx.get_node_attributes(G, "type")
custom_node_attrs = {}
for node, attr in node_attrs.items():
    custom_node_attrs[node] = "{" + str(type) +":  + attr + }"

nx.draw_networkx_labels(G, pos_attrs, labels=custom_node_attrs)
mpltPlt.show()

dicoResult = []

graphLevel = 0
nodeID = 0
cpt = 0
str_graphLevel = str(graphLevel) + "_" + str(nodeID)
dicoResult[cpt][0] = str_graphLevel
dicoResult[cpt][1] = model.PATRON
dicoResult[cpt][2] = model.SHAPE_LIST