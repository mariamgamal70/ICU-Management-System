from flask import get_flashed_messages
from flask import Flask, render_template, redirect, url_for, request, session, flash, Response
from flask_session import Session
import mysql.connector
from flask_mail import Mail, Message
from werkzeug.utils import secure_filename

from datetime import datetime
current_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

app = Flask(__name__)

app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Session encryption key
app.config["SECRET_KEY"] = "zf_b1JkWCAQneZoA0Xe8Gw"


app.config["MAIL_SERVER"] = "smtp.gmail.com"
app.config["MAIL_PORT"] = 465
app.config["MAIL_USERNAME"] = "mariamgamal70@gmail.com"  # senders email
app.config["MAIL_PASSWORD"] = "azaesjimhgtnsydq"  # senders password
app.config["MAIL_USE_TLS"] = False
app.config["MAIL_USE_SSL"] = True
mail = Mail()
mail.init_app(app)

mydb = mysql.connector.connect(
    host="localhost",
    user="root",
    password="Eng_8730667",
    database="icu_management_lastttt"
)
mycursor = mydb.cursor()
# GET used when no info is sent(written in URL) , POST is used when info is sent(Ex:Sensitive info)(not written in URL)
# get function route("route)
# functions are GET only by default, to make it GET and POST , u should define it as a parameter in route
# route("route",methods=["POST","GET"])
# in case it is GET and POST you should check inside the function whether the incoming is a get or post request , if its a get ,return template, if its a post , send data do changes


def countnotification():
    messages = get_flashed_messages()
    message_count = len(messages)
    return {'notification_count': message_count}


def notifynurse(notification):
    string = notification['type']+'\n'+notification['info']
    flash(string, 'warning')

# def calculate_age(born):
#    BORN SHOULD BE WRITTIN IN THIS FORMAT FIRST BEFORE PUTTING IT AS A PARAMETER
#    born = datetime(1997, 5, 21)
#    today = datetime.now()
#    return today.year - born.year - ((today.month, today.day) < (born.month, born.day))


def sendmessage(result):
    msg = Message(subject="Inquiry/Complaint",
                  sender=result['email'], recipients=["mariamgamal70@gmail.com"])
    msg.body = 'from ' + result['email'] + '\n'+'Name: '+result['firstname'] + \
        ' '+result['lastname'] + '\n' 'Complaint: ' + result['complaint']
    mail.send(msg)


@app.route("/")  # GET METHOD
def index():
    return render_template("index.html")

#################################################### Admin##################################


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
        

     mycursor.execute(
      "SELECT Doctor_ID,Fname,Lname,Sex, TIMESTAMPDIFF(YEAR, Birthdate, CURDATE()) AS Age,Speciality,StartShift,EndShift FROM doctor ORDER BY Doctor_ID ")
    #row_headers = [x[0] for x in mycursor.description]
    doctors_data = mycursor.fetchall()

    Dr_Data = {
      'records': doctors_data

   }

        
    return render_template("/Admin/AdminDr.html", Doc_data=Dr_Data)





@app.route('/Admin_Add_Dr',methods=["POST", "GET"])
def AddDr():
    
    if request.method=="GET":
         mycursor.execute("SELECT PSSN FROM patient")
         PatientSSn=mycursor.fetchall()
         mycursor.execute("SELECT PatientID FROM patient")
         Patientid=mycursor.fetchall()
         patientdata={
            'ssn':PatientSSn,
            'id':Patientid
            }

         return render_template("/Admin/Admin_Add_Dr.html",Patient_data=patientdata)
        
    elif request.method=="POST" :
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
       AssignedPatientSSN = request.form.get('patientssn')
       AssignedPatientID = request.form.get('patientid')


    try:
        sql = "INSERT INTO doctor(DoctorSSN,Doctor_ID,FName,Lname,email,Sex,Birthdate, Phone, Address, Speciality, Experience,Salary) VALUES(%s, %s, %s, %s, %s, %s, %s, %s,%s,%s,%s,%s)"
        val = (SSN,DoctorID,FirstName,LastName,Email,Gender,formatted_date,PhoneNumber,Address,Speciality,Experience,Salary)
        mycursor.execute(sql,val)
        sql="INSERT INTO user(UserID,Username,Password,Permission,email,Doctor_DoctorSSN)"
        val=(DoctorID,FirstName+' '+LastName,Password,"Doctor",Email,SSN)
        mycursor.execute(sql,val)
        """
        if AssignedPatientSSN!=None and AssignedPatientID!=None:
            sql="INSERT INTO patient(AssignedDrSSN) WHERE PSSN=%s and PatientID=%s "
            val=(AssignedPatientSSN,AssignedPatientID)
            mycursor.execute(sql,val)
            """
        mydb.commit()    

        return redirect(url_for('AdminDr'))    

    except:
        return redirect(url_for('AddDr'))
    
