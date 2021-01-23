'''
Copyright (c) 2020 Cisco and/or its affiliates.

This software is licensed to you under the terms of the Cisco Sample
Code License, Version 1.1 (the "License"). You may obtain a copy of the
License at

               https://developer.cisco.com/docs/licenses

All use of the material herein must be in accordance with the terms of
the License. All rights not expressly granted by the License are
reserved. Unless required by applicable law or agreed to separately in
writing, software distributed under the License is distributed on an "AS
IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express
or implied.

'''
from http.server import HTTPServer, BaseHTTPRequestHandler
import urllib.request as urllib2
import json
import ssl
import re
import requests
from operator import itemgetter
from config import *
from crayons import cyan,red,green,yellow

ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE

# USED FOR OFF-LINE DEBUG
debug_flag = True

class SimpleHTTPRequestHandler(BaseHTTPRequestHandler):
    def do_POST(self):
        content_length = int(self.headers['Content-Length'])
        body = self.rfile.read(content_length)
        self.send_response(200)
        self.end_headers()
        print(cyan('Webhook triggered',bold=True))
        webhook = json.loads(body)
        print(green('    Retreive message',bold=True))
        result = send_webex_get('https://webexapis.com/v1/messages/{0}'.format(webhook['data']['id']))
        result = json.loads(result)
        if webhook['data']['personEmail'] != bot_email:
            in_message = result.get('text', '').lower()
            in_message = in_message.replace(bot_name.lower(), '')
            print(yellow("Message :",bold=True))
            print(cyan(in_message,bold=True))
            if in_message.startswith('help'):
                print(yellow("help received let s reply",bold=True))
                msg = '''**How To Use:**\n- **help**, bring this help; \n- **:command-1**, trigger some python function 
                \n- **:command-2**, trigger some python function 2\n
                '''
                send_webex_post("https://webexapis.com/v1/messages",
                                {"roomId": webhook['data']['roomId'], "markdown": msg})
            elif in_message.startswith('ping'):
                print(yellow("let s reply to thind ping",bold=True))
                send_webex_post("https://webexapis.com/v1/messages",
                               {"roomId": webhook['data']['roomId'], "markdown": "*PONG !*"}  ) 
            elif in_message.startswith(':command-1'):
                print(yellow("command-1",bold=True))
                send_webex_post("https://webexapis.com/v1/messages",
                               {"roomId": webhook['data']['roomId'], "markdown": "*Do this* - ( line 65 in the script )"}  )   
            elif in_message.startswith(':command-2'):
                print(yellow("command-2",bold=True))
                send_webex_post("https://webexapis.com/v1/messages",                               {"roomId": webhook['data']['roomId'], "markdown": "*Do that- ( line 68 in the script )*"}  )                                 
            else:
                send_webex_post("https://webexapis.com/v1/messages",
                                {"roomId": webhook['data']['roomId'], "markdown": "*I don't understand this*"})
        else:
            print(cyan('This is a message is a reply sent by BOT. Don t handle it',bold=True))
        return "true"
def json_loads_byteified(json_text):
    return _byteify(
        json.loads(json_text, object_hook=_byteify),
        ignore_dicts=True
    )

def json_load_byteified(file_handle):
    return _byteify(
        json.load(file_handle, object_hook=_byteify),
        ignore_dicts=True
    )

def _byteify(data, ignore_dicts=False):
    if type(data) == 'str':
        return data.encode('utf-8')
    if isinstance(data, list):
        return [_byteify(item, ignore_dicts=True) for item in data]
    if isinstance(data, dict) and not ignore_dicts:
        return {
            _byteify(key, ignore_dicts=True): _byteify(value, ignore_dicts=True)
            for key, value in data.items()
        }
    return data
    
def send_webex_get(url):
    request = urllib2.Request(url,
                              headers={"Accept": "application/json",
                                       "Content-Type": "application/json"})
    request.add_header("Authorization", "Bearer " + bearer)
    contents = urllib2.urlopen(request, context=ctx).read()
    return contents

def send_webex_post(url, data):
    request = urllib2.Request(url, json.dumps(data).encode('utf-8'),
                              headers={"Accept": "application/json",
                                       "Content-Type": "application/json"})
    request.add_header("Authorization", "Bearer " + bearer)
    contents = urllib2.urlopen(request, context=ctx).read()
    return contents
    
