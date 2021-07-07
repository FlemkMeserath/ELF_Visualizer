from GeneralLibraries import ReadingFiles as RF
from GeneralLibraries import GeneralUtilities as GU
from GeneralLibraries import DistanceUtilities as D
from GeneralLibraries import CountingUtilities as C
from GeneralLibraries import PrintingFiles as PF
from ase import Atoms
import sys
import re

##############################################
#CLASS TO STORE SADDLE POINTS
class POS_STORAGE():
    cell = []
    positions = []

#DEFINING AN AUXILIARY CLASS FOR THE ATOMS
class POS_STORAGE2():
    cell = []
    positions = []
###############################################

POS = []
NUM   = []
CELL     = []
Keyword = " b " #Keyword for critic acquisition



CriticPath = sys.argv[1]
CubePath = sys.argv[2]
Networking_Value = float(sys.argv[3])


B = RF.GREP_STRUCTURE_FROM_CRITIC(CriticPath)
A = RF.GREP_CELL_FROM_CRITIC(CriticPath)


for b in range(0,len(B)):
    POS.append([float(B[b][1]), float(B[b][2]), float(B[b][3])])
    NUM.append(int(B[b][5]))

for a in range(0,len(A)):
    CELL.append([ float(A[a][1]), float(A[a][2]), float(A[a][3]) ])

Instance = Atoms(numbers = NUM, cell= CELL, positions = POS)
#atomic_set = C.GET_ATOMS_TYPE(Instance)  #Retrns the atom names with the multiplicity
#atom_list = Instance.get_atomic_numbers() #gets the atomic numbers from the atoms in the compountds.

Saddle = POS_STORAGE
Structure = POS_STORAGE2

#Fills the objects with the structures in Bohr
for i in range(0,3):
    Saddle.cell.append([Instance.cell[i][0],Instance.cell[i][1],Instance.cell[i][2]])
    Structure.cell.append([Instance.cell[i][0],Instance.cell[i][1],Instance.cell[i][2]])

#greps the saddle point position data from Critic
tmp_bond_list = RF.GREP_AllBONDS_FROM_CRITIC(CriticPath,Keyword)


#makes sure all the atoms are folded inside the unit cell.
Instance = D.FOLDIN_CELL(Instance)


#Fills the saddle point array with the position of the saddle points and the extra data.
# [x] [y] [z] [Saddle points number(critic)] [Index in list] [Saddle point group] [ELF value](this last one is set to 0 for now)
for line in tmp_bond_list:
    Saddle.positions.append([line[2],line[3],line[4],    line[0],line[1],0])
#Fills the Instance object with the atomic positions.
TMPA = Instance.get_chemical_symbols()
TMPB = Instance.get_atomic_numbers()
for i in range(0,len(Instance)):
    Structure.positions.append([Instance.positions[i][0],\
                                Instance.positions[i][1],\
                                Instance.positions[i][2],\
                                TMPA[i],i,TMPB[i]])





#replicates the atoms and saddle points at the boundaries of the cell
list_addendum = D.EXPAND_LIST(Structure)

for i in range(0,len(list_addendum)):
    Structure.positions.append(list_addendum[i])

list_addendum = D.EXPAND_LIST(Saddle) 
for i in range(0,len(list_addendum)): 
    Saddle.positions.append(list_addendum[i])




#Convert the stucture to cartesian Angstrom
Structure = D.TO_CART_ANG_ALT(Structure)
#converts the saddle points to cartesian Angstrom
Saddle = D.TO_CART_ANG_ALT(Saddle)

#removes saddle points too close to atoms
Saddle.positions = GU.REMOVE_NOISE_SADDLE(Structure,Saddle)



#Greps and add the saddle point ELF value to the saddle point list.
ELF_values= RF.GREP_BONDSELF_FROM_CRITIC(CriticPath,"bond")

for i in range(0, len(ELF_values)):
    for j in range(0,len(Saddle.positions)):
        if Saddle.positions[j][4] == ELF_values[i][0]:
            Saddle.positions[j][5] = ELF_values[i][1]  

#Orders Saddle points in ELF
Saddle.positions =  C.ORDERING(Saddle.positions)





#prints the files
PF.WRITE_XYZ_SADDLE_FILE(Structure,Saddle.positions,"ELF_NETWORK.xyz",Networking_Value)
if CubePath != "None":
    PF.WRITE_CUBE_SADDLE_FILE(CubePath,Structure,Saddle.positions,"ELF_NETWORK.cube",Networking_Value)








