class Kangaroo:
    def __init__(self):
        self.pouch_contents = []
    
    def put_in_pouch(self, string):
        if string not in self.pouch_contents:
            self.pouch_contents.append(string)
        else:
            print ('object already in pouch')
    
    def __str__(self):
        if len(self.pouch_contents) == 0:
            print ("The kangaroo's pouch is empty")
        else:
            print("the kangaroo's pouch contains: {0}".format(self.pouch_contents))