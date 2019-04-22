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
print('Chose the test you want to make, avilable tests are: math and python')
print('1 for math')
print('2 for python')
test = raw_input()
client_socket.sendall(test)
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
