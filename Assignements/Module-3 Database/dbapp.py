import sqlite3

try:
    db=sqlite3.connect("topsdb.db")
    print("Database created/connected!")
except Exception as e:
    print(e)
    
#Table Create
tbl_create="create table studinfo(id integer primary key autoincrement, name text, city text)"

try:
    db.execute(tbl_create)
    print("Table created!")
except Exception as e:
    print(e)    


#Insert Data
insert_data="insert into studinfo(name,city)values('sanket','rajkot'),('ashok','surat'),('hitesh','baroda'),('nirav','jamnagar')"

try:
    db.execute(insert_data)
    db.commit()
    print("Record inserted!")
except Exception as e:
    print(e)

