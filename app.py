from flask import Flask,render_template,request
app = Flask(__name__)
#GET used when no info is sent(written in URL) , POST is used when info is sent(Ex:Sensitive info)(not written in URL)
#get function route('route)
#functions are GET only by default, to make it GET and POST , u should define it as a parameter in route
#route('route',methods=['POST','GET'])
# in case it is GET and POST you should check inside the function whether the incoming is a get or post request , if its a get ,return template, if its a post , send data do changes
@app.route('/')#GET METHOD
def index():
   return render_template('index.html')

@app.route('/signin',method=['POST','GET'])  # GET METHOD
def signin():
   if request.method=='POST':
      patientid=request.form['patientID']
      patientpassword = request.form['patientpassword']
      doctorid = request.form['doctorID']
      doctorpassword = request.form['doctorpassword']
      nurseid = request.form['nurseID']
      nursepassword = request.form['nursepassword']
      adminid = request.form['adminID']
      adminpassword = request.form['adminpassword']
      receptionistid = request.form['receptionistID']
      receptionistpassword = request.form['receptionistpassword']
   else:
      return render_template('signin.html')

@app.route('/contactus')  # GET METHOD
def contactus():
   return render_template('contactus.html')



if __name__ == '__main__':
   app.run()