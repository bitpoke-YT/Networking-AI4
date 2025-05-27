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
        self.__completed = False

    def databaseTuple(self):
        return (self.title, self.description, self.due_date.timestamp(), int(self.__completed))

class TaskList:
    _instances = {}
    __database = None

    def __new__(cls, userID):
        if userID not in cls._instances:
            print(f"Creating new TaskList for user {userID}.")
            cls.__userid = userID
            instance = super(TaskList, cls).__new__(cls)
            cls.__database = database.database()
            cls._instances[userID] = instance
        else:
            print(f"TaskList for user {userID} already exists, returning existing instance.")
        return cls._instances[userID]

    def add_task(self, task):
        try:
            server = database.database()
            taskid = server.addTask(task, self.__userid)
            return taskid
        except Exception as e:
            print(e)
            return None

    def deleteTask(self, task):
        try:
            self.__database.deleteTask(task.taskid)
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

    def compleateTask(self, task):
        try:
            task.__completed = True
        except Exception as e:
            print(e)

    def getTaskId(self, taskID):
        for task in self.__tasks:
            if task.taskid == taskID:
                return task
        return None

    def getTasks(self,):
        return self.__database.getCurrentTasks(self.__userid)
    
    def getCompleatedTasks(self):
        return self.__database.getCompleatedTasks(self.__userid)

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
    
    taskList = TaskList(userID)

    for task in tasks:
        taskList.add_task(task)

    return taskList

