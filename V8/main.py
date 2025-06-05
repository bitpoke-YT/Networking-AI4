import task
from flask import *
import database
from werkzeug.security import generate_password_hash, check_password_hash
from dotenv import load_dotenv
import os
import secrets

app = Flask(__name__)

app.secret_key = "UnlimitedPower"

@app.route("/")
def mainPage():
    if 'userid' in session:
        return redirect(url_for('tasks'))
    return render_template("home.html")

@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")
        if not username or not password:
            return render_template("register.html", error="Please fill in all fields.")
        db = database.database()
        # Check if user exists
        user = db.getUserByUsername(username)
        if user:
            db.close()
            return render_template("register.html", error="Username already exists.")
        # Register user
        hashed_pw = generate_password_hash(password)
        userid = db.createUser(username, hashed_pw)
        db.close()
        session['userid'] = userid
        session['logged'] = True
        return redirect(url_for('tasks'))
    return render_template("register.html")

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")
        db = database.database()
        user = db.getUserByUsername(username)
        if user and check_password_hash(user['password'], password):
            db.close()
            session['userid'] = user['userid']
            session['username'] = user['username']
            return redirect(url_for('tasks'))
        db.close()
        return make_response(render_template("login.html", error="Invalid credentials."), 401)
    else:
        return render_template("login.html")

@app.route("/logout")
def logout():
    session.pop('userid', None)
    return redirect(url_for('mainPage'))

@app.route("/tasks", methods=["GET", "POST", "PUT"])
def tasks():
    if 'userid' not in session:
        print(session)
        return redirect(url_for('login'))
    userid = session['userid']
    db = database.database()
    if request.method == "GET":
        completed = request.args.get("completed")
        if completed is not None:
            completed = completed.lower() == "true"
            tasks_data = db.getCompleatedTasks(userid) if completed else db.getCurrentTasks(userid)
            db.close()
            tasks_json = [
                {
                    'taskid': t.taskid,
                    'title': t.title,
                    'description': t.description,
                    'due_date': t.due_date.strftime('%Y-%m-%d'),
                    '__completed': t.completed
                }
                for t in tasks_data
            ]
            return jsonify({'tasks': tasks_json})

        tasks_data = db.getCurrentTasks(userid)
        db.close()
        context = {'tasks': tasks_data, 'userid': userid}
        return render_template("userTask.html", **context)

    if request.method == "PUT":
        data = request.get_json()
        if data is None:
            db.close()
            return jsonify({'message': 'Invalid request body'}), 400
        title = data.get('title')
        description = data.get('description')
        due_date = data.get('dueDate')
        putTask = task.Task(title, description, due_date)
        try:
            taskid = db.addTask(putTask, userid)
        except:
            db.close()
            raise Exception(f"Failed to add task to the database {putTask.databaseTuple()} {userid}")
        db.close()
        if not taskid:
            return jsonify({'message': 'Failed to create task', 'taskid': None}), 500
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


    return redirect(url_for('mainPage'))

@app.route("/task", methods=["POST"])
def taskComplete():
    if 'userid' not in session:
        return redirect(url_for('login'))
    if request.method == "POST":
        data = request.get_json()
        if data is None:
            return jsonify({'message': 'Invalid request body'}), 400
        taskid = data.get('taskid')
        db = database.database()
        db.completeTask(taskid)
        db.close()
        return jsonify({'message': 'Task completed successfully'}), 200
    return redirect(url_for('mainPage'))

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
