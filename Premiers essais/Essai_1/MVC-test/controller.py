import model
import vue

import numpy
import matplotlib.path as mpltPath
import matplotlib.pyplot as mpltPlt
import networkx as nx
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

#function to get the list of different shapes in a list
#input the list you want to check
#output list of the different shapes
def getDifferentShapes(shapeList) : 
    listResult = []
    for i in range(len(shapeList)) :
        if shapeList[i] not in listResult :
            listResult.append(shapeList[i])
    return listResult

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
                toDelete.append(listResult[i])
    while toDelete:
        occToDelete = toDelete.count(toDelete[0])
        occToDelete /= 2
        occToDelete -= 1
        for i in range(int(occToDelete)):
            listResult.remove(toDelete[0])
            toDelete.remove(toDelete[0])
            toDelete.remove(toDelete[0])
        toDelete.remove(toDelete[0])
        toDelete.remove(toDelete[0])
    #print(listResult)
    return listResult

# function to substract a certain shape to a patron
# input : emplacement of the shape, the shape and the patron
# output : the new patron
def reshapePatron(offset, shape, patron) :
    if not(patron):
        return []
    localShape = Polygon(offsetShape(shape, offset)) # object polygon needed to use the function difference
    localPatron = Polygon(patron)
    try:    
        localPatron = localPatron.difference(localShape) # to create the new patron
    except:
        return []
    if localPatron.geom_type == 'MultiPolygon':
        localPatronTabFloat = []
        for i in range(len(localPatron)):
            localPatronTabFloat += localPatron[i].exterior.coords[:]
        if(localPatronTabFloat[0] == localPatronTabFloat[-1]):
            localPatronTabFloat.pop() # to delete the last value which is also the first (avoiding double detection)
        # print("local patron_mmulti")
        # print(localPatron)
        # print("local patron float_mmulti")
        # print(localPatronTabFloat)
    else:
        localPatronTabFloat = localPatron.exterior.coords[:] # to convert the object polygon into a tab of float
        if localPatronTabFloat: # at the end the result is an empty list and so you can't substract anything
            localPatronTabFloat.pop()# to delete the last value which is also the first (avoiding double detection)
    localPatronTabInt = []
    for i in reversed(range(len(localPatronTabFloat))): # a certain order is needed to detect fits
        localPatronTabInt.append([int(localPatronTabFloat[i][0]),int(localPatronTabFloat[i][1])])
    # print(localPatronTabInt)
    return localPatronTabInt

#function to build the entire graph following the rules of the game using BFS method
#input : a directed graph which will be edited
#output : none
def graphBuilderBFS(DG):
    nodeID = 0
    graphLevel = 0
    str_nodeID = str(graphLevel) + "_" + str(nodeID) 
    DG.add_node(str_nodeID, patron = model.PATRON, shapes = model.SHAPE_LIST)
    DG.add_node("End")
    listParents = [str_nodeID]
    listChilds = []
    coordinatesListChilds = []
    graphLevel += 1
    
    while listParents:
        str_currentNode = listParents.pop(0)
        listDifferentShapes = []
        listShapeResult = [] # first column = the shape second = the result pf this shape in patron
        listDifferentShapes = getDifferentShapes(DG.nodes(data = 'shapes')[str_currentNode])
        #find all the possibilities with this predecessor
        for y in range(len(listDifferentShapes)):
            for i in range(len(DG.nodes(data = 'patron')[str_currentNode])):
                coordinatesListChilds = shapeFits(listDifferentShapes[y], DG.nodes(data = 'patron')[str_currentNode])
                if(coordinatesListChilds):
                    break
            listShapeResult.append([listDifferentShapes[y],coordinatesListChilds]) 
                
        #create all those successors
        for y in range(len(listShapeResult)):
            for i in range(len(listShapeResult[y][1])):
                str_nodeID = str(graphLevel) + "_" + str(nodeID)
                # print(listShapeResult[y][0])
                # print(listShapeResult[y][1])
                newPatron = reshapePatron(listShapeResult[y][1][i], listShapeResult[y][0], DG.nodes(data = 'patron')[str_currentNode])
                newShapes = DG.nodes(data = 'shapes')[str_currentNode].copy()
                for z in range(len(newShapes)):
                    if newShapes[z] == listShapeResult[y][0]:
                        newShapes.pop(z)
                        break
                DG.add_node(str_nodeID, patron = newPatron, shapes = newShapes)
                DG.add_edge(str_currentNode,str_nodeID)
                listChilds.append(str_nodeID)
                nodeID += 1
                model.PATRON_EDITED = newPatron
                #if newPatron: vue.affiche() 
        #if we succeed the game the winning node will be linked to end
        if not(coordinatesListChilds) and not(DG.nodes(data = 'shapes')[str_currentNode]): #checking coo.. is still enough because it'll be full if they are any solution
            DG.add_edge(str_currentNode,"End")
        
        # to watch the building of the graph step by step
        # nx.draw(DG, with_labels=True)
        # mpltPlt.show()
        
        # when you have a certain degree of the graph is complete you skip it and pass to the next level
        if not(listParents):
            graphLevel += 1
            nodeID = 0
            listParents = listChilds.copy()
            coordinatesListChilds.clear()
            listChilds.clear()
  
