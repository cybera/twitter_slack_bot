#!/usr/bin/env python
import os
import numpy as np
from datetime import datetime
import time

from stream_tweets_to_slack import real_time_tweets


def init_first_time(query_list):
    tot_size_first_time = len(query_list)
    list_last_ids = np.array([])
    print("Initializing all queries for the first time")
    for query in query_list:
        last_id = real_time_tweets(query, first_time=True)
        list_last_ids = np.append(list_last_ids, last_id)

    return list_last_ids


def call_twitter_slack_apis(query_list, list_last_ids):
    ind_flag = 0
    for query in query_list:
        if list_last_ids[ind_flag] != "1111111111111111111":
            print(query, list_last_ids[ind_flag])
            last_id = real_time_tweets(query, last_tweet_id=list_last_ids[ind_flag])
            if last_id != list_last_ids[ind_flag]:
                list_last_ids[ind_flag] = last_id
        ind_flag += 1

    return list_last_ids


def query_file_path():
    # In container
    # query_file_path = "/app/twitter_queries/twitter_queries.txt"
    # In normal environment
    # query_file_path = "twitter_queries/twitter_queries.txt"
    return "twitter_queries/twitter_queries.txt"


if __name__ == "__main__":

    # In container
    # query_file_path = "/app/twitter_queries/twitter_queries.txt"
    # In normal environment
    file_path = query_file_path()
    flag_first_time = True
    now = datetime.now()
    timestampnow = datetime.timestamp(now)

    while True:

        if flag_first_time:
            with open(file_path, "r") as f:
                query_content = f.readlines()
            query_list = [x.strip() for x in query_content]

            if flag_first_time:
                list_last_ids = init_first_time(query_list)

            flag_first_time = False

        list_last_ids = call_twitter_slack_apis(query_list, list_last_ids)

        time.sleep(5)
