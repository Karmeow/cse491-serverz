import cgi
import jinja2
import urlparse
from StringIO import StringIO
from wsgiref.util import setup_testing_defaults

def simple_app(environ, start_response):

    renvars = urlparse.parse_qs(environ['QUERY_STRING'])

    # Extract some headers for field storage to work properly
    headers = {}
    if 'CONTENT_LENGTH' in environ:
        headers['content-length'] = environ['CONTENT_LENGTH']
    if 'CONTENT_TYPE' in environ:
        headers['content-type'] = environ['CONTENT_TYPE']

    fs = cgi.FieldStorage(fp=environ['wsgi.input'],
                          headers=headers,
                          environ={'REQUEST_METHOD':'POST'})

    # Add post data to the render vars
    renvars.update(dict([(x, [fs[x].value]) for x in fs.keys()]))

    # Dict of current possible paths
    pages = { '/' : 'index.html', \
              '/content' : 'content.html', \
              '/image' : 'image.html', \
              '/file' : 'file.html', \
              '/form' : 'form.html', \
              '/submit' : 'submit.html' }

    # Load up the templates
    loader = jinja2.FileSystemLoader('./templates')
    env = jinja2.Environment(loader=loader)
    # Set the status and headers for start_response
    status = '200 OK'
    headers = [('Content-type', 'text/html')]
    
    # Templates for post
    if environ['REQUEST_METHOD'] == 'POST':
        template = env.get_template('submit.html')
    
    # Deny access to methods other than post and get
    elif environ['REQUEST_METHOD'] != 'GET':
        template = env.get_template('404.html')
        status = '404 Not Found'
        
    # Check if the path exists    
    elif environ['PATH_INFO'] in pages:
        template = env.get_template(pages[environ['PATH_INFO']])

    # If the path doesn't exist
    else:
        template = env.get_template('404.html')
        status = '404 Not Found'
    
    start_response(status, headers)
    return  [template.render(renvars).encode('utf-8')]

def make_app():
    return simple_app
