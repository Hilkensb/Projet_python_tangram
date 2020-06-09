# coding: utf-8
#____________________________Input___________________

def main():
    pass

if __name__ == '__main__':
    main()

from tkinter import *
from tkinter.messagebox import *

import model
from shapely.ops import cascaded_union
from shapely.geometry import Polygon
from shapely.ops import unary_union


#faire laselction point ou forme , enregiste nombre forme utilisé , puis épuré le code

clickedOnShape = 0

POINT_INTER= []
OVAL_CREATED = []
SHAPES_ON_GRID=[]
GRID_MATRIX = {}

canvas_width = 1600
canvas_height = 900

main_window = Tk()
main_window.geometry(str(canvas_width)+"x"+str(canvas_height))
my_grid = Canvas(main_window,width=900,height=900)
my_shapes = Canvas(main_window,width=300,height=900)
my_button = Canvas(main_window,width=200,height=900)




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
            if decalage_x not in POINT_INTER and  decalage_y not in POINT_INTER :
                POINT_INTER.append([decalage_x,decalage_y])
            if decalage_x+100 not in POINT_INTER and  decalage_y+100 not in POINT_INTER :
                POINT_INTER.append([decalage_x+100,decalage_y+100])

            my_grid.create_rectangle(decalage_x,decalage_y,decalage_x+100,decalage_y+100,fill='green',tag=str(num_y)+"_"+str(num_x))
            my_grid.tag_bind(str(num_y)+"_"+str(num_x),'<Button-1>', onObjectClick)
            my_grid.create_text(decalage_x+50,decalage_y+50,text=str(num_y)+"_"+str(num_x))
            GRID_MATRIX[str(num_y)+"_"+str(num_x)] =[0,0]
            decalage_y+=100
            num_y+=1
            print(decalage_y)
        decalage_x+=100
        num_y=0
        num_x+=1
    print(POINT_INTER)

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
    buttonFinish =Button(text="Finish",command = TkObject.destroy )
    buttonQuit = Button(text='Stop', width=25, command=TkObject.destroy)
    my_button.create_window(20,20,window=buttonClear)
    my_button.create_window(20,50,window=buttonFinish)
    my_button.create_window(20,80,window=buttonQuit)

def onFormClick(event):
    global clickedOnShape
    currentElement=event.widget.gettags("current")[0]
    print(event.widget.gettags("current"))



    print(model.SHAPE_FORMS[currentElement])
    if model.SHAPE_FORMS[currentElement][1]== 1 : # if the shape was currently clicked on
        model.SHAPE_FORMS[currentElement][1]= 0 #deselect that shape
        print(" deselection de la forme "+currentElement)
        clickedOnShape = 0

        for k,l in model.SHAPE_FORMS.items():#here we check if no shapes at all were slected
            if model.SHAPE_FORMS[k][1]==1:
                clickedOnShape = 1
    else  :
        model.SHAPE_FORMS[currentElement][1]=1 #select the shape that is currently clicked on
        clickedOnShape = 1
        print(" selection de la forme "+currentElement)




    print(clickedOnShape)

def onObjectClick(event):
    print ('Clicked', event.x, event.y, event.widget)
    print (event.widget.find_closest(event.x, event.y))
    print('clicked ',event.widget.gettags("current")[0])
    print(clickedOnShape)
    counter =0
    erro = False



    if clickedOnShape == 0: #there is no shape who has been clicked on
        offsetPtn=50 # raduius of the point
        for k in POINT_INTER:
            if (event.x <= k[0]+offsetPtn and event.x >= k[0]-offsetPtn) and(event.y <= k[1]+offsetPtn and event.y >= k[1]-offsetPtn) and ([k[0],k[1]] not in model.PATRON):
       	        oval=my_grid.create_oval(k[0]-5,k[1]-5,k[0]+5,k[1]+5, fill="black")
                OVAL_CREATED.append(oval)
                model.PATRON.append([k[0],k[1]])
    else :
        for i,j in model.SHAPE_FORMS.items():#range(len(model.SHAPE_FORMS)):
            if model.SHAPE_FORMS[i][1] == 1 :
                counter+=1
                if counter >= 2 :
                    erro = True
                    showwarning("warning","impossible de selectionne plus de deux forme a la foix, veuillez deselctionne toute les forme dabord")

        if not erro :
            for k,l in model.SHAPE_FORMS.items():#range(len(model.SHAPE_FORMS)):
                if model.SHAPE_FORMS[k][1] == 1 and GRID_MATRIX[event.widget.gettags("current")[0]][1] == 0 :
                    GRID_MATRIX[event.widget.gettags("current")[0]] =[model.SHAPE_FORMS[k][0],1]
                    poly = my_grid.create_polygon(model.SHAPE_FORMS[k][0],tag="SHAPE_ON_"+str(event.widget.gettags("current")[0]))
                    SHAPES_ON_GRID.append(poly)
                    offset=[100*int(event.widget.gettags("current")[0][2]),100*int(event.widget.gettags("current")[0][0])]#offset
                    print(event.widget.gettags("current")[0])
                    print("Shape list")
                    model.SHAPE_LIST.append(model.SHAPE_FORMS[k][0])#add shape used to shape list
                    print(model.SHAPE_LIST)
                    #for i in range(len(model.SHAPE_FORMS[k][0])) :
    	               # model.POLYGON_ON_GRID.append([model.SHAPE_FORMS[k][0][i][0]+offset[0],model.SHAPE_FORMS[k][0][i][1]+offset[1]])# used to be polygon used according to offset
                    my_grid.move(poly,100*int(event.widget.gettags("current")[0][2]),100*int(event.widget.gettags("current")[0][0])) #move the drawn polygon to the correct location
    				#model.POLYGON_ON_GRID.append(offsetShape(model.SHAPE_FORMS[k][0],[100*int(event.widget.gettags("current")[0][2]),100*int(event.widget.gettags("current")[0][0])]))## only safe the form of shapes saved and maybe the outline

    print(model.PATRON)





