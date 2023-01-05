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
    password="lovelygirl12",
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

    # mycursor.execute("SELECT FName FROM admin") Until we set our database
    # name=mycursor.fetchone()

    mydict = {
        "number1": 2,
        "number2": 0,
        "number3": 3,
        "number4": 5
    }

    mycursor.execute("SELECT COUNT(Nurse_SSN) FROM Nurse")
    n = mycursor.fetchone()[0]
    print(n)
    mycursor.execute("SELECT COUNT(DoctorSSN) FROM Doctor")
    d = mycursor.fetchone()[0]
    mycursor.execute("SELECT COUNT(Receptionist_SSN) FROM Receptionist ")
    r = mycursor.fetchone()[0]
    mycursor.execute("SELECT COUNT(PSSN) FROM Patient ")
    p = mycursor.fetchone()[0]
    mycursor.execute("SELECT COUNT(BedID) FROM Beds")
    b = mycursor.fetchone()[0]
    mycursor.execute("SELECT COUNT(RoomNumber) FROM Unit_Rooms")
    U = mycursor.fetchone()[0]
    mycursor.execute("SELECT SUM(TotalValue) FROM Bills")
    V = mycursor.fetchone()[0]

    Statistics = {
        "NurseNum": n,  # Number of nurses in ICU
        "DoctorNum": d,  # Number of doctors in ICU
        "RecepNum": r,  # Number of Receptionists in ICU
        "PatientNum": p,  # Number of Patients in ICU
        "BedNum": b,  # Number of Beds in ICU
        "RoomNum": U,  # Number of Rooms in ICU
        "ICUIncome": V  # Income of ICU

    }

    return render_template('/Admin/adminDashboard.html', Stats=Statistics)


@app.route('/AdminDr', methods=["GET", "POST"])
def AdminDr():
    if request.method == "GET":

        mycursor.execute(
            "SELECT Doctor_ID,Fname,Lname,Sex,(SELECT TIMESTAMPDIFF(YEAR, Birthdate, CURDATE()) AS Age FROM doctor),Speciality,StartShift,EndShift FROM doctor")
    # row_headers = [x[0] for x in mycursor.description]
    doctors_data = mycursor.fetchall()
    Dr_Data = {
        # 'header': row_headers,
        'records': doctors_data

    }

    return render_template("/Admin/AdminDr.html", Doc_data=Dr_Data)


@app.route('/Admin_Add_Dr', methods=["POST", "GET"])
def Admin_Add_Dr():

    if request.method == "GET":
        mycursor.execute("SELECT PSSN FROM patient")
        PatientSSn = mycursor.fetchall()
        mycursor.execute("SELECT PatientID FROM patient")
        Patientid = mycursor.fetchall()
        patientdata = {
            'ssn': PatientSSn,
            'id': Patientid
        }

        return render_template("/Admin/Admin_Add_Dr.html", Patient_data=patientdata)

    elif request.method == "POST":
        FirstName = request.form.get('FirstName')
        Password = request.form.get('password')
        Experience = request.form.get('Experience')
        LastName = request.form.get('LastName')
        Gender = request.form.get('gender')
        Salary = request.form.get('Salary')
        DoctorID = request.form.get('DoctorID')
        SSN = request.form.get('ssn')
        formatted_date = request.form.get('Birthdate')  # add age
        Speciality = request.form.get('Speciality')
        Address = request.form.get('Address')
        Email = request.form.get('Email')
        PhoneNumber = request.form.get('PhoneNumber')
        # AssignedPatientSSN = request.form.get('patientssn')
        # AssignedPatientID = request.form.get('patientid')

    try:
        sql = "INSERT INTO doctor(DoctorSSN,Doctor_ID,FName,Lname,email,Sex,Birthdate, Phone, Address, Speciality, Experience,Salary) VALUES(%s, %s, %s, %s, %s, %s, %s, %s,%s,%s,%s,%s)"
        val = (SSN, DoctorID, FirstName, LastName, Email, Gender,
               formatted_date, PhoneNumber, Address, Speciality, Experience, Salary)
        mycursor.execute(sql, val)
        sql = "INSERT INTO user(UserID,Username,Password,Permission,email,Doctor_DoctorSSN)"
        val = (DoctorID, FirstName, Password, "Doctor", Email, SSN)
        mycursor.execute(sql, val)
        """
        if AssignedPatientSSN!=None and AssignedPatientID!=None:
            sql="INSERT INTO patient(AssignedDrSSN) WHERE PSSN=%s and PatientID=%s "
            val=(AssignedPatientSSN,AssignedPatientID)
            mycursor.execute(sql,val)
            """
        mydb.commit()

        return redirect(url_for('AdminDr'))

    except:
        return redirect(url_for('Admin_Add_Dr'))


