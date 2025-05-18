# This is where the Flask front end will go
import task
from flask import *
# Temp before set up in task
import database

app = Flask(__name__)

@app.route("/")
def mainPage():
    return render_template("home.html")

@app.route("/tasks", methods=["GET", "POST", "PUT"])
def tasks():
    if request.method == "POST":
        ID = request.form.get("userId")
        taskList = task.TaskList(ID)
        context = {'tasks':taskList.getTasks(), 'userid':ID}
        return render_template("userTask.html", **context)
    if request.method == "PUT":
        # try:
            data = request.get_json()
            if data is None:
                return jsonify({'message': 'Invalid request body'}), 400

            title = data.get('title')
            description = data.get('description')
            due_date = data.get('dueDate')
            userid = data.get('id')

            putTask = task.Task(title, description, due_date)
            server = database.database()
            taskid = server.addTask(putTask, userid)
            # Make sure taskid is not None
            if not taskid:
                return jsonify({'message': 'Failed to create task', 'taskid': None}), 500

            # Prepare task dict for frontend
            from datetime import datetime
            due_date_str = datetime.fromtimestamp(int(due_date)/1000).strftime('%Y-%m-%d')
            task_dict = {
                'taskid': taskid,
                'title': title,
                'description': description,
                'due_date': due_date_str,
                '__completed': False
            }

            return jsonify({'message': 'Task created successfully', 'taskid': taskid}), 201
        # except Exception as e:
        #     print(e)
        #     return jsonify({'message': 'An error occurred'}), 500

    return redirect(url_for('mainPage'))

if __name__ == '__main__':
    app.run(debug=True)

# while True:
#     print("Press 1 to create a task.")
#     print("Press 2 to delete a task.")
#     print("Press 3 to list tasks.")
#     print("Press 4 to exit.")

#     try:
#         choice = int(input("Choose an option: "))
#     except:
#         print("Invalid input!")


#     t = task.TaskList()

#     if (choice == 1):
#         task_title = input("Task Title: ")
#         task_desc = input("Task Description: ")
#         task_date = input("Task due date (DD/MM/YYYY): ").split("/")
#         t.add_task(task.Task(task_title, task_desc, task_date))
#     elif (choice == 2):
#         n = input("Enter task name to delete: ")
#         t.delete_task(n)
#     elif (choice == 3):
#         t.print_list()
#     elif (choice == 4):
#         exit()

#     print()
