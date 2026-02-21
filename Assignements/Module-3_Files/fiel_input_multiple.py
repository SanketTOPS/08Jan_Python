fl=open("stdata.txt","a")

n=int(input("Enter number of students:"))

for i in range(n):
    stid=input("Enter an ID:")
    stnm=input("Enter a Name:")
    
    fl.write(f"ID:{stid}\nName:{stnm}\n")