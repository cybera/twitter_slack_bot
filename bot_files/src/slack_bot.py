import os
import time
import logging
from slack_sdk import WebClient
from slack_sdk.errors import SlackApiError


def auth_slack():
    return os.environ.get("SLACK_BOT_TOKEN")


def post_message_to_slack(slack_client, msg, attachments=None, channel_id=None):

    try:
        if channel_id:
            slack_client.chat_postMessage(
                channel=channel_id,
                text=msg,
                attachments=attachments,
            )
        else:
            slack_client.chat_postMessage(
                channel=os.environ.get("SLACK_CHANNEL_NAME"),
                text=msg,
                attachments=attachments,
            )
    except SlackApiError as e:
        # You will get a SlackApiError if "ok" is False
        assert e.response["ok"] is False
        assert e.response["error"]  # str like 'invalid_auth', 'channel_not_found'
        print(f"Got an error: {e.response['error']}")


def slackbot(msg, attachments=None, channel_id=None):

    slack_bot_token = auth_slack()
    slack_client = WebClient(slack_bot_token)
    post_message_to_slack(slack_client, msg, attachments, channel_id)
