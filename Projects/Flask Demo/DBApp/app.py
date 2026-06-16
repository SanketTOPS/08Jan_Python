from flask import Flask,render_template,request
from flask_sqlalchemy import SQLAlchemy

app=Flask(__name__)

#DB Config.
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///tops.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False  # Saves memory/resources

db=SQLAlchemy(app)

#DB Model
class Studinfo(db.Model):
    id=db.Column(db.Integer,primary_key=True)
    name=db.Column(db.String(20))
    city=db.Column(db.String(20))

with app.app_context():
    db.create_all()

@app.route('/',methods=['GET','POST'])
def index():
    if request.method=="POST":
        name=request.form.get("name")
        city=request.form.get("city")
        stdata=Studinfo(name=name,city=city)
        db.session.add(stdata)
        db.session.commit()
    return render_template('index.html')


@app.route('/showdata',methods=['GET'])
def showdata():
    stdata=Studinfo.query.all()
    return render_template('showdata.html',stdata=stdata)

app.run(debug=True)