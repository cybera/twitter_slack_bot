#!/usr/bin/env python

import requests
import os
import json
import pandas as pd
import numpy as np

from twitter_apis import create_url_recent_search, connect_to_endpoint_recent_search
from slack_bot import slackbot

# To set your enviornment variables in your terminal run the following line:
# export 'BEARER_TOKEN'='<your_bearer_token>'
def auth():
    return os.environ.get("BEARER_TOKEN_TWITTER")


def create_headers(bearer_token):
    headers = {"Authorization": "Bearer {}".format(bearer_token)}
    return headers


def real_time_tweets(query, first_time=None, last_tweet_id=None):
    # Access the bearer_token
    bearer_token = auth()
    # Send in the query string and last tweet

    if first_time:
        url_recent_search = create_url_recent_search(query)
        headers = create_headers(bearer_token)
        json_response = connect_to_endpoint_recent_search(url_recent_search, headers)
        first_tweet_count = json_response["meta"]["result_count"]
        if first_tweet_count != 0:
            df_week_tweets = pd.json_normalize(json_response["data"])
            return df_week_tweets.loc[3, "id"]
        else:
            return "Invalid Input"

    if last_tweet_id:
        since_id = last_tweet_id
        url_recent_search = create_url_recent_search(query, last_tweet=since_id)
        headers = create_headers(bearer_token)
        json_response_recent_search = connect_to_endpoint_recent_search(
            url_recent_search, headers
        )
        tweet_count = json_response_recent_search["meta"]["result_count"]
        if tweet_count != 0:
            # print(json.dumps(json_response, indent=4, sort_keys=True))
            df_tweet = pd.json_normalize(json_response_recent_search["data"])
            df_name = pd.json_normalize(
                json_response_recent_search["includes"]["users"]
            )
            for ind in np.arange(df_tweet.shape[0]):
                if ind == 0:
                    name = df_name.loc[0, "name"]
                    username = df_name.loc[0, "username"]
                    tweet_content = df_tweet.loc[ind, "text"]
                    msg = (
                        "*" + name + "*" + " | _" + username + "_ | \n" + tweet_content
                    )
                    slackbot(msg)

                else:
                    tweet_content = df_tweet.loc[ind, "text"]
                    msg = tweet_content
                    if ind == (df_tweet.shape[0] - 1):
                        slackbot(
                            msg,
                            attachments=[{"blocks": [{"type": "divider"}]}],
                        )
                    else:
                        slackbot(msg)
            print("Latest tweets are sent in slack messages.")
            return df_tweet.loc[0, "id"]

        else:
            print("No new tweets exist.")
            return since_id
