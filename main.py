import task
from flask import *
import database
from werkzeug.security import generate_password_hash, check_password_hash
import os

app = Flask(__name__)

# Read secret key from .env file
env_path = os.path.join(os.path.dirname(__file__), '.env')
secret_key = None
if os.path.exists(env_path):
    with open(env_path, 'r') as f:
        for line in f:
            if line.startswith('FLASK_SECRET_KEY='):
                secret_key = line.strip().split('=', 1)[1]
                break
if not secret_key:
    raise RuntimeError(".env file missing FLASK_SECRET_KEY or file not found")
app.secret_key = secret_key

@app.before_request
def before_request():
    database.database()

@app.route("/")
def mainPage():
    if 'userid' in session:
        return redirect(url_for('tasks'))
    elif request.cookies.get('sessionID', 0) == 0:
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
            return render_template("register.html", error="Username already exists.")
        # Register user
        hashed_pw = generate_password_hash(password)
        userid = db.createUser(username, hashed_pw)
        session['userid'] = userid
        session['username'] = username
        resp = make_response(redirect(url_for('tasks')))
        resp.set_cookie('sessionID', f"{userid}")
        return resp
    return render_template("register.html")

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")
        db = database.database()
        user = db.getUserByUsername(username)
        if user and check_password_hash(user['password'], password):
            session['userid'] = user['userid']
            session['username'] = username
            resp = make_response(redirect(url_for('tasks')))
            resp.set_cookie('sessionID', f"{user['userid']}")
            return resp
        return render_template("login.html", error="Invalid credentials.")
    return render_template("login.html")

@app.route("/logout")
def logout():
    session.clear()
    resp = make_response(redirect(url_for('mainPage')))
    resp.set_cookie('userid', '', expires=0)
    return resp

@app.route("/tasks", methods=["GET", "POST", "PUT"])
def tasks():
    if 'userid' not in session or request.cookies.get('sessionID', 0) == 0:
        return redirect(url_for('login'))
    userid = session['userid']
    userid = request.cookies.get('sessionID')
    print(f"The user id is {userid}")
    if request.method == "GET":
        completed = request.args.get("completed")
        # Use session userid if not provided
        if completed is not None:
            completed = completed.lower() == "true"
            taskList = task.TaskList(userid)
            if completed:
                tasks_data = taskList.getCompleatedTasks()
            else:
                tasks_data = taskList.getTasks()
            tasks_json = []
            for t in tasks_data:
                tasks_json.append({
                    'taskid': getattr(t, 'taskid', None),
                    'title': getattr(t, 'title', ''),
                    'description': getattr(t, 'description', ''),
                    'due_date': t.due_date.strftime('%Y-%m-%d') if hasattr(t, 'due_date') else '',
                    '__completed': getattr(t, '_Task__completed', False)
                })
            return jsonify({'tasks': tasks_json})

        # Render page with tasks
        taskList = task.TaskList(userid)
        context = {'tasks': taskList.getTasks(), 'userid': userid}
        return render_template("userTask.html", **context)

    if request.method == "PUT":
        data = request.get_json()
        if data is None:
            return jsonify({'message': 'Invalid request body'}), 400
        title = data.get('title')
        description = data.get('description')
        due_date = data.get('dueDate')
        # Always use session userid
        userid = session['userid']
        userid = request.cookies.get('sessionID')
        putTask = task.Task(title, description, due_date)
        taskList = task.TaskList(userid)
        taskid = taskList.add_task(putTask)
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
    elif request.cookies.get('sessionID', 0) == 0:
        return redirect(url_for('login'))
    if request.method == "POST":
        data = request.get_json()
        if data is None:
            return jsonify({'message': 'Invalid request body'}), 400
        taskid = data.get('taskid')
        server = database.database()
        server.completeTask(taskid) 
        return jsonify({'message': 'Task completed successfully'}), 200
    return redirect(url_for('mainPage'))

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
