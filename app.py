from flask import get_flashed_messages
from flask import Flask, render_template, redirect, url_for, request, session, flash, Response
from flask_session import Session
import mysql.connector
from flask_mail import Mail, Message
from werkzeug.utils import secure_filename

# from flask_socketio import SocketIO

# from google.auth.transport.requests import Request
# from google.oauth2.credentials import Credentials
# from google_auth_oauthlib.flow import InstalledAppFlow
# from googleapiclient.discovery import build
# from googleapiclient.errors import HttpError
# scopes = ['https://www.googleapis.com/auth/calendar']
# flow = InstalledAppFlow.from_client_secrets_file("client_secret.json", scopes=scopes)
#flow.run_console()
# app.config['SECRET_KEY'] = 'vnkdjnfjknfl1232#'
# socketio = SocketIO(app)

from datetime import datetime
current_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

app = Flask(__name__)

app.config["SESSION_PERMANENT"]=False
app.config["SESSION_TYPE"]="filesystem"
Session(app)

# Session encryption key
app.config["SECRET_KEY"] = "zf_b1JkWCAQneZoA0Xe8Gw"


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
   password="Eng_8730667",
   database="icu_management_system"
)
mycursor = mydb.cursor()
#GET used when no info is sent(written in URL) , POST is used when info is sent(Ex:Sensitive info)(not written in URL)
#get function route("route)
#functions are GET only by default, to make it GET and POST , u should define it as a parameter in route
#route("route",methods=["POST","GET"])
# in case it is GET and POST you should check inside the function whether the incoming is a get or post request , if its a get ,return template, if its a post , send data do changes
def updatenotificationbutton():
   messages = get_flashed_messages()
   message_count = len(messages)
   return message_count

def notifynurse(notification):
   string=notification['type']+'\n'+notification['info']
   flash(string,'warning')

def calculate_age(born):
   # BORN SHOULD BE WRITTIN IN THIS FORMAT FIRST BEFORE PUTTING IT AS A PARAMETER  
   # born = datetime(1997, 5, 21)
   today = datetime.now()
   return today.year - born.year - ((today.month, today.day) < (born.month, born.day))

def sendmessage(result):
   msg = Message(subject="Inquiry/Complaint", sender=result['email'], recipients=["mariamgamal70@gmail.com"])
   msg.body = 'from ' + result['email'] + '\n'+'Name: '+result['firstname'] +' '+result['lastname'] + '\n' 'Complaint: ' + result['complaint']
   mail.send(msg)

@app.route("/")#GET METHOD
def index():
   return render_template("index.html")

@app.route('/AdminDashboard')
def Adminhome():

    #mycursor.execute("SELECT FName FROM admin") Until we set our database
    #name=mycursor.fetchone()
 
    mydict={
      "number1":2,
      "number2":0,
      "number3":3,
      "number4":5
    }
    """
    mycursor.execute("SELECT COUNT(NurseSSN) FROM Nurse")
    x=mycursor.fetchone()
    mycursor.execute("SELECT COUNT(DoctorSSN) FROM Doctors")
    y=mycursor.fetchone()
    mycursor.execute("SELECT COUNT(ReceptionistSSN) FROM Recptionist ")
    z=mycursor.fetchone()
    mycursor.execute("SELECT COUNT(PSSN) FROM Patient ")
    p=mycursor.fetchone()
    Statistics={
      "NurseNum":x,
      "DoctorNum":y,
      "RecepNum":z,
      "PatientNum":p
    }
    """

    return render_template('/Admin/adminDashboard.html',Stats=mydict)

@app.route("/Admin_Department")
def ViewDepartmentInfo():
   return render_template('/Admin/ViewDep.html')