######################################### ---ADMINEND---#################################################

######################################### ---INDEXSTART---#################################################
# Modified version for user

@app.route("/signin", methods=["POST", "GET"])  # GET METHOD
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
def nursehome():
    # nurseid = #session['id']
    result = {}
    mycursor.execute(
        'SELECT nurse.FName,LName,TIMESTAMPDIFF(YEAR, Birthdate, CURDATE()) AS age ,Nurse_SSN,Sex from nurse where NurseID=%s', ([1]))
    nurse = mycursor.fetchone()
    #  result['nurseid'] = session['id']
    #  result['nursename'] = nurse[0]+' ' + nurse[1]
    #  result['nursebirthdate'] = nurse[2]
    #  result['nursessn'] = nurse[3]
    #  result['nursegender'] = nurse[4]
    mycursor.execute(
        'SELECT patient.FName,patient.LName,PatientID from patient join  nurse on AssignedNurseSSN=Nurse_SSN where NurseID=%s', ([1]))
    patient = mycursor.fetchone()
    # result['patientname'] = patient[0]+' '+patient[1]
    # result['patientid'] = patient[2]
    # [1] = patient[2]
    return render_template('/nurse/nursehome.html', nurseid=1, nurse=nurse, patient=patient)


@app.route("/patientrecord", methods=["POST", "GET"])
def patientrecord():
    mycursor.execute(
        'SELECT RecordID,patient.FName,patient.LName,TIMESTAMPDIFF(YEAR,patient.Birthdate,CURDATE()),patient.Sex,patient.Emergency_Contact,MedicalStatus,MedicalHistory,Blood_Group,Level_of_consiousness,pupils,skin,BloodPressure,BloodGlucose,RespiratoryRate,OxygenSaturation,PulseRateMin,IV_Access,IV_Acess_Date,Takes_Heparin,MedicalDiagnosis,Admission_Reasoning,Date_Admitted,Beds_BedID,doctor.Fname,doctor.LName,Doctor_ID,patientID from patient join patientrecord on Patient_PSSN=PSSN join Doctor on AssignedDrSSN=DoctorSSN where PatientID=%s', ([1]))
    patients = mycursor.fetchone()
    return render_template('/nurse/patientrecord.html', patient=patients)


