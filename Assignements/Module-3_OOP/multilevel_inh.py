class sanket:
    sid:int
    stech=str
    
    def s_getdata(self):
        self.sid=input("Enter Sanket's ID:")
        self.stech=input("Enter Sanket's Tech:")

class gopal(sanket):
    gid:int
    gtech=str
    
    def g_getdata(self):
        self.gid=input("Enter Gopal's ID:")
        self.gtech=input("Enter Gopal's Tech:")

class ashok(gopal):
    aid:int
    atech=str
    
    def a_getdata(self):
        self.aid=input("Enter Ashok's ID:")
        self.atech=input("Enter Ashok's Tech:")


class tops(ashok):
    def printdata(self):
        print("Sanket's ID:",self.sid)
        print("Sanket's Tech:",self.stech)
        print("-------------------")
        print("Gopal's ID:",self.gid)
        print("Gopal's Tech:",self.gtech)
        print("-------------------")
        print("Ashok's ID:",self.aid)
        print("Ashok's Tech:",self.atech)
        
tp=tops()
tp.s_getdata()
tp.g_getdata()
tp.a_getdata()
tp.printdata()
