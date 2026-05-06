import tkinter
from tkinter import ttk,messagebox

x=tkinter.Tk()
x.title("MyApp")
x.geometry("400x500")
x.config(background="orange")

#tkinter.Label(text="Firstname").pack()
l1=tkinter.Label(text="Firstname",bg="orange",fg="blue",font="Corbel 15 bold")
#l1.pack()
#l1.place(x=0,y=0)
l1.grid(row=0,column=0,sticky='w')

l2=tkinter.Label(text="Lastname",bg="orange",fg="blue",font="Corbel 15 bold")
#l2.pack()
#l2.place(x=0,y=30)
l2.grid(row=1,column=0,sticky='w')

t1=tkinter.Entry()
t1.grid(row=0,column=1,sticky='w')

t2=tkinter.Entry()
t2.grid(row=1,column=1)

m=tkinter.Radiobutton(value=0,text="Male",bg="orange",fg="blue",font="Corbel 15 bold")
f=tkinter.Radiobutton(value=1,text="Female",bg="orange",fg="blue",font="Corbel 15 bold")
m.grid(row=2,column=0,sticky='w')
f.grid(row=2,column=1,sticky='w')

ch1=tkinter.Checkbutton(text="Gujarati",bg="orange",fg="blue",font="Corbel 15 bold")
ch2=tkinter.Checkbutton(text="Hindi",bg="orange",fg="blue",font="Corbel 15 bold")
ch3=tkinter.Checkbutton(text="English",bg="orange",fg="blue",font="Corbel 15 bold")
ch1.grid(row=3,column=0,sticky='w')
ch2.grid(row=4,column=0,sticky='w')
ch3.grid(row=5,column=0,sticky='w')

city=['Rajkot','Baroda','Ahmedabad','Surat','Gandhinagar']
cm=ttk.Combobox(values=city)
cm.grid(row=6,column=0)

def btnClick():
    #print("Button Clicked!")
    print("Firstname:",t1.get())
    print("Lastname:",t2.get())
    
    #messagebox.showerror("Error","Something went wrong...")
    #messagebox.showinfo("Success","Your form has been submitted!")
    #messagebox.showwarning("Warning","Your disk is full!")
    
    messagebox.showinfo("Hello",f"Welcome, {t1.get()}")

btn=tkinter.Button(text="Submit",fg="blue",font="Corbel 15 bold",command=btnClick)
#btn.grid(row=10,column=0)
btn.place(x=160,y=240)
x.mainloop()