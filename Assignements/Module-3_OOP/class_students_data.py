class studinfo:
    def __init__(self,id,name,city):
        self.id=id
        self.name=name
        self.city=city
        
stdata=[]
        
for i in range(2):
    id=input("Enter an ID:")
    nm=input("Enter a Name:")
    ct=input("Enter a City")
            
    st=studinfo(id,nm,ct)
    stdata.append(st)
        
for i in stdata:
    print(i.id)
    print(i.name)
    print(i.city)