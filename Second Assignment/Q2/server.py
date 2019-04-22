import socket
import json
import hashlib, binascii, os
import datetime
HOST = '127.0.0.1'
PORT = 1160
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
    def __init__(self, question, choiceA, choiceB, choiceC, choiceD, correct_answer):
        # super(Qquestion, self).__init__()
        self.question = question
        self.choiceA = choiceA
        self.choiceB = choiceB
        self.choiceC = choiceC
        self.choiceD = choiceD
        self.correct_answer = correct_answer

def get_questions():
    questins_file = open('Questions.txt', 'r')
    answers_file  = open('Answers.txt', 'r')
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
    users_file = open('users.txt', 'r+')
    users = users_file.readlines()
    for user in users:
        user = json.loads(user)
        if user['username'] == username:
            return False
    user = {
        'username': username,
        'password': hash_password(password)
    }
    json.dump(user, users_file)
    users_file.write('\n')
    return True

def login(username, password):
    users_file = open('users.txt', 'r+')
    users = users_file.readlines()
    for user in users:
        user = json.loads(user)
        if user['username'] == username:
            return verify_password(user['password'], password)
    return False

def print_result(username, test, result):
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


server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind((HOST, PORT))
server_socket.listen(5)

while True:
    print("Waiting for connection ")
    client_socket, addr = server_socket.accept()
    print("Connection recived from addres ", addr)
    username = ""
    while True:
        request_type = client_socket.recv(BUFFSIZE)
        # client_socket.sendall(b'Input username: ')
        username = client_socket.recv(BUFFSIZE)
        # client_socket.sendall(b'Input password: ')
        password = client_socket.recv(BUFFSIZE)
        if request_type == "register":
            if register(username, password) == True:
                print('Account created for user ', username)
                client_socket.sendall(b'Succesfully Registred!')
                break
            else:
                client_socket.sendall(b'Username alreday exists')
        else:
            if login(username, password) == True:
                print('User ', username, ' has Logedin')
                client_socket.sendall(b'Succesfully Logedin!')
                break
            client_socket.sendall(b'Invaild username and/or password')
    # loged in
    # questins and answers files
    correct = 0
    cnt = 0
    questions = get_questions()
    for i in range(5):
        cur_question = questions[i]
        temp = questions[i]
        correct_answer = cur_question["correct_answer"]
        cur_question["correct_answer"] = "?"
        # cur_question = str(cur_question)
        client_socket.sendall(str(cur_question))
        user_answer = client_socket.recv(BUFFSIZE)
        user_answer +='\n'
        cur_question = temp
        if correct_answer == user_answer:
            correct +=1

    # end of questions
    grade = correct * 100.0 / 5
    grade = str(grade)
    print_result(username, "Python test", grade)
    client_socket.sendall(grade.decode("utf-8"))
    client_socket.close()
