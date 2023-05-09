import os
import json
import requests
import tritonclient.http as httpclient

def request_http(stub, sent_data):
    print('max_num :',sent_data[0])
    print(type(sent_data[0]))
    [input_ids, token_type_ids, attention_mask] = sent_data
    input0 = httpclient.InferInput('input__0', [max_num,256], 'INT64')
    input0.set_data_from_numpy(input_ids, binary_data=False)
    input1 = httpclient.InferInput('input__1', [max_num,256], 'INT64')
    input1.set_data_from_numpy(token_type_ids, binary_data=False)
    input2 = httpclient.InferInput('input__2', [max_num,256], 'INT64')
    input2.set_data_from_numpy(attention_mask, binary_data=False)
    output = httpclient.InferRequestedOutput('output__0',  binary_data=False)

    prediction = stub.infer(
                model_name='torch_sbert', inputs=[input0, input1, input2], 
                outputs=[output], headers={"context-type":"application/json"}
                )
    logits = response.as_numpy('output__0')
    return logits