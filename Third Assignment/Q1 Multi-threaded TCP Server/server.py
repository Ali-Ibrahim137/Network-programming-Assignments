import sqlite3
import socket
import json
import hashlib, binascii, os
import datetime
from threading import Thread
HOST = '127.0.0.1'
PORT = 6666
BUFFSIZE = 2048


def hash_password(password):
    """Hash a password for storing."""
    salt = hashlib.sha256(os.urandom(60)).hexdigest().encode('ascii')
    pwdhash = hashlib.pbkdf2_hmac('sha512', password.encode('utf-8'),
                                salt, 100000)
    pwdhash = binascii.hexlify(pwdhash)
    return (salt + pwdhash).decode('ascii')

def verify_password(stored_password, provided_password):
    """Verify a stored password against one provided by user"""
    salt = stored_password[:64]
    stored_password = stored_password[64:]
    pwdhash = hashlib.pbkdf2_hmac('sha512',
                                  provided_password.encode('utf-8'),
                                  salt.encode('ascii'),
                                  100000)
    pwdhash = binascii.hexlify(pwdhash).decode('ascii')
    return pwdhash == stored_password

class Question(object):
    """docstring for question."""
    def __init__(self, question, choiceA,
        choiceB, choiceC, choiceD, correct_answer):
        # super(Qquestion, self).__init__()
        self.question = question
        self.choiceA = choiceA
        self.choiceB = choiceB
        self.choiceC = choiceC
        self.choiceD = choiceD
        self.correct_answer = correct_answer

def get_questions(test):
    questins_file = open(test + '_Questions.txt', 'r')
    answers_file  = open(test + '_Answers.txt', 'r')
    q_lines = questins_file.readlines()
    correct_answers = answers_file.readlines()
    ret = []
    cur_question = Question("Q", "A", "B", "C", "D", "?")
    c = 0
    cnt = 0
    for q in q_lines:
        if q[0]=='-':
            correct_answer = correct_answers[cnt]
            cnt+=1
            cur_question.correct_answer = correct_answer
            cur_question = json.dumps(cur_question.__dict__)
            cur_question = json.loads(cur_question)
            ret.append(cur_question)
            c = 0
            cur_question = Question("Q", "A", "B", "C", "D", "?")
            continue
        if c == 0:
            cur_question.question = q
        elif c == 1:
            cur_question.choiceA = q
        elif c == 2:
            cur_question.choiceB = q
        elif c == 3:
            cur_question.choiceC = q
        elif c == 4:
            cur_question.choiceD = q
        c+=1
    return ret

def register(username, password):
    if len(query_user(username))!=0:
        return False
    insert_user(username, password)
    return True

def login(username, password):
    user = query_user(username)
    if len(user)!=0 and verify_password(user[0][1], password):
        return True
    return False

def send_threads(client_socket):
    mes = ""
    for thread in threads:
        mes += (str(thread.ip) + ':' + str(thread.port) + '\n')
    client_socket.send(mes)
    print("in send_threads function!")

class ClientThread(Thread):
    def __init__(self, ip, port, count):
        Thread.__init__(self)
        self.ip = ip
        self.port = port
        self.count = count
        self.name = 'Thread - ' + str(count)
        print "[+] New server socket thread started for " + ip + ":" + str(port)

    def run(self):
        if(self.count == 7):
            client_socket.sendall("Congratulations you are the sevnth user!!!")
            send_threads(client_socket)
        else:
            client_socket.sendall("Welcome to the server!")
        username = authinticate(client_socket)
        do_exam(client_socket, username)
        print('closing socket for user ' + username)
        client_socket.close()

def do_exam(client_socket, username):
    test = client_socket.recv(BUFFSIZE)
    if test=="1":
        test = 'math'
    else:
        test = 'python'
    # loged in
    # questins and answers files
    correct = 0
    cnt = 0
    questions = get_questions(test)
    for i in range(5):
        cur_question = questions[i]
        temp = questions[i]
        correct_answer = cur_question["correct_answer"]
        cur_question["correct_answer"] = "?"
        client_socket.sendall(str(cur_question))
        user_answer = client_socket.recv(BUFFSIZE)
        user_answer +='\n'
        cur_question = temp
        if correct_answer == user_answer:
            correct +=1
    # end of questions
    grade = correct * 100.0 / 5
    grade = str(grade)
    add_to_log(username, test, grade)
    client_socket.sendall(grade.decode("utf-8"))

def authinticate(client_socket):
    username = ""
    while True:
        request_type = client_socket.recv(BUFFSIZE)
        username = client_socket.recv(BUFFSIZE)
        password = client_socket.recv(BUFFSIZE)
        if request_type == "register":
            if register(username, password) == True:
                print('Account created for user ', username)
                client_socket.sendall(b'Succesfully Registred!')
                break
            else:
                client_socket.sendall(b'Username alreday exists')
        elif request_type=="login":
            if login(username, password) == True:
                print('User ', username, ' has Logedin')
                client_socket.sendall(b'Succesfully Logedin!')
                break
            client_socket.sendall(b'Invaild username and/or password')
        else:
            client_socket.sendall(b'Please chose a valid command.')
    return username

def add_to_log(username, test, result):
    date = str(datetime.datetime.now())
    log_file = open('log.txt', 'a')
    s = "|" + username
    while True:
        if len(s) == 27:
            s+='|'
            break;
        s+=' '
    s+=test
    while True:
        if len(s) == 41:
            s+='|'
            break;
        s+=' '
    s+=result
    while True:
        if len(s) == 50:
            s+='|'
            break;
        s+=' '
    s+=date
    while True:
        if len(s) >= 80:
            s+='|'
            break;
        s+=' '
    s+='\n'
    log_file.write(s)
    s = '|--------------------------|-------------|--------|-----------------------------|\n'
    log_file.write(s)

def create_db():
    con=sqlite3.connect("users.db")
    cur=con.cursor()
    cur.execute('CREATE TABLE if not exists users (username TEXT, password TEXT)')
    con.commit()
    con.close()

def insert_user(username, password):
    con=sqlite3.connect("users.db")
    cur=con.cursor()
    password = hash_password(password)
    cur.execute("INSERT INTO users values(?,?)",(username,password))
    con.commit()
    con.close()

def query_user(username):
    con=sqlite3.connect("users.db")
    cur=con.cursor()
    cur.execute("SELECT * from users where username=?",(username,))
    data=cur.fetchall()
    con.commit()
    con.close()
    return data

if __name__=='__main__':
    create_db()
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((HOST, PORT))
    threads = []
    while True:
        server_socket.listen(10)
        print("Waiting for connections ")
        (client_socket, (ip,port)) = server_socket.accept()
        new_thread = ClientThread(ip,port, len(threads) + 1)
        new_thread.start()
        threads.append(new_thread)
