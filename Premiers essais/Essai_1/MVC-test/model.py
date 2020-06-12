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


#version bram
# PATRON = [[0,0],[400,0],[400,400],[0,400]]  # pattern that will be used
# PATRON_EDITED = [[0,0],[400,0],[400,400],[0,400]]
PATRON = []  # pattern that will be used
PATRON_EDITED = []

SHAPE_1 = [[0,0],[0,100],[100,100],[100,0]] # petit carré
SHAPE_2 = [[0,0],[0,200],[100,200],[100,0]] # rectangle vertical
SHAPE_3 = [[0,0],[0,100],[200,100],[200,0]] # rectangle horizontal
SHAPE_4 = [[0,0],[0,200],[200,200],[200,0]] # gros carré
SHAPE_5 = [[0,100],[100,0],[100,200]] # triangle haut à droite
SHAPE_6 = [[0,0],[400,0],[200,200]] # gros triangle haut
SHAPE_7 = [[0,0],[200,200],[0,400]] # gros triangle gauche
SHAPE_8 = [[0,100],[100,0],[200,100],[100,200]] # losange
SHAPE_9 = [[0,100],[100,0],[200,100]] # triangle milieu
SHAPE_10= [[0,100],[100,0],[300,0],[200,100]] # parallèlogramme
SHAPE_11= [[0,200],[200,0],[200,200]] # gros triangle bas droite

# H_SHAPE_1 = 5
# H_SHAPE_2 = 3
# H_SHAPE_3 = 3
# H_SHAPE_4 = 1
# H_SHAPE_5 = 2
# H_SHAPE_6 = 1
# H_SHAPE_7 = 1
# H_SHAPE_8 = 3
# H_SHAPE_9 = 5
# H_SHAPE_10 = 2
# H_SHAPE_11 = 1

H_SHAPE_1 = 1
H_SHAPE_2 = 2
H_SHAPE_3 = 2
H_SHAPE_4 = 10
H_SHAPE_5 = 1
H_SHAPE_6 = 10
H_SHAPE_7 = 10
H_SHAPE_8 = 4
H_SHAPE_9 = 3
H_SHAPE_10 = 7
H_SHAPE_11 = 7

# SHAPE_LIST = [SHAPE_6,SHAPE_7,SHAPE_11,SHAPE_10,SHAPE_9,SHAPE_8,SHAPE_5]
# SHAPE_LIST_EDITED = [SHAPE_6,SHAPE_7,SHAPE_11,SHAPE_10,SHAPE_5,SHAPE_8,SHAPE_9]
SHAPE_LIST = []
SHAPE_LIST_EDITED = []

SHAPE_FORMS = {"SHAPE_1":[SHAPE_1,0], "SHAPE_2": [SHAPE_2,0],"SHAPE_3":[SHAPE_3,0],"SHAPE_4":[SHAPE_4,0],"SHAPE_5":[SHAPE_5,0],"SHAPE_6": [SHAPE_6,0],"SHAPE_7":[SHAPE_7,0],"SHAPE_8":[SHAPE_8,0],"SHAPE_9":[SHAPE_9,0],"SHAPE_10": [SHAPE_10,0],"SHAPE_11":[SHAPE_11,0]}#here , all shapes that can be used are stored using a associative list, the first value is  the coordinates of  the shape and the second value is if the shape has been clicked or not
RESULT = [] # result obtained after a star algorithm was used


#version un rectangle et deux carrés
# PATRON = [[0,0],[100,0],[200,0],[200,100],[200,200],[100,200],[0,200],[0,100]]
# PATRON_EDITED = [[0,0],[100,0],[200,0],[200,100],[200,200],[100,200],[0,200],[0,100]]

# SHAPE_1 = [[0,0],[100,0],[100,200],[0,200]]
# SHAPE_2 = [[0,0],[0,100],[100,100],[100,0]]
# SHAPE_3 = [[0,0],[0,100],[100,100],[100,0]]

# SHAPE_LIST = [SHAPE_3, SHAPE_2, SHAPE_1]
# SHAPE_LIST_EDITED = [SHAPE_3, SHAPE_2, SHAPE_1]


#version que des triangles
# PATRON = [[0,0],[100,100],[0,100],[100,200],[100,100],[200,200],[100,200],[0,200],[0,100]]
# PATRON_EDITED = [[0,0],[100,100],[0,100],[100,200],[100,100],[200,200],[100,200],[0,200],[0,100]]

# SHAPE_1 = [[0,0],[0,100],[100,100]]
# SHAPE_2 = [[0,0],[0,100],[100,100]]
# SHAPE_3 = [[0,0],[0,100],[100,100]]

# SHAPE_LIST = [SHAPE_1, SHAPE_2, SHAPE_3]
# SHAPE_LIST_EDITED = [SHAPE_1, SHAPE_2, SHAPE_3]


#version 1 triangle en haut
# PATRON = [[0,0],[100,100],[200,100],[200,200],[100,200],[0,200],[0,100]]
# PATRON_EDITED = [[0,0],[100,100],[200,100],[200,200],[100,200],[0,200],[0,100]]

# SHAPE_1 = [[0,0],[0,100],[100,100]]
# SHAPE_2 = [[0,0],[0,100],[100,100],[100,0]]
# SHAPE_3 = [[0,0],[0,100],[100,100],[100,0]]

# SHAPE_LIST = [SHAPE_1, SHAPE_2, SHAPE_3]
# SHAPE_LIST_EDITED = [SHAPE_1, SHAPE_2, SHAPE_3]


# version que des carrés
# PATRON = [[0,0],[100,0],[100,100],[200,100],[200,200],[100,200],[0,200],[0,100]]
# PATRON_EDITED = [[0,0],[100,0],[100,100],[200,100],[200,200],[100,200],[0,200],[0,100]]

# SHAPE_1 = [[0,0],[0,100],[100,100],[100,0]]
# SHAPE_2 = [[0,0],[0,100],[100,100],[100,0]]
# SHAPE_3 = [[0,0],[0,100],[100,100],[100,0]]

# SHAPE_LIST = [SHAPE_1, SHAPE_2, SHAPE_3]
# SHAPE_LIST_EDITED = [SHAPE_1, SHAPE_2, SHAPE_3]