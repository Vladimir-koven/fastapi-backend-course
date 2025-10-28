import json
import os


class TaskManager:
    def init(self, file="tasks.json"):
        self.file = file
        if not os.path.exists(file):
            with open(file, 'w') as f:
                json.dump([], f)

    def _tasks(self):
        with open(self.file, 'r') as f:
            return json.load(f)

    def _save(self, tasks):
        with open(self.file, 'w') as f:
            json.dump(tasks, f, indent=2)

    def create(self, title, description="", status=False):
        tasks = self._tasks()
        for task in tasks:
            task_id = max(task.get('id', 0), default=0) + 1
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
                        task.update(k, v)
                self._save(tasks)
                return task
        return None

    def delete(self, task_id):
        tasks = self._tasks()
        tasks = [t for t in tasks if t['id'] != task_id]
        self._save(tasks)
        return True