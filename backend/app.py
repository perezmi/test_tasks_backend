from flask import Flask, request, jsonify
from datetime import datetime
from uuid import uuid4
from config import Config
from models import db, Task, TaskStatus
from sqlalchemy.exc import IntegrityError

app = Flask(__name__)
app.config.from_object(Config)
db.init_app(app)

with app.app_context():
    db.create_all()

def error_response(message: str, status_code: int):
    return jsonify({"error": message}), status_code

@app.route('/tasks', methods=['POST'])
def create_task():
    #Создание задачи
    data = request.get_json()
    if not data:
        return error_response("JSON data required", 400)
    now = datetime.now()
    task = Task(
        id=str(uuid4()),
        title=data['title'].strip(),
        description=data.get('description'),
        status=TaskStatus(data.get('status', 'todo')),
        created_at=now,
        updated_at=now,
    )
    if data.get('due_date'):
        task.due_date = datetime.fromisoformat(data['due_date'].replace('Z', '+00:00'))
    db.session.add(task)
    db.session.commit()
    return jsonify(task.to_dict()), 201


@app.route('/tasks', methods=['GET'])
def get_tasks():
    #Список тасков
    status = request.args.get('status')
    due_before = request.args.get('due_before')
    query = Task.query
    if status:
        query = query.filter(Task.status == TaskStatus(status))
    if due_before:
        try:
            due_date = datetime.fromisoformat(due_before.replace('Z', '+00:00'))
            query = query.filter(Task.due_date <= due_date)
        except ValueError:
            return error_response("due_before must be in ISO 8601", 400)
    tasks = query.all()
    return jsonify([task.to_dict() for task in tasks]),200


@app.route('/tasks/<string:task_id>', methods=['GET'])
def get_task(task_id):
    #Таск по ID
    task = Task.query.get(task_id)
    if task is None:
        return error_response("Task not found", 404)

    return jsonify(task.to_dict()), 200


@app.route('/tasks/<string:task_id>', methods=['PATCH'])
def update_task(task_id):
    #Изменение таска
    task_to_patch = Task.query.get(task_id)
    if task_to_patch is None:
        return error_response("Task not found", 404)
    else:
        data = request.get_json()
        if data:
            task_to_patch.title = data['title'].strip()
            task_to_patch.description = data.get('description')
            task_to_patch.status = TaskStatus(data.get('status', 'todo'))
            task_to_patch.updated_at = datetime.now()
            db.session.commit()
            return '', 200
        else:
            return error_response("JSON data required", 400)

@app.route('/tasks/<string:task_id>', methods=['DELETE'])
def delete_task(task_id):
    #Удаление таска по ID
    task_to_delete = Task.query.get(task_id)
    if task_to_delete is None:
        return error_response("Task not found", 404)
    else:
        db.session.delete(task_to_delete)
        db.session.commit()
        return '', 204


if __name__ == '__main__':
    app.run(debug=True,port=Config.port)