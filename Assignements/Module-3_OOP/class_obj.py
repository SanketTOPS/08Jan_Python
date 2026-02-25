class student:
    stid=101
    stnm="Sanket"
    
    def getsum(self,a,b):
        print("Sum:",a+b)


st=student()
print("ID:",st.stid)
print("Name:",st.stnm)

st.getsum(12,56)