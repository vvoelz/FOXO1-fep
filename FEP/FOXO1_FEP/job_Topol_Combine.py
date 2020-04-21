
import os
import sys
import copy

class job_Topol_Combine:

    def __init__(self, read_mcpb, read_hybrid):

        self.path_read_mcpb = read_mcpb
        self.path_read_hybrid = read_hybrid
        self.index_diff = 0

        self.path_write_atomtypes = "new1_atomtypes.itp"
        self.path_write_atoms = "new2_atoms.itp"
        self.path_write_bonds = "new3_bonds.itp"
        self.path_write_pairs = "new4_pairs.itp"
        self.path_write_angles = "new5_angles.itp"
        self.path_write_dihedrals = "new6_dihedrals.itp"

        self.title_atomtypes = "atomtypes"
        self.title_moleculetype = "moleculetype"
        self.title_atoms = "atoms"
        self.title_bonds = "bonds"
        self.title_pairs = "pairs"
        self.title_angles = "angles"
        self.title_dihedrals = "dihedrals"

        self.special_atoms = ['CX', 'A2C', 'A3C', 'Y1', 'CX', 'Y2', 'CX', 'Y3', 'M1']
        self.special_atom_index_m = [1063, 1065, 1068, 1079, 1112, 1126, 1162, 1179, 1572]
        self.special_atom_index_h = []
        self.residues_mcpb = ["LU1", "HE1", "PE1", "MG1"]
        self.residues_hybrid = ["68    LEU", "71    HIS", "74    PHE"]
        self.position_title = 1
        self.position_residue = 3


# /////////////////////////////////////////////////////////////////////////////////////////////////////////

    # Calculate index difference between mcpb and hybrid files.

    def cal_index_diff(self):
        
        with open(self.path_read_mcpb, "r") as f1:
            for line in f1:
                fields = line.strip().split()
                if len(fields) >= 4 and fields[self.position_residue] == "LU1":
                    index_resid_m = fields[0]
                    break
                
        with open(self.path_read_hybrid, "r") as f2:
            for line in f2:
                fields = line.strip().split()
                if len(fields) >= 4 and line[23:32] == "68    LEU":
                    index_resid_h = fields[0]
                    break
                    
        self.index_diff = (int(index_resid_h) - int(index_resid_m))
        # print(self.index_diff)

        self.special_atom_index_h = [i+self.index_diff for i in self.special_atom_index_m]


# /////////////////////////////////////////////////////////////////////////////////////////////////////////

    def newEDIT1_atomtypes(self):

        self.new_itp_file_atomtypes()


    def new_itp_file_atomtypes(self):
            
        fields_per_line = []
        lines = []
        title_found = False

        with open(self.path_read_mcpb, "r") as f:
            for line in f:
                fields = line.strip().split()
                if title_found == False and len(fields) <= 2:
                    continue
                if len(fields) > 2 and fields[self.position_title] == self.title_atomtypes:
                    title_found = True
                if title_found == True and len(fields) > 2:
                    fields_per_line.append(fields)
                    lines.append(line)
                if title_found == True and len(fields) <= 2:
                    break

        # print(len(lines))
        # print(lines)
        # print(fields_per_line)            
                                    
        with open(self.path_write_atomtypes, "w") as f:
            for line in lines:
                f.write(line)
            f.write("\n")    

# /////////////////////////////////////////////////////////////////////////////////////////////////////////

    def newEDIT2_atoms(self):

        lines_special = self.search_residues_mcpb()
        # print(lines_special)
        new_lines = self.modify_atom_index_mcpb(lines_special)
        # this is to make sure lines_special_atoms and new_lines have different address
        lines_special_atoms = copy.copy(new_lines)
        self.new_itp_file_atoms(lines_special_atoms)

    def search_residues_mcpb(self):
            
        fields_per_line = []
        lines = []
        title_found = False

        with open(self.path_read_mcpb, "r") as f:
            for line in f:
                fields = line.strip().split()
                if title_found == False and len(fields) <= 2:
                    continue
                if len(fields) > 2 and fields[self.position_title] == self.title_atoms:
                    title_found = True
                if title_found == True and len(fields) > 3 and fields[self.position_residue] in self.residues_mcpb:
                    fields_per_line.append(fields)
                    lines.append(line)
                if title_found == True and len(fields) <= 2:
                    break

        # print(len(lines))
        # print(lines)
        # print(fields_per_line)
        
        return(lines)

    def modify_atom_index_mcpb(self, lines):

        new_lines = []
        for line in lines:
                new_line = "  " + str(int(line[2:6])+self.index_diff) + line[6:30] \
                                + str(int(line[30:34])+self.index_diff) + line[34:]
                new_lines.append(new_line)
        return new_lines

    def new_itp_file_atoms(self, lines_special_atoms):
        
        fields_per_line = []
        lines = []
        title1_found = False
        title2_found = False

        with open(self.path_read_hybrid, "r") as f1:
        
            for line in f1:
                fields = line.strip().split()
                
                # before title1
                if title1_found == False and len(fields) <= 2:
                    continue
                
                # get title1
                if len(fields) == 3 and fields[self.position_title] == self.title_moleculetype:
                    title1_found = True
                    fields_per_line.append(fields)
                    lines.append(line)
                    continue
                
                # get title2
                if len(fields) == 3 and fields[self.position_title] == self.title_atoms:
                    title2_found = True 
                    fields_per_line.append(fields)
                    lines.append(line)
                    continue
                
                # get content after title1
                if title1_found == True and title2_found == False:
                    fields_per_line.append(fields)
                    lines.append(line)                     
                
                # get content after title2
                if title2_found == True and len(fields) > 3 and line[23:32] not in self.residues_hybrid:
                    fields_per_line.append(fields)
                    lines.append(line) 
                
                # replace content of special atoms (after title2) with their corresponding content in mcpb file
                if title2_found == True and len(fields) > 3 and line[23:32] in self.residues_hybrid:
                    lines.append(lines_special_atoms.pop(0)[:-1] + "     ;<<<<<<<<< update atoms\n")
                            
                if title2_found == True and len(fields) <= 2:
                    break
            
            # add last line: magnesium line, which is not included in hybrid file, from mcpb file to combined file
            lines.append(lines_special_atoms.pop(0)[:-1] + "     ;<<<<<<<<< update atoms\n")    

        # print(len(lines))
        # print(lines)
                                    
        with open(self.path_write_atoms, "w") as f2:
            for line in lines:
                f2.write(line)
            f2.write("\n")           
                
