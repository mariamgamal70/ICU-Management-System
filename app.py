from flask import Flask, render_template, redirect, url_for, request,session,flash,Response
from flask_session import Session
import mysql.connector
from flask_mail import Mail, Message
# from flask_socketio import SocketIO



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
    database="icu_management_finalll"
)
mycursor = mydb.cursor()
#GET used when no info is sent(written in URL) , POST is used when info is sent(Ex:Sensitive info)(not written in URL)
#get function route("route)
#functions are GET only by default, to make it GET and POST , u should define it as a parameter in route
#route("route",methods=["POST","GET"])
# in case it is GET and POST you should check inside the function whether the incoming is a get or post request , if its a get ,return template, if its a post , send data do changes


# def countnotification():
#     messages = get_flashed_messages()
#     message_count = len(messages)
#     return {'notification_count': message_count}


# def notifynurse(notification):
#     string = notification['type']+'\n'+notification['info']
#     flash(string, 'warning')


def sendmessage(result):
   msg = Message(subject="Inquiry/Complaint", sender=result['email'], recipients=["mariamgamal70@gmail.com"])
   msg.body = 'from ' + result['email'] + '\n'+'Name: '+result['firstname'] +' '+result['lastname'] + '\n' 'Complaint: ' + result['complaint']
   mail.send(msg)

# notifications={}
# notificationcounter=0
# def updatenotifications(notification):
#    notificationcounter = notificationcounter+1
#    notifications['count'] = notificationcounter
#    notifications['typeofnotification']=notification
   


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


@app.route('/AdminDr',methods=["GET"])
def AdminDr():
    if request.method=="GET":
        mycursor.execute("SELECT Doctor_ID,Fname,Lname,Sex, TIMESTAMPDIFF(YEAR, Birthdate, CURDATE()) AS Age,Speciality,StartShift,EndShift FROM doctor ORDER BY Doctor_ID ")
    #row_headers = [x[0] for x in mycursor.description]
    doctors_data = mycursor.fetchall()
    Dr_Data = {
    'records': doctors_data
    }
    return render_template("/Admin/AdminDr.html", Doc_data=Dr_Data)


@app.route('/Admin_Add_Dr',methods=["POST", "GET"])
def Admin_Add_Dr():
    if request.method=="GET":
        return render_template("/Admin/Admin_Add_Dr.html")
    else: 
        FirstName = request.form.get('FirstName')
        Password=request.form.get('password')
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
    try:
        sql = "INSERT INTO doctor (DoctorSSN,Doctor_ID,FName,Lname,email,Sex,Birthdate, Phone, Address, Speciality,Experience,Salary) VALUES(%s, %s, %s, %s, %s, %s, %s, %s,%s,%s,%s,%s)"
        val = (SSN,DoctorID,FirstName,LastName,Email,Gender,formatted_date,PhoneNumber,Address,Speciality,Experience,Salary)
        mycursor.execute(sql,val)
        """
        sql="INSERT INTO user(UserID,Username,Password,Permission,email,Doctor_DoctorSSN)"
        val=(DoctorID,FirstName,Password,'Doctor',Email,SSN)
        mycursor.execute(sql,val)
        """
        mydb.commit() 
        return redirect(url_for('AdminDr'))
    except:
        return render_template("/Admin/Admin_Add_Dr.html")

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
        result = {}
        result['firstname'] = request.form["FirstName"]
        result['lastname'] = request.form["LastName"]
        result['email'] = request.form["email"]
        result['complaint'] = request.form["complain"]
        sendmessage(result)
        flash('Email is successfully sent', 'success')
        return redirect("/contactus")
    return render_template("contactus.html")
######################################### ---INDEXEND---#################################################

# Nurse Page############################################3

######################################### ---NURSESTART---#################################################

