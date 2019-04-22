import socket
import json
HOST = '127.0.0.1'
PORT = 1160
BUFFSIZE = 2048

client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect((HOST, PORT))
while True:
    # login/register
    request_type = raw_input('register or login? ')
    client_socket.sendall(request_type)
    username = raw_input('Input username ')
    client_socket.sendall(username)
    password = raw_input('Input password ')
    client_socket.sendall(password)
    response = client_socket.recv(BUFFSIZE)
    print(response)
    if response == 'Succesfully Registred!' or response == 'Succesfully Logedin!':
        break
for i in range(5):
    data = client_socket.recv(BUFFSIZE)
    data = eval(data)
    print(data["question"])
    print(data["choiceA"])
    print(data["choiceB"])
    print(data["choiceC"])
    print(data["choiceD"])
    user_answer = raw_input('Input your answer for this question ')
    client_socket.sendall(user_answer.decode("utf-8"))
grade = client_socket.recv(BUFFSIZE)
client_socket.close()
print('Your grade is ' + str (grade))
