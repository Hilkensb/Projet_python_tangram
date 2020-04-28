# -*- coding: utf-8 -*-
"""
Created on Tue Apr 28 11:26:40 2020

@author: bramh_000
"""
import model
import numpy
import cv2

def affiche():
    display = numpy.zeros((model.SCREEN_LENGTH,model.SCREEN_WIDTH,3), numpy.uint8)
    
    #to dispaly the grid
    for i in range(1,model.NB_LINES+1):
        display = cv2.line(display, (100,i*100), (model.SCREEN_WIDTH-100,i*100), model.GRAY, 1)
        cv2.putText(display,(str)(i*100)  ,(30,i*100+10), cv2.FONT_HERSHEY_SIMPLEX, 1,model.WHITE,2,cv2.LINE_AA)
    for i in range(1,model.NB_COLUMNS+1):
        display = cv2.line(display, (i*100,100), (i*100,model.SCREEN_LENGTH-100), model.GRAY, 1)
        cv2.putText(display,(str)(i*100)  ,(i*100-20,85), cv2.FONT_HERSHEY_SIMPLEX, 1,model.WHITE,2,cv2.LINE_AA)
    
    display = cv2.rectangle(display,(100,100),(200,200),model.BLUE,3)
    display = cv2.rectangle(display,(100,200),(200,300),model.BLUE,3)
    display = cv2.rectangle(display,(100,300),(200,400),model.BLUE,3)
    
    pts = numpy.array(model.PATRON, numpy.int32)
    display = cv2.polylines(display,[pts],True,model.RED,3)
    
    cv2.putText(display,'Formes : ',(0,50), cv2.FONT_HERSHEY_SIMPLEX, 2,model.WHITE,2,cv2.LINE_AA)
    cv2.putText(display,'Patron : ',(512,50), cv2.FONT_HERSHEY_SIMPLEX, 2,model.WHITE,2,cv2.LINE_AA)
    
    cv2.imshow('Display',display)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
    return 0
