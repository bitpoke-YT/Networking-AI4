import sqlite3
import os 
import task
import datetime

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
            UserID INTEGER PRIMARY KEY,
            TaskID INTEGER
        )''')



        self.__server.commit()

    def __init__(self):
        path = os.path.expanduser('~/Documents/Task_Management')
        if not os.path.exists(path):
            os.makedirs(path)
        try:
            self.__server = sqlite3.connect(f"{path}/Task.db")
            self.__setupTable()
        except Exception as e:
            print(f"Could Not Connect to server This is the Issue {e}")


    def addTasks(self, tasks, userID):
        cursor = self.__server.cursor()
        for task in tasks:
            params = task.databaseTuple()
            cursor.execute(f"INSERT INTO Tasks VALUES (NULL, ?, ?, ?, ?)", params)
            ID = cursor.lastrowid
            cursor.execute(f"INSERT INTO TaskUser (TaskID, UserID) VALUES ({ID}, {userID})")
        
        self.__server.commit()


    # Get Tasks

    # Completed is a Int
    def getTask(self, taskID, completed):
        tasksDB = self.__server.execute(f"SELECT * FROM Tasks WHERE TaskID ='{taskID}' Compleated = '{completed}'")
        taskClass = None
        for taskDB in tasksDB:
            taskClass = task.Task(taskDB[1], taskDB[2], datetime.datetime.fromtimestamp(taskDB[3]), (taskDB[4] <= 1))
        return taskClass

    def getCompleatedTasks(self, userID):
        TaskDB = self.__server.execute(f"SELECT TaskID FROM TaskUser WHERE UserID ='{userID}'")
        tasks = []
        for taskID in TaskDB:
            tasks.append(self.getTask(taskID[0], 1))
        return tasks
    
    def getCurrentTasks(self, userID):
        TaskDB = self.__server.execute(f"SELECT TaskID FROM TaskUser WHERE UserID ='{userID}'")
        tasks = []
        for taskID in TaskDB:
            # Getting Non compleated 
            tasks.append(self.getTask(taskID[0], 0))
        return tasks

    def getAllTasks(self, userID):
        TaskDB = self.__server.execute(f"SELECT TaskID FROM TaskUser WHERE UserID ='{userID}'")
        tasks = []
        for taskID in TaskDB:
            tasks.append(self.getTask(taskID[0], 1))
            tasks.append(self.getTask(taskID[0], 0))
        return tasks