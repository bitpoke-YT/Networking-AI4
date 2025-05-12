class Task:
    def __init__(self, name, due_date):
        self.name = name
        self.due_date = due_date

class TaskList:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(TaskList, cls).__new__(cls)
        else:
            return cls._instance