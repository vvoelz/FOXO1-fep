import sys

def main(path_read):

    path_write = path_read[:-4] + "_K" + path_read[-4:]
    lines = []
    line_index = -1
    index_Insert = 0
    line_index_K_name = 0

    with open(path_read, "r") as f1:
        for line in f1:
            lines.append(line)
            line_index += 1
            fields = line.strip().split()
            if len(fields) < 2:
                continue
            if fields[1] == "bonds":
                index_Insert = line_index - 1
                # insert line is above [ bonds ] title line
            if fields[0] == "K":
                line_index_K_name = line_index
                # K name line is in [ molecules ] section

    # insert K parameters
#    print(index_Insert)
#    print(lines[index_Insert-1])
    index_K_top = int(lines[index_Insert-1].strip().split()[0]) + 1
    line_K_top = "    " + str(index_K_top) + "           K    102      K      K     " + str(index_K_top) + \
                 "   1.000000    39.1000           K   0.000000    39.1000\n"
    comment_top = ";   nr        type  resnr  resid   atom   cgnr     charge       mass       " + \
                  "typeB    chargeB      massB\n"

    lines.insert(index_Insert, line_K_top)
    lines.insert(index_Insert+1, comment_top)
#    print(lines)

    # change K number
#    print(line_index_K_name)
    line_K_name = lines[line_index_K_name+2]
    # +2 because line_K_top and comment_top above new two lines increase the index by 2
    lines.remove(line_K_name)
    num_K = int(line_K_name.strip().split()[1])
    if num_K > 1:
        new_line_K_name = line_K_name[:-5] + str(num_K-1) + "\n"
        lines.insert(line_index_K_name+2, new_line_K_name)
        # line_K_name[-1] => '\n' => ONLY one character
        # line_K_name[-2] => '2'    
#    print(lines)

    with open(path_write, "w") as f2:
        for line in lines:
            f2.write(line)


if __name__ == "__main__":

    filename = sys.argv[1]
    main(filename)

