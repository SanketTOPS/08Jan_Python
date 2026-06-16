from flask import Flask

app=Flask(__name__) #app init

@app.route('/')
def index():
    return "Hello Flask!"

@app.route('/about')
def about():
    return "This Is About Page!"


app.run(debug=True)