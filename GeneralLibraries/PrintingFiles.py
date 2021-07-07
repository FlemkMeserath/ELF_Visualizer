from GeneralLibraries import ReadingFiles as RF
from GeneralLibraries import ConstantsDefinition as CD


#####################################################
#FUNCTION TO PRINT THE SADDLE POINTS IN AN XYZ FORMAT
#[N_atoms]
#[Auxiliary comment line]
#[atoms in Angstrom]
def WRITE_XYZ_SADDLE_FILE(cpd,sdl,filename,Net_value):   #cpd,sdl are object like [POS_STORAGE], filename is string

    file_to_write = open(filename, "w")
    counter = 0
	
    for i in range(0,len(sdl)):
        if sdl[i][5] < Net_value:
            counter = counter + 1
	
    total_items = len(cpd.positions) + len(sdl) - counter  #Get total number of atoms + saddle points

    file_to_write.write(str(total_items) + "\n\n") #prints [N_atoms] and [auxiliary comment line]



#prints atoms as [Chemical symbol] [x] [y] [z]
    for i in range(0,len(cpd.positions)): 
        file_to_write.write(str(cpd.positions[i][3]) + "    "\
                                + str(cpd.positions[i][0]) + "   "\
                                + str(cpd.positions[i][1]) + "   "\
                                + str(cpd.positions[i][2]) + "\n")                                                    

#prints saddle points as [Indicator (X)] [x] [y] [z] [Saddle points number(critic)] [Index in list] [Saddle point group] [ELF value]
#Only first four columns are read from graphic tools
    for i in range(0,len(sdl)): 
        if sdl[i][5] > Net_value:
            file_to_write.write("X    " \
               + str(sdl[i][0]) + "   "\
               + str(sdl[i][1]) + "   "\
               + str(sdl[i][2]) + "   "\
               + str(sdl[i][3]) + "   "\
               + str(i) + "   "\
               + str(sdl[i][4]) + "   "\
               + str(sdl[i][5]) + "\n") 
####################################################




####################################################################################
#Writes the cube files with atoms and saddle points and the ELF data.
def WRITE_CUBE_SADDLE_FILE(Index,cpd,sdl,filename,Net_value): #Index is an INT, cpd is a [POS_STORAGE] object for atoms, sdl is a [POS_STORAGE] object for saddle points, filename is STRING

    file_to_write = open(filename, "w") #opens file

    counter = 0
	
    for i in range(0,len(sdl)):
        if sdl[i][5] < Net_value:
            counter = counter + 1



    total_items = len(cpd.positions) + len(sdl) - counter #read numbers of lines to write

    file_to_write.write(" Cubefile created from PWScf calculation\n Contains the selected quantity on a FFT grid\n")

    file_to_write.write("  " + str(total_items) +"   0.000000    0.000000    0.000000\n") #prints things

    returned = RF.READ_CUBE(Index,"vectors") #reads vectors to print

    for line in returned: file_to_write.write(line)  #prints all the atoms and saddle points in in Bohr.


    for i in range(0,len(cpd.positions)):
        file_to_write.write(str(cpd.positions[i][5]) + "   " + str(cpd.positions[i][5]) + "   "\
                                + str(cpd.positions[i][0] / CD.BHOR_RADIUS()) + "   "\
                                + str(cpd.positions[i][1] / CD.BHOR_RADIUS()) + "   "\
                                + str(cpd.positions[i][2] / CD.BHOR_RADIUS()) + "\n")

    for i in range(0,len(sdl)): 
        if sdl[i][5] > Net_value:

            file_to_write.write("0    0   " \
               + str(sdl[i][0] / CD.BHOR_RADIUS()) + "   "\
               + str(sdl[i][1] / CD.BHOR_RADIUS()) + "   "\
               + str(sdl[i][2] / CD.BHOR_RADIUS()) + "\n")

    returned = RF.READ_CUBE(Index,"cube")   #Prints ELF data.                                                                                                                        
    for line in returned: file_to_write.write(line)
##################################################################################




