class studinfo:
    #Method Overloading
    def getdata(self,stid):
        print("ID:",stid)
    
    def getdata(self,stnm):
        print("Name:",stnm)

st=studinfo()
st.getdata("Sanket")
st.getdata(101)