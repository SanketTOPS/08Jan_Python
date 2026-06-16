from flask import Flask,render_template,request,redirect
from flask_sqlalchemy import SQLAlchemy


app=Flask(__name__)

#DB Config
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///tops.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db=SQLAlchemy(app)

#Model
class Studinfo(db.Model):
    id=db.Column(db.Integer,primary_key=True)
    name=db.Column(db.String(20))
    email=db.Column(db.String(20))
    city=db.Column(db.String(20))

with app.app_context():
    db.create_all()


@app.route('/', methods=['GET','POST'])
def index():
    if request.method=='POST':
        nm=request.form['name']
        em=request.form['email']
        ct=request.form['city']

        stdata=Studinfo(name=nm,email=em,city=ct)
        db.session.add(stdata)
        db.session.commit()
    return render_template('index.html')


@app.route('/showdata')
def showdata():
    stdata=Studinfo.query.all()
    return render_template('showdata.html',stdata=stdata)

@app.route('/deletedata/<int:id>')
def deletedata(id):
    stid=Studinfo.query.get(id)
    db.session.delete(stid)
    db.session.commit()
    return redirect('/showdata')

@app.route('/updatedata/<int:id>',methods=['GET','POST'])
def udpatedata(id):
    stid=Studinfo.query.get(id)
    if request.method=='POST':
        stid.name=request.form['name']
        stid.email=request.form['email']
        stid.city=request.form['city']
        db.session.commit()
        print("Record Updated!")
        return redirect('/showdata')
    return render_template('updatedata.html',stid=stid)

app.run(debug=True)