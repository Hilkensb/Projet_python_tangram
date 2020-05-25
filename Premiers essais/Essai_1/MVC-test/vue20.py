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

PATRON = [[0,0],[100,0],[100,100],[200,100],[200,200],[100,200],[0,200],[0,100]]
PATRON_EDITED = [[0,0],[100,0],[100,100],[200,100],[200,200],[100,200],[0,200],[0,100]]

SHAPE_1 = [[0,0],[0,100],[100,100],[100,0]]
SHAPE_2 = [[0,0],[0,100],[100,100],[100,0]]
SHAPE_3 = [[0,0],[0,100],[100,100],[100,0]]
SHAPE_LIST = [SHAPE_1, SHAPE_2, SHAPE_3]
SHAPE_LIST_EDITED = [SHAPE_1, SHAPE_2, SHAPE_3]


main_window = Tk()

canvas_width = 1600
canvas_height = 900
main_window.geometry(str(canvas_width)+"x"+str(canvas_height))

##w = Canvas(main_window,
##           width=100,
##           height=100)
##
##w.create_line(0, 30, 100, 30, fill="#476042")
##w.create_window(400,400,tags='moncu')
##test2 = Canvas(main_window,width=400,heigh=400)
###test2.coords(100,100)
##test2.create_rectangle(0,0,200,200,fill='red')
##w.grid(row=0,column=0)
##test2.grid(row=1,column=0)

my_grid = Canvas(main_window,width=900,height=900)
my_grid.grid(row=1,column=1)

decalage_x=0
decalage_y=0
num_x=0
num_y=0
for x in range(9):
    decalage_y=0
    for y in range(4):
        my_grid.create_rectangle(decalage_x,decalage_y,decalage_x+100,decalage_y+100,fill='green',tag=str(num_y)+"_"+str(num_x))
        decalage_y+=100
        num_y+=1
        print(decalage_y)
    decalage_x+=100
    num_x+=1
    print(decalage_x)


main_window.mainloop()
##
##
##def create_grid(event=None):
##    w = c.winfo_width() # Get current width of canvas
##    h = c.winfo_height() # Get current height of canvas
##    c.delete('grid_line') # Will only remove the grid_line
##
##    # Creates all vertical lines at intevals of 100
##    for i in range(0, w, 100):
##        c.create_line([(i, 0), (i, h)], tag='grid_line')
##
##    # Creates all horizontal lines at intevals of 100
##    for i in range(0, h, 100):
##        c.create_line([(0, i), (w, i)], tag='grid_line')
##
##root = Tk()
##
##c = Canvas(root, height=1000, width=1000, bg='white')
##c.pack(fill=BOTH, expand=True)
##
##c.bind('<Configure>', create_grid)
##
##root.mainloop()