# This script removes the "_Genomovirus from the input file"

import sys

def main(arg):

    fileref=open("{}".format(arg[1]),"r")
    lines=fileref.readlines()
    fileref.close()

    fileref=open("{}".format(arg[1]),"w")
    for line in lines:
        if("_Genomovirus" in line):
            line=line.replace("_Genomovirus","")
            fileref.write(line)
            continue
        fileref.write(line)
    fileref.close()

main(sys.argv)
