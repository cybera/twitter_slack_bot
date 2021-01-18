from slack_sdk import WebClient
import os
from flask import Flask 
from slackeventsapi import SlackEventAdapter

app= Flask(__name__)

slack_event_adapter = SlackEventAdapter(os.environ['SLACK_SIGNING_SECRET'], '/slack/events' , app)

slack_client = WebClient(token = os.environ['SLACK_BOT_TOKEN'])

@slack_event_adapter.on('app_mention')
def message(payload):
    event = payload.get('event',{})
    channel_id = event.get('channel')
    user_id = event.get('user')
    text = event.get('text')
    slack_client.chat_postMessage(channel=channel_id,text=text)


if __name__ == "__main__":
    app.run(host='0.0.0.0', debug=True, port=6789)