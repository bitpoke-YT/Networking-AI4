class Task:
    compleated = False
    def __init__(self, title, description, due_date):
        self.title = title
        self.description = description
        self.due_date = due_date

class TaskList:
    _instance = None
    __tasks = []

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(TaskList, cls).__new__(cls)
        else:
            return cls._instance
    
    def deleteTask(self, task):
        try:
            self.__tasks.remove(task)
            return True
        except:
            return False