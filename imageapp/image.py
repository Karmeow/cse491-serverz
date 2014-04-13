# image handling API
import sqlite3

images_size = 0

def add_image(data, title, description):
    db = sqlite3.connect('images.sqlite')
    db.text_factory = bytes
    db.execute('INSERT INTO image_store (image, title, description) \
                VALUES (?, ?, ?)' ,(data, title, description))
    db.commit()
    return 1

def get_image(num):
    db = sqlite3.connect('images.sqlite')
    db.text_factory = bytes
    
    c = db.cursor()
    c.execute('SELECT i,image FROM image_store WHERE i=?', (num,))
    i, image = c.fetchone()
    return image

def get_latest_image():
    db = sqlite3.connect('images.sqlite')
    db.text_factory = bytes

    c = db.cursor()
    c.execute('SELECT i,image FROM image_store ORDER BY i DESC LIMIT 1')
    #image_num = max(images.keys())
    #return images[image_num]
    i, image =  c.fetchone()
    return image

def get_image_list():
    db = sqlite3.connect('images.sqlite')
    db.text_factory = bytes
    c = db.cursor()
    c.execute('SELECT i,image FROM image_store ORDER BY i DESC LIMIT 1')
    i, image =  c.fetchone()
    print i
    count = 1
    img_list = []
    while (count < i+1):
        img_list.append(count)
        count += 1

    return img_list

def image_traverse(terms):
    db = sqlite3.connect('images.sqlite')
    db.text_factory = bytes
    c = db.cursor()
    c.execute('SELECT title, description FROM image_store')
    image_list = c.fetchall()

    found_image_list = []
    count = 1


    # Iterate through title elements
    for x in image_list:
        title_list = x[0].split(' ')
        title_list = [z.lower() for z in title_list]
        for y in terms:
            if (y.lower() in title_list) and (count not in found_image_list):
                found_image_list.append(count)
                break
        count += 1
    
    count = 1
    # Iterate through description elements
    for x in image_list:
        desc_list = x[1].split(' ')
        desc_list = [z.lower() for z in desc_list]
        for y in terms:
            if (y in desc_list) and (count not in found_image_list):
                found_image_list.append(count)
                break
        count += 1

    print found_image_list
    return found_image_list


