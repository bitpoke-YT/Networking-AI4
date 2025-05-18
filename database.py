import sqlite3
import os 
import task
import datetime

class database():
    __server = None
    _instance = None

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
            UserID INTEGER,
            TaskID INTEGER
        )''')



        self.__server.commit()

    def __new__(cls):
        if cls._instance is not None:
            return cls._instance
        cls._instance = super(database, cls).__new__(cls)
        path = os.path.expanduser('~/Documents/Task_Management')
        if not os.path.exists(path):
            os.makedirs(path)
        try:
            cls.__server = sqlite3.connect(f"{path}/Task.db", check_same_thread=False)
            cls.__setupTable()
        except Exception as e:
            print(f"Could Not Connect to server This is the Issue {e}")
            return cls._instance


    def addTasks(self, tasks, userID):
        cursor = self.__server.cursor()
        for task in tasks:
            params = task.databaseTuple()
            cursor.execute(f"INSERT INTO Tasks VALUES (NULL, ?, ?, ?, ?)", params)
            ID = cursor.lastrowid
            cursor.execute(f"INSERT INTO TaskUser (TaskID, UserID) VALUES ({ID}, {userID})")
        
        self.__server.commit()

    def addTask(self, task, userID):
        cursor = self.__server.cursor()
        params = task.databaseTuple()
        cursor.execute(f"INSERT INTO Tasks VALUES (NULL, ?, ?, ?, ?)", params)
        ID = cursor.lastrowid
        cursor.execute(f"INSERT INTO TaskUser (TaskID, UserID) VALUES ({ID}, {userID})")
        print("Add DB")
        self.__server.commit()

        return ID
    


    # Get Tasks

    # Completed is a Int
    def getTask(self, taskID, completed):
        tasksDB = self.__server.execute(f"SELECT * FROM Tasks WHERE TaskID ='{taskID}' AND Compleated ={int(completed)}")
        taskClass = None
        for taskDB in tasksDB:
            taskClass = task.Task(taskDB[1], taskDB[2], datetime.datetime.fromtimestamp(taskDB[3]), taskID,(taskDB[4] >= 1))
        return taskClass

    def getCompleatedTasks(self, userID):
        TaskDB = self.__server.execute(f"SELECT TaskID FROM TaskUser WHERE UserID ='{userID}'")
        tasks = []
        for taskID in TaskDB:
            # Getting Non compleated 
            task = self.getTask(taskID[0], True)
            if task != None:
                tasks.append(task)
        return tasks
    
    def getCurrentTasks(self, userID):
        TaskDB = self.__server.execute(f"SELECT TaskID FROM TaskUser WHERE UserID ='{userID}'")
        tasks = []
        for taskID in TaskDB:
            # Getting Non compleated 
            task = self.getTask(taskID[0], False)
            if task != None:
                tasks.append(task)
        return tasks

    def getAllTasks(self, userID):
        TaskDB = self.__server.execute(f"SELECT TaskID FROM TaskUser WHERE UserID ='{userID}'")
        tasks = []
        for taskID in TaskDB:
            # Getting Non compleated 
            task = self.getTask(taskID[0], False)
            if task != None:
                tasks.append(task)
        for taskID in TaskDB:
            # Getting Non compleated 
            task = self.getTask(taskID[0], True)
            if task != None:
                tasks.append(task)
        return tasks

    def completeTask(self, taskID):
        cursor = self.__server.cursor()
        cursor.execute("UPDATE Tasks SET Compleated = 1 WHERE TaskID = ?", (taskID,))
        self.__server.commit()

    def deleteTask(self, taskID):
        cursor = self.__server.cursor()
        cursor.execute("DELETE FROM Tasks WHERE TaskID = ?", (taskID,))
        cursor.execute("DELETE FROM TaskUser WHERE TaskID = ?", (taskID,))
        self.__server.commit()