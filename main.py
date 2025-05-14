# This is where the Flask front end will go
import task
from flask import *

# print("Welcome to the Task Management Tool.\n")
# print("Press 1 to create a task.")
# print("Press 2 to delete a task.")

# try:
#     choice = int(input("Choose an option: "))
# except:
#     print("Invalid input!")

# t = task.TaskList()
# if (choice == 1):
#     n = input("Enter task name to add: ")
#     t.add_task(n)
# elif (choice == 2):
#     n = input("Enter task name to delete: ")
#     t.delete_task(n)

# task.placeholder()


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