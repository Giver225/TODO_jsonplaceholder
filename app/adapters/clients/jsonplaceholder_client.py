import requests

class JSONPlaceholderClient:
    BASE_URL = "https://my-json-server.typicode.com/Giver225/JSONPlaceholder_db"

    def get_tasks(self):
        response = requests.get(f"{self.BASE_URL}/todos")
        response.raise_for_status()
        return response.json()

    def create_task(self, task_data):
        response = requests.post(f"{self.BASE_URL}/todos", json=task_data)
        response.raise_for_status()
        return response.json()

    def update_task(self, task_id, task_data):
        response = requests.put(f"{self.BASE_URL}/todos/{task_id}", json=task_data)
        response.raise_for_status()
        return response.json()
    
    def delete_task(self, task_id):
        response = requests.delete(f"{self.BASE_URL}/todos/{task_id}")
        response.raise_for_status()
        return response.json()
    