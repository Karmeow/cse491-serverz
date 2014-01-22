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
        self.sent += s

    def close(self):
        self.is_closed = True

# Test a basic GET call.

def test_handle_connection():
    conn = FakeConnection("GET / HTTP/1.0\r\n\r\n")
    expected_return = 'HTTP/1.0 200 OK\r\n' + \
                      'Content-type: text/html\r\n' + \
                      '\r\n' + \
                      '<h1>Hello, world.</h1>' + \
                      'This is Karmeow\'s Web server.' + \
                      '<p><a href="/content">Content :)</a></p>' + \
                      '<p><a href="/file">File :)</a></p>' + \
                      '<p><a href="/image">Image :(</a></p>'

    server.handle_connection(conn)

    assert conn.sent == expected_return, 'Got: %s' % (repr(conn.sent),)

def test_handle_content_connection():
    conn = FakeConnection("GET /content HTTP/1.0\r\n\r\n")
    expected_return = 'HTTP/1.0 200 OK\r\n' + \
                      'Content-type: text/html\r\n' + \
                      '\r\n' + \
                      '<b>Ya\'ll requested some content</b>'

    server.handle_connection(conn)

    assert conn.sent == expected_return, 'Got: %s' % (repr(conn.sent),)

def test_handle_file_connection():
    conn = FakeConnection("GET /file HTTP/1.0\r\n\r\n")
    expected_return = 'HTTP/1.0 200 OK\r\n' + \
                      'Content-type: text/html\r\n' + \
                      '\r\n' + \
                      '<b>Ya\'ll requested some file</b>'

    server.handle_connection(conn)

    assert conn.sent == expected_return, 'Got: %s' % (repr(conn.sent),)

def test_handle_image_connection():
    conn = FakeConnection("GET /image HTTP/1.0\r\n\r\n")
    expected_return = 'HTTP/1.0 200 OK\r\n' + \
                      'Content-type: text/html\r\n' + \
                      '\r\n' + \
                      '<b>Ya\'ll requested some image</b>'

    server.handle_connection(conn)

    assert conn.sent == expected_return, 'Got: %s' % (repr(conn.sent),)

def test_post_connection():
    conn = FakeConnection("POST /send-post-request HTTP/1.0\r\n\r\n")
    expected_return = 'hello world'

    server.handle_connection(conn)

    assert conn.sent == expected_return, 'Got: %s' % (repr(conn.sent),)

