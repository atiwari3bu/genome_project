import re
import os


def main():
    
#    print("Please enter the name of file")
#    file_name=input()
    for files in os.listdir(os.getcwd()):
        file_name=files
        print("\n",file_name)
        hit=[]
        for i in range(2500):
            hit.append(0)
        fileref=open("{}".format(file_name),"r")
        lines=fileref.readlines()
        fileref.close()
        line_number=0

        for line in lines:
            if("Query" in line):
                line_number+=1
                if(line_number==1):
                    continue
                my_list=(re.findall('\d+',line))
               # print("{} - {}".format(my_list[0],my_list[1]))
                for i in range(int(my_list[0]),int(my_list[1])+1):
                    hit[i]=1
        flag=0
        straight_to=0
        for i in range(2500):
            if(flag==0 and hit[i]==0):
                if(straight_to==0):
                    #print(" ")
                    flag=1
                    straight_to=1
                    continue
               # print(i-1)
                flag=1
            if(hit[i]==1 and flag==1):
                #print("hit :",end=" ")
                #print(i,end='-',flush=True)
                flag=0
       
        intron_end=0  
        straight_to=0
        for i in range(2500):
            if(flag==0 and hit[i]==0):
               # print("intron :",end=" ")
               # print(i,end='-',flush=True)
                intron_start=i
                flag=1
            if(hit[i]==1 and flag==1):
                if(straight_to==0):
                    flag=0
                    straight_to=1
                    continue
               # print(i-1,flush=True)
                intron_end=i-1
                flag=0
        if(intron_end!=0):
            print(" Intron: {} - {} ".format(intron_start,intron_end))
        else:
            print(" No Intron found") 

main()