@app.route("/patientlabsandscans", methods=["POST", "GET"])
def getpatientlabsandscans():
    if request.method == "POST":
        if "uploadlab" in request.form:
            selected_radio = request.form.get('lab')
            file = request.files['existinglab']
            if selected_radio is None:
                flash('Please check the form again')
                redirect('/patientlabsandscans')
            file_contents = file.read()
            val = (selected_radio, file_contents,
                   request.form.get('dataissued'), 1)
            mycursor.execute(
                "INSERT INTO labresults (Type, LabResult, DateIssued, Patient_PSSN,Flag) VALUES (%s, %s, %s, (SELECT PSSN FROM patient WHERE PatientID=%s),'Checked')", val)
            mydb.commit()
            return redirect('/patientlabsandscans')
        elif "uploadimaging" in request.form:
            selected_radio = request.form.get('imaging')
            file = request.files['existingimaging']
            file_contents = file.read()
            if selected_radio is None:
                flash('Please check the form again')
                redirect('/patientlabsandscans')
            val = ((selected_radio, file_contents,
                   request.form.get('dataissued')), 1)
            mycursor.execute(
                'INSERT INTO patientscans (Type,LabResult,DateIssued) VALUES (%s, %s, %s, (SELECT PSSN FROM patient WHERE PatientID=%s))', val)
            mydb.commit()
            redirect('/patientlabsandscans')
    mycursor.execute(
        "SELECT LabResultID,LabResult,Type,DateIssued from labresults join patient on Patient_PSSN=PSSN where PatientID=%s and Flag='Checked'", ([1]))
    checkedlabs = mycursor.fetchall()
    mycursor.execute(
        "SELECT LabResultID,LabResult,Type,DateIssued from labresults join patient on Patient_PSSN=PSSN where PatientID=%s and Flag='Pending'", ([1]))
    pendinglabs = mycursor.fetchall()
    mycursor.execute(
        "SELECT PatientScanID,PatientScans,Type,DataIssued from patientscans join patient on Patient_PSSN=PSSN where PatientID=%s and Flag='Checked'", ([1]))
    checkedimaging = mycursor.fetchall()
    mycursor.execute(
        "SELECT PatientScanID,PatientScans,Type,DataIssued from patientscans join patient on Patient_PSSN=PSSN where PatientID=%s and Flag='Pending'", ([1]))
    pendingimaging = mycursor.fetchall()
    return render_template('/nurse/patientlabsandscans.html', checkedlabs=checkedlabs, pendinglabs=pendinglabs, checkedimaging=checkedimaging, pendingimaging=pendingimaging)


@app.route('/patientlabsandscans/<int:file_id>')
def viewfile(file_id):
    mycursor.execute(
        'SELECT LabResult from labresults where LabResultID=%s', ([file_id]))
    file = mycursor.fetchone()
    return Response(file, mimetype='application/octet-stream')


@app.route("/dailyassessment/<int:patient_id>", methods=["POST", "GET"])
def dailyassessment(patient_id):
    if request.method == "POST":
        val = ((request.form.get('consciousness')), (request.form.get('pupils')), (request.form.get('skin')), (request.form.get('bloodtype')), (request.form.get('bloodpressure')), (request.form.get('bloodglucose')), (request.form.get(
            'respiratoryrate')), (request.form.get('oxygensaturation')), (request.form.get('heartrate')), (request.form.get('painlevel')), (request.form.get('ivaccess')), (request.form.get('ivaccessdate')), (request.form.get('heparin')))
        mycursor.execute('UPDATE TABLE patient SET Level_of_consciousness=%s,pupils=%s,skin=%s,BloodGlucose=%s,Respiratoryrate=%s,OxygenSaturation=%s,PulseRateMin=%s,PainLevel=%s,IV_Access=%s,IV_Acess_date=%s,Takes_Heparin=%s', val)
        return redirect("/dailyassessment/<int:patient_id>")
    return render_template('dailyassessment.html')


@app.route("/prescriptiontable", methods=["POST", "GET"])
def prescriptiontable():
    mycursor.execute(
        'SELECT medicine_id,medicine_name,Dosage,Frequency,COUNT(timestamp)as Noadmisntered,StartDate,EndDate from prescribed_medication join patient on patient_PSSN=PSSN join medicine_prescription_timestamps on medicine_id= medicine_prescription_id group by medicine_id where patientID=%s', ([1]))
    # TRANSFORMED LIST OF TUPLES INTO DICTIONARY VV ACCESSED BY KEYWORDS
#    columns = [col[0] for col in mycursor.description]
#    result = [dict(zip(columns, row)) for row in mycursor.fetchall()]
    # RETURNS LIST OF TUPLES, TUPLES ARE ACCESSED USING INDEXES
    prescriptions = mycursor.fetchall()
    return render_template('prescriptiontable.html', prescriptions=prescriptions)


@app.route('/administer_in_prescription_table/<int:medicineid>')
def administer_in_prescription_table(medicineid):
    mycursor.execute(
        'INSERT INTO medicine_prescription_timestamps (medicine_prescription_id, timestamp) values(%s, CURRENT_TIMESTAMP)', (medicineid))
    mydb.commit()
    return render_template('prescriptiontable.html')


