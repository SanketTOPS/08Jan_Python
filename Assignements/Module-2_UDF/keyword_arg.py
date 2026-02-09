def getdata(id,name,city):
    print("ID:",id)
    print("Name:",name)
    print("City:",city)

#getdata(101,'Sanket','Rajkot') #positional arg.
#getdata('Sanket',101,'Rajkot') #positional arg.

#getdata(id=101,name='Ashok',city='Surat') #keyword arg.

getdata(city='Surat',id=101,name='Ashok') #keyword arg.