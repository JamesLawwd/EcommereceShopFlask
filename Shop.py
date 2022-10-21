# Ecommerce project
from flask import Flask, render_template, url_for, request, redirect, session
import pymysql

# Database Connection
# parameters ->host='localhost',user='root',password='',Database='EcommerceShopDB'
connection = pymysql.connect(host='localhost', user='root', password='', database='EcommerceShopDB')
print("Database connection successful")


# start
app = Flask(__name__)
app.secret_key="ILOVEProgramming"




@app.route('/')
def products():

    if 'key' in session:
        cursor = connection.cursor()
        sql = 'SELECT * FROM products'
        cursor.execute(sql)

        data = cursor.fetchall()
        print(data)
        return render_template('myproducts.html', mydata=data)

    else:
        return redirect('/login')


@app.route('/login', methods=['POST', 'GET'])
def login():
    if request.method =='POST':
        user_email = request.form['email']
        user_password = request.form['pswd']

        cursor = connection.cursor()
        sql = 'SELECT * FROM users WHERE user_email=%s AND user_password=%s'
        cursor.execute(sql, (user_email, user_password))

        if cursor.rowcount == 0:
            return render_template('login_signup.html', error="Invalid Credential Try Again")
        elif cursor.rowcount == 1:
            row = cursor.fetchone()
            session['key'] = row[1] # user_name
            session['email'] = row[2] # Email
            return redirect('/')
        else:
            return render_template('login_signup.html', error="Something  wrong with your Credential")



    return render_template('login_signup.html')


@app.route('/signup', methods=['POST','GET'])
def signup():
    if request.method == 'POST':

        user_name = request.form['txt']
        user_email = request.form['email']
        user_password = request.form['pswd']
        cursor = connection.cursor()
        sql = 'INSERT INTO users (user_name, user_email, user_password) VALUES (%s, %s,%s)'
        cursor.execute(sql, (user_name, user_email, user_password))
        connection.commit()

        return render_template('login_signup.html', message="REGISTERED SUCCESSFULLY")


    else:
        return render_template('login_signup.html')

@app.route('/logout')
def logout():
    if 'key' in session:
        session.clear()
        return redirect('/login')


app.run(debug=True)
# End App

# Jinja Templating Engine in Flask -> Python code can be written in html files
# variables {{variables}}
# {% python statement%}, if conditions , for loops

# {% for item in mydata%}
# {% endfor %}

# sessions
