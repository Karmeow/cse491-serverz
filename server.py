#!/usr/bin/env python
import urlparse
import random
import socket
import time

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

def handle_connection(conn):
    data = conn.recv(1000)

    if (not (data)):   # Bye indexing error
        return

    poststr = data
    data = data.split(" ")

    parse = urlparse.urlparse(data[1])
    if (parse.query):
        queryParse = urlparse.parse_qs(parse.query)


    if (data[0] == "POST"):
        if (poststr.find("application/x-www-form-urlencoded") != -1):
            fni = poststr.find('firstname')
            queryParse = urlparse.parse_qs(poststr[fni:])
            ok200Response(conn)
            submit(conn, queryParse)

    elif (data[0] == "GET"):
        ok200Response(conn)

        if (parse.path == "/content"):
            content(conn)

        elif (parse.path == "/form"):
            form(conn)

        elif (parse.path == "/submit"):
		    submit(conn, queryParse)

        elif (parse.path == "/file"):
            file(conn)

        elif (parse.path == "/image"):
            image(conn)

        elif (parse.path == "/"):
            index(conn)

        else:
            # @karabonk TODO add exception code
		    conn.send("NOPE")

    else:
        # @karabonk TODO add exception code
        conn.send("NOPE")

    conn.close()

def ok200Response(conn):
    conn.send("HTTP/1.0 200 OK\r\n")
    conn.send("Content-Type: text/html\r\n")
    conn.send("\r\n")

def index(conn):
    conn.send("<h1>Hello, world.</h1>")
    conn.send("This is Karmeow's Web server.")
    conn.send('<p><a href="/content">Content :)</a></p>')
    conn.send('<p><a href="/file">File :)</a></p>')
    conn.send('<p><a href="/image">Image :(</a></p>')
    conn.send('<p><a href="/form">Form</a></p>')

def submit(conn, qP):
    sendString = "<h1>Hello Mr. %s %s</h1>" % (qP['firstname'][0], qP['lastname'][0])
    conn.send(sendString)

def image(conn):
    conn.send("<b>Ya'll requested some image</b>")

def file(conn):
    conn.send("<b>Ya'll requested some file</b>")

def content(conn):
    conn.send("<b>Ya'll requested some content</b>")

def form(conn):
    conn.send("<form action='/submit' method='GET'>")
    conn.send("First Name:<input type='text' name='firstname'><br>")
    conn.send("Last Name:<input type='text' name='lastname'>")
    conn.send("<input type='submit' value='Submit'>")
    conn.send("</form>")

if __name__ == '__main__':
    main()
