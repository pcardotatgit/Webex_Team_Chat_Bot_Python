'''
    List rooms of the Webex Team Bot
'''
import requests
import json
from crayons import green

BOT_ACCESS_TOKEN = 'PUT HERE THE WEBEX TEAM BOT BEARER TOKEN'

URL = f'https://webexapis.com/v1/rooms'
headers = {'Authorization': 'Bearer ' + BOT_ACCESS_TOKEN,
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