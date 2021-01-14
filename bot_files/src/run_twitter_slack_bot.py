#!/usr/bin/env python
import os
import numpy as np
from datetime import datetime
import time

from stream_tweets_to_slack import real_time_tweets

if __name__ == "__main__":

    # In container
    # query_file_path = "/app/twitter_queries/twitter_queries.txt"
    # In normal environment
    query_file_path = "twitter_queries/twitter_queries.txt"
    init_first_time = True
    bot_id = os.environ.get("SLACK_BOT_ID")
    now = datetime.now()
    timestampnow = datetime.timestamp(now)

    while True:

        if init_first_time:
            with open(query_file_path, "r") as f:
                query_content = f.readlines()
            query_list = [x.strip() for x in query_content]

            if init_first_time:
                tot_size_first_time = len(query_list)
                list_last_ids = np.array([])
                print("Initializing all queries for the first time")
                for query in query_list:
                    last_id = real_time_tweets(query, first_time=True)
                    list_last_ids = np.append(list_last_ids, last_id)

            init_first_time = False

        ind_flag = 0
        for query in query_list:
            if list_last_ids[ind_flag] != "1111111111111111111":
                print(query, list_last_ids[ind_flag])
                last_id = real_time_tweets(query, last_tweet_id=list_last_ids[ind_flag])
                if last_id != list_last_ids[ind_flag]:
                    list_last_ids[ind_flag] = last_id

            ind_flag += 1

        time.sleep(5)