@app.route('/prescriptiontimestamps/<int:medicineid>')
def prescriptiontimestamps(medicineid):
    mycursor.execute('SELECT COUNT(timestamp),medicine_prescription_id,medicine_name,timestamp from medicine_prescription_timestamps join prescribed_medicine on medicine_prescription_id=medicine_id WHERE medicine_prescription_id=%s GROUP BY medicine_prescription_id', (medicineid))
    rows = mycursor.fetchall()
    columns = [col[0] for col in mycursor.description]
    medicinetimestamps = [dict(zip(columns, row)) for row in rows]
    return render_template('prescriptiontimestamps.html', medicinetimestamps=medicinetimestamps)


@app.route('/nursenotifications')
def notification():
    return render_template('nursenotifcations.html')


@app.context_processor
def inject_notification_count():
    return countnotification()

###################################################### Patient Page ############################################
#Age
@app.route('/patient_homepage')
def patientRecord():
#    patientid=session['id']
   result={}
   mycursor.execute('SELECT FName,MName,LName,Sex,PSSN,Address,email,Phone,Emergency_Contact,Birthdate,Insurance_Status,PatientID from patient join patientrecord on PSSN=Patient_PSSN where patientid=%s',([1]))
   patient=mycursor.fetchone()
   result['patientname'] = patient[0]+' '+patient[1]+' '+patient[2]
   result['patientsex']=patient[3]
   result['patientssn']=patient[4]
   result['patientaddress']=patient[5]
   result['patientemail']=patient[6]
   result['patientphone']=patient[7]
   result['patientemergencycontact']=patient[8]
   result['patientbirthdate']=patient[9]
   result['patientinsurance']=patient[10]
   result['patientid']=patient[11]
   mycursor.execute('SELECT TIMESTAMPDIFF (YEAR, Birthdate, CURDATE()) from patient AS age')
   patient=mycursor.fetchone()
   result['patientage']=patient[0]
   return render_template('/Patient/patient_homepage.html',data=result)

#edit sum and groupby 
@app.route('/patient_icuinfo')
def ICUInfo():
   mycursor.execute('SELECT Date_Admitted,Date_Discharged,Doctor.Fname,Doctor.Lname,Nurse.Fname,Nurse.Lname,MedicalDiagnosis,Bills_ID,TotalValue,Insurance_Percent,SUM(Price_Day),SUM(Price) from patient join prescribed_medication on PSSN=Patient_PSSN join bills on PSSN=bills.Patient_PSSN join beds on Beds_BedID=BedID join patientrecord on PSSN=patientrecord.Patient_PSSN join Doctor on AssignedDrSSN=DoctorSSN join Nurse on AssignedNurseSSN=Nurse_SSN where patientid=%s' ,([1]))
   patient=mycursor.fetchone()
   mycursor.execute('SELECT medicine_name,Dosage,Frequency,StartDate,EndDate,Specifications from patient join prescribed_medication on PSSN=Patient_PSSN where PatientID=%s' ,([1]))
   medicine=mycursor.fetchone()
   return render_template('/Patient/patient_icuinfo.html',data=patient,medicine=medicine)

# ###################################################### Receptionist Page ############################################
@app.route('/receptionist_viewrecord')
def R_ViewRecord():
#   patientid=session['id']
   result={}
   mycursor.execute('SELECT patient.FName,patient.MName,patient.LName,patient.Sex,PSSN,patient.Address,patient.email,patient.Phone,patient.Emergency_Contact,patient.Birthdate,Insurance_Status,PatientID,Doctor.Fname,Doctor.Lname,Nurse.Fname,Nurse.Lname,RecordID from patient join patientrecord on PSSN=Patient_PSSN join Doctor on AssignedDrSSN=DoctorSSN join Nurse on AssignedNurseSSN=Nurse_SSN where patientid=%s' ,([1]))
   patient=mycursor.fetchone()
   result['patientname'] = patient[0]+' '+patient[1]+' '+patient[2]
   result['patientsex']=patient[3]
   result['patientssn']=patient[4]
   result['patientaddress']=patient[5]
   result['patientemail']=patient[6]
   result['patientphone']=patient[7]
   result['patientemergencycontact']=patient[8]
   result['patientbirthdate']=patient[9]
   result['patientinsurance']=patient[10]
   result['patientid']=patient[11]
   result['assigneddoctor']=patient[12]+' '+patient[13]
   result['assignednurse']=patient[14]+' '+patient[15]
   result['recordid']=patient[16]
   mycursor.execute('SELECT TIMESTAMPDIFF (YEAR, Birthdate, CURDATE()) from patient AS age')
   patient=mycursor.fetchone()
   result['patientage']=patient[0]
   return render_template('receptionist/receptionist_viewrecord.html',data=result)