@app.route("/nursehome", methods=["POST", "GET"])
def nursehome():
    # nurseid = #session['id']
    result = {}
    mycursor.execute(
        'SELECT FName,LName,TIMESTAMPDIFF(YEAR, Birthdate, CURDATE()) AS age ,Nurse_SSN,Sex from nurse where NurseID=%s', ([1]))
    nurse = mycursor.fetchone()
    mycursor.execute(
        'SELECT patient.FName,patient.LName,PatientID from patient join  nurse on AssignedNurseSSN=Nurse_SSN where NurseID=%s', ([1]))
    patient = mycursor.fetchone()
    return render_template('/nurse/nursehome.html', nurseid=1, nurse=nurse, patient=patient)


@app.route("/patientrecord", methods=["POST", "GET"])
def patientrecord():
    mycursor.execute('SELECT RecordID,patient.FName,patient.LName,TIMESTAMPDIFF(YEAR, patient.Birthdate, CURDATE()),patient.Sex,patient.Emergency_Contact,MedicalStatus,MedicalHistory,Blood_Group,Level_of_consiousness,Pupils,Skin,BloodPressure,BloodGlucose,RespiratoryRate,OxygenSaturation,PulseRateMin,IV_Access,IV_Acess_Date,Takes_Heparin,MedicalDiagnosis,Admission_Reasoning,Date_Admitted,Beds_BedID,doctor.Fname,doctor.Lname,Doctor_ID,patient.PatientID from patient join patientrecord on PSSN=Patient_PSSN join Doctor on AssignedDrSSN=DoctorSSN where PatientID=%s',([1]))
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
                return redirect('/patientlabsandscans')
            file_contents = file.read()
            val = (selected_radio, file_contents,request.form.get('dataissued'), 1)
            mycursor.execute("INSERT INTO labresults (Type, LabResult, DateIssued, Patient_PSSN,Flag) VALUES (%s, %s, %s, (SELECT PSSN FROM patient WHERE PatientID=%s),'Checked')", val)
            mydb.commit()
            return redirect('/patientlabsandscans')
        elif "uploadimaging" in request.form:
            selected_radio = request.form.get('Imaging')
            file = request.files['existingimaging']
            file_contents = file.read()
            if selected_radio is None:
                flash('Please check the form again')
                return redirect('/patientlabsandscans')
            val = (selected_radio, file_contents, request.form.get('dataissued'), 1)
            mycursor.execute("INSERT INTO patientscans(Type,PatientScans,DataIssued,Patient_PSSN,Flag) VALUES (%s, %s, %s, (SELECT PSSN FROM patient WHERE PatientID=%s),'Checked')", val)
            mydb.commit()
            return redirect('/patientlabsandscans')
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
        val1 = ((request.form.get('consciousness')), (request.form.get('pupils')), (request.form.get('skin')), (request.form.get('bloodpressure')), (request.form.get('bloodglucose')), (request.form.get('respiratoryrate')),(request.form.get('oxygensaturation')), (request.form.get('heartrate')), (request.form.get('painlevel')), (request.form.get('ivaccess')), (request.form.get('ivaccessdate')), (request.form.get('heparin')), (patient_id))
        val2 = ((request.form.get('bloodtype')), (patient_id))
        mycursor.execute('UPDATE patientrecord SET Level_of_consiousness=%s,Pupils=%s,Bloodpressure=%s,Skin=%s,BloodGlucose=%s,Respiratoryrate=%s,OxygenSaturation=%s,PulseRateMin=%s,PainLevel=%s,IV_Access=%s,IV_Acess_date=%s,Takes_Heparin=%s where Patient_PSSN in(SELECT PSSN FROM patient WHERE PatientID=%s)', val1)
        mycursor.execute('UPDATE patient SET Blood_Group=%s WHERE PatientID=%s',val2)
        return redirect("/patientrecord")
    return render_template('/nurse/dailyassessment.html')


