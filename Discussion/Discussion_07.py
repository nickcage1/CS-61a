####
##Q1
####

class Student:
    students = 0
    
    def __init__(self,name,staff):
        self.name = name
        self.understanding = 0
        Student.students += 1
        print ("There are now", Student.students, "students")
        staff.add_student(self)

    def visit_office_hours(self, staff):
        staff.assist(self)
        print ('Thanks, ' + staff.name)

class Professor:
    def __init__(self, name):
        self.name = name
        self.students = {}

    def add_student(self , student):
        self.students[student.name] = student

    def assist(self, student):
        student.understanding += 1

####
##Q2
####

class MinList:
    
    def __init__(self):
        self.items = []
        self.size = 0

    def append(self, item):
        self.items = self.items + [item]
        self.size += 1
    
    def pop(self):
        smallest = 100
        for item in self.items:
            if item < smallest:
                smallest = item
        new_list = []
        for item in self.items:
            if item != smallest:
                new_list = new_list + [item]
        self.items = new_list
        self.size -= 1
        return smallest

####
##Q3
####

class Email:

    def __init__(self, msg, sender_name, recipient_name):
        self.msg = msg
        self.sender_name = sender_name
        self.recipient_name = recipient_name
    
class Server:
    
    def __init__(self):
        self.clients = {}
    
    def send(self, email):