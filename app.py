from flask import Flask, render_template, redirect, url_for, request,session,flash
from flask_session import Session
import mysql.connector
from flask_mail import Mail, Message
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
now = datetime.now()
formatted_date = now.strftime('%Y-%d-%m %H:%M:%S')

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
   password="adanGneCUFE2025$",
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





####################################################Admin##################################

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

###############################################Index####################################

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
            mycursor.execute(
            "SELECT Username FROM user WHERE UserID = %s AND Password = %s", (patientid, patientpassword))
            patientname=mycursor.fetchone()
            session["name"]=patientname        #to reference patient name   
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

################################################Nurse Page############################################3
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
   session['patientid'] = patient[2]
   render_template('/nursehome',data=result)

@app.route("/viewpatientrecord")
def getpatientrecord():
   mycursor.execute('SELECT RecordID,FirstName,LastName,Birthdate,Gender,SSN,Address,PhoneNumber,EmergencyContact,MedicalStatus,AdmissionReason,DateofAdmittance,MedicalDiagnosis,BedNumber,AttendingPhysicianFirstName,AttendingPhysicianLastName,AttendingPhysicianID from patient join record on SSN=PatientSSN join Doctor on AttendingPhysicianID=DoctorID where patientid=%s',(session['patientid']))
   patient=mycursor.fetchone()
   render_template('/viewpatientrecord',data=patient)
##############################################sidebar#####################################
@app.route("/logout")
def LogOut():
   session.pop("id",None)
   session.pop("name",None) 
   session.pop("Permission",None)
   return redirect(url_for('/'))
###################################################### Patient Page ############################################
#Age
@app.route("/patient/homepage")
def PatientRecord():
    mycursor.execute('SELECT FirstName,MiddleName,LastName,Birthdate,Gender,PSSN,Address,email,PhoneNumber,EmergencyContact,PatientID,Insurance_Status from patient join record on PSSN=PatientSSN where patientid=%s',(session['patientid']))
    patient=mycursor.fetchone()
    render_template('/patient/homepage',data=patient)

#edit sum and groupby 
@app.route("/patient/icuinfo")
def ICUInfo():
    mycursor.execute('SELECT Date_Admitted,Date_Discharged,AttendingPhysicianFirstName,AttendingPhysicianLastName,AttendingPhysicianFirstName,AttendingNurseLastName,Diagnosis,Bills_ID,TotalValue,Insurance_Percent,Price,Specifications,Frequency,Dosage,StartDate,EndDate from patient join Prescribed_Medication on PSSN=Patient_PSSN join bills on PSSN=Patient_PSSN join beds on Beds_BedID=BedID join record on SSN=PatientSSN join Doctor on AttendingPhysicianID=DoctorID join Nurse on AttendingNurseID=NurseID where patientid=%s',(session['patientid']))
    patient=mycursor.fetchone()
    render_template('/patient/icuinfo',data=patient)

###################################################### Receptionist Page ############################################
@app.route("/receptionist/viewrecord")
def R_ViewRecord():
    mycursor.execute('SELECT FirstName,MiddleName,LastName,Birthdate,Gender,PSSN,Address,email,PhoneNumber,EmergencyContact,PatientID,Insurance_Status,AttendingPhysicianFirstName,AttendingPhysicianLastName,AttendingPhysicianFirstName,AttendingNurseLastName from patient join record on PSSN=PatientSSN join Doctor on AttendingPhysicianID=DoctorID join Nurse on AttendingNurseID=NurseID where patientid=%s',(session['patientid']))
    patient=mycursor.fetchone()
    render_template('/receptionist/viewrecord',data=patient)

@app.route("/receptionist/homepage", methods=["POST", "GET"])
def ReceptionistHomePage():
   receptionistid=session['id']
   result={}
   mycursor.execute('SELECT FirstName,LastName,Birthdate,SSN,Gender from receptionist where receptionistID=%s',(receptionistid))
   receptionist=mycursor.fetchone()
   result['receptionistid']=session['id']
   result['receptionistname'] = receptionist[0] + receptionist[1]
   result['receptionistbirthdate']=receptionist[2]                         #age
   result['receptionistssn']=receptionist[3]
   result['receptionistgender']=receptionist[4]
   render_template('/receptionist/homepage',data=result)

@app.route('/receptionist/addrecord', methods=['POST', 'GET'])
def R_AddRecord():
    if request.method == 'POST':
        FirstName = request.form.get('FirstName')
        MiddleName = request.form.get('MiddleName')
        LastName = request.form.get('LastName')
        Gender = request.form.get('Gender')
        RecordID = request.form.get('RecordID')
        PatientID = request.form.get('PatientID')
        SSN = request.form.get('SSN')
        formatted_date = request.form.get('Birthdate')  #add age
        Insurance = request.form.get('Insurance')
        Address = request.form.get('Address')
        Email = request.form.get('Email')
        PhoneNumber = request.form.get('PhoneNumber')
        EmergencyContact = request.form.get('PhoneNumber')
        AssignedDoctor = request.form.get('AssignedDoctor')
        AssignedNurse = request.form.get('AssignedNurse')
        try:
            sql = "INSERT INTO Patient(PSSN,FirstName, MiddleName, LastName,PatientID, Sex, Birthdate,Address, Email, PhoneNumber,EmergencyContact,AssignedDoctor,AssignedNurse) VALUES(%s, %s, %s, %s, %s, %s, %s, %s,%s,%s,%s,%s,%s)"
            val = (SSN, FirstName, MiddleName, LastName, PatientID,Gender,
                   formatted_date, Address, Email,PhoneNumber,EmergencyContact,AssignedDoctor,AssignedNurse)
            mycursor.execute(sql, val)
            sql = "INSERT INTO PatientRecord(RecordID,Insurance_Status) VALUES(%s, %s)"
            val = (RecordID,Insurance)
            mydb.commit()
            return render_template('/receptionist/managerecords.html', message=FirstName + ' ' + LastName+" has been successfully added to the database")
        except:
            return render_template('/receptionist/addrecord.html', error="Invalid input!")

    else:
        return render_template('/receptionist/addrecord.html')

#####################################################Run#############################################################

if __name__ == "__main__":
   app.run(debug=True)
   #socketio.run(app, debug=True)
