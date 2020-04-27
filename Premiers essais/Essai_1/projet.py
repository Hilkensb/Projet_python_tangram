import numpy
import cv2

#main constants
SCREEN_WIDTH = 1000
SCREEN_LENGTH = 600
NB_LINES = 5
NB_COLUMNS = 9

#BGR codes used in the code
GRAY = (192,192,192)
WHITE = (255,255,255)
BLACK = (0,0,0)
RED = (0,0,255)
GREEN = (0,255,0)
BLUE = (255,0,0)

display = numpy.zeros((SCREEN_LENGTH,SCREEN_WIDTH,3), numpy.uint8)

#to dispaly the grid
for i in range(1,NB_LINES+1):
    display = cv2.line(display, (100,i*100), (SCREEN_WIDTH-100,i*100), GRAY, 1)
    cv2.putText(display,(str)(i*100)  ,(30,i*100+10), cv2.FONT_HERSHEY_SIMPLEX, 1,WHITE,2,cv2.LINE_AA)
for i in range(1,NB_COLUMNS+1):
    display = cv2.line(display, (i*100,100), (i*100,SCREEN_LENGTH-100), GRAY, 1)
    cv2.putText(display,(str)(i*100)  ,(i*100-20,85), cv2.FONT_HERSHEY_SIMPLEX, 1,WHITE,2,cv2.LINE_AA)


display = cv2.rectangle(display,(100,100),(200,200),BLUE,3)
display = cv2.rectangle(display,(100,200),(200,300),BLUE,3)
display = cv2.rectangle(display,(100,300),(200,400),BLUE,3)

pts = numpy.array([[600,100],[700,100],[700,200],[800,200],[800,300],[600,300]], numpy.int32)
display = cv2.polylines(display,[pts],True,RED,3)

cv2.putText(display,'Formes : ',(0,50), cv2.FONT_HERSHEY_SIMPLEX, 2,WHITE,2,cv2.LINE_AA)
cv2.putText(display,'Patron : ',(512,50), cv2.FONT_HERSHEY_SIMPLEX, 2,WHITE,2,cv2.LINE_AA)

cv2.imshow('Display',display)
cv2.waitKey(0)
cv2.destroyAllWindows()