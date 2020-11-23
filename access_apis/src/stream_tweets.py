#!/usr/bin/env python

import requests
import os
import json
import time
import datetime
import pandas as pd
import numpy as np
from flask import jsonify

from slack_bot import slackbot

# To set your enviornment variables in your terminal run the following line:
# export 'BEARER_TOKEN'='<your_bearer_token>'


def auth():
    return os.environ.get("BEARER_TOKEN_TWITTER")


def create_url(query, last_tweet=None):
    # Tweet fields are adjustable.
    # Options include:
    # attachments, author_id, context_annotations,
    # conversation_id, created_at, entities, geo, id,
    # in_reply_to_user_id, lang, non_public_metrics, organic_metrics,
    # possibly_sensitive, promoted_metrics, public_metrics, referenced_tweets,
    # source, text, and withheld
    if query:
        tweet_fields = "tweet.fields=created_at"
        expansion_field = "expansions=author_id"
        if last_tweet:
            since_id = "since_id=" + str(last_tweet)
            print("Accessing Last Tweet ", since_id)
            url = "https://api.twitter.com/2/tweets/search/recent?query={}&{}&{}&{}".format(
                query, tweet_fields, expansion_field, since_id
            )
        else:
            print("Accessing Last 10 Tweets")
            url = "https://api.twitter.com/2/tweets/search/recent?query={}&{}".format(
                query, tweet_fields, expansion_field
            )

    return url


def create_headers(bearer_token):
    headers = {"Authorization": "Bearer {}".format(bearer_token)}
    return headers


def connect_to_endpoint(url, headers):
    response = requests.request("GET", url, headers=headers)
    print(response.status_code)
    if response.status_code != 200:
        raise Exception(response.status_code, response.text)
    return response.json()


def real_time_tweets(query, first_time=None, last_tweet_id=None):
    # Access the bearer_token
    bearer_token = auth()
    # Send in the query string and last tweet

    if first_time:
        url = create_url(query)
        headers = create_headers(bearer_token)
        json_response = connect_to_endpoint(url, headers)
        if json_response:
            df_week_tweets = pd.json_normalize(json_response["data"])
            return df_week_tweets.loc[3, "id"]

    if last_tweet_id:
        since_id = last_tweet_id
        url = create_url(query, last_tweet=since_id)
        headers = create_headers(bearer_token)
        json_response = connect_to_endpoint(url, headers)
        tweet_count = json_response["meta"]["result_count"]
        if tweet_count != 0:
            # print(json.dumps(json_response, indent=4, sort_keys=True))
            df_tweet = pd.json_normalize(json_response["data"])
            df_name = pd.json_normalize(json_response["includes"]["users"])
            attachments_blocks= []
            for ind in np.arange(df_tweet.shape[0]):
                if ind==0:
                    name = "*" + df_name.loc[0, "name"] + "*"
                    username = "(" + df_name.loc[0, "username"] + ")  \n"
                    tweet_content = df_tweet.loc[ind, "text"]
                    msg = name + username + tweet_content
                else: 
                    tweet_attachment = { "type": "section", "text": { "type": "mrkdwn", "text": df_tweet.loc[ind, "text"] } }
                    attachments_blocks.append(tweet_attachment)
            slackbot(msg, attachments = [{'blocks': attachments_blocks}])
            print("Latest tweets are sent in slack messages.")
            return df_tweet.loc[0, "id"]

        else:
            print("No new tweets exist.")
            return since_id


if __name__ == "__main__":

    query_file_path = "./sample_queries.txt"

    with open(query_file_path, "r") as f:
        query_content = f.readlines()

    query_list = [x.strip() for x in query_content]
    list_last_ids = np.array([])

    for query in query_list:
        print("Running", query)
        last_id = real_time_tweets(query, first_time=True)
        list_last_ids = np.append(list_last_ids, last_id)

    while True:
        ind_flag = 0
        for query in query_list:
            last_id = real_time_tweets(query, last_tweet_id=list_last_ids[ind_flag])
            if last_id != list_last_ids[ind_flag]:
                list_last_ids[ind_flag] = last_id
            ind_flag += 1

        print("Last refreshed for new tweets at", datetime.datetime.now())
        time.sleep(20)
