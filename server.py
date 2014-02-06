#!/usr/bin/env python
import urlparse
import random
import socket
import time
import cgi
import StringIO
import jinja2

def handle_connection(conn):
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

    # Parse the path and add query dictionary to the render vars
    url = urlparse.urlparse(req[1])
    renvars = urlparse.parse_qs(url.query)

    # Extra content if the type is post
    content = ''
    if data.startswith('POST '):
        # Receive the content data, based off the content length header
        while len(content) < int(headers['content-length']):
            content += conn.recv(1)
    print (data,)
    print (content,)
    environ = {}
    environ['REQUEST_METHOD'] = 'POST'

    fs = cgi.FieldStorage(fp = StringIO.StringIO(content), headers=headers \
                              , environ=environ)
    print fs.keys()
    # Add post data to the render vars
    renvars.update(dict([(x, [fs[x].value]) for x in fs.keys()]))

    # Dict of current possible paths
    pages = { '/' : 'index.html', \
              '/content' : 'content.html', \
              '/image' : 'image.html', \
              '/file' : 'file.html', \
              '/form' : 'form.html', \
              '/submit' : 'submit.html' }

    loader = jinja2.FileSystemLoader('./templates')
    env = jinja2.Environment(loader=loader)
    status = 'HTTP/1.0 200 OK\r\nContent-Type: text/html\r\n\r\n'

    if data.startswith('POST '):
        template = env.get_template('submit.html')

    elif url.path in pages:
        template = env.get_template(pages[url.path])

    else:
        template = env.get_template('404.html')
        status = 'HTTP/1.0 404 Not Found\r\nContent-Type: text/html\r\n\r\n'


    status += template.render(renvars)
    conn.send(status)

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
