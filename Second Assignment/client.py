import socket
HOST = '127.0.0.1'
PORT = 1234
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

number_of_questions = int(client_socket.recv(BUFFSIZE))
print("You have " + str (number_of_questions) + ' questins to answer, Good Luck! ')
while True:
    data = client_socket.recv(BUFFSIZE)
    if data[3:5]=='--':
        user_answer = raw_input('Input your answer for this question ')
        client_socket.sendall(user_answer.decode("utf-8"))
        number_of_questions -=1
        if number_of_questions == 0:
            break
        continue
    print(data)

grade = client_socket.recv(BUFFSIZE)
client_socket.close()
print('Your grade is ' + str (grade))
