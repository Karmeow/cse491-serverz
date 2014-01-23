#!/usr/bin/env python
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
    data = data.split(" ")

    if (data[0] == "POST"):
        conn.send("hello world")

    else:
        conn.send("HTTP/1.0 200 OK\r\n")
        conn.send("Content-Type: text/html\r\n")
        # ~CAT :           ^ This should be capital to meet HTML spec. Fixed.
        conn.send("\r\n")

        if (data[1] == "/content"):
            conn.send("<b>Ya'll requested some content</b>")

        elif (data[1] == "/file"):
            conn.send("<b>Ya'll requested some file</b>")

        elif (data[1] == "/image"):
            conn.send("<b>Ya'll requested some image</b>")

        else:
            # ~CAT: Doing it this way is technically OK, if you don't want
            #  people to know if they tried accessing a page that doesn't exist.
            # IE: Try accessing "/foobar". Do you want that to assume they want
            #  the index, or would you rather tell them that 'foobar' doesn't
            #  exist?
            #  Whichever way you want to do it is fine, just make sure your
            #  intentions are made clear.
            conn.send("<h1>Hello, world.</h1>")
            conn.send("This is Karmeow's Web server.")
            conn.send('<p><a href="/content">Content :)</a></p>')
            conn.send('<p><a href="/file">File :)</a></p>')
            conn.send('<p><a href="/image">Image :(</a></p>')

    conn.close()

if __name__ == '__main__':
    main()
