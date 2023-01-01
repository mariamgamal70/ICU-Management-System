from flask import Flask, render_template, redirect, url_for, request,session,flash
from flask_session import Session
import mysql.connector
from flask_mail import Mail, Message
# from flask_socketio import SocketIO
# from apiclient.discovery import build #builds service object for any google api
# from google_auth_oauthlib.flow import InstalledAppFLow
# scopes = ['https://www.googleapis.com/auth/calendar.events']

# app.config['SECRET_KEY'] = 'vnkdjnfjknfl1232#'
# socketio = SocketIO(app)

from datetime import datetime
now = datetime.now()
formatted_date = now.strftime('%Y-%d-%m %H:%M:%S')

app = Flask(__name__)

app.config["SESSION_PERMANENT"]=False
app.config["SESSION_TYPE"]="filesystem"
Session(app)

app.config["MAIL_SERVER"]="smtp.gmail.com"
app.config["MAIL_PORT"] = 465
app.config["MAIL_USERNAME"] = "mariamgamal70@gmail.com" #senders email
app.config["MAIL_PASSWORD"] = "azaesjimhgtnsydq" #senders password
app.config["MAIL_USE_TLS"] = False
app.config["MAIL_USE_SSL"] = True
mail = Mail()
mail.init_app(app)
mydb = mysql.connector.connect(
   host="localhost",
   user="root",
   password="lovelygirl12",
   database="icu_management_system"
)
mycursor = mydb.cursor()
#GET used when no info is sent(written in URL) , POST is used when info is sent(Ex:Sensitive info)(not written in URL)
#get function route("route)
#functions are GET only by default, to make it GET and POST , u should define it as a parameter in route
#route("route",methods=["POST","GET"])
# in case it is GET and POST you should check inside the function whether the incoming is a get or post request , if its a get ,return template, if its a post , send data do changes


def sendmessage(result):
   msg = Message(subject="Inquiry/Complaint", sender=result['email'], recipients=["mariamgamal70@gmail.com"])
   msg.body = 'from ' + result['email'] + '\n'+'Name: '+result['firstname'] +' '+result['lastname'] + '\n' 'Complaint: ' + result['complaint']
   mail.send(msg)


@app.route("/")#GET METHOD
def index():
   return render_template("index.html")

@app.route('/adminhome')
def Adminhome():
   return render_template('/admin/adminDashboard.html')

@app.route("/AdminMain")
def AdminMain():
   return render_template("AdminMain.html")
   diction={"name":"sharif"}
   # sql="SELECT "  

