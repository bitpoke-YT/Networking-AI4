import sqlite3
import os 
from task import Task 

class database():
    __server = None

    def __setupTable(self):
        if self.__server == None:
            raise "Server Not Setup Yet"
        cursor = self.__server.cursor()

        cursor.execute('''
        CREATE TABLE IF NOT EXISTS Tasks (
            TaskID INTEGER PRIMARY KEY,
            Title TEXT,
            Description TEXT,
            DueDate INTEGER,
            Compleated INTEGER
        )''')

        cursor.execute('''
        CREATE TABLE IF NOT EXISTS User (
            UserID INTEGER PRIMARY KEY,
            UserName TEXT
        )''')

        cursor.execute('''
        CREATE TABLE IF NOT EXISTS TaskUser (
            TaskID INTEGER PRIMARY KEY,
            UserID INTEGER PRIMARY KEY,
        )''')



        self.__server.commit()

    def __init__(self):
        path = os.path.expanduser('-/Documents/Task_Management')
        if not os.path.exists(path):
            os.makedirs(path)
        try:
            self.__server = sqlite3.connect(f"{path}/Task.db")
            self.__setupTable()
        except Exception as e:
            print(f"Could Not Connect to server This is the Issue {e}")

    def getTask(self, taskID):
        tasksDB = self.__server.execute(f"SELECT * FROM Tasks WHERE TaskID ='{taskID}'")
        taskClass = None
        for taskDB in tasksDB:
            taskClass = Task(taskDB[1], taskDB[2], taskDB[3], (taskDB[4] <= 1))
        return taskClass

    def getTasks(self, userID):
        TaskDB = self.__server.execute(f"SELECT TaskID FROM TaskUser WHERE UserID ='{userID}'")
        tasks = []
        for taskID in TaskDB:
            tasks.append(self.getTask(taskID[0]))
        return tasks
    
    def AddTasks(self, tasks, userID):
        cursor = self.__server.cursor()
        # for task in tasks:
        #     cursor.execute(f"INSERT INTO Tasks")