def index(request):
    print(request)
    webhook = json.loads(request.body)
    result = send_webex_get('https://webexapis.com/v1/messages/{0}'.format(webhook['data']['id']))
    result = json.loads(result)
    if webhook['data']['personEmail'] != bot_email:
        in_message = result.get('text', '').lower()
        in_message = in_message.replace(bot_name.lower(), '')
        if in_message.startswith('help'):
            msg = "**How To Use:**\n- *help*, bring this help; \n- *investigate*, put your indicators in free " \
                  "form or with types specified explicitly (<type>:\"observable\"), types:  " \
                  "\n    - " + '  \n    - '.join(observable_types_list)

            send_webex_post("https://webexapis.com/v1/messages",
                            {"roomId": webhook['data']['roomId'], "markdown": msg})
        else:
            send_webex_post("https://webexapis.com/v1/messages",
                            {"roomId": webhook['data']['roomId'], "markdown": "*Let the investigation begin...*"})

            analyze_string_investigation(in_message)

            send_webex_post("https://webexapis.com/v1/messages",
                            {"roomId": webhook['data']['roomId'], "markdown": "***  \n" + '  \n'.join(investigation_report) + "\n\n***"})

            send_webex_post("https://webexapis.com/v1/messages",
                            {"roomId": webhook['data']['roomId'],
                           "markdown": "*Mission accomplished, observe my findings above...*"})
        investigation_report = []

    return "true"


def webex_print(header, message):
    global investigation_report
    if debug_flag:
        print(header + message.replace('\n', ''))
    investigation_report.append(header + message)
    return

def delete_webhook(webhook_id):

    url = "https://webexapis.com/v1/webhooks/" + webhook_id

    payload = {}
    headers = {
        'Content-Type': 'application/json',
        'Authorization': "Bearer " + bearer
    }

    requests.request("DELETE", url, headers=headers, data=payload)


def add_webhook():

    url = "https://webexapis.com/v1/webhooks"
    payload = "{\"name\": \"" + webhook_name + "\",\"targetUrl\": \"" + webhook_url + "\",\"resource\": \"messages\",\"event\": \"created\"}"
    headers = {
        'Content-Type': 'application/json',
        'Authorization': 'Bearer ' + bearer
    }

    response = requests.request("POST", url, headers=headers, data=payload)
    print(response)


def update_webhook():

    url = "https://webexapis.com/v1/webhooks"
    payload = "{\"name\": \"" + webhook_name + "\",\"targetUrl\": \"" + webhook_url + "\",\"status\": \"active\"}"
    headers = {
        'Content-Type': 'application/json',
        'Authorization': 'Bearer ' + bearer
    }

    requests.request("PUT", url, headers=headers, data=payload)


def get_bot_status():
    url = "https://webexapis.com/v1/rooms"
    payload = {}
    headers = {
        'Content-Type': 'application/json',
        'Authorization': "Bearer " + bearer
    }

    response = requests.request("GET", url, headers=headers, data=payload)
    data = json_loads_byteified(response.text)
    print(yellow("Bot is currently member of Webex Rooms:",bold=True))
    if 'items' in data:
        for room in data['items']:
            print(green("     ID: {}".format(room['id']),bold=True))

    url = "https://webexapis.com/v1/webhooks"
    response = requests.request("GET", url, headers=headers, data=payload)
    data = json_loads_byteified(response.text)
    print(green("Bot is currently configured with webhooks:",bold=True))
    if 'items' in data:
        for webhook in data['items']:
            print(" => ID: {}".format(webhook['id']))
            print("     Name: {}".format(webhook['name'].encode('utf8')))
            print("     Url: {}".format(webhook['targetUrl']))
            print(green("     Status: {}".format(webhook['status']),bold=True))
            if webhook['name'] != webhook_name:
                print("    === REMOVING WEBHOOK ===")
                delete_webhook(webhook['id'])
                print("    === REMOVED ===")
            if webhook['status'] != 'active':
                print("    === UPDATING WEBHOOK STATUS ===")
                update_webhook()
                print("    === STATUS UPDATED ===")
            if (webhook['targetUrl'] != webhook_url):
                print("    === NEED TO UPDATE WEBHOOK ===")
                delete_webhook(webhook['id'])
                print("    === OLD WEBHOOK REMOVED ===")
                print("    === ADDING NEW WEBHOOK ===")
                add_webhook()
                print("    === NEW WEBHOOK ADDED ===")
        if len(data['items']) == 0:
            print("    === NO WEBHOOKS DETECTED ===")
            add_webhook()
            print("    === NEW WEBHOOK ADDED  ===")        
def main():
    print(yellow("Don't forget to start NGROK with : ngrok http 3000",bold=True))
    print()
    print(yellow("Let's check the Webex Team Bot Status",bold=True))
    get_bot_status()
    print(yellow("Bot Ready, Let's start the Web Server and listen on Port 3000",bold=True))
    httpd = HTTPServer(('localhost', 3000), SimpleHTTPRequestHandler)
    httpd.serve_forever()


if __name__== "__main__":
    main()
