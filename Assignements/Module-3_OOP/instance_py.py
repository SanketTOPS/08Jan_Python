class student:
    stid=12
    stnm="Sanket"
    
    def getdata(self):
        print("ID:",self.stid)
        print("Name:",self.stnm)

"""st=student() #object
st.getdata()
st.stid=101
st.stnm="Ashok"
st.getdata()
"""

student().getdata() #instance
student().stid=14
student().stnm="Ashok"
student().getdata()