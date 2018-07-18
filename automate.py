
def main():
    
    fileref=open("output1","r")
    lines=fileref.readlines()
    fileref.close()
    
    fileref=open("output","r")
    lines1=fileref.readlines()
    fileref.close()
    
    for line1 in lines1:
        if("intron" in line1):
            continue
        virus=line1
        index=lines1.index('{}'.format(virus))
        index+=1
        print(virus.strip('\n'))
        print(lines1[index].strip('\n'))
        for line in lines:
            if(virus in line):
                index1=lines.index('{}'.format(line))
                index1+=1
                print(lines[index1])


main()
