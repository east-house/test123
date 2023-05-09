import base64
import io
import uuid
from logging import getLogger
from typing import Any, Dict

import requests
from fastapi import APIRouter, BackgroundTasks

from background import background_job, store_data_job, utils
from schemas.data import Data
from transformers import AutoTokenizer, RobertaTokenizer
# from configurations import ModelConfigurations

logger = getLogger(__name__)
router = APIRouter()

# health check
@router.get("/health")
def health()-> Dict[str, str]:
    respon = {
            "message": "True"
        }
    return respon

@router.get("/predict")
def predict(data:Data, background_tasks: BackgroundTasks) -> Dict[str, str]:
    tokenizer = AutoTokenizer.from_pretrained('sentence-transformers/all-MiniLM-L6-v2')
    max_num = len(data)
    encoded_input = tokenizer(sent_list, padding=True, truncation=True, max_length=256, return_tensors='pt')

    input_ids = padding_array(encoded_input['input_ids'])
    token_type_ids = padding_array(encoded_input['token_type_ids'])
    attention_mask = padding_array(encoded_input['attention_mask'])

    job_id = str(uuid.uuid4())[:6]
    background_job.save_data_job(
        data=[input_ids, token_type_ids, attention_mask],
        job_id=job_id,
        background_tasks=background_tasks,
        enqueue=True
    )
    return {'job_id': job_id}


@router.post('/predict/test')
def predict_test(background_tasks: BackgroundTasks, excel_path=None):
    job_id = str(uuid.uuid4())[:6]
    data = Data()
    excel_path ="/src/tmp_file/RAC_Printed_Material_Checklist_labeling_Type11_0425 (1).xlsx"
    # pdf_path ="/home/lee/workplace/lg_web/lg-manual/backend/src/tmp_file/MFL69491102-MN.pdf"
    excel_df = utils.excel_parser(excel_path)
    # print('excel_df : ',excel_df)
    # print(excel_df.shape)
    # print(excel_df.columns)
    data.sent_data = list(excel_df['Checking_data'])
    background_job.save_data_job(data.sent_data, job_id, background_tasks, True)
    return {'job_id': job_id}