@app.route('/AdminReceptionist',methods=["GET"])
def AdminReceptionist():
    if request.method=="GET":
        

     mycursor.execute(
      "SELECT ReceptionistID,Fname,Lname,Sex, TIMESTAMPDIFF(YEAR, Birthdate, CURDATE()) AS Age,Experience,StartShift,EndShift FROM receptionist ORDER BY ReceptionistID ")
    #row_headers = [x[0] for x in mycursor.description]
    recep_data = mycursor.fetchall()

    R_DATA = {
      'records': recep_data

   }

        
    return render_template("/Admin/AdminReceptionist.html", RECEP_data=R_DATA)




@app.route('/Admin_Add_Receptionist',methods=["POST", "GET"])
def Admin_Add_Receptionist():
    if request.method=="GET":
     return render_template("/Admin/Admin_Add_Receptionist.html")
        
   
        
    else: 
       FirstName = request.form.get('FirstName')
       Password=request.form.get('password')
       Experience = request.form.get('Experience')
       LastName = request.form.get('LastName')
       Gender = request.form.get('gender')
       Salary = request.form.get('Salary')
       recepID = request.form.get('RecepID')
       SSN = request.form.get('ssn')
       formatted_date = request.form.get('Birthdate')  # add age
       Address = request.form.get('Address')
       Email = request.form.get('Email')
       PhoneNumber = request.form.get('PhoneNumber')
    try:

       sql = "INSERT INTO receptionist (Receptionist_SSN,ReceptionistID,Fname,Lname,email,Salary, Sex, Birthdate, Phone,Address,Experience) VALUES(%s, %s, %s, %s, %s, %s, %s, %s,%s,%s,%s)"
       val = (SSN,recepID,FirstName,LastName,Email,Salary,Gender,formatted_date,PhoneNumber,Address,Experience)
       mycursor.execute(sql,val)
       """
       sql="INSERT INTO user(UserID,Username,Password,Permission,email,Doctor_DoctorSSN)"
       val=(DoctorID,FirstName,Password,'Doctor',Email,SSN)
       mycursor.execute(sql,val)
       """
       mydb.commit() 
       return redirect(url_for('AdminReceptionist'))
   
    except:
        return render_template("/Admin/Admin_Add_Receptionist.html")

    """
@app.route('/AdminReceptionist',methods=["GET"])
def AdminReceptionist():
    if request.method=="GET":
        

     mycursor.execute(
      "SELECT ReceptionistID,Fname,Lname,Sex, TIMESTAMPDIFF(YEAR, Birthdate, CURDATE()) AS Age,Experience,StartShift,EndShift FROM receptionist ORDER BY ReceptionistID ")
    #row_headers = [x[0] for x in mycursor.description]
    recep_data = mycursor.fetchall()

    R_DATA = {
      'records': recep_data

   }

        
    return render_template("/Admin/AdminReceptionist.html", RECEP_data=R_DATA)
"""