@app.route('/receptionist_homepage')
def receptionistHome():
   result={}
   mycursor.execute('SELECT Fname,Lname,Receptionist_SSN,Sex,ReceptionistID from receptionist where receptionistID=%s',([123]))
   receptionist=mycursor.fetchone()
   result['receptionistid']=receptionist[4]
   result['receptionistname'] = receptionist[0]+' '+receptionist[1]
   result['receptionistfirstname'] = receptionist[0]
   result['receptionistssn']=receptionist[2]
   result['receptionistgender']=receptionist[3]
   mycursor.execute('SELECT TIMESTAMPDIFF (YEAR, Birthdate, CURDATE()) from receptionist AS age')
   receptionist=mycursor.fetchone()
   result['receptionistage']=receptionist[0]
   return render_template('receptionist/receptionist_homepage.html',data=result)

        # data = {
        #     'message': "Data retrieved",
        #     'recordinfo': recordinfo
        #  }
        # mycursor.execute(
        #     "SELECT FirstName FROM from patient join patientrecord on PSSN=Patient_PSSN And ReportID=%s", (ReportID))
        # patient = mycursor.fetchone()
        # FirstName = patient[0]
        # mycursor.execute(
        #     "SELECT LastName from patient join patientrecord on PSSN=Patient_PSSN AND ReportID=%s", (ReportID))
        # patient = mycursor.fetchone()
        # LastName = patient[0]
        # mycursor.execute("SELECT Date_Admitted FROM from patient join record on PSSN=PatientSSN AND ReportID=%s", (ReportID))
        # patient = mycursor.fetchone()
        # Date_Admitted = patient[0]
@app.route('/receptionist_managerecords', methods=["POST", "GET"])
def manage_records():
       if request.method == 'POST':
        ReportID = request.form.get['ReportID']
        mycursor.execute("SELECT RecordID,FName,LName,Date_Admitted from patient join patientrecord on PSSN=Patient_PSSN WHERE ReportID=%s", (ReportID))
        recordinfo = mycursor.fetchall()
        data = {
            'recordinfo': recordinfo
         }
        return render_template('/receptionist/receptionist_managerecords.html', data=data)
       else:
         mycursor.execute("SELECT RecordID,FName,LName,Date_Admitted from patient join patientrecord on PSSN=Patient_PSSN WHERE PatientID=%s", ([1]))
         recordinfo=mycursor.fetchall()
         data = {
            'recordinfo': recordinfo
         }
         return render_template('/receptionist/receptionist_managerecords.html',data=data)


