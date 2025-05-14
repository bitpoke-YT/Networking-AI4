import datatime

class Task:
    __compleated = False
    def __init__(self, title, description, due_date, compleated):
        self.title = title
        self.description = description
        self.due_date = due_date
        self.__compleated = compleated

    def compleate(self):
        __compleated = False

    def databaseTuple(self):
        return (self.title, self.description, self.due_date)

class TaskList:
    _instance = None
    __tasks = []

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(TaskList, cls).__new__(cls)   
        return cls._instance
    
    def add_task(self, task):
        try:
            self.__tasks.append(task)
        except Exception as e:
            print(e)

    def delete_task(self, task):
        try:
            self.__tasks.remove(task)
            return True
        except:
            return False
    
    def print_list(self):
        print(self.__tasks)

def placeholder():
    # Create task list
    tasklist = TaskList()

    # Test Methods
    TaskList().print_list()
