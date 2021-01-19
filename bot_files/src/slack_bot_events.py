from slack_sdk import WebClient
import os
from flask import Flask 
from slackeventsapi import SlackEventAdapter
from slack_bot import slackbot
import re

app= Flask(__name__)

slack_event_adapter = SlackEventAdapter(os.environ['SLACK_SIGNING_SECRET'], '/slack/events' , app)

query_file_path = "twitter_queries/twitter_queries.txt"

def process_incoming_bot_message(channel_id, text):
    text = re.sub(r'\<.*?\>', '', text)
    print(text)
    if text[0:6].strip() == 'from:':
        with open(query_file_path, "a") as queryfile:
                        queryfile.write("\n" + text.lstrip())
        post_text = "Success!! Added " + "*" + text[6:] + "*" + " to the twitter queries:white_check_mark: :blush: "
        slackbot(msg=post_text,channel_id=channel_id)
    elif text[0:5].strip() == 'HELP':
        post_text = "Call the bot and text *from:<twitter-username>* :speech_balloon:"
        slackbot(msg=post_text,channel_id=channel_id)
    elif text[0:9].strip() == 'SHOW ALL':
        with open(query_file_path, "r") as f:
            query_content = f.readlines()
            query_list = [x.strip() for x in query_content]
            post_text = "Listing all queries:page_with_curl:"
            slackbot(msg=post_text,channel_id=channel_id)
            for query in query_list:
                slackbot(msg=query,channel_id=channel_id)
    else:
        post_text = "Invalid query! Please try again:X: :face_with_rolling_eyes:" 
        slackbot(msg=post_text,channel_id=channel_id)
        post_text = "Call the bot and text *HELP* for support:thinking_face:"
        slackbot(msg=post_text,channel_id=channel_id)

@slack_event_adapter.on('app_mention')
def message(payload):
    event = payload.get('event',{})
    channel_id = event.get('channel')
    user_id = event.get('user')
    text = event.get('text')
    process_incoming_bot_message(channel_id, text)


if __name__ == "__main__":
    app.run(host='0.0.0.0', debug=True, port=6789)