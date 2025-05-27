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
    db = database.database()

    if request.method == "GET":
        completed = request.args.get("completed")
        if completed is not None:
            completed = completed.lower() == "true"
            tasks_data = db.getCompleatedTasks(userid) if completed else db.getCurrentTasks(userid)
            tasks_json = [
                {
                    'taskid': t.taskid,
                    'title': t.title,
                    'description': t.description,
                    'due_date': t.due_date.strftime('%Y-%m-%d'),
                    '__completed': t._Task__completed
                }
                for t in tasks_data
            ]
            return jsonify({'tasks': tasks_json})

        # Render page with tasks
        tasks_data = db.getCurrentTasks(userid)
        context = {'tasks': tasks_data, 'userid': userid}
        return render_template("userTask.html", **context)

    if request.method == "PUT":
        data = request.get_json()
        if data is None:
            return jsonify({'message': 'Invalid request body'}), 400
        title = data.get('title')
        description = data.get('description')
        due_date = data.get('dueDate')
        putTask = task.Task(title, description, due_date)
        try:
            taskid = db.addTask(putTask, userid)
        except:
            raise exception(f"Failed to add task to the database {userid}")
        if not taskid:
            return jsonify({'message': 'Failed to create task', 'taskid': None}), 500
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
        db = database.database()
        db.completeTask(taskid)
        return jsonify({'message': 'Task completed successfully'}), 200
    return redirect(url_for('mainPage'))

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