@app.route("/prescriptiontable", methods=["POST", "GET"])
def prescriptiontable():
    mycursor.execute('SELECT medicine_id,medicine_name,Dosage,Frequency,StartDate,EndDate from prescribed_medication join patient on Patient_PSSN=PSSN WHERE PatientID=%s', ([1]))
    prescription = mycursor.fetchall()
    mycursor.execute(
        'SELECT COUNT(timestamps) from medicine_prescription_timestamps join prescribed_medication on medicine_id=medicine_prescription_id join patient on Patient_PSSN=PSSN WHERE PatientID=%s GROUP BY timestampid', ([1]))
    timestamp=mycursor.fetchall()
    return render_template('/nurse/prescriptiontable.html', prescriptionlist=prescription, timestamps=timestamp)


@app.route('/administer_in_prescription_table/<int:medicineid>')
def administer_in_prescription_table(medicineid):
    mycursor.execute('INSERT INTO medicine_prescription_timestamps(medicine_prescription_id,timestamps) values(%s, CURRENT_TIMESTAMP)', [medicineid])
    mydb.commit()
    flash('Medicine adminstered','success')
    return redirect('/prescriptiontable')

@app.route('/prescriptiontimestamps/<int:medicineid>')
def prescriptiontimestamps(medicineid):
    mycursor.execute('SELECT COUNT(timestamps),medicine_prescription_id,medicine_name from medicine_prescription_timestamps join prescribed_medication on medicine_prescription_id=medicine_id WHERE medicine_prescription_id=%s GROUP BY medicine_prescription_id', [medicineid])
    medicinetimestamps = mycursor.fetchone()
    mycursor.execute(
        'SELECT timestamps FROM medicine_prescription_timestamps where medicine_prescription_id=%s', [medicineid])
    timestamps=mycursor.fetchall()
    # columns = [col[0] for col in mycursor.description]
    # medicinetimestamps = [dict(zip(columns, row)) for row in rows]
    return render_template('/nurse/prescriptiontimestamps.html', medicinetimestamps=medicinetimestamps,timestamps=timestamps)


# @app.route('/nursenotifications')
# def notification():
#     return render_template('/nurse/nursenotifcations.html')


# @app.context_processor
# def inject_notification_count():
#     return countnotification()

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


@app.route("/Doctor_home")
def getdoctordata():
   # doctorid = session["id"]
   result = {}
   mycursor.execute(
       "SELECT Fname, Lname, Birthdate, DoctorSSN, Sex, Doctor_ID from doctor where Doctor_ID = %s", ([123]))
   doctor = mycursor.fetchone()
   result['doctorid'] = doctor[5]
   result['doctorname'] = doctor[0] + doctor[1]
   result['doctorbirthdate'] = doctor[2]
   result['doctorssn'] = doctor[3]
   result['doctorgender'] = doctor[4]
   # (doctorid)))
   mycursor.execute(
       'SELECT COUNT(PSSN) from patient join doctor on AssignedDrSSN = DoctorSSN where doctor_ID = %s', ([123]))
   count = mycursor.fetchone()
   result['patientsnumber'] = count[0]
   mycursor.execute(
       'SELECT TIMESTAMPDIFF (YEAR, Birthdate, CURDATE()) from doctor AS age')
   doctora = mycursor.fetchone()
   result['doctorage'] = doctora[0]

   return render_template('/Doctor/Doctor_home.html', data=result)


@app.route("/View_patients")
def viewpatientdata():
   # doctorid = session["id"]
   mycursor.execute(
       "SELECT PatientID, patient.FName, patient.LName, MedicalStatus, Level_of_consiousness from patient join doctor on AssignedDrSSN = DoctorSSN join patientrecord on PSSN = Patient_PSSN where PatientID = %s", ([1]))
   patient = mycursor.fetchone()
   return render_template('/Doctor/View_patients.html', patient=patient)

