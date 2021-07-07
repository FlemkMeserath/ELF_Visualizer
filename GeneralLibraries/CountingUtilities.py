
#OPENS THE STRUCTURE AN GRABS THE LIST OF DIFFERENT ATOMS IN THE UNIT CELL
#THIS IS THE VERY SOLID VERSION WHICH IS NOT AFFECTED BY WEIRD DOUBLE COUTINGS
#RETURNS THE ATOM NAME WITH ITS MULTIPLICITY

def GET_ATOMS_TYPE(Instance):
    AtomsType = Instance.get_chemical_symbols()
    atoms_list = []
    atoms_set = [["X",0],]
    logic_gate = False
    for i in range(0,len(AtomsType)): atoms_list.append(AtomsType[i])
    for i in range(0,len(atoms_list)):
        logic_gate = False
        for j in range(0,len(atoms_set)):
             if atoms_set[j][0] == atoms_list[i]:
                 logic_gate = True
        if logic_gate == False:
            atoms_set.append([atoms_list[i], 0])
            for k in range(i,len(atoms_list)):
                if atoms_list[i] == atoms_list[k]:
                    atoms_set[len(atoms_set)-1][1] = atoms_set[len(atoms_set)-1][1] +1
    return atoms_set



#############################################################################
#General bubble sort routine, coz you never know. :)
def ORDERING(flist):
    swapped = True
    while swapped:
        swapped = False
        for i in range(0,len(flist)-1):
            if flist[i][-1] < flist[i+1][-1]:
                flist[i], flist[i+1] = flist[i+1], flist[i]
                swapped = True
    return flist
##############################################################################