#Modified version for user
@app.route("/signin",methods=["POST","GET"])  # GET METHOD
def signin():
   if request.method == "POST":
      #PATIENT ONLY-----------------------------------------------------------------
      if "patient" in request.form:
         patientid = request.form["patientID"]
         patientpassword = request.form["patientpassword"]
         mycursor.execute(
             "SELECT * FROM user WHERE UserID = %s AND Password = %s", (patientid, patientpassword))
         account = mycursor.fetchone()
         if account:
            #mycursor.execute(
            #"SELECT Username FROM user WHERE UserID = %s AND Password = %s", (patientid, patientpassword))
            #patientname=mycursor.fetchone()
            session["name"] = account["Username"]
            #session["name"]=patientname        #to reference patient name   
            session["id"]=patientid
            session["Permision"]="Patient"     #Permision_level 
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
             "SELECT * FROM user WHERE UserID = %s AND Password = %s", (doctorid, doctorpassword,))
         account = mycursor.fetchone()
         if account:
            mycursor.execute(
            "SELECT Username FROM user WHERE doctorid = %s AND doctorpassword = %s", (doctorid, doctorpassword,))
            doctorname=mycursor.fetchone()
            session["name"]=doctorname
            session["id"]=doctorid
            session["Permision"]="Doctor"
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
             "SELECT * FROM user WHERE UserID = %s AND Password = %s", (nurseid, nursepassword,))
         account = mycursor.fetchone()
         if account:
            mycursor.execute(
            "SELECT Username FROM useer WHERE UserID = %s AND Password = %s", (nurseid, nursepassword,))
            nursename=mycursor.fetchone()
            session["id"]=doctorid
            session["name"]=nursename
            session["Permision"]="Nurse"
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
             "SELECT * FROM user WHERE UserID = %s AND Password = %s", (adminid, adminpassword,))
         account = mycursor.fetchone()
         if account:
            mycursor.execute(
            "SELECT Username FROM user WHERE UserID = %s AND Password = %s", (adminid, adminpassword,))
            adminname=mycursor.fetchone()
            session["id"]=adminid
            session["name"]=adminname
            session["Permision"]="Admin"
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
             "SELECT * FROM user WHERE UserID = %s AND Password = %s", (receptionistid, receptionistpassword,))
         account = mycursor.fetchone()
         if account:
            mycursor.execute(
            "SELECT Username FROM user WHERE UserID = %s AND Password = %s", (receptionistid, receptionistpassword,))
            receptionistname=mycursor.fetchone()
            session["id"]=receptionistid
            session["name"]=receptionistname
            session["Permision"]="Receptionist"
            return render_template("receptionist1.html")
         else:
            flash('ID/Password is incorrect', 'warning')
            return redirect('/signin')
      #RECEPTIONISTEND-------------------------------------------------------------------------------
   return render_template('signin.html')

"""
@app.route("/signin",methods=["POST","GET"])  # GET METHOD
def signin():
   if request.method == "POST":
      #PATIENT ONLY-----------------------------------------------------------------
      if "patient" in request.form:
         patientid = request.form["patientID"]
         patientpassword = request.form["patientpassword"]
         mycursor.execute(
             "SELECT * FROM patient_record WHERE PatientID = %s AND password = %s", (patientid, patientpassword))
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
            session["id"]=receptionistid
            return render_template("receptionist1.html")
         else:
            flash('ID/Password is incorrect', 'warning')
            return redirect('/signin')
      #RECEPTIONISTEND-------------------------------------------------------------------------------
   return render_template('signin.html')
"""

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
def nursehome():
   nurseid=session['id']
   result={}
   mycursor.execute('SELECT FirstName,LastName,Birthdate,SSN,Gender from nurse where NurseID=%s',(nurseid))
   nurse=mycursor.fetchone()
   result['nurseid']=session['id']
   result['nursename'] = nurse[0]+' '+ nurse[1]
   result['nursebirthdate']=nurse[2]
   result['nursessn']=nurse[3]
   result['nursegender']=nurse[4]
   mycursor.execute('SELECT FirstName,LastName,patientID from inpatient join nurse on nurseID=nurseID where nurseID=%s',(nurseid))
   patient=mycursor.fetchone()
   result['patientname']= patient[0]+' '+patient[1]
   result['patientid']= patient[2]
   session['patientid'] = patient[2]
   render_template('/nursehome',data=result)

@app.route("/patientrecord")
def getpatientrecord():
   mycursor.execute('SELECT RecordID,FirstName,LastName,Birthdate,Gender,SSN,Address,PhoneNumber,EmergencyContact,MedicalStatus,AdmissionReason,DateofAdmittance,MedicalDiagnosis,BedNumber,AttendingPhysicianFirstName,AttendingPhysicianLastName,AttendingPhysicianID from patient join record on SSN=PatientSSN join Doctor on AttendingPhysicianID=DoctorID where patientid=%s',(session['patientid']))
   patient=mycursor.fetchone()
   render_template('/patientrecord',data=patient)


