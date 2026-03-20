import tkinter
import pymysql

try:
    db=pymysql.connect(host="localhost",user="root",password="",database="testdb")
    print("Database connected!")
except Exception as e:
    print(e)

cr=db.cursor()

tbl_create="create table stdata(id integer primary key auto_increment,firstname varchar(20),lastname varchar(20),city varchar(20))"
try:
    cr.execute(tbl_create)
    print("Table created!")
except Exception as e:
    print(e)
    

tk=tkinter.Tk()
tk.title("DBApp")
tk.config(bg="lightblue")
tk.geometry("400x300")

lbl_fnm=tkinter.Label(text="Firstname:",bg="lightblue",fg="red",font="Cooper 12 bold")
lbl_fnm.grid(row=0,column=0,sticky='w')

lbl_lnm=tkinter.Label(text="Lastname:",bg="lightblue",fg="red",font="Cooper 12 bold")
lbl_lnm.grid(row=1,column=0,sticky='w')

lbl_ct=tkinter.Label(text="City:",bg="lightblue",fg="red",font="Cooper 12 bold")
lbl_ct.grid(row=2,column=0,sticky='w')


txt_fnm=tkinter.Entry()
txt_fnm.grid(row=0,column=1)

txt_lnm=tkinter.Entry()
txt_lnm.grid(row=1,column=1)

txt_ct=tkinter.Entry()
txt_ct.grid(row=2,column=1)

def save_data():
    fnm=txt_fnm.get()
    lnm=txt_lnm.get()
    ct=txt_ct.get()
    
    insert_data=f"insert into stdata(firstname,lastname,city)values('{fnm}','{lnm}','{ct}')"
    try:
        cr.execute(insert_data)
        db.commit()
        print("Record inserted!")
    except Exception as e:
        print(e)

btn_submit=tkinter.Button(text="Save",fg="black",font="Cooper 12 bold",command=save_data)
btn_submit.place(x=180,y=120)
tk.mainloop()