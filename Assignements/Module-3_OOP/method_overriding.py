class base:
    def header(self):
        print("This is Header")
        
    def footer(self):
        print("This is footer")

class home(base):
    def header(self):
        return super().header()

    def footer(self):
        return super().footer()

class about(base):
    def header(self):
        return super().header()

    def footer(self):
        return super().footer()