import server

class FakeConnection(object):
    """
    A fake connection class that mimics a real TCP socket for the purpose
    of testing socket I/O.
    """
    def __init__(self, to_recv):
        self.to_recv = to_recv
        self.sent = ""
        self.is_closed = False

    def recv(self, n):
        if n > len(self.to_recv):
            r = self.to_recv
            self.to_recv = ""
            return r

        r, self.to_recv = self.to_recv[:n], self.to_recv[n:]
        return r

    def send(self, s):
        if len(self.sent) < 10000:  # For huge resolution images
            self.sent += s


    def close(self):
        self.is_closed = True

def test_handle_connection():
    conn = FakeConnection("GET / HTTP/1.0\r\n\r\n")
    expected_return = 'HTTP/1.0 200 OK'
    server.handle_connection(conn)
    splitconn = conn.sent.split('\r\n')[0]

    assert splitconn == expected_return, 'Got: %s' %(repr(conn.sent),)

def test_handle_content_connection():
    conn = FakeConnection("GET /content HTTP/1.0\r\n\r\n")
    expected_return = 'HTTP/1.0 200 OK'

    server.handle_connection(conn)
    splitconn = conn.sent.split('\r\n')[0]

    assert splitconn == expected_return, 'Got: %s' %(repr(conn.sent),)

def test_handle_file_connection():
    conn = FakeConnection("GET /file HTTP/1.0\r\n\r\n")
    expected_return = 'HTTP/1.0 200 OK'

    server.handle_connection(conn)
    splitconn = conn.sent.split('\r\n')[0]

    assert splitconn == expected_return, 'Got: %s' %(repr(conn.sent),)

def test_handle_image_connection():
    conn = FakeConnection("GET /image HTTP/1.0\r\n\r\n")
    expected_return = 'HTTP/1.0 200 OK'

    server.handle_connection(conn)
    splitconn = conn.sent.split('\r\n')[0]

    assert splitconn == expected_return, 'Got: %s' %(repr(conn.sent),)

def test_form_connection():
    conn = FakeConnection('GET /submit?firstname=Robert&lastname=Paulson' + \
                          ' HTTP/1.0\r\n\r\n')
    expected_return = 'HTTP/1.0 200 OK'

    server.handle_connection(conn)
    splitconn = conn.sent.split('\r\n')[0]

    assert splitconn == expected_return, 'Got: %s' %(repr(conn.sent),)

def test_app_post_connection():
    conn = FakeConnection('POST / HTTP/1.0\r\n' + \
            'From: test@testserver\r\n' + \
            'Content-Type: application/x-www-form-urlencoded\r\n'
            'Content-Length: 33\r\n' + \
            '\r\n'
            'firstname=Robert&lastname=Paulson')

    expected_return = 'HTTP/1.0 200 OK'


    server.handle_connection(conn)
    splitconn = conn.sent.split('\r\n')[0]

    assert splitconn == expected_return, 'Got: %s' %(repr(conn.sent),)

def test_multi_post_connection():
    conn = FakeConnection('POST /submit HTTP/1.1\r\n' + \
        'Host: arctic.cse.msu.edu:9684\r\n' + \
        'Connection: keep-alive\r\n' + \
        'Content-Length: 248\r\n' + \
        'Content-Type: multipart/form-data; boundary=----' + \
        'WebKitFormBoundaryeDbkALVq8cSTv4RB\r\n\r\n' + \
        '------WebKitFormBoundaryeDbkALVq8cSTv4RB\r\n' + \
        'Content-Disposition: form-data; name="firstname"\r\n\r\n' +
        'Robert\r\n------WebKitFormBoundaryeDbkALVq8cSTv4RB\r\n' +
        'Content-Disposition: form-data; name="lastname"\r\n\r\n' +
        'Paulson\r\n------WebKitFormBoundaryeDbkALVq8cSTv4RB--\r\n')

    expected_return = 'HTTP/1.0 200 OK'

    server.handle_connection(conn)
    splitconn = conn.sent.split('\r\n')[0]

    assert splitconn == expected_return, 'Got: %s' %(repr(conn.sent),)

def test_bad_connection():
    conn = FakeConnection('GET /autobiography HTTP/1.0\r\n\r\n')

    expected_return = 'HTTP/1.0 404 Not Found'

    server.handle_connection(conn)
    splitconn = conn.sent.split('\r\n')[0]

    assert splitconn == expected_return, 'Got: %s' %(repr(conn.sent),)

def test_put_connection():
    conn = FakeConnection('PUT / HTTP/1.0\r\n\r\n')

    expected_return = 'HTTP/1.0 404 Not Found'

    server.handle_connection(conn)
    splitconn = conn.sent.split('\r\n')[0]

    assert splitconn == expected_return, 'Got: %s' %(repr(conn.sent),)

