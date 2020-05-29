import model
import vue

import numpy
import re
import matplotlib.path as mpltPath
import matplotlib.pyplot as mpltPlt
import networkx as nx
import shapely.wkt
from shapely.geometry import LineString
from shapely.geometry import Polygon

# function to transform the coordinates of a shape to be displayed at a certain
# localisation
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







# vue.affiche()

# DG = nx.DiGraph()

# graphLevel = 0
# nodeID = 0
# tabGraphLevel = []

# for i in range(len(model.SHAPE_LIST)):
#     listResult = shapeFits(model.SHAPE_LIST[i], model.PATRON)
#     if(listResult):
#         break

# str_graphLevel = str(graphLevel) + "_" + str(nodeID)
# DG.add_node(str_graphLevel, visited = False, patron = model.PATRON, shapes = model.SHAPE_LIST, listResult = listResult)
# DG.add_node("End",terminated = True)

# graphLevel += 1
# nodeID = 0
# tabGraphLevel[0] = 1
# str_graphLevel_father = str_graphLevel

# while not(DG.nodes( data = 'visited')["0_0"]):
#     str_graphLevel = str(graphLevel) + "_" + str(nodeID)
#     fatherPatron = DG.nodes( data = 'patron')[str_graphLevel_father]
#     fatherShapeList = DG.nodes( data = 'shapes')[str_graphLevel_father]
#     fatherListResult = DG.nodes( data = 'listResult')[str_graphLevel_father]
#     newPatron = reshapePatron(fatherListResult[-1], fatherShapeList[0], fatherPatron)
#     #________________________________________marche pas besoin de mettre la forme correspondante à la list result
#     newShapeList = fatherShapeList.copy()
#     newShapeList.pop()
#     for i in range(len(newShapeList)):
#         listResult = shapeFits(newShapeList[i], newPatron)
#         if(listResult):
#             break
#     DG.add_node(str_graphLevel, visited = False, patron = newPatron, shapes = newShapeList, listResult = listResult)
#     DG.add_edge(str_graphLevel_father,str_graphLevel)
    
#     if listResult:
#         str_graphLevel_father = str_graphLevel
#         tabGraphLevel[graphLevel]+=1
#         graphLevel +=1
#     elif not(listResult) and not(newShapeList):
#         print("RESULTAT")
#         print(str_graphLevel)
#         DG.add_edge(str_graphLevel_father,"End")
#         graphLevel -=1
    
#     elif not(listResult) and newShapeList:
#         print("CA MARCHE PAS")
#         graphLevel -=1
    

#_________________________________________________DISPLAY_________________________________________________

DG = nx.DiGraph()

graphLevel = 0
nodeID = 0
SUCCESS = False

for i in range(len(model.SHAPE_LIST)):
    listResult = shapeFits(model.SHAPE_LIST[i], model.PATRON)
    if(listResult):
        break
    
str_graphLevel = str(graphLevel) + "_" + str(nodeID)
DG.add_node(str_graphLevel, patron = model.PATRON, shapes = model.SHAPE_LIST, listResult = listResult,terminated = False)
DG.add_node("End",terminated = True)

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
    while DG.nodes( data = 'listResult' )[str_graphLevel_father]:
        str_graphLevel = str(graphLevel) + "_" + str(nodeID)
        fatherPatron = DG.nodes( data = 'patron')[str_graphLevel_father]
        fatherShapeList = DG.nodes( data = 'shapes')[str_graphLevel_father]
        fatherListResult = DG.nodes( data = 'listResult')[str_graphLevel_father]
        newPatron = reshapePatron(fatherListResult[-1], fatherShapeList[0], fatherPatron)
        #________________________________________marche pas besoin de mettre la forme correspondante à la list result
        newShapeList = fatherShapeList.copy()
        newShapeList.pop()
        if len(fatherListResult) == 1 and len(fatherShapeList) == 1: # which mean that we have a solution
            #DG.nodes( data = 'terminated')[str_graphLevel_father] = True
            DG.add_edge(str_graphLevel_father,"End")
            str_graphLevel = "End"
        else:
            for i in range(len(newShapeList)):
                listResult = shapeFits(newShapeList[i], newPatron)
                if(listResult):
                    break
            DG.add_node(str_graphLevel, patron = newPatron, shapes = newShapeList, listResult = listResult,terminated = False)
            DG.add_edge(str_graphLevel_father,str_graphLevel)
        fatherListResult.pop()
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
    nodeID = 0
    if (str_graphLevel == "End") :
        SUCCESS = True
        break
    else:
        graphLevel += 1
        str_graphLevel_father = str_graphLevel
        
    
print("Nodes of graph: ")
print(DG.nodes())
print("Edges of graph: ")
print(DG.edges())

nx.draw(DG, with_labels=True)
mpltPlt.show()
mpltPlt.savefig("test.png")

print("A*")
print(nx.astar_path(DG,"0_0","End"))

#_________________________________________________RULES_________________________________________________