# /////////////////////////////////////////////////////////////////////////////////////////////////////////

    def newEDIT3_bonds(self):

        bonds_fields_mcpb, bonds_lines_mcpb = self.search_bonds_mcpb()
        # print(len(bonds_fields_mcpb))
        # print(len(bonds_lines_mcpb))
        # print(bonds_fields_mcpb)
        # print(bonds_lines_mcpb)

        bonds_fields_hybrid, bonds_lines_hybrid = self.search_bonds_hybrid()
        # print(len(bonds_fields_hybrid))
        # print(len(bonds_lines_hybrid))
        # print(bonds_fields_hybrid)
        # print(bonds_lines_hybrid)

        list_bonds_mcpb_special, strlist_bonds_mcpb_special, index_in_mcpb_special = \
        self.special_bonds_mcpb(bonds_fields_mcpb, bonds_lines_mcpb)
        # print(list_bonds_mcpb_special)
        # print(len(list_bonds_mcpb_special))
        # print(index_in_mcpb_special)
        # print(strlist_bonds_mcpb_special)

        new_list_bonds_mcpb_special, new_strlist_bonds_mcpb_special = \
        self.change_index_special_bonds_mcpb(list_bonds_mcpb_special, strlist_bonds_mcpb_special)
        # print(list_bonds_mcpb_special)
        # print(new_list_bonds_mcpb_special)
        # print(len(new_list_bonds_mcpb_special))
        # print(new_strlist_bonds_mcpb_special)

        list_bonds_hybrid_special, index_in_hybrid_special = \
        self.special_bonds_hybrid(bonds_fields_hybrid)
        # print(list_bonds_hybrid_special)
        # print(len(list_bonds_hybrid_special))
        # print(index_in_hybrid_special)

        count_match, new_list = \
        self.compare_bonds(new_list_bonds_mcpb_special, new_strlist_bonds_mcpb_special, list_bonds_hybrid_special)
        # print(count_match)
        # print(new_list)
        # print(len(new_list))

        new_bonds_lines_hybrid = \
        self.new_itp_file_bonds(bonds_lines_hybrid, bonds_fields_hybrid, new_list, new_strlist_bonds_mcpb_special)
        # print(new_bonds_lines_hybrid)                        
        # print(len(new_bonds_lines_hybrid))

    def search_bonds_mcpb(self):
        
        fields_per_line = []
        lines = []
        title_found = False
        
        with open(self.path_read_mcpb, "r") as f:
            for line in f:
                fields = line.strip().split()        
                if title_found == False and len(fields) <= 2:
                    continue
                if len(fields) > 2 and fields[self.position_title] == self.title_bonds:
                    title_found = True
                if title_found == True and len(fields) > 2:
                    fields_per_line.append(fields)
                    lines.append(line)
                if title_found == True and len(fields) <= 2:
                    break
                    
        return (fields_per_line, lines)

    def search_bonds_hybrid(self):
        
        fields_per_line = []
        lines = []
        title_found = False
        
        with open(self.path_read_hybrid, "r") as f:
            for line in f:
                fields = line.strip().split()        
                if title_found == False and len(fields) <= 2:
                    continue
                if len(fields) > 2 and fields[self.position_title] == self.title_bonds:
                    title_found = True
                if title_found == True and len(fields) > 2:
                    fields_per_line.append(fields)
                    lines.append(line)
                if title_found == True and len(fields) <= 2:
                    break
                    
        return (fields_per_line, lines)

    def special_bonds_mcpb(self, bonds_fields_mcpb, bonds_lines_mcpb):
        
        list_bonds_mcpb_special = []
        index_in_mcpb_special = []
        index_out_mcpb_special =  []

        for i in range(len(bonds_fields_mcpb)):
        
            if i > 1 and (int(bonds_fields_mcpb[i][0]) in self.special_atom_index_m or \
                          int(bonds_fields_mcpb[i][1]) in self.special_atom_index_m):
            
                list_bonds_mcpb_special.append(bonds_fields_mcpb[i])
                index_in_mcpb_special.append(i)
            else:
                index_out_mcpb_special.append(i)

        index_out_mcpb_special.pop(0)
        index_out_mcpb_special.pop(0)

        # this is a new way
        strlist_bonds_mcpb_special = [bonds_lines_mcpb[i] for i in index_in_mcpb_special]
        
        return (list_bonds_mcpb_special, strlist_bonds_mcpb_special, index_in_mcpb_special)

    def change_index_special_bonds_mcpb(self, list_bonds_mcpb_special, strlist_bonds_mcpb_special):
        
        new_list_bonds_mcpb_special = []
        for i in list_bonds_mcpb_special:
        
            result_1 = int(i[0]) + self.index_diff
            result_2 = int(i[1]) + self.index_diff
            new_i = [str(result_1), str(result_2)] + i[2:]
            new_list_bonds_mcpb_special.append(new_i)

        # this is a new way

        new_strlist_bonds_mcpb_special = []
        for i in range(len(strlist_bonds_mcpb_special)):
        
            newline = "  " + str(int(strlist_bonds_mcpb_special[i][2:6])+self.index_diff) + \
                      "   " + str(int(strlist_bonds_mcpb_special[i][9:13])+self.index_diff) + \
                      strlist_bonds_mcpb_special[i][13:-1] + "     ;<<<<<<<<< update bonds\n"
        
            new_strlist_bonds_mcpb_special.append(newline)

        return (new_list_bonds_mcpb_special, new_strlist_bonds_mcpb_special)

    def special_bonds_hybrid(self, bonds_fields_hybrid):
        
        list_bonds_hybrid_special = []
        index_in_hybrid_special = []
        index_out_hybrid_special =  []

        for i in range(len(bonds_fields_hybrid)):
        
            if i > 1 and (int(bonds_fields_hybrid[i][0]) in self.special_atom_index_h or \
                          int(bonds_fields_hybrid[i][1]) in self.special_atom_index_h):
            
                list_bonds_hybrid_special.append(bonds_fields_hybrid[i])
                index_in_hybrid_special.append(i)
            else:
                index_out_hybrid_special.append(i)

        index_out_hybrid_special.pop(0)
        index_out_hybrid_special.pop(0)
        
        return (list_bonds_hybrid_special, index_in_hybrid_special)

    def compare_bonds(self, new_list_bonds_mcpb_special, new_strlist_bonds_mcpb_special, list_bonds_hybrid_special):
        
        count_match = 0

        for i in range(len(new_list_bonds_mcpb_special)):
        
            atom1_index = int(new_list_bonds_mcpb_special[i][0])
            atom2_index = int(new_list_bonds_mcpb_special[i][1])
        
            for j in range(len(list_bonds_hybrid_special)):
            
                if (atom1_index == int(list_bonds_hybrid_special[j][0])) and \
                   (atom2_index == int(list_bonds_hybrid_special[j][1])):
                    count_match += 1
                    # print(str(atom1_index) + " " + str(atom2_index))
                    break

        new_list = []

        for x in range(len(new_list_bonds_mcpb_special)):
        
            atom1_index = int(new_list_bonds_mcpb_special[x][0])
            atom2_index = int(new_list_bonds_mcpb_special[x][1])
        
            for y in range(len(list_bonds_hybrid_special)):
            
                if (atom1_index == int(list_bonds_hybrid_special[y][0])) and \
                   (atom2_index == int(list_bonds_hybrid_special[y][1])):
                
                    # this is an improvement
                    new_bond_line = new_strlist_bonds_mcpb_special[x]
                
                    # new_bond_line = [atom1_index, atom2_index, int(new_list_bonds_mcpb_special[x][2]), 
                    #                  float(new_list_bonds_mcpb_special[x][3]), 
                    #                  float(new_list_bonds_mcpb_special[x][4])]

                    new_list.append(new_bond_line)            
                    break

        return(count_match, new_list)

    def new_itp_file_bonds(self, bonds_lines_hybrid, bonds_fields_hybrid, new_list, new_strlist_bonds_mcpb_special):
        
        new_bonds_lines_hybrid = []
        new_bonds_lines_hybrid.append(bonds_lines_hybrid[0])
        new_bonds_lines_hybrid.append(bonds_lines_hybrid[1])

        for i in range(2, len(bonds_fields_hybrid), 1):
        
            atom1_index = int(bonds_fields_hybrid[i][0])
            atom2_index = int(bonds_fields_hybrid[i][1])
        
            match = 0
        
            for j in range(len(new_list)):
            
                if (atom1_index == int(new_list[j][2:6])) and \
                   (atom2_index == int(new_list[j][9:13])):
                
                    new_bonds_lines_hybrid.append(new_list[j])
                    match += 1
                    break
          
            if match == 0:
                new_bonds_lines_hybrid.append(bonds_lines_hybrid[i])

        for x in range(len(new_strlist_bonds_mcpb_special)):    
            if new_strlist_bonds_mcpb_special[x] not in new_list:
                new_bonds_lines_hybrid.append(new_strlist_bonds_mcpb_special[x])
                        
        with open(self.path_write_bonds, "w") as f:
            for line in new_bonds_lines_hybrid:
                f.write(line)
            f.write("\n")           
        
        return(new_bonds_lines_hybrid)

