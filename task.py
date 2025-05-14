class Task:
    completed = False
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
        return cls._instance

    def add_task(self, task):
        try:
            self.__tasks.append(task)
        except Exception as e:
            print(e)

    def deleteTask(self, task):
        try:
            self.__tasks.remove(task)
            return True
        except:
            return False
    
    def print_list(self):
        print(self.__tasks)
