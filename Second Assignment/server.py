import socket
import json
import hashlib, binascii, os
HOST = '127.0.0.1'
PORT = 1234
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






server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind((HOST, PORT))
server_socket.listen(5)
while True:
    print("Waiting for connection ")
    client_socket, addr = server_socket.accept()
    print("Connection recived from addres ", addr)
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
    questins = open('Questions.txt', 'r')
    answers  = open('Answers.txt', 'r')
    correct = 0
    question_count = 0
    # read the questions file
    q_lines = questins.readlines()
    correct_answers = answers.readlines()
    number_of_questions = len(correct_answers)
    client_socket.sendall(str(number_of_questions).decode("utf-8"))
    for q_line in q_lines:
        client_socket.sendall(q_line.decode("utf-8"))
        if q_line[3:5]=='--':
            # questins are seperated by a line of dashes -
            correct_answer = correct_answers[question_count]
            user_answer = client_socket.recv(BUFFSIZE)
            user_answer +='\n'
            question_count +=1
            if correct_answer == user_answer:
                correct +=1
            if question_count == number_of_questions:
                break
            continue

    # end of questions
    grade = correct * 100.0 / question_count
    grade = str(grade)
    client_socket.sendall(grade.decode("utf-8"))
    client_socket.close()