@app.route('/AdminViewPatient',methods=["GET"])
def AdminViewPatient():
    if request.method=="GET":
        mycursor.execute("SELECT PSSN,FName,MName,LName,Sex,TIMESTAMPDIFF(YEAR, Birthdate, CURDATE()) as Age,Date_Admitted,Date_Discharged,Beds_BedID,AssignedDrSSN,AssignedNurseSSN,COUNT(PatientScans)  FROM patient JOIN patientscans  ON PSSN=Patient_PSSN GROUP BY PSSN ORDER BY PSSN ")
        Patient_info=mycursor.fetchall()
        data={
            'Patientdata':Patient_info
            
        }
        
        return render_template('/Admin/AdminPatient.html',Pat_inf=data)
    
   
        
    else: 
       FirstName = request.form.get('FirstName')
       Password=request.form.get('password')
       Experience = request.form.get('Experience')
       LastName = request.form.get('LastName')
       Gender = request.form.get('gender')
       Salary = request.form.get('Salary')
       recepID = request.form.get('RecepID')
       SSN = request.form.get('ssn')
       formatted_date = request.form.get('Birthdate')  # add age
       Address = request.form.get('Address')
       Email = request.form.get('Email')
       PhoneNumber = request.form.get('PhoneNumber')
    try:

       sql = "INSERT INTO receptionist (Receptionist_SSN,ReceptionistID,Fname,Lname,email,Salary, Sex, Birthdate, Phone,Address,Experience) VALUES(%s, %s, %s, %s, %s, %s, %s, %s,%s,%s,%s)"
       val = (SSN,recepID,FirstName,LastName,Email,Salary,Gender,formatted_date,PhoneNumber,Address,Experience)
       mycursor.execute(sql,val)
       """
       sql="INSERT INTO user(UserID,Username,Password,Permission,email,Doctor_DoctorSSN)"
       val=(DoctorID,FirstName,Password,'Doctor',Email,SSN)
       mycursor.execute(sql,val)
       """
       mydb.commit() 
       return redirect(url_for('AdminReceptionist'))
   
    except:
        return render_template("/Admin/Admin_Add_Receptionist.html")

    """
@app.route('/AdminReceptionist',methods=["GET"])
def AdminReceptionist():
    if request.method=="GET":
        

     mycursor.execute(
      "SELECT ReceptionistID,Fname,Lname,Sex, TIMESTAMPDIFF(YEAR, Birthdate, CURDATE()) AS Age,Experience,StartShift,EndShift FROM receptionist ORDER BY ReceptionistID ")
    #row_headers = [x[0] for x in mycursor.description]
    recep_data = mycursor.fetchall()

    R_DATA = {
      'records': recep_data

   }

        
    return render_template("/Admin/AdminReceptionist.html", RECEP_data=R_DATA)
"""

@app.route('/AdminViewPatient',methods=["GET"])
def AdminViewPatient():
    if request.method=="GET":
        mycursor.execute("SELECT PSSN,FName,MName,LName,Sex,TIMESTAMPDIFF(YEAR, Birthdate, CURDATE()) as Age,Date_Admitted,Date_Discharged,Beds_BedID,AssignedDrSSN,AssignedNurseSSN,COUNT(PatientScans)  FROM patient JOIN patientscans  ON PSSN=Patient_PSSN GROUP BY PSSN ORDER BY PSSN ")
        Patient_info=mycursor.fetchall()
        data={
            'Patientdata':Patient_info
            
        }
        
        return render_template('/Admin/AdminPatient.html',Pat_inf=data)
    


        
      
@app.route("/AdminPayment")
def viewadminpayment():
   mycursor.execute('SELECT * from bills')
   payments=mycursor.fetchall()
   data={
       'pay':payments
   }
   return render_template('/Admin/AdminPayment.html',Payments=data)
       
######################################### ---ADMINEND---#################################################

######################################### ---INDEXSTART---#################################################
# Modified version for user