@app.route('/receptionist_editrecord/<int:id>',methods=['POST', 'GET'])
def editRecord(id):
   if request.method == 'POST':
      FirstName = request.form.get('FirstName')
      MiddleName = request.form.get('MiddleName')
      LastName = request.form.get('LastName')
      Gender = request.form.get('Gender')
      RecordID = request.form.get('RecordID')
      PatientID = request.form.get('PatientID')
      SSN = request.form.get('SSN')
      formatted_date = request.form.get('Birthdate')  
      Insurance = request.form.get('insurance')
      Address = request.form.get('Address')
      Email = request.form.get('email')
      PhoneNumber = request.form.get('PhoneNumber')
      EmergencyContact = request.form.get('emergencyPhoneNumber')
      AssignedDoctorSSN = request.form.get('doctorssn')
      AssignedNurseSSN = request.form.get('nursessn')
      val1 = ((FirstName),(MiddleName), (LastName),(Gender), (PatientID),(SSN),(formatted_date), (Address), (Email),(PhoneNumber),(EmergencyContact),(AssignedDoctorSSN),(AssignedNurseSSN),(1))
      mycursor.execute('UPDATE patient SET FName=%s,MName=%s,LName=%s,Sex=%s,PatientID=%s,PSSN=%s,Birthdate=%s,Address=%s,email=%s,Phone=%s,Emergency_Contact=%s,AssignedDrSSN=%s,AssignedNurseSSN=%s WHERE PatientID=%s',  val1) 
      val2 = ((RecordID),(Insurance),(SSN))
      mycursor.execute('UPDATE patientrecord SET RecordID=%s,Insurance_Status=%s,Patient_Pssn=%s', val2) 
      mydb.commit()
    #   return redirect("/receptionist/receptionist_viewrecord")
      return render_template('/receptionist/receptionist_editrecord.html')
   else:
      mycursor.execute('SELECT patient.FName,patient.MName,patient.LName,patient.Sex,PatientID,PSSN,patient.Birthdate,patient.Address,patient.email,patient.Phone,patient.Emergency_Contact,AssignedDrSSN,AssignedNurseSSN,RecordID,Insurance_Status from patient join patientrecord on PSSN=Patient_PSSN join Doctor on AssignedDrSSN=DoctorSSN join Nurse on AssignedNurseSSN=Nurse_SSN where PatientID=%s' ,([1]))
      patient=mycursor.fetchone()
      return render_template('/receptionist/receptionist_editrecord.html',data=patient)

@app.route('/receptionist_addrecord', methods=['POST', 'GET'])
def R_AddRecord():
   if request.method == 'GET':
      mycursor.execute('SELECT DoctorSSN from Doctor')
      doctors=mycursor.fetchall()
      mycursor.execute('SELECT Nurse_SSN from Nurse')
      nurses=mycursor.fetchall()
      data={
            'doctorssn':doctors,
            'nursessn':nurses
      }
      return render_template('/receptionist/receptionist_addrecord.html',data=data)
   else:
      FirstName = request.form.get('FirstName')
      MiddleName = request.form.get('MiddleName')
      LastName = request.form.get('LastName')
      Gender = request.form.get('Gender')
      RecordID = request.form.get('RecordID')
      PatientID = request.form.get('PatientID')
      SSN = request.form.get('SSN')
      formatted_date = request.form.get('Birthdate')  
      Insurance = request.form.get('insurance')
      Address = request.form.get('Address')
      Email = request.form.get('email')
      PhoneNumber = request.form.get('PhoneNumber')
      EmergencyContact = request.form.get('emergencyPhoneNumber')
      AssignedDoctorSSN = request.form.get('doctorssn')
      AssignedNurseSSN = request.form.get('nursessn')
      sql = "INSERT INTO Patient(patient.FName,patient.MName,patient.LName,patient.Sex,PatientID,PSSN,patient.Birthdate,patient.Address,patient.email,patient.Phone,patient.Emergency_Contact,AssignedDrSSN,AssignedNurseSSN) VALUES(%s, %s, %s, %s, %s, %s,%s,%s,%s,%s,%s,%s,%s)"
      val = (FirstName, MiddleName, LastName, Gender, PatientID,SSN,formatted_date, Address, Email,PhoneNumber,EmergencyContact,AssignedDoctorSSN,AssignedNurseSSN)
      mycursor.execute(sql, val)
      sql2 = "INSERT INTO patientrecord(RecordID,Insurance_Status,Patient_Pssn) VALUES(%s, %s,%s)"
      val2 = (RecordID,Insurance,SSN)
      mycursor.execute(sql2, val2)
      mydb.commit()
      return render_template('/receptionist/receptionist_addrecord.html')
      
      #, message=FirstName + ' ' + LastName+" has been successfully added to the database")
    #   except:
    #         return redirect(url_for('receptionist_addrecord'), error="Invalid input!")
#####################################################Run#############################################################
if __name__ == "__main__":
   app.run(debug=True)
   #socketio.run(app, debug=True)
