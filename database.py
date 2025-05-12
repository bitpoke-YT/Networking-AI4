import sqlite3
import os 

class database():
    
    def __setupTable(self):
        if self.server == None:
            raise "Server Not Setup Yet"
        cursor = self.server.cursor()

        cursor.execute('''
        CREATE TABLE IF NOT EXISTS Tasks (
            TaskID INTEGER PRIMARY KEY,
            Title TEXT,
            Description TEXT,
            DueDate INTEGER
        )''')

        self.server.commit()

    def __init__(self):
        path = os.path.expanduser('-/Documents/Task_Management')
        if not os.path.exists(path):
            os.makedirs(path)
        try:
            self.server = sqlite3.connect(f"{path}/Task.db")
            self.__setupTable()
        except Exception as e:
            print(f"Could Not Connect to server This is the Issue {e}")
