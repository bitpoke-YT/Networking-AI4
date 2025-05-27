import sqlite3
import os 
import task
import datetime

class database():
    def __init__(self):
        path = os.path.expanduser('~/Documents/Networking-AI4/V1')
        if not os.path.exists(path):
            os.makedirs(path)
        self.__server = sqlite3.connect(f"{path}/Task.db", check_same_thread=False)
        self.__server.execute('PRAGMA journal_mode=WAL;')  # Enable WAL mode
        self.__server.execute('PRAGMA busy_timeout=5000;') # Wait up to 5 seconds for locks
        self.__setupTable()

    def __setupTable(self):
        if self.__server is None:
            raise Exception("Server Not Setup Yet")
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
            UserName TEXT UNIQUE,
            Password TEXT
        )''')

        cursor.execute('''
        CREATE TABLE IF NOT EXISTS TaskUser (
            UserID INTEGER,
            TaskID INTEGER
        )''')

        self.__server.commit()

    def addTasks(self, tasks, userID):
        cursor = self.__server.cursor()
        for task in tasks:
            params = task.databaseTuple()
            cursor.execute(f"INSERT INTO Tasks VALUES (NULL, ?, ?, ?, ?)", params)
            ID = cursor.lastrowid
            # Ensure both userID and ID are integers
            try:
                userID_int = int(userID)
                ID_int = int(ID)
            except Exception as e:
                print(f"Type conversion error in addTasks: userID={userID}, ID={ID}, error={e}")
                raise
            cursor.execute("INSERT INTO TaskUser (UserID, TaskID) VALUES (?, ?)", (userID_int, ID_int))
        self.__server.commit()

    def addTask(self, task, userID):
        cursor = self.__server.cursor()
        params = task.databaseTuple()
        cursor.execute(f"INSERT INTO Tasks VALUES (NULL, ?, ?, ?, ?)", params)
        ID = cursor.lastrowid
        # Ensure both userID and ID are integers
        try:
            userID_int = int(userID)
            ID_int = int(ID)
        except Exception as e:
            print(f"Type conversion error in addTask: userID={userID}, ID={ID}, error={e}")
            raise
        cursor.execute("INSERT INTO TaskUser (UserID, TaskID) VALUES (?, ?)", (userID_int, ID_int))
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

    # --- User Authentication Methods ---
    def createUser(self, username, password_hash):
        cursor = self.__server.cursor()
        cursor.execute("INSERT INTO User (UserName, Password) VALUES (?, ?)", (username, password_hash))
        self.__server.commit()
        return cursor.lastrowid

    def getUserByUsername(self, username):
        cursor = self.__server.cursor()
        cursor.execute("SELECT UserID, UserName, Password FROM User WHERE UserName = ?", (username,))
        row = cursor.fetchone()
        if row:
            return {'userid': row[0], 'username': row[1], 'password': row[2]}
        return None

    def close(self):
        if self.__server:
            self.__server.close()
            self.__server = None