@app.route("/patientrecord_doctor")
def getpatientrecord():
   mycursor.execute(
      'SELECT RecordID, patient.FName,patient.LName,TIMESTAMPDIFF(YEAR, patient.Birthdate, CURDATE()),patient.Sex,patient.Emergency_Contact,MedicalStatus,MedicalHistory,Blood_Group,Level_of_consiousness,Pupils,Skin,BloodPressure,BloodGlucose,RespiratoryRate,OxygenSaturation,PulseRateMin,IV_Access,IV_Acess_Date,Takes_Heparin,MedicalDiagnosis,Admission_Reasoning,Date_Admitted,Beds_BedID,doctor.Fname,doctor.Lname,Doctor_ID,PatientID from patient join patientrecord on Patient_PSSN=PSSN join Doctor on AssignedDrSSN=DoctorSSN where PatientID=%s', ([1]))
   patient = mycursor.fetchone()
   mycursor.execute('SELECT medicine_name,Dosage,Frequency,StartDate,EndDate,Specifications from patient join prescribed_medication on PSSN=Patient_PSSN where patientid=%s' , ([1]))
   medicine = mycursor.fetchone()
   return render_template('/Doctor/patientrecord_doctor.html', patient=patient, medicine=medicine)







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

      if "submit1" in request.form:
         mycursor.execute(
             'SELECT Patient_PSSN, DoctorSSN from patientrecord join patient on PSSN = Patient_PSSN join doctor on AssignedDrSSN = DoctorSSN where PatientID=%s', ([1]))
         pat = mycursor.fetchone()
         val = ((12), (request.form.get("Medicinename")), (request.form.get('Dosage')), (request.form.get('freq')), (request.form.get(
             'startdatee')), (request.form.get('enddatee')), (request.form.get('instruction')), (pat[1]), pat[0])
         # mycursor.execute('select PSSN from patient join patientrecord on PSSN = Patient_PSSN where PatientID=%s' ,([1]))
         mycursor.execute("INSERT INTO prescribed_medication (medicine_id,medicine_name,Dosage, Frequency, StartDate, EndDate, Specifications,Doctor_DoctorSSN,Patient_PSSN) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s)", val)
         mydb.commit()

      elif "submit2" in request.form:
         val = request.form.get("diagnosis")
         mycursor.execute(
             'UPDATE patientrecord SET MedicalDiagnosis = %s', [val])
         mydb.commit()

      elif "request" in request.form:
         val = ((request.form.get("bID")), (request.form.get("admitdate")))
         mycursor.execute(
             'UPDATE patient SET Beds_BedID =%s, Date_Admitted = %s', val)
         mycursor.execute('UPDATE patientrecord SET Admission_Reasoning = %s', [
                          request.form.get("reason")])
         mydb.commit()

      elif "request1" in request.form:
         amin = request.form.getlist("lb")
         str1 = ','.join(amin)
         mycursor.execute(
             'SELECT PatientID, PSSN from patient join patientrecord on PSSN = Patient_PSSN where PatientID=%s', ([1]))
         patient = mycursor.fetchone()
         date = request.form.get('labdate')
         mycursor.execute("INSERT INTO labresults (LabResultID, Patient_PSSN,Type,DateIssued) VALUES (%s,%s,%s,%s)", [
                          patient[0], patient[1], str1, date])
         mydb.commit()

      elif "request2" in request.form:
         amin = request.form.getlist("sc")
         str1 = ','.join(amin)
         mycursor.execute(
             'SELECT PatientID, PSSN from patient join patientrecord on PSSN = Patient_PSSN where PatientID=%s', ([1]))
         patient = mycursor.fetchone()
         date = request.form.get('scandate')
         mycursor.execute("INSERT INTO patientscans (PatientScanID, Patient_PSSN,Type, DataIssued) VALUES (%s,%s,%s,%s)", [
                          patient[0], patient[1], str1, date])
         mydb.commit()

      return redirect("/patientrecord_doctor")
   return render_template('/Doctor/patientrecord_doctor.html')



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
