fl=open("temp.txt","w")

stid=input("Enter an ID:")
stnm=input("Enter a Name:")

"""fl.write(stid)
fl.write(stnm)"""

fl.write(f"ID:{stid}\nName:{stnm}")