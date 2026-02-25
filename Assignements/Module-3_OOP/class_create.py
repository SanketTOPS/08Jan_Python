class studinfo:
    stid=12
    stnm="Sanket"
    
    def myfunc(self):
        print("This is studinfo class")
    

st=studinfo() #object
print("ID:",st.stid)
print("Name:",st.stnm)
st.myfunc()
    