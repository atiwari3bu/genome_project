import os
from time import sleep

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
    os.system("blastn -query virus_query.fas -db copy_{} -out virus_output/{} 2> garbage".format(database,virus_name))
            
def creatingQueryAndBlasting(database):
    global times
    times+=1
    if(times==160): 
        return 
    #if(times==5):
    #    return
    (virus_name,virus)=creatingQueryFromDatabase(database)
    os.system("cp {} copy_{}".format(database, database))
    removingVirusFromDatabase(virus_name,virus,database)
    runningBlast(database,virus_name)
    sleep(0.15)
    creatingQueryAndBlasting(database)

def separatingVirusWithHits(directory,virus_with_hits):
    os.system("mkdir {}/virus_with_hits".format(directory))
    directory1=directory+"/virus_with_hits"
    for files in os.listdir(directory):
        if files in virus_with_hits:
            os.system("mv {}/{} {}".format(directory,files,directory1))

def separatingVIrusWithNoHits(directory,virus_with_no_hits):
    os.system("mkdir {}/virus_with_no_hits".format(directory))
    directory1=directory+"/virus_with_no_hits"
    for files in os.listdir(directory):
        if files in virus_with_no_hits:
            os.system("mv {}/{} {}".format(directory,files,directory1))

def findingIntron(directory):
    virus_with_no_hits=[]
    total_virus=[]
    virus_with_hits=[]
   
    for files in os.listdir(directory):
        if(files=="virus_with_hits" or files=="virus_with_no_hits"):
            continue
        text_file=os.path.join(directory,files)
        with open(text_file,errors="ignore") as f:
            total_virus.append(files)
            for row in f:
                if("***** No hits found *****" in row):
                    virus_with_no_hits.append(files)

        f.close()
    
    virus_with_hits=[x for x in total_virus if x not in virus_with_no_hits] 
    print("\nTotal virus in directory\n")
    print(total_virus)
    print("\nvirus with no hits\n")
    print(virus_with_no_hits)
    print("\nvirus with hits\n")
    print(virus_with_hits)
    print(\n\n)
   
    separatingVirusWithHits(directory,virus_with_hits)
    separatingVIrusWithNoHits(directory,virus_with_no_hits)


def main():
    print("\nThe list of files in your directory is\n")
    os.system("ls")
    print("\nEnter the database..\n")
    #database=input()
    database="CP_nuc.fas"
    os.system("mkdir virus_output"); 
    creatingQueryAndBlasting(database)
    os.system("rm *.nin *.nsd *.nsi *.nog *.nsq *.nhr garbage copy_{}".format(database))
    
    # Part Three

    print("\nFinding out the intron in the above viruses:\n")
    directory=os.getcwd()
    directory+='/virus_output'
    findingIntron(directory)
    
main()
