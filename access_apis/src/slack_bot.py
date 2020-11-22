import os
import time
import logging
from slack.web.client import WebClient
from slack.errors import SlackApiError


def auth():
    return os.environ.get("BEARER_TOKEN_SLACK")


def post_message_to_slack(slack_client, msg):

    try:
        slack_client.chat_postMessage(channel="#testing", text=msg)
    except SlackApiError as e:
        logging.error("Request to Slack API Failed: {}.".format(e.response.status_code))
        logging.error(e.response)


def slackbot(msg):
    slack_bot_token = auth()
    slack_client = WebClient(slack_bot_token)
    # # For testing
    # msg = "Good Afternoon! Testing from Python script"
    post_message_to_slack(slack_client, msg)
