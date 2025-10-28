import json
import os

class TaskManager:
    def __init__(self, file="tasks.json"):
        self.file = file

    def _tasks(self):
        try:
            with open(self.file, 'r', encoding='utf-8') as f:
                return json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            return []

    def _save(self, tasks):
        try:
            with open(self.file, 'w', encoding='utf-8') as f:
                json.dump(tasks, f, indent=2, ensure_ascii=False)
            return True
        except Exception:
            return False

    def create(self, title, description="", status=False):
        tasks = self._tasks()
        if tasks:
            ids = [task['id'] for task in tasks if 'id' in task]
            task_id = max(ids) + 1 if ids else 1
        else:
            task_id = 1
        new_task = {"id": task_id,
                    "title": title,
                    "description": description,
                    "status": status
                    }
        tasks.append(new_task)
        self._save(tasks)
        return new_task

    def get_all(self):
        return self._tasks()

    def update(self, task_id, **updates):
        tasks = self._tasks()
        for task in tasks:
            if task['id'] == task_id:
                for k, v in updates.items():
                    if v is not None:
                        task[k] == v
                self._save(tasks)
                return task
        return None

    def delete(self, task_id):
        tasks = self._tasks()
        tasks = [task for task in tasks if task.get('id') != task_id]
        self._save(tasks)
        return True