import os
import time
import logging
from slack_sdk import WebClient
from slack_sdk.errors import SlackApiError


def auth_slack():
    return os.environ.get("BEARER_TOKEN_SLACK")


def post_message_to_slack(slack_client, msg, attachments = None):

    try:
        slack_client.chat_postMessage(channel=os.environ.get("SLACK_CHANNEL_NAME"), text=msg, attachments = attachments)
    except SlackApiError as e:
        logging.error("Request to Slack API Failed: {}.".format(e.response.status_code))
        logging.error(e.response)


def retrieve_messages_from_slack(slack_client, ts_old):

    try:
        return slack_client.conversations_history(channel=os.environ.get("SLACK_CHANNEL_ID"), oldest = ts_old)
    except SlackApiError as e:
        logging.error("Request to Slack API Failed: {}.".format(e.response.status_code))
        logging.error(e.response)


def slackbot(action_string,msg = None, attachments = None, time_stamp = None):
    slack_bot_token = auth_slack()
    slack_client = WebClient(slack_bot_token)
    # # For testing
    # msg = "Good Afternoon! Testing from Python script"
    
    if action_string == "post_message":
        post_message_to_slack(slack_client, msg, attachments)
    if action_string == "retrieve_message":
        response = retrieve_messages_from_slack(slack_client, time_stamp)
        return response
        #print(response)
