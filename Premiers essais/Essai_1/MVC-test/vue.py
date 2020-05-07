import model
import numpy
import cv2

def offsetShape (shape, offset) :
    for i in range(0, len(shape)) :
        shape[i][0] += offset[0]
        shape[i][1] += offset[1]
    return shape

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
    pts = numpy.array(offsetShape(model.PATRON,[600,100]), numpy.int32)
    cv2.fillPoly(display, [pts], model.RED)
    display = cv2.polylines(display,[pts],True,model.WHITE,3)
    
    cv2.putText(display,'Formes : ',(0,50), cv2.FONT_HERSHEY_SIMPLEX, 2,model.WHITE,2,cv2.LINE_AA)
    cv2.putText(display,'Patron : ',(512,50), cv2.FONT_HERSHEY_SIMPLEX, 2,model.WHITE,2,cv2.LINE_AA)
    
    cv2.imshow('Display',display)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
    return 0
