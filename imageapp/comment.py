import os
import sqlite3

comments = []
COMMENTS_DB_FILE = 'comments.sqlite'

class Comment(object):
    def __init__(self, name, com, flag):
        self.name = name
        self.com = com
        # Don't reinsert items in database, really bad way to handle it
        if (flag != 1):
            insert(self)
        comments.append(self)

def insert(comment):
    db = sqlite3.connect(COMMENTS_DB_FILE)
    print comment.name
    print comment.com
    db.execute("INSERT INTO comment_store (user, comment) VALUES (?, ?)",
                                            (comment.name, comment.com))
    db.commit()
    db.close()

def reset():
    global comments
    comments = []
    db = sqlite3.connect(COMMENTS_DB_FILE)
    db.execute("DELETE FROM comment_store")
    db.commit()
    db.close()

def initialize():
    if (not os.path.isfile(COMMENTS_DB_FILE)):
        db = sqlite3.connect(COMMENTS_DB_FILE)
        db.execute('CREATE TABLE comment_store (user TEXT, comment TEXT)')  
        db.commit()
        db.close()
    load()

def load():
    global comments
    db = sqlite3.connect(COMMENTS_DB_FILE)
    db.text_factory = str
    c = db.cursor()

    c.execute('SELECT user, comment FROM comment_store')
    for user, comment in c.fetchall():
        Comment(user, comment, 1)
