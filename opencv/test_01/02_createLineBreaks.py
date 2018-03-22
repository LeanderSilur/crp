def isfloat(value):
  try:
    float(value)
    return True
  except ValueError:
    return False
def hasfloat(value):
    value.replace(" ", "")
    return isfloat(value)


def create_line_breaks(file_read, file_write):
    outF = open(file_write, "w")

    filename = file_read
    previous_had_float = False

    indent = ""
    tabstop = "    "

    action_chars = ["{", "[", "]", "}", ","]
    large_number = 1000000

    with open(filename, 'r') as handle:
        for line in handle:
            while (len(line) > 0):
                print(str(len(line)))
                distances = [line.find(x) if(line.find(x) > -1) else large_number for x in action_chars]
                next_distance = -1
                if (len(distances) > 0):
                    next_distance = min(distances)
                next_item = action_chars[distances.index(next_distance)]

                if (next_distance > -1):
                    outF.write(line[:next_distance])
                    line = line[next_distance+1:]
                    if (next_item in {"{", "["}):
                        indent += tabstop
                        outF.write(next_item + "\n" + indent)
                    if (next_item in {"]", "}"}):
                        indent = indent[:-4]
                        outF.write("\n" + indent + next_item)# + "\n" + indent)
                    if (next_item == ","):
                        outF.write(next_item)
                        next_comma = min([line.find(x) for x in action_chars])
                        if (next_comma >= 0):
                            if (hasfloat(line[:next_comma])):
                                next_comma = -2
                        if (next_comma > -2):
                            outF.write("\n" + indent)
                else:
                    outF.write(line)
                    line = ""
    outF.close()


create_line_breaks("data_matplotlib.txt", "data.txt")