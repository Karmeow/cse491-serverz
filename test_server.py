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
# ^ ~CAT : This is the ONLY comment in the file, and it just seems out of place.
# Either document them all, or document none. Obviously the former is more
# preferred.
# Here's an optional suggested format for function declarations:
# def function_name(params):
#     "Function Documentation"
#     # Code goes here
#
# If you use this format, I think you'll start to like it quite a bit. You can
# also use triple-quoted strings for the function documentation, just like ctb
# did with the documentation on the FakeConnection class above.
# Again, just a suggestion, but either way, BE CONSISTENT is the big deal.

def test_handle_connection():
    conn = FakeConnection("GET / HTTP/1.0\r\n\r\n")
    expected_return = 'HTTP/1.0 200 OK\r\n' + \
                      'Content-Type: text/html\r\n' + \
                      '\r\n' + \
                      '<h1>Hello, world.</h1>' + \
                      'This is Karmeow\'s Web server.' + \
                      '<p><a href="/content">Content :)</a></p>' + \
                      '<p><a href="/file">File :)</a></p>' + \
                      '<p><a href="/image">Image :(</a></p>' + \
                      '<p><a href="/form">Form</a></p>'

    server.handle_connection(conn)

    assert conn.sent == expected_return, 'Got: %s' % (repr(conn.sent),)

def test_handle_content_connection():
    conn = FakeConnection("GET /content HTTP/1.0\r\n\r\n")
    expected_return = 'HTTP/1.0 200 OK\r\n' + \
                      'Content-Type: text/html\r\n' + \
                      '\r\n' + \
                      '<b>Ya\'ll requested some content</b>'

    server.handle_connection(conn)

    assert conn.sent == expected_return, 'Got: %s' % (repr(conn.sent),)

def test_handle_file_connection():
    conn = FakeConnection("GET /file HTTP/1.0\r\n\r\n")
    expected_return = 'HTTP/1.0 200 OK\r\n' + \
                      'Content-Type: text/html\r\n' + \
                      '\r\n' + \
                      '<b>Ya\'ll requested some file</b>'

    server.handle_connection(conn)

    assert conn.sent == expected_return, 'Got: %s' % (repr(conn.sent),)

def test_handle_image_connection():
    conn = FakeConnection("GET /image HTTP/1.0\r\n\r\n")
    expected_return = 'HTTP/1.0 200 OK\r\n' + \
                      'Content-Type: text/html\r\n' + \
                      '\r\n' + \
                      '<b>Ya\'ll requested some image</b>'

    server.handle_connection(conn)

    assert conn.sent == expected_return, 'Got: %s' % (repr(conn.sent),)

def test_form_connection():
    conn = FakeConnection('GET /submit?firstname=Robert&lastname=Paulson' + \
                          'HTTP/1.0\r\n\r\n')
    expected_return = 'HTTP/1.0 200 OK\r\n' + \
                      'Content-Type: text/html\r\n' + \
                      '\r\n' + \
                      '<h1>Hello Mr. Robert Paulson' + \
                      'HTTP/1.0\r\n\r\n</h1>'

    server.handle_connection(conn)

    assert conn.sent == expected_return, 'Got: %s' % (repr(conn.sent),)

def test_post_connection():
    conn = FakeConnection('POST / HTTP/1.0\r\n' + \
            'From: test@testserver\r\n' + \
            'Content-Type: application/x-www-form-urlencoded\r\n'
            'Content-Length: 33\r\n' + \
            'firstname=Robert&lastname=Paulson\r\n' + \
            '\r\n')

    expected_return = 'HTTP/1.0 200 OK\r\n' + \
                      'Content-Type: text/html\r\n' + \
                      '\r\n' + \
                      '<h1>Hello Mr. Robert Paulson\r\n\r\n</h1>'


    server.handle_connection(conn)

    assert conn.sent == expected_return, 'Got: %s' % (repr(conn.sent),)


# ~CAT : You didn't test for failure conditions...
# What happens if a PUT or DELETE comes in? Or a page that doesn't exist?
