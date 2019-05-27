from flask import Flask,render_template,redirect,url_for,request
import sqlite3
def con_db():
    con=sqlite3.connect("Student_log.db")
    cur=con.cursor()
    cur.execute("create table if not exists Fifth_students(Name text, ID integer, Age integer)")
    con.commit()
    con.close()

def insert_student(S_Name, S_ID, S_Age):
    con=sqlite3.connect("Student_log.db")
    cur=con.cursor()
    cur.execute("insert into Fifth_students values(?,?,?)",(S_Name,S_ID,S_Age))
    con.commit()
    con.close()

def clear_students():
    con=sqlite3.connect("Student_log.db")
    cur=con.cursor()
    cur.execute("delete from Fifth_students")
    con.commit()
    con.close()

def selectall_student():
    con=sqlite3.connect("Student_log.db")
    cur=con.cursor()
    cur.execute("select * from Fifth_students")
    data=cur.fetchall()
    con.commit()
    con.close()
    return(data)

def selectone_student(S_ID):
    con=sqlite3.connect("Student_log.db")
    cur=con.cursor()
    cur.execute("select * from Fifth_students where ID=?",(S_ID,))
    data=cur.fetchall()
    con.commit()
    con.close()
    return(data)

app = Flask('__main__')
@app.route('/')
def home():
    return(redirect(url_for("login")))

@app.route('/login')
def login():
    return(render_template("login.html"))
@app.route('/handlelogin', methods=['POST'])
def handlelogin():
    _ID=request.form.get('ID')
    if selectone_student(_ID):
        l=selectone_student(_ID)
        print(l)
        Name=l[0][0]
        ID=l[0][1]
        Age=l[0][2]
        return(render_template('handlelogin.html', Name=Name ,ID=ID, Age=Age))
    else:
     return(render_template('error.html'))


if __name__=='__main__':
    con_db()
    clear_students()
    insert_student('Karam',1711,23)
    insert_student('Ali',1866,23)
    insert_student('Suzan',1709,22)
    insert_student('Sara',1800,23)
    app.run()
