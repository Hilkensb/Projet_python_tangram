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

PATRON = [[0,0],[100,0],[100,100],[200,100],[200,200],[100,200],[0,200],[0,100]]
PATRON_EDITED = [[0,0],[100,0],[100,100],[200,100],[200,200],[100,200],[0,200],[0,100]]

SHAPE_1 = [[0,0],[0,100],[100,100],[100,0]]
SHAPE_2 = [[0,0],[0,200],[100,200],[100,0]]
SHAPE_3 = [[0,0],[0,100],[100,100],[100,0]]
SHAPE_LIST = [SHAPE_1, SHAPE_2, SHAPE_3]
SHAPE_LIST_EDITED = [SHAPE_1, SHAPE_2, SHAPE_3]

SHAPE_FORMS = {"SHAPE_1":[SHAPE_1,0], "SHAPE_2": [SHAPE_2,0]}#here , all shapes that can be used are stored using a associative list, the first value is  the coordinates of  the shape and the second value is if the shape has been clicked or not
PATTERN = [] # pattern that will be used
RESULT = [] # result obtained after a star algorithm was used