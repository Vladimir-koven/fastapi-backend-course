import json


class TaskManager:
    def __init__(self, file="tasks.json"):
        self.file = file

    def _tasks(self):
        try:
            with open(self.file, 'r') as f:
                return json.load(f)
        except FileNotFoundError:
            return []

    def _save(self, tasks):
        with open(self.file, 'w') as f:
            json.dump(tasks, f, indent=2)

    def create(self, title, description="", status=False):
        tasks = self._tasks()
        for task in tasks:
            task_id = max(task['id']) + 1
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
        tasks = [t for t in tasks if t['id'] != task_id]
        self._save(tasks)
        return True