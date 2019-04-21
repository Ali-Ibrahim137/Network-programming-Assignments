import socket
import urllib
from bs4 import BeautifulSoup

# retrive the page using socket:
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)   # define client socket
server_address = ('localhost', 80)                                  # server address
client_socket.connect(server_address)                               # connect to the server

request_header = 'GET /second/ HTTP/1.0\r\n\r\n'                    # define request header for the home page
client_socket.send(request_header)                                  # send the request
# recive the response
response = ''
while True:
    recv = client_socket.recv(1024)
    if not recv:
        break
    response += recv

# print the response
print('response from the home page:')
print(response)

client_socket.close()                                               # close the socket

client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)   # define client socket
client_socket.connect(server_address)                               # connect to the server


request_header = 'GET /second/p1.html HTTP/1.0\r\n\r\n'             # define request header for page p1
client_socket.send(request_header)                                  # send the request
# recive the response
response = ''
while True:
    recv = client_socket.recv(1024)
    if not recv:
        break
    response += recv
# print the response
print('response from page p1:')
print(response)
client_socket.close()                                               # close the socket

for i in range(3):
    print('\n')

# retrive the page using urllib:
url  = 'http://localhost/second/p1.html'
page = urllib.urlopen(url).read()
print('page p1:')
print(page)

url  = 'http://localhost/second/index.html'
page = urllib.urlopen(url).read()
print('the home page:')
print(page)


for i in range(3):
    print('\n')

# list of linkes:
soup = BeautifulSoup(page, 'html.parser')
links = soup.find_all('a')
for link in links:
    print(link.get('href') + '  ' + link.get_text())
