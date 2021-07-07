from ase import Atoms
from ase.io import write
from ase.io import read
from math import sqrt
from GeneralLibraries import ConstantsDefinition as C



 ##################################################
 #  PASSING TO CARTESIAN COORDINATES IN ANGSTROM  #
 ##################################################
def TO_CART_ANG(Cpd):
    TMP = [0,0,0]
    for i in range(0,len(Cpd)):
        for j in range(0,3):
            TMP[j] = Cpd.cell[0][j]*Cpd.positions[i][0] + \
                     Cpd.cell[1][j]*Cpd.positions[i][1] + \
                     Cpd.cell[2][j]*Cpd.positions[i][2]
        for j in range(0,3): Cpd.positions[i][j] = TMP[j] * C.BHOR_RADIUS()
    for i in range(0,3):
        Cpd.cell[i] = Cpd.cell[i] * C.BHOR_RADIUS()

    return Cpd
  #################################################


 ##################################################
 #  PASSING TO CARTESIAN COORDINATES IN ANGSTROM  #
 #                DIFFERENT VERSION               #
 ##################################################
def TO_CART_ANG_ALT(Cpd):
    TMP = [0,0,0]
    for i in range(0,len(Cpd.positions)):
        for j in range(0,3):
            TMP[j] = Cpd.cell[0][j]*Cpd.positions[i][0] + \
                     Cpd.cell[1][j]*Cpd.positions[i][1] + \
                     Cpd.cell[2][j]*Cpd.positions[i][2]
        for j in range(0,3): Cpd.positions[i][j] = TMP[j] * C.BHOR_RADIUS()
    for i in range(0,3):
        Cpd.cell[i][0] = Cpd.cell[i][0] * C.BHOR_RADIUS()
        Cpd.cell[i][1] = Cpd.cell[i][1] * C.BHOR_RADIUS()
        Cpd.cell[i][2] = Cpd.cell[i][2] * C.BHOR_RADIUS()

    return Cpd
  #################################################





 ##########################################################
 # REARRANGING THE STRUCTURE TO MAKE IT FIT THE UNIT CELL #
 #   WITHOUT GOING OUT OF IT                              #
 ##########################################################
def FOLDIN_CELL(Cpd):
    for i in range(0, int(len(Cpd))):
        for j in range(0, 3):
            if Cpd.positions[i][j] < 0:
                Cpd.positions[i][j] = 1 + Cpd.positions[i][j]
            elif Cpd.positions[i][j] > 1:
                 Cpd.positions[i][j] =  Cpd.positions[i][j] - 1
    return Cpd
   ###############################################################





#############################################################################
#Mirrors all the atoms closer the INTERVAL to the boundaries of the cell.
#This function helps to visualize how the networks passes from a cell to an other.
def EXPAND_LIST(array): #object like [POS_STORAGE] 
    atom = [0,0,0]
    tmp_list = []
    one_shift = []
    final_list = []
    INTERVAL = 0.00001
 
    for i in range(0, len(array.positions)):  #Cycles on positions

        tmp_list = ["O"]
        one_shift = []
        tmp_list.append(array.positions[i])
        for j in range(0,3):              #Calculates distances from cell and mirroring (working in Crystal coordinates)
            if abs(array.positions[i][j]) <= INTERVAL:
                atom[j] = 1
            elif abs(1-array.positions[i][j]) <= INTERVAL:
                atom[j] = -1
            else:
                atom[j] = 0
        for j in range(0,3):          #Whatever this does it works fine, touch it at your own risk
            for k in range(1,len(tmp_list)):
                if atom[j] != 0:
                    one_shift = []
                    for p in range(0,len(tmp_list[1])):
                        if p == j:
                            one_shift.append(tmp_list[k][p] + atom[j])
                        else:
                            one_shift.append(tmp_list[k][p])
                    tmp_list.append(one_shift)
        for  j in range(2,len(tmp_list)):
            final_list.append(tmp_list[j])
    return final_list 
############################################################################

 
 
