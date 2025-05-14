# This is where the Flask front end will go
import task
from flask import Flask, render_template

print("Welcome to the Task Management Tool.\n")

while True:
    print("Press 1 to create a task.")
    print("Press 2 to delete a task.")
    print("Press 3 to list tasks.")
    print("Press 4 to exit.")

    try:
        choice = int(input("Choose an option: "))
    except:
        print("Invalid input!")


    t = task.TaskList()

    if (choice == 1):
        task_title = input("Task Title: ")
        task_desc = input("Task Description: ")
        task_date = input("Task due date (DD/MM/YYYY): ").split("/")
        t.add_task(task.Task(task_title, task_desc, task_date))
    elif (choice == 2):
        n = input("Enter task name to delete: ")
        t.delete_task(n)
    elif (choice == 3):
        t.print_list()
    elif (choice == 4):
        exit()

    print()

app = Flask(__name__)

@app.route("/")
def mainPage():
    return render_template("home.html")

@app.route("/tasks", methods=["GET", "POST"])
def tasks():
    if request.method == "POST":
        ID = request.form.get("userId")
        print(ID)
        # Auth = request.form.get("Auth")
    
    return redirect(url_for('mainPage'))

if __name__ == '__main__':
    app.run(debug=True)
