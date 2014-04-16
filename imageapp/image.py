# image handling API
import sqlite3
import os
import comment
IMAGE_DB_FILE = 'images.sqlite'

images = {}

def initialize():
    load()

def load():
    global images
    if (not os.path.isfile(IMAGE_DB_FILE)):
        db = sqlite3.connect(IMAGE_DB_FILE)
        db.execute('CREATE TABLE image_store (i INTEGER PRIMARY KEY, \
                                              image BLOB,            \
                                              title TEXT,            \
                                              description TEXT       \
                                              )')    
        db.commit()
        db.text_factory = bytes
        some_data = open('imageapp/dice.png', 'rb').read()
        add_image(some_data, 'Dice', 'Four six sided dice')
        db.commit()
        db.close()
        comment.reset()

    db = sqlite3.connect(IMAGE_DB_FILE)
    db.text_factory = bytes
    c = db.cursor()

    c.execute('SELECT i, image, title, description FROM image_store')
    for i,image,title,description in c.fetchall():
        images[i] = (image, title,description)


def add_image(data, title, description):
    if images:
        image_num = max(images.keys()) + 1
    else:
        image_num = 0

    db = sqlite3.connect(IMAGE_DB_FILE)
    db.text_factory = bytes
    db.execute('INSERT INTO image_store (image, title, description) \
                VALUES (?, ?, ?)' ,(data, title, description))
    db.commit()
    
    images[image_num] = data, title, description
    return image_num

def get_image(num):
    return images[num][0]

def get_latest_image():
    image_num = max(images.keys())
    return images[image_num][0]

def get_image_list():
    count = 1
    img_list = []
    while (count < max(images.keys())+1):
        img_list.append(count)
        count += 1

    return img_list

def image_traverse(terms):
    #db = sqlite3.connect('IMAGE_DB_FILE')
    #db.text_factory = bytes
    #c = db.cursor()
    #c.execute('SELECT title, description FROM image_store')
    #image_list = c.fetchall()
    #print
    #print image_list
    #print
    global images

    found_image_list = []
    count = 1

    # Iterate through title elements
    for x in images.values():
        title_list = x[1].split(' ')
        title_list = [z.lower() for z in title_list]
        for y in terms:
            if (y.lower() in title_list) and (count not in found_image_list):
                found_image_list.append(count)
                break
        count += 1
    
    count = 1
    # Iterate through description elements
    for x in images.values():
        desc_list = x[2].split(' ')
        desc_list = [z.lower() for z in desc_list]
        for y in terms:
            if (y in desc_list) and (count not in found_image_list):
                found_image_list.append(count)
                break
        count += 1

    print found_image_list
    return found_image_list


