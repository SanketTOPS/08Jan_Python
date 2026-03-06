class studinfo:
    #private
    __stid=12
    __stnm="Sanket"
    
    def __getdata(self): #private
        print("This is getdata!")
        print("ID:",self.__stid)
        print("Name:",self.__stnm)
    
    def printdata(self):
        self.__getdata()

st=studinfo()
#print("ID:",st.stid)
#print("Name:",st.stnm)
#st.getdata()
st.printdata()

    