@app.route("/signin", methods=["POST", "GET"])  # GET METHOD
def signin():
    if request.method == "POST":
        # -------------------------------PATIENT ONLY----------------------------------
        if "patient" in request.form:
            patientid = request.form["patientID"]
            patientpassword = request.form["patientpassword"]
            mycursor.execute(
                "SELECT * FROM user WHERE UserID = %s AND Password = %s", (patientid, patientpassword))
            account = mycursor.fetchone()
            if account:
                mycursor.execute(
                    "SELECT Username FROM user WHERE UserID = %s AND Password = %s", (patientid, patientpassword))
                patientname = mycursor.fetchone()
                session["name"] = account["Username"]
                session["name"] = patientname  # to reference patient name
                session["id"] = patientid
                session["Permision"] = "Patient"  # Permision_level
                return render_template("patienthome.html")
            else:
                flash('ID/Password is incorrect', 'warning')
                return redirect('/signin')
        # ----------------------------------ENDPATIENT---------------------------------------
        # ---------------------------------DOCTORONLY-----------------------------------------
        elif "doctor" in request.form:
            doctorid = request.form["doctorID"]
            doctorpassword = request.form["doctorpassword"]
            mycursor.execute(
                "SELECT * FROM user WHERE UserID = %s AND Password = %s", (doctorid, doctorpassword,))
            account = mycursor.fetchone()
            if account:
                mycursor.execute(
                    "SELECT Username FROM user WHERE doctorid = %s AND doctorpassword = %s", (doctorid, doctorpassword,))
                doctorname = mycursor.fetchone()
                session["name"] = doctorname
                session["id"] = doctorid
                session["Permision"] = "Doctor"
                return render_template("doctorhome.html")
            else:
                flash('ID/Password is incorrect', 'warning')
                return redirect('/signin')
        # ------------------------------------ENDDOCTOR-------------------------------------------
        # -------------------------------------NURSEONLY------------------------------------------
        elif "nurse" in request.form:
            nurseid = request.form["nurseID"]
            nursepassword = request.form["nursepassword"]
            mycursor.execute(
                "SELECT * FROM user WHERE UserID = %s AND Password = %s", (nurseid, nursepassword,))
            account = mycursor.fetchone()
            if account:
                mycursor.execute(
                    "SELECT Username FROM useer WHERE UserID = %s AND Password = %s", (nurseid, nursepassword,))
                nursename = mycursor.fetchone()
                session["id"] = doctorid
                session["name"] = nursename
                session["Permision"] = "Nurse"
                return render_template("doctorhome.html")
            else:
                flash('ID/Password is incorrect', 'warning')
                return redirect('/signin')
        # ----------------------------------------ENDNURSE---------------------------------------------
        # --------------------------------------ADMINONLY----------------------------------------------
        elif "admin" in request.form:
            adminid = request.form["adminID"]
            adminpassword = request.form["adminpassword"]
            mycursor.execute(
                "SELECT * FROM user WHERE UserID = %s AND Password = %s", (adminid, adminpassword,))
            account = mycursor.fetchone()
            if account:
                mycursor.execute(
                    "SELECT Username FROM user WHERE UserID = %s AND Password = %s", (adminid, adminpassword,))
                adminname = mycursor.fetchone()
                session["id"] = adminid
                session["name"] = adminname
                session["Permision"] = "Admin"
                return render_template("AdminMain.html")
            else:
                flash('ID/Password is incorrect', 'warning')
                return redirect('/signin')
        # ----------------------------------------ADMINEND-----------------------------------------------
        # ------------------------------------RECEPTIONISTSONLY------------------------------------------
        elif "receptionist" in request.form:
            receptionistid = request.form["receptionistID"]
            receptionistpassword = request.form["receptionistpassword"]
            mycursor.execute("SELECT * FROM user WHERE UserID = %s AND Password = %s",
                             (receptionistid, receptionistpassword,))
            account = mycursor.fetchone()
            if account:
                mycursor.execute("SELECT Username FROM user WHERE UserID = %s AND Password = %s", (
                    receptionistid, receptionistpassword,))
                receptionistname = mycursor.fetchone()
                session["id"] = receptionistid
                session["name"] = receptionistname
                session["Permision"] = "Receptionist"
                return render_template("receptionist1.html")
            else:
                flash('ID/Password is incorrect', 'warning')
                return redirect('/signin')
        # ------------------------------------RECEPTIONISTEND-------------------------------------------
    return render_template('signin.html')


"""
@app.route("/signin",methods=["POST","GET"])  # GET METHOD
def signin():
   if request.method == "POST":
      #-------------------------------PATIENT ONLY----------------------------------
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
      #----------------------------------ENDPATIENT---------------------------------------
      #---------------------------------DOCTORONLY-----------------------------------------
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
      #------------------------------------ENDDOCTOR-------------------------------------------
      #-------------------------------------NURSEONLY------------------------------------------
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
      #----------------------------------------ENDNURSE---------------------------------------------
      #--------------------------------------ADMINONLY----------------------------------------------
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
      #----------------------------------------ADMINEND-----------------------------------------------
      #------------------------------------RECEPTIONISTSONLY------------------------------------------
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
      #------------------------------------RECEPTIONISTEND-------------------------------------------
   return render_template('signin.html')
"""


