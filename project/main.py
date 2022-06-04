from flask import Flask,render_template,request,redirect,flash, url_for,Response,session
from flask_session import Session
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import exc,func
import psycopg2
import os
from sqlalchemy import create_engine, exc
from sqlalchemy.orm import scoped_session,sessionmaker
from models import Base, Agent, Car, Company, Customer
from werkzeug.utils import secure_filename
import json
# from sqlalchemy.orm import query
with open('config.json','r') as c:
    params=json.load(c)["params"]

app=Flask(__name__)
#app.config["SQLALCHEMY_DATABASE_URI"] =  "postgresql://postgres:password@localhost/postgres"
app.config['UPLOAD_FOLDER']=params['upload_location']
db = SQLAlchemy(app)
app.secret_key = os.urandom(24)

engine=create_engine('postgresql://postgres:password@localhost/postgres')
Base.metadata.bind=engine
db=scoped_session(sessionmaker(bind=engine))

# -----------------------------------------------------------------------------
# simple front pages
@app.route('/')
def home():
    return render_template('project_homepage.html')

@app.route('/aboutus')
def aboutus():
    return render_template('aboutus.html') 

@app.route('/contactus')
def contactus():
    return render_template('contactus.html')

@app.route('/login_page',methods=['GET','POST'])
def login():
    return render_template('login_page.html') 
# ----------------------------------------------------------------------------------
# customer main page
@app.route('/customer_page',methods=['GET','POST'])
def page():
    info=db.execute("select * from cars order by car_id").fetchall()
    # image_url=url_for('static',filename='/'+info.img)
    return render_template("customer_page.html",result=value, data=info)

# -------------------------------------------------------------------------------
                                 # agents operations
# agent login
@app.route('/agent-sign',methods=['GET','POST'])
def agentsign():
    if(request.method =='POST'):
        usern=int(request.form.get("id"))
        passw=request.form.get("password")

        result=db.execute("select * from agents where a_id= :u and pass= :p" ,{"u":usern,"p":passw}).fetchone()
        if result is not None:
            if(result['a_id'] == usern and result['pass'] == passw):
                session['user']=result.a_id
                session['namet']=result.name
                flash("you are successfully logged in ","success")
                global user
                user = result
                return render_template("admin_upload.html",result=user)
        else:   
            flash("username or password invalid","danger")
            return render_template("agent-sign.html")
    return render_template("agent-sign.html")                

# ---- ----- ------- ------- ------- ------- ------ ------- -------- ------- -

# delete data 
@app.route('/delete',methods=['GET','POST'])
def delete():
    data=db.execute("select * from cars order by car_id").fetchall()
    return render_template('delete.html', result=user,data=data)

@app.route('/delete_id',methods=['GET','POST'])
def delete_id():
    if (request.method=='POST'):
            cid=int(request.form.get("id"))
            query=db.execute("select * from cars where car_id= :u",{"u":cid}).fetchone()
            if query is not None:
                db.execute("delete from cars where car_id= :u " ,{"u":cid})
                db.commit()
                flash("successfully deleted!")
                data=db.execute("select * from cars order by car_id").fetchall()
                return render_template('delete.html', result=user,data=data)
            else:
                flash("Error: invalid Car id")
                data=db.execute("select * from cars order by car_id").fetchall()
                return render_template('delete.html', result=user,data=data)
            data=db.execute("select * from cars").fetchall()
            return render_template('delete.html', result=user,data=data)
                        
    


# customers data
@app.route('/customers',methods=['GET','POST'])
def customers():
    name=user.a_id
    data=db.execute("select * from cust where agent_id= :u " ,{"u":name}).fetchall()
    return render_template('customers.html', result=user,data=data)    
    
# update data
@app.route('/update',methods=['GET','POST'])
def updates():
    data=db.execute("select * from cars order by car_id").fetchall()
    return render_template('update.html', result=user,data=data)   
