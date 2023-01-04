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
   password="mysql",
   database="icu_management_last"
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

notifications={}
notificationcounter=0
def updatenotifications(notification):
   notificationcounter = notificationcounter+1
   notifications['count'] = notificationcounter
   notifications['typeofnotification']=notification
   


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
   result['patientname']= patient[0] + patient[1]
   result['patientid']= patient[2]
   session['patientid'] = patient[2]
   render_template('/nursehome',data=result)


@app.route("/Doctor_home")
def getdoctordata():  
   #doctorid = session["id"]
   result = {}
   mycursor.execute("SELECT Fname, Lname, Birthdate, DoctorSSN, Sex, Doctor_ID from doctor where Doctor_ID = %s",([1]))
   doctor = mycursor.fetchone()
   result['doctorid'] = doctor[5]
   result['doctorname'] = doctor[0] + doctor[1]
   result['doctorbirthdate'] = doctor[2]
   result['doctorssn'] = doctor[3]
   result['doctorgender'] = doctor[4]
   mycursor.execute('SELECT COUNT(PSSN) from patient join doctor on AssignedDrSSN = DoctorSSN where doctor_ID = %s',([1]))#(doctorid)))
   count = mycursor.fetchone()
   result['patientsnumber'] = count[0]
   mycursor.execute('SELECT TIMESTAMPDIFF (YEAR, Birthdate, CURDATE()) from doctor AS age')
   doctora=mycursor.fetchone()
   result['doctorage'] = doctora[0]

   return render_template('/Doctor/Doctor_home.html', data = result)




@app.route("/patientrecord_doctor")
def getpatientrecord():
   mycursor.execute('SELECT RecordID, patient.FName,patient.LName,TIMESTAMPDIFF(YEAR, patient.Birthdate, CURDATE()),patient.Sex,patient.Emergency_Contact,MedicalStatus,MedicalHistory,Blood_Group,Level_of_consiousness,Pupils,Skin,BloodPressure,BloodGlucose,RespiratoryRate,OxygenSaturation,PulseRateMin,IV_Access,IV_Acess_Date,Takes_Heparin,MedicalDiagnosis,Admission_Reasoning,Date_Admitted,Beds_BedID,doctor.Fname,doctor.Lname,Doctor_ID,PatientID from patient join patientrecord on Patient_PSSN=PSSN join Doctor on AssignedDrSSN=DoctorSSN where PatientID=%s', ([1]))
   patient = mycursor.fetchone()
   mycursor.execute('SELECT medicine_name,Dosage,Frequency,StartDate,EndDate,Specifications from patient join prescribed_medication on PSSN=Patient_PSSN where patientid=%s' ,([1]))
   medicine=mycursor.fetchone()
   return render_template('/Doctor/patientrecord_doctor.html', patient=patient, medicine = medicine)
  






# @app.route("/viewpatientrecord")
# def getpatientrecord():
#    mycursor.execute('SELECT RecordID,FirstName,LastName,Birthdate,Gender,SSN,Address,PhoneNumber,EmergencyContact,MedicalStatus,AdmissionReason,DateofAdmittance,MedicalDiagnosis,BedNumber,AttendingPhysicianFirstName,AttendingPhysicianLastName,AttendingPhysicianID from patient join record on SSN=PatientSSN join Doctor on AttendingPhysicianID=DoctorID where patientid=%s',(session['patientid']))
#    patient=mycursor.fetchone()
#    render_template('/viewpatientrecord',data=patient)


@app.route('/receptionist_homepage')
def receptionistHomePage():
   # receptionistid=session['id']
   result={}
   mycursor.execute('SELECT Fname,Lname,Receptionist_SSN,Sex,ReceptionistID from receptionist where receptionistID=%s',([39]))
   receptionist=mycursor.fetchone()
   result['receptionistid']=receptionist[4]  #session['id']
   result['receptionistname'] = receptionist[0] + receptionist[1]
   result['receptionistfirstname'] = receptionist[0]
   result['receptionistssn']=receptionist[2]
   result['receptionistgender']=receptionist[3]
   mycursor.execute('SELECT TIMESTAMPDIFF (YEAR, Birthdate, CURDATE()) from receptionist AS age')
   receptionist=mycursor.fetchone()
   result['receptionistage']=receptionist[0]
   return render_template('/receptionist/receptionist_homepage.html.html',data=result)
   

@app.route("/patientrecord_doctor/<int:file_id>", methods=["POST", "GET"])
def admit(file_id):
   if request.method == "POST":
      if "request" in request.form:
         val = ((request.form.get("bID")), (request.form.get("admitdate")))
         mycursor.execute('UPDATE patient SET Beds_BedID =%s, Date_Admitted = %s' , val)
         mycursor.execute('UPDATE patientrecord SET Admission_Reasoning = %s', [request.form.get("reason")])

      elif "request2" in request.form:
         amin = request.form.getlist("sc")
         str1 = ','.join(amin)
         mycursor.execute('SELECT PatientID, PSSN from patient join patientrecord on PSSN = Patient_PSSN')
         patient = mycursor.fetchone()
         mycursor.execute("INSERT INTO patientscans (PatientScanID, Patient_PSSN,Type) VALUES (%s,%s,%s)", [patient[0], patient[1], str1])

      elif "request1" in request.form:
         amin = request.form.getlist("sc")
         str1 = ','.join(amin)
         mycursor.execute('SELECT PatientID, PSSN from patient join patientrecord on PSSN = Patient_PSSN')
         patient = mycursor.fetchone()
         mycursor.execute("INSERT INTO patientscans (PatientScanID, Patient_PSSN,Type) VALUES (%s,%s,%s)", [patient[0], patient[1], str1])
         # mycursor.execute("INSERT INTO patientscans (Type) VALUES (%s)",[str1])
        

      return redirect("/patientrecord_doctor")
   return render_template('/Doctor/patientrecord_doctor.html')


@app.route("/logout")
def LogOut():
   session.pop("id",None)
   session.pop("name",None) 
   session.pop("Permission",None)
   return redirect(url_for('/'))

if __name__ == "__main__":
   app.run(debug=True)
   #socketio.run(app, debug=True)
