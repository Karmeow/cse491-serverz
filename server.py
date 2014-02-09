#!/usr/bin/env python
import urlparse
import random
import socket
import time
import cgi
import StringIO
import app

def handle_connection(conn):

    def start_response(status, response_headers):
        return closure()
        
    # Start connection and receive data through headers
    data = conn.recv(1)
    while data[-4:] != '\r\n\r\n':
        data += conn.recv(1)

    # Repurpose code used earlier to parse headers into a dict
    reqc = StringIO.StringIO(data)
    reqc.readline()
    headers = {}
    while (True):
        temp = reqc.readline()
        if temp == "\r\n":
            break

        temp = temp.split("\r\n")[0].split(":", 1)
        headers[temp[0].lower()] = temp[1]

    req = data.split(" ")

    # Extra content if the type is post
    content = ''
    if data.startswith('POST '):
        # Receive the content data, based off the content length header
        while len(content) < int(headers['content-length']):
            content += conn.recv(1)

    
    path = urlparse.urlparse(req[1])
    # Create the environ dict for the app
    environ = {}
    environ['REQUEST_METHOD'] = req[0]
    environ['PATH_INFO'] = path.path
    environ['QUERY_STRING'] = path.query
    if 'content-type' in headers:
        environ['CONTENT_TYPE'] = headers['content-type']
    if 'content-length' in headers:
        environ['CONTENT_LENGTH'] = headers['content-length']
    environ['wsgi.input'] = StringIO.StringIO(content)
    
    def start_response(status, response_headers):
        conn.send('HTTP/1.0 %s' % status)
        conn.send('\r\n')
        conn.send('%s : %s' % (response_headers[0][0], response_headers[0][1]))
        conn.send('\r\n\r\n')

    result = app.simple_app(environ, start_response)

    conn.send(result[0])
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
