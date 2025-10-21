# Тестовое задание
Тестовое задание ПМИ. 

## Установка и запуск

Клонируем репозиторий:

```bash
git clone https://github.com/perezmi/test_tasks_backend.git
```

Установка зависимостей:

```bash
cd test_tasks_backend
python -m venv .venv
pip install -r requirements.txt
```

Запуск приложения:

```bash
python app.py
```

## Использование:

Добавление записи:

```bash
curl -X POST http://localhost:8000/tasks \
-H "Content-Type: application/json" \
-d '{
  "title": "Купить продукты",
  "description": "Болты, Гайки, Ведра",
  "status": "todo",
  "due_date": "2025-10-31T10:00:00Z"
}'
```
Получение всех записей:

```bash
curl -X GET "http://localhost:5000/tasks?status=todo&due_before=2025-10-30T00:00:00Z"
```

Обновление записи:
```bash
curl -X PATCH http://localhost:5000/tasks/some-unique-task-id \
-H "Content-Type: application/json" \
-d '{
  "title": "Купить продукты",
  "description": "Болты, Гайки, Ведра, Гвозди",
  "status": "in-progress"
}'
```

Удаление записи:
```bash
curl -X DELETE http://localhost:5000/tasks/<ID таска>
```
