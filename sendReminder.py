import smtplib
import sqlite3
from email.mime.text import MIMEText
from collections import defaultdict
 
def sendemail(from_addr, to_addr_list, cc_addr_list,
              subject, message,
              login, password,
              smtpserver='smtp.gmail.com:587'):
    header  = 'From: %s\n' % from_addr
    header += 'To: %s\n' % ','.join(to_addr_list)
    header += 'Cc: %s\n' % ','.join(cc_addr_list)
    header += 'Subject: %s\n\n' % subject
    message = header + message
 
    server = smtplib.SMTP(smtpserver)
    server.starttls()
    server.login(login,password)

    problems = server.sendmail(from_addr, to_addr_list, message)
    server.quit()
    return problems


conn = sqlite3.connect("/tmp/expense.db")
c = conn.cursor()

#PersonDict = {Andrew:"andrew.mahan@colorado.edu",Anita:"abalakristnan93@gmail.com",Ryder:"tung.pham@smfa.edu"}
personDict = {"Andrew":["andrew.mahan@colorado.edu"],"Anita":["abalakrishnan93@gmail.com"],"Ryder":["tung.pham@smfa.edu"]}
choreDict = defaultdict(list)

for row in c.execute('''select person,choreList.choreSub from weeklyChores
Join choreList on weeklyChores.choreid = choreList.choreid
Join choreDesc on weeklyChores.choreid = choreDesc.choreid
WHERE choreList.subComplete != 1;'''):
  choreDict[row[0]].append(row[1])

fromad = "nagbot@andrewmahan.com"
cc = ""
subject = "Please do your chores!"
login = "nagbot@andrewmahan.com"
password = "Sublime44!!"
smtpserver = "smtp.andrewmahan.com:587"

for person in choreDict:
  to = personDict[person]
  message = "Hey %s, \nJust as a friendly reminder, you have until 11:59 on Sunday to do the following chores: \n \n" % person 
  for chore in choreDict[person]:
    message += chore + "\n"

  sendemail(fromad,to,cc,subject,message,login,password,smtpserver)