@app.route("/patientlabsandscans", methods=["POST", "GET"])
def getpatientlabsandscans():
   if request.method == "POST":
      if "uploadlab" in request.form:
         selected_radio = request.form.get('lab')
         file=request.files['existinglab']
         if selected_radio is None or not file:
            flash('Please check the form again')
            redirect('/patientlabsandscans')
         file_contents = file.read()
         val = (selected_radio, file_contents, request.method.get(
            'dataissued'), session['patientid'])
         mycursor.execute('INSERT INTO lab(type,labfile,dateissued,patientid) values()',val )
      else:
         selected_radio = request.form.get('imaging')
         file = request.files['existing']
         if selected_radio is None or not file:
            flash('Please check the form again')
            redirect('/patientlabsandscans')
         val = (selected_radio, request.files['existinglab'], request.method.get(
            'dataissued'), session['patientid'])
         mycursor.execute(
            'INSERT INTO scan (type,labfile,dateissued,patientid) values()', val)
   mycursor.execute('SELECT Labfile,Type,DateIssued,TimeIssued from lab join patient on patientid=patientid where patientid=%s and flag=checked',(session['patientid']))
   checkedlabs=mycursor.fetchall()
   mycursor.execute(
      'SELECT labfile,Type,DateIssued,TimeIssued from lab join patient on patientid=patientid where patientid=%s and flag=pending', (session['patientid']))
   pendinglabs = mycursor.fetchall()
   mycursor.execute('SELECT labfile,Type,DateIssued,TimeIssued from lab join patient on patientid=patientid where patientid=%s and flag=pending', (session['patientid']))
   checkedimaging=mycursor.fetchall
   mycursor.execute('SELECT scanfile,Type,DateIssued,TimeIssued from scan join patient on patientid=patientid where patientid=%s and flag=pending', (session['patientid']))
   pendingimaging = mycursor.fetchall()

   render_template('/patientlabsandscans',checkedlabs=checkedlabs,pendinglabs=pendinglabs,checkedimaging=checkedimaging,pendingimaging=pendingimaging)


@app.route('/patientlabsandscans/<int:file_id>')
def viewfile(file_id):
   mycursor.execute('SELECT file from lab where id=%s',(file_id))
   file=mycursor.fetchone()
   return Response(file, mimetype='application/octet-stream')

@app.route("/dailyassessment", methods=["POST", "GET"])
def dailyassessment():
   if request.method == "POST":
      val = ((request.form.get('consciousness')),(request.form.get('pupils')), (request.form.get('skin')), (request.form.get('bloodtype')), (request.form.get('bloodpressure')), (request.form.get('bloodglucose')), (request.form.get('respiratoryrate')), (request.form.get('oxygensaturation')) , (request.form.get('heartrate')) , (request.form.get('painlevel')), (request.form.get('ivaccess')) , (request.form.get('ivaccessdate')), (request.form.get('heparin')))
      mycursor.execute('UPDATE TABLE patient SET consciousness=%s,pupils=%s,skin=%s,bloodgluecose=%s,respiratoryrate=%s,oxygensaturation=%s,heartrate=%s,painlevel=%s,ivaccess=%s,ivaccessdate=%s,heparin=%s',val)
      return redirect("/dailyassessment")
   return render_template('/dailyassessment')

@app.route('/notifications')
def notification():
   render_template('/notifcations')

@app.route("/prescriptiontable", methods=["POST", "GET"])
def prescriptiontable():
   mycursor.execute('SELECT Name,Dosage,Frequency,Noadminsetered,StartDate,EndDate from prescription join patient on patient_PSSN=PSSN where patientID=%s', (session['patientid']))
   prescriptions=mycursor.fetchall()


@app.route('/prescriptiontable/<string:medicinename>')
def prescriptiontable(medicinename):
   mycursor.execute('SELECT Noadminsetered from prescription where Name=%s', (medicinename))
   noadminster=mycursor.fetchone()
   if request.method == "POST":
      checkedboxes = request.form.getlist('checklist')
      counter = 0
      for checked in checkedboxes:
         counter += 1
         noadminster = noadminster-counter
         mycursor.execute('UPDATE TABLE prescription SET Noadminsetered=noadminster where Name=%s', (medicinename))
   return render_template('/prescriptiontable/<string:medicinename>', number=noadminster,name=medicinename)


@app.route("/logout")
def LogOut():
   session.pop("id",None)
   session.pop("name",None) 
   session.pop("Permission",None)
   return redirect(url_for('/'))

if __name__ == "__main__":
   app.run(debug=True)
   #socketio.run(app, debug=True)
