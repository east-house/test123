import asyncio
import base64
import io
import os
from concurrent.futures import ProcessPoolExecutor
from logging import DEBUG, Formatter, StreamHandler, getLogger
from time import sleep

from background import store_data_job, triton_api
import tritonclient.http as httpclient

log_format = Formatter("%(asctime)s %(name)s [%(levelname)s] %(message)s")
logger = getLogger("prediction_batch")
stdout_handler = StreamHandler()
stdout_handler.setFormatter(log_format)
logger.addHandler(stdout_handler)
logger.setLevel(DEBUG)


def _trigger_prediction_if_queue(stub):
    job_id = store_data_job.right_pop_queue("queue")
    logger.info(f"predict job_id: {job_id}")
    if job_id is not None:
        data = store_data_job.get_data_redis(job_id)
        if data !="":
            return True
        sent_key = store_data_job.make_data_key(job_id)
        sent_data = store_data_job.get_sent_redis(sent_key)
        predict = triton_api.request_http(stub, sent_data)

        if predict is not None:  # 응답이 성공적으로 오면
            logger.info(f"{job_id} {predict}")
            store_data_job.set_data_redis(job_id, predict)  # job id에 예측값 등록
        else:
            store_data_job.left_push_queue(CacheConfigurations.queue_name, job_id)  # 응답이 지연된 경우나 오지 않은 경우 다시 큐에 등록
        
def _loop():
    triton_client = httpclient.InferenceServerClient(
        url='triton:8000', verbose=False
        )

    while True:
        sleep(5)
        _trigger_prediction_if_queue(stub=triton_client)

# 멀티 프로세스로 기동
def prediction_loop(num_procs: int=2):
    excutor = ProcessPoolExecutor(num_procs)  # 병렬 연산을 위한 ProcessPoolExecutor
    loop = asyncio.get_event_loop()

    for _ in range(num_procs):
        asyncio.ensure_future(loop.run_in_executor(excutor, _loop()))

    loop.run_forever()

def main():
    NUM_PROCS = int(os.getenv("NUM_PROCS", 2))
    prediction_loop(NUM_PROCS)


if __name__ == '__main__':
    logger.info('start backend')
    main()