def clearAllShapes(): #will delete all elements added on interface or any data added un the different containers from model
    for b in range(len(SHAPES_ON_GRID)):
        my_grid.delete(SHAPES_ON_GRID[b])
    for b in SHAPES_ON_GRID:
        my_grid.delete(b)
    for b in OVAL_CREATED:
        my_grid.delete(b)
    #clean grid
    for  o,p in GRID_MATRIX.items() :
        GRID_MATRIX[o] = [0,0]
    model.PATRON= []
    model.SHAPE_LIST = []

def finishSelection():
    final_window = Tk()
    final_window.geometry(str(canvas_width)+"x"+str(canvas_height))

    my_gridFinal = Canvas(main_window,width=400,height=900)
    finalPoly = my_gridFinal.create_polygon(model.RESULT,tag="FINAL_POLYGON")
    for i in model.RESULT:
        oval=my_grid.create_oval(i[0]-5,i[1]-5,i[0]+5,i[1]+5, fill="black")

    my_buttonFinish = Canvas(main_window,width=200,height=900)
    my_buttonFinish.grid(row=1,column=2)

    buttonExit = Button(text='Exit', width=25, command=main_window.destroy)
    buttonExit.place(x=10,y=10)
    mainDisplay()
    print(model.PATRON)
    print("lol")

    #içi  on passe du coup un polygon pour le controlleur
    #on recrée tout ensuite et on affiche le polygon reconstruit à partir de l'aglo

## can be replacedby tag instead of all canvas.delete("all")



#____________________________Output___________________

import model
import numpy
import cv2

def offsetShape (shape, offset) :
    localShape = numpy.copy(shape)
    for i in range(0, len(shape)) :
        localShape[i][0] += offset[0]
        localShape[i][1] += offset[1]
    return localShape

def affiche():
    display = numpy.zeros((model.SCREEN_LENGTH,model.SCREEN_WIDTH,3), numpy.uint8)
    
    #to dispaly the grid
    for i in range(1,model.NB_LINES+1):
        display = cv2.line(display, (100,i*100), (model.SCREEN_WIDTH-100,i*100), model.GRAY, 1)
        cv2.putText(display,(str)(i*100)  ,(30,i*100+10), cv2.FONT_HERSHEY_SIMPLEX, 1,model.WHITE,2,cv2.LINE_AA)
    for i in range(1,model.NB_COLUMNS+1):
        display = cv2.line(display, (i*100,100), (i*100,model.SCREEN_LENGTH-100), model.GRAY, 1)
        cv2.putText(display,(str)(i*100)  ,(i*100-20,85), cv2.FONT_HERSHEY_SIMPLEX, 1,model.WHITE,2,cv2.LINE_AA)
    
    #Shape_1
    pts = numpy.array(offsetShape(model.SHAPE_1,[100,100]), numpy.int32)
    cv2.fillPoly(display, [pts], model.BLUE)
    display = cv2.polylines(display,[pts],True,model.WHITE,3)
    
    #Shape_2
    pts = numpy.array(offsetShape(model.SHAPE_2,[200,100]), numpy.int32)
    cv2.fillPoly(display, [pts], model.BLUE)
    display = cv2.polylines(display,[pts],True,model.WHITE,3)
    
    #Shape_3
    pts = numpy.array(offsetShape(model.SHAPE_3,[300,100]), numpy.int32)
    cv2.fillPoly(display, [pts], model.BLUE)
    display = cv2.polylines(display,[pts],True,model.WHITE,3)
    
    #Patron
    pts = numpy.array(offsetShape(model.PATRON_EDITED,[600,100]), numpy.int32)
    cv2.fillPoly(display, [pts], model.RED)
    display = cv2.polylines(display,[pts],True,model.WHITE,3)
    
    cv2.putText(display,'Formes : ',(0,50), cv2.FONT_HERSHEY_SIMPLEX, 2,model.WHITE,2,cv2.LINE_AA)
    cv2.putText(display,'Patron : ',(512,50), cv2.FONT_HERSHEY_SIMPLEX, 2,model.WHITE,2,cv2.LINE_AA)
    
    cv2.imshow('Display',display)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
    return 0