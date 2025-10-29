from fastapi import FastAPI, HTTPException
from task_manager import TaskManager

app = FastAPI()
task_manager = TaskManager()

@app.get('/tasks')
def get_tasks():
    return task_manager.get_all()

@app.post('/tasks')
def create_task(task: dict):
    if not isinstance(task, dict):
        raise HTTPException(status_code=400, detail='Invalid data format')
    try:
        return task_manager.create(
            title=task.get('title', ''),
            description=task.get('description', ''),
            status=task.get('status', False)
            )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.put("/tasks/{task_id}")
def update_task(task_id: int, task_update: dict):
    if not isinstance(task_update, dict):
        raise HTTPException(status_code=400, detail='Invalid data format')
    update = task_manager.update(task_id, **task_update)
    if not update:
        raise  HTTPException(404, 'Task not found')
    return update

@app.delete('/tasks/{task_id}')
def delete_task(task_id: int):
    result = task_manager.delete(task_id)
    if not result:
        raise HTTPException(status_code=404, detail='Task not found')
    return {'message': 'Task deleted'}