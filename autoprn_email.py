import sqlite3
import datetime
import smtplib, ssl
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import time
import random
import mysql.connector


try:
    #INSERT TASK DETAILS IN PROCESS INFO DB
    start_time = time.time()
    d = datetime.datetime.now()
    db_start_date=str(d.year)+"-"+str(d.month)+"-"+str(d.day)
    db_start_time=str(d.hour)+":"+str(d.minute)+":"+str(d.second)
    conn = sqlite3.connect('process_info.db')
    conn.execute("INSERT INTO process_log(start_date,start_time,task_type) VALUES(?,?,?)",(str(db_start_date),str(db_start_time),"AUTOPRN-AUTOEMAIL"))
    conn.commit()
    conn.close()
except Exception as e:
    print(e)

sender_email ='bk.ims.iiot@gmail.com'
#receiver_email = "asrrjprince@gmail.com"
#password = 'KOKI@1234'
password = 'lmpv ekvq zzvr tvdv'
#receiver_email = ["atul.moghe@bestgroup.co.in","rakesh.jena@bestkoki.com","asrrjprince@gmail.com","parveen.sharma@bestkoki.com","bkims.common@bestkoki.com","sandeep.aggarwal@bestgroup.co.in","mayank.arora@bestgroup.co.in","sanjay.sharma@bestgroup.co.in","neeraj.khanna@bestgroup.co.in","parveen.gupta@bestkoki.com","robocell@bestkoki.com","assembly@bestkoki.com","sanjeev.bharadwaj@bestgroup.co.in","kailash.kumar@bestkoki.com","vishal.sharma@bestkoki.com","vinay.kumar@bestkoki.com","ithelpdesk@bestkoki.com","processqa@bestkoki.com","vishal.mohal@bestgroup.co.in"]
#receiver_email = ["asrrjprince@gmail.com","atul.moghe@bestgroup.co.in"]
receiver_email = ["atul.moghe@bestgroup.co.in","rakesh.jena@bestkoki.com","asrrjprince@gmail.com","parveen.sharma@bestkoki.com","bkims.common@bestkoki.com","sandeep.aggarwal@bestgroup.co.in","mayank.arora@bestgroup.co.in","sanjay.sharma@bestgroup.co.in","neeraj.khanna@bestgroup.co.in","parveen.gupta@bestkoki.com","robocell@bestkoki.com","assembly@bestkoki.com","sanjeev.bharadwaj@bestgroup.co.in","kailash.kumar@bestkoki.com","vishal.sharma@bestkoki.com","vinay.kumar@bestkoki.com","ithelpdesk@bestkoki.com","processqa@bestkoki.com","vishal.mohal@bestgroup.co.in","neeraj.tyagi@bestkoki.com","briham.pal@best-cables.com","yogesh.joshi@bestgroup.co.in","manish.vats@bestkoki.com"]


message = MIMEMultipart("alternative")
sub="PRN DATA STATUS EMAIL"
message["Subject"] = sub
message["From"] = sender_email

one_day = datetime.timedelta(days=1)
query_date= datetime.date.today()-one_day

mydb = mysql.connector.connect(
  host="localhost",
  user="root",
  password="mysql",
  database="machine"
)
table=""
mycursor = mydb.cursor()
mycursor.execute("SELECT * FROM prn_data  WHERE date='"+str(query_date)+"'")
myresult = mycursor.fetchall()
for x in myresult:
  table+="<tr>"+"<td>"+str(x[0])+"</td>"+"<td>"+str(x[4])+"</td>"+"<td>"+str(x[2])+"</td>"+"<td>"+str(x[9])+"</td>"+"<td>"+str(x[6
  ])+"</td>"+"</tr>"
# Create the plain-text and HTML version of your message
html = """\
<!DOCTYPE html>
<html>
<head>
<style>
table {
  font-family: arial, sans-serif;
  border-collapse: collapse;
  width: 100%;
}

td, th {
  border: 1px solid #dddddd;
  text-align: left;
  padding: 8px;
  
}
th{

  background-color:gold;
 
}
tr:nth-child(even) {
  background-color: #dddddd;
}
</style>
</head>
<body>
<p style='font-size:20px;'>This is a system generated mail being forwarded to all users for their reference. <br>
Following Table indicates the status of <b>“PRN DATA STATUS”</b> availability on the Server for the mentioned date, which can be accessed by all authorized users(Team IMS is Working on it...). 
<br><br>
</p>
<center><h2>AUTO PRN REPORT FOR DATE: """+str(query_date)+"""</h2></center>

<table>
  <tr>
    <th>Serial</th>
    <th>Product Name(Model)</th>
    <th>M/C Name</th>
    <th>Total Count</th>
    <th>"""+str(query_date)+"""</th>
  </tr>
  """+str(table) +"""
</table>
<br>
<br>
<br>
<h2>
<i>Thanks & Regards</i><br>
<b>Team IMS, BEST KOKI</b></h2>
</body>
</html>

"""

# Turn these into plain/html MIMEText objects
part2 = MIMEText(html, "html")

# Add HTML/plain-text parts to MIMEMultipart message
# The email client will try to render the last part first
message.attach(part2)
msg_time=datetime.datetime.now().time()
msg_date= datetime.date.today()
# Create secure connection with server and send email
try:
  context = ssl.create_default_context()
  with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=context) as server:
      server.login(sender_email, password)
      for eid in receiver_email:
        message["To"] = ""
        message["To"] = eid
        server.sendmail(sender_email, eid, message.as_string())
        conn1 = sqlite3.connect('C:\Program Files\Ampps\www\eol\controller\db\eol_email.db')
        email_data="INSERT INTO email_log (email,msg,msg_date,msg_time,msg_subject) VALUES ('"+str(eid)+"',"+'"'+str(html)+'"'+",'"+str(msg_date)+"','"+str(msg_time)+"','"+str(sub)+"')"
        conn1.execute(str(email_data))
        print(email_data)
        conn1.commit()
        print ("Records created successfully")
        conn1.close()
        print(table)
except Exception as e:
  print(e)
finally:
  print("MSG HAS BEEN SENT TO THESE EMAIL ADDRESSES: ",receiver_email)


try:
  #UPDATE TASK DETAILS IN PROCESS INFO DB
  d = datetime.datetime.now() 
  db_end_date=str(d.year)+"-"+str(d.month)+"-"+str(d.day)
  db_end_time=str(d.hour)+":"+str(d.minute)+":"+str(d.second)
  end_time=time.time() - start_time
  conn = sqlite3.connect('process_info.db')
  #print("UPDATE process_log SET end_ date='"+str(db_end_date)+"',end_time="+str(db_end_date)+",time_taken="+str(int(end_time))+" WHERE start_date="+str(db_start_date)+" AND start_time="+str(db_start_time)+" AND task_type="+"DMC-LITE")
  conn.execute("UPDATE process_log SET end_date='"+str(db_end_date)+"',end_time='"+str(db_end_time)+"',time_taken="+str(int(end_time))+" WHERE start_date='"+str(db_start_date)+"' AND start_time='"+str(db_start_time)+"' AND task_type="+"'EOL-AUTOEMAIL'")
  conn.commit()
  conn.close()
except Exception as e:
  print(e)
print("Thank You!")
