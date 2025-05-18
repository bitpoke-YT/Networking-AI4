from datetime import datetime
import database

class Task:
    def __init__(self, title, description, due_date, taskid=None, completed=False):
        self.taskid = taskid
        self.__completed = completed
        self.title = title
        self.description = description
        if (type(due_date) == type(datetime.now())):
            print("Good")
            self.due_date = due_date
        elif (type(due_date) == type(int(1))):
            self.due_date = datetime.fromtimestamp(due_date/100)
        elif (type(due_date) == type(float(1))):
            self.due_date = datetime.fromtimestamp(int(due_date)/100)
        elif (type(due_date) == type(str(1))):
            print(float(due_date))
            self.due_date = datetime.fromtimestamp(float(due_date)/100)
        else:
            print(type(due_date))
            raise TypeError("Input must be int, string or datetime")
        

    def complete(self):
        self.__completed = False

    def databaseTuple(self):
        return (self.title, self.description, self.due_date.timestamp(), int(self.__completed))

class TaskList:
    _instance = None
    __tasks = []

    def __new__(cls, userID):
        if cls._instance is None:
            cls._instance = super(TaskList, cls).__new__(cls)
        if cls.__tasks == []:
            cls.__tasks = database.database().getCurrentTasks(userID)
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
        
    def edit_task(self, task, newtask):
        try:
            self.__tasks[int(task)] = newtask
        except Exception as e:
            print(e)
    
    def print_list(self):
        print(self.__tasks)

    def getTasks(self):
        return self.__tasks

def placeholder():
    # Create task list
    tasklist = TaskList()

    # Test Methods
    print("Task List: ", end="")
    TaskList().print_list()

def createUsersList(userID, isCompleated):
    tasks = []
    server = database.database()
    if(isCompleated == True):
        tasks = server.getCompleatedTasks(userID)
    elif(isCompleated == False):
        tasks = server.getCurrentTasks(userID)
    else:
        tasks = server.getAllTasks(userID)
    
    taskList = TaskList()

    for task in tasks:
        taskList.add_task(task)

    return taskList

