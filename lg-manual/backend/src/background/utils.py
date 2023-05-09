import pandas as pd
import re

def excel_parser(excel_path):
    def refine_function(data):
        if data == str:
            temp = data.replace('\n',' ')
            while temp and not temp[0].isalnum():
                temp = temp[1:]
            return str(temp)
        else:
            return data
    df = pd.read_excel(excel_path)
    df = df.loc[:,'Unnamed: 0':'Unnamed: 8']
    columns = list(df.iloc[1])
    columns = [re.sub(' ','_',a.strip()) for a in columns]
    df=df.iloc[2:].reset_index(drop=True)
    df.columns = columns
    df['Checking_data'] = df['Checking_data'].apply(lambda x : refine_function(x))
    df = df.fillna('')
    return df