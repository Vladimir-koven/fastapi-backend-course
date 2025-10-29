import os
from cloud_storage import JSONBinStorage
from dotenv import load_dotenv


load_dotenv('passwords.env')

class TaskManager:
    def __init__(self):
        self.bin_id = os.getenv('JSON_BIN_ID')
        self.api_key = os.getenv('JSON_API_KEY')
        if not self.bin_id or not self.api_key:
            raise ValueError('Не найдены JSON_BIN_ID или JSON_API_KEY')
        self.storage = JSONBinStorage(self.bin_id, self.api_key)

    def _tasks(self):
        return self.storage.load_data()

    def get_all(self):
        return self._tasks()

    def _save(self, tasks):
        return self.storage.save_data(tasks)

    def create(self, title, description='', status=False):
        tasks = self._tasks()
        ids = [task['id'] for task in tasks] if tasks else []
        task_id = max(ids) + 1 if ids else 1
        new_task = {'id': task_id,
                    'title': title,
                    'description': description,
                    'status': status
                    }
        tasks.append(new_task)
        self._save(tasks)
        return new_task

    def update(self, task_id, **updates):
        tasks = self._tasks()
        for task in tasks:
            if task['id'] == task_id:
                for k, v in updates.items():
                    if v is not None:
                        task[k] = v
                self._save(tasks)
                return task
        return None

    def delete(self, task_id):
        tasks = self._tasks()
        tasks = [task for task in tasks if task.get('id') != task_id]
        self._save(tasks)
        return True