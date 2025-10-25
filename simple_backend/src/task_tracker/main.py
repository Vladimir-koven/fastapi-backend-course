from fastapi import FastAPI

app = FastAPI()
tasks = []
count_next_id = 1

@app.get("/tasks")
def get_tasks():
    return tasks

@app.post("/tasks")
def create_task(task):
    global count_next_id
    new_task = {
        'id': count_next_id,
        'title': task.get('title', ''),
        'description': task.get('description', ''),
        'status': task.get('status', False)
    }
    tasks.append(new_task)
    count_next_id += 1
    return new_task

@app.put("/tasks/{task_id}")
def update_task(task_id: int, task_update: dict):
    for task in tasks:
        if task['id'] == task_id:
            if task_update.get('title') is not None:
                task['title'] = task_update['title']
            if task_update.get('description') is not None:
                task['description'] = task_update['description']
            if task_update.get('status') is not None:
                task['status'] = task_update['status']
            return task
    return {'error': 'Task not found'}

@app.delete("/tasks/{task_id}")
def delete_task(task_id: int):
    global tasks
    for i, task in enumerate(tasks):
        if task['id'] == task_id:
            tasks.pop(i)
            return {'message': f'Task {task_id} deleted'}
    return {'error': 'Task not found'}