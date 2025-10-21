import pytest
from app import app, db


@pytest.fixture
def client():
    app.config['TESTING'] = True
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
    with app.app_context():
        db.create_all()
        yield app.test_client()
        db.session.remove()
        db.drop_all()


def test_create_task(client):
    response = client.post('/tasks', json={
        'title': 'Test Task',
        'description': 'This is a test task.',
        'status': 'todo',
        'due_date': '2023-10-01T12:00:00Z'
    })
    assert response.status_code == 201
    assert 'id' in response.json
    assert response.json['title'] == 'Test Task'

def test_get_tasks(client):
    client.post('/tasks', json={
        'title': 'Another Task',
        'description': 'This task should be retrievable.',
        'status': 'done'
    })
    response = client.get('/tasks')
    assert response.status_code == 200
    assert len(response.json) >= 1


def test_get_task(client):
    create_response = client.post('/tasks', json={
        'title': 'Task to Retrieve',
        'description': 'This task will be retrieved.',
        'status': 'todo'
    })
    task_id = create_response.json['id']

    response = client.get(f'/tasks/{task_id}')
    assert response.status_code == 200
    assert response.json['title'] == 'Task to Retrieve'


def test_get_task_not_found(client):
    response = client.get('/tasks/non_existent_id')
    assert response.status_code == 404
    assert response.json['error'] == 'Task not found'


def test_update_task(client):
    create_response = client.post('/tasks', json={
        'title': 'Task to Update',
        'description': 'This task will be updated.',
        'status': 'todo'
    })
    task_id = create_response.json['id']

    response = client.patch(f'/tasks/{task_id}', json={
        'title': 'Updated Task',
        'description': 'This task has been updated.',
        'status': 'done'
    })
    assert response.status_code == 200

    get_response = client.get(f'/tasks/{task_id}')
    assert get_response.json['title'] == 'Updated Task'
    assert get_response.json['status'] == 'done'


def test_delete_task(client):
    create_response = client.post('/tasks', json={
        'title': 'Task to Delete',
        'description': 'This task will be deleted.'
    })
    task_id = create_response.json['id']

    response = client.delete(f'/tasks/{task_id}')
    assert response.status_code == 204

    get_response = client.get(f'/tasks/{task_id}')
    assert get_response.status_code == 404
    assert get_response.json['error'] == 'Task not found'


def test_update_non_existent_task(client):
    response = client.patch('/tasks/non_existent_id', json={
        'title': 'Attempting to Update Non-Existent Task'
    })
    assert response.status_code == 404
    assert response.json['error'] == 'Task not found'
