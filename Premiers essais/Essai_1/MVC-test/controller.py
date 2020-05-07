import model
import vue

# functio to transform the coordinates of a shape to be displayed at a certain
# locolisation
# input : shape[[x,y]...],
# top left hand corner coordinates where it's displayed [x,y]
# output : new shape with offset
def offsetShape (shape, offset) :
    for i in range(shape) :
        shape[i][0] += offset[0]
        shape[i][1] += offset[1]

def shapeFits (shape, editedPatron):
    return 0

#_________________________________________________TEST_________________________________________________
shapePtaron = model.PATRON
offsetShape(shapePtaron, [1000,1000])
print(shapePtaron)

#_________________________________________________DISPLAY_________________________________________________

vue.affiche()

#_________________________________________________RULES_________________________________________________