@app.route("/logout")
def LogOut():
    session.pop("id", None)
    session.pop("name", None)
    session.pop("Permission", None)
    return redirect(url_for('/'))


@app.route("/contactus", methods=["POST", "GET"])  # GET METHOD
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
   nurseid = session['id']
   result = {}
   mycursor.execute(
       'SELECT nurse.FName,LName,TIMESTAMPDIFF(YEAR, Birthdate, CURDATE()) AS age ,Nurse_SSN,Sex,Unit_Rooms_RoomNumber from nurse where NurseID=%s', (nurseid))
   nurse = mycursor.fetchone()
   #  result['nurseid'] = session['id']
   #  result['nursename'] = nurse[0]+' ' + nurse[1]
   #  result['nursebirthdate'] = nurse[2]
   #  result['nursessn'] = nurse[3]
   #  result['nursegender'] = nurse[4]
   mycursor.execute('SELECT patient.FName,patient.LName,PatientID from patient join  nurse on Assignednurse=Nurse_SSN where NurseID=%s', (nurse[5]))
   patient = mycursor.fetchone()
   # result['patientname'] = patient[0]+' '+patient[1]
   # result['patientid'] = patient[2]
   # session['patientid'] = patient[2]
   return render_template('nursehome.html',nurseid=nurseid,nurse=nurse,patient=patient)


@app.route("/patientrecord")#NEEDS FIXING
def getpatientrecord():
   mycursor.execute('SELECT patient.RecordID,patient.FName,patient.LName,TIMESTAMPDIFF(YEAR, patient.Birthdate, CURDATE()),patient.Sex,patient.Emergency_Contact,MedicalStatus,MedicalHistory,Blood_Group,Level_of_consiousness,pupils,skin,BloodPressure,BloodGlucose,RespiratoryRate,OxygenSaturation,PulseRateMin,IV_Access,IV_Acess_Date,Takes_Heparin,Admission_Reasoning,Date_Admitted,Beds_BedID,doctor.Fname,doctor.LName,Doctor_ID from patient join patientrecord on PatientRecord_RecordID=RecordID join Doctor on AssignedDrSSN=DoctorSSN where PatientID=%s', (session['patientid']))
   patient = mycursor.fetchone()
   return render_template('patientrecord.html', patient=patient)

@app.route("/patientlabsandscans", methods=["POST", "GET"])
def getpatientlabsandscans():
   if request.method == "POST":
      if "uploadlab" in request.form:
            selected_radio = request.form.get('lab')
            file = request.files['existinglab']
            if selected_radio is None or not file:
               flash('Please check the form again')
               redirect('/patientlabsandscans')
               file_contents = file.read()
               val = ((selected_radio, file_contents, request.form.get('dataissued')), (session['patientid']))
               mycursor.execute('INSERT INTO labresults (Type,LabResult,DateIssued) values(%s) where Patient_PSSN in(SELECT PSSN FROM patient where PatientID=%s )', val)
               mydb.commit()
               return render_template('patientlabsandscans.html')
            else:
               selected_radio = request.form.get('imaging')
               file = request.files['existing']
               if selected_radio is None or not file:
                  flash('Please check the form again')
                  redirect('/patientlabsandscans')
               val = ((selected_radio, request.files['existinglab'], request.form.get('dataissued')), (session['patientid']))
               mycursor.execute('INSERT INTO patientscans (Type,LabResult,DateIssued) values(%s) where Patient_PSSN in(SELECT PSSN FROM patient where PatientID=%s )', val)
               mydb.commit()
               return render_template('patientlabsandscans.html')
   mycursor.execute('SELECT LabResultID,Labfile,Type,DateIssued from labresults join patient on PSSN=Patient_PSSN where patientid=%s and flag=checked', (session['patientid']))
   checkedlabs = mycursor.fetchall()
   mycursor.execute('SELECT LabResultID,labfile,Type,DateIssued from labresults join patient on PSSN=Patient_PSSN where patientid=%s and flag=pending', (session['patientid']))
   pendinglabs = mycursor.fetchall()
   mycursor.execute('SELECT PatientScanID,labfile,Type,DateIssued from PatientScans join patient on PSSN=Patient_PSSN where patientid=%s and flag=pending', (session['patientid']))
   checkedimaging = mycursor.fetchall()
   mycursor.execute('SELECT PatientScanID,scanfile,Type,DateIssued from PatientScans join patient on PSSN=Patient_PSSN where patientid=%s and flag=pending', (session['patientid']))
   pendingimaging = mycursor.fetchall()
   return render_template('patientlabsandscans.html',checkedlabs=checkedlabs, pendinglabs=pendinglabs, checkedimaging=checkedimaging, pendingimaging=pendingimaging)

