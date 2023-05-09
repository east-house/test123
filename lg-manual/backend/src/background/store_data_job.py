import io
import logging
import numpy as np
from typing import Any, Dict

from background.redis_client import redis_client
from transformers import AutoTokenizer, RobertaTokenizer

logger = logging.getLogger(__name__)

def make_data_key(key: str) -> str:
    return f"{key}_sent"

def left_push_queue(queue_name : str, key: str)-> bool:
    try:
        redis_client.lpush(queue_name, key)
        return True
    except Exception as e:
        print("Error message : ",e)
        return False

def right_pop_queue(queue_name: str) -> Any:
    if redis_client.llen(queue_name) > 0:
        return redis_client.rpop(queue_name)
    else:
        return None

def set_data_redis(key:str, value:str)-> bool:
    redis_client.set(key, value)
    return True

def get_data_redis(key: str)-> Any:
    data = redis_client.get(key)
    return data



def padding_array(aa, fixed_length=256, padding_value=0):
    rows = []
    for a in aa:
        rows.append(np.pad(a, (0, fixed_length), 'constant', constant_values=padding_value)[:fixed_length])
    return np.concatenate(rows, axis=0).reshape(-1, fixed_length)

def set_sent_redis(key:str, sent) -> str:
    sent_key = make_data_key(key)
    tokenizer = AutoTokenizer.from_pretrained('obrizum/all-MiniLM-L6-v2')
    encoded_input = tokenizer(sent, padding=True, truncation=True, max_length=256, return_tensors='pt')
    
    input_ids = padding_array(encoded_input['input_ids'])
    print('input_ids:',input_ids.shape)
    token_type_ids = padding_array(encoded_input['token_type_ids'])
    attention_mask = padding_array(encoded_input['attention_mask'])
    encoded = [input_ids.tobytes(), token_type_ids.tobytes(), attention_mask.tobytes()]

    redis_client.set(sent_key, str(encoded))
    return sent_key

def get_sent_redis(key:str):
    redis_data = redis_client.get(key)
    sent_list = [np.frombuffer(arr, dtype=np.int64) for arr in eval(redis_data)]
    return sent_list

def save_sent_redis_job(job_id:str, sent)->bool:
    set_sent_redis(job_id, sent)
    redis_client.set(job_id, "")
    return True

