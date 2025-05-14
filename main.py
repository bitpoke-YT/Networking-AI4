# This is where the Flask front end will go
import task

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
        n = input("Enter task name to add: ")
        t.add_task(n)
        t.add_task(task.Task(input("Task Title: "),
                             input("Task Description: "),
                             input("Task_due_date: ")))
    elif (choice == 2):
        n = input("Enter task name to delete: ")
        t.delete_task(n)
    elif (choice == 3):
        t.print_list()
    elif (choice == 4):
        exit()
