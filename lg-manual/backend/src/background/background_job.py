import logging

from typing import Any, Dict, List, Optional
from fastapi import BackgroundTasks
from pydantic import BaseModel

from background.store_data_job import left_push_queue, save_sent_redis_job

logger = logging.getLogger(__name__)

class SaveDataJob(BaseModel):
    job_id: str
    data : Any
    queue_name: str = "redis_queue"
    is_completed: bool = False

    def __call__(self):
        pass

class SaveDataRedisJob(SaveDataJob):
    enqueue: bool = False
    def __call__(self):
        save_data_jobs[self.job_id]= self
        logger.info(f"registered job : {self.job_id} in {self.__class__.__name__}")
        self.is_completed = save_sent_redis_job(job_id = self.job_id, sent=self.data)
        if self.enqueue:
            self.is_completed = left_push_queue(self.queue_name, self.job_id)
        logger.info(f"completed save data: {self.job_id}")

def save_data_job(
    data: Any,
    job_id: str,
    background_tasks: BackgroundTasks,
    enqueue: bool = False
)-> str:
    task = SaveDataRedisJob(
        job_id = job_id,
        data = data,
        queue_name = "queue",
        enqueue = enqueue,
    )
    background_tasks.add_task(task)
    return job_id


save_data_jobs: Dict[str, SaveDataJob] = {}