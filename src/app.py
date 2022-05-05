from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow

# Database
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root@localhost/flask_mysql'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Init db
db = SQLAlchemy(app)
# Init ma
ma = Marshmallow(app)

# Task Class/Model
class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(70), unique=True)
    description = db.Column(db.String(100))

    def __init__(self, title, description):
        self.title = title
        self.description = description

# Create tables
db.create_all()

# TaskSchema Class/Schema
class TaskSchema(ma.Schema):
    class Meta:
        fields = ('id', 'title', 'description')

# Init schema
task_schema = TaskSchema()
tasks_schema = TaskSchema(many=True)

# Index page
@app.route('/')
def index():
    return jsonify({"message": "Welcome to the API"})

# Creat a task
@app.route('/tasks', methods=['POST'])
def createTask():
    title = request.json['title']
    description = request.json['description']
    new_task = Task(title, description)
    #Save data in the db
    db.session.add(new_task)
    #end the operation
    db.session.commit()
    return task_schema.jsonify(new_task)

# Show tasks
@app.route('/tasks', methods=['GET'])
def getTasks():
    all_tasks = Task.query.all()
    result = tasks_schema.dump(all_tasks)
    return jsonify(result)

# Show task
@app.route('/tasks/<id>')
def getTask(id):
    task = Task.query.get(id)
    return task_schema.jsonify(task)

# Update task
@app.route('/tasks/<id>', methods=['PUT'])
def updateTask(id):
    task = Task.query.get(id)
    title = request.json['title']
    description = request.json['description']
    task.title = title
    task.description = description
    db.session.commit()
    return task_schema.jsonify(task)

# Delete task
@app.route('/tasks/<id>', methods=['DELETE'])
def deleteTask(id):
    task = Task.query.get(id)
    db.session.delete(task)
    db.session.commit()
    return task_schema.jsonify(task)

# Run Server
if __name__ == "__main__":
    app.run(debug=True)
