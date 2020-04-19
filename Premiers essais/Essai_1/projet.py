import numpy
import cv2

display = numpy.zeros((600,1024,3), numpy.uint8)

display = cv2.rectangle(display,(100,100),(200,200),(0,255,0),3)
display = cv2.rectangle(display,(100,250),(200,350),(0,255,0),3)
display = cv2.rectangle(display,(100,400),(200,500),(0,255,0),3)

pts = numpy.array([[600,100],[700,100],[700,200],[800,200],[800,300],[600,300]], numpy.int32)
img = cv2.polylines(display,[pts],True,(0,255,0),3)

cv2.putText(display,'Formes : ',(0,50), cv2.FONT_HERSHEY_SIMPLEX, 2,(255,255,255),2,cv2.LINE_AA)
cv2.putText(display,'Patron : ',(512,50), cv2.FONT_HERSHEY_SIMPLEX, 2,(255,255,255),2,cv2.LINE_AA)

cv2.imshow('Display',display)
cv2.waitKey(0)
cv2.destroyAllWindows()