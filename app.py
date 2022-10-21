# Client-server
# Framework
# Flask
# Request-response

# client -> listen to server response,send response to server (webbroweser)
# sever-> process client request , sends response to the client (flask application)

# Framework ,make development easy, by utilizing reusable code .... , flask, django

from flask import *

# start
app = Flask(__name__)


# decorators
# flask routing
# method -> route()
# tto bind the method route to our app object, then we use decorator @
@app.route('/home')
def home_page():
    return "Hello welcome to Flask"


@app.route('/login')
def login():
    return render_template('login.html')


@app.route('/signup')
def signup():
    return render_template('signup.html')


@app.route('/')
def index():
    return "View index page here"


@app.route('/add')
def add():
    cars = ['Mercedes', 'Subaru']
    return cars


# css, js, images,boostrap on flask
# static folder

@app.route('/back')
def back():
    return render_template('background.html')


app.run(debug=True)
# End
