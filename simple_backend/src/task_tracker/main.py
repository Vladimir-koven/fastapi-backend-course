from fastapi import FastAPI, HTTPException
from task_manager import TaskManager

app = FastAPI()
task_manager = TaskManager()

@app.get("/tasks")
def get_tasks():
    return task_manager.get_all()

@app.post("/tasks")
def create_task(task):
    return task_manager.create(
        task.get('title', ''),
        task.get('description', ''),
        task.get('status', False)
        )

@app.put("/tasks/{task_id}")
def update_task(task_id: int, task_update: dict):
    update = task_manager.update(task_id, **task_update)
    if not update:
        raise  HTTPException(404, 'Task not found')
    return update

@app.delete("/tasks/{task_id}")
def delete_task(task_id: int):
    result = task_manager.delete(task_id)
    if not result:
        raise HTTPException(status_code=404, detail='Task not found')
    return {'message': 'Task deleted'}