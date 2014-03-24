#!/usr/bin/env python
import urlparse
import random
import socket
import time
import cgi
import StringIO
import app
import argparse
import sys

import imageapp
import quixote
from quixote.demo.altdemo import create_publisher
from wsgiref.validate import validator

_the_app = None
def make_app():
    global _the_app

    if _the_app is None:
        p = create_publisher()
        _the_app = quixote.get_wsgi_app()

    return _the_app

def handle_connection(conn, pargs):

    # Start connection and receive data through headers
    data = conn.recv(1)
    while data[-4:] != '\r\n\r\n':
        bit = conn.recv(1)
        if bit == '':
            return
        else:
            data += bit

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
    environ['SERVER_NAME'] = pargs['host']
    environ['SERVER_PORT'] = str(pargs['p'])
    if 'content-type' in headers:
        environ['CONTENT_TYPE'] = headers['content-type']
    if 'content-length' in headers:
        environ['CONTENT_LENGTH'] = headers['content-length']
    environ['wsgi.input'] = StringIO.StringIO(content)
    environ['wsgi.errors'] = sys.stderr
    environ['wsgi.multithread'] = 0
    environ['wsgi.multiprocess'] = 0
    environ['wsgi.run_once'] = 0
    environ['wsgi.url_scheme'] = 'http'
    environ['wsgi.version'] = (1,0)
    environ['SCRIPT_NAME'] = ''
    if 'cookie' in headers:
        environ['HTTP_COOKIE'] = headers['cookie']
    else:
        environ['HTTP_COOKIE'] = ''

    print "%s %s" %(req[0], path.path)

    def start_response(status, response_headers):
        conn.send('HTTP/1.0 %s' % status)
        conn.send('\r\n')

        for head in response_headers:
            key, value = head
            conn.send('%s: %s' % (key, value))
            conn.send('\r\n')

        conn.send('\r\n')

    if (pargs['A'] == 'altdemo'):
        _the_app = make_app()

    elif (pargs['A'] == 'myapp'):
        _the_app = app.make_app()

    else:
        _the_app = quixote.get_wsgi_app()

    #app1 = quixote.get_wsgi_app()
    result = _the_app(environ, start_response)

    for data in result:
        try:
            conn.send(data)
        except socket.error:
            break

    ##result.close()
    conn.close()

def main():
    parser = argparse.ArgumentParser(description='Process server info')
    parser.add_argument('-A', default='image', choices=['image', 'altdemo', 'myapp'],
                       type=str)
    parser.add_argument('-p', type=int, choices=range(8000,10000),
                        default=random.randint(8000,9999))
    args = parser.parse_args()
    args = vars(args)

    if args['A'] == 'image':
        imageapp.setup()
        x = imageapp.create_publisher()

    s = socket.socket()         # Create a socket object
    host = socket.getfqdn()     # Get local machine name
    port = args['p']
    s.bind((host, port))        # Bind to the port
    args['host'] = host

    print 'Starting server on', host, port
    print 'The Web server URL for this would be http://%s:%d/' % (host, port)

    s.listen(5)                 # Now wait for client connection.

    print 'Entering infinite loop; hit CTRL-C to exit'
    while True:
        # Establish connection with client.
        c, (client_host, client_port) = s.accept()
        print 'Got connection from', client_host, client_port

        try:
            handle_connection(c, args)
        finally:
            imageapp.teardown()



if __name__ == '__main__':
    main()
