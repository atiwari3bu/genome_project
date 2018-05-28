import os

def main():
    print("\nThe list of files in your directory is: \n")
    os.system("ls")
    print("\nEnter your query file:\n ")
    query=input()
    print("\nEnter your database: \n")
    database=input()
    print("\nCreating nucleotide database for query...\n")
    os.system("makeblastdb -in {} -parse_seqids -dbtype nucl".format(database))
    print("\nRunning Blast for query with nucleotide database...\n")
    os.system("blastn -query {} -db {} -out output 2> garbage".format(query,database))
    print("\nRemoving unnecessary files...\n")
    os.system("rm *.nin *.nsd *.nsi *.nog *.nsq *.nhr garbage")
    print("\n Your output file is created with title output...\n")

main()
