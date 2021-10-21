from flask import Flask, render_template
import os

app = Flask(__name__)

@app.route('/')
def hello_world():
    return render_template("index.html")

@app.route('/login')
def login():
    return render_template("login.html")

@app.route('/inicioSesion', methods=['GET','POST'])
def inicioSesion():
    return render_template("login.html")
    



if  __name__ == "__main__":
    os.environ['FLASK_ENV'] = 'development'
    app.run(debug=True)