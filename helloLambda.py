import json
import boto3
from botocore.vendored import requests

from datetime import datetime

def lambda_handler(event, context):
    # TODO implement

    current_date_time = datetime.now()
    datetime_str = str(current_date_time)
    object_name = "ctt" + datetime_str.replace(" ", "") + ".json"

    
    
    api_endpoint = "https://data.cityofchicago.org/resource/n4j6-wkkf.json"
    r = requests.get(api_endpoint)
    
    if ( r.status_code == 200):
        #API will return a list of dictionaries.  Each dictonary contains a traffic segment data point
        traffic_data_dict_list = r.json()     
        msg = "Request status OK"
    else:
    	msg = "Error Code "+str(r.status_code)
    	
    data = ""
    for segment in traffic_data_dict_list:
        line = str(segment) + '\n'
        data = data + line
        
    s3 = boto3.resource('s3')
    object = s3.Object('nolanchenbucket1',object_name)
    object.put(Body=data)
    
    return {
        'statusCode': 200,
        'body': json.dumps('Lambda executed at: '+ str(datetime.now())+" "+ msg)
    }
