# all the imports
import sqlite3
from flask import Flask, request, session, g, redirect, url_for, \
     abort, render_template, flash
from contextlib import closing
from flask_bootstrap import Bootstrap
import hashlib

# configuration
# the database is not in tmp on the deployed verson 
DATABASE = '/tmp/expense.db'
DEBUG = True
SECRET_KEY = 'development key'
USERNAME = 'admin'
PASSWORD = 'default'


# create our little application :)
app = Flask(__name__)
app.config.from_object(__name__)
Bootstrap(app)

def connect_db():
    return sqlite3.connect(app.config['DATABASE'])

def init_db():
    with closing(connect_db()) as db:
        with app.open_resource('schema.sql', mode='r') as f:
            db.cursor().executescript(f.read())
        db.commit()

def runScript(scriptName):
    with closing(connect_db()) as db:
        with app.open_resource('scripts/' + scriptName, mode='r') as f:
            db.cursor().executescript(f.read())
        db.commit()


@app.before_request
def before_request():
    g.db = connect_db()

@app.teardown_request
def teardown_request(exception):
    db = getattr(g, 'db', None)
    if db is not None:
        db.close()

#Load the homepage where the announcements are displayed
@app.route('/')
def home():
    cur = g.db.execute('SELECT announcement, details, id, user, Timestamp FROM announcements ORDER BY id DESC LIMIT 5')
    entries = [dict(announcement=row[0], details=row[1],  key=row[2], user = row[3], timestamp = row[4]) for row in cur.fetchall()]
    return render_template('home.html', entries=entries)

#Add an announcement to the homepage
@app.route('/add_announcement', methods=['POST'])
def add_announcement():
    if not session.get('logged_in'):
        abort(401)
    g.db.execute('INSERT INTO announcements (announcement, details,user) VALUES (?, ?,?)',
                 [request.form['announcement'], request.form['details'], request.form['user']])
    g.db.commit()
    flash('New entry was successfully posted')
    return redirect(url_for('home'))

#Load the expense page where users can add roommate expenses
@app.route('/expense')
def show_entries():
    cur = g.db.execute('SELECT expense, name, amount, note FROM entries ORDER BY id DESC')
    entries = [dict(expense=row[0], name=row[1],  amount=row[2], note=row[3]) for row in cur.fetchall()]
    return render_template('show_entries.html', entries=entries)

#add an expense
@app.route('/add', methods=['POST'])
def add_entry():
    if not session.get('logged_in'):
        abort(401)
    g.db.execute('insert into entries (expense, name , amount, note) values (?, ?, ?, ?)',
                 [request.form['expense'], request.form['person'], request.form['amount'], request.form['note']])
    g.db.commit()
    g.db.execute('UPDATE payments SET amount = CASE WHEN payee = ? THEN  amount + ?/3.0 WHEN payer = ? THEN amount - ?/3.0 ELSE amount END', [request.form['person'],request.form['amount'],request.form['person'],request.form['amount']])
    g.db.commit()
    flash('New entry was successfully posted')
    return redirect(url_for('show_entries'))

#Load the payment page where users can track their payments to other users
@app.route('/payments')
def payments():
    cur = g.db.execute('SELECT payer, payee, amount FROM payments WHERE payer = ? OR payee = ?',[session['user'], session['user']])
    entries = [dict(payer=row[0], payee=row[1], amount=row[2]) for row in cur.fetchall() ]
    cur2 = g.db.execute('select payer, payee, amount, Timestamp from paymentHistory order by id desc')
    history = [dict(payer=row[0], payee=row[1], amount=row[2], date=row[3]) for row in cur2.fetchall()]   
    return render_template('payments.html',**locals())

#Add a payment
@app.route('/add_payment', methods=['POST'])
def add_payment():
	if not session.get('logged_in'):
		abort(401)
	g.db.execute('UPDATE payments SET amount = CASE WHEN payer = ? THEN amount - ? WHEN payer = ? THEN amount + ? END WHERE (payer = ? AND payee = ?) OR (payer = ? and payee = ?)',[request.form['payer'], request.form['amount'], request.form['payee'], request.form['amount'], request.form['payer'],request.form['payee'] ,request.form['payee'] ,request.form['payer'] ])
	g.db.execute('INSERT INTO paymentHistory (payer, payee, amount) values (?,?,?)', [request.form['payer'],request.form['payee'], request.form['amount']])

	g.db.commit()
	return redirect(url_for('payments'))

#Load the chore page which shows the chores for the week for the user. There is a cron script called rotateChores.py that rotates the chores 
#every week Monday morning
@app.route('/chores')
def chores():
    cur = g.db.execute('''

        SELECT person,choreDesc.desc,choreList.choreSub,completed,choreList.subComplete,choreList.id FROM weeklyChores
        JOIN choreList ON weeklyChores.choreid = choreList.choreid
        Join choreDesc ON weeklyChores.choreid = choreDesc.choreid
        WHERE person = ? AND choreList.subComplete != 1;

        ''',[session['user']])

    entries = [dict(person=row[0], choreDesc=row[1], choreSub=row[2], choreComplete=row[3], subComplete=row[4], subID = row[5]) for row in cur.fetchall() ]
    if not entries:
        g.db.execute("UPDATE weeklyChores SET completed = 1 WHERE person = ?", [session['user']])
        g.db.commit()
    return render_template('chores.html', entries=entries)

#Update the chorepage when a user completes a chore
@app.route('/chores_update',methods=['POST'])
def chores_update():
    if not session.get('logged_in'):
        abort(401)
    for chorekeys in request.form:
        print chorekeys
        g.db.execute('UPDATE choreList SET subComplete = 1 WHERE id = ?',[chorekeys])
    g.db.commit()
    return redirect(url_for('chores'))

#login and set the session name
@app.route('/login', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
	cur = g.db.execute('select username, pass from users where username = ?',[request.form['username']])
    	entries = [dict(username=row[0], password=row[1]) for row in cur.fetchall()]
        m = hashlib.md5()
	m.update(request.form['password'])
	print request.form['password']
	checkHash = m.hexdigest()

	if not entries:
		error = 'Invalid Username or Password'
	elif checkHash != entries[0]['password']:
		error = 'Invalid Username or Password'
	else:
		session['logged_in'] = True
		session['user'] = entries[0]['username']
        	return redirect(url_for('home'))
    return render_template('login.html', error=error)

#log out: update the session
@app.route('/logout')
def logout():
    session.pop('logged_in', None)
    flash('You were logged out')
    return redirect(url_for('show_entries'))


if __name__ == '__main__':
    app.run()



