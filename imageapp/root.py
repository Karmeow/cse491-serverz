import quixote
import cgi
import StringIO
from quixote.directory import Directory, export, subdir
from . import html, image, comment
from PIL import Image
import sqlite3

class RootDirectory(Directory):
    _q_exports = []

    @export(name='')                    # this makes it public.
    def index(self):
        request = quixote.get_request()
        if len(request.form.keys()):
            name = request.form['name']
            com = request.form['comment']
            x = comment.Comment(name,com)

        return html.render('index.html', values = {"com":comment.comments})

    @export(name='upload')
    def upload(self):
        return html.render('upload.html')

    @export(name='upload_receive')
    def upload_receive(self):
        request = quixote.get_request()
        print request.form.keys()

        the_file = request.form['file']
        title = request.form['title']
        description = request.form['description']
        print dir(the_file)
        print 'received file with name:', the_file.base_filename
        data = the_file.read(int(1e9))

        image.add_image(data, title, description)
        comment.comments = []
        return
        #return quixote.redirect('./')

    @export(name='image')
    def image(self):
        return html.render('image.html')

    @export(name='image_raw')
    def image_raw(self):
        request = quixote.get_request()
        response = quixote.get_response()
        response.set_content_type('image/png')
        query = request.get_query()
        query_value = query[query.find('=')+1:]
        
        if (query_value == 'latest'):
            img = image.get_latest_image()
        else:
            img = image.get_image(query_value)
            buff = StringIO.StringIO()
            buff.write(img)
            buff.seek(0)
            img = Image.open(buff)
            basewidth = 75
            wpercent = (basewidth/float(img.size[0]))
            hsize = int((float(img.size[1])*float(wpercent)))
            img = img.resize((basewidth, hsize), Image.ANTIALIAS)
            output = StringIO.StringIO()
            img.save(output, format="png")
            img = output.getvalue()

        return img

    @export(name='image_list')
    def image_list(self):
        #response = quixote.get_response()
        #response.set_content_type('image/png')
        img_list = image.get_image_list()
        return html.render('image_list.html', values={"images":img_list})

    @export(name='image_search')
    def image_search(self):
        return html.render('image_search.html')

    @export(name='search')
    def search(self):
        request = quixote.get_request()
        term_str = request.form['terms']
        terms = term_str.split(' ')
        img_list = image.image_traverse(terms)
        print img_list
        return html.render('search_results.html', values={"images":img_list})