@app.route("/signin",methods=["POST","GET"])  # GET METHOD
def signin():
   if request.method == "POST":
      #PATIENT ONLY-----------------------------------------------------------------
      if "patient" in request.form:
         patientid = request.form["patientID"]
         patientpassword = request.form["patientpassword"]
         mycursor.execute(
             "SELECT * FROM patient_record WHERE IdPatient_Record = %s AND password = %s", (patientid, patientpassword))
         account = mycursor.fetchone()
         if account:
            mycursor.execute(
            "SELECT FirstName FROM patient WHERE patientid = %s AND patientpassword = %s", (patientid, patientpassword))
            patientname=mycursor.fetchone()
            session["id"]=patientid
            return render_template("patienthome.html")
         else: 
            flash('ID/Password is incorrect','warning')
            return redirect('/signin')
      #ENDPATIENT-------------------------------------------------------------------------
      #DOCTORONLY--------------------------------------------------------------------------
      elif "doctor" in request.form:
         doctorid = request.form["doctorID"]
         doctorpassword = request.form["doctorpassword"]
         mycursor.execute(
             "SELECT * FROM doctor WHERE doctorid = %s AND doctorpassword = %s", (doctorid, doctorpassword,))
         account = mycursor.fetchone()
         if account:
            mycursor.execute(
            "SELECT FirstName FROM patient WHERE doctorid = %s AND doctorpassword = %s", (doctorid, doctorpassword,))
            doctorname=mycursor.fetchone()
            session["id"]=doctorid
            return render_template("doctorhome.html")
         else:
            flash('ID/Password is incorrect', 'warning')
            return redirect('/signin')
      #ENDDOCTOR-------------------------------------------------------------------------------
      #NURSEONLY-------------------------------------------------------------------------------
      elif "nurse" in request.form:
         nurseid = request.form["nurseID"]
         nursepassword = request.form["nursepassword"]
         mycursor.execute(
             "SELECT * FROM nurse WHERE nurseid = %s AND nursepassword = %s", (nurseid, nursepassword,))
         account = mycursor.fetchone()
         if account:
            mycursor.execute(
            "SELECT FirstName FROM nurse WHERE nurseid = %s AND nursepassword = %s", (nurseid, nursepassword,))
            nursename=mycursor.fetchone()
            session["id"]=doctorid
            return render_template("doctorhome.html")
         else:
            flash('ID/Password is incorrect', 'warning')
            return redirect('/signin')
      #ENDNURSE-------------------------------------------------------------------------------------
      #ADMINONLY------------------------------------------------------------------------------------
      elif "admin" in request.form:
         adminid = request.form["adminID"]
         adminpassword = request.form["adminpassword"]
         mycursor.execute(
             "SELECT * FROM admin WHERE adminid = %s AND adminpassword = %s", (adminid, adminpassword,))
         account = mycursor.fetchone()
         if account:
            mycursor.execute(
            "SELECT FirstName FROM admin WHERE adminid = %s AND adminpassword = %s", (adminid, adminpassword,))
            adminname=mycursor.fetchone()
            session["id"]=adminid
            return render_template("AdminMain.html")
         else:
            flash('ID/Password is incorrect', 'warning')
            return redirect('/signin')
      #ADMINEND---------------------------------------------------------------------------------------
      #RECEPTIONISTSONLY------------------------------------------------------------------------------
      elif "receptionist" in request.form:
         receptionistid = request.form["receptionistID"]
         receptionistpassword = request.form["receptionistpassword"]
         mycursor.execute(
             "SELECT * FROM receptionist WHERE receptionistid = %s AND receptionistpassword = %s", (receptionistid, receptionistpassword,))
         account = mycursor.fetchone()
         if account:
            mycursor.execute(
            "SELECT FirstName FROM receptionist WHERE receptionistid = %s AND receptionistpassword = %s", (receptionistid, receptionistpassword,))
            adminname=mycursor.fetchone()
            session["id"]=adminid
            return render_template("receptionist1.html")
         else:
            flash('ID/Password is incorrect', 'warning')
            return redirect('/signin')
      #RECEPTIONISTEND-------------------------------------------------------------------------------
   return render_template('signin.html')

@app.route("/contactus",methods=["POST","GET"])  # GET METHOD
def contactus():
   if request.method == "POST":
      result={}
      result['firstname'] = request.form["FirstName"]
      result['lastname'] = request.form["LastName"]
      result['email'] = request.form["email"]
      result['complaint']= request.form["complain"]
      sendmessage(result)
      flash('Email is successfully sent','success')
      return redirect("/contactus")
   return render_template("contactus.html")


@app.route("/nursehome", methods=["POST", "GET"])
def getnursepatientdata():
   nurseid=session['id']
   result={}
   mycursor.execute('SELECT FirstName,LastName,Birthdate,SSN,Gender from nurse where NurseID=%s',(nurseid))
   nurse=mycursor.fetchone()
   result['nurseid']=session['id']
   result['nursename'] = nurse[0] + nurse[1]
   result['nursebirthdate']=nurse[2]
   result['nursessn']=nurse[3]
   result['nursegender']=nurse[4]
   mycursor.execute('SELECT FirstName,LastName,patientID from inpatient join nurse on nurseID=nurseID where nurseID=%s',(nurseid))
   patient=mycursor.fetchone()
   result['patientname']= patient[0] +patient[1]
   result['patientid']= patient[2]
   render_template('/nursehome',data=result)

@app.route("/logout")
def LogOut():
   session.pop("id",None)
   redirect("/")

if __name__ == "__main__":
   app.run(debug=True)
   #socketio.run(app, debug=True)
