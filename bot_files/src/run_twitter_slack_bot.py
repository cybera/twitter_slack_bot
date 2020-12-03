#!/usr/bin/env python
import os
import numpy as np
import pandas as pd
from datetime import datetime
import time

from stream_tweets_to_slack import real_time_tweets
from slack_bot import slackbot

if __name__ == "__main__":

    query_file_path = "./twitter_queries.txt"
    init_first_time = True
    init_new_query = False
    bot_id = os.environ.get("SLACK_BOT_ID")
    now = datetime.now()
    timestampnow = datetime.timestamp(now)

    while True:
        if (init_first_time) or (init_new_query):
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

            if init_new_query:
                new_query_list = query_list[tot_size_first_time:]
                tot_size_first_time = len(new_query_list) + tot_size_first_time
                print("Initializing the new queries for the first time")
                for new_query in new_query_list:
                    last_id = real_time_tweets(new_query, first_time=True)
                    if last_id == "Invalid Input":
                        slackbot("post_message", msg="Invalid query try again")
                        list_last_ids = np.append(list_last_ids, "1111111111111111111")
                    else:
                        list_last_ids = np.append(list_last_ids, last_id)

            init_first_time = False
            init_new_query = False


        ind_flag = 0
        for query in query_list:
            if list_last_ids[ind_flag] != "1111111111111111111":
                print(query, list_last_ids[ind_flag])
                last_id = real_time_tweets(query, last_tweet_id=list_last_ids[ind_flag])
                if last_id != list_last_ids[ind_flag]:
                    list_last_ids[ind_flag] = last_id

            ind_flag += 1

        # print("Last refreshed for new tweets at", datetime.datetime.now())

        # Check to see if an user has sent a message
        response = slackbot("retrieve_message", time_stamp=timestampnow)
        df_response = pd.json_normalize(response["messages"])
        if not (df_response.empty):
            df_response = df_response[~df_response["user"].str.contains(bot_id)]
            if not (df_response.empty):
                query_new_list = df_response["text"].tolist()
                user_list = df_response["user"].tolist()
                ts_list = df_response["ts"].tolist()
                timestampnow = ts_list[0]

                for query_new in query_new_list:
                    with open(query_file_path, "a") as queryfile:
                        queryfile.write("\n" + query_new)
                init_new_query = True

        time.sleep(5)
