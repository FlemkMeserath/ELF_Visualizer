import re
import os



def GREP_STRUCTURE_FROM_CRITIC(filename):
 
    Keyword = "+ List of atoms in the unit cell (cryst. coords.):"
    Atomic_List = []

    TRIGGER_FLAG = False
    Counter = 0

    critic_out = open(str(filename), "r")

    Counter = 0
    for line_to_read in critic_out:
        if Keyword in line_to_read:
            TRIGGER_FLAG = True
        if line_to_read == "\n":
            TRIGGER_FLAG = False
        if TRIGGER_FLAG == True:
            Counter = Counter + 1
            if Counter > 2: 
                splitted_chars = re.findall(r'\S*', line_to_read)
                stored_line = []
                for char in splitted_chars:
                    if char != "":       #REMOVING EMPTY CHARS
                        stored_line.append(char)    #STORING NON EMPTY CHARS
                Atomic_List.append(stored_line)

    return Atomic_List

def GREP_CELL_FROM_CRITIC(filename):
 
    Keyword = "+ Lattice vectors (bohr)"
    Vector_List = []
    TRIGGER_FLAG = False

    critic_out = open(str(filename), "r")

    for line_to_read in critic_out:

        if line_to_read == "\n":
            TRIGGER_FLAG = False

        if TRIGGER_FLAG == True:
                splitted_chars = re.findall(r'\S*', line_to_read)
                stored_line = []
                for char in splitted_chars:
                    if char != "":       #REMOVING EMPTY CHARS
                        stored_line.append(char)    #STORING NON EMPTY CHARS
                Vector_List.append(stored_line)

        if Keyword in line_to_read:
            TRIGGER_FLAG = True
    return Vector_List



def GREP_AllBONDS_FROM_CRITIC(Index,Keyword):
    STORE_FLAG  = False      #FLAG TO TRIGGER DATA ACQUISITION
    bond_list = []           #DEFINING ARRAYS
    stored_line = []
    List_Keyword = "* Complete CP list,"
    critic_out = open(str(Index), "r") #OPENING FILE

    for line_to_read in critic_out:        #CYCLING OVER THE FILE
        if List_Keyword in line_to_read: STORE_FLAG = True
        if Keyword in line_to_read:     #CNDITION TO TRIGGER DATA ACQUISITION
            if STORE_FLAG == True:             #IF THE KEYWORD WAS MET
                splitted_chars = re.findall(r'\S*', line_to_read)    #SLITTING CHE CHARS IN THE LINE
                stored_line = []        #CLEANING ARRAY TO STORE CHARS
                if splitted_chars[0] != "#"and\
                   splitted_chars[0] != "*":           #ESCLUDING FIRST LINE AND COMMENTS
                    if len(splitted_chars) <= 8:
                        STORE_FLAG = False    # IN CASE THERE ARE LESS THEN 4 CHARS IT STOPS DATA ACQUISITION
                    else:
                        for char in splitted_chars:  #SAVES THE NON EMPTY CHARS
                            if char != "" and char != "x":     #EXCLUDES EMPTY CHARS
                                stored_line.append(char)
                        bond_list.append(   [ int( stored_line[0] ), \
                                              int( stored_line[1] ), \
                                             float(stored_line[3] ), \
                                             float(stored_line[4] ), \
                                             float(stored_line[5] ) ] )
               #SAVING RELAVANT VARS IN FINAL LIST: num, Atm1 #atm Atm2 #atm dist1 dist2 ratio angle
    return bond_list

def GREP_BONDSELF_FROM_CRITIC(Index,Keyword): #GETS NUMBER OF COMPOUND AND WHAT TO GREP bond,ring,cage (nucleai non implemented. might not work)

    f_number = 9             #DEFAULT VALUES FOR ELF COLUMN TO GREP
    bond_list = []           #DEFINING ARRAYS
    stored_line = []

    if Keyword   == "ring": f_number=10   #LISTO OF KEYWORD INDEXS FOR COLUMN TO GREP
    elif Keyword == "bond": f_number = 9
    elif Keyword == "cage": f_number = 11

    critic_out = open(str(Index), "r") #OPENING FILE

    for line_to_read in critic_out: #CYCLING ON LINES
        if Keyword in line_to_read:  #LOOKING FOR KEYWORD IN LINE
            splitted_chars = re.findall(r'\S*', line_to_read) #SPLITTING LINE
            stored_line = []         #CLEANING ARRAY TO STORE CHARS
            for char in splitted_chars:
                if char != "":       #REMOVING EMPTY CHARS
                    stored_line.append(char)    #STORING NON EMPTY CHARS
            if stored_line[0] != "#" and \
               stored_line[0] != "*" and \
               stored_line[0] != "+":   #^^^REMOVING NON NECESSARY LINES
                bond_list.append( [ int(  stored_line[0]),\
                                   float( stored_line[f_number]),\
                                    str(  stored_line[1])] ) #SAVING RELEVANT VARS 1 NUMBER 2 ELF 3 RANDOM THING I DON'T UNDERSTAN
    return bond_list
######################################################################



###################################################################################
#Thus function is neccessary to take the ELF data and the cell vectors data from the cube files
# and to attatch them to the cube file with the saddle points.
def READ_CUBE(Index,Request):  #Index is INT, request is string, either "vectors" or "cube"

    cube_file = open(str(Index)) #opens the file
    count = 0 
    Final_list = []
    stored_line = [100,100] #storing array

    if Request == "vectors":  #grabs the vectors from the file
        for line in cube_file:
            if count > 2 and count < 6: Final_list.append(line)
            count = count + 1
    elif Request == "cube":   #grabs the cube data from the file
        for line in cube_file:
            if count == 2:
                splitted_chars = re.findall(r'\S*', line)
                stored_line = []
                for char in splitted_chars:
                    if char != "": stored_line.append(char) 

            if count > (5+int(stored_line[0])): Final_list.append(line)
            count = count +1

    else: return 0  
    

    return Final_list
####################################################################################


