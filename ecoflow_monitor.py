import json
import time
from datetime import datetime
import pytz
import argparse
import requests

def argument_parser():
    # Same as before
    ...

def write_log(filepath:str, data:str):
    # Same as before
    ...

def dic_to_csv(data_dic:str):
    # Same as before
    ...

def ecoflow_get(URL:str, Serial:str, appKey:str, secretKey:str):
    headers = {
        'Content-Type': 'application/json',
        'appKey': appKey,
        'secretKey': secretKey
    }
    try:
        response = requests.get(URL + Serial, headers=headers, timeout=10)
        data = response.json()
        return data
    except requests.exceptions.Timeout:
        print("Timeout error occurred. Will retry after 5 minutes.")
        time.sleep(300)
        return None
    except:
        raise

def ecoflow_logger(URL:str, Serial:str, appKey:str, secretKey:str, filepath:str):
    ecoflow_json = ecoflow_get(URL, Serial, appKey, secretKey)
    if ecoflow_json is None:
        return
    data_dic = ecoflow_json.get('data')
    data_str = dic_to_csv(data_dic)
    
    timestamp = datetime.now(pytz.timezone('UTC')).astimezone(pytz.timezone('Asia/Tokyo')).strftime("%Y-%m-%d %H:%M:%S")
    data = timestamp + ',' + data_str
    write_log(filepath, data)

args = argument_parser()
URL = args.url
Serial = args.serial
appKey = args.appkey
secretKey = args.secretkey
filepath = args.filepath

while True:
    ecoflow_logger(URL, Serial, appKey, secretKey, filepath)
    time.sleep(300)
