import os

virus_list=[]
times=0
flag=0

def creatingQueryFromDatabase(database):
    global flag
    fileref=open("{}".format(database),"r+")
    for row in fileref:
        if(row in virus_list):
            flag=1
            continue
        if(flag==1):
            flag=0
            continue
        if(">" in row):
            virus_name=row
            continue
            
        virus=row
        break
    fileref.close()

    #query_file="virus_query.fas"

    fileref=open("virus_query.fas","r+")
    fileref.write(virus_name)
    fileref.write(virus)
    fileref.close()
    
    return (virus_name,virus)

def removingVirusFromDatabase(virus_name,virus,database):
    fileref=open("copy_{}".format(database),"r")
    lines=fileref.readlines()
    fileref.close()

    fileref=open("copy_{}".format(database),"w")
    for line in lines:
        if(line in virus_name or line in virus):
            continue
        fileref.write(line)
    fileref.close()

def runningBlast(database,virus_name):
    virus_list.append(virus_name)
    virus_name=virus_name.strip('\n')
    virus_name=virus_name.strip('>')
    os.system("makeblastdb -in copy_{} -parse_seqids -dbtype nucl".format(database))
    os.system("blastn -query virus_query.fas -db copy_{} -out {} 2> garbage".format(database,virus_name))
    os.system("rm *.nin *.nsd *.nsi *.nog *.nsq *.nhr garbage copy_{}".format(database))
            
def creatingQueryAndBlasting(database):
    global times
    times+=1
    if(times==160): 
        return 
    (virus_name,virus)=creatingQueryFromDatabase(database)
    os.system("cp {} copy_{}".format(database, database))
    removingVirusFromDatabase(virus_name,virus,database)
    runningBlast(database,virus_name)
    creatingQueryAndBlasting(database)

def main():
    print("\nThe list of files in your directory is\n")
    os.system("ls")
    print("\nEnter the database..\n")
    #database=input()
    database="CP_nuc.fas"
    
    creatingQueryAndBlasting(database)
    print(virus_list)

main()
