# from http://docs.python.org/2/library/wsgiref.html

from wsgiref.util import setup_testing_defaults
from wsgiref.validate import validator
from wsgiref.simple_server import make_server

# A relatively simple WSGI application. It's going to print out the
# environment dictionary after being updated by setup_testing_defaults
def simple_app(environ, start_response):
    setup_testing_defaults(environ)

    status = '200 OK'
    headers = [('Content-type', 'text/plain')]

    start_response(status, headers)

    ret = ["%s: %s\n" % (key, value)
           for key, value in environ.iteritems()]
    ret.insert(0, "This is your environ.  Hello, world!\n\n")

    return ret

def make_app():
    return simple_app

validator_app = validator(simple_app)
httpd = make_server('', 9569, validator_app)
httpd.serve_forever()
