#!/usr/bin/env python

import requests
import os
import json
import numpy as np

from twitter_apis import create_url_recent_search, connect_to_endpoint_recent_search
from slack_bot import slackbot

# To set your enviornment variables in your terminal run the following line:
# export 'BEARER_TOKEN'='<your_bearer_token>'
def auth_twitter():
    return os.environ.get("TWITTER_TOKEN")


def create_headers(bearer_token):
    headers = {"Authorization": "Bearer {}".format(bearer_token)}
    return headers


def real_time_tweets(query, first_time=None, last_tweet_id=None):
    # Access the bearer_token
    bearer_token = auth_twitter()
    # Send in the query string and last tweet

    if first_time:
        url_recent_search = create_url_recent_search(query)
        headers = create_headers(bearer_token)
        response_dict_recent_search = connect_to_endpoint_recent_search(
            url_recent_search, headers
        )
        tweet_count = response_dict_recent_search["meta"]["result_count"]
        if tweet_count != 0:
            return response_dict_recent_search["data"][0]["id"]
        else:
            return "1111111111111111111"

    if last_tweet_id:
        url_recent_search = create_url_recent_search(query, last_tweet=last_tweet_id)
        headers = create_headers(bearer_token)

        response_dict_recent_search = connect_to_endpoint_recent_search(
            url_recent_search, headers
        )

        tweet_count = response_dict_recent_search["meta"]["result_count"]

        if tweet_count != 0:

            name = response_dict_recent_search["includes"]["users"][0]["name"]
            username = response_dict_recent_search["includes"]["users"][0]["username"]

            for ind in range(len(response_dict_recent_search["data"])):
                status_id = response_dict_recent_search["data"][ind]["id"]
                try: 
                    response = response_dict_recent_search["data"][ind]["referenced_tweets"][0]['type']
                    msg = (
                        "*" + name + "*" + " | _" + username + "_ |" + " -" + response + "\n"
                    )
                    slackbot(msg)
                    msg = "https://twitter.com/" +  username + "/status/" + status_id
                    slackbot(msg)
                except:
                    msg = "https://twitter.com/" +  username + "/status/" + status_id
                    slackbot(msg)
#                tweet_content = response_dict_recent_search["data"][ind]["text"]
#                if ind == 0:
#                    msg = (
#                        "*" + name + "*" + " | _" + username + "_ | \n" + tweet_content
#                    )
#                    slackbot(msg)
#                else:
#                    msg = tweet_content
#                    if ind == (len(response_dict_recent_search["data"]) - 1):
#                        slackbot(
#                            msg,
#                            attachments=[{"blocks": [{"type": "divider"}]}],
#                        )
#                    else:
#                        slackbot(msg)
            print("Latest tweets are sent in slack messages.")
            return response_dict_recent_search["meta"]["newest_id"]

        else:
            print("No new tweets exist.")
            return last_tweet_id
