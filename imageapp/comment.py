comments = []

class Comment(object):
    def __init__(self, name, com):
        self.name = name
        self.com = com
        comments.append(self)
