#-------------------------------------------------------------------------------
# Name:        module1
# Purpose:
#
# Author:      bramh_000
#
# Created:     25/05/2020
# Copyright:   (c) bramh_000 2020
# Licence:     <your licence>
#-------------------------------------------------------------------------------

def main():
    pass

if __name__ == '__main__':
    main()

from tkinter import *
import model
from shapely.ops import cascaded_union
from shapely.geometry import Polygon
from shapely.ops import unary_union



##def offsetShape (shape, offset) :
##    localShape = numpy.copy(shape)
##    for i in range(0, len(localShape)) :
##        localShape[i][0] += offset[0]
##        localShape[i][1] += offset[1]
##    return localShape



SHAPES_ON_GRID=[]
GRID_MATRIX = {}

canvas_width = 1600
canvas_height = 900

main_window = Tk()
main_window.geometry(str(canvas_width)+"x"+str(canvas_height))
my_grid = Canvas(main_window,width=900,height=900)
my_shapes = Canvas(main_window,width=200,height=900)
my_button = Canvas(main_window,width=200,height=900)




def DelOccurence(listOfThings):
    toDelete = []
    for i in range(len(listOfThings)): # to delete the double detections must do all that stuff because list(set( methods isn't working with this kind  of list))
        for y in range(len(listOfThings)):
            if (listOfThings[i] == listOfThings[y]) and (i != y):
                toDelete.append(listOfThings[i])
    for k in toDelete :
        if k in listOfThings :
           listOfThings.remove(k)

    poly = Polygon([(800, 0),(800, 100),(900, 100)])
    poly2 = Polygon( [(800, 100),(800, 200),(900, 0)])
    poly3= Polygon([(700, 100),(900, 200),(900, 100) ])
    poly4 = Polygon([(700, 200),(800, 200),(800, 100)])

    polylist= [poly,poly2,poly3,poly4]

    poly= unary_union(polylist)

#[[800, 0], [900, 0], [900, 200], [700, 100], [700, 200]]
    return poly



def mainDisplay() :
    showGrid(main_window)
    showShapes(main_window)
    showButton(main_window)
    main_window.mainloop()


def showGrid(TkObject):
    decalage_x=0
    decalage_y=0
    num_x=0
    num_y=0
    my_grid.grid(row=1,column=1)
    for x in range(9):
        decalage_y=0
        for y in range(4):
            my_grid.create_rectangle(decalage_x,decalage_y,decalage_x+100,decalage_y+100,fill='green',tag=str(num_y)+"_"+str(num_x),width=20)
            my_grid.tag_bind(str(num_y)+"_"+str(num_x),'<Button-1>', onObjectClick)
            my_grid.create_text(decalage_x+50,decalage_y+50,text=str(num_y)+"_"+str(num_x))
            GRID_MATRIX[str(num_y)+"_"+str(num_x)] =[0,0]
            decalage_y+=100
            num_y+=1
            print(decalage_y)
        decalage_x+=100
        num_y=0
        num_x+=1
        print(decalage_x)

def showShapes(TkObject) :
    decalagePoly=0
    numPoly=1
    my_shapes.grid(row=1,column=2)
    for x,v in model.SHAPE_FORMS.items() : #range(len(model.SHAPE_FORMS)):
   # for i in range(len(model.SHAPE_LIST_EDITED[x])):
        test=my_shapes.create_polygon(model.SHAPE_FORMS[x][0],fill="red",outline="black",tag="SHAPE_"+str(numPoly))
        my_shapes.tag_bind("SHAPE_"+str(numPoly),'<Button-1>', onFormClick)
        my_shapes.move(test,10,decalagePoly)
        decalagePoly+=102
        numPoly+=1

def showButton(TkObject) :
    my_button.grid(row=1,column=3)
    buttonClear =Button(text="Clear_all",command = clearAllShapes )
    buttonFinish =Button(text="Finish",command = finishSelection )
    buttonQuit = Button(text='Stop', width=25, command=TkObject.destroy)
    my_button.create_window(20,20,window=buttonClear)
    my_button.create_window(20,50,window=buttonFinish)
    my_button.create_window(20,80,window=buttonQuit)

