import os
from cloud_storage import JSONBinStorage
from cloudflare_ai import CloudflareAI
from dotenv import load_dotenv
from pydantic import BaseModel
from typing import Optional, List

load_dotenv('passwords.env')

class TaskModel(BaseModel):
    title: str
    description: Optional[str] = None
    status: bool = False

class TaskResponse(TaskModel):
    id: int
    ai_solution: Optional[str] = None

class TaskManager:
    def __init__(self):
        self.bin_id = os.getenv('JSON_BIN_ID')
        self.api_key = os.getenv('JSON_API_KEY')
        if not self.bin_id or not self.api_key:
            raise ValueError('Не найдены JSON_BIN_ID или JSON_API_KEY')
        self.storage = JSONBinStorage(self.bin_id, self.api_key)
        self.ai = CloudflareAI()

    def _tasks(self) -> List[dict]:
        return self.storage.load_data()

    def get_all(self) -> List[TaskResponse]:
        tasks = self._tasks()
        return [TaskResponse(**task) for task in tasks]

    def _save(self, tasks):
        self.storage.save_data(tasks)

    def create(self, title: str, description: str = '', status: bool = False) -> TaskResponse:
        task_data = TaskModel(title=title, description=description, status=status)
        tasks = self._tasks()
        ids = [task['id'] for task in tasks] if tasks else []
        task_id = max(ids) + 1 if ids else 1
        ai_solution = ''
        if task_data.description:
            try:
                ai_solution = self.ai.generate_solution(f'{task_data.title}. {task_data.description}')
            except Exception as e:
                ai_solution = f'{e}. Не удалось сгенерировать решение'

        new_task = {'id': task_id,
                    'title': task_data.title,
                    'description': task_data.description,
                    'status': task_data.status,
                    'ai_solution': ai_solution,
                    }
        tasks.append(new_task)
        self._save(tasks)
        return TaskResponse(**new_task)

    def update(self, task_id: int, **updates) -> Optional[TaskResponse]:
        update_data = TaskModel(**updates)
        valid_updates = update_data.model_dump(exclude_unset=True)
        if not valid_updates:
            return None
        tasks = self._tasks()
        for task in tasks:
            if task['id'] == task_id:
                for k, v in valid_updates.items():
                    if v is not None:
                        task[k] = v
                self._save(tasks)
                return TaskResponse(**task)
        return None

    def delete(self, task_id: int) -> bool:
        tasks = self._tasks()
        initial_count = len(tasks)
        tasks = [task for task in tasks if task.get('id') != task_id]
        if len(tasks) == initial_count:
            return False
        self._save(tasks)
        return True