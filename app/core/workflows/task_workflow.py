from temporalio import workflow

@workflow.defn
class TaskWorkflow:
    @workflow.run
    async def run(self, task_data: dict):
        # Логика рабочего процесса
        return {"status": "Task processed successfully"}