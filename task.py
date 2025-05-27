from datetime import datetime
import database

class Task:
    def __init__(self, title, description, due_date, taskid=None, completed=False):
        self.taskid = taskid
        self.__completed = completed
        self.title = title
        self.description = description
        if (type(due_date) == type(datetime.now())):
            self.due_date = due_date
        elif (type(due_date) == type(int(1))):
            self.due_date = datetime.fromtimestamp(due_date/100)
        elif (type(due_date) == type(float(1))):
            self.due_date = datetime.fromtimestamp(int(due_date)/100)
        elif (type(due_date) == type(str(1))):
            self.due_date = datetime.fromtimestamp(float(due_date)/100)
        else:
            print(type(due_date))
            raise TypeError("Input must be int, string or datetime")
        

    def complete(self):
        self.__completed = True  # Fixed logic to mark as completed

    def databaseTuple(self):
        return (self.title, self.description, self.due_date.timestamp(), int(self.__completed))