@app.route('/patientlabsandscans/<int:file_id>')
def viewfile(file_id):
   mycursor.execute('SELECT LabResults from labresults where id=%s', (file_id))
   file = mycursor.fetchone()
   return Response(file, mimetype='application/octet-stream')


@app.route("/dailyassessment/<int:file_id>", methods=["POST", "GET"])
def dailyassessment():
   if request.method == "POST":
      val = ((request.form.get('consciousness')), (request.form.get('pupils')), (request.form.get('skin')), (request.form.get('bloodtype')), (request.form.get('bloodpressure')), (request.form.get('bloodglucose')), (request.form.get('respiratoryrate')), (request.form.get('oxygensaturation')), (request.form.get('heartrate')), (request.form.get('painlevel')), (request.form.get('ivaccess')), (request.form.get('ivaccessdate')), (request.form.get('heparin')))
      mycursor.execute('UPDATE TABLE patient SET Level_of_consciousness=%s,pupils=%s,skin=%s,BloodGluecose=%s,Respiratoryrate=%s,OxygenSaturation=%s,HeartRate=%s,PainLevel=%s,IV_Access=%s,iv_Acess_date=%s,Takes_Heparin=%s', val)
      return redirect("/dailyassessment")
   return render_template('dailyassessment.html')

@app.route("/prescriptiontable", methods=["POST", "GET"])
def prescriptiontable():
   mycursor.execute('SELECT medicine_id,medicine_name,Dosage,Frequency,COUNT(timestamp)as Noadmisntered,StartDate,EndDate from prescribed_medication join patient on patient_PSSN=PSSN join medicine_prescription_timestamps on medicine_id= medicine_prescription_id group by medicine_prescription_id where patientID=%s', (session['patientid']))
   #TRANSFORMED LIST OF TUPLES INTO DICTIONARY VV ACCESSED BY KEYWORDS
#    columns = [col[0] for col in mycursor.description]
#    result = [dict(zip(columns, row)) for row in mycursor.fetchall()]
   prescriptions = mycursor.fetchall() #RETURNS LIST OF TUPLES, TUPLES ARE ACCESSED USING INDEXES
   return render_template('prescriptiontable.html', prescriptions=prescriptions)

# @app.route('/prescriptiontable/<id:medicineid>')
# def prescriptiontable(medicineid):
#     mycursor.execute(
#         'INSERT INTO medicine_prescription_timestamps (medicine_prescription_id, timestamp) values(%s, CURRENT_TIMESTAMP)', (medicineid))
#     return redirect('prescriptionchecklist.html')


# @app.route('/prescriptionchecklist/<id:medicineid>')
# def prescriptiontable(medicineid):
#    mycursor.execute('SELECT SUM(id),id,timestamp from medicine_prescription_timestamps group by id where medicine_prescription_id=%s', (medicineid))
#    medicinetimestamps=mycursor.fetchall()
#    return render_template('prescriptionchecklist.html',medicinetimestamps=medicinetimestamps)


@app.route('/nursenotifications')
def notification():
    return render_template('nursenotifcations.html')


@app.context_processor
def inject_notification_count():
    return countnotification()

######################################### ---NURSEEND---#################################################
############################################## sidebar#####################################
############################################### Patient Page ############################################
# Age


@app.route("/patient/homepage")
def PatientRecord():
    mycursor.execute(
        'SELECT FirstName,MiddleName,LastName,Birthdate,Gender,PSSN,Address,email,PhoneNumber,EmergencyContact,PatientID,Insurance_Status from patient join record on PSSN=PatientSSN where patientid=%s', (session['patientid']))
    patient = mycursor.fetchone()
    render_template('/patient/homepage', data=patient)

