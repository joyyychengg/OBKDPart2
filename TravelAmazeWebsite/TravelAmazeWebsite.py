from flask import Flask, render_template, redirect, url_for, request
import hashlib
import mysql.connector
from mysql.connector import Error

app=Flask(__name__)
@app.route('/index', methods=['GET'])
@app.route('/now', methods=['GET'])
@app.route('/', methods=['GET'])
def default():
    return render_template('index.html')

@app.route('/login',methods=['POST'])
def login():

    if request.method == "POST":
        user_name = request.form['loginUserName']
        user_password = request.form['loginPassword']


        rec = select_customer(user_name,user_password)
        if rec == None:
            print("Record is null")
        else:
            print("rec="+str(rec))
            print("\nPrinting each customer record")
            for row in rec:
                print("FirstName = ", row[1])
                print("LastName = ", row[2])

    return render_template('login.html', tFirstName=row[1], tLastName=row[2])

def select_customer(username, password_salt):
    query = "SELECT * FROM ta_customers WHERE UserName = %s AND PasswordSalt = %s"
    print("query="+query)
    args = (username, password_salt)

    try:
        conn = mysql.connector.connect(host='localhost', database='travelamazedb', user='root', password='')

        cursor = conn.cursor()
        cursor.execute(query,args)
        records = cursor.fetchall()
        print("total number of rows in customer is: ", cursor.rowcount)

        print("Row Count = " + str(cursor.rowcount))
        if cursor.rowcount == 0:
            records = None
    
    except Error as e:
        print("Error reading data from MySQL Table", e)
    
    finally:
        if(conn.is_connected()):
            conn.close()
            cursor.close()
            print("MySQL connection is closed")
        return records