def onFormClick(event):
    counter =0
    for i,j in model.SHAPE_FORMS.items():#range(len(model.SHAPE_FORMS)):
        if model.SHAPE_FORMS[i][1] == 1 :
            counter+=1
        if counter >= 2 :
            print("something's wrong")
        else :
            print(model.SHAPE_FORMS[event.widget.gettags("current")[0]])
            if model.SHAPE_FORMS[event.widget.gettags("current")[0]][1]== 1 :
                model.SHAPE_FORMS[event.widget.gettags("current")[0]][1]= 0
                print(" déselection de la forme "+event.widget.gettags("current")[0])
            else :
                model.SHAPE_FORMS[event.widget.gettags("current")[0]][1]=1
                print(" selection de la forme "+event.widget.gettags("current")[0])


def onObjectClick(event):
    print ('Clicked', event.x, event.y, event.widget)
    print (event.widget.find_closest(event.x, event.y))
    print('clicked ',event.widget.gettags("current")[0])

    for k,l in model.SHAPE_FORMS.items():
        if model.SHAPE_FORMS[k][1] == 1 and GRID_MATRIX[event.widget.gettags("current")[0]][1] == 0 :
            GRID_MATRIX[event.widget.gettags("current")[0]] =[model.SHAPE_FORMS[k][0],1]
            poly = my_grid.create_polygon(model.SHAPE_FORMS[k][0],tag="SHAPE_ON_"+str(event.widget.gettags("current")[0]))
            SHAPES_ON_GRID.append(poly)

            offset=[100*int(event.widget.gettags("current")[0][2]),100*int(event.widget.gettags("current")[0][0])]
            print(event.widget.gettags("current")[0])
            print("ok")
            print(model.SHAPE_FORMS[k][0])
            for i in range(len(model.SHAPE_FORMS[k][0])) :
                print(i)
                print(model.SHAPE_FORMS[k][0][i])
                model.POLYGON_ON_GRID.append([model.SHAPE_FORMS[k][0][i][0]+offset[0],model.SHAPE_FORMS[k][0][i][1]+offset[1]])
            print(model.POLYGON_ON_GRID)

            my_grid.move(poly,100*int(event.widget.gettags("current")[0][2]),100*int(event.widget.gettags("current")[0][0]))
            #model.POLYGON_ON_GRID.append(offsetShape(model.SHAPE_FORMS[k][0],[100*int(event.widget.gettags("current")[0][2]),100*int(event.widget.gettags("current")[0][0])]))## only safe the form of shapes saved and maybe the outline

        else :
            print ("error there is already a shape on this section or no shape was elected")#showerror showwarning
    print(type(model.POLYGON_ON_GRID[0]))





def clearAllShapes():
    for b in range(len(SHAPES_ON_GRID)):
        my_grid.delete(SHAPES_ON_GRID[b])
    #clean grid
    for  o,p in GRID_MATRIX.items() :
        GRID_MATRIX[o] = [0,0]

    for q in range(len(model.POLYGON_ON_GRID)):
        model.POLYGON_ON_GRID = []


def finishSelection():
    my_grid.grid_remove()
    my_shapes.grid_remove()
    my_button.grid_remove()
    #numpy.concatenate( model.POLYGON_ON_GRID, axis=0 )
    main_window.mainloop()

    newarray = []
    for k in range(len(model.POLYGON_ON_GRID)) :
        for i in  model.POLYGON_ON_GRID[k]:
            newarray.append(i)


    print(model.POLYGON_ON_GRID)
    model.POLYGON_ON_GRID =   DelOccurence(model.POLYGON_ON_GRID)
    print("lol")
    print(model.POLYGON_ON_GRID)

    #içi  on passe du coup un polygon pour le controlleur
    #on recrée tout ensuite et on affiche le polygon reconstruit à partir de l'aglo

## can be replacedby tag instead of all canvas.delete("all")




mainDisplay()