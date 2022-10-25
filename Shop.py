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

        cursor_camera = connection.cursor()
        sql_camera = 'SELECT * FROM products WHERE product_category="electronic" '
        cursor_camera.execute(sql_camera)

        camera = cursor_camera.fetchall()

        cursor_watch = connection.cursor()
        sql_watch ='SELECT * FROM products WHERE product_category="watch" LIMIT 3'
        cursor_watch.execute(sql_watch)
        watch = cursor_watch.fetchall()

        cursor_shoe = connection.cursor()
        sql_shoe = 'SELECT * FROM products WHERE product_category="sports"'
        cursor_shoe.execute(sql_shoe)
        shoe = cursor_shoe.fetchall()




        return render_template('myproducts.html', camera=camera , watch=watch, shoe=shoe)


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



@app.route('/single/<product_id>')
def single(product_id):
    if 'key' in session:

        cursor = connection.cursor()
        sql = 'SELECT * FROM products WHERE product_id=%s'
        cursor.execute(sql, (product_id))


        row = cursor.fetchone()

        return render_template('single.html', item_data=row)

    else:
         return redirect('login.html')






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


import requests
import base64
import datetime

from requests.auth import HTTPBasicAuth


@app.route('/mpesa_payment', methods=['POST', 'GET'])
def mpesa():
    if request.method == 'POST':
        phone = request.form['phone']
        amount = request.form['amount']

        consumer_key = "GTWADFxIpUfDoNikNGqq1C3023evM6UH"
        consumer_secret = "amFbAoUByPV2rM5A"

        api_URL = "https://sandbox.safaricom.co.ke/oauth/v1/generate?grant_type=client_credentials"
        r = requests.get(api_URL, auth=HTTPBasicAuth(consumer_key, consumer_secret))

        data = r.json()

        access_token = "Bearer" + ' ' + data['access_token']


        #  GETTING THE PASSWORD
        timestamp = datetime.datetime.today().strftime('%Y%m%d%H%M%S')

        passkey = 'bfb279f9aa9bdbcf158e97dd71a467cd2e0c893059b10f78e6b72ada1ed2c919'
        business_short_code = "174379"

        data = business_short_code + passkey + timestamp
        encoded = base64.b64encode(data.encode())

        password = encoded.decode('utf-8')

        payload = {
            "BusinessShortCode": "174379",
            "Password": "{}".format(password),
            "Timestamp": "{}".format(timestamp),
            "TransactionType": "CustomerPayBillOnline",
            "Amount": amount,  # use 1 when testing
            "PartyA": phone,  # change to your number
            "PartyB": "174379",
            "PhoneNumber": phone,
            "CallBackURL": "https://modcom.co.ke/job/confirmation.php",
            "AccountReference": "Modcom",
            "TransactionDesc": "Modcom"
        }

        headers = {
            "Authorization": access_token,
            "Content-Type": "application/json"
        }

        url = "https://sandbox.safaricom.co.ke/mpesa/stkpush/v1/processrequest"

        response = requests.post(url, json=payload, headers=headers)
        print(response.text)

        return render_template('mpesa_payment.html', message="Please check your phone for Payment")

    else:
        return render_template('mpesa_payment.html')




app.run(debug=True)
# End App

# Jinja Templating Engine in Flask -> Python code can be written in html files
# variables {{variables}}
# {% python statement%}, if conditions , for loops

# {% for item in mydata%}
# {% endfor %}

# sessions
