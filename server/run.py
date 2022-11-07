from flask import Flask, render_template,request,session,redirect,url_for
import os
from werkzeug.utils import secure_filename

app=Flask (__name__)

app.secret_key='56tf645fg6f676hg66'


# from flask import Flask, render_template,request,session,redirect,url_for
# from flaskext.mysql import MySQL
# import os
# from werkzeug.utils import secure_filename

# import datetime
# app=Flask (__name__)

# app.secret_key='56tf645fg6f676hg66'

# mysql = MySQL()
# app.config['MYSQL_DATABASE_USER']='root' 


# app.config['MYSQL_DATABASE_PASSWORD']='root'

# app.config['MYSQL_DATABASE_DB']='agro_db'

# app.config['MYSQL_DATABASE_HOST']='localhost'

# mysql.init_app(app)


UPLOAD_FOLDER = '/agro/server/static/uploads/'
ALLOWED_EXTENSIONS = {'txt','pdf','png','jpg','jpeg','gif'}

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
def allowed_file(filename):
    return '.' in filename and \
        filename.rsplit('.',1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/')
def index():
    return render_template('login.html')
    

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
            print(account)
            session['loggedin'] = True
            session['id'] = account[0]
            session['user_id']=1
            session['username'] = account[1]
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


@app.route('/logout', methods =['GET'])
def logout():
    if session['loggedin']:
        session['loggedin'] = False
        session.pop('id',None)
        session.pop('username',None)
        return redirect(url_for('login'))
    else:
        print("login first")


@app.route('/farmer_home',methods=['GET','POST'])
def farmer_home():
    if request.method == 'GET':
        conn = mysql.connect()
        cursor = conn.cursor()
        query = "select * from pro_registration"
        cursor.execute(query)
        data = cursor.fetchall()
        print(len(data))
        conn.close()
        return render_template('farmer_home.html',result=data)

            




@app.route('/product_registration',methods=['GET','POST'])
def product_registration():
    if request.method == 'GET':
        return render_template('farmer_product_registration.html')
    if request.method == 'POST':
        # try:
        data = request.form

        file = request.files['image']
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'],filename))
        
        conn= mysql.connect()
        cursor = conn.cursor()
        s = session['user_id']
        path = os.path.join(app.config['UPLOAD_FOLDER'],filename)
        print(path)
        d1=data['desc']
        query = "INSERT INTO pro_registration(`pname`,`image`,`desc`,`prz`,`user_id`) values(%s,%s,%s,%s,%s)"
        cursor.execute(query,(data['pname'],filename,d1,data['prz'],s))
        conn.commit()
        conn.close()
        return render_template('farmer_product_registration.html')
@app.route('/farmer_view_fertilizer',methods=['GET','POST'])
def farmer_view_fertilizer():
    if request.method == 'GET':
        conn = mysql.connect()
        cursor = conn.cursor()
        query = "select * from fertilizer"
        cursor.execute(query)
        data = cursor.fetchall()
        conn.close()
        return render_template('farmer_view_fertilizer.html',result=data)
@app.route('/farmer_view_tips',methods=['GET','POST'])
def farmer_view_tips():
    if request.method == 'GET':
        conn = mysql.connect()
        cursor = conn.cursor()
        query = "select * from tips"
        cursor.execute(query)
        data = cursor.fetchall()
        conn.close()
        return render_template('farmer_view_tips.html',result=data)

@app.route('/farmer_view_notification',methods=['GET','POST'])
def farmer_view_notification():
    if request.method == 'GET':
        conn = mysql.connect()
        cursor = conn.cursor()
        query = "select * from notification"
        cursor.execute(query)
        data = cursor.fetchall()
        conn.close()
        return render_template('farmer_view_notification.html',result=data)

@app.route('/farmer_view_pestiside',methods=['GET','POST'])
def farmer_view_pestiside():
    if request.method == 'GET':
        conn = mysql.connect()
        cursor = conn.cursor()
        query = "select * from pestiside"
        cursor.execute(query)
        data = cursor.fetchall()
        conn.close()
        return render_template('farmer_view_pestiside.html',result=data)

@app.route('/farmer_view_seeds',methods=['GET','POST'])
def farmer_view_seeds():
    if request.method == 'GET':
        conn = mysql.connect()
        cursor = conn.cursor()
        query = "select * from seeds"
        cursor.execute(query)
        data = cursor.fetchall()
        conn.close()
        return render_template('farmer_view_seeds.html',result=data)

@app.route('/farmer_view_plants',methods=['GET','POST'])
def farmer_view_plants():
    if request.method == 'GET':
        conn = mysql.connect()
        cursor = conn.cursor()
        query = "select * from plants"
        cursor.execute(query)
        data = cursor.fetchall()
        conn.close()
        return render_template('farmer_view_plants.html',result=data)


@app.route('/farmer_view_subsidies',methods=['GET','POST'])
def farmer_view_subsidies():
    if request.method == 'GET':
        conn = mysql.connect()
        cursor = conn.cursor()
        query = "select * from subsidies"
        cursor.execute(query)
        data = cursor.fetchall()
        conn.close()
        return render_template('farmer_view_subsidies.html',result=data)

@app.route('/admin_view_notification',methods=['GET','POST'])
def admin_view_notification():
    if request.method == 'GET':
        conn = mysql.connect()
        cursor = conn.cursor()
        query = "select * from notification"
        cursor.execute(query)
        data = cursor.fetchall()
        conn.close()
        return render_template('admin_view_notification.html',result=data)
    if request.method == 'POST':
        conn = mysql.connect()
        cursor = conn.cursor()
        query = "delete from notification where id=%s"
        cursor.execute(query, request.form.get('delete_by_id'))
        conn.commit()
        conn.close()
        conn=mysql.connect()
        cursor= conn.cursor() 
        query="select * from notification"
        cursor.execute(query)
        data = cursor.fetchall()
        conn.close()
        return render_template('admin_view_notification.html',result=data)


    

@app.route('/admin_home')
def admin_home():
    return render_template('admin_home.html')

@app.route('/admin_view_farmer',methods=['GET','POST'])
def admin_view_farmer():
    if request.method == 'GET':
        conn = mysql.connect()
        cursor = conn.cursor()
        query = "select * from registration where type='farmer'"
        cursor.execute(query)
        data = cursor.fetchall()
        conn.close()
        return render_template('admin_view_farmer.html',result=data)
    if request.method == 'POST':
        conn = mysql.connect()
        cursor = conn.cursor()
        query = "delete from registration where id=%s"
        cursor.execute(query, request.form.get('delete_by_id'))
        conn.commit()
        conn.close()
        conn=mysql.connect()
        cursor= conn.cursor()
        query="select * from registration where type='farmer'"
        cursor.execute(query)
        data = cursor.fetchall()
        conn.close()
        return render_template('admin_view_farmer.html',result=data)

        
@app.route('/admin_view_customer',methods=['GET','POSt'])
def admin_view_customer():
    if request.method == 'GET':
        conn = mysql.connect()
        cursor = conn.cursor()
        query = "select * from registration where type='customer'"
        cursor.execute(query)
        data = cursor.fetchall()
        conn.close()
        return render_template('admin_view_customer.html',result=data)
    if request.method == 'POST':
        conn = mysql.connect()
        cursor = conn.cursor()
        query = "delete from registration where id=%s"
        cursor.execute(query, request.form.get('delete_by_id'))
        conn.commit()
        conn.close()
        conn=mysql.connect()
        cursor= conn.cursor()
        query="select * from registration"
        cursor.execute(query)
        data = cursor.fetchall()
        conn.close()
        return render_template('admin_view_customer.html',result=data)

@app.route('/farmer_view_product',methods=['GET','POST'])
def farmer_view_product():
    if request.method == 'GET':
        conn = mysql.connect()
        cursor = conn.cursor()
        query = "select * from pro_registration"
        cursor.execute(query)
        data = cursor.fetchall()
        conn.close()
        return render_template('farmer_view_product.html',result=data)
    if request.method == 'POST':
        conn = mysql.connect()
        cursor = conn.cursor()
        query = "delete from pro_registration where id=%s"
        cursor.execute(query, request.form.get('delete_by_id'))
        conn.commit()
        conn.close()
        conn=mysql.connect()
        cursor= conn.cursor()
        query="select * from pro_registration"
        cursor.execute(query)
        data = cursor.fetchall()
        conn.close()
        return render_template('farmer_view_product.html',result=data)
        
@app.route('/admin_view_product',methods=['GET','POST'])
def admin_view_product():
    if request.method == 'GET':
        conn = mysql.connect()
        cursor = conn.cursor()
        query = "select * from pro_registration"
        cursor.execute(query)
        data = cursor.fetchall()
        conn.close()
        return render_template('admin_view_product.html',result=data)
    if request.method == 'POST':
        conn = mysql.connect()
        cursor = conn.cursor()
        query = "delete from pro_registration where id=%s"
        cursor.execute(query, request.form.get('delete_by_id'))
        conn.commit()
        conn.close()
        conn=mysql.connect()
        cursor= conn.cursor()
        query="select * from pro_registration"
        cursor.execute(query)
        data = cursor.fetchall()
        conn.close()
        return render_template('admin_view_product.html',result=data)



@app.route('/customer_view_product',methods=['GET','POST'])
def customer_view_product():
    if request.method == 'GET':
        conn = mysql.connect()
        cursor = conn.cursor()
        query = "select * from pro_registration"
        cursor.execute(query)
        data = cursor.fetchall()
        conn.close()
        return render_template('customer_view_product.html',result=data)
    

@app.route('/admin_add_notification',methods=['GET','POST'])
def admin_add_notification():
    if request.method=='GET':  
        return render_template('admin_add_notification.html')
    if request.method=='POST':
        data=request.form
        today = datetime.datetime.now()
        conn=mysql.connect()
        cursor=conn.cursor()
        query="insert into notification(notification,date) values(%s,%s)"
        cursor.execute(query,(data['notification'],today.strftime("%x")))
        conn.commit()
        conn.close()
        return render_template('admin_home.html')
@app.route('/admin_add_subsidies',methods=['GET','POST'])
def admin_add_subsidies():
    if request.method=='GET':  
        return render_template('admin_add_subsidies.html')
    if request.method=='POST':
        data=request.form
        today = datetime.datetime.now()
        conn=mysql.connect()
        cursor=conn.cursor()
        query="insert into subsidies(subsidies,date) values(%s,%s)"
        cursor.execute(query,(data['subsidies'],today.strftime("%x")))
        conn.commit()
        conn.close()
        return render_template('admin_home.html')


@app.route('/admin_add_seeds',methods=['GET','POST'])
def admin_add_seeds():
    if request.method=='GET':  
        return render_template('admin_add_seeds.html')
    if request.method=='POST':
        data=request.form
        today = datetime.datetime.now()
        conn=mysql.connect()
        cursor=conn.cursor()
        query="insert into seeds(seeds,date) values(%s,%s)"
        cursor.execute(query,(data['seeds'],today.strftime("%x")))
        conn.commit()
        conn.close()
        return render_template('admin_home.html')


@app.route('/admin_view_seeds',methods=['GET','POST'])
def admin_view_seeds():
    if request.method == 'GET':
        conn = mysql.connect()
        cursor = conn.cursor()
        query = "select * from seeds"
        cursor.execute(query)
        data = cursor.fetchall()
        conn.close()
        return render_template('admin_view_seeds.html',result=data)
    if request.method == 'POST':
        conn = mysql.connect()
        cursor = conn.cursor()
        query = "delete from seeds where id=%s"
        cursor.execute(query, request.form.get('delete_by_id'))
        conn.commit()
        conn.close()
        conn=mysql.connect()
        cursor= conn.cursor() 
        query="select * from seeds"
        cursor.execute(query)
        data = cursor.fetchall()
        conn.close()
        return render_template('admin_view_seeds.html',result=data)

@app.route('/admin_view_fertilizer',methods=['GET','POST'])
def admin_view_fertilizer():
    if request.method == 'GET':
        conn = mysql.connect()
        cursor = conn.cursor()
        query = "select * from fertilizer"
        cursor.execute(query)
        data = cursor.fetchall()
        conn.close()
        return render_template('admin_view_fertilizer.html',result=data)
    if request.method == 'POST':
        conn = mysql.connect()
        cursor = conn.cursor()
        query = "delete from fertilizer where id=%s"
        cursor.execute(query, request.form.get('delete_by_id'))
        conn.commit()
        conn.close()
        conn=mysql.connect()
        cursor= conn.cursor() 
        query="select * from fertilizer"
        cursor.execute(query)
        data = cursor.fetchall()
        conn.close()
        return render_template('admin_view_fertilizer.html',result=data)


@app.route('/admin_add_fertilizer',methods=['GET','POST'])
def admin_add_fertilizer():
    if request.method=='GET':  
        return render_template('admin_add_fertilizer.html')
    if request.method=='POST':
        data=request.form
        today = datetime.datetime.now()
     
        conn=mysql.connect()
        cursor=conn.cursor()
        query="insert into fertilizer(fertilizer,date) values(%s,%s)"
        cursor.execute(query,(data['fertilizer'],today.strftime("%x")))
        conn.commit()
        conn.close()
        return render_template('admin_home.html')

@app.route('/admin_view_pestiside',methods=['GET','POST'])
def admin_view_pestiside():
    if request.method == 'GET':
        conn = mysql.connect()
        cursor = conn.cursor()
        query = "select * from pestiside"
        cursor.execute(query)
        data = cursor.fetchall()
        conn.close()
        return render_template('admin_view_pestiside.html',result=data)
    if request.method == 'POST':
        conn = mysql.connect()
        cursor = conn.cursor()
        query = "delete from pestiside where id=%s"
        cursor.execute(query, request.form.get('delete_by_id'))
        conn.commit()
        conn.close()
        conn=mysql.connect()
        cursor= conn.cursor() 
        query="select * from pestiside"
        cursor.execute(query)
        data = cursor.fetchall()
        conn.close()
        return render_template('admin_view_pestiside.html',result=data)


@app.route('/admin_add_pestiside',methods=['GET','POST'])
def admin_add_pestiside():
    if request.method=='GET':  
        return render_template('admin_add_pestiside.html')
    if request.method=='POST':
        data=request.form
        today = datetime.datetime.now()
     
        conn=mysql.connect()
        cursor=conn.cursor()
        query="insert into pestiside(pestiside,date) values(%s,%s)"
        cursor.execute(query,(data['pestiside'],today.strftime("%x")))
        conn.commit()
        conn.close()
        return render_template('admin_home.html')

@app.route('/admin_view_plants',methods=['GET','POST'])
def admin_view_plants():
    if request.method == 'GET':
        conn = mysql.connect()
        cursor = conn.cursor()
        query = "select * from plants"
        cursor.execute(query)
        data = cursor.fetchall()
        conn.close()
        return render_template('admin_view_plants.html',result=data)
    if request.method == 'POST':
        conn = mysql.connect()
        cursor = conn.cursor()
        query = "delete from plants where id=%s"
        cursor.execute(query, request.form.get('delete_by_id'))
        conn.commit()
        conn.close()
        conn=mysql.connect()
        cursor= conn.cursor() 
        query="select * from plants"
        cursor.execute(query)
        data = cursor.fetchall()
        conn.close()
        return render_template('admin_view_plants.html',result=data)


@app.route('/admin_add_plants',methods=['GET','POST'])
def admin_add_plants():
    if request.method=='GET':  
        return render_template('admin_add_plants.html')
    if request.method=='POST':
        data=request.form
        today = datetime.datetime.now()
     
        conn=mysql.connect()
        cursor=conn.cursor()
        query="insert into plants(plants,date) values(%s,%s)"
        cursor.execute(query,(data['plants'],today.strftime("%x")))
        conn.commit()
        conn.close()
        return render_template('admin_home.html')

@app.route('/admin_view_subsidies',methods=['GET','POST'])
def admin_view_subsidies():
    if request.method == 'GET':
        conn = mysql.connect()
        cursor = conn.cursor()
        query = "select * from subsidies"
        cursor.execute(query)
        data = cursor.fetchall()
        conn.close()
        return render_template('admin_view_subsidies.html',result=data)
    if request.method == 'POST':
        conn = mysql.connect()
        cursor = conn.cursor()
        query = "delete from subsidies where id=%s"
        cursor.execute(query, request.form.get('delete_by_id'))
        conn.commit()
        conn.close()
        conn=mysql.connect()
        cursor= conn.cursor() 
        query="select * from subsidies"
        cursor.execute(query)
        data = cursor.fetchall()
        conn.close()
        return render_template('admin_view_subsidies.html',result=data)




@app.route('/admin_view_tips',methods=['GET','POST'])
def admin_view_tips():
    if request.method == 'GET':
        conn = mysql.connect()
        cursor = conn.cursor()
        query = "select * from tips"
        cursor.execute(query)
        data = cursor.fetchall()
        conn.close()
        return render_template('admin_view_tips.html',result=data)
    if request.method == 'POST':
        conn = mysql.connect()
        cursor = conn.cursor()
        query = "delete from tips where id=%s"
        cursor.execute(query, request.form.get('delete_by_id'))
        conn.commit()
        conn.close()
        conn=mysql.connect()
        cursor= conn.cursor() 
        query="select * from tips"
        cursor.execute(query)
        data = cursor.fetchall()
        conn.close()
        return render_template('admin_view_tips.html',result=data)


@app.route('/admin_add_tips',methods=['GET','POST'])
def admin_add_tips():
    if request.method=='GET':  
        return render_template('admin_add_tips.html')
    if request.method=='POST':
        data=request.form
        today = datetime.datetime.now()
     
        conn=mysql.connect()
        cursor=conn.cursor()
        query="insert into tips(tips,date) values(%s,%s)"
        cursor.execute(query,(data['tips'],today.strftime("%x")))
        conn.commit()
        conn.close()
        return render_template('admin_home.html')

@app.route('/customer_registration',methods=['GET','POST'])
def customer_registration():
    if request.method=='GET':  
        return render_template('customer_registration.html')
    if request.method=='POST':
        data=request.form
        conn=mysql.connect()
        cursor=conn.cursor()
        query="insert into registration(fname,lname,gender,adrs,panchayath,ward_no,cnum,street_name,house_no,type) values(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
        cursor.execute(query,(data['fname'],data['lname'],data['gender'],data['adrs'],data['panchayath'],data['ward_no'],data['cnum'],data['street_name'],data['house_no'],'customer'))
        conn.commit()
    
        query="insert into login(username,password,type,user_id) values (%s,%s,%s,%s)"
        cursor.execute(query,(data['username'],data['password'],'customer',cursor.lastrowid))
        conn.commit()
       
        conn.close()
        return render_template('customer_home.html')
@app.route('/farmer_registration',methods=['GET','POST'])
def registration():
    if request.method=='GET':  
        return render_template('farmer_registration.html')
    if request.method=='POST':
        data=request.form
        conn=mysql.connect()
        cursor=conn.cursor()
        query="insert into registration(fname,lname,gender,adrs,panchayath,ward_no,cnum,street_name,house_no,type) values(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
        cursor.execute(query,(data['fname'],data['lname'],data['gender'],data['adrs'],data['panchayath'],data['ward_no'],data['cnum'],data['street_name'],data['house_no'],'farmer'))
        conn.commit()

        query="insert into login(username,password,type,user_id) values (%s,%s,%s,%s)"
        cursor.execute(query,(data['username'],data['password'],'farmer',cursor.lastrowid))
        conn.commit()
     
        conn.close()
        return render_template('farmer_home.html')



@app.route('/about')
def about():
    return render_template('about.html')
    


@app.route('/customer_home',methods=['GET','POST'])
def customer_home():
    if request.method == 'GET':
        conn = mysql.connect()
        cursor = conn.cursor()
        query = "select * from pro_registration"
        cursor.execute(query)
        data = cursor.fetchall()
        print(len(data))
        conn.close()
        return render_template('customer_home.html',result=data)


@app.route('/new_order',methods=['GET','POST'])
def newOrder():
    if request.method == 'POST':
        print('here')
        print(request.args.get('pid'))
        product_id=request.args.get('pid')
        conn = mysql.connect()
        cursor = conn.cursor()
        query="select user_id,prz from pro_registration where id="+product_id
        cursor.execute(query)
        data = cursor.fetchone()
        today = datetime.datetime.now()
        cursor.close()
        conn.close()
        conn = mysql.connect()
        cursor = conn.cursor()
        order_query = "INSERT INTO orders(p_id,c_id,date,status,farmer_id) values(%s,%s,%s,%s,%s)"
        cursor.execute(order_query,(product_id,data[0],today.strftime("%x"),'pending',session['user_id']))
        conn.commit()
        conn.close()
        return render_template('customer_home.html')

@app.route('/order',methods = ['GET','POST'])
def order():
    if request.method == 'GET':
        conn = mysql.connect()
        cursor = conn.cursor()
        query = "select * from orders o, pro_registration p,registration r where o.p_id=p.id and o.farmer_id=r.id and o.status='pending'"
        cursor.execute(query)
        data = cursor.fetchall()
        conn.close()
        return render_template('order.html',result=data)
    if request.method == "POST":
        print(request.form)
        conn = mysql.connect()
        cursor = conn.cursor()

        q = "update orders set status='{}' where id='{}'"
        query = q.format('Approved',request.form.get("id"))
        print(query)
        cursor.execute(query)
        conn.commit() 
        return redirect(url_for('order'))



# @app.route('/new_order',methods=['GET','POST'])
# def newOrder():
#     if request.method == 'POST':
#         print('here')
#         print(request.args.get('pid'))
#         product_id=request.args.get('pid')
#         conn = mysql.connect()
#         cursor = conn.cursor()
#         query="select user_id,prz from pro_registration where id="+product_id
#         cursor.execute(query)
#         data = cursor.fetchone()
#         today = datetime.datetime.now()
#         cursor.close()
#         conn.close()
#         conn = mysql.connect()
#         cursor = conn.cursor()
#         order_query = "INSERT INTO orders(p_id,c_id,date,status,farmer_id) values(%s,%s,%s,%s,%s)"
#         cursor.execute(order_query,(product_id,data[0],today.strftime("%x"),'pending',session['user_id']))
#         conn.commit()
#         conn.close()
#         return render_template('customer_home.html')

@app.route('/customer_view_order',methods = ['GET','POST'])
def customer_view_order():
    if request.method == 'GET':
        conn = mysql.connect()
        cursor = conn.cursor()
        query = "select * from orders o, pro_registration p,registration r where o.p_id=p.id and o.c_id=r.id and o.status='Approved'"
        cursor.execute(query)
        data = cursor.fetchall()
        conn.close()
        return render_template('customer_view_order.html',result=data)
    # if request.method == "POST":
    #     print(request.form)
    #     conn = mysql.connect()
    #     cursor = conn.cursor()

    #     q = "update orders set status='{}' where id='{}'"
    #     query = q.format('Approved',request.form.get("id"))
    #     print(query)
    #     cursor.execute(query)
    #     conn.commit() 
    #     return redirect(url_for('order'))
    if request.method == 'POST':
        conn = mysql.connect()
        cursor = conn.cursor()
        query = "delete from orders where id=%s"
        cursor.execute(query, request.form.get('delete_by_id'))
        conn.commit()
        conn.close()
        conn=mysql.connect()
        cursor= conn.cursor() 
        query = "select * from orders o, pro_registration p,registration r where o.p_id=p.id and o.c_id=r.id and o.status='Approved'"
        cursor.execute(query)
        data = cursor.fetchall()
        conn.close()
        return render_template('customer_view_order.html',result=data)
 
            
if __name__=='__main__':
    app.run(debug=True,port=8000,host="localhost")

# select agro_db.orders.date, agro_db.pro_registration.pname, agro_db.registration from agro_db.orders inner join ( agro_db.pro_registration inner join agro_db.registration on agro_db.registration.id = agro_db.pro_registration.user_id) on agro_db.orders.p_id and agro_db.registration.id = agro_db.orders.farmer_id;
# select * from orders o, pro_registration p where o.p_id=p.id and o.farmer_id='27';
# select * from orders o, pro_registration p,registration r where o.p_id=p.id and o.farmer_id=r.id;