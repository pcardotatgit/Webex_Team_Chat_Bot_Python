# Introduction

In this repo you will find instructions for :

- Creating a Webex Team Bot 
- Adding a Webhook to your Webex Team Bot.
- Installing a Pedagogic Python Web logic to your Webex bot. 
- Interact with your bot through it's own Webex Team Room.

The goal of this article is mainly help you to understand how it work and how to start quickly.

# Create a Webex Team Bot

Webex Team Bot are very good interfaces for applications which doesn't have any GUI or output console ( Python scripts or SecureX Workflows for examples ). It is worthit to understand how we could use it in our Networking and Security Applications.

The benefits of using a Webex Team bot is that it will have a permanent Webex Bearer Token. 

Let's create this bot.

Let's go to [Cisco Webex for Developper]('https://developer.webex.com/my-apps')

 ![](img/webex_team_bot-1.gif)

Click on the **start building apps** button and create an new application

![](img/webex_team_bot-2.gif)


Fill all requested fields and create your new bot.

![](img/webex_team_bot-3.gif)
![](img/webex_team_bot-3a.gif)

Once created **COPY THE WEBEX BOT TOKEN !!**  and copy it's mail as well.

![](img/webex_team_bot-3b.gif)

## Create a webhook

One of magic of Webex Team bots is that you can interact directly with them.  You can send them messages and they will answer to you !.

For doing this you need a Webhook.

The Webex Webhook will allow to any web server to receive all the messages which will be sent to the room.

These message will be copied when they will received in the Webex Team Room and sent to the Web server URL.

The Web Server is any web server and the logic inside which can process the sent data by the webhook.

Actually the message is sent thanks to a HTTP **POST** call which act exactly as the calls used to send a formular to a web server.

![](img/webex_team_bot-12.gif)

That means that the web server will act exactly like any web server. It will read the variables sent thru this call and will process them.

The result of the data processing will be an HTTP result containing all the information to be sent as results.

And these results will be sent to the webex team room thanks to Send Message API call to the room ID, with the Webex BOT BEARER TOKEN.

Let's have a look now to how to set up all this.

## The Webhook

Before talking about the bot logic, let's see how to create the webhook which will be used to hook the messages sent to the Webex Team Room

go to :

[Create a Webhook]('https://developer.webex.com/docs/api/v1/webhooks/create-a-webhook')

The **targetURL** must be your Web **Server public URL**

And use Your **Bot Webex BEARER TOKEN**

![](img/webex_team_bot-13.gif)
![](img/webex_team_bot-14.gif)

**resource = messages**

**event = created**

**targetUrl** is the full URL of your bot.Either you have a public Web Server... or not. If not, and for developpment purpose only, consider **NGROK**. NGROK makes Your developpment BOT located into your laptop available on the INTERNET in less than 5 minutes.

**Remark :** the **update_webhook.py** file can help you to automate your bot targetUrl.

[Configure the project to run on your local PC]('https://developer.cisco.com/learning/lab/collab-spark-botkit/step/4')

## The BOT Webex Room

Starting from now, we are going to use the BOT Webex Room Id, in order to interact with it.

Go to your Webex Team and **contact** your bot thanks to it's mail.

![](img/webex_team_bot-16.gif)

And enter to the Bot's room. 
As test, You can send some test messages into the room.  

Nothing will happen until we add the bot logic.

Locate the BOT ROOM ID then. We will use it as the Destination ROOM ID in our logic scripts.

You can use the **list_room.py** to help you to get this room id.

Edit this file, assign to the **BOT_ACCESS_TOKEN** variable at the top of this file the value of the BOT Bearer Token and run the file.

It will return you the Bot's room ID.

Or go to the Webex Developer documentation, use the Webex BOT token to call the **/v1/rooms** api call to get this room id.

## The Bot Logic

The Webex Team Bot logic attached to the Webex Team Bot, is just a web server which listens to webhook calls. Everytime a message is send into the Bot's room, a webhook call is sent to a target URL that will be our Bot Logic Web Server.

This Bot Logic Web Server is the **python_webex-bot.py** python file.

## Make Your Bot Logic available on the INTERNET

We need to make our bot logic publicly available for Webex.

**NGROK** is a wonderful tool for doing that in minutes. NGROK exposes a public URL on the INTERNET and built a tunnel between this public location and an application within your laptop.

![](img/relay_module-51b.png )

### install NGROK

https://ngrok.com/download

![](img/relay_module-14.png )

Open a new CMD console window.  Change directory to the folder where you unzipped ngrok and start it thanks the following command.

    cd {ngrok directory}
    ngrok http 3000

![](img/relay_module-15.png )

We will see later that our bot logic will listen on port 3000.

Copy the NGROK FQDN that was assigned to you ( it will remain available during 7 hours ), we will used it later.

Perfect,  We are now ready  to go to the next step that is to install and start our bot logic server.

## Install and start your bot logic web server

Create a working directory named **bot_logic** into your laptop, and cd to it.

Open a terminal window ( Windows CMD console )

For Windows:

    md bot_logic
    cd bot_logic

For Linux

    mkdir bot_logic
    cd bot_logic
    
### Start your python virtual environment

For Linux/Mac 

	python3 -m venv venv
	source venv/bin/activate

For Windows 

	virtualenv env 
	\env\Scripts\activate.bat 
	
or
	
	python -m venv venv 
	venv\Scripts\activate

### clone the bot logic code

Then clone the code :

    git clone https://github.com/pcardotatgit/Webex_Team_Chat_Bot_Python.git

Change directory to the bot logic folder:

    cd Webex_Team_Chat_Bot_Python

### Install Python Modules

    python -m pip install --upgrade pip
    pip install -r requirements.txt

## Edit the config.py initialization file

**config.py** is an init file that contains Your Webex Team Bot details. 

Edit this file and assign the correct values to the listed variables

bot_email = "ex:my_python_bot@webex.bot"
bot_name = "ex:my_python_bot"
bearer = "THE_Webex_Bot_Bearer_token_here"
webhook_url = 'targetUrl here ex:http://db19a7dc123.ngrok.io'
webhook_name = 'ex:My_Web_Hook'

### Start your bot logic 

    python python_webex-bot.py

![](img/webex_team_bot-17.png )

As you can see, the application tells you that it is listening on port 3000.	
You can change that in the python script ( Line 242 )

	httpd = HTTPServer(('localhost', 3000), SimpleHTTPRequestHandler)
	
And don't forget to start NGROK on that port.

**Let's test the bot !**

At this point, we can test that the bot work.

Go the Bot Webex Room and send **ping** into it.

![](img/webex_team_bot-18.png)

Now you should receive back the message : **PONG !**

And you can check the python bot console

![](img/webex_team_bot-19.png)

Same in the NGROK console

![](img/webex_team_bot-20.png)

Now send **help** into the Bot's room and have a look to the result

## Add New functions to your bot logic

As your bot logic works, you can modify it's behavior.

Edit the **python_webex-bot.py** file and go to the **def do_POST(self):** function.

Ok it's up to YOU now !!

## Credits


- https://github.com/dmkazakoff/WebexTeams-Investigation-Bot
