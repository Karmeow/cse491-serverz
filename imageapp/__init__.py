# __init__.py is the top level file in a Python package.

from quixote.publish import Publisher

# this imports the class RootDirectory from the file 'root.py'
from .root import RootDirectory
from . import html, image
import sqlite3
import os.path
import image

def create_publisher():
     p = Publisher(RootDirectory(), display_exceptions='plain')
     p.is_thread_safe = True
     return p

def setup():                            # stuff that should be run once.
    html.init_templates()

    if (not os.path.isfile('images.sqlite')):
        db = sqlite3.connect('images.sqlite')
        db.execute('CREATE TABLE image_store (i INTEGER PRIMARY KEY, image BLOB)')
        db.commit()

        db.text_factory = bytes
        some_data = open('imageapp/dice.png', 'rb').read()
        image.add_image(some_data)
        
        # insert first image with num starting at 0
        #db.execute('INSERT INTO image_store (image) VALUES (?)',
        #          (some_data,))
        db.commit()
        db.close()
        #image.add_image(some_data)


def teardown():                         # stuff that should be run once.
    pass
