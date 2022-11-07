from flask import Flask, render_template,request,session,redirect,url_for
from flaskext.mysql import MySQL
import os
from werkzeug.utils import secure_filename

app=Flask (__name__)

app.secret_key='56tf645fg6f676hg66'

mysql = MySQL()
app.config['MYSQL_DATABASE_USER']='root' 


app.config['MYSQL_DATABASE_PASSWORD']='root'

app.config['MYSQL_DATABASE_DB']='text_db'

app.config['MYSQL_DATABASE_HOST']='localhost'

mysql.init_app(app)

@app.route('/')
def index():
    return render_template('index.html')





@app.route('/login',methods=['GET','POST'])
def login():
    if request.method == 'GET':
        return render_template('login.html')
    
    if request.method == 'POST':
        conn = mysql.connect()
        curser = conn.cursor()
        query ="select * from login where username=%s and password=%s"
        curser.execute(query, (request.form['username'],request.form['password']))
        conn.commit()
        account = curser.fetchone()
        if account:
            
            if account[3] == 'admin':
                return redirect(url_for('admin_home'))
            elif account[3] == 'farmer':
                return redirect(url_for('farmer_home'))
            elif account[3] == 'customer':
                print(account[3])
                return redirect(url_for('customer_home'))
            else:
                return 'Please Register' 
        else:
            msg = "Incorrect Username or Password"
            return render_template("login.html",msg=msg)

@app.route('/admin_home')
def admin_home():
    return render_template('admin_home.html')





@app.route('/add_colleges',methods=['GET','POST'])
def add_colleges():
    if request.method=='GET':  
        return render_template('admin_home.html')
    if request.method=='POST':
        data=request.form
        conn=mysql.connect()
        cursor=conn.cursor()
        query="insert into add_colleges(clg_name,clg_code,adrs,email,cnum,district,clg_pin) values(%s,%s,%s,%s,%s,%s,%s)"
        cursor.execute(query,(data['clg_name'],data['clg_code'],data['adrs'],data['email'],data['district'],data['cnum'],data['clg_pin']))
        conn.commit()
        conn.close()
        return render_template('admin_home.html')


@app.route('/hod_registration',methods=['GET','POST'])
def hod_registration():
    if request.method=='GET':  
        return render_template('admin_home.html')
    if request.method=='POST':
        data=request.form
        conn=mysql.connect()
        cursor=conn.cursor()
        query="insert into hod_registration(fname,lname,adrs,email,cnum,gender,clg,dep) values(%s,%s,%s,%s,%s,%s,%s,%s)"
        cursor.execute(query,(data['fname'],data['lname'],data['adrs'],data['email'],data['cnum'],data['gender'],data['clg'],data['dep']))
        conn.commit()
        conn.close()
        return render_template('admin_home.html')

    
@app.route('/other_staff_registration',methods=['GET','POST'])
def other_staff_registration():
    if request.method=='GET':  
        return render_template('admin_home.html')
    if request.method=='POST':
        data=request.form
        conn=mysql.connect()
        cursor=conn.cursor()
        query="insert into other_staff_registration(fname,lname,blood,email,cnum,gender,clg,duty) values(%s,%s,%s,%s,%s,%s,%s,%s)"
        cursor.execute(query,(data['fname'],data['lname'],data['blood'],data['email'],data['cnum'],data['gender'],data['clg'],data['duty']))
        conn.commit()
        conn.close()
        return render_template('admin_home.html')


@app.route('/student_registration',methods=['GET','POST'])
def student_registration():
    if request.method=='GET':  
        return render_template('admin_home.html')
    if request.method=='POST':
        data=request.form
        conn=mysql.connect()
        cursor=conn.cursor()
        query="insert into student_registration(fname,lname,blood,email,cnum,gender,clg,adrs,date,pname,pnum) values(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
        cursor.execute(query,(data['fname'],data['lname'],data['blood'],data['email'],data['cnum'],data['gender'],data['clg'],data['adrs'],data['date'],data['pname'],data['pnum']))
        conn.commit()
        conn.close()
        return render_template('admin_home.html')



























if __name__=='__main__':
    app.run(debug=True,port=8000,host="localhost")
