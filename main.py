# This is where the Flask front end will go
import task

print("Welcome to the Task Management Tool.\n")
print("Press 1 to create a task.")
print("Press 2 to delete a task.")

try:
    choice = int(input("Choose an option: "))
except:
    print("Invalid input!")

t = task.TaskList()
if (choice == 1):
    n = input("Enter task name to add: ")
    t.add_task(n)
elif (choice == 2):
    n = input("Enter task name to delete: ")
    t.delete_task(n)

task.placeholder()