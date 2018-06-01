import os

def creatingQueryFromDatabase(database):
    fileref=open("{}".format(database),"r+")
    for row in fileref:
        if(">" in row):
            virus_name=row
            continue
            
        virus=row
        break
    fileref.close()

    query_file="virus_query.fas"

    fileref=open("{}".format(query_file),"r+")
    fileref.write(virus_name)
    fileref.write(virus)
    fileref.close()
    
    return (virus_name,virus)

def removingVirusFromDatabase(virus_name,virus,database):
    print(virus_name)
    
    fileref=open("copy_{}".format(database),"r")
    lines=fileref.readlines()
    fileref.close()

    fileref=open("copy_{}".format(database),"w")
    for line in lines:
        if(line in virus_name or line in virus):
            continue
        fileref.write(line)
    fileref.close()

            
def creatingQueryAndBlasting(database):
    (virus_name,virus)=creatingQueryFromDatabase(database)
    os.system("cp {} copy_{}".format(database, database))
    removingVirusFromDatabase(virus_name,virus,database)

def main():
    print("\nThe list of files in your directory is\n")
    os.system("ls")
    print("\nEnter the database..\n")
    #database=input()
    database="CP_nuc.fas"
    
    creatingQueryAndBlasting(database)

main()
