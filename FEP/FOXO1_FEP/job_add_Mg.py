import sys
import copy

def main(path_read_Mg, path_read_FOXO1):

    line_Mg = ""    
    with open(path_read_Mg, "r") as f1:
        for line in f1:
            fields = line.strip().split()
            if len(fields) >= 2 and fields[1] == "MG":
            	line_Mg = line

    line_FOXO1 = []
    with open(path_read_FOXO1, "r") as f2:
        for line in f2:
        	line_FOXO1.append(line)

    line_FOXO1_new = copy.copy(line_FOXO1)
    line_FOXO1_new[1] = " " + str(int(line_FOXO1[1].strip())+1) + "\n"
    line_FOXO1_new[-1] = "  101MG1     MG " + str(int(line_FOXO1[-2].strip().split()[2])+1) + str(line_Mg[20:])
    line_FOXO1_new.append(line_FOXO1[-1])

    path_write = path_read_FOXO1[:-4] + "_Mg.gro"
    with open(path_write, "w") as f3:
        for line in line_FOXO1_new:
            f3.write(line)

if __name__ == "__main__":

    filename1 = sys.argv[1]
    filename2 = sys.argv[2]
    main(filename1, filename2)









