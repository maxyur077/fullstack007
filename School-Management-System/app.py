from flask import Flask, render_template, request, redirect, url_for ,session
from flask_mysqldb import MySQL
import MySQLdb.cursors
import re  

app = Flask(__name__) 

app.secret_key = 'xyzsdfg'

app.config["DEBUG"] = True
app.config['MYSQL_HOST'] = 'userauthentication.cgt87kxr0gky.eu-north-1.rds.amazonaws.com'
app.config['MYSQL_USER'] = 'admin'
app.config['MYSQL_PASSWORD'] = 'Pass#123'
app.config['MYSQL_DB'] = 'fullstack' 
app.config['MYSQL_CURSORCLASS']='DictCursor' 
  
 
mysql = MySQL(app)  
@app.route('/')

@app.route('/login', methods =['GET', 'POST'])
def login():
    mesage = ''
    if request.method == 'POST' and 'email' in request.form and 'password' in request.form:
        email = request.form['email']
        password = request.form['password']
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM user WHERE email = % s AND password = % s', (email, password, ))
        user = cursor.fetchone()
        cursor.execute('SELECT * FROM student WHERE email = % s ', (email,  ))
        user1=cursor.fetchone()
        
        
        
        if user:            
            if user['role'] == 'Teacher':
                session['loggedin'] = True
                session['userid'] = user['userid']
                session['name'] = user['name']
                session['email'] = user['email']
                mesage = 'Logged in successfully !'
                return redirect(url_for('users'))
            elif user1:
                session['loggedin'] = True

                session['email']=user1['email']
                msg="Only Teachers can Login"

                return render_template('login.html',mesage=msg)
            else:
                return render_template("register.html")
                 

               
        else:
            mesage = 'Please enter correct email / password !'
    return render_template('login.html', mesage = mesage)
  
@app.route('/logout')

@app.route('/register', methods =['GET', 'POST'])
def register():
    mesage = ''
    if request.method == 'POST' and 'name' in request.form and 'email' in request.form and 'password' in request.form and 'role' and request.form:

        userName = request.form['name']

        email = request.form['email']
        password= request.form['password']
        role=request.form['role']
         
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM user WHERE email = % s', (email, ))
        account = cursor.fetchone()
        if account:
            mesage = 'User already exists !'
        elif not re.match(r'[^@]+@[^@]+\.[^@]+', email):
            mesage = 'Invalid email address !'
          
        else:
            cursor.execute('INSERT INTO user VALUES (NULL, % s, % s, % s, % s)', (userName, email, password,role))
            mysql.connection.commit()
            mesage = 'New user created!'
    elif request.method == 'POST':
        mesage = 'Please fill out the form !'
    return render_template('newuser.html', mesage = mesage)




@app.route('/students', methods =['GET', 'POST'])
def students():
    mesage = ''
    if request.method == 'POST'  :
        viewUserId = request.args.get('id') 
        userName = request.form['name']

        email = request.form['email']
        course= request.form['course']
        division=request.form['Division']
        rollno=request.form['Rollno']
        mentorname=request.form['Mentorname']


        

        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM student WHERE email = % s', (email, ))
        account = cursor.fetchone()
        if account:
            mesage = 'Email allready exists !'
        elif not re.match(r'[^@]+@[^@]+\.[^@]+', email):
            mesage = 'Invalid email address !'
 
        else:
            cursor.execute('INSERT INTO student VALUES (NULL, % s, % s, % s, % s,%s,%s)', (userName, email, course,division,rollno,mentorname))
            mysql.connection.commit()
            mesage = 'New Student created!'
    elif request.method == 'POST':
        mesage = 'Please fill out the form !'
    return render_template('register.html',mesage=mesage)
@app.route("/users", methods =['GET', 'POST'])
def users():
    if 'loggedin' in session:
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute("SELECT * FROM student")
        users = cursor.fetchall()
        cursor.execute("SELECT * FROM user ")
        student = cursor.fetchall()    
        return render_template("users.html", users = users,student=student)
    return redirect(url_for('login'))
@app.route("/edit", methods=['GET', 'POST'])
def edit():
    msg = ''
    if 'loggedin' in session:
        editUserId = request.args.get('userid')
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM student WHERE id = %s', (editUserId,))
        editUser = cursor.fetchone()
        if request.method == 'POST' and 'name' in request.form and 'userid' in request.form and 'email' in request.form and 'course' in request.form and 'division' in request.form and 'rollno' in request.form and 'mentorname' in request.form:
            userName = request.form['name']
            email = request.form['email']
            course = request.form['course']
            division = request.form['division']
            rollno = request.form['rollno']
            mentorname = request.form['mentorname']
            userId = request.form['userid']
            if not re.match(r'[A-Za-z0-9]+', userName):
                msg = 'name must contain only characters and numbers !'
            else:
                cursor.execute(
                    'UPDATE student SET name = %s, email = %s, course = %s, division = %s, rollno = %s, mentor_name = %s WHERE id = %s',
                    (userName, email, course, division, rollno, mentorname, userId,))
                mysql.connection.commit()
                msg = 'User updated !'
                return redirect(url_for('users'))
        elif request.method == 'POST':
            msg = 'Please fill out the form !'
        return render_template("edit.html", msg=msg, editUser=editUser)
    return redirect(url_for('login'))
    
  
@app.route("/password_change", methods =['GET', 'POST'])
def password_change():
    mesage = ''
    if 'loggedin' in session:
        changePassUserId = request.args.get('userid')        
        if request.method == 'POST' and 'password' in request.form and 'confirm_pass' in request.form and 'userid' in request.form  :
            password = request.form['password']   
            confirm_pass = request.form['confirm_pass'] 
            userId = request.form['userid']
            if not password or not confirm_pass:
                mesage = 'Please fill out the form !'
            elif password != confirm_pass:
                mesage = 'Confirm password is not equal!'
            else:
                cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
                cursor.execute('UPDATE user SET  password =% s WHERE userid =% s', (password, (userId, ), ))
                mysql.connection.commit()
                mesage = 'Password updated !'            
        elif request.method == 'POST':
            mesage = 'Please fill out the form !'        
        return render_template("password_change.html", mesage = mesage, changePassUserId = changePassUserId)
    return redirect(url_for('login'))

@app.route("/view/<int:userid>", methods =['GET', 'POST'])
def view(userid):
    id=userid
    if 'loggedin' in session:
        viewUserId = request.args.get('id')   
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM student WHERE id = % s', (id, ))
        user = cursor.fetchone()   
        return render_template("view.html", user = user)
    return redirect(url_for('login'))


@app.route('/delete/<int:userid>', methods=['GET', 'POST'])
def delete(userid):
    if 'loggedin' in session:
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('DELETE FROM student WHERE id = %s', (userid,))
        mysql.connection.commit()
        return redirect(url_for('users'))
    return redirect(url_for('login'))

if __name__ == "__main__":
    app.run(debug=True)
