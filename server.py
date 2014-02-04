#!/usr/bin/env python
import urlparse
import random
import socket
import time

def index(conn, url):
    conn.send("HTTP/1.0 200 OK\r\n")
    conn.send("Content-Type: text/html\r\n")
    conn.send("\r\n")
    conn.send("<h1>Hello, world.</h1>")
    conn.send("This is Karmeow's Web server.")
    conn.send('<p><a href="/content">Content :)</a></p>')
    conn.send('<p><a href="/file">File :)</a></p>')
    conn.send('<p><a href="/image">Image :(</a></p>')
    conn.send('<p><a href="/form">Form</a></p>')

def submit(conn, url):
    print url
    queryParse = urlparse.parse_qs(url.query)
    conn.send("HTTP/1.0 200 OK\r\n")
    conn.send("Content-Type: text/html\r\n")
    conn.send("\r\n")
    sendString = "<h1>Hello Mr. %s %s</h1>" % (queryParse['firstname'][0], \
    queryParse['lastname'][0])
    conn.send(sendString)

def image(conn, url):
    conn.send("HTTP/1.0 200 OK\r\n")
    conn.send("Content-Type: text/html\r\n")
    conn.send("\r\n")
    conn.send("<b>Ya'll requested some image</b>")

def file(conn, url):
    conn.send("HTTP/1.0 200 OK\r\n")
    conn.send("Content-Type: text/html\r\n")
    conn.send("\r\n")
    conn.send("<b>Ya'll requested some file</b>")

def content(conn, url):
    conn.send("HTTP/1.0 200 OK\r\n")
    conn.send("Content-Type: text/html\r\n")
    conn.send("\r\n")
    conn.send("<b>Ya'll requested some content</b>")

def form(conn, url):
    conn.send("HTTP/1.0 200 OK\r\n")
    conn.send("Content-Type: text/html\r\n")
    conn.send("\r\n")
    conn.send("<form action='/submit' method='GET'>")
    conn.send("First Name:<input type='text' name='firstname'><br>")
    conn.send("Last Name:<input type='text' name='lastname'>")
    conn.send("<input type='submit' value='Submit'>")
    conn.send("</form>")

def post(conn, url):
    fni = url.find('firstname')
    queryParse = urlparse.parse_qs(url[fni:])
    conn.send("HTTP/1.0 200 OK\r\n")
    conn.send("Content-Type: text/html\r\n")
    conn.send("\r\n")
    sendString = "<h1>Hello Mr. %s %s</h1>" % (queryParse['firstname'][0], \
    queryParse['lastname'][0])
    conn.send(sendString)


def handle_connection(conn):
    data = conn.recv(1000)

    if (not (data)):   # Bye indexing error
        return

    poststr = data
    data = data.split(" ")

    url = urlparse.urlparse(data[1])

    if (data[0] == "POST"):
        if (poststr.find("application/x-www-form-urlencoded") != -1):
            post(conn, poststr)

    elif (data[0] == "GET"):

        if (url.path == "/content"):
            content(conn, url)

        elif (url.path == "/form"):
            form(conn, url)

        elif (url.path == "/submit"):
		    submit(conn, url)

        elif (url.path == "/file"):
            file(conn, url)

        elif (url.path == "/image"):
            image(conn, url)

        elif (url.path == "/"):
            index(conn, url)

        else:
            # @karabonk TODO add exception code
		    conn.send("NOPE")

    else:
        # @karabonk TODO add exception code
        conn.send("NOPE")

    conn.close()

def main():
    s = socket.socket()         # Create a socket object
    host = socket.getfqdn() # Get local machine name
    port = random.randint(8000, 9999)
    s.bind((host, port))        # Bind to the port

    print 'Starting server on', host, port
    print 'The Web server URL for this would be http://%s:%d/' % (host, port)

    s.listen(5)                 # Now wait for client connection.

    print 'Entering infinite loop; hit CTRL-C to exit'
    while True:
        # Establish connection with client.
        c, (client_host, client_port) = s.accept()
        print 'Got connection from', client_host, client_port
        handle_connection(c)



if __name__ == '__main__':
    main()
