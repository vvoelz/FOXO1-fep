import sys

def main(path_read):

    path_write = path_read[:-13] + "K_" + path_read[-13:]
    lines = []
    line_index = -1
    index_Insert = 0
    num_102 = 0
    line_index_K_gro = 0
    num_K = 0
    with open(path_read, "r") as f1:
        for line in f1:
            lines.append(line)
            line_index += 1
            fields = line.strip().split()
            if len(fields) == 1:
                continue
            if fields[0][0:3] == "102" and num_102 == 0:
                index_Insert = line_index
                num_102 += 1
            if fields[0][-1] == "K" and num_K == 0:
                line_index_K_gro = line_index
                num_K += 1

#     print(len(lines))
#     print(index_Insert)
#     print(line_index_K_gro)
#     print(lines)

    line_K_gro = lines[line_index_K_gro]
    # remove by value
    lines.remove(line_K_gro)
    lines.insert(index_Insert, line_K_gro)
#     print(lines)

    with open(path_write, "w") as f2:
        for line in lines:
            f2.write(line)


if __name__ == "__main__":

    filename = sys.argv[1]
    main(filename)

