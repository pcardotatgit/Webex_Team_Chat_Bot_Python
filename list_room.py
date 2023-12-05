'''
    List rooms the Webex Team Bot belongs to
'''
import requests
import json
from crayons import green
from config import *

URL = f'https://webexapis.com/v1/rooms'
headers = {'Authorization': 'Bearer ' + bearer,
           'Content-type': 'application/json;charset=utf-8'}
response = requests.get(URL, headers=headers)
#print(type(response))
if response.status_code == 200:
    print(json.dumps(response.json(),sort_keys=True,indent=4, separators=(',', ': ')))
    #result=json.dumps(response.json())
    result=response.json()
    the_id=result['items'][0]['id']
    print(green(the_id))
else:
    # Oops something went wrong...  Better do something about it.
    print(response.status_code, response.text)