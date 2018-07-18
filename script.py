import os

line_number=0

def makeCopy(query,database):
    print("\nCreating copy of query and database...\n")
    os.system("cp {} copy_{}".format(query, query)) 
    os.system("cp {} copy_{}".format(database,database))


def runningSelectedVirus(query,database):
    global line_number
    makeCopy(query,database)
    
    fileref=open("copy_{}".format(query),"r+")
    for row in fileref:
        if(">" in row):
            virus=row
            line_number+=1
            break
    fileref.close()    
    
    fileref=open("copy_{}".format(database),"r+")
    for row in fileref:
        if(virus=="row"):
            print("Virus Found\n")
            print(row)
    fileref.close()

     
def main():
    print("\nRun blast normally?\n ")
    a=input()
    a="no"
    #
    print("\nThe list of files in your directory is: \n")
    os.system("ls")
    print("\nEnter your query file:\n ")
    query=input()
    #query="genomes.fas"
    print("\nEnter your database: \n")
    database=input()
    #database="CP_nuc.fas"
    print("\nCreating nucleotide database for query...\n")
    os.system("makeblastdb -in {} -parse_seqids -dbtype nucl".format(database))
    
    if(a=='YES' or a=='Yes' or a=='yes'):
        print("\nRunning Blast for query with nucleotide database...\n")
        os.system("blastn -query {} -db {} -out output 2> garbage".format(query,database))
        print("\nRemoving unnecessary files...\n")
        os.system("rm *.nin *.nsd *.nsi *.nog *.nsq *.nhr garbage")
        print("\n Your output file is created with title output...\n")

    else:
        print("\nWorking on specific viruses...\n")
        runningSelectedVirus(query,database)
main()
