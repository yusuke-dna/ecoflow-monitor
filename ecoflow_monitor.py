import json
import time
from datetime import datetime
import pytz
import argparse
import requests

def argument_parser():
    # Import the argparse library
    import argparse
    # Create the parser
    my_parser = argparse.ArgumentParser(description='EcoFlow Monitor')
    # Add the arguments
    my_parser.add_argument('-u', '--url', type=str, help='URL of the EcoFlow device')
    my_parser.add_argument('-s', '--serial', type=str, help='Serial number of the EcoFlow device')
    my_parser.add_argument('-a', '--appkey', type=str, help='App key of the EcoFlow device')
    my_parser.add_argument('-k', '--secretkey', type=str, help='Secret key of the EcoFlow device')
    my_parser.add_argument('-f', '--filepath', type=str, help='File path of the log file')
    my_parser.add_argument('-I', '--on', type=str, help='URL of webhook to turn on charger')
    my_parser.add_argument('-O', '--off', type=str, help='URL of webhook to turn off charger')
    # Execute the parse_args() method
    args = my_parser.parse_args()
    # Return the arguments
    return args 

def write_log(filepath:str, data:str):
    # Open the file in append mode
    with open(filepath, 'a') as f:
        # Write the data to the file
        f.write(data)
        # Write a new line
        f.write('\n')

def dic_to_csv(data_dic:str):
    # Get the keys
    keys = data_dic.keys()
    # Get the values
    values = [str(value) for value in data_dic.values()]
    # Convert the keys to a string
    keys_str = ','.join(keys)
    # Convert the values to a string
    values_str = ','.join(values)
    # Combine the keys and values strings
    data_str = keys_str + ',' + values_str
    return data_str

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

def ecoflow_logger(URL:str, Serial:str, appKey:str, secretKey:str, filepath:str, charge_URL:str, discharge_URL:str):
    ecoflow_json = ecoflow_get(URL, Serial, appKey, secretKey)
    if ecoflow_json is None:
        return
    else:
        data_dic = ecoflow_json.get('data')
        data_str = dic_to_csv(data_dic)
    
        timestamp = datetime.now(pytz.timezone('UTC')).astimezone(pytz.timezone('Asia/Tokyo')).strftime("%Y-%m-%d %H:%M:%S")
        data = timestamp + ',' + data_str
        write_log(filepath, data)
        # charge if battery is lower than 20%
        if data_dic['soc'] < 20 :
            r = requests.get(charge_URL)
        # discharge if battery is charged above 50%
        elif data_dic['soc'] > 50 :
            r = requests.get(discharge_URL)

args = argument_parser()
URL = args.url
Serial = args.serial
appKey = args.appkey
secretKey = args.secretkey
filepath = args.filepath
charge_URL = args.on
discharge_URL = args.off

while True:
    ecoflow_logger(URL, Serial, appKey, secretKey, filepath, charge_URL, discharge_URL)
    time.sleep(300)
