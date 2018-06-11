import os

virus_list=[]
times=0
flag1=0
flag2=0

def creatingQueryFromDatabase(database,query):
    global flag1
    global flag2
        
    fileref=open("{}".format(database),"r+")
    for row in fileref:
        if(row in virus_list):
            flag1=1
            continue
        if(flag1==1):
            flag1=0
            continue
        if(">" in row):
            virus_name=row
            continue
        
        virus=row
        break
    fileref.close()

    print(virus_name)

    os.system("cp {} copy_{}".format(query,query)) 
    fileref=open("copy_{}".format(query),"r")
    lines=fileref.readlines()
    fileref.close()
    
    fileref=open("copy_{}".format(query),"w")
    for line in lines:
        if(line in virus_name):
            fileref.write(line)
            flag2=1
            continue
        if(flag2==1):
            fileref.write(line)
            flag2=0
            continue
        else:
            continue
    fileref.close()
    
    os.system("cp copy_{} virus_query.fas".format(query))
    #fileref=open("virus_query.fas","r+")
    #fileref.write(virus_name)
    #fileref.write(virus)
    #fileref.close()
    
    return (virus_name,virus)

def removingVirusFromDatabase(virus_name,virus,database):
    fileref=open("copy_{}".format(database),"r")
    lines=fileref.readlines()
    fileref.close()

    fileref=open("copy_{}".format(database),"w")
   # for line in lines:
   #     if(line in virus_name or line in virus):
   #         continue
   #     fileref.write(line)
   # fileref.close()

    for line in lines:
        if(line in virus_name or line in virus):
            fileref.write(line)
        continue
    fileref.close()


def runningBlast(database,virus_name):
    virus_list.append(virus_name)
    virus_name=virus_name.strip('\n')
    virus_name=virus_name.strip('>')
    os.system("makeblastdb -in copy_{} -parse_seqids -dbtype nucl".format(database))
    os.system("blastn -query virus_query.fas -db copy_{} -out virus_output/{} 2> garbage".format(database,virus_name))
            
def creatingQueryAndBlasting(database,query):
    global times
    times+=1
    if(times==160): 
        return 
    #if(times==10):
    #     return
    (virus_name,virus)=creatingQueryFromDatabase(database,query)
    os.system("cp {} copy_{}".format(database, database))
    removingVirusFromDatabase(virus_name,virus,database)
    runningBlast(database,virus_name)
    creatingQueryAndBlasting(database,query)

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
            f.seek(0)
            first_char=f.read(1)
            if not first_char:
                continue
            else:
                f.seek(0)
            total_virus.append(files) 
            for row in f:
                if("***** No hits found *****" in row ):
                    virus_with_no_hits.append(files)
            line_number=0

        f.close()
    
    virus_with_hits=[x for x in total_virus if x not in virus_with_no_hits] 
    print("\nTotal virus in directory\n")
    print(total_virus)
    print("\nvirus with no hits\n")
    print(virus_with_no_hits)
    print("\nvirus with hits\n")
    print(virus_with_hits)
    print("\n\n")
   
    separatingVirusWithHits(directory,virus_with_hits)
    separatingVIrusWithNoHits(directory,virus_with_no_hits)


def main():
    print("\nThe list of files in your directory is\n")
    os.system("ls")
    print("\nEnter the database..\n")
  #  database=input()
    print("\nEnter the query file...\n")
#    query=input()
    database="spliced_reps.fas"
    query="genomes.fas"
    if("spliced" in database):
        os.system("python3 script2.py {}".format(database))
    os.system("mkdir virus_output"); 
    creatingQueryAndBlasting(database,query)
    os.system("rm *.nin *.nsd *.nsi *.nog *.nsq *.nhr garbage copy_{} copy_{} virus_query.fas".format(database,query))
    # Part Three

    print("\nFinding out the intron in the above viruses:\n")
    directory=os.getcwd()
    directory+='/virus_output'
    findingIntron(directory)

main()