#_________________________________________________DISPLAY_________________________________________________

vue.mainDisplay()

model.PATRON_EDITED = model.PATRON
model.SHAPE_LIST_EDITED = model.SHAPE_LIST

vue.affiche()

DG = nx.DiGraph()

graphBuilderBFS(DG)
 
    
print("Nodes of graph: ")
print(DG.nodes())
print("Edges of graph: ")
print(DG.edges())

# nx.draw(DG, with_labels=True)
# mpltPlt.show()
# mpltPlt.savefig("test.png")

try:
    print("A*")
    print(nx.astar_path(DG,"0_0","End"))
except:
    print("PAS DE RESULTATS AVEC A*")
   
#_________________________________________________TEST_________________________________________________

#V1


# graphLevel = 0
# nodeID = 0
# SUCCESS = False

# for i in range(len(model.SHAPE_LIST)):
#     listResult = shapeFits(model.SHAPE_LIST[i], model.PATRON)
#     if(listResult):
#         break
    
# str_graphLevel = str(graphLevel) + "_" + str(nodeID)
# DG.add_node(str_graphLevel, patron = model.PATRON, shapes = model.SHAPE_LIST, listResult = listResult,terminated = False)
# DG.add_node("End",terminated = True)

# graphLevel += 1
# nodeID = 0
# str_graphLevel_father = str_graphLevel

# #debug analyse
# print(str_graphLevel)
# print("model.PATRON")
# print(model.PATRON)
# print("model.SHAPE_LIST")
# print(model.SHAPE_LIST)
# vue.affiche()

# while not SUCCESS:   
#     while DG.nodes( data = 'listResult' )[str_graphLevel_father]:
#         str_graphLevel = str(graphLevel) + "_" + str(nodeID)
#         fatherPatron = DG.nodes( data = 'patron')[str_graphLevel_father]
#         fatherShapeList = DG.nodes( data = 'shapes')[str_graphLevel_father]
#         fatherListResult = DG.nodes( data = 'listResult')[str_graphLevel_father]
#         newPatron = reshapePatron(fatherListResult[-1], fatherShapeList[0], fatherPatron)
#         #________________________________________marche pas besoin de mettre la forme correspondante à la list result
#         newShapeList = fatherShapeList.copy()
#         newShapeList.pop()
#         if len(fatherListResult) == 1 and len(fatherShapeList) == 1: # which mean that we have a solution
#             #DG.nodes( data = 'terminated')[str_graphLevel_father] = True
#             DG.add_edge(str_graphLevel_father,"End")
#             str_graphLevel = "End"
#         else:
#             for i in range(len(newShapeList)):
#                 listResult = shapeFits(newShapeList[i], newPatron)
#                 if(listResult):
#                     break
#             DG.add_node(str_graphLevel, patron = newPatron, shapes = newShapeList, listResult = listResult,terminated = False)
#             DG.add_edge(str_graphLevel_father,str_graphLevel)
#         fatherListResult.pop()
#         nodeID+=1
#         #debug analyse
#         print(str_graphLevel)
#         print("fatherPatron")
#         print(fatherPatron)
#         print("newPatron")
#         print(newPatron)
#         print("newShapelist")
#         print(newShapeList)
#         model.PATRON_EDITED = newPatron
#         if newPatron:
#             vue.affiche()
    
#     #prblm on rebalaye pas tous les fils dans l'instance suivante
#     nodeID = 0
#     if (str_graphLevel == "End") :
#         SUCCESS = True
#         break
#     else:
#         graphLevel += 1
#         str_graphLevel_father = str_graphLevel
       

#V2

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