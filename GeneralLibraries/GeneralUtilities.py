from math import sqrt
from math import pow


########################################################################
#Function to remove all the saddle points too close to the hydrogen atoms.
#Removes all points closer then 0.34 A to any atom.
def REMOVE_NOISE_SADDLE(cpd,sdl): #cpd,sdl are object like [POS_STORAGE]
    
    sdl_len = len(sdl.positions)#gets N# saddle points
    cpd_len = len(cpd.positions)#gets N# of atoms
    TRIGGER_FLAG = True
    distance = 0
    final_list = []
 
    for i in range(0,sdl_len): #cycle to calculate distance
        TRIGGER_FLAG = True
        for j in range(0,cpd_len):
            if cpd.positions[j][3] == "H":
                distance = 0
                distance = (cpd.positions[j][0]-sdl.positions[i][0])**2
                distance = distance + ( cpd.positions[j][1]-sdl.positions[i][1])**2
                distance = distance + ( cpd.positions[j][2]-sdl.positions[i][2])**2
                distance = sqrt(distance)
            if distance < 0.34:
               TRIGGER_FLAG = False
         
        if TRIGGER_FLAG == True: #storest the saddle points to return
            final_list.append([sdl.positions[i][0],\
                               sdl.positions[i][1],\
                               sdl.positions[i][2],\
                               sdl.positions[i][3],\
                               sdl.positions[i][4],\
                               sdl.positions[i][5]])               
    return final_list                                                                                      
############################################################################