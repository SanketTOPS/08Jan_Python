"""class master:
    def header(hid):
        print("This is Header")
    def footer(fid):
        print("This is Footer")

class home(master):
    def header(hid):
        return super().header()
  """
  
class student:
    def getdata(id):
        print("ID:",id)
    
    def getdata(name):
        print("Name:",name)
    
st=student()
st.getdata()