# edit sum and groupby


@app.route("/patient/icuinfo")
def ICUInfo():
    mycursor.execute(
        'SELECT Date_Admitted,Date_Discharged,AttendingPhysicianFirstName,AttendingPhysicianLastName,AttendingPhysicianFirstName,AttendingNurseLastName,Diagnosis,Bills_ID,TotalValue,Insurance_Percent,Price,Specifications,Frequency,Dosage,StartDate,EndDate from patient join Prescribed_Medication on PSSN=Patient_PSSN join bills on PSSN=Patient_PSSN join beds on Beds_BedID=BedID join record on SSN=PatientSSN join Doctor on AttendingPhysicianID=DoctorID join Nurse on AttendingNurseID=NurseID where patientid=%s', (session['patientid']))
    patient = mycursor.fetchone()
    render_template('/patient/icuinfo', data=patient)

############################################# Receptionist Page ############################################


@app.route("/receptionist/viewrecord")
def R_ViewRecord():
    mycursor.execute(
        'SELECT FirstName,MiddleName,LastName,Birthdate,Gender,PSSN,Address,email,PhoneNumber,EmergencyContact,PatientID,Insurance_Status,AttendingPhysicianFirstName,AttendingPhysicianLastName,AttendingPhysicianFirstName,AttendingNurseLastName from patient join record on PSSN=PatientSSN join Doctor on AttendingPhysicianID=DoctorID join Nurse on AttendingNurseID=NurseID where patientid=%s', (session['patientid']))
    patient = mycursor.fetchone()
    render_template('/receptionist/viewrecord', data=patient)


@app.route("/receptionist/homepage", methods=["POST", "GET"])
def ReceptionistHomePage():
    receptionistid = session['id']
    result = {}
    mycursor.execute(
        'SELECT FirstName,LastName,Birthdate,SSN,Gender from receptionist where receptionistID=%s', (receptionistid))
    receptionist = mycursor.fetchone()
    result['receptionistid'] = session['id']
    result['receptionistname'] = receptionist[0] + receptionist[1]
    result['receptionistbirthdate'] = receptionist[2]
    result['receptionistssn'] = receptionist[3]
    result['receptionistgender'] = receptionist[4]
    mycursor.execute(
        'SELECT TIMESTAMPDIFF (YEAR, Birthdate, CURDATE()) from receptionist AS age')
    receptionist = mycursor.fetchone()
    result['receptionistage'] = receptionist  # age
    render_template('/receptionist/homepage', data=result)


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
        formatted_date = request.form.get('Birthdate')  # add age
        Insurance = request.form.get('Insurance')
        Address = request.form.get('Address')
        Email = request.form.get('Email')
        PhoneNumber = request.form.get('PhoneNumber')
        EmergencyContact = request.form.get('PhoneNumber')
        AssignedDoctor = request.form.get('AssignedDoctor')
        AssignedNurse = request.form.get('AssignedNurse')
        try:
            sql = "INSERT INTO Patient(PSSN,FirstName, MiddleName, LastName,PatientID, Sex, Birthdate,Address, Email, PhoneNumber,EmergencyContact,AssignedDoctor,AssignedNurse) VALUES(%s, %s, %s, %s, %s, %s, %s, %s,%s,%s,%s,%s,%s)"
            val = (SSN, FirstName, MiddleName, LastName, PatientID, Gender, formatted_date,
                   Address, Email, PhoneNumber, EmergencyContact, AssignedDoctor, AssignedNurse)
            mycursor.execute(sql, val)
            sql = "INSERT INTO PatientRecord(RecordID,Insurance_Status) VALUES(%s, %s)"
            val = (RecordID, Insurance)
            mydb.commit()
            return render_template('/receptionist/managerecords.html', message=FirstName + ' ' + LastName+" has been successfully added to the database")
        except:
            return render_template('/receptionist/addrecord.html', error="Invalid input!")

    else:
        return render_template('/receptionist/addrecord.html')

##################################################### Run#############################################################
 

if __name__ == "__main__":
    app.run(debug=True)
