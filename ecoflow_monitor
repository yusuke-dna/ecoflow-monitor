import json
import time
from datetime import datetime

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
    # Import the requests library
    import requests
    # Create the headers
    headers = {
        'Content-Type': 'application/json',
        'appKey': appKey,
        'secretKey': secretKey
    }
    # Send the request
    response = requests.get(URL + Serial, headers=headers)
    # Get the response data
    data = response.json()
    return data

def ecoflow_logger(URL:str, Serial:str, appKey:str, secretKey:str, filepath:str):
  # Get the data from the EcoFlow device
    ecoflow_json = ecoflow_get(URL, Serial, appKey, secretKey)
    # Convert the data to a string
    data_dic = ecoflow_json.get('data')
    # Convert dic to CSV string
    data_str = dic_to_csv(data_dic)
    # Get current time
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    # Add timestamp at the most left of data_dic
    data = timestamp + ',' + data_str
    # Write the data to the file
    write_log(filepath, data)

args = argument_parser()
URL = args.url
Serial = args.serial
appKey = args.appkey
secretKey = args.secretkey
filepath = args.filepath

# Run the script every 5 minutes
while True:
    ecoflow_logger(URL, Serial, appKey, secretKey, filepath)
    time.sleep(300)
