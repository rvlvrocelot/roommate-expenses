import sqlite3

def assessFines(person):
	pass

#update on deployed
conn = sqlite3.connect("/tmp/expense.db")
c = conn.cursor()

choreDict = {}

for row in c.execute("SELECT * FROM weeklyChores"):
	choreDict[row[1]] = [row[2],row[3]] 

for person in choreDict:
	c.execute("UPDATE weeklyChores SET choreid = ? WHERE person = ?", ((choreDict[person][0] + 1)%3 ,person))
	if choreDict[person][1] == 0:
		assessFines(person)


c.execute("UPDATE weeklyChores SET completed = 0")
c.execute("UPDATE choreList SET subComplete = 0")

conn.commit()