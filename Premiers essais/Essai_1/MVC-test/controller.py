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
#_________________________________________________SUPPRIMER TOUS LES DOUBLONS__________________________________________________________________________________________________________
    toDelete = []
    for i in range(len(listResult)): # to delete the double detections must do all that stuff because list(set( methods isn't working with this kind  of list))
        for y in range(len(listResult)):
            if (listResult[i] == listResult[y]) and (i != y):
                toDelete.append(y)
    toDelete = list(set(toDelete))
    for z in reversed(toDelete):
        listResult.pop(z)
    #print(listResult)
    return listResult

# function to substract a certain shape to a patron
# input : emplacement of the shape, the shape and the patron
# output : the new patron
def reshapePatron(offset, shape, patron) :
    localShape = Polygon(offsetShape(shape, offset)) # object polygon needed to use the function difference
    localPatron = Polygon(patron)
    localPatron = localPatron.difference(localShape) # to create the new patron
    if localPatron.geom_type == 'MultiPolygon':
        localPatronTabFloat = []
        for i in range(len(localPatron)):
            localPatronTabFloat += localPatron[i].exterior.coords[:]
        localPatronTabFloat.pop() # to delete the last value which is also the first (avoiding double detection)
        print("local patron_mmulti")
        print(localPatron)
        print("local patron float_mmulti")
        print(localPatronTabFloat)
    else:
        localPatronTabFloat = localPatron.exterior.coords[:] # to convert the object polygon into a tab of float
        if localPatronTabFloat: # at the end the result is an empty list and so you can't substract anything
            localPatronTabFloat.pop()# to delete the last value which is also the first (avoiding double detection)
    localPatronTabInt = []
    for i in reversed(range(len(localPatronTabFloat))): # a certain order is needed to detect fits
        localPatronTabInt.append([int(localPatronTabFloat[i][0]),int(localPatronTabFloat[i][1])])
    print(localPatronTabInt)
    return localPatronTabInt

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

#vue.affiche()

DG = nx.DiGraph()

graphLevel = 0
nodeID = 0
SUCCESS = False

for i in range(len(model.SHAPE_LIST)):
    listResult = shapeFits(model.SHAPE_LIST[i], model.PATRON)
    if(listResult):
        break
    
str_graphLevel = str(graphLevel) + "_" + str(nodeID)
DG.add_node(str_graphLevel, patron = model.PATRON, shapes = model.SHAPE_LIST)

graphLevel += 1
nodeID = 0
str_graphLevel_father = str_graphLevel

#debug analyse
print(str_graphLevel)
print("model.PATRON")
print(model.PATRON)
print("model.SHAPE_LIST")
print(model.SHAPE_LIST)
vue.affiche()

while not SUCCESS:   
    while listResult:
        str_graphLevel = str(graphLevel) + "_" + str(nodeID)
        fatherPatron = DG.nodes( data = 'patron')[str_graphLevel_father]
        fatherShapeList = DG.nodes( data = 'shapes')[str_graphLevel_father]
        newPatron = reshapePatron(listResult[0], fatherShapeList[0], fatherPatron)
        newShapeList = fatherShapeList.copy()
        newShapeList.pop()
        DG.add_node(str_graphLevel, patron = newPatron, shapes = newShapeList)
        DG.add_edge(str_graphLevel_father,str_graphLevel)
        listResult.pop(0)
        nodeID+=1
        #debug analyse
        print(str_graphLevel)
        print("fatherPatron")
        print(fatherPatron)
        print("newPatron")
        print(newPatron)
        print("newShapelist")
        print(newShapeList)
        model.PATRON_EDITED = newPatron
        if newPatron:
            vue.affiche()
    
    #prblm on rebalaye pas tous les fils dans l'instance suivante
    graphLevel += 1
    nodeID = 0
    str_graphLevel_father = str_graphLevel
    fatherPatron = DG.nodes( data = 'patron')[str_graphLevel_father]
    fatherShapeList = DG.nodes( data = 'shapes')[str_graphLevel_father]
    for i in range(len(fatherShapeList)):
        listResult = shapeFits(fatherShapeList[i], fatherPatron)
        if(listResult):
            break
    if not listResult:
        SUCCESS = True
        print("wahou")
        
print("Nodes of graph: ")
print(DG.nodes())
print("Edges of graph: ")
print(DG.edges())

nx.draw(DG, with_labels=True)
mpltPlt.show()
mpltPlt.savefig("test.png")











DG.add_node("0_0", pat = model.PATRON, tes = model.SHAPE_LIST)
DG.add_node("1_0", var = "test")
DG.add_node("1_1", var = "test")

print(DG.nodes( data = 'tes')["0_0"])


# DG.nodes[0][str_graphLevel] = model.PATRON
# DG.nodes[1][str_graphLevel] = model.SHAPE_LIST

#print(DG.nodes[0][str_graphLevel])
#nx.set_node_attributes(DG, [model.PATRON,model.SHAPE_LIST], str_graphLevel)
#print(nx.get_node_attributes(DG,str_graphLevel))
# print("la")
# var = DG.nodes.data(str_graphLevel,True)
# print(var)

# DG.nodes[str_graphLevel]['patron'] = model.PATRON
# DG.nodes[str_graphLevel]['shape'] = model.SHAPE_LIST
# print(DG.nodes[str_graphLevel]['patron'])
# print(DG.nodes[str_graphLevel]['shape'])


#_________________________________________________RULES_________________________________________________

