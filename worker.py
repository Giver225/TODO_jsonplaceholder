import asyncio
from temporalio.client import Client
from app.core.workflows.task_workflow import TaskWorkflow

async def main():
    client = await Client.connect("localhost:7233")
    await client.execute_workflow(
        TaskWorkflow.run,
        {"task": "example"},
        id="task-workflow",
        task_queue="task-queue",
    )

if __name__ == "__main__":
    asyncio.run(main())