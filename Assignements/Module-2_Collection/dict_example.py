stdata={'id':101,'name':'sanket','sub':'python'}
#print(stdata)
#print(stdata['sub'])
#print(stdata.get('name'))
#print(stdata.keys())
#print(stdata.values())

"""if 'name' in stdata:
    print("Yes..")
else:
    print("Noo..")"""


"""if 'sanket' in stdata.values():
    print("Yes..")
else:
    print("Noo..")"""


"""for i in stdata:
    print(i)"""

"""for i in stdata.values():
    print(i)"""
    
"""for i in stdata.items():
    print(i)"""

"""for i,j in stdata.items():
    print(i,j)"""
    
# ---------------------- #
print(stdata)
#stdata["city"]='rajkot'
#stdata["id"]=102
#stdata.pop('name')
#stdata.clear()
#print(stdata)
#print(len(stdata))

newdata=stdata.copy()
print(newdata)