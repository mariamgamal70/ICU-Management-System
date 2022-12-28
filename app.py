from flask import Flask, redirect, url_for, request, render_template
import mysql.connector
app = Flask(__name__)
mydb = mysql.connector.connect(
   host="localhost",
   user="root",
   password="whatever",
   database="quiztrial1"
)
mycursor = mydb.cursor()
#GET used when no info is sent(written in URL) , POST is used when info is sent(Ex:Sensitive info)(not written in URL)
#get function route('route)
#functions are GET only by default, to make it GET and POST , u should define it as a parameter in route
#route('route',methods=['POST','GET'])
# in case it is GET and POST you should check inside the function whether the incoming is a get or post request , if its a get ,return template, if its a post , send data do changes
@app.route('/')#GET METHOD
def index():
   return render_template('index.html')

@app.route('/signin',methods=['POST','GET'])  # GET METHOD
def signin():
   msg = 'Incorrect username/password!'
   if request.method == 'POST':
      if 'patient' in request.form:
         patientid = request.form['patientID']
         patientpassword = request.form['patientpassword']
         mycursor.execute(
             'SELECT * FROM patient WHERE patientid = %s AND patientpassword = %s', (patientid, patientpassword,))
         account = mycursor.fetchone()
         if account:
            render_template('patient.html')
         else: 
            return msg
      elif 'doctor' in request.form:
         doctorid = request.form['doctorID']
         doctorpassword = request.form['doctorpassword']
         mycursor.execute(
             'SELECT * FROM doctor WHERE doctorid = %s AND doctorpassword = %s', (doctorid, doctorpassword,))
         account = mycursor.fetchone()
         if account:
            render_template('doctor.html')
         else:
            return msg
      elif 'nurse' in request.form :
         nurseid = request.form['nurseID']
         nursepassword = request.form['nursepassword']
         mycursor.execute(
             'SELECT * FROM nurse WHERE nurseid = %s AND nursepassword = %s', (nurseid, nursepassword,))
         account = mycursor.fetchone()
         if account:
            render_template('nurse.html')
         else:
            return msg
      elif 'admin' in request.form:
         adminid = request.form['adminID']
         adminpassword = request.form['adminpassword']
         mycursor.execute(
             'SELECT * FROM admin WHERE adminid = %s AND adminpassword = %s', (adminid, adminpassword,))
         account = mycursor.fetchone()
         if account:
            render_template('admin.html')
         else:
            return msg
      if 'receptionist' in request.form:
         receptionistid = request.form['receptionistID']
         receptionistpassword = request.form['receptionistpassword']
         mycursor.execute(
             'SELECT * FROM receptionist WHERE receptionistid = %s AND receptionistpassword = %s', (receptionistid, receptionistpassword,))
         account = mycursor.fetchone()
         if account:
            render_template('receptionist1.html')
         else:
            return msg
      # If account exists in accounts table in out database
      #if account:
         # Create session data, we can access this data in other routes
         #session['loggedin'] = True
         #session['id'] = account['id']
         #session['username'] = account['username']
         # Redirect to home page
         #return 'Logged in successfully!'
      #else:    
         # Account doesnt exist or username/password incorrect
         #msg = 'Incorrect username/password!'
   else:
      return render_template('signin.html')

@app.route('/contactus')  # GET METHOD
def contactus():
   return render_template('contactus.html')

if __name__ == '__main__':
   app.run()