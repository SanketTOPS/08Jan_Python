def getdata(id,name):
    return id,name

def userdata():
    x=getdata(101,'Sanket')
    print("ID:",x[0])
    print("Name:",x[1])

userdata()