# /////////////////////////////////////////////////////////////////////////////////////////////////////////

    def newEDIT4_pairs(self):

        pairs_fields_mcpb, pairs_lines_mcpb = self.search_pairs_mcpb()
        # print(len(pairs_fields_mcpb))
        # print(len(pairs_lines_mcpb))
        # print(pairs_fields_mcpb)
        # print(pairs_lines_mcpb)

        pairs_fields_hybrid, pairs_lines_hybrid = self.search_pairs_hybrid()
        # print(len(pairs_fields_hybrid))
        # print(len(pairs_lines_hybrid))
        # print(pairs_fields_hybrid)
        # print(pairs_lines_hybrid)

        list_pairs_mcpb_special, strlist_pairs_mcpb_special, index_in_mcpb_special = \
        self.special_pairs_mcpb(pairs_fields_mcpb, pairs_lines_mcpb)
        # print(list_pairs_mcpb_special)
        # print(len(list_pairs_mcpb_special))
        # print(index_in_mcpb_special)
        # print(strlist_pairs_mcpb_special)

        new_list_pairs_mcpb_special, new_strlist_pairs_mcpb_special = \
        self.change_index_special_pairs_mcpb(list_pairs_mcpb_special, strlist_pairs_mcpb_special)
        # print(list_pairs_mcpb_special)
        # print(new_list_pairs_mcpb_special)
        # print(len(new_list_pairs_mcpb_special))
        # print(new_strlist_pairs_mcpb_special)

        list_pairs_hybrid_special, index_in_hybrid_special = self.special_pairs_hybrid(pairs_fields_hybrid)
        # print(list_pairs_hybrid_special)
        # print(len(list_pairs_hybrid_special))
        # print(index_in_hybrid_special)

        count_match, new_list = \
        self.compare_pairs(new_list_pairs_mcpb_special, new_strlist_pairs_mcpb_special, list_pairs_hybrid_special)
        # print(count_match)
        # print(new_list)
        # print(len(new_list))

        new_pairs_lines_hybrid = \
        self.new_itp_file_pairs(pairs_lines_hybrid, pairs_fields_hybrid, new_list, new_strlist_pairs_mcpb_special)
        # print(new_pairs_lines_hybrid)                        
        # print(len(new_pairs_lines_hybrid))

    def search_pairs_mcpb(self):
        
        fields_per_line = []
        lines = []
        title_found = False
        
        with open(self.path_read_mcpb, "r") as f:
            for line in f:
                fields = line.strip().split()        
                if title_found == False and len(fields) <= 2:
                    continue
                if len(fields) > 2 and fields[self.position_title] == self.title_pairs:
                    title_found = True
                if title_found == True and len(fields) > 2:
                    fields_per_line.append(fields)
                    lines.append(line)
                if title_found == True and len(fields) <= 2:
                    break
                    
        return (fields_per_line, lines)

    def search_pairs_hybrid(self):
        
        fields_per_line = []
        lines = []
        title_found = False
        
        with open(self.path_read_hybrid, "r") as f:
            for line in f:
                fields = line.strip().split()        
                if title_found == False and len(fields) <= 2:
                    continue
                if len(fields) > 2 and fields[self.position_title] == self.title_pairs:
                    title_found = True
                if title_found == True and len(fields) > 2:
                    fields_per_line.append(fields)
                    lines.append(line)
                if title_found == True and len(fields) <= 2:
                    break
                    
        return (fields_per_line, lines)

    def special_pairs_mcpb(self, pairs_fields_mcpb, pairs_lines_mcpb):
        
        list_pairs_mcpb_special = []
        index_in_mcpb_special = []
        index_out_mcpb_special =  []

        for i in range(len(pairs_fields_mcpb)):
        
            if i > 1 and (int(pairs_fields_mcpb[i][0]) in self.special_atom_index_m or \
                          int(pairs_fields_mcpb[i][1]) in self.special_atom_index_m):
            
                list_pairs_mcpb_special.append(pairs_fields_mcpb[i])
                index_in_mcpb_special.append(i)
            else:
                index_out_mcpb_special.append(i)

        index_out_mcpb_special.pop(0)
        index_out_mcpb_special.pop(0)

        # this is a new way
        strlist_pairs_mcpb_special = [pairs_lines_mcpb[i] for i in index_in_mcpb_special]
        
        return (list_pairs_mcpb_special, strlist_pairs_mcpb_special, index_in_mcpb_special)

    def change_index_special_pairs_mcpb(self, list_pairs_mcpb_special, strlist_pairs_mcpb_special):
        
        new_list_pairs_mcpb_special = []
        for i in list_pairs_mcpb_special:
        
            result_1 = int(i[0]) + self.index_diff
            result_2 = int(i[1]) + self.index_diff
            new_i = [str(result_1), str(result_2)] + i[2:]
            new_list_pairs_mcpb_special.append(new_i)

        # this is a new way

        new_strlist_pairs_mcpb_special = []
        for i in range(len(strlist_pairs_mcpb_special)):
        
            newline = "  " + str(int(strlist_pairs_mcpb_special[i][2:6])+self.index_diff) + \
                      "   " + str(int(strlist_pairs_mcpb_special[i][9:13])+self.index_diff) + \
                      strlist_pairs_mcpb_special[i][13:-1] + "     ;<<<<<<<<< update pairs\n"
        
            new_strlist_pairs_mcpb_special.append(newline)

        return (new_list_pairs_mcpb_special, new_strlist_pairs_mcpb_special)

    def special_pairs_hybrid(self, pairs_fields_hybrid):
        
        list_pairs_hybrid_special = []
        index_in_hybrid_special = []
        index_out_hybrid_special =  []

        for i in range(len(pairs_fields_hybrid)):
        
            if i > 1 and (int(pairs_fields_hybrid[i][0]) in self.special_atom_index_h or \
                          int(pairs_fields_hybrid[i][1]) in self.special_atom_index_h):
            
                list_pairs_hybrid_special.append(pairs_fields_hybrid[i])
                index_in_hybrid_special.append(i)
            else:
                index_out_hybrid_special.append(i)

        index_out_hybrid_special.pop(0)
        index_out_hybrid_special.pop(0)
        
        return (list_pairs_hybrid_special, index_in_hybrid_special)

    def compare_pairs(self, new_list_pairs_mcpb_special, new_strlist_pairs_mcpb_special, list_pairs_hybrid_special):
        
        count_match = 0

        for i in range(len(new_list_pairs_mcpb_special)):
        
            atom1_index = int(new_list_pairs_mcpb_special[i][0])
            atom2_index = int(new_list_pairs_mcpb_special[i][1])
        
            for j in range(len(list_pairs_hybrid_special)):
            
                if (atom1_index == int(list_pairs_hybrid_special[j][0])) and \
                   (atom2_index == int(list_pairs_hybrid_special[j][1])):
                    count_match += 1
                    # print(str(atom1_index) + " " + str(atom2_index))
                    break

        new_list = []

        for x in range(len(new_list_pairs_mcpb_special)):
        
            atom1_index = int(new_list_pairs_mcpb_special[x][0])
            atom2_index = int(new_list_pairs_mcpb_special[x][1])
        
            for y in range(len(list_pairs_hybrid_special)):
            
                if (atom1_index == int(list_pairs_hybrid_special[y][0])) and \
                   (atom2_index == int(list_pairs_hybrid_special[y][1])):
                
                    # this is an improvement
                    new_pair_line = new_strlist_pairs_mcpb_special[x]
                
                    # new_pair_line = [atom1_index, atom2_index, int(new_list_pairs_mcpb_special[x][2]), 
                    #                  float(new_list_pairs_mcpb_special[x][3]), 
                    #                  float(new_list_pairs_mcpb_special[x][4])]

                    new_list.append(new_pair_line)            
                    break

        return(count_match, new_list)

    def new_itp_file_pairs(self, pairs_lines_hybrid, pairs_fields_hybrid, new_list, new_strlist_pairs_mcpb_special):
        
        new_pairs_lines_hybrid = []
        new_pairs_lines_hybrid.append(pairs_lines_hybrid[0])
        new_pairs_lines_hybrid.append(pairs_lines_hybrid[1])

        for i in range(2, len(pairs_fields_hybrid), 1):
        
            atom1_index = int(pairs_fields_hybrid[i][0])
            atom2_index = int(pairs_fields_hybrid[i][1])
        
            match = 0
        
            for j in range(len(new_list)):
            
                if (atom1_index == int(new_list[j][2:6])) and \
                   (atom2_index == int(new_list[j][9:13])):
                
                    new_pairs_lines_hybrid.append(new_list[j])
                    match += 1
                    break
          
            if match == 0:
                new_pairs_lines_hybrid.append(pairs_lines_hybrid[i])

        for x in range(len(new_strlist_pairs_mcpb_special)):    
            if new_strlist_pairs_mcpb_special[x] not in new_list:
                new_pairs_lines_hybrid.append(new_strlist_pairs_mcpb_special[x])
                        
        with open(self.path_write_pairs, "w") as f:
            for line in new_pairs_lines_hybrid:
                f.write(line)
            f.write("\n")           
        
        return(new_pairs_lines_hybrid)

# /////////////////////////////////////////////////////////////////////////////////////////////////////////

    def newEDIT5_angles(self):

        angles_fields_mcpb, angles_lines_mcpb = self.search_angles_mcpb()
        # print(len(angles_fields_mcpb))
        # print(len(angles_lines_mcpb))
        # print(angles_fields_mcpb)
        # print(angles_lines_mcpb)        

        angles_fields_hybrid, angles_lines_hybrid = self.search_angles_hybrid()
        # print(len(angles_fields_hybrid))
        # print(len(angles_lines_hybrid))
        # print(angles_fields_hybrid)
        # print(angles_lines_hybrid)

        list_angles_mcpb_special, strlist_angles_mcpb_special, index_in_mcpb_special = \
        self.special_angles_mcpb(angles_fields_mcpb, angles_lines_mcpb)
        # print(list_angles_mcpb_special)
        # print(len(list_angles_mcpb_special))
        # print(index_in_mcpb_special)
        # print(strlist_angles_mcpb_special)        
    
        new_list_angles_mcpb_special, new_strlist_angles_mcpb_special = \
        self.change_index_special_angles_mcpb(list_angles_mcpb_special, strlist_angles_mcpb_special)
        # print(list_angles_mcpb_special)
        # print(new_list_angles_mcpb_special)
        # print(len(new_list_angles_mcpb_special))
        # print(new_strlist_angles_mcpb_special)

        list_angles_hybrid_special, index_in_hybrid_special = self.special_angles_hybrid(angles_fields_hybrid)
        # print(list_angles_hybrid_special)
        # print(len(list_angles_hybrid_special))
        # print(index_in_hybrid_special)

        count_match, new_list = \
        self.compare_angles(new_list_angles_mcpb_special, new_strlist_angles_mcpb_special, list_angles_hybrid_special)
        # print(count_match)
        # print(new_list)
        # print(len(new_list))

        new_angles_lines_hybrid = \
        self.new_itp_file_angles(angles_lines_hybrid, angles_fields_hybrid, new_list, new_strlist_angles_mcpb_special)
        # print(new_angles_lines_hybrid)                        
        # print(len(new_angles_lines_hybrid))

    def search_angles_mcpb(self):
        
        fields_per_line = []
        lines = []
        title_found = False
        
        with open(self.path_read_mcpb, "r") as f:
            for line in f:
                fields = line.strip().split()        
                if title_found == False and len(fields) <= 2:
                    continue
                if len(fields) > 2 and fields[self.position_title] == self.title_angles:
                    title_found = True
                if title_found == True and len(fields) > 2:
                    fields_per_line.append(fields)
                    lines.append(line)
                if title_found == True and len(fields) <= 2:
                    break
                    
        return (fields_per_line, lines)

    def search_angles_hybrid(self):
        
        fields_per_line = []
        lines = []
        title_found = False
        
        with open(self.path_read_hybrid, "r") as f:
            for line in f:
                fields = line.strip().split()        
                if title_found == False and len(fields) <= 2:
                    continue
                if len(fields) > 2 and fields[self.position_title] == self.title_angles:
                    title_found = True
                if title_found == True and len(fields) > 2:
                    fields_per_line.append(fields)
                    lines.append(line)
                if title_found == True and len(fields) <= 2:
                    break
                    
        return (fields_per_line, lines)

    def special_angles_mcpb(self, angles_fields_mcpb, angles_lines_mcpb):
        
        list_angles_mcpb_special = []
        index_in_mcpb_special = []
        index_out_mcpb_special =  []

        for i in range(len(angles_fields_mcpb)):
        
            if i > 1 and (int(angles_fields_mcpb[i][0]) in self.special_atom_index_m or \
                          int(angles_fields_mcpb[i][1]) in self.special_atom_index_m or \
                          int(angles_fields_mcpb[i][2]) in self.special_atom_index_m):
            
                list_angles_mcpb_special.append(angles_fields_mcpb[i])
                index_in_mcpb_special.append(i)
            else:
                index_out_mcpb_special.append(i)

        index_out_mcpb_special.pop(0)
        index_out_mcpb_special.pop(0)

        # this is a new way
        strlist_angles_mcpb_special = [angles_lines_mcpb[i] for i in index_in_mcpb_special]
        
        return (list_angles_mcpb_special, strlist_angles_mcpb_special, index_in_mcpb_special)

    def change_index_special_angles_mcpb(self, list_angles_mcpb_special, strlist_angles_mcpb_special):
        
        new_list_angles_mcpb_special = []
        for i in list_angles_mcpb_special:
        
            result_1 = int(i[0]) + self.index_diff
            result_2 = int(i[1]) + self.index_diff
            result_3 = int(i[2]) + self.index_diff
            new_i = [str(result_1), str(result_2), str(result_3)] + i[3:]
            new_list_angles_mcpb_special.append(new_i)

        # this is a new way

        new_strlist_angles_mcpb_special = []
        for i in range(len(strlist_angles_mcpb_special)):
        
            newline = "  " + str(int(strlist_angles_mcpb_special[i][2:6])+self.index_diff) + \
                      "   " + str(int(strlist_angles_mcpb_special[i][9:13])+self.index_diff) + \
                      "   " + str(int(strlist_angles_mcpb_special[i][16:20])+self.index_diff) + \
                      strlist_angles_mcpb_special[i][20:-1] + "     ;<<<<<<<<< update angles\n"
        
            new_strlist_angles_mcpb_special.append(newline)

        return (new_list_angles_mcpb_special, new_strlist_angles_mcpb_special)


    def special_angles_hybrid(self, angles_fields_hybrid):
        
        list_angles_hybrid_special = []
        index_in_hybrid_special = []
        index_out_hybrid_special =  []

        for i in range(len(angles_fields_hybrid)):
        
            if i > 1 and (int(angles_fields_hybrid[i][0]) in self.special_atom_index_h or \
                          int(angles_fields_hybrid[i][1]) in self.special_atom_index_h or \
                          int(angles_fields_hybrid[i][2]) in self.special_atom_index_h):
            
                list_angles_hybrid_special.append(angles_fields_hybrid[i])
                index_in_hybrid_special.append(i)
            else:
                index_out_hybrid_special.append(i)

        index_out_hybrid_special.pop(0)
        index_out_hybrid_special.pop(0)
        
        return (list_angles_hybrid_special, index_in_hybrid_special)

    def compare_angles(self, new_list_angles_mcpb_special, new_strlist_angles_mcpb_special, list_angles_hybrid_special):
        
        count_match = 0

        for i in range(len(new_list_angles_mcpb_special)):
        
            atom1_index = int(new_list_angles_mcpb_special[i][0])
            atom2_index = int(new_list_angles_mcpb_special[i][1])
            atom3_index = int(new_list_angles_mcpb_special[i][2])
        
            for j in range(len(list_angles_hybrid_special)):
            
                if (atom1_index == int(list_angles_hybrid_special[j][0])) and \
                   (atom2_index == int(list_angles_hybrid_special[j][1])) and \
                   (atom3_index == int(list_angles_hybrid_special[j][2])):
                    count_match += 1
                    # print(str(atom1_index) + " " + str(atom2_index) + " " + str(atom3_index))
                    break

        new_list = []

        for x in range(len(new_list_angles_mcpb_special)):
        
            atom1_index = int(new_list_angles_mcpb_special[x][0])
            atom2_index = int(new_list_angles_mcpb_special[x][1])
            atom3_index = int(new_list_angles_mcpb_special[x][2])
        
            for y in range(len(list_angles_hybrid_special)):
            
                if (atom1_index == int(list_angles_hybrid_special[y][0])) and \
                   (atom2_index == int(list_angles_hybrid_special[y][1])) and \
                   (atom3_index == int(list_angles_hybrid_special[y][2])):
                
                    # this is an improvement
                    new_angle_line = new_strlist_angles_mcpb_special[x]
                
                    # new_angle_line = [atom1_index, atom2_index, atom3_index, int(new_list_angles_mcpb_special[x][3]), 
                    #                   float(new_list_angles_mcpb_special[x][4]), 
                    #                   float(new_list_angles_mcpb_special[x][5])]

                    new_list.append(new_angle_line)            
                    break

        return(count_match, new_list)

    def new_itp_file_angles(self, angles_lines_hybrid, angles_fields_hybrid, new_list, new_strlist_angles_mcpb_special):
        
        new_angles_lines_hybrid = []
        new_angles_lines_hybrid.append(angles_lines_hybrid[0])
        new_angles_lines_hybrid.append(angles_lines_hybrid[1])

        for i in range(2, len(angles_fields_hybrid), 1):
        
            atom1_index = int(angles_fields_hybrid[i][0])
            atom2_index = int(angles_fields_hybrid[i][1])
            atom3_index = int(angles_fields_hybrid[i][2])
        
            match = 0
        
            for j in range(len(new_list)):
            
                if (atom1_index == int(new_list[j][2:6])) and \
                   (atom2_index == int(new_list[j][9:13]))and \
                   (atom3_index == int(new_list[j][16:20])):
                
                    new_angles_lines_hybrid.append(new_list[j])
                    match += 1
                    break
          
            if match == 0:
                new_angles_lines_hybrid.append(angles_lines_hybrid[i])

        for x in range(len(new_strlist_angles_mcpb_special)):    
            if new_strlist_angles_mcpb_special[x] not in new_list:
                new_angles_lines_hybrid.append(new_strlist_angles_mcpb_special[x])
                        
        with open(self.path_write_angles, "w") as f:
            for line in new_angles_lines_hybrid:
                f.write(line)
            f.write("\n")           
        
        return(new_angles_lines_hybrid)

# /////////////////////////////////////////////////////////////////////////////////////////////////////////

    def newEDIT6_dihedrals(self):

        dihedrals_fields_mcpb, dihedrals_lines_mcpb = self.search_dihedrals_mcpb()
        # print(len(dihedrals_fields_mcpb))
        # print(len(dihedrals_lines_mcpb))
        # print(dihedrals_fields_mcpb)
        # print(dihedrals_lines_mcpb)

        self.rm_improper_title(dihedrals_fields_mcpb, dihedrals_lines_mcpb)
        # print(len(dihedrals_fields_mcpb))
        # print(len(dihedrals_lines_mcpb))
        # print(dihedrals_fields_mcpb)
        # print(dihedrals_lines_mcpb)

        dihedrals_fields_hybrid, dihedrals_lines_hybrid = self.search_dihedrals_hybrid()
        # print(len(dihedrals_fields_hybrid))
        # print(len(dihedrals_lines_hybrid))
        # print(dihedrals_fields_hybrid)
        # print(dihedrals_lines_hybrid)

        list_dihedrals_mcpb_special, strlist_dihedrals_mcpb_special, index_in_mcpb_special = \
        self.special_dihedrals_mcpb(dihedrals_fields_mcpb, dihedrals_lines_mcpb)
        # print(list_dihedrals_mcpb_special)
        # print(len(list_dihedrals_mcpb_special))
        # print(index_in_mcpb_special)
        # print(strlist_dihedrals_mcpb_special)

        new_list_dihedrals_mcpb_special, new_strlist_dihedrals_mcpb_special = \
        self.change_index_special_dihedrals_mcpb(list_dihedrals_mcpb_special, strlist_dihedrals_mcpb_special)
        # print(list_dihedrals_mcpb_special)
        # print(new_list_dihedrals_mcpb_special)
        # print(len(new_list_dihedrals_mcpb_special))
        # print(new_strlist_dihedrals_mcpb_special)

        list_dihedrals_hybrid_special, index_in_hybrid_special = \
        self.special_dihedrals_hybrid(dihedrals_fields_hybrid)
        # print(list_dihedrals_hybrid_special)
        # print(len(list_dihedrals_hybrid_special))
        # print(index_in_hybrid_special)

        count_match, new_list = \
        self.compare_dihedrals(new_list_dihedrals_mcpb_special, new_strlist_dihedrals_mcpb_special, list_dihedrals_hybrid_special)
        # print(count_match)
        # print(new_list)
        # print(len(new_list))

        new_dihedrals_lines_hybrid = \
        self.new_itp_file_dihedrals(dihedrals_lines_hybrid, dihedrals_fields_hybrid, new_list, new_strlist_dihedrals_mcpb_special)
        # print(new_dihedrals_lines_hybrid)                        
        # print(len(new_dihedrals_lines_hybrid))

    # there are 2 types in dihedrals: dihedrals propers and dihedrals impropers
    def search_dihedrals_mcpb(self):
        
        fields_per_line = []
        lines = []
        title1_found = False
        title2_found = False
        
        with open(self.path_read_mcpb, "r") as f:
            # ===> dihedrals propers
            for line in f:
                fields = line.strip().split()        
                if title1_found == False and len(fields) <= 2:
                    continue
                if len(fields) > 2 and fields[self.position_title] == self.title_dihedrals:
                    title1_found = True
                if title1_found == True and len(fields) > 2:
                    fields_per_line.append(fields)
                    lines.append(line)
                if title1_found == True and len(fields) <= 2:
                    break
            # ===> dihedrals impropers
            for line in f:
                fields = line.strip().split()        
                if title2_found == False and len(fields) <= 2:
                    continue
                if len(fields) > 2 and fields[self.position_title] == self.title_dihedrals:
                    title2_found = True
                if title2_found == True and len(fields) > 2:
                    fields_per_line.append(fields)
                    lines.append(line)
                if title2_found == True and len(fields) <= 2:
                    break
                                   
        return (fields_per_line, lines)

    def rm_improper_title(self, dihedrals_fields_mcpb, dihedrals_lines_mcpb):
        
        index_improper_title = 0
        for i, element in enumerate(dihedrals_fields_mcpb):
            if element[4] == "impropers":
                index_improper_title = i
                break
        # print(index_improper_title)
        
        for ctr in range(3):
            dihedrals_fields_mcpb.pop(index_improper_title)
            dihedrals_lines_mcpb.pop(index_improper_title)

    def search_dihedrals_hybrid(self):
        
        fields_per_line = []
        lines = []
        title_found = False
        
        with open(self.path_read_hybrid, "r") as f:
            for line in f:
                fields = line.strip().split()        
                if title_found == False and len(fields) <= 2:
                    continue
                if len(fields) > 2 and fields[self.position_title] == self.title_dihedrals:
                    title_found = True
                if title_found == True and len(fields) > 2:
                    fields_per_line.append(fields)
                    lines.append(line)
                if title_found == True and len(fields) <= 2:
                    break
                    
        return (fields_per_line, lines)

    def special_dihedrals_mcpb(self, dihedrals_fields_mcpb, dihedrals_lines_mcpb):
        
        list_dihedrals_mcpb_special = []
        index_in_mcpb_special = []
        index_out_mcpb_special =  []

        for i in range(len(dihedrals_fields_mcpb)):
        
            if i > 2 and (int(dihedrals_fields_mcpb[i][0]) in self.special_atom_index_m or \
                          int(dihedrals_fields_mcpb[i][1]) in self.special_atom_index_m or \
                          int(dihedrals_fields_mcpb[i][2]) in self.special_atom_index_m or \
                          int(dihedrals_fields_mcpb[i][3]) in self.special_atom_index_m):
                
            # use i > 2 here because there are 3 title lines
            
                list_dihedrals_mcpb_special.append(dihedrals_fields_mcpb[i])
                index_in_mcpb_special.append(i)
            else:
                index_out_mcpb_special.append(i)

        index_out_mcpb_special.pop(0)
        index_out_mcpb_special.pop(0)
        index_out_mcpb_special.pop(0)

        # this is a new way
        strlist_dihedrals_mcpb_special = [dihedrals_lines_mcpb[i] for i in index_in_mcpb_special]
        
        return (list_dihedrals_mcpb_special, strlist_dihedrals_mcpb_special, index_in_mcpb_special)

    def change_index_special_dihedrals_mcpb(self, list_dihedrals_mcpb_special, strlist_dihedrals_mcpb_special):
        
        new_list_dihedrals_mcpb_special = []
        for i in list_dihedrals_mcpb_special:
        
            result_1 = int(i[0]) + self.index_diff
            result_2 = int(i[1]) + self.index_diff
            result_3 = int(i[2]) + self.index_diff
            result_4 = int(i[3]) + self.index_diff
            new_i = [str(result_1), str(result_2), str(result_3), str(result_4)] + i[4:]
            new_list_dihedrals_mcpb_special.append(new_i)

        # this is a new way

        new_strlist_dihedrals_mcpb_special = []
        for i in range(len(strlist_dihedrals_mcpb_special)):
        
            newline = "  " + str(int(strlist_dihedrals_mcpb_special[i][2:6])+self.index_diff) + \
                      "   " + str(int(strlist_dihedrals_mcpb_special[i][9:13])+self.index_diff) + \
                      "   " + str(int(strlist_dihedrals_mcpb_special[i][16:20])+self.index_diff) + \
                      "   " + str(int(strlist_dihedrals_mcpb_special[i][23:27])+self.index_diff) + \
                      strlist_dihedrals_mcpb_special[i][27:-1] + "     ;<<<<<<<<< update dihedrals\n"
        
            new_strlist_dihedrals_mcpb_special.append(newline)

        return (new_list_dihedrals_mcpb_special, new_strlist_dihedrals_mcpb_special)

    def special_dihedrals_hybrid(self, dihedrals_fields_hybrid):
        
        list_dihedrals_hybrid_special = []
        index_in_hybrid_special = []
        index_out_hybrid_special =  []

        for i in range(len(dihedrals_fields_hybrid)):
        
            if i > 1 and (int(dihedrals_fields_hybrid[i][0]) in self.special_atom_index_h or \
                          int(dihedrals_fields_hybrid[i][1]) in self.special_atom_index_h or \
                          int(dihedrals_fields_hybrid[i][2]) in self.special_atom_index_h or \
                          int(dihedrals_fields_hybrid[i][3]) in self.special_atom_index_h):
                
        # use i > 1 here because there are 2 title lines in hybrid file
        
        # this is different from 3 title lines in mcpb file
        
        # Although i > 2 here does not affect the result, I correct it here anyway            
                        
                list_dihedrals_hybrid_special.append(dihedrals_fields_hybrid[i])
                index_in_hybrid_special.append(i)
            else:
                index_out_hybrid_special.append(i)

        index_out_hybrid_special.pop(0)
        index_out_hybrid_special.pop(0)
        
        return (list_dihedrals_hybrid_special, index_in_hybrid_special)

    def compare_dihedrals(self, new_list_dihedrals_mcpb_special, new_strlist_dihedrals_mcpb_special, list_dihedrals_hybrid_special):
        
        count_match = 0

        for i in range(len(new_list_dihedrals_mcpb_special)):
        
            atom1_index = int(new_list_dihedrals_mcpb_special[i][0])
            atom2_index = int(new_list_dihedrals_mcpb_special[i][1])
            atom3_index = int(new_list_dihedrals_mcpb_special[i][2])
            atom4_index = int(new_list_dihedrals_mcpb_special[i][3])
        
            for j in range(len(list_dihedrals_hybrid_special)):
            
                if (atom1_index == int(list_dihedrals_hybrid_special[j][0])) and \
                   (atom2_index == int(list_dihedrals_hybrid_special[j][1])) and \
                   (atom3_index == int(list_dihedrals_hybrid_special[j][2])) and \
                   (atom4_index == int(list_dihedrals_hybrid_special[j][3])):
                    
                    count_match += 1
                    # print(str(atom1_index) + " " + str(atom2_index) + " " + str(atom3_index) + " " + str(atom4_index))
                    break

                # this elif is for improvement
                elif (atom4_index == int(list_dihedrals_hybrid_special[j][0])) and \
                     (atom3_index == int(list_dihedrals_hybrid_special[j][1])) and \
                     (atom2_index == int(list_dihedrals_hybrid_special[j][2])) and \
                     (atom1_index == int(list_dihedrals_hybrid_special[j][3])):
                    
                    count_match += 1
                    # print(str(atom1_index) + " " + str(atom2_index) + " " + str(atom3_index) + " " + str(atom4_index))
                    break

        new_list = []

        for x in range(len(new_list_dihedrals_mcpb_special)):
        
            atom1_index = int(new_list_dihedrals_mcpb_special[x][0])
            atom2_index = int(new_list_dihedrals_mcpb_special[x][1])
            atom3_index = int(new_list_dihedrals_mcpb_special[x][2])
            atom4_index = int(new_list_dihedrals_mcpb_special[x][3])
        
            for y in range(len(list_dihedrals_hybrid_special)):
            
                if (atom1_index == int(list_dihedrals_hybrid_special[y][0])) and \
                   (atom2_index == int(list_dihedrals_hybrid_special[y][1])) and \
                   (atom3_index == int(list_dihedrals_hybrid_special[y][2])) and \
                   (atom4_index == int(list_dihedrals_hybrid_special[y][3])):
                
                    # this is an improvement
                    new_dihedral_line = new_strlist_dihedrals_mcpb_special[x]
                
                    # new_dihedral_line = [atom1_index, atom2_index, atom3_index, atom4_index,
                    #                      int(new_list_dihedrals_mcpb_special[x][4]), 
                    #                      float(new_list_dihedrals_mcpb_special[x][5]), 
                    #                      float(new_list_dihedrals_mcpb_special[x][6]),
                    #                      int(new_list_dihedrals_mcpb_special[x][7])]

                    new_list.append(new_dihedral_line)            
                    break
                
                # this elif is for improvement
                elif (atom4_index == int(list_dihedrals_hybrid_special[y][0])) and \
                     (atom3_index == int(list_dihedrals_hybrid_special[y][1])) and \
                     (atom2_index == int(list_dihedrals_hybrid_special[y][2])) and \
                     (atom1_index == int(list_dihedrals_hybrid_special[y][3])):
                
                    # this is an improvement
                    new_dihedral_line = new_strlist_dihedrals_mcpb_special[x]
                
                    # new_dihedral_line = [atom1_index, atom2_index, atom3_index, atom4_index,
                    #                      int(new_list_dihedrals_mcpb_special[x][4]), 
                    #                      float(new_list_dihedrals_mcpb_special[x][5]), 
                    #                      float(new_list_dihedrals_mcpb_special[x][6]),
                    #                      int(new_list_dihedrals_mcpb_special[x][7])]

                    new_list.append(new_dihedral_line)            
                    break        
            
        return(count_match, new_list)

    def new_itp_file_dihedrals(self, dihedrals_lines_hybrid, dihedrals_fields_hybrid, new_list, new_strlist_dihedrals_mcpb_special):
        
        new_dihedrals_lines_hybrid = []
        new_dihedrals_lines_hybrid.append(dihedrals_lines_hybrid[0])
        new_dihedrals_lines_hybrid.append(dihedrals_lines_hybrid[1])

        for i in range(2, len(dihedrals_fields_hybrid), 1):
        
            atom1_index = int(dihedrals_fields_hybrid[i][0])
            atom2_index = int(dihedrals_fields_hybrid[i][1])
            atom3_index = int(dihedrals_fields_hybrid[i][2])
            atom4_index = int(dihedrals_fields_hybrid[i][3])
        
            match = 0
        
            for j in range(len(new_list)):
            
                if (atom1_index == int(new_list[j][2:6])) and \
                   (atom2_index == int(new_list[j][9:13])) and \
                   (atom3_index == int(new_list[j][16:20])) and \
                   (atom4_index == int(new_list[j][23:27])):
                
                    new_dihedrals_lines_hybrid.append(new_list[j])
                    match += 1

                    # this is important!!!
                    # this is important!!!
                    # this is important!!!
                
                    # break is NOT used here since there are some duplicates, these duplicates are necessary!!!

                elif (atom4_index == int(new_list[j][2:6])) and \
                     (atom3_index == int(new_list[j][9:13])) and \
                     (atom2_index == int(new_list[j][16:20])) and \
                     (atom1_index == int(new_list[j][23:27])):
                
                    new_dihedrals_lines_hybrid.append(new_list[j])
                    match += 1

                    # this is important!!!
                    # this is important!!!
                    # this is important!!!
                
                    # break is NOT used here since there are some duplicates, these duplicates are necessary!!!                

            if match == 0 and (atom1_index not in self.special_atom_index_h and atom2_index not in self.special_atom_index_h and \
                               atom3_index not in self.special_atom_index_h and atom4_index not in self.special_atom_index_h):            
                new_dihedrals_lines_hybrid.append(dihedrals_lines_hybrid[i])
            
            # *** COMMENT OUT not matched special dihedrals but in hybrid top
            elif match == 0 and (atom1_index in self.special_atom_index_h or atom2_index in self.special_atom_index_h or \
                                 atom3_index in self.special_atom_index_h or atom4_index in self.special_atom_index_h):             
                new_dihedrals_lines_hybrid.append("; " + dihedrals_lines_hybrid[i][:-1] + "     ;********* not defined by mcpb\n")
        
        # *** ADD not matched special dihedrals but in mcpb top
        for x in range(len(new_strlist_dihedrals_mcpb_special)):    
            if new_strlist_dihedrals_mcpb_special[x] not in new_list:
                new_dihedrals_lines_hybrid.append(new_strlist_dihedrals_mcpb_special[x])
                        
        with open(self.path_write_dihedrals, "w") as f:
            for line in new_dihedrals_lines_hybrid:
                f.write(line)
            f.write("\n")           
        
        return(new_dihedrals_lines_hybrid)

# /////////////////////////////////////////////////////////////////////////////////////////////////////////

    def concat_files(self):

        os.system("cat new1_atomtypes.itp new2_atoms.itp new3_bonds.itp new4_pairs.itp new5_angles.itp new6_dihedrals.itp > pretop.top")

        with open("top_comb.top", "w") as f1:
            
            f1.write('\n#include "amber14sbmut.ff/forcefield.itp"\n\n')
            
            with open("pretop.top", "r") as f2:
                for line in f2:
                    f1.write(line)
                    
            f1.write('#ifdef POSRES\n#include "posre.itp"\n#endif\n\n\n')
            f1.write('#include "amber14sbmut.ff/tip3p.itp"\n#ifdef POSRES_WATER\n[ position_restraints ]\n' + 
                     '1    1       1000       1000       1000\n#endif\n#include "amber14sbmut.ff/ions.itp"\n\n')
            f1.write('[ system ]\nPMX MODEL\n\n[ molecules ]\nProtein_chain_A 1\n')

# /////////////////////////////////////////////////////////////////////////////////////////////////////////
# /////////////////////////////////////////////////////////////////////////////////////////////////////////

top_comb1 = job_Topol_Combine(sys.argv[1], sys.argv[2])

top_comb1.cal_index_diff()

top_comb1.newEDIT1_atomtypes()

top_comb1.newEDIT2_atoms()
    
top_comb1.newEDIT3_bonds()

top_comb1.newEDIT4_pairs()

top_comb1.newEDIT5_angles()

top_comb1.newEDIT6_dihedrals()

top_comb1.concat_files()





