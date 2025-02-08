from app.adapters.clients.jsonplaceholder_client import JSONPlaceholderClient

class TaskService:
    def __init__(self):
        self.client = JSONPlaceholderClient()

    def get_tasks(self):
        return self.client.get_tasks()

    def create_task(self, task_data):
        return self.client.create_task(task_data)

    def update_task(self, task_id, task_data):
        return self.client.update_task(task_id, task_data)