# update data id
@app.route('/update_id',methods=['GET','POST'])
def updates_id():
    if (request.method=='POST'):
            cid=int(request.form.get("cid"))
            manu=request.form.get("manu")
            price=int(request.form.get("price"))
            model=request.form.get("model")
            bid=int(request.form.get("bid"))
            query=db.execute("select * from cars where car_id= :u",{"u":cid}).fetchone()
            if query is not None:
                checker=db.execute("select * from Company where id=:d",{"d":bid}).fetchone()
                if checker is not None:
                    db.execute("update cars set manufacturer=:m,price=:p,model=:mod,branch_id=:b where car_id= :u " ,{"u":cid,"m":manu,"p":price,"mod":model,"b":bid})
                    db.commit()
                    flash("successfully updated!")
                    data=db.execute("select * from cars order by car_id").fetchall()
                    return render_template('update.html', result=user,data=data)
                else:
                    flash("Error:incorrect branch id")
                    data=db.execute("select * from cars order by car_id").fetchall()
                    return render_template('update.html', result=user,data=data)
            else:
                flash("Error: invalid Car id")
                data=db.execute("select * from cars order by car_id").fetchall()
                return render_template('update.html', result=user,data=data)
    data=db.execute("select * from cars order by car_id").fetchall()
    return render_template('update.html', result=user,data=data)   


# --------------------------------------------------------------------------------------------

    # signin page
@app.route("/cus-sign")
def customer_page():
    return render_template('cus-sign.html')       


# customer signup data
@app.route("/cus-sign-up",methods=['GET','POST'])
def customer_signup():
    if(request.method=='POST'):
        rid=int(request.form.get("ref_id"))
        name=request.form.get("name")
        email=request.form.get("email")
        nic=int(request.form.get("cnic"))
        no=int(request.form.get("phoneno"))
        address=request.form.get("address")
        passw=request.form.get("password")
        result=db.execute("select * from Customer where cnic= :u",{"u":nic}).fetchone()
        if result is not None:
            flash("cnic already in use","danger")  
            return render_template('cus-sign.html')
        else:
            entry=Customer(cnic=nic,cname=name,email=email,passwords=passw,address=address,agent_id=rid,phone=no)
            db.add(entry)
            db.commit()
            result= db.execute("select * from Customer where cnic=:u",{"u":nic}).fetchone()  
            if result is not None:
                flash("your account has been created!!","success")
                return redirect(url_for('customer_signup'))
            flash("unable to create","danger")  
            return render_template('cus-sign.html')
        return render_template('cus-sign.html')
    return render_template('cus-sign.html')       


#  customer signin data
@app.route("/cus-sign-in",methods=['GET','POST'])
def customer_signin():
    if(request.method =='POST'):
        nic=int(request.form.get("nic"))
        passw=request.form.get("password")

        result=db.execute("select * from Customer where cnic= :u and passwords= :p" ,{"u":nic,"p":passw}).fetchone()
        if result is not None:
            if(result['cnic'] == nic and result['passwords'] == passw):
                session['user']=result.cnic
                session['namet']=result.cname
                flash("you are successfully logged in ","success")
                global value
                value = result
                return redirect(url_for('page'))
                # return render_template("customer_page.html",result=value)
        else:   
            flash("username or password invalid","danger")
            return render_template("cus-sign.html")
    return render_template('cus-sign.html')       



# admin upload
@app.route('/admin_upload', methods=['GET','POST'])
def cars_data():
    if(request.method=='POST'):
        cid=int(request.form.get("cid"))
        mod=request.form.get("mod")
        price=int(request.form.get("price"))
        bid=int(request.form.get("bid"))
        manu=request.form.get("manu")
        img=request.files['img1']
        img.save(os.path.join(app.config['UPLOAD_FOLDER'],secure_filename(img.filename)))
        if not img:
            flash("no images uploaded")
            return render_template('admin_upload.html',result=user)  
        # entring data in database
        result=db.execute("select * from cars where car_id= :u",{"u":cid}).fetchone()
        if result is not None:
            flash("car id already in use","danger")  
            return render_template('admin_upload.html',result=user)
        else:

            entries=Car(car_id=cid,manufacturer=manu,model=mod,branch_id=bid,price=price,img=secure_filename(img.filename))
            db.add(entries)
            db.commit()
            result= db.execute("select * from cars where car_id=:u",{"u":cid}).fetchone()  
            if result is not None:
                flash("car data has been upload!!","success")
                return redirect(url_for('cars_data'))
            flash("unable to upload","danger")  
            return render_template('admin_upload.html')
        return render_template('admin_upload.html')
    return render_template('admin_upload.html', result=user) 

if __name__ == '__main__':
    app.secret_key='super_secret_key'
    app.debug = True
    app.run(host='0.0.0.0', port=5000)