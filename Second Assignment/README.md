# Q1
## A
We used Apache server, as we are ubuntu users. To install Apache server we should first update the local package index using the command:
```
sudo apt update
```

Then, install the `apache2` package:

```
sudo apt install apache2
```

To check the service is running, just run the command:
```
sudo systemctl status apache2
```
the output should be something similar to:
```● apache2.service - The Apache HTTP Server
   Loaded: loaded (/lib/systemd/system/apache2.service; enabled; vendor preset: enabled)
  Drop-In: /lib/systemd/system/apache2.service.d
           └─apache2-systemd.conf
   Active: active (running) since Sun 2019-04-21 20:06:23 EEST; 2h 34min ago
  Process: 935 ExecStart=/usr/sbin/apachectl start (code=exited, status=0/SUCCESS)
 Main PID: 1017 (apache2)
    Tasks: 55 (limit: 4327)
   CGroup: /system.slice/apache2.service
           ├─1017 /usr/sbin/apache2 -k start
           ├─1018 /usr/sbin/apache2 -k start
           └─1019 /usr/sbin/apache2 -k start
```
Now the Apache Server is running.
## B
We make the website, four pages with the names:
```
index.html 
p1.html
p2.html
p3.html
```
Page `index.html` is the home page.
Next we place the four pages in the directory:
`/var/www/html/second/Q1/index.html`
## C
To browse the website using the browser, we type these URLs in the browser:
[Home page](http://localhost/second/Q1/)
[page1](http://localhost/second/Q1/p1.html)
[page2](http://localhost/second/Q1/p2.html)
[page3](http://localhost/second/Q1/p3.html)

## D
The solution for this part is in the `code.py` file.
First we import the libraries `socket` and `urllib` the server address is `localhost` port `80` the client connects to the server and sends `GET` request, to retrieve the home page, the request header will be:
```
GET /second/Q1 HTTP/1.0
```
then the client receives the response, the response will be:
```
HTTP/1.1 200 OK
Date: Sun, 21 Apr 2019 20:03:20 GMT
Server: Apache/2.4.29 (Ubuntu)
X-Frame-Options: DENY
X-Content-Type-Options: nosniff
Last-Modified: Sun, 21 Apr 2019 11:25:33 GMT
ETag: "12d-587089c32eaa9"
Accept-Ranges: bytes
Content-Length: 301
Vary: Accept-Encoding
Connection: close
Content-Type: text/html

<!DOCTYPE html>
<html lang="en" dir="ltr">
  <head>
    <meta charset="utf-8">
    <title>Home page</title>
  </head>
  <body>
    <h1>This is the home page.</h1>
    <p><a href="p1.html">page 1</a></p>
    <p><a href="p2.html">page 2</a></p>
    <p><a href="p3.html">page 3</a></p>
  </body>
</html>
```
And we do the same for `page1`
To retrieve the page using `urllib` we use:
```
page = urllib.urlopen('http://localhost/second/Q1/p1.html').read()
```
When we print the `page` we get:
```
<!DOCTYPE html>
<html lang="en" dir="ltr">
  <head>
    <meta charset="utf-8">
    <title>P1</title>
  </head>
  <body>
    <h2>This is page 1</h2>
    <p><a href="index.html">Home page</a></p>
  </body>
</html>
```
## E
To extract the links in the homepage, we need to import `BeautifulSoup` from `bs4`
We used the `HTML parser` included in Python’s standard library and passed it with the `page` variable to the `BeautifulSoup` constructor. then used the parser to extract the links using:
```
links = soup.find